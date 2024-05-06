from lark import Token
from lark import Tree

from .data_types import DATE_DIRECTIVE_ENTRY_TYPES
from .data_types import Entry
from .data_types import EntryType
from .data_types import Metadata
from .data_types import Posting
from .data_types import SIMPLE_DIRECTIVE_ENTRY_TYPES


def get_entry_type(statement: Tree) -> EntryType:
    first_child: Tree = statement.children[0]
    if first_child.data == "date_directive":
        return DATE_DIRECTIVE_ENTRY_TYPES[first_child.children[0].data.value]
    elif first_child.data == "simple_directive":
        return SIMPLE_DIRECTIVE_ENTRY_TYPES[first_child.children[0].data.value]
    else:
        raise ValueError(f"Unexpected first child type {first_child.data}")


def collect_entries(tree: Tree) -> tuple[list[Entry], list[Tree]]:
    entries: list[Entry] = []
    comments: list[Tree] = []
    for statement in tree.children:
        if statement is None:
            continue
        if statement.data != "statement":
            raise ValueError("Expected statement here")
        first_child = statement.children[0]
        if isinstance(first_child, Token):
            if first_child.type == "COMMENT":
                comments.append(statement)
            elif first_child.type == "SECTION_HEADER":
                entry = Entry(
                    type=EntryType.SECTION_HEADER,
                    comments=comments,
                    statement=statement,
                    metadata=[],
                    postings=[],
                )
                entries.append(entry)
                comments = []
            else:
                raise ValueError(f"Unexpected token {first_child.type}")
        else:
            if first_child.data == "posting":
                last_entry = entries[-1]
                if last_entry.type != EntryType.TXN:
                    raise ValueError("Transaction expected")
                last_entry.postings.append(
                    Posting(comments=comments, statement=statement, metadata=[])
                )
                comments = []
                continue
            elif first_child.data == "metadata_item":
                last_entry = entries[-1]
                metadata = Metadata(comments=comments, statement=statement)
                if last_entry.postings:
                    last_posting: Posting = last_entry.postings[-1]
                    last_posting.metadata.append(metadata)
                else:
                    last_entry.metadata.append(metadata)
                comments = []
                continue
            entry = Entry(
                type=get_entry_type(statement),
                comments=comments,
                statement=statement,
                metadata=[],
                postings=[],
            )
            entries.append(entry)
            comments = []
    return entries, comments
