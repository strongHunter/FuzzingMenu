from typing import Any # TODO: add validation

class CommandGenerator:
    __config: Any

    def __init__(self, config: Any): # TODO: Any
        self.__config = config

    def create_command(self, item: str) -> str:
        return f'echo "Hello, {item}!"' # TODO
