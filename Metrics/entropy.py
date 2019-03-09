import numpy as np
# import gaze transition
import os,sys,inspect
from .metric import Metric
#import from a parent directory package
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from transition_matrix import *


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
        self.gz     = GazeTransitions(screen_dimension,aoi_dict,gaze_array)
        # build the probability matrices
        self.sp = np.array(self.get_stationary_prob())
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
        return  statprob_list

    def get_tranprobabilities(self):
        """Calculates the transition probabilities Pij

        Returns
        -------
        np array
            matrix of transition probabilties between aoi's

        """
        return np.array(self.gz.get_transition_matrix()/len(self.gaze_array))

    def _calc_stationary(self,stat_prob):
        """calculates the stationary entropy

        Parameters
        ----------
        stat_prob : list of probabilities

        Returns
        -------
        entropy: float
            Stationary Entropy
        """
        e = 0
        for j in stat_prob:
                e +=j * np.log(j+ 0.00000001)
        return e* -1

    def _calc_transition(self,stat_prob,tran_prob):
        """calculates the transition entropy

        Parameters
        ----------
        stat_prob : list of probabilities

        stat_trans : numpy array (matrix) of transition probabilities

        Returns
        -------
        entropy: float
            Transition Entropy
        """
        e=0
        for i in range(len(stat_prob)):
            ent_sum = 0
            for j in range(len(self.tp)):
                ent_sum += tran_prob[i,j] * np.log(tran_prob[i,j] + 0.00000001)
            e += stat_prob[i] * ent_sum
        return e* -1

    def compute(self):
        """Compute the gaze entropy based on Krejtz et al., 2014

        Returns
        -------
        entropy: float
        """
        entropy=0
        if self.entropy_method.lower() == 'transition' :
            entropy  = self._calc_transition(self.sp,self.tp)
            return np.around(entropy,decimals=2)

        elif self.entropy_method.lower() == 'stationary' :
            entropy = self._calc_stationary(self.sp)
            return np.around(entropy,decimals=2)
        else:
            raise Exception('Entropy takes options [transition,stationary]')
