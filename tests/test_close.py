import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def close_parser() -> Lark:
    return Lark(
        """
    start: close
    %import .close.close
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 close Assets",
        "2022-03-31 close Assets:Bank",
        "2022-03-31 close Assets:Bank ; this is a comment",
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
