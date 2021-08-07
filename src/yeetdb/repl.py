#!/usr/bin/env python
from pygments.lexers.sql import SqlLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit import print_formatted_text
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .sql_compiler import QueryExecutor

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


def open_repl(database):
    session = PromptSession(
        history=InMemoryHistory(),
        lexer=PygmentsLexer(SqlLexer),
        completer=sql_completer,
    )
    print_formatted_text("Salutations ! Welcome to YeetDB\n")
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
            qe = QueryExecutor(text)
            result, operation, time = qe.run()
        except Exception as error:
            print_formatted_text(f"ERROR: {error}")
        else:
            if result:
                print_formatted_text(result)
            else:
                print_formatted_text(f"{operation} executed in {round(time, 5)} sec")

    print_formatted_text("\nYeet!")
