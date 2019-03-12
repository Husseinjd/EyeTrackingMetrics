import numpy as np



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

    def compute(self):
        '''
        - implement metric computation
        '''
        raise NotImplementedError("compute should be implemented for each metric")
