import typing
from abc import ABC, abstractmethod
from os import PathLike


class BaseProvider(ABC):
    extensions: typing.List[str]

    @property
    @abstractmethod
    def __dict__(self):
        ...

    @abstractmethod
    def get_section(self, section: str) -> dict:
        ...

    @abstractmethod
    def get_item(self, section: str, variable: str) -> typing.Any:
        ...

    @abstractmethod
    def set_item(self, section: str, variable: str,
                 item: typing.Any) -> typing.Any:
        ...

    @abstractmethod
    def save(self) -> PathLike:
        ...

    @abstractmethod
    def reload(self) -> bool:
        ...
