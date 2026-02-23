"""
Differential GNSS (DGNSS) Correction Script
=============================================
Known exact base station position (starting point):
  12.990123 N, 80.223452 E

For each row:
  1. Correction = Known base position - Measured base position
  2. DGNSS Rover position = Raw rover reading + Correction
  3. Convert corrected position to local XY (ENU) in metres
     relative to the known starting point
"""

import pandas as pd
import numpy as np

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_CSV  = r"C:\Users\nspan\Downloads\anveshak app\GNSS\dgps_rover_data.csv"
OUTPUT_CSV = r"C:\Users\nspan\Downloads\anveshak app\GNSS\dgps_rover_data_corrected.csv"

# Known exact coordinates of the base station
BASE_KNOWN_LAT = 12.990123
BASE_KNOWN_LON = 80.223452

# Earth mean radius in metres
R_EARTH = 6371000

# =============================================================================
# LOAD
# =============================================================================

df = pd.read_csv(INPUT_CSV)
df.to_csv(OUTPUT_CSV, index=False)
df2 = pd.read_csv(OUTPUT_CSV)

# =============================================================================
# STEP 1 — DGNSS Correction
# =============================================================================

df2["Correction_Lat"] = df["Base Latitude (Measured)"] - BASE_KNOWN_LAT
df2["Correction_Lon"] = df["Base Longitude (Measured)"] - BASE_KNOWN_LON

df2["DGNSS_Lat"] = df["Rover Latitude (Measured)"]  - df2["Correction_Lat"]
df2["DGNSS_Lon"] = df["Rover Longitude (Measured)"] - df2["Correction_Lon"]

# =============================================================================
# STEP 2 — Convert to local XY (ENU) in metres
# Formulae derived from ECEF → ENU rotation:
#   x (East)  = R · Δλ · cos(φ₀)
#   y (North) = R · Δφ
# where Δφ, Δλ are in radians and φ₀ is the origin latitude
# =============================================================================

origin_lat_rad = np.radians(BASE_KNOWN_LAT)

delta_lat_rad = np.radians(df2["DGNSS_Lat"] - BASE_KNOWN_LAT)
delta_lon_rad = np.radians(df2["DGNSS_Lon"] - BASE_KNOWN_LON)

df2["X_m"] = (R_EARTH * delta_lon_rad * np.cos(origin_lat_rad)).round(8)
df2["Y_m"] = (R_EARTH * delta_lat_rad).round(8)

# Round lat/lon columns for readability
df2["Correction_Lat"] = df2["Correction_Lat"].round(8)
df2["Correction_Lon"] = df2["Correction_Lon"].round(8)
df2["DGNSS_Lat"]      = df2["DGNSS_Lat"].round(8)
df2["DGNSS_Lon"]      = df2["DGNSS_Lon"].round(8)

# =============================================================================
# SAVE
# =============================================================================

df2.to_csv(OUTPUT_CSV, index=False)
