from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Find the data folder inside your repo.
repo = Path(__file__).resolve().parent.parent
data_file = repo / "data" / "synthetic_accelerometer_1.csv"

data = pd.read_csv(data_file)

time = data["time_s"]
acceleration = data[["ax_m_s2", "ay_m_s2", "az_m_s2"]]

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(time, acceleration, label=["X", "Y", "Z"])

for boundary in [30, 60, 90, 120]:
    ax.axvline(boundary, color="gray", linestyle="--")

ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Acceleration (m/s²)")
ax.set_title("Synthetic accelerometer data 1")
ax.legend()
ax.grid(True)

fig.tight_layout()

import numpy as np

A = acceleration.to_numpy()
t = time.to_numpy()
fs = 1 / np.median(np.diff(t))

# MSA: compare combined acceleration with gravity.
msa = np.abs(np.linalg.norm(A, axis=1) - 9.81)

# Jerk: measure changes between neighboring readings.
jerk = np.zeros(len(A))
jerk[:-1] = np.linalg.norm(np.diff(A, axis=0) * fs, axis=1)

fig2, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

axes[0].plot(t, msa)
axes[0].set_title("MSA — Python")
axes[0].set_ylabel("MSA (m/s²)")

axes[1].plot(t, jerk)
axes[1].set_title("Norm-jerk — Python")
axes[1].set_ylabel("Jerk (m/s³)")
axes[1].set_xlabel("Time (seconds)")

for ax in axes:
    for boundary in [30, 60, 90, 120]:
        ax.axvline(boundary, color="gray", linestyle="--")
    ax.grid(True)

fig2.tight_layout()

# Save numerical results for comparison with MATLAB.
results_folder = repo / "results"
results_folder.mkdir(exist_ok=True)

pd.DataFrame({
    "time_s": t,
    "MSA": msa,
    "Jerk": jerk,
}).to_csv(results_folder / "python_results_data_1.csv", index=False)

matlab_file = repo / "results" / "matlab_results_data_1.csv"

if matlab_file.exists():
    matlab = pd.read_csv(matlab_file)

    if len(matlab) != len(t):
        raise ValueError("MATLAB and Python have different numbers of samples.")

    if not np.allclose(matlab["time_s"], t, rtol=0, atol=1e-8):
        raise ValueError("MATLAB and Python timestamps do not match.")

    for name, python_values in [("MSA", msa), ("Jerk", jerk)]:
        matlab_values = matlab[name].to_numpy()

        difference = np.max(np.abs(python_values - matlab_values))
        match = np.allclose(
            python_values, matlab_values,
            rtol=1e-7, atol=1e-8
        )

        print(f"{name}: largest difference = {difference:.3e}")
        print(f"{name}: matches MATLAB = {match}")
else:
    print(f"MATLAB results file not found: {matlab_file}")

from scipy.signal import lfilter

# Match Animal Tags' MATLAB moving-average implementation.
window_samples = int(np.floor(2 * fs + 0.5))
window_samples = 2 * (window_samples // 2) + 1
half_window = window_samples // 2

# Repeat the first and last readings at the edges.
padded = np.pad(
    A,
    ((half_window, half_window), (0, 0)),
    mode="edge"
)

# Subtract the moving average from the centered reading.
filter_weights = -np.ones(window_samples) / window_samples
filter_weights[half_window] += 1

filtered = lfilter(filter_weights, [1.0], padded, axis=0)

start = window_samples - 1
dynamic = filtered[start:start + len(A)]

odba_python = np.sum(np.abs(dynamic), axis=1)
vedba_python = np.linalg.norm(dynamic, axis=1)

# Plot the two results.
fig3, axes3 = plt.subplots(
    2, 1, figsize=(12, 7), sharex=True
)

for ax, values, name in [
    (axes3[0], odba_python, "ODBA"),
    (axes3[1], vedba_python, "VeDBA"),
]:
    ax.plot(t, values)
    ax.set_title(f"{name} — Python")
    ax.set_ylabel(f"{name} (m/s²)")
    ax.grid(True)

    for boundary in [30, 60, 90, 120]:
        ax.axvline(boundary, color="gray", linestyle="--")

axes3[1].set_xlabel("Time (seconds)")
fig3.tight_layout()

# Save all four Python results.
pd.DataFrame({
    "time_s": t,
    "MSA": msa,
    "Jerk": jerk,
    "ODBA": odba_python,
    "VeDBA": vedba_python,
}).to_csv(
    results_folder / "python_results_data_1.csv",
    index=False
)

# Compare with the saved MATLAB results.
if matlab_file.exists():
    reference = pd.read_csv(matlab_file)

    if len(reference) != len(t):
        raise ValueError("Different numbers of samples.")

    if not np.allclose(
        reference["time_s"], t, rtol=0, atol=1e-8
    ):
        raise ValueError("Timestamps do not match.")

    for name, values in [
        ("ODBA", odba_python),
        ("VeDBA", vedba_python),
    ]:
        expected = reference[name].to_numpy()
        difference = np.max(np.abs(values - expected))
        matches = np.allclose(
            values, expected, rtol=1e-7, atol=1e-8
        )

        print(f"{name}: largest difference = {difference:.3e}")
        print(f"{name}: matches MATLAB = {matches}")
          
plt.show()