import pytest
from lark import Lark

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


@pytest.mark.parametrize(
    "text",
    [
        "Assets 10 USD",
        "Assets -10 USD",
        "Assets:Bank -10 USD",
    ],
)
def test_parse_posting(posting_parser: Lark, text: str):
    posting_parser.parse(text)
