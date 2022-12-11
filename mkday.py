from pathlib import Path
from typing import cast
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("DAY", type=Path)
    args = parser.parse_args()

    d = cast(Path, args.DAY)
    d.mkdir()
    for fname in ("__init__.py", "_input.py", "__main__.py"):
        (d / fname).touch()



if __name__ == "__main__":
    main()