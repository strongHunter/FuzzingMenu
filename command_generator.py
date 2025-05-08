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
        cmd = target['run'][0]['cmd']
        return self._cmd_replace_placeholders(cmd)

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

    def _cmd_replace_placeholders(self, cmd: str) -> str:
        glob = self.__global
        template = Template(cmd)

        return template.safe_substitute(
            TARGETS_PATH=glob['targets_path'],
            ARTIFACTS_PATH=glob['artifacts_path'],
            INPUTS_PATH=glob['inputs_path'],
            MUTATORS_PATH=glob['mutators_path'],
        )
