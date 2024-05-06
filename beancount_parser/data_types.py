import enum
import typing

from lark import Tree


@enum.unique
class EntryType(str, enum.Enum):
    # Date directives
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    BALANCE = "BALANCE"
    EVENT = "EVENT"
    COMMODITY = "COMMODITY"
    DOCUMENT = "DOCUMENT"
    PRICE = "PRICE"
    NOTE = "NOTE"
    PAD = "PAD"
    CUSTOM = "CUSTOM"
    TXN = "TXN"
    # Simple directives
    OPTION = "OPTION"
    INCLUDE = "INCLUDE"
    PLUGIN = "PLUGIN"
    # Other
    COMMENTS = "COMMENTS"
    SECTION_HEADER = "SECTION_HEADER"


DATE_DIRECTIVE_ENTRY_TYPES = {
    "open": EntryType.OPEN,
    "close": EntryType.CLOSE,
    "balance": EntryType.BALANCE,
    "event": EntryType.EVENT,
    "commodity": EntryType.COMMODITY,
    "document": EntryType.DOCUMENT,
    "price": EntryType.PRICE,
    "note": EntryType.NOTE,
    "pad": EntryType.PAD,
    "custom": EntryType.CUSTOM,
    "txn": EntryType.TXN,
}
SIMPLE_DIRECTIVE_ENTRY_TYPES = {
    "option": EntryType.OPTION,
    "include": EntryType.INCLUDE,
    "plugin": EntryType.PLUGIN,
}


class Metadata(typing.NamedTuple):
    comments: list[Tree]
    statement: Tree


class Posting(typing.NamedTuple):
    comments: list[Tree]
    statement: Tree
    metadata: list[Metadata]


class Entry(typing.NamedTuple):
    type: EntryType
    comments: typing.List[Tree]
    statement: Tree | None
    metadata: typing.List[Metadata]
    postings: typing.List[Posting]
