import pytest
from .aoi import *

TEST_X = 60
TEST_Y = 100
TEST_SCREENDIM = [1920, 1200]
TEST_RADIUS = 60
TEST_VERTICES = [[ 50,50] , [100,100], [40,200]]
TEST_CENTER_PASS = [50, 50]
TEST_CENTER_FAIL = [-1, 50]


@pytest.fixture
def setup_poly(request):
    return PolyAOI(TEST_SCREENDIM, TEST_VERTICES)


def test_contain(setup_poly):
    assert ([TEST_X, TEST_Y]
            in setup_poly), 'wrong answer for checking contains method in poly'


@pytest.fixture
def setup_circle(request):
    return CircleAOI(TEST_SCREENDIM, TEST_RADIUS, TEST_CENTER_PASS)


def test_contains_circle(setup_circle):
    assert ([TEST_X, TEST_Y]
            in setup_circle), 'wrong answer for checking contains method in circle'


def test_center_circle():
    with pytest.raises(Exception) as e_info:
        CircleAOI(TEST_SCREENDIM, TEST_RADIUS, TEST_CENTER_FAIL)
