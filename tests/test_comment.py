import pytest
from lark import Lark

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.mark.parametrize(
    "text",
    [
        ";",
        "; whatever",
        ";     ",
    ],
)
def test_parse_comment(text: str):
    parser = Lark(
        """
    start: COMMENT
    %import .comment.COMMENT
    """,
        import_paths=[GRAMMAR_FOLDER],
    )
    parser.parse(text)
