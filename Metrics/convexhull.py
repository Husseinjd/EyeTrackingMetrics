from scipy.spatial import ConvexHull as conv
from .metric import Metric
import numpy as np



class ConvexHull(Metric):
    '''
    This Metric calculates the ConvexHUll Area given
    a list of fixation coordinates on the screen
    '''

    def __init__(self, fixation_array,func):
        """Init convexhull

        Parameters
        ----------
        func : str
            area or volume
        """
        super().__init__(fixation_array)
        if not func in ('area','volume'):
            raise Exception('Function not supported please use \'area\' or \'volume\' ')
        self.func = func

    def compute(self):
        """Compute the convexhull result based on the func parameter
        Returns
        -------
        convexhull: float
        """
        con = conv(self.fixation_array[:, [0, 1]])
        if self.func == 'area':
            return con.area
        else:
            return con.volume
