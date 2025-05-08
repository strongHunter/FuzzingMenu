from typing import Any # TODO: add validation
from string import Template

# Item should be `target name` and `fuzzer` splitted by `-`
# Returns tuple (`target name`, `fuzzer`)
def target_name_parser(item: str) -> tuple[str, str]:
    name, fuzzer = item.rsplit('-')
    return name, fuzzer


class CommandGenerator:
    __global: Any
    __fuzzers: Any

    def __init__(self, config: Any): # TODO: Any
        self.__global = config['global']
        self.__fuzzers = config['fuzzers']

    def create_command(self, item: str) -> str:
        target = self._get_target(item)

        current = target['run'][0]
        cmd = current['cmd']

        # Using `get` because key may not exists
        args = current.get('args') 
        env = current.get('env')

        command = self._cmd_replace_placeholders(cmd, args)
        if env:
            envs_str = ' '.join(env)
            command = f'{envs_str} {command}'
        return command

    def _get_target(self, item: str) -> Any: # TODO: Any
        name, fuzzer = target_name_parser(item)
        fuzzer = self._fuzzer_map(fuzzer)

        return self.__fuzzers[fuzzer][name]

    @staticmethod
    def _fuzzer_map(fuzzer: str) -> str:
        fuzzers = {
            'afl': 'afl',
            'lf': 'libfuzzer'
        }
        return fuzzers[fuzzer]

    def _cmd_replace_placeholders(self, cmd: str, args: str) -> str:
        glob = self.__global
        template = Template(cmd)

        self._cmd_validate_args(cmd, args)
        cmd = template.safe_substitute(
            TARGETS_PATH=glob['targets_path'],
            ARTIFACTS_PATH=glob['artifacts_path'],
            INPUTS_PATH=glob['inputs_path'],
            MUTATORS_PATH=glob['mutators_path'],
            ARGS=args,
        )
        return cmd

    @staticmethod
    def _cmd_validate_args( cmd: str, args: str) -> None:
        if '$ARGS' in cmd and args is None:
            raise ValueError("$ARGS found in command, but 'args' is None!")
        elif '$ARGS' not in cmd and args is not None:
            raise KeyError(f"$ARGS not found in command, but 'args' == {args}")
