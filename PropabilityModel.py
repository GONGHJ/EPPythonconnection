from KDEpy import FFTKDE
import numpy as np
import scipy.stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import math
from Initialize import  Number_of_GKDE_fit_points
from cdf_kde import cdf_kde


def KDEestimator(input_for_estimator, individual_houses_one_timepoint):
    bw = input_for_estimator[0]
    cdf_low = input_for_estimator[1]
    cdf_high = input_for_estimator[2]
    data = individual_houses_one_timepoint
    # estimator = FFTKDE(kernel='gaussian', bw='silverman')
    estimator = FFTKDE(kernel='gaussian', bw=bw)
    PowerDistribution, PossibilityDensity = estimator.fit(data, weights=None).evaluate(Number_of_GKDE_fit_points)
    step = (max(PowerDistribution)-min(PowerDistribution))/Number_of_GKDE_fit_points

    expection = np.dot(PowerDistribution, PossibilityDensity)*step
    expection = np.around(expection, decimals=2)

    cdf_for_kde, cdf_lookup_matrix, CI_low, CI_high = cdf_kde(PowerDistribution, PossibilityDensity, step, cdf_low, cdf_high)

    KDE_estimator_output = [expection, PowerDistribution, PossibilityDensity, cdf_for_kde, cdf_lookup_matrix, CI_low, cdf_low, CI_high, cdf_high]

    return KDE_estimator_output



