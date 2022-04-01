from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def document_parser() -> Lark:
    return Lark(
        """
    start: document
    %import .document.document
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        '2022-03-31 document Assets "/path/to/the/file.pdf"',
        '2022-03-31 document Assets "/path/to/the/file.pdf" ; this is a comment',
        '2022-03-31 document Assets "/path/to/the/file.pdf"',
        dedent(
            """\
        2022-03-31 document Assets "/path/to/the/file.pdf"
            foo: "bar"
            egg: #spam
        """
        ),
    ],
)
def test_parse_document(document_parser: Lark, text: str):
    document_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'document Assets "this account looks good"',
        "2022-03-31 document Assets",
    ],
)
def test_parse_bad_document(document_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        document_parser.parse(text)
