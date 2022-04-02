import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def include_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="include", rule="include", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        'include "/path/to/file.bean"',
        'include "/path/to/file.bean" ; this is a comment',
    ],
)
def test_parse_include(include_parser: Lark, text: str):
    include_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'INCLUDE "/path/to/file.bean"',
        "include '/path/to/file.bean'" "include /path/to/file.bean",
    ],
)
def test_parse_bad_include(include_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        include_parser.parse(text)
