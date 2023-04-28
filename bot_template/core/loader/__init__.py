import glob
import os
from importlib import import_module
from os.path import basename, isdir, isfile
from typing import List

from loguru import logger

from bot_template.core.config_manager import ConfigManager


class ModuleLoader:
    __slots__ = ["project_name", "is_prod", "config", "supported_modules"]

    def __init__(self, project_name: str, is_prod: bool,
                 config: ConfigManager) -> None:
        logger.info(f"Initializing {project_name} modloader...")
        self.project_name = project_name
        self.is_prod = is_prod
        self.config = config
        self.supported_modules = self.config.get_item("core",
                                                      "supported_modules")

    def __list_all_modules(self, abs_path: str) -> List[str]:
        """List all modules of package

        Args:
            abs_path (str): absolute path of package

        Returns:
            List[str]: list of modules
        """
        py_mod_paths = glob.glob(abs_path + "/*.py")
        dir_mod_paths = glob.glob(abs_path + "/*/")
        all_py_modules = [
            basename(f)[:-3] for f in py_mod_paths if isfile(f)
            and f.endswith(".py") and not f.endswith("__init__.py")
            and not (basename(f)[:-3].startswith("_") and self.is_prod)
            and not ("database" in f
                     and not self.config.get_item("features", "use_database"))
            and not ("sentry" in f
                     and not self.config.get_item("features", "use_sentry"))
        ]
        all_dir_modules = [
            basename(f[:-1]) for f in dir_mod_paths
            if isdir(f[:-1]) and not f[:-1].endswith(".py/")
            and not f[:-1].endswith("__pycache__")
            and not (basename(f[:-1]).startswith("_") and self.is_prod)
        ]
        return sorted(
            [module for module in all_py_modules + all_dir_modules if module])

    def get_loadable(self) -> List[str]:
        """Get loadable modules

        Returns:
            List[str]: list of loadable modules
        """
        return [
            x for x in self.supported_modules
            if os.path.isdir(f'{self.project_name}/{x}')
        ]

    def load_module(self, project: str, package: str, module: str):
        """Load module

        Args:
            project (str): project directory
            package (str): package name
            module (str): module name
        """
        import_module(f"{project}.{package}.{module}")
        logger.info(
            f"Loaded {package.rstrip('s')} {project}.{package}.{module}")

    def load_all(self):
        """Load all loadable modules
        """
        logger.info(f"Loading all {self.project_name} modules...")
        for package in self.get_loadable():
            _package_modules = self.__list_all_modules(
                os.path.abspath(f"{self.project_name}/{package}"))
            logger.info(
                f"{package.capitalize()} to load: {', '.join(_package_modules)}"
            )
            for module in _package_modules:
                self.load_module(self.project_name, package, module)
        logger.info("All modules loaded! Ready for startup!")
