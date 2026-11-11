SYNTHETIC ACCELEROMETER DATA 1
Teaching/test fixture only. Not measured whale data or a validated whale simulator.
150 seconds; 50 Hz; 7500 samples; SI acceleration units m/s^2; seed 42.
Time runs from 0 to 149.98 seconds. Sampling rate is illustrative.
Fixed sensor/body alignment; no tag slip. Positive Z carries gravity at rest.

0 <= t < 30: stationary plus independent Gaussian sensor noise.
30 <= t < 60: gentle 0.5 Hz rhythmic dynamic acceleration, smoothly tapered.
60 <= t < 90: stronger 0.5 Hz rhythmic dynamic acceleration, smoothly tapered.
90 <= t < 120: quiet baseline with Gaussian pulses centered at 96, 105, 114 s.
120 <= t < 150: smooth 0-to-60-degree gravity-vector rotation; no dynamic acceleration.
Noise standard deviation is 0.02 m/s^2 per axis throughout.
The burst_segment label covers the whole interval, not only individual pulses.

synthetic_accelerometer_1.csv: time_s, ax_m_s2, ay_m_s2, az_m_s2, condition.
ground_truth_1.csv: noise-free gravity and dynamic components for checking results.
Do not feed condition labels or ground-truth columns into the signal-processing methods.
plot_synthetic_data_1.m: base MATLAB script to load the CSV and plot its three axes.
No extra toolbox or Animal Tags installation is needed for this plotting script.
For Animal Tags, A is the acceleration matrix and fs the sampling rate.
Use help for each repository function before calling it.
Orientation changes may produce jerk despite zero translational dynamic acceleration.
MSA is a lower bound; filtering-based metrics can respond to orientation changes.
Do not interpret these simulated pulses as validated feeding events.
This one recording is for learning/debugging, not independent replicates for hypothesis testing.
