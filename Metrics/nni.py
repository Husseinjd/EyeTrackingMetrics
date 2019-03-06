import numpy as np
from .metric import Metric
from scipy.spatial import KDTree


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
