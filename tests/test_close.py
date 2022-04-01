import typing
from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def close_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="close", rule="close", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 close Assets",
        "2022-03-31 close Assets:Bank",
        "2022-03-31 close Assets:Bank ; this is a comment",
        dedent(
            """\
        2022-03-31 close Assets:Bank
            foo: "bar"
            egg: #spam
        """
        ),
    ],
)
def test_parse_close(close_parser: Lark, text: str):
    close_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "close Assets",
        "2022-03 close Assets:Bank",
        "2022-03-31 close Assets:Bank USD",
        "2022-03-31 close",
    ],
)
def test_parse_bad_close(close_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        close_parser.parse(text)
