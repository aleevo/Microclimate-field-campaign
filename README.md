# Microclimate Analysis: Field Campaign

## Overview
In-situ meteorological field campaign analyzing spatiotemporal microclimate dynamics across a heterogeneous urban landscape. The study links surface properties (vegetation, built structures, impervious surfaces) to near-surface atmospheric conditions through handheld sensor measurements and thermal infrared imagery.

## Research Questions
1. How do air temperature, relative humidity, and wind patterns across two heights (30cm and 2m) correlate with underlying surface types?
2. To what extent can diurnal atmospheric variability be attributed to surface energy balance differences via thermal imagery?
3. What do near-surface vertical temperature gradients reveal about surface heating strength and local stability?

## Data Collection

### In-Situ Measurements (4 Locations: A, B, C, D)
| Variable | Heights | Interval | Duration |
|----------|---------|----------|----------|
| Air Temperature | 30cm, 2m | 15 min | 09:00–16:30 |
| Relative Humidity | 30cm, 2m | 15 min | 09:00–16:30 |
| Wind Speed | 30cm, 2m | 15 min | 09:00–16:30 |
| Wind Direction | 30cm, 2m | 15 min | 09:00–16:30 |

### Remote Sensing
- **Thermal infrared camera**: Spatial radiative surface temperature snapshots at 09:00, 12:00, 16:00
- **AWS reference**: German Weather Station data at 16m height for synoptic context

## Key Findings

### Two Distinct Microclimatic Regimes Identified

| Regime | Location | Characteristics | Dominant Flux |
|--------|----------|-----------------|---------------|
| **Sensible Heat Dominated** | B (and C/D) | ΔT = +1.45°C, ΔRH = -0.86%, peak 40.2°C | Dry, impervious surface |
| **Latent Heat Dominated** | A | ΔT = -0.07°C, ΔRH = +0.73%, humid near-surface | Vegetated, pervious surface |

### Surface-Atmosphere Coupling
- **Exposed grassy/soil patch**: Strong coupling (r = 0.79, RMSE = 1.15°C) — radiative temperature predicts air temperature accurately
- **Shaded tree canopy**: Weak coupling (r = 0.48, RMSE = 1.65°C) — canopy insulates, decoupling surface from air temperature

### Wind Field Heterogeneity
- Location C: Well-ventilated, dominant SSW flow, highest wind speeds
- Location B: Sheltered, calm conditions, intensified microclimate extremes
- Locations A & D: Semi-sheltered, SSE primary direction

## Files

| File/Folder | Description |
|-------------|-------------|
| `Final Report.pdf` | Full academic report with methodology, results, discussion |
| `Final Code` | Python scripts for data processing and visualization |
| `plots/` | Generated figures: time series, wind roses, thermal imagery, gradient analysis |
| `Thermal imagery at three time steps` | 09:00, 12:00, 16:00 radiative temperature maps |
| `Wind Rose per Location` | Directional wind patterns at 2m for sites A-D |
| `Wind Rose Locations and AWS` | Comparison with 16m synoptic reference |
| `Temperature Time Series 2m vs 30cm` | Diurnal evolution across all locations |
| `Temperature Difference` | Vertical gradient dynamics (ΔT = T₃₀cm - T₂m) |
| `Relative Humidity Time Series` | RH diurnal cycles at both heights |
| `Relative Humidity Difference` | Vertical humidity gradients |
| `Wind Speed Time Series` | Wind speed at 30cm vs 2m |
| `Wind Speed Time Series Locations and AWS` | Local vs. synoptic wind comparison |
| `ROI Average Thermal profiles` | Grassy/soil vs. shaded area thermal evolution |
| `Quantification of thermal and air temperature` | Correlation analysis: surface vs. air temperature |
| `Two thermal ROI` | Grassy patch vs. shaded area comparison |
| `AWS Global Radiation vs Time` | Solar forcing context |

## Tech Stack
- **Python**: Pandas, NumPy, Matplotlib
- **Data Processing**: Statistical analysis, gradient computation, correlation/regression
- **Visualization**: Time series, wind roses, thermal maps, scatter plots

## Methodology Highlights
- **Vertical Gradient Analysis**: ΔT = T₃₀cm - T₂m and ΔRH = RH₃₀cm - RH₂m computed per timestep
- **ROI Analysis**: Manual selection of contrasting surfaces (grass/soil vs. shade) on thermal imagery
- **Normalization**: z-score standardization for comparing surface and air temperature dynamics
- **Validation**: AWS 16m data for synoptic forcing context


## Implications
The findings support urban planning and climate adaptation strategies:
- **Green infrastructure** (trees, permeable surfaces) mitigates urban heat island effects
- **Surface type** is the first-order control on local microclimate — not just background weather
- Thermal imagery can predict air temperature well over exposed surfaces, but fails over shaded canopies

## Citation
If referencing this work:
&gt; Field campaign analyzing surface-atmosphere coupling and microclimate heterogeneity via in-situ sensors and thermal imagery.
