from .eyesmetriccalculator import EyesMetricCalculator
from .transition_matrix import *

import numpy as np
import pytest


TEST_ARRAY = np.array([[0, 0], [100, 50], [78, 31]])
TEST_SCREENDIM = (100, 50)
TEST_SCREENDIM_2 = (1920, 1200)
TEST_CELLX = 50
TEST_CELLY = 10
TEST_RADIUS = 100
TEST_VERTICES_1 = [[ 20,20] , [400,250], [40,400]]
TEST_VERTICES_2 = [[800,800], [1000,800], [700,650]]

TEST_TRAN_PROB = np.array([[0.78, 0.06, 0.16],
                           [0.18, 0.46, 0.36],
                           [0.15, 0.09, 0.76]
                           ])

TEST_STAT_PROB = np.array([0.42, 0.14, 0.44
                           ])


TEST_AOI_DICT = {
                'aoi_poly1': PolyAOI(TEST_SCREENDIM_2,TEST_VERTICES_1),
                'aoi_circle2': CircleAOI(TEST_SCREENDIM_2, TEST_RADIUS, center=[500,500]),
                'aoi_poly2': PolyAOI(TEST_SCREENDIM_2,TEST_VERTICES_2)
                }


GAZE_ARRAY = np.array([
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
def valid_calc(request):
    return EyesMetricCalculator(TEST_ARRAY,GAZE_ARRAY, TEST_SCREENDIM)


def test_spatialDensity_result(valid_calc):
    assert (valid_calc.spatialDensity(TEST_CELLX, TEST_CELLY).compute()
            == 3 / 10), 'failed spatial density result'


def test_spatialDensity_grid(valid_calc):
    a = np.array([[0., 1.], [0., 1.], [0., 0.], [0., 0.], [1., 0.]])
    assert (np.array_equal(valid_calc.spatialDensity(
        TEST_CELLX, TEST_CELLY).get_grid(), a)), 'Wrong grid structure'


def test_nni(valid_calc):
    assert(valid_calc.NNI().compute() == 2.3200303835449625), 'wrong NNI Value'


@pytest.fixture
def valid_calc2(request):
    return EyesMetricCalculator(TEST_ARRAY,GAZE_ARRAY, TEST_SCREENDIM_2)

def test_entropy(valid_calc2):
    g = valid_calc2.GEntropy(TEST_AOI_DICT,entropy='transition')
    val = np.around(g._calc_stationary(TEST_STAT_PROB),
                      decimals=2)
    assert (val == 1.0), 'Wrong stationary entropy calculation, result: {}'.fomrat(val)
    assert (np.around(g._calc_transition(TEST_STAT_PROB,TEST_TRAN_PROB),
                      decimals=2) == 0.73), 'Wrong transition entropy calculation val'
