import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def commodity_parser() -> Lark:
    return Lark(
        """
    start: commodity
    %import .commodity.commodity
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 commodity USD",
        "2022-03-31 commodity BTC ; this is a comment",
        "2022-03-31 commodity BTC ; this is a comment",
    ],
)
def test_parse_commodity(commodity_parser: Lark, text: str):
    commodity_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "commodity Assets",
        "2022-03-1 commodity Assets:Bank",
        "2022-03 commodity USD",
        "2022-03-31 commodity Assets:Bank ",
    ],
)
def test_parse_bad_commodity(commodity_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        commodity_parser.parse(text)
