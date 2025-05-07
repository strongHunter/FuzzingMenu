from typing import Any # TODO: add validation

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
        return f'echo "Hello, {item}!"' # TODO

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
