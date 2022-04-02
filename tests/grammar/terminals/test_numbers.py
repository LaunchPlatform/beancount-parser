import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def number_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="numbers", rule="NUMBER")


@pytest.fixture
def signed_number_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="numbers", rule="SIGNED_NUMBER")


@pytest.mark.parametrize(
    "text",
    [
        "1",
        "12",
        "123",
        "1234",
        "4578",
        "4,578",
        "4,578.1234",
        "1,123,578.1234",
        "12.34",
        ".34",
        "0.0",
    ],
)
def test_parse_number(number_parser: Lark, text: str):
    number_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "-0",
        "1000,000",
        "1000,00",
        "1,0000",
        "+1234",
        "-5.67",
        "4578.123.45",
        "0x12.34",
        "..34",
        "0.0.",
        "abc",
    ],
)
def test_parse_bad_number(number_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        number_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "0",
        "1234",
        "4578",
        "12.34",
        "12.34",
        ".34",
        "0.0",
        "-5",
        "-5.67",
        "+5.67",
    ],
)
def test_parse_signed_number(signed_number_parser: Lark, text: str):
    signed_number_parser.parse(text)


@pytest.mark.parametrize("text", ["0a", "1234..", "..4578", "12..34", "abc"])
def test_parse_bad_signed_number(signed_number_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        signed_number_parser.parse(text)
