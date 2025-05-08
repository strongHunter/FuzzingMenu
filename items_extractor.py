from abc import ABC, abstractmethod

class ItemsProvider(ABC):
    @abstractmethod
    def items(self) -> list[str]:
        pass

class StubTargetsExtractor(ItemsProvider):
    def items(self) -> list[str]:
        return ['target_1-afl', 'target_2-afl', 'target_3-afl', 'target_1-lf', 'target_2-lf']
