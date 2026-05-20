"""


@author: ali
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from windrose import WindroseAxes
import xarray as xr
import os
from glob import glob
from PIL import Image
from pathlib import Path 
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator

# Base directory
src = Path("/ERM/Microclimates/Final/")

# Import field campaign data
locations = ['A', 'B', 'C', 'D']
df = {}

for loc in locations:
    file_path= src / f'field-campaign_loc{loc}_20250702.csv'
    df[loc] = pd.read_csv(file_path)                          

# print(df['A'].head())

# print(df['A'].columns)

# ----------------------------------------------------
aws_file = src / "AWS_DWD_202050702.csv"
aws = pd.read_csv(aws_file)

# print(aws.head())
# print(aws.columns)

# Create time index for the campaign day (09:00 → 16:30, every 15 minutes)
time_index = pd.date_range(start="2025-07-02 09:00", end="2025-07-02 16:30", freq="15min")

# Calculate statistics for all locations
# 1.1 Minimum , Maximum , Standard Deviation of Temperatue and RH
temp_stats = {}
rh_stats = {}

for loc in locations:
    # Temperature statistics
    temp_2m = df[loc]['Ta_2m']
    temp_30cm = df[loc]['Ta_30cm']
    
    temp_stats[loc] = {
        'Ta_2m_min': temp_2m.min(),
        'Ta_2m_max': temp_2m.max(),
        'Ta_2m_std': temp_2m.std(),
        'Ta_30cm_min': temp_30cm.min(),
        'Ta_30cm_max': temp_30cm.max(),
        'Ta_30cm_std': temp_30cm.std()
    }
    
    # Relative humidity statistics
    rh_2m = df[loc]['RH_2m']
    rh_30cm = df[loc]['RH_30cm']
    
    rh_stats[loc] = {
        'RH_2m_min': rh_2m.min(),
        'RH_2m_max': rh_2m.max(),
        'RH_2m_std': rh_2m.std(),
        'RH_30cm_min': rh_30cm.min(),
        'RH_30cm_max': rh_30cm.max(),
        'RH_30cm_std': rh_30cm.std()
    }

# Create summary DataFrames
temp_summary = pd.DataFrame(temp_stats).T
rh_summary = pd.DataFrame(rh_stats).T

print("TEMPERATURE ANALYSIS (09:00 - 16:30)")
print("=" * 50)
print("\nTemperature at 2m height:")
print("-" * 25)
for loc in locations:
    stats = temp_stats[loc]
    print(f"Location {loc}: Min={stats['Ta_2m_min']:.1f}°C, Max={stats['Ta_2m_max']:.1f}°C, Std={stats['Ta_2m_std']:.2f}°C")

print("\nTemperature at 30cm height:")
print("-" * 30)
for loc in locations:
    stats = temp_stats[loc]
    print(f"Location {loc}: Min={stats['Ta_30cm_min']:.1f}°C, Max={stats['Ta_30cm_max']:.1f}°C, Std={stats['Ta_30cm_std']:.2f}°C")

print("\nRELATIVE HUMIDITY ANALYSIS (09:00 - 16:30)")
print("=" * 60)
print("\nRelative Humidity at 2m height:")
print("-" * 35)
for loc in locations:
    stats = rh_stats[loc]
    print(f"Location {loc}: Min={stats['RH_2m_min']:.1f}%, Max={stats['RH_2m_max']:.1f}%, Std={stats['RH_2m_std']:.2f}%")

print("\nRelative Humidity at 30cm height:")
print("-" * 40)
for loc in locations:
    stats = rh_stats[loc]
    print(f"Location {loc}: Min={stats['RH_30cm_min']:.1f}%, Max={stats['RH_30cm_max']:.1f}%, Std={stats['RH_30cm_std']:.2f}%")

# Calculate overall statistics across all locations
print("\nOVERALL STATISTICS ACROSS ALL LOCATIONS")
print("=" * 45)

# Combine all data for overall statistics
all_temp_2m = pd.concat([df[loc]['Ta_2m'] for loc in locations])
all_temp_30cm = pd.concat([df[loc]['Ta_30cm'] for loc in locations])
all_rh_2m = pd.concat([df[loc]['RH_2m'] for loc in locations])
all_rh_30cm = pd.concat([df[loc]['RH_30cm'] for loc in locations])

print(f"\nTemperature at 2m (Overall):")
print(f"Min: {all_temp_2m.min():.1f}°C, Max: {all_temp_2m.max():.1f}°C, Std: {all_temp_2m.std():.2f}°C")

print(f"\nTemperature at 30cm (Overall):")
print(f"Min: {all_temp_30cm.min():.1f}°C, Max: {all_temp_30cm.max():.1f}°C, Std: {all_temp_30cm.std():.2f}°C")

print(f"\nRelative Humidity at 2m (Overall):")
print(f"Min: {all_rh_2m.min():.1f}%, Max: {all_rh_2m.max():.1f}%, Std: {all_rh_2m.std():.2f}%")

print(f"\nRelative Humidity at 30cm (Overall):")
print(f"Min: {all_rh_30cm.min():.1f}%, Max: {all_rh_30cm.max():.1f}%, Std: {all_rh_30cm.std():.2f}%")

# Additional analysis: Diurnal patterns
print("\nDIURNAL PATTERNS ANALYSIS")
print("=" * 30)

# Add time index to each dataframe for time-based analysis
for loc in locations:
    df[loc]['Time'] = time_index

# Calculate hourly averages
hourly_stats = {}
for loc in locations:
    df_loc = df[loc].copy()
    df_loc['Hour'] = df_loc['Time'].dt.hour
    hourly_stats[loc] = df_loc.groupby('Hour').agg({
        'Ta_2m': ['mean', 'std'],
        'Ta_30cm': ['mean', 'std'],
        'RH_2m': ['mean', 'std'],
        'RH_30cm': ['mean', 'std']
    })

# Peak temperature times
print("\nTime of maximum temperature at each location:")
for loc in locations:
    max_temp_time = df[loc].loc[df[loc]['Ta_2m'].idxmax(), 'Time']
    print(f"Location {loc}: {max_temp_time.strftime('%H:%M')} - {df[loc]['Ta_2m'].max():.1f}°C")
    

# 1.2 Calculate differences between height levels for each location
height_differences = {}

for loc in locations:
    # Temperature differences
    temp_diff = df[loc]['Ta_30cm'] - df[loc]['Ta_2m']
    abs_temp_diff = np.abs(temp_diff)
    
    # Relative humidity differences
    rh_diff = df[loc]['RH_30cm'] - df[loc]['RH_2m']
    abs_rh_diff = np.abs(rh_diff)
    
    height_differences[loc] = {
        # Temperature statistics
        'Temp_diff_mean': temp_diff.mean(),
        'Temp_diff_std': temp_diff.std(),
        'Temp_diff_max': temp_diff.max(),
        'Temp_diff_min': temp_diff.min(),
        'Temp_abs_diff_mean': abs_temp_diff.mean(),
        'Temp_abs_diff_max': abs_temp_diff.max(),
        
        # RH statistics
        'RH_diff_mean': rh_diff.mean(),
        'RH_diff_std': rh_diff.std(),
        'RH_diff_max': rh_diff.max(),
        'RH_diff_min': rh_diff.min(),
        'RH_abs_diff_mean': abs_rh_diff.mean(),
        'RH_abs_diff_max': abs_rh_diff.max(),
        
        # Percentage of time when 30cm is warmer than 2m
        'pct_time_warmer_at_30cm': (temp_diff > 0).mean() * 100,
        
        # Percentage of time when RH is higher at 30cm than 2m
        'pct_time_wetter_at_30cm': (rh_diff > 0).mean() * 100
    }

# Create summary DataFrame
diff_summary = pd.DataFrame(height_differences).T

print("HEIGHT LEVEL DIFFERENCES ANALYSIS (30cm vs 2m)")
print("=" * 55)
print("\nTEMPERATURE DIFFERENCES (Ta_30cm - Ta_2m)")
print("-" * 40)

for loc in locations:
    diff = height_differences[loc]
    print(f"\nLocation {loc}:")
    print(f"  Mean difference: {diff['Temp_diff_mean']:+.2f}°C")
    print(f"  Standard deviation: {diff['Temp_diff_std']:.2f}°C")
    print(f"  Maximum difference: {diff['Temp_diff_max']:+.2f}°C")
    print(f"  Minimum difference: {diff['Temp_diff_min']:+.2f}°C")
    print(f"  Mean absolute difference: {diff['Temp_abs_diff_mean']:.2f}°C")
    print(f"  30cm was warmer than 2m: {diff['pct_time_warmer_at_30cm']:.1f}% of time")

print("\nRELATIVE HUMIDITY DIFFERENCES (RH_30cm - RH_2m)")
print("-" * 45)

for loc in locations:
    diff = height_differences[loc]
    print(f"\nLocation {loc}:")
    print(f"  Mean difference: {diff['RH_diff_mean']:+.2f}%")
    print(f"  Standard deviation: {diff['RH_diff_std']:.2f}%")
    print(f"  Maximum difference: {diff['RH_diff_max']:+.2f}%")
    print(f"  Minimum difference: {diff['RH_diff_min']:+.2f}%")
    print(f"  Mean absolute difference: {diff['RH_abs_diff_mean']:.2f}%")
    print(f"  RH was higher at 30cm than 2m: {diff['pct_time_wetter_at_30cm']:.1f}% of time")

# Calculate overall statistics across all locations
print("\nOVERALL DIFFERENCES ACROSS ALL LOCATIONS")
print("=" * 40)


# 1.3 Visualiztion

# TEMPERATURE, HUMIDITY TIME SERIES

# Helper for formatting time axis
def format_time_axis(ax, xlabel="Time of Day", ylabel="Value"):
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# General plotting function
def plot_microclimate(variable, ylabel, diff_label):
    """
    variable : str
        "Ta" for temperature or "RH" for humidity
    ylabel : str
        Y-axis label for main plots
    diff_label : str
        Y-axis label for difference plots
    """

# --- 1. 2x2 grid: 2m vs 30cm ---
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'{ylabel} Time Series: 30cm vs 2m (09:00 - 16:30)',
                 fontsize=16, fontweight='bold', y=0.95)

    for ax, loc in zip(axes.flatten(), locations):
        df[loc]['Time'] = time_index
        ax.plot(df[loc]['Time'], df[loc][f'{variable}_2m'], 'o-', label="2m", color="blue", alpha=0.8)
        ax.plot(df[loc]['Time'], df[loc][f'{variable}_30cm'], 's-', label="30cm", color="red", alpha=0.8)

        ax.set_title(f"Location {loc}", fontsize=14, fontweight="bold")
        format_time_axis(ax, ylabel=ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

        # Stats box
        diff = df[loc][f'{variable}_30cm'] - df[loc][f'{variable}_2m']
        text = f"Mean Δ: {diff.mean():+.1f}\nMax Δ: {diff.max():+.1f}"
        ax.text(0.02, 0.98, text, transform=ax.transAxes, va="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8), fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()

    # --- 3. 2x2 grid: Difference (30cm - 2m) ---
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'{ylabel} Difference: (30cm - 2m) (09:00 - 16:30)',
                 fontsize=16, fontweight='bold', y=0.95)

    for ax, loc in zip(axes.flatten(), locations):
        df[loc]['Time'] = time_index
        diff = df[loc][f'{variable}_30cm'] - df[loc][f'{variable}_2m']

        ax.plot(df[loc]['Time'], diff, 'o-', color="darkorange", alpha=0.8, label="Δ")
        ax.axhline(0, color="red", linestyle="--", alpha=0.7)
        ax.fill_between(df[loc]['Time'], diff, 0, where=diff>=0, color="red", alpha=0.2, label="30cm higher")
        ax.fill_between(df[loc]['Time'], diff, 0, where=diff<0, color="blue", alpha=0.2, label="2m higher")

        ax.set_title(f"Location {loc}", fontsize=14, fontweight="bold")
        format_time_axis(ax, ylabel=diff_label)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()


# ============================
# CALL FUNCTION FOR BOTH CASES
# ============================
plot_microclimate("Ta", "Temperature (°C)", "ΔT (°C)")
plot_microclimate("RH", "Relative Humidity (%)", "ΔRH (%)")


# ============================
# 1.4 WIND SPEED PLOTS (time series + wind rose)
# ============================

# Time series plots
def plot_wind_speed(df, locations):
    # --- 1. 2x2 grid: 2m vs 30cm ---
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Wind Speed Time Series: 30cm vs 2m (09:00 - 16:30)',
                 fontsize=16, fontweight='bold', y=0.95)

    for ax, loc in zip(axes.flatten(), locations):
        df[loc]['Time'] = time_index
        ax.plot(df[loc]['Time'], df[loc]['Windspeed_2m'], 'o-', label="2m", color="blue", alpha=0.8)
        ax.plot(df[loc]['Time'], df[loc]['Windspeed_30cm'], 's-', label="30cm", color="red", alpha=0.8)

        ax.set_title(f"Location {loc}", fontsize=14, fontweight="bold")
        format_time_axis(ax, ylabel="Wind Speed (m/s)")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

        # Stats box for Δ
        diff = df[loc]['Windspeed_30cm'] - df[loc]['Windspeed_2m']
        text = f"Mean Δ: {diff.mean():+.1f}\nMax Δ: {diff.max():+.1f}"
        ax.text(0.02, 0.98, text, transform=ax.transAxes, va="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8), fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()


# --- Wind rose (using 2 m wind direction and speed) ---

from windrose import WindroseAxes

def plot_wind_rose(df, locations):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10),
                             subplot_kw={'projection': 'windrose'})
    fig.suptitle('Wind Rose (2 m) per Location', fontsize=16, fontweight='bold', y=0.95)

    axes = axes.flatten()
    for ax, loc in zip(axes, locations):
        ws = df[loc]['Windspeed_2m']
        wd = df[loc]['WindDirection']  # single direction column
        ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
        ax.set_title(f"Location {loc}", fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


# ============================
# CALL WIND SPEED PLOTS
# ============================
plot_wind_speed(df, locations)
plot_wind_rose(df, locations)

# 2.1 Incorporating AWS and rename columns

aws_df = aws.copy()
aws_df['Time'] = time_index  # Align with campaign time

# Rename columns to match other DataFrames
aws_df = aws_df.rename(columns={
    'wind_speed_16m(ms-1)': 'Windspeed_16m',
    'wind_direction_16m(deg)': 'WindDirection_16m',
    'radiation_global(Wm-2)': 'Global_Radiation'
})

# Add a 'Location' column to each DataFrame
for loc in locations:
    df[loc]['Location'] = loc

aws_df['Location'] = 'AWS'

# Combine all DataFrames into a single one
combined_df = pd.concat([df[loc] for loc in locations] + [aws_df], ignore_index=True)

# Optional - check the combined DataFrame
# print(combined_df.head())
# print(combined_df.tail())

# Visualisation of AWS global radiation
# --- AWS Global Radiation Time Series ---
fig, ax = plt.subplots(figsize=(12, 6))
aws_df['Time'] = pd.to_datetime(aws_df['Time'])  # Ensure datetime

ax.plot(aws_df['Time'], aws_df['Global_Radiation'], 
        color='orange', marker='o', linestyle='-', alpha=0.8, label='Global Radiation')

# Customize
ax.set_title('AWS Global Radiation vs Time (09:00 - 16:30)', fontsize=16, fontweight='bold')
ax.set_xlabel('Time of Day', fontsize=12)
ax.set_ylabel('Global Radiation (W/m²)', fontsize=12)

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# Grid & legend
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)

plt.tight_layout()
plt.show()


# --- Wind Speed Time Series (, 2m, AWS 16m) ---
# Combined wind speed time series for all locations + AWS

# Ensure AWS date column is datetime
aws['Date'] = pd.to_datetime(aws['Date'])

plt.figure(figsize=(14, 8))
plt.title('Wind Speed Time Series: 2m (Locations) & 16m (AWS)', fontsize=16, fontweight='bold')

# Define colors and markers
loc_colors = {'A': 'blue', 'B': 'green', 'C': 'red', 'D': 'purple', 'AWS': 'orange'}
loc_markers = {'A': 'o', 'B': 's', 'C': '^', 'D': 'd', 'AWS': 'x'}

# Plot 2m wind speed for each location
for loc in locations:
    plt.plot(df[loc]['Time'], df[loc]['Windspeed_2m'], 
             label=f'Loc {loc} - 2m', color=loc_colors[loc],
             marker=loc_markers[loc], markersize=5, alpha=0.8)

# Plot AWS 16m wind speed
plt.plot(aws['Date'], aws['wind_speed_16m(ms-1)'], 
         label='AWS - 16m', color=loc_colors['AWS'],
         marker=loc_markers['AWS'], markersize=6, alpha=0.9, linestyle='--')

# Format x-axis to show only hours
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))

# Axis labels and formatting
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Wind Speed (m/s)', fontsize=12)
plt.xticks(rotation=0)  # keep hours horizontal
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()

# Create figure with 5 subplots: 4 locations + AWS
fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection':'windrose'})
axes = axes.flatten()
fig.suptitle('Wind Roses for 2m (Locations) and 16m (AWS)', fontsize=16, fontweight='bold', y=0.95)

# List including AWS as fifth entry
all_sources = locations + ['AWS']

for i, src in enumerate(all_sources):
    ax = axes[i]
    
    if src == 'AWS':
        ws = aws['wind_speed_16m(ms-1)']
        wd = aws['wind_direction_16m(deg)']
    else:
        ws = df[src]['Windspeed_2m']
        wd = df[src]['WindDirection']
    
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white', bins=6, cmap=plt.cm.viridis)
    title = f"Location {src}" if src != 'AWS' else "AWS - 16m"
    ax.set_title(title, fontsize=12, fontweight='bold')

# Hide the empty subplot (6th subplot in 2x3 grid)
axes[-1].axis('off')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# 3.Thermal Imagery 

# === Load frames ===
src = Path("/ERM/Microclimates/Final/frames_thermalCam/")
frame_files = sorted(glob(str(src / "*.png")))
frames = [np.array(Image.open(f).convert("L")) for f in frame_files]  # convert to grayscale

# Example time mapping (every 15 min from 09:00)
# frame_000 = 09:00, frame_012 = 12:00, frame_028 = 16:00
snapshot_indices = {"09:00": 0, "12:00": 12, "16:00": 28}

# === Plot snapshots ===
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
vmin, vmax = np.min(frames), np.max(frames)  # consistent color scale

for ax, (time, idx) in zip(axes, snapshot_indices.items()):
    im = ax.imshow(frames[idx], cmap="inferno", vmin=vmin, vmax=vmax)
    ax.set_title(f"Thermal {time}", fontsize=14)
    ax.axis("off")

fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.6, label="Temperature (a.u.)")
plt.show()

# 3.1 Temporal differences
delta_morning = frames[snapshot_indices["12:00"]] - frames[snapshot_indices["09:00"]]
delta_afternoon = frames[snapshot_indices["16:00"]] - frames[snapshot_indices["12:00"]]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, delta, title in zip(axes, [delta_morning, delta_afternoon], ["12:00-09:00", "16:00-12:00"]):
    im = ax.imshow(delta, cmap="bwr", vmin=-20, vmax=20)
    ax.set_title(f"ΔT {title}", fontsize=14)
    ax.axis("off")

fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.6, label="ΔTemperature (a.u.)")
plt.show()

# 3.2 Define ROI(Regions of Interests
# Example pixel ranges (you will adjust by checking images):
roi_grass = (slice(800, 1200), slice(1000, 1400))   # y, x
roi_shadow = (slice(1500, 1800), slice(2200, 2600))

# === Extract ROI means over time ===
grass_mean = [np.mean(f[roi_grass]) for f in frames]
shadow_mean = [np.mean(f[roi_shadow]) for f in frames]

# Time axis
hours = np.arange(9, 9 + len(frames)*0.25, 0.25)[:len(frames)]  # 15-min steps

plt.figure(figsize=(10,6))
plt.plot(hours, grass_mean, label="Grass/Soil Patch", color="green")
plt.plot(hours, shadow_mean, label="Tree Shade", color="blue")
plt.xlabel("Time of Day (h)")
plt.ylabel("Mean Temperature (a.u.)")
plt.title("ROI Average Thermal Profiles")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


# 4. Compare the thermal temperature obtained by the camera for each subset selected 
# --- CONFIG ---
# If you already created ROIs interactively, just re-use that list here.
# Each ROI is a tuple: (y1, y2, x1, x2). Example below can be edited.
rois = [
    (800, 1200, 1000, 1400),   # ROI1 e.g., grass/soil
    (1500, 1800, 2200, 2600),  # ROI2 e.g., tree shade
]
roi_names = [f"ROI{i+1}" for i in range(len(rois))]

# If you want to compare each ROI to a *specific* location’s Ta_2m,
# set this mapping; otherwise the script will use the mean Ta across A–D.
# Example: {'ROI1': 'A', 'ROI2': 'C'}
roi_to_loc = {}   # leave empty to use mean Ta across all locations


# Assumes you already have `df` dict with locations A–D loaded and `time_index` created (15-min steps 09:00–16:30)
# and that frames live in this folder:
thermal_dir = Path("/ERM/Microclimates/Final/frames_thermalCam")
thermal_files = sorted(glob(str(thermal_dir / "frame_*.png")))
assert len(thermal_files) > 0, "No thermal frames found."

# Build thermal ROI means over all frames
roi_means = {name: [] for name in roi_names}
for f in thermal_files:
    img = np.array(Image.open(f).convert("L"))  # intensity proxy
    for name, (y1, y2, x1, x2) in zip(roi_names, rois):
        roi_means[name].append(img[y1:y2, x1:x2].mean())

roi_df = pd.DataFrame(roi_means)
# Make sure length matches your station data length; both should be 31 points (09:00–16:30 every 15 min)
# If needed, trim/pad here; by default we assume they match the same 15-min grid:
roi_df.index = time_index[:len(roi_df)]

# Assemble Ta_2m per location and the mean
ta_df = pd.DataFrame({loc: df[loc]["Ta_2m"].values for loc in ['A','B','C','D']}, index=time_index)
ta_df = ta_df.loc[roi_df.index]  # align
ta_df["MEAN"] = ta_df.mean(axis=1)

# compare one ROI to a chosen Ta series
def compare_roi_to_Ta(roi_series: pd.Series, ta_series: pd.Series, roi_label: str, ta_label: str):
    # Ensure alignment
    roi_series = roi_series.loc[ta_series.index]

    # Linear fit: predict Ta from ROI intensity (unit conversion via fit)
    x = roi_series.values.astype(float)
    y = ta_series.values.astype(float)
    a, b = np.polyfit(x, y, 1)                     # y_hat = a*x + b
    y_hat = a*x + b

    # Metrics
    r = np.corrcoef(x, y)[0, 1]
    rmse = np.sqrt(np.mean((y - y_hat)**2))
    bias = np.mean(y - y_hat)

    # ---- VISUALS: 2-panel figure ----
    fig = plt.figure(figsize=(12, 5), constrained_layout=True)  # ✅ use constrained_layout
    gs = fig.add_gridspec(1, 2, wspace=0.25)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    # (A) Time series (normalized to compare shapes)
    def zscore(s): 
        v = s.values.astype(float)
        return (v - v.mean()) / (v.std() + 1e-9)
    ax0.plot(roi_series.index, zscore(roi_series), marker='o', label=f"{roi_label} (thermal, z-score)", alpha=0.8)
    ax0.plot(ta_series.index, zscore(ta_series), marker='s', label=f"{ta_label} (Ta, z-score)", alpha=0.8)
    ax0.set_title(f"Temporal evolution ({roi_label} vs {ta_label})", fontweight='bold')
    ax0.set_ylabel("z-score")
    ax0.set_xlabel("Time of day")
    ax0.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax0.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax0.xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))
    plt.setp(ax0.xaxis.get_majorticklabels(), rotation=45)
    ax0.grid(True, alpha=0.3)
    ax0.legend(fontsize=9)

    # (B) Scatter with linear fit in physical Ta units
    ax1.plot(x, y, 'o', alpha=0.7, label='Samples')
    xx = np.linspace(x.min(), x.max(), 100)
    ax1.plot(xx, a*xx + b, '-', label=f'Fit: Ta = {a:.3f}·Thermal + {b:.2f}')
    ax1.set_title("Thermal vs Air Temperature (2 m)", fontweight='bold')
    ax1.set_xlabel(f"{roi_label} thermal intensity (a.u.)")
    ax1.set_ylabel("Ta (°C)")
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=9, loc='best')

    # Annotate metrics
    text = f"r = {r:.2f}\nRMSE = {rmse:.2f} °C\nBias = {bias:+.2f} °C\nN = {len(x)}"
    ax1.text(0.05, 0.95, text, transform=ax1.transAxes, va='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)

    plt.show()  # ✅ no tight_layout() needed

    return dict(r=r, rmse=rmse, bias=bias, a=a, b=b)


# Run comparisons for each ROI
results = {}
for roi_name in roi_names:
    # pick Ta series: mapped location or mean of all
    if roi_to_loc.get(roi_name) in ['A','B','C','D']:
        ta_series = ta_df[roi_to_loc[roi_name]]
        ta_label = f"Loc {roi_to_loc[roi_name]} (2 m)"
    else:
        ta_series = ta_df["MEAN"]
        ta_label = "Mean of A–D (2 m)"

    res = compare_roi_to_Ta(roi_df[roi_name], ta_series, roi_name, ta_label)
    results[roi_name] = res

# Print a compact summary
print("\n=== Thermal vs Ta (2 m) — Summary ===")
for k, v in results.items():
    print(f"{k}: r={v['r']:.2f}, RMSE={v['rmse']:.2f} °C, Bias={v['bias']:+.2f} °C, Fit: Ta≈{v['a']:.3f}*Thermal+{v['b']:.2f}")

