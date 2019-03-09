import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib


class AOI():
    '''
    Class representing an area of interest on a screen
    '''

    def __init__(self, screen_dimension):
        """init methods

        Parameters
        ----------
        screen_dimension : tuple or list
                screen (width,length)

        center : float or int
        """
        self.screen_x = screen_dimension[0]
        self.screen_y = screen_dimension[1]
        self.points_in_aoi = []  # defines the points that belong to the aoi [[x1,y1],..]


class PolyAOI(AOI):
    '''
    Defines a square shaped aoi at a position over the screen
    '''

    def __init__(self, screen_dimension, vertices):
        """Init method

        Parameters
        ----------
        screen_dimension : list or tuple

        vertices : numpy array
             array list of the poly vertices
             e.g. np.array ( [ [0,0], ...       ])
        Returns
        -------
        type
            Description of returned object.

        """
        super().__init__(screen_dimension)

        if len(vertices) < 3:
            raise Exception('minimum number of vertices equal to three')

        self.vertices = [(x, y) for x, y in vertices]

        # create polygon
        self.poly = Polygon(self.vertices)

    def __contains__(self, pt):
        """checks if the point is on or inside the square

        Parameters
        ----------
        pt: float list or tuple of size 2

        Returns
        -------
        boolean
            returns true if a point is inside or on the square
        """
        return self.poly.contains(Point(pt[0], pt[1]))

    def plot_shape(self):
        """Plot polygon
        """
        x, y = self.poly.exterior.coords.xy
        points = np.array([x, y], np.int32).T
        fig, ax = plt.subplots(1)
        poly = matplotlib.patches.Polygon(
            points, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(poly)
        plt.scatter(x, y)
        #list to array
        a = np.array(self.points_in_aoi)
        if len(a > 1):
            plt.scatter(a[:,0],a[:,1])
        plt.axis("auto")
        plt.show()


class CircleAOI(AOI):
    '''
    Defines a circle shaped aoi at a position over the screen
    '''

    def __init__(self, screen_dimension, radius, center=[0, 0]):

        super().__init__(screen_dimension)
        # check if the given center is inside the screen
        if center[0] > self.screen_x or center[1] > self.screen_y:
            raise Exception('Center cannot exceed screen boundries')
        if center[0] < 0 or center[1] < 0:
            raise Exception('Center cannot be negat3ive')
        self.center_x = center[0]
        self.center_y = center[1]

        if radius < 0:
            raise Exception('radius cannot be negative')
        self.radius = radius

        self.circle_shape = plt.Circle(
            (self.center_x, self.center_y), self.radius, color='r',fill=False)

    def __contains__(self, pt):
        """checks if the point is inside or on the circle

        Parameters
        ----------
        pt: float list or tuple of size 2

        Returns
        -------
        boolean
            returns true if a point is inside or on the circle
        """
        return np.sqrt((self.center_x - pt[0])**2 + (self.center_y - pt[1])**2) <= self.radius


    def plot_shape(self):
        c = self.circle_shape
        fig, ax = plt.subplots(1)
        ax.add_patch(c)
        a = np.array(self.points_in_aoi)
        if len(a > 1):
            plt.scatter(a[:,0],a[:,1])
        plt.axis('scaled')
        plt.axis("auto")
        plt.show()
