"""Main entry point: runs the cleaning pipeline."""

from cleaner.normalisers import clean_row
from cleaner.validators import validate_row
from cleaner.io_helpers import load_csv, write_csv, strip_internal_fields


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