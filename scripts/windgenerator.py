import csv
import random
from datetime import datetime, timedelta

# Wind speed ranges and weights (in m/s)
# >12 m/s approximated with reasonable upper bound (e.g., up to 20 m/s)
wind_ranges = [
    (0, 1),     # 15%
    (2, 3),     # 30%
    (4, 5),     # 25%
    (6, 8),     # 15%
    (9, 12),    # 10%
    (13, 20),   # 5% (approximating >12 with upper bound)
]
wind_weights = [0.15, 0.3, 0.25, 0.15, 0.1, 0.05]
wind_total_weight = sum(wind_weights)

def generate_wind_value(ranges, weights, total_weight):
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
with open('thess_wind.csv', 'w', newline='') as csvfile:
    # ... (the rest of the script remains unchanged)
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(['timestamp', 'avrg_wind_spd'])
    
    current = start_dt
    while current < end_dt:
        # Generate random wind speed for this 3-hour period
        wind_val = generate_wind_value(wind_ranges, wind_weights, wind_total_weight)
        
        # For each 10-minute interval in this 3-hour period
        begin_period = current
        period_end = current + timedelta(hours=3)
        while begin_period < period_end:
            timestamp_ms = int(begin_period.timestamp() * 1000)
            writer.writerow([
                timestamp_ms,
                wind_val
            ])
            begin_period += timedelta(minutes=10)
        
        # Move to next 3-hour period
        current += timedelta(hours=3)