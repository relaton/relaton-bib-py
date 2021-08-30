import datetime
import dataclasses
import re

from .localized_string import LocalizedString


class RequestError(Exception):
    pass


def parse_date(date, str_res=True):
    """Convert date from string to date or string
    """

    if date is datetime.datetime:
        return date

    cases = [
        # February 2012
        (r"(?P<date>\w+\s\d{4})", "%B %Y", "%Y-%m"),
        # February 11, 2012
        (r"(?P<date>\w+\s\d{1,2},\s\d{4})", "%B %d, %Y", "%Y-%m-%d"),
        # 2012-02-11
        (r"(?P<date>\d{4}-\d{2}-\d{2})", "%Y-%m-%d", None),
        # 2012-02
        (r"(?P<date>\d{4}-\d{2})", "%Y-%m", None),
        # 2012
        (r"(?P<date>\d{4})", "%Y", None),
    ]

    for regexp, strp, strf in cases:
        m = re.match(regexp, str(date))
        if m:
            value = m.group("date")
            d = datetime.datetime.strptime(value, strp)
            if strf:
                return d.strftime(strf) if str_res else d
            else:
                return value if str_res else d.strftime(strp)


# TODO we don't need this for python probably
# @param array [Array]
# @return [Array<String>, String]
def single_element_array(array):
    if len(array) > 1:
        return map(lambda x: x if x is str else dataclasses.asdict(x), array)
    else:
        return array[0] if array[0] is str else dataclasses.asdict(array[0])


def lang_filter(target, opts={}):
    filtered = list(filter(lambda t: opts.get("lang") in t.language, target))
    return filtered if filtered else target


def localized_string(s):
    if isinstance(s, dict):
        return LocalizedString(**s)
    elif isinstance(s, str):
        return LocalizedString(s)
    elif isinstance(s, LocalizedString):
        return s
    else:
        ValueError(f"don't know how to convert {type(s)}")


def to_ds_instance(klass, fail=False):
    def f(x):
        if isinstance(x, klass):
            return x
        elif isinstance(x, dict):
            return klass(**x)
        elif isinstance(x, str):
            return klass(x)
        elif fail:
            ValueError(f"Unknown how to conver {type(x).__name__} to {klass}")
        else:
            return x
    return f


def delegate(to, *methods):
    """https://stackoverflow.com/a/55563139/902217"""
    def dec(klass):
        def create_delegator(method):
            def delegator(self, *args, **kwargs):
                obj = getattr(self, to)
                m = getattr(obj, method)
                return m(*args, **kwargs)
            return delegator
        for m in methods:
            setattr(klass, m, create_delegator(m))
        return klass
    return dec
