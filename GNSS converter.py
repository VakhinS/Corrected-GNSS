import pandas as pd
import numpy as np

# CONFIGURATION

INPUT_CSV  = r"C:\Users\nspan\Downloads\anveshak app\GNSS\dgps_rover_data.csv"
OUTPUT_CSV = r"C:\Users\nspan\Downloads\anveshak app\GNSS\dgps_rover_data_corrected.csv"

# Known exact coordinates of the base station
BASE_KNOWN_LAT = 12.990123
BASE_KNOWN_LON = 80.223452

# Earth mean radius in metres
R_EARTH = 6371000

# LOAD

df = pd.read_csv(INPUT_CSV)
df.to_csv(OUTPUT_CSV, index=False)



# DGNSS Correction

df["Correction_Lat"] = BASE_KNOWN_LAT - df["Base Latitude (Measured)"]
df["Correction_Lon"] = BASE_KNOWN_LON - df["Base Longitude (Measured)"]

df["DGNSS_Lat"] = df["Rover Latitude (Measured)"]  + df["Correction_Lat"]
df["DGNSS_Lon"] = df["Rover Longitude (Measured)"] + df["Correction_Lon"]


# Convert to local XY (ENU) in metres
#   x (East)  = R · Δλ · cos(φ₀)
#   y (North) = R · Δφ

origin_lat_rad = np.radians(BASE_KNOWN_LAT)

delta_lat_rad = np.radians(df["DGNSS_Lat"] - BASE_KNOWN_LAT)
delta_lon_rad = np.radians(df["DGNSS_Lon"] - BASE_KNOWN_LON)

df["X_m"] = (R_EARTH * delta_lon_rad * np.cos(origin_lat_rad)).round(8)
df["Y_m"] = (R_EARTH * delta_lat_rad).round(8)

# Round lat/lon columns for readability
df["Correction_Lat"] = df["Correction_Lat"].round(8)
df["Correction_Lon"] = df["Correction_Lon"].round(8)
df["DGNSS_Lat"]      = df["DGNSS_Lat"].round(8)
df["DGNSS_Lon"]      = df["DGNSS_Lon"].round(8)


# SAVE

df.to_csv(OUTPUT_CSV, index=False)
