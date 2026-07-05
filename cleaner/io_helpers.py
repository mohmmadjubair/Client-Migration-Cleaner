"""Helpers for reading and writing CSV files."""

import csv
import os


def load_csv(filepath):
    """Read a CSV file and return rows as a list of dictionaries."""
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(filepath, rows, fieldnames):
    """Write rows to a CSV file. Creates the folder if needed."""
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def strip_internal_fields(row):
    """Remove internal-only fields before writing to CSV."""
    return {k: v for k, v in row.items() if k != 'phone_valid'}