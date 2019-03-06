from .metric import Metric
import numpy as np



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
