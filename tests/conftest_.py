# conftest.py

import sys


def pytest_configure(config):
    root_dir = "/path/to/the/project"
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
