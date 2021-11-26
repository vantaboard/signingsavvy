import os
from curses import wrapper

import pytest
from pysign import start


def test_make_asset_dirs():
  os.chdir('tests')
  with pytest.raises(SystemExit) as e:
    start.make_asset_dirs()
    assert e.value.code == 0
