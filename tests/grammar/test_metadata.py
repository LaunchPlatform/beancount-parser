import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters


@pytest.fixture
def metadata_key_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="METADATA_KEY")


@pytest.fixture
def metadata_value_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="metadata_value", ignore_spaces=True)


@pytest.fixture
def metadata_item_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="metadata_item", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "a",
        "abc",
        "abc-DEF",
        "abc_DEF",
        "abc123",
        "aBC",
    ],
)
def test_parse_metadata_key(metadata_key_parser: Lark, text: str):
    metadata_key_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "0",
        "0abc",
        "Abc",
        "_abc",
        "_ABC",
        "_Abc",
    ],
)
def test_parse_bad_metadata_key(metadata_key_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        metadata_key_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        '"String value"',
        "2020-03-31",
        "12.34",
        "12.34 USD",
        "USD",
        "#foobar",
        "#foo #bar",
    ],
)
def test_parse_metadata_value(metadata_value_parser: Lark, text: str):
    metadata_value_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "abc",
        "_abc",
        "_ABC",
        "_Abc",
    ],
)
def test_parse_bad_metadata_value(metadata_value_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        metadata_value_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'foo: "String value"',
        "bar: 2020-03-31",
        "eggs: 12.34",
    ],
)
def test_parse_metadata_item(metadata_item_parser: Lark, text: str):
    metadata_item_parser.parse(text)
