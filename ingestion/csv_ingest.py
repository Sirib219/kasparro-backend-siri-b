import csv
from pathlib import Path


def fetch_csv_data():
    """
    Reads asset data from CSV file
    """
    csv_path = Path("data/sample_assets.csv")

    records = []
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    return records
