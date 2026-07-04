import csv

# File paths for now (we'll turn these into a proper CLI later in the week)
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
    # Load the messy data
    rows = load_csv(INPUT_FILE)
    print(f"Loaded {len(rows)} rows from {INPUT_FILE}")

    # Clean each row
    cleaned_rows = [clean_row(row) for row in rows]

    # Show the first cleaned row so we can see it worked
    print(f"First cleaned row: {cleaned_rows[0]}")


if __name__ == "__main__":
    main()