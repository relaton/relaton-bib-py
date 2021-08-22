import datetime
import dataclasses
import re


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
