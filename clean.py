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

def is_valid_email(email):
    """Check if an email looks valid. Basic check: has @ and a dot after it."""
    if not email:
        return False
    if '@' not in email:
        return False
    parts = email.split('@')
    if len(parts) != 2:
        return False
    if '.' not in parts[1]:
        return False
    return True

def validate_row(row):
    """Check if a cleaned row is safe to import. Returns (is_valid, reason)."""
    if not row['name']:
        return False, "Missing name"
    if not row['email']:
        return False, "Missing email"
    if not is_valid_email(row['email']):
        return False, "Invalid email format"
    return True, None
def write_csv(filepath, rows, fieldnames):
    """Write rows to a CSV file. Creates the folder if needed."""
    import os
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    input_file = "sample_data/messy_clients.csv"
    clean_output = "output/clean.csv"
    review_output = "output/review.csv"

    rows = load_csv(input_file)
    print(f"Loaded {len(rows)} rows from {input_file}")

    clean_rows = []
    review_rows = []

    for row in rows:
        cleaned = clean_row(row)
        is_valid, reason = validate_row(cleaned)

        if is_valid:
            clean_rows.append(cleaned)
        else:
            review_rows.append({**cleaned, 'reason': reason})

    write_csv(clean_output, clean_rows, ['name', 'email', 'phone', 'dob', 'suburb'])
    write_csv(review_output, review_rows, ['name', 'email', 'phone', 'dob', 'suburb', 'reason'])

    print("-" * 40)
    print(f"Clean rows:  {len(clean_rows)} → {clean_output}")
    print(f"Review rows: {len(review_rows)} → {review_output}")
    print(f"Total:       {len(clean_rows) + len(review_rows)}")


if __name__ == "__main__":
    main()