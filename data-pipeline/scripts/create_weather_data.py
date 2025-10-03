import pandas as pd
import os
import random
from datetime import date, timedelta

# --- Configuration --
PROCESSED_DIR = 'data/processed'
OUTPUT_CSV = 'data/weather_data.csv'

# Simulation parameters
START_DATE = date(2023, 6, 1) # A typical growing season month
DAYS_IN_PERIOD = 30
TEMP_RANGE_CELSIUS = (15, 28)
HUMIDITY_RANGE_PERCENT = (60, 95)

def generate_weather_data():
    """Creates a synthetic weather CSV for all processed images."""

    # Get a list of all image filenames from all subdirectories in processed/
    all_images = []
    for class_folder in os.listdir(PROCESSED_DIR):
        class_path = os.path.join(PROCESSED_DIR, class_folder)
        if os.path.isdir(class_path):
            for filename in os.listdir(class_path):
                all_images.append(filename)

    if not all_images:
        print("Error: No images found in the processed directory. Please run the label_severity script first.")
        return

    print(f"Found {len(all_images)} total images. Generating weather data...")

    weather_records = []
    for filename in all_images:
        # Assign a random date and weather to each image
        random_day_offset = random.randint(0, DAYS_IN_PERIOD - 1)
        image_date = START_DATE + timedelta(days=random_day_offset)

        temp = round(random.uniform(*TEMP_RANGE_CELSIUS), 1)
        humidity = round(random.uniform(*HUMIDITY_RANGE_PERCENT), 1)

        weather_records.append({
            'image_filename': filename,
            'date': image_date.strftime("%Y-%m-%d"),
            'temperature_celsius': temp,
            'humidity_percent': humidity
        })

    # Create a pandas DataFrame and save to CSV
    df = pd.DataFrame(weather_records)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"\n✅ Successfully created weather data with {len(df)} rows at: {OUTPUT_CSV}")
    print("\nSample of the generated data:")
    print(df.head())

if __name__ == '__main__':
    generate_weather_data()
