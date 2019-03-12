# EyeTracking Metrics Calculator


## Overview
The project contains methods to calculate some of the known metrics used in eye tracking research
including:

1) Spatial Density (Goldberg, H. J., & Kotval, X. P. (1999))
2) ConvexHull
3) Nearest Neighbor Index (Di Nocera et al., 2006)
4) Entropy Based Metrics : Gaze Stationary and Transition Entropies (Krejtz et al., 2014)


A Juypter notebook is included to illustrate the usage with some dummy examples.


## Additional Package Requirements

- shapely
- numpy
- Pandas
- scipy


## Testing

A test module is included to test the metric methods used.
More can be added and tested.

to run the tests across the whole package:

```
pip install pytest

pytest [package-directory]
```

## Future Work
Addition of more metrics 
