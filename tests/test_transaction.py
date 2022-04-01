import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def posting_parser() -> Lark:
    return Lark(
        """
    start: posting
    %import .transaction.posting
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.fixture
def transaction_header_parser() -> Lark:
    return Lark(
        """
        start: transaction_header
        %import .transaction.transaction_header
        %ignore " "
        """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.fixture
def transaction_parser() -> Lark:
    return Lark(
        """
        start: transaction
        %import .transaction.transaction
        %ignore " "
        """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "Assets 10 USD",
        "Assets -10 USD",
        "Assets:Bank -10.0 USD",
        "Assets:Bank -10.0 TWD",
        "Assets:Bank -10.0 TWD ; this is a comment",
        "Assets:Bank -10.0 TWD; this is a comment",
        "Assets:Bank -10.0 TWD @ 2.56 USD",
        "Assets:Bank -10.0 TWD @  2.56  USD",
        "Assets:Bank -10.0 TWD {100.56 USD}",
        "Assets:Bank -10.0 TWD { 100.56 USD }",
        "Assets:Bank -10.0 TWD {{100.56 USD}}",
        "Assets:Bank -10.0 TWD {{ 100.56  USD}}",
        "Assets:Bank -10.0 TWD {100.56 # 12.34 USD}",
        "Assets:Bank -10.0 TWD { 100.56  #  12.34 USD }",
        "Assets:Bank -10.0 TWD {100.56 # 3.45 CAD }",
        "Assets:Bank -10.0 TWD {100.56 USD, 2021-06-07}",
        "Assets:Bank -10.0 TWD {100.56 USD  , 2021-06-07}",
        "Assets:Bank -10.0 TWD { 100.56 USD , 2021-06-07 }",
        "! Assets:Bank -10.0 TWD",
        "* Assets:Bank -10.0 TWD",
    ],
)
def test_parse_posting(posting_parser: Lark, text: str):
    posting_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "Assets 10",
        "A -10 USD",
        "@ Assets:Bank -10.0 TWD",
    ],
)
def test_parse_bad_posting(posting_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        posting_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        '1970-01-01 * "Foobar"',
        '1970-01-01 ! "Foobar"',
        '1970-01-01 ! "Jane Doe" "Foobar"',
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
