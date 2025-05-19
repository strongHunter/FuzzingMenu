from abc import ABC, abstractmethod

class ItemsProvider(ABC):
    @abstractmethod
    def items(self) -> list[str]:
        pass


import os
import magic
from collections.abc import Callable

class BinaryExecutableExtractor(ItemsProvider):
    __directory: str

    def __init__(self, directory: str):
        self.__directory = directory
        super().__init__()

    def items(self) -> list[str]:
        return self.find_elf_executables(self.__directory, self.is_elf_executable)
    
    @staticmethod
    def find_elf_executables(directory: str, filter_func: Callable[[str], bool]) -> list[str]:
        elf_executables = []
        for root, _, files in os.walk(directory):
            for name in files:
                full_path = os.path.join(root, name)
                if filter_func(full_path):
                    elf_executables.append(full_path)
        return elf_executables

    @staticmethod
    def is_elf_executable(path: str) -> bool:
        try:
            file_type = magic.from_file(path)
            return "ELF" in file_type and "executable" in file_type
        except Exception:
            return False
