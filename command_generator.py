from typing import Any # TODO: add validation

class CommandGenerator:
    __global: Any
    __fuzzers: Any

    def __init__(self, config: Any): # TODO: Any
        self.__global = config['global']
        self.__fuzzers = config['fuzzers']

    def create_command(self, item: str) -> str:
        return f'echo "Hello, {item}!"' # TODO
