import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def metadata_key_parser() -> Lark:
    return Lark(
        """
    start: METADATA_KEY
    %import .metadata.METADATA_KEY
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.fixture
def metadata_value_parser() -> Lark:
    return Lark(
        """
    start: metadata_value
    %import .metadata.metadata_value
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


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
    ],
)
def test_parse_metadata_key(metadata_value_parser: Lark, text: str):
    metadata_value_parser.parse(text)


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
def test_parse_bad_metadata_key(metadata_value_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        metadata_value_parser.parse(text)
