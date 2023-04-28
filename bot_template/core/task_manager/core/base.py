from abc import ABC, abstractmethod


class BaseCoreTask(ABC):
    name: str

    def __repr__(self) -> str:
        return f'<CoreTask name={self.name} at {hex(id(self))}>'  # yapf: disable

    @abstractmethod
    async def run_task(self):
        ...
