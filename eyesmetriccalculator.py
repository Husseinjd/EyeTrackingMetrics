from .metrics import *
import numpy as np


class EyesMetricCalculator():

    def __init__(self, data_fixations,data_gazes, screen_dimension):
        """Init Method

        Parameters
        ----------
        data_fixations: DataFrame or numpyarray
             having 3 columns containing fixations coordinates x,y and their duration as columns
        data_gazes: DataFrame or numpyarray
                    similar structure to data_fixations but for gaze data
        screen_dimensions : tuple or list of size 2
            tuple containing the screen dimensions (width , length)
        """

        #adding appending aoi's for later calculations
        self.aoi_list = []

        if not isinstance(screen_dimension, tuple) and not isinstance(screen_dimension, list):
            raise Exception('screen_dimension is not a tuple or list')
        else:
            if len(screen_dimension) > 2 or len(screen_dimension) < 2:
                raise Exception('tuple size > 2')

        self.screen_dimensions = screen_dimension

        if self.screen_dimensions[0] < 0 or self.screen_dimensions[1] < 0:
            raise Exception('Screen dimension cannot be negative')

        self.fixation_array = np.array(data_fixations)
        self.gaze_array = np.array(data_gazes)

    def spatialDensity(self, cellx=20, celly=20):
        """Calculates the spatialDensity

        Parameters
        ----------
        cellx : float-int
            width of the cell
        celly : float-int
            length of the cell

        Returns
        -------
        spatialDensity metric object


        """
        if not isinstance(cellx, (int, float)):
            raise Exception('cellx is not an int or float ')

        if not isinstance(celly, (int, float)):
            raise Exception('celly is not an int or float ')

        if cellx > self.screen_dimensions[0]:
            raise Exception('cellx greate than screen width')

        if celly > self.screen_dimensions[0]:
            raise Exception('celly greate than screen width')

        if celly < 0 or cellx < 0:
            raise Exception('cell inputs should be positive')

        self._check_dimensions(cellx, celly)  # raises assertion error

        # compute spatial Density
        return SpatialDensity(self.fixation_array[:, [0, 1]], cellx, celly, self.screen_dimensions)

    def convexHull(self, func='area'):
        """Calculates the ConvexHull based on Scipy Spatial ConvexHull

        Returns
        -------
        ConvexHullArea  metric object

        """
        # taking only the x and y columns from the fixation array
        return ConvexHull(self.fixation_array[:, [0, 1]], func)

    def NNI(self):
        """Calculates the NNI metric

        Returns
        -------
        NNI metric
        """
        return NNI(self.fixation_array[:, [0, 1]], self.screen_dimensions)

    def GEntropy(self,aoi_dict,entropy='transition'):
        """Calculates the transition or stationary entropy for the given gaze data

        Parameters
        ----------
        aoi_dict : dict {aoi_poly1: PolyAOI(..)}
                dictionary containing AOI names as keys
                and AOI object as values

        entropy : str
            specifying which entropy metric to calculate, takes values
            (transition,stationary)

        Returns
        -------
        GazeEntropy object

        """
        return GazeEntropy(self.screen_dimensions,aoi_dict,self.gaze_array,entropy)



    def _check_dimensions(self, cellx, celly):
        # check width
        assert(self.screen_dimensions[0] % cellx
               == 0), "Please change cellx to fit the screen width"
        # check width
        assert(self.screen_dimensions[1] % celly
               == 0), "Please change celly to fit the screen length"
