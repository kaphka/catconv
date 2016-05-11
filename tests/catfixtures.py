import pytest
import os
import os.path as op

@pytest.fixture
def page():
    return {'path': 'SD_png/SD001/00000001.png'}

@pytest.fixture
def unconv_catalog_dir(tmpdir, request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    unconv = op.join(test_dir, 'SD')
    return unconv
