import numpy as np


class Fixation():
    """
    Fixation Object representing a fixation on a screen with coordinates
    and a duration

    """
    def __init__(self,x,y,duration=0,aoi=None):
        """Init Method

        Parameters
        ----------
        x : float or int
            Description of parameter `x`.
        y : float or int
            Description of parameter `y`.
        duration : float or int
            fixation duration
        aoi : AOI object

        """
        self.x = x
        self.y = y
        self.duration = duration
        self.aoi = aoi

    def get_coor(self):
        """Get fixation coordinates

        Returns
        -------
        tuple : (x,y)
        fixation coordinates
        """
        return (self.x,self.y)
