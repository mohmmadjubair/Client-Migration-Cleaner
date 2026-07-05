import csv

INPUT_FILE = "sample_data/messy_clients.csv"


def load_csv(filepath):
    """Read a CSV file and return rows as a list of dictionaries."""
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def clean_row(row):
    """Apply basic cleaning to one row."""
    return {
        'name': row.get('name', '').strip().title(),
        'email': row.get('email', '').strip().lower(),
        'phone': row.get('phone', '').strip(),
        'dob': row.get('dob', '').strip(),
        'suburb': row.get('suburb', '').strip().title(),
    }


def main():
    rows = load_csv(INPUT_FILE)
    print(f"Loaded {len(rows)} rows from {INPUT_FILE}")

    cleaned_rows = [clean_row(row) for row in rows]

    print(f"First cleaned row: {cleaned_rows[0]}")
    print(f"Last cleaned row: {cleaned_rows[-1]}")


if __name__ == "__main__":
    main()