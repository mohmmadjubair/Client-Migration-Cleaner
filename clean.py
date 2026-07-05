import csv 
import phonenumbers

INPUT_FILE = "sample_data/messy_clients.csv"


def load_csv(filepath):
    """Read a CSV file and return rows as a list of dictionaries."""
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def normalise_phone(phone, region="AU"):
    """Convert phone to E.164 format. Returns (cleaned, is_valid)."""
    if not phone or not phone.strip():
        return "", False

    try:
        parsed = phonenumbers.parse(phone, region)
        if phonenumbers.is_valid_number(parsed):
            formatted = phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )
            return formatted, True
        else:
            return phone.strip(), False
    except phonenumbers.NumberParseException:
        return phone.strip(), False

def clean_row(row):
    """Apply basic cleaning to one row."""
    phone_value, phone_valid = normalise_phone(row.get('phone', ''))

    return {
        'name': row.get('name', '').strip().title(),
        'email': row.get('email', '').strip().lower(),
        'phone': phone_value,
        'phone_valid': phone_valid,
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
    if not row['phone_valid']:
        return False, "Invalid phone number"
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

def strip_internal_fields(row):
    """Remove internal-only fields before writing to CSV."""
    return {k: v for k, v in row.items() if k != 'phone_valid'}

def main():
    input_file = "sample_data/messy_clients.csv"
    clean_output = "output/clean.csv"
    review_output = "output/review.csv"

    rows = load_csv(input_file)
    print(f"Loaded {len(rows)} rows from {input_file}")

    clean_rows = []
    review_rows = []

    seen_emails = {}

    for index, row in enumerate(rows):
        row_number = index + 2

        cleaned = clean_row(row)
        email = cleaned['email']

        if email and email in seen_emails:
            first_seen_row = seen_emails[email]
            review_rows.append({
                **cleaned,
                'reason': f"Duplicate email (first seen in row {first_seen_row})"
            })
            continue

        is_valid, reason = validate_row(cleaned)
        if not is_valid:
            review_rows.append({**cleaned, 'reason': reason})
            continue

        if email:
            seen_emails[email] = row_number

        clean_rows.append(cleaned)

    clean_out = [strip_internal_fields(r) for r in clean_rows]
    review_out = [strip_internal_fields(r) for r in review_rows]

    write_csv(clean_output, clean_out, ['name', 'email', 'phone', 'dob', 'suburb'])
    write_csv(review_output, review_out, ['name', 'email', 'phone', 'dob', 'suburb', 'reason'])

    print("-" * 40)
    print(f"Clean rows:  {len(clean_rows)} → {clean_output}")
    print(f"Review rows: {len(review_rows)} → {review_output}")
    print(f"Total:       {len(clean_rows) + len(review_rows)}")


if __name__ == "__main__":
    main()