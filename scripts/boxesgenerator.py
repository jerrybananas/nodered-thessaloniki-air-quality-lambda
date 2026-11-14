import csv
import random
from datetime import datetime, timedelta

# Define the 10 box_ids with their fixed latitude and longitude
boxes = [
    ("678fc8ea06a21b00088ff150", 40.658679, 22.953987),
    ("67a4a0ce4ef45d00085c1f9a", 40.650273, 22.922475),
    ("68a3a571b15a1e000843a5cd", 40.651557, 22.948227),
    ("67a23bd9982b6b0007fdff9b", 40.631713, 22.948229),
    ("67c6156a25dcef000805ddcd", 40.619839, 22.971566),
    ("683f922b16e8290007e4c5b6", 40.667052, 22.892515),
    ("67b1f76a07a8dc000787762c", 40.671329, 22.92482),
    ("67c60ef825dcef0008faec23", 40.58524, 22.951671),
    ("67e1cbc97ac85e00082e3c3f", 40.597471, 23.029297),
    ("6789048711da9c000756bac7", 40.637886, 22.948408),
    ("67be36810031890007a16b50", 40.635836, 22.946003),
    ("67e1c3737ac85e00081f4bb4", 40.629985, 22.9532),
    ("680d6acf0f126f0007a4dab1", 40.600995, 22.950196),
    ("67e1b8167ac85e00080ae995", 40.597502, 22.954845),
    ("67b1ed0307a8dc000775189f", 40.599694, 22.989556),
    ("67a3e0414ef45d00080fec45", 40.647768, 22.960743),
    ("680d792b0f126f0007bd56af", 40.614085, 22.966644),
    ("67b1ff5f07a8dc0007958f19", 40.599179, 22.951613),
    ("67e1d3b67ac85e00083cb80a", 40.633732, 22.956715),
    ("67a6801e4ef45d00089d1d88", 40.596252, 22.977519),
    ("68a39776b15a1e00082bcb69", 40.582762, 22.948544),
    ("68a24f0f04fef70007f3bfe9", 40.585058, 22.942985),
]

# PM2.5 ranges and weights
pm25_ranges = [
    (0, 5),    # 40%
    (6, 10),   # 35%
    (11, 20),  # 20%
    (21, 40),  # 4%
    (41, 60),  # 1% (approximating >40 with a reasonable upper bound)
]
pm25_weights = [0.4, 0.35, 0.2, 0.04, 0.01]
pm25_total_weight = sum(pm25_weights)

# PM10 ranges and weights
pm10_ranges = [
    (0, 15),   # 35%
    (16, 30),  # 40%
    (31, 50),  # 20%
    (51, 100), # 4%
    (101, 150),# 1% (approximating >100 with a reasonable upper bound)
]
pm10_weights = [0.35, 0.4, 0.2, 0.04, 0.01]
pm10_total_weight = sum(pm10_weights)

def generate_value(ranges, weights, total_weight):
    pick = random.uniform(0, total_weight)
    accum = 0
    for i, w in enumerate(weights):
        accum += w
        if pick <= accum:
            low, high = ranges[i]
            return round(random.uniform(low, high), 2)  # Round to 2 decimal places like sample
    return 0  # Fallback

# Updated: Start date is now 7 days before the current date
start_dt = datetime.now() - timedelta(days=7)
# Updated: End date is now the current date
end_dt = datetime.now()

# Open CSV file for writing
with open('thess_boxes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(['timestamp', 'box_id', 'pm25', 'pm10', 'latitude', 'longitude'])
    
    current = start_dt
    while current < end_dt:
        # Generate random PM values for this 3-hour period
        pm25_val = generate_value(pm25_ranges, pm25_weights, pm25_total_weight)
        pm10_val = generate_value(pm10_ranges, pm10_weights, pm10_total_weight)
        
        # For each 10-minute interval in this 3-hour period
        begin_period = current
        period_end = current + timedelta(hours=3)
        while begin_period < period_end:
            timestamp_ms = int(begin_period.timestamp() * 1000)
            for box_id, lat, lng in boxes:
                writer.writerow([
                    timestamp_ms,
                    box_id,
                    pm25_val,
                    pm10_val,
                    lat,
                    lng
                ])
            begin_period += timedelta(minutes=10)
        
        # Move to next 3-hour period
        current += timedelta(hours=3)