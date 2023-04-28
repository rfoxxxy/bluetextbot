import os
import sys

import pytest

os.environ["DISABLE_UVLOOP"] = "True"

sys.path.append('./')

from bot_template.core.config_manager import (  # pylint: disable=import-error
    ConfigManager, IniProvider, TomlProvider)


def get_config_manager_id(fixture_value):
    return f'ConfigManager({fixture_value.config_path.name})'


@pytest.fixture(scope="session",
                params=[
                    ConfigManager(TomlProvider("tests/e-config.toml")),
                    ConfigManager(IniProvider("tests/e-config.ini"))
                ],
                ids=get_config_manager_id)
def config_manager(request):
    return request.param
