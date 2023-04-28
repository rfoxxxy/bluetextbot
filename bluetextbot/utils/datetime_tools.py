from datetime import timedelta


def td_format(td_object: timedelta,
              language: str = "ru",
              add_ago: bool = False) -> str:
    """Format timedelta as "ago" string

    Args:
        td_object (timedelta): timedelta object

    Returns:
        str: formatted string
    """
    seconds = int(td_object.total_seconds())
    strings = []
    match language:
        case "ru":
            _ago = "назад"
            periods = [
                (('год', 'года', 'лет'), 60 * 60 * 24 * 365),
                (('месяц', 'месяца', 'месяцев'), 60 * 60 * 24 * 30),
                (('день', 'дня', 'дней'), 60 * 60 * 24),
                (('час', 'часа', 'часов'), 60 * 60),
                (('минуту', 'минуты', 'минут'), 60),
                (('секунду', 'секунды', 'секунд'), 1)
            ]

            for _period_name, period_seconds in periods:
                if seconds >= period_seconds:
                    period_value, seconds = divmod(seconds, period_seconds)
                    period_name = _period_name[0] if period_value == 1 \
                        else _period_name[1] if str(period_value)[-1] in ["2", "3", "4"] and (len(str(period_value)) < 2 or
                                                                                              str(period_value)[-2] != "1") \
                        else _period_name[2]
                    strings.append(f"{period_value} {period_name}")

        case "en":
            _ago = "ago"
            periods = [('year', 60 * 60 * 24 * 365),
                       ('month', 60 * 60 * 24 * 30),
                       ('day', 60 * 60 * 24),
                       ('hour', 60 * 60),
                       ('minute', 60),
                       ('second', 1)]

            for period_name, period_seconds in periods:
                if seconds >= period_seconds:
                    period_value, seconds = divmod(seconds, period_seconds)
                    has_s = 's' if period_value > 1 else ''
                    strings.append(f"{period_value} {period_name}{has_s}")
        case _:
            return td_format(td_object, "en", add_ago)

    return ", ".join(strings) + (f" {_ago}" if add_ago else "")
