import typing
from os import PathLike
from pathlib import Path

import toml

from bot_template.core.config_manager.providers import BaseProvider
from bot_template.core.config_manager.types.exceptions import \
    InvalidConfigTypeError


class TomlProvider(BaseProvider):
    extensions = ["toml"]

    def __init__(self, config_path: str):
        self.config_path = Path(config_path).resolve()
        self.config_type = self.config_path.suffix.lstrip(".")

        if self.config_type not in self.extensions:
            raise InvalidConfigTypeError(
                f"Invalid config type: {self.config_type}")

        self.config = toml.load(self.config_path)

    @property
    def __dict__(self):
        return self.config

    def get_section(self, section: str) -> dict:
        """Get dictionary section

        Args:
            section (str): Section name

        Returns:
            dict: Section object
        """
        current_section = self.config
        for _section in section.split("."):
            current_section = current_section.get(_section, {})
        return current_section

    def get_item(self, section: str, variable: str) -> typing.Any:
        """Get dictionary item by it's section and name

        Args:
            section (str): Section name
            variable (str): Item name

        Returns:
            typing.Any: Item
        """
        return self.get_section(section).get(variable)

    def set_item(self, section: str, variable: str,
                 item: typing.Any) -> typing.Any:
        """Set dictionary item by it's section and var name

        Args:
            section (str): section name
            variable (str): variable name
            item (A): item to be setted

        Returns:
            typing.Any: setted item
        """
        current_section = self.config
        sections = section.split('.')
        for _section in sections:
            current_section = current_section.setdefault(_section, {})
        current_section[variable] = item
        return current_section[variable]

    def save(self) -> PathLike:
        """Save config in file

        Raises:
            InvalidConfigType: invalid config type detected

        Returns:
            PathLike: path to config file
        """
        with open(self.config_path, "w", encoding="utf-8") as file:
            toml.dump(self.config, file)
        return self.config_path

    def reload(self) -> bool:
        """Reload config from file

        Raises:
            InvalidConfigType: invalid config type detected

        Returns:
            bool: status of reload
        """
        self.config = toml.load(self.config_path)
        return True
