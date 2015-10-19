from __future__ import unicode_literals
from mode import stat_mode as sm
import pytest


@pytest.fixture()
def random_mode_list():
    from random import randint
    li = [randint(0, 1000) for num in range(1000)]
    return li


@pytest.fixture()
def fixed_mode_list_dupe():
    li = [100, 100, 44, 44, 23, 12, 12, 1]
    return li


@pytest.fixture()
def fixed_mode_list_unique():
    li = [1000, 1000, 900, 800, 700, 600, 500]
    return li


def test_mode_fixed_dupes(fixed_mode_list_dupe):
    li = fixed_mode_list_dupe
    assert sm(li) == [12, 44, 100]


def test_mode_fixed_uniques(fixed_mode_list_unique):
    li = fixed_mode_list_unique
    assert sm(li) == [1000]


def test_mode_of_tuple():
    li = (1, 2, 3, 4)
    assert sm(li) == [1, 2, 3, 4]


def test_mode_of_dict():
    li = {'a': 'a'}
    with pytest.raises(AttributeError):
        sm(li)
