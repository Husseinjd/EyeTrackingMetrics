import numpy as np
import pandas as pd
from scipy.spatial import KDTree, ConvexHull as conv


class Metric():
    '''
        Metric Class
    '''

    def __init__(self, fixation_array):
        """Init method

        Parameters
        ----------
        fixation_array : numpy float array
                    array having coordinates x,y, and duration as columns values

        """
        if len(fixation_array) < 2 :
            raise Exception('Fixation Array is too small')

        if not isinstance(fixation_array, (np.ndarray, np.generic) ):
            raise Exception('Fixation array is not a numpy array')

        self.fixation_array = fixation_array


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
        float
        """
        con = conv(self.fixation_array[:, [0, 1]])
        if self.func == 'area':
            return con.area
        else:
            return con.volume

class SpatialDensity(Metric):
    '''
    This Metric calculates the Spatialdensity
    accross the screen

    '''

    def __init__(self, fixation_array, cellx, celly, screen_dimension):
        super().__init__(fixation_array)
        self.cellx = cellx
        self.celly = celly
        self.screen_x, self.screen_y = screen_dimension
        self.num_cells = (
            screen_dimension[0] / cellx) * (screen_dimension[1] / celly)


    def get_grid(self):
        """Returns the grid after filling the cells that were visited

        Returns
        -------
        numpy array

        """
        res = self.compute()
        return self.grid

    def compute(self):
        """Calculates the SpatialDensity as
         defined in Goldberg, H. J., & Kotval, X. P. (1999)

        Dividing the screen into equal cell sizes

        Returns
        -------
        float
            spatialDensity

        """

        num_height = int(self.screen_y / self.celly)  # number of cells y
        num_width = int(self.screen_x / self.cellx)  # number of cells x

        # init empty grid to check visited
        self.grid = np.zeros((num_height, num_width))

        # creating array of cell edges for the width and height
        w = np.linspace(0, self.screen_x, num=num_width + 1)
        h = np.linspace(0, self.screen_y, num=num_height + 1)

        for pos,(x,y) in enumerate(self.fixation_array):

            try:
                x = float(x)
                y = float(y)
            except:
                raise Exception("Invalid X or Y type at position".format(pos))

            if x > self.screen_x or x < 0:
                raise Exception('invalid X value at position {}'.format(pos))
            if y > self.screen_y or y < 0:
                raise Exception('invalid Y value at position {}'.format(pos))

            # making sure the x and y are not exactly equal to the max screeny and screenx
            if x == self.screen_x:
                x = self.screen_x - 0.001
            if y == self.screen_y:
                y = self.screen_y - 0.001

            i = len(h) - 2 - np.where(h == h[h <= y][-1])[0][0]  # cell number
            j = np.where(w == w[w <= x][-1])[0][0]  # cell number

            self.grid[i, j] = 1

        res = np.sum(self.grid) / self.num_cells
        assert(res <= 1 and res >= 0),'Invalid spatialDensity value'
        return res


class NNI(Metric):
    '''
    Nearest neighbor Index Metric
    calculate based on Di Nocera et al., 2006
    '''
    def __init__(self,fixation_array,screen_dimension):
        super().__init__(fixation_array)
        self.screen_dm = screen_dimension

    def compute(self):
        """Computes the nni metric

        Returns
        -------
        float
            NNI value
        """
        temp_fixation_array = np.copy(self.fixation_array)
        dist_list = []

        for pos,(x,y) in enumerate(self.fixation_array):
            #remove point from array
            temp_fixation_array = np.delete(temp_fixation_array,pos,0)
            pt = [x,y]
            #find the distance to the nearest neighbor
            dist = self._find_neighbor_distance(temp_fixation_array,pt)

            dist_list.append(dist)

            #restoring the list with all the points
            temp_fixation_array = np.copy(self.fixation_array)

        dNN = np.mean(dist_list)
        dran = 0.5 * np.sqrt((self.screen_dm[0]*self.screen_dm[1]) /len(dist_list))

        return dNN/dran



    def _find_neighbor_distance(self,A,pt):
        """find the distance between a point and its nearest neighbor

        Parameters
        ----------
        A : numpy array
            array containing the X,Y positions
        pt : list
            list representing a point[X,Y]

        Returns
        -------
        distance
            euclidean distance
        """
        if len(pt) > 2 or len(pt) < 2:
            raise Exception('List must have length of 2')

        if A.shape[1] > 2 or  A.shape[1] < 2 :
            raise Exception('A must have a dim of shape (n,2)')

        distance,index = KDTree(A).query(pt)
        return distance
