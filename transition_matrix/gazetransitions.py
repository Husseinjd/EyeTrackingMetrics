import numpy as np
from .fixation import Fixation
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from .aoi import *
import copy


class GazeTransitions():
    '''
    This class models gaze transitions from one AOI to the other,
    additionally calculating important metrics.
    '''

    def __init__(self, screen_dimension, aoi_dict, gaze_array):
        """Init method

        Parameters
        ----------
        aoi_dict : dict {aoi_poly1: PolyAOI(..)}
                dictionary containing AOI names as keys
                and AOI object as values

        gaze_list : numpy array
            a numpy array representing x,y gaze positions and last column as duration

        screen_dimension: tuple or list of size
        """
        self.aoi_dict = aoi_dict
        self.aoi_count_dict = dict()
        self.gaze_array = gaze_array
        self.screen_dim = screen_dimension
        self.points_outside_aoi = 0
        self.n = len(gaze_array)
        # matrix representing the tranisition counts from one aoi to the other
        self.transition_matrix = pd.DataFrame(np.zeros((len(aoi_dict), len(
            aoi_dict))), columns=list(aoi_dict.keys()), index=list(aoi_dict.keys()))
        self._load_transitions()

    def get_prob_aoi(self, aoi):
        """Returns the probability of having a point in the given aoi

        Parameters
        ----------
        aois : str
                aoi name given in the dict
        Returns
        -------
        prob: float

        """
        # checks if aoi belongs to the list provided
        for k, a in self.aoi_count_dict.items():
            if k == aoi:
                return len(self.aoi_count_dict[k]) / self.n
        raise Exception('AOI is not in the AOI dict provided')


    def _load_transitions(self):
        """
        - checks to which AOI a point belongs to and adds that point to the aoi
        (assuming here that AOI's do not intersect and thus no two points can belong to
        more than one AOI)

        -Populates the transition matrix between aois

        Parameters
        ----------
        pt : type
            Description of parameter `pt`.
        """
        fixation_array = [Fixation(x, y) for x, y, z in self.gaze_array]

        #init count points in AOI dictionary
        for k, a in self.aoi_dict.items():
            self.aoi_count_dict[k] = [] #representing the points that each dict has


        prev_aoi = None  # init prev_aoi

        for indx_fx in range(len(fixation_array)):
            found_aoi = False  # checks whether an aoi was found for a point
            for indx, (aoi_name, aoi) in enumerate(self.aoi_dict.items()):
                fx = fixation_array[indx_fx]  # current fixation
                if fx.get_coor() in aoi:
                    self._update_pointsContainer(aoi_name,fx)
                    fx.aoi = aoi
                    # check if the previous fixation was in a certain AOI
                    if prev_aoi is not None:
                        # increment the (previous_index_aoi,next_index_aoi) position of the transition matrix
                        self.transition_matrix.loc[prev_aoi, aoi_name] += 1

                    prev_aoi = aoi_name  # update prev_aoi to current
                    found_aoi = True
                    break

            # reset prev_aoi to none if a point did not belong to any aoi
            if not found_aoi:
                prev_aoi = None

            if prev_aoi is None:
                self.points_outside_aoi += 1

    def get_aoi_points(self,aoi):
        """Returns a list of points that are contained in an AOI

        Parameters
        ----------
        aoi : Str
            aoi name

        Returns
        -------
        list of tuples
            list of x,y coordinates that are contained in AOI
        """
        try:
            return self.aoi_count_dict[aoi]
        except KeyError:
            print('AOI name not recognized')

    def _update_pointsContainer(self,aoi_name,fx):
        """updates aoi array of points

        Parameters
        ----------
        aoi_name: str

        fx : Fixation
            fixation to be added to the list of points
        """
        self.aoi_count_dict[aoi_name].append(fx.get_coor())


    def get_transition_matrix(self):
        """Returns the transition matrix between AOI's

        Returns
        -------
        dataframe

        """
        return self.transition_matrix

    def plot_all(self, background_img_path=None,annotate_points=False):
        """Plots the screen with all the AOI's provided and the data points

        Parameters
        ----------
        background_img_path : str
            path to an image to add as a background
        annotate_points : boolean
                true or false whether to provided sequence point labeling
                on the plot
        """
        fig = plt.figure(1, figsize=(12, 9))
        ax = fig.add_subplot(111)
        if background_img_path:
            img = plt.imread(background_img_path)
            ax.imshow(
                img, extent=[0, self.screen_dim[0], self.screen_dim[1], 0])

        plt.xlim((0, self.screen_dim[0]))
        plt.ylim((self.screen_dim[1], 0))
        for aoi_name, aoi in self.aoi_dict.items():
            if isinstance(aoi, PolyAOI):
                x, y = aoi.poly.exterior.coords.xy
                points = np.array([x, y], np.int32).T
                poly = matplotlib.patches.Polygon(
                    points, linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(poly)
            elif isinstance(aoi, CircleAOI):
                ax.add_patch(aoi.circle_shape)
            else:
                raise Exception('Object not of any AOI type')

        plt.axis('scaled')
        plt.scatter(self.gaze_array[:, 0], self.gaze_array[:, 1])
        plt.axis('auto')
        if annotate_points:
            for i, txt in enumerate(self.gaze_array):
                ax.annotate(tuple(txt[0:2]), (self.gaze_array[i,0] -5, self.gaze_array[i,1]+25))
        # plt.savefig("aoi.png")
        plt.show()

    def get_transition_prob(self, aoi_1, aoi_2):
        """Get the transition probability between two aois
        that were given in the aoi list

        prob(aoi2|aoi1)

        Parameters
        ----------
        aoi_1 : str
            name of the first aoi
        aoi_2 : str
            name of the second aoi

        Returns
        -------
        prob: float between 0 and 1
            probability of going from aoi1 to aoi2
        """
        return self.transition_matrix[aoi_1, aoi_2] / np.sum(self.transition_matrix[aoi_1], axis=0)
