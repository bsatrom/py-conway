import pytest

import os
import sys
sys.path.insert(0, os.path.abspath(
                   os.path.join(os.path.dirname(__file__), '..')))

from py_conway import PseudoEnum  # nopep8


def test_valid_pseudo_enum():
    my_enum = PseudoEnum(['ONE', 'TWO'])

    assert my_enum.ONE == 'ONE'


def test_valid_pseudo_enum_bad_call():
    with pytest.raises(AttributeError):
        my_enum = PseudoEnum(['ONE', 'TWO'])
        my_enum.THREE
