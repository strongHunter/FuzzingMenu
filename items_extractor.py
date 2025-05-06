from abc import ABC, abstractmethod

class ItemsProvider(ABC):
    @abstractmethod
    def items(self) -> list[str]:
        pass

class StubTargetsExtractor(ItemsProvider):
    def items(self) -> list[str]:
        return ['target_1-afl.elf', 'target_2-afl.elf', 'target_3-afl.elf', 'target_1-lf.elf', 'target_2-lf.elf']
