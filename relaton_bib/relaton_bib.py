import datetime
import dataclasses


class RequestError(Exception):
    pass


def parse_date(date, str_res=True):
    """Convert date from string to date or string
    """

    if date is datetime.datetime:
        return date

    cases = [
        # February 2012
        (r"(?<date>\w+\s\d{4})", "%B %Y", "%Y-%m"),
        # February 11, 2012
        (r"(?<date>\w+\s\d{1,2},\s\d{4})", "%B %d, %Y", "%Y-%m-%d"),
        # 2012-02-11
        (r"(?<date>\d{4}-\d{2}-\d{2})", "%Y-%m-%d", None),
        # 2012-02
        (r"(?<date>\d{4}-\d{2})", "%Y-%m", None),
        # 2012
        (r"(?<date>\d{4})", "%Y", None),
    ]

    for regexp, strp, strf in cases:
        m = re.match(regexp, str(date)).group("date")
        if m:
            d = datetime.strptime(m, strp)
            if strf:
                return d.strftime(strf) if str_res else d
            else:
                return m if str_res else d.strptime(strp)


# @param array [Array]
# @return [Array<String>, String]
def single_element_array(array):
    if len(array) > 1:
        return map(lambda x: x if x is str else dataclasses.asdict(x), array)
    else:
        return array[0] if array[0] is str else dataclasses.asdict(array[0])
