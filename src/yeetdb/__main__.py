import sys
from .repl import open_repl

if __name__ == "__main__":
    if len(sys.argv) < 2:
        db = ":yeet"
    else:
        db = sys.argv[1]

    open_repl(db)
