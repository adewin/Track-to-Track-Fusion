"""calc_metrics module for calculating metrics

Module contains functions for calculating metrics
TODO
"""
import numpy as np
from stonesoup.types.track import Track
from stonesoup.types.groundtruth import GroundTruthPath
from stonesoup.types.state import State
from stonesoup.types.groundtruth import GroundTruthState

import scipy.linalg as la


def calc_nees(tracks: Track, ground_truths: GroundTruthPath):
    """
    Calculates NEES. Assumes that tracks and ground_truths are of same length, and that the elements on the same
    index correlates.
    :param tracks:
    :param ground_truths:
    :return:
    """
    nees = []
    for (state, ground_truth) in zip(tracks, ground_truths):
        chol_cov = la.cholesky(state.covar, lower=True)
        mean_diff = state.state_vector - ground_truth.state_vector
        inv_chol_cov_diff = la.solve_triangular(chol_cov, mean_diff, lower=True)
        nees.append((inv_chol_cov_diff ** 2).sum())
    return nees


def calc_anees(nees):
    """
    Calculates anees
    :param nees:
    :return: np.array containing the anees value
    """
    return np.array(nees).mean()
