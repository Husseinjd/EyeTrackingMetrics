import numpy as np
# import gaze transition
from EyeTrackingMetrics.transition_matrix import *


class GazeEntropy(Metric):
    '''
    GazeEntropy metric calculating both
    the graze transition and stationary entropy
    '''

    def __init__(self,screen_dimension,aoi_dict,gaze_array,entropy):
        """Short summary.

        Parameters
        ----------
        screen_dimension : tuple or list

        aoi_dict : dict {\'aoi_poly1\': PolyAOI(..)}
                dictionary containing AOI names as keys
                and AOI object as values

        gaze_array : list of coordinates lists

        entropy : str
            specifying which entropy metric to calculate, takes values
            (transition,stationary)

        """
        self.screen_dim = screen_dimension
        self.gaze_array = gaze_array
        self.entropy_method = entropy
        self.aoi_dict = aoi_dict
        self.gz = GazeTransitions(screen_dimension,aoi_dict,gaze_array)
        # build the probability matrices
        self.sp = self.get_stationary_prob()
        self.tp  = self.get_tranprobabilities()

    def get_stationary_prob(self):
        """calculates an array of probabilities for have a point in each aoi

        Returns
        -------
        statporb_list : float numpyarray
        """

        statprob_list = []
        for n,a in self.aoi_dict.items():
            statprob_list.append(self.gz.get_prob_aoi(n))
        return  np.array(statprob_list)

    def get_tranprobabilities(self):
        """Calculates the transition probabilities Pij

        Returns
        -------
        np array
            matrix of transition probabilties between aoi's

        """
        return np.array(self.gz.get_transition_matrix()/len(self.gaze_array))


    def compute(self):
        """Compute the gaze entropy based on Krejtz et al., 2014

        Returns
        -------
        entropy: float
        """
        entropy = 0
        if self.entropy_method.tolower() == 'transition' :
            entropy = 0
            for i in range(len(self.sp)):
                ent_sum = 0
                for j in range(len(self.tp)):
                    ent_sum += self.tp[i,j] * np.log(self.tp[i,j])
                entropy += self.sp[i] * ent_sum
            return np.around(entropy,decimals=2) * -1

        elif self.entropy_method.tolower() == 'stationary' :
            for j in self.sp:
                    entropy +=j * np.log(j)
            return np.around(entropy,decimals=2)* -1
        else:
            raise Exception('Entropy takes options [transition,stationary]')
