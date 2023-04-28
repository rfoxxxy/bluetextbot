import configparser
import typing
from os import PathLike
from pathlib import Path

from bot_template.core.config_manager.providers import BaseProvider
from bot_template.core.config_manager.types.exceptions import \
    InvalidConfigTypeError


class IniProvider(BaseProvider):
    extensions = ["ini"]

    def __init__(self, config_path: str):
        self.config_path = Path(config_path).resolve()
        self.config_type = self.config_path.suffix.lstrip(".")

        if self.config_type not in self.extensions:
            raise InvalidConfigTypeError(
                f"Invalid config type: {self.config_type}")

        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    @staticmethod
    def __format_ini_variable(data: str):
        formatted_data = data

        if data.isdigit():
            formatted_data = int(data)
        elif 0 < data.count(".") < 2 and data.replace(".", "").isdigit():
            formatted_data = float(data)
        elif data in ["yes", "no", "true", "false"]:
            formatted_data = data in ["yes", "true"]
        elif len(data.split(",")) > 1:
            formatted_data = [
                item for item in [
                    IniProvider.__format_ini_variable(var.strip())
                    for var in data.split(",")
                ] if item
            ]

        return formatted_data

    @staticmethod
    def __format_ini(data: dict):
        current_section = data.copy()
        for var in current_section:
            current_section[var] = IniProvider.__format_ini_variable(
                current_section[var])
        return current_section

    @property
    def __dict__(self):
        sections = self.config.sections()
        cfg = {}
        for section in sections:
            _section = dict(self.config.items(section))
            cfg[section] = self.__format_ini(_section)
        return cfg

    def get_section(self, section: str) -> dict:
        """Get dictionary section

        Args:
            section (str): Section name

        Returns:
            dict: Section object
        """
        current_section = dict(self.config.items(section))
        return self.__format_ini(current_section)

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
        self.config.set(section, variable, item)
        return self.config.get(section, variable)

    def save(self) -> PathLike:
        """Save config in file

        Raises:
            InvalidConfigType: invalid config type detected

        Returns:
            PathLike: path to config file
        """
        with open(self.config_path, "w", encoding="utf-8"):
            self.config.write(self)
        return self.config_path

    def reload(self) -> bool:
        """Reload config from file

        Raises:
            InvalidConfigType: invalid config type detected

        Returns:
            bool: status of reload
        """
        self.config.clear()
        self.config.read(self.config_path)
        return True
