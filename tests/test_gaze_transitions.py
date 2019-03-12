import pytest
from ..transition_matrix.gazetransitions import *
from ..transition_matrix.aoi import *
import numpy as np


TEST_SCREENDIM = [1920, 1200]
TEST_RADIUS = 100
TEST_VERTICES_1 = [[20, 20], [400, 250], [40, 400]]
TEST_VERTICES_2 = [[800, 800], [1000, 800], [700, 650]]

TEST_AOI_DICT = {
    'aoi_poly1': PolyAOI(TEST_SCREENDIM, TEST_VERTICES_1),
    'aoi_circle2': CircleAOI(TEST_SCREENDIM, TEST_RADIUS, center=[500, 500]),
    'aoi_poly2': PolyAOI(TEST_SCREENDIM, TEST_VERTICES_2)
}


TEST_GAZE_ARRAY = np.array([
    [41, 41, 0],
    [80, 80, 0],
    [501, 501, 0],
    [100, 200, 0],
    [1002, 1002, 0],
    [400, 400, 0],
    [200, 200, 0],
    [250, 250, 0],
    [540, 540, 0]])



@pytest.fixture
def setup_transition(request):
    return GazeTransitions(TEST_SCREENDIM, TEST_AOI_DICT, TEST_GAZE_ARRAY)


def test_prob(setup_transition):
    assert(setup_transition.get_prob_aoi('aoi_poly1') ==
           5 / 9), 'wrong probability result'

def test_transitions(setup_transition):
    assert(setup_transition.get_transition_matrix().loc['aoi_poly1','aoi_poly1'] == 2.0),'Wong transition result'
    assert(setup_transition.get_transition_matrix().loc['aoi_poly1','aoi_circle2'] == 2.0),'Wong transition result'
    assert(setup_transition.get_transition_matrix().loc['aoi_circle2','aoi_poly1'] == 1.0),'Wong transition result'


def test_points_outside(setup_transition):
    assert (setup_transition.points_outside_aoi == 2),'wrong outside points detection'
