import os
from pathlib import Path
from distutils import dir_util
import pytest


@pytest.fixture
def datadir(tmpdir, request):
    filepath = request.module.__file__
    test_dir = Path(filepath).parent.absolute() / "templates"

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir
