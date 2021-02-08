#!/usr/bin/env python
import sys

from pygments.lexers.sql import SqlLexer

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit import print_formatted_text
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from sql_compiler import QueryCompiler

sql_completer = WordCompleter(
    [
        ".t",
        "create",
        "alter",
        "drop",
        "rename",
        "select",
        "insert",
        "update",
        "delete",
        "from",
        "where",
    ],
    ignore_case=True,
)


def main(database):
    session = PromptSession(
        history=InMemoryHistory(),
        lexer=PygmentsLexer(SqlLexer),
        completer=sql_completer,
    )
    print_formatted_text("Salutations\n")
    while True:
        try:
            text = session.prompt(
                f"YeetDB@{database}> ", auto_suggest=AutoSuggestFromHistory()
            )
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.

        try:
            q = QueryCompiler(text)
            message = q.run()
        except Exception as e:
            print(repr(e))
        else:
            print(message)

    print("\nYeet!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        db = ":yeet"
    else:
        db = sys.argv[1]

    main(db)
