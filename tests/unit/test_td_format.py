import logging
import sys
from datetime import timedelta  # noqa: e402

LOGGER = logging.getLogger(__name__)

sys.path.append('./')

from bot_template.utils import td_format  # pylint: disable=import-error


class TestTimeDeltaFormat():
    def test_td_format_en(self):
        formatted = td_format(
            timedelta(days=1, hours=4, minutes=30, seconds=20), "en")
        # LOGGER.info(formatted)
        assert formatted == "1 day, 4 hours, 30 minutes, 20 seconds"

    def test_td_format_ru(self):
        formatted = td_format(
            timedelta(days=2, hours=22, minutes=12, seconds=20), "ru")
        # LOGGER.info(formatted)
        assert formatted == "2 дня, 22 часа, 12 минут, 20 секунд"

    def test_td_format_en_with_ago(self):
        formatted = td_format(
            timedelta(days=1, hours=4, minutes=30, seconds=20), "en", True)
        # LOGGER.info(formatted)
        assert formatted == "1 day, 4 hours, 30 minutes, 20 seconds ago"

    def test_td_format_ru_with_ago(self):
        formatted = td_format(
            timedelta(days=2, hours=22, minutes=12, seconds=20), "ru", True)
        # LOGGER.info(formatted)
        assert formatted == "2 дня, 22 часа, 12 минут, 20 секунд назад"
