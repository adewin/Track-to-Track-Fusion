"""Generates a simple one target scenario

Using stonesoup's functions, a simple one target scenario is generated. Similar measurement and process models. Same
timestep size.

Inspiration for how to generate ground truth and measurements are taken from
https://stonesoup.readthedocs.io/en/latest/auto_tutorials/01_KalmanFilterTutorial.html#sphx-glr-auto-tutorials-01-kalmanfiltertutorial-py
"""

from datetime import datetime
from datetime import timedelta
import numpy as np

from stonesoup.models.transition.linear import CombinedLinearGaussianTransitionModel, \
    ConstantVelocity
from stonesoup.types.groundtruth import GroundTruthPath, GroundTruthState
from stonesoup.types.detection import Detection
from stonesoup.models.measurement.linear import LinearGaussian

from utils import store_object

start_time = datetime.now()

# specify seed to be able repeat example
np.random.seed(1996)

# combine two 1-D CV models to create a 2-D CV model
transition_model = CombinedLinearGaussianTransitionModel([ConstantVelocity(0.01), ConstantVelocity(0.01)])

# starting at 0,0 and moving NE
truth = GroundTruthPath([GroundTruthState([0, 1, 0, 1], timestamp=start_time)])

# generate truth using transition_model and noise
for k in range(1, 21):
    truth.append(GroundTruthState(
        transition_model.function(truth[k - 1], noise=True, time_interval=timedelta(seconds=1)),
        timestamp=start_time + timedelta(seconds=k)))

# Simulate measurements
# Specify measurement model for radar
measurement_model_radar = LinearGaussian(
    ndim_state=4,  # number of state dimensions
    mapping=(0, 2),  # mapping measurement vector index to state index
    noise_covar=np.array([[1, 0],  # covariance matrix for Gaussian PDF
                          [0, 1]])
)

# Specify measurement model for AIS (Same as for radar)
measurement_model_ais = LinearGaussian(
    ndim_state=4,
    mapping=(0, 2),
    noise_covar=np.array([[1, 0],
                          [0, 1]])
)

# generate "radar" measurements
measurements_radar = []
for state in truth:
    measurement = measurement_model_radar.function(state, noise=True)
    measurements_radar.append(Detection(measurement, timestamp=state.timestamp))

# generate "AIS" measurements
measurements_AIS = []
for state in truth:
    measurement = measurement_model_ais.function(state, noise=True)
    measurements_AIS.append(Detection(measurement, timestamp=state.timestamp))

# save the ground truth and the measurements for the radar and the AIS
store_object.store_object(truth, "../scenarios/scenario2/ground_truth.pk1")
store_object.store_object(measurements_radar, "../scenarios/scenario2/measurements_radar.pk1")
store_object.store_object(measurements_AIS, "../scenarios/scenario2/measurements_ais.pk1")
store_object.store_object(start_time, "../scenarios/scenario2/start_time.pk1")
store_object.store_object(measurement_model_radar, "../scenarios/scenario2/measurement_model_radar.pk1")
store_object.store_object(measurement_model_ais, "../scenarios/scenario2/measurement_model_ais.pk1")
store_object.store_object(transition_model, "../scenarios/scenario2/transition_model.pk1")


