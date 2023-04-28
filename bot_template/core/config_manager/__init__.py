import typing
from os import PathLike
from pathlib import Path

from bot_template.core.config_manager.providers import (BaseProvider,
                                                        IniProvider,
                                                        TomlProvider)
from bot_template.core.config_manager.types.exceptions import \
    InvalidConfigTypeError


class ConfigManager():
    def __init__(self, config: BaseProvider | str, create: bool = False):
        if not isinstance(config, BaseProvider):
            self.config_path = Path(config).resolve()
            self.config_type = self.config_path.suffix.lstrip(".")
            if not self.config_path.exists() and Path("tests/e-config.toml").resolve().exists() and create:
                with open(self.config_path, "x", encoding="utf-8") as writable:
                    with open("tests/e-config.toml", "r", encoding="utf-8") as readable:
                        writable.write(readable.read())
            match self.config_type:
                case "toml":
                    self.config_instance = TomlProvider(self.config_path)
                case "ini":
                    self.config_instance = IniProvider(self.config_path)
                case _:
                    raise InvalidConfigTypeError(f"Invalid config type: {self.config_type}")
        else:
            self.config_instance = config
            self.config_path = self.config_instance.config_path
            self.config_type = self.config_instance.config_type

    @property
    def __dict__(self):
        return self.config_instance.__dict__

    def get_section(self, section: str) -> dict:
        """Get dictionary section

        Args:
            section (str): Section name

        Returns:
            dict: Section object
        """
        return self.config_instance.get_section(section)

    def get_item(self, section: str, variable: str) -> typing.Any:
        """Get dictionary item by it's section and name

        Args:
            section (str): Section name
            variable (str): Item name

        Returns:
            typing.Any: Item
        """
        return self.config_instance.get_item(section, variable)

    def set_item(self, section: str, variable: str, item: typing.Any) -> typing.Any:
        """Set dictionary item by it's section and var name

        Args:
            section (str): section name
            variable (str): variable name
            item (A): item to be setted

        Returns:
            typing.Any: setted item
        """
        return self.config_instance.set_item(section, variable, item)

    def save(self) -> PathLike:
        """Save config in file

        Raises:
            InvalidConfigType: invalid config type detected

        Returns:
            PathLike: path to config file
        """
        return self.config_instance.save()

    def reload(self) -> bool:
        """Reload config from file

        Raises:
            InvalidConfigType: invalid config type detected

        Returns:
            bool: status of reload
        """
        return self.config_instance.reload()
