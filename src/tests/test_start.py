import os

import pytest

from pysign import start


def test_make_dirs() -> None:
  """Tests making directories using the start module.

  :return: no value
  :rtype: none
  """

  os.chdir("../tests")
  with pytest.raises(SystemExit) as e:
    start.make_dirs()
    assert e.value.code == 0
