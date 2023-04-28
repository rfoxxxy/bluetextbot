from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs):
        if AbstractDataclass in (cls, cls.__bases__[0]):
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)


@dataclass(slots=True)
class BaseKeyboardButton(AbstractDataclass):  # pylint: disable=too-many-instance-attributes
    """Base button object
    """
    type: str
    text: str
    callback_data: str = field(default=None)
    url: str = field(default=None)
    switch_inline_query: str = field(default=None)
    poll_type: str = field(default=None)
    user_id: int = field(default=None)
    additional_data: dict = field(default=None)

    def __repr__(self) -> str:
        return f'<KeyboardButton type={self.type} text={self.text} at {hex(id(self))}>'  # yapf: disable

    @abstractmethod
    async def build_button(self, ctx):
        ...


@dataclass(init=False, slots=True)
class ButtonRow:
    buttons: List[BaseKeyboardButton]

    def __init__(self, *args: BaseKeyboardButton):
        self.buttons = list(args)

    def append(self, button: BaseKeyboardButton) -> None:
        self.buttons.append(button)

    def __repr__(self) -> str:
        return f'<ButtonRow object at {hex(id(self))}>'  # yapf: disable
