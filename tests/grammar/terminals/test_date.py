import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters


@pytest.fixture
def date_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="date", rule="DATE")


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31",
        "1970-01-01",
        "2022/03/31",
        "1970/01/01",
        "2022-03/31",
        "20222-03-31",
        "1970-1-01",
        "1970-1-1",
    ],
)
def test_parse_date(date_parser: Lark, text: str):
    date_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "2022--01"
        "foobar",
    ],
)
def test_parse_invalid_date(date_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        date_parser.parse(text)
