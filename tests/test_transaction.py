import typing
from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def transaction_header_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(
        module="transaction", rule="transaction_header", ignore_spaces=True
    )


@pytest.fixture
def transaction_body_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(
        module="transaction", rule="transaction_body", ignore_spaces=True
    )


@pytest.fixture
def transaction_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="transaction", rule="transaction", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "1970-01-01",
        '1970-01-01 * "Foobar"',
        '1970-01-01 ! "Foobar"',
        '1970-01-01 ! "\\"Foobar\\""',
        '1970-01-01 ! "Jane Doe" "Foobar"',
        '1970-01-01 ! "Jane Doe" "Foobar" #hash-tag',
        '1970-01-01 ! "Jane Doe" "Foobar" #hash-tag ^link',
        '1970-01-01 ! "Jane Doe" "Foobar" #hash-tag ^link-1 #hash2',
        '1970-01-01 * "Jane Doe" "Foobar" ; this is a comment',
        '1970-01-01 txn "Jane Doe" "Foobar"',
    ],
)
def test_parse_transaction_header(transaction_header_parser: Lark, text: str):
    transaction_header_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        '1970-01-01 @ "Foobar"',
        "1970-01-01 ! Foobar",
        '1970-01-01 ! "Jane Doe" Foobar',
        '1970-01-01 TXN "Jane Doe" "Foobar"',
        'TXN "Jane Doe" "Foobar"',
    ],
)
def test_parse_bad_transaction_header(transaction_header_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        transaction_header_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "\n Assets  10 USD",
        "\n "
        + "\n ".join(
            [
                "Assets 123.0 USD ; this is a comment",
                'foo: "bar"',
                "eggs: 2021-01-01 ; this is a metadata",
                "Income -123.0 USD @ 456.0 CAD",
            ]
        ),
    ],
)
def test_parse_transaction_body(transaction_body_parser: Lark, text: str):
    transaction_body_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        dedent(
            """\
        1970-01-01 * "Foobar"
            Assets  10 USD
            Income -10 USD
        """
        ),
        dedent(
            """\
        1970-01-01 * "Foobar"
            Assets  10 USD
            Income
        """
        ),
        dedent(
            """\
        1970-01-01 * "Foobar" ; header
            Assets  10 USD ; posting body
            Income -10 USD ; posting body
        """
        ),
        dedent(
            """\
        1970-01-01 * "Foobar"
            statement: "foobar.pdf"
            Assets  10 USD
                item: "item name" ; this is fine
            Income -10 USD
        """
        ),
        dedent(
            """\
        1970-01-01 * "Foobar" #my-hash-tag ^travel #second ^second
            Assets  10 USD
            Income -10 USD
        """
        ),
    ],
)
def test_parse_transaction(transaction_parser: Lark, text: str):
    transaction_parser.parse(text)
