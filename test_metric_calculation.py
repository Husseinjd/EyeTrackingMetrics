from eyesmetriccalculator import EyesMetricCalculator
import numpy as np
import pytest


TEST_ARRAY = np.array([[0, 0], [100, 50], [78, 31]])
TEST_SCREENDIM =  (100, 50)
TEST_CELLX = 50
TEST_CELLY = 10

tp = np.array([[0.78,0.06,0.16] ,
            [0.18,0.46,0.36],
             [0.15,0.09,0.76]
            ])

sp = np.array([0.42,0.14,0.44])


@pytest.fixture
def valid_calc(request):
    return EyesMetricCalculator(TEST_ARRAY,TEST_SCREENDIM)


def test_spatialDensity_result(valid_calc):
    assert (valid_calc.spatialDensity(TEST_CELLX, TEST_CELLY).compute() ==
            3 / 10), 'failed spatial density result'


def test_spatialDensity_grid(valid_calc):
    a = np.array([[0., 1.],[0., 1.],[0., 0.],[0., 0.],[1., 0.]])
    assert (np.array_equal(valid_calc.spatialDensity(
        TEST_CELLX, TEST_CELLY).get_grid(),a)), 'Wrong grid structure'

def test_nni(valid_calc):
    assert(valid_calc.NNI().compute() == 2.3200303835449625 ),'wrong NNI Value'


def test_entropy(valid_calc):
    pass #assert ht = 0.73
    #assert hs = 1.0
