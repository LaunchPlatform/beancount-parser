import pytest
from lark import Lark

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def comment_parser() -> Lark:
    return Lark(
        """
    start: COMMENT
    %import .comment.COMMENT
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        ";",
        ";;",
        "; whatever",
        ";; whatever",
        ";     ",
    ],
)
def test_parse_comment(comment_parser: Lark, text: str):
    comment_parser.parse(text)
