from __future__ import unicode_literals
# from mode import stat_mode
import pytest


@pytest.fixture()
def random_mode_list():
    from random import randint
    li = [randint(0, 1000000) for num in range(1000)]
    return li


@pytest.fixture()
def fixed_mode_list_dupe():
    li = [100, 100, 44, 44, 23, 23, 12, 12, 1, 1]
    return li


@pytest.fixture()
def fixed_mode_list_unique():
    li = [1000, 1000, 900, 800, 700, 600, 500]
    return li


def test_mode_fixed_uniques():
    pass


def test_mode_fixed_dupes():
    pass


def test_mode_randoms():
    pass
