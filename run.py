from importlib import import_module
import cProfile
import sys

if __name__ == "__main__":
    assert len(sys.argv) == 2
    cProfile.run('import_module(f"{sys.argv[1]}.__main__")')
