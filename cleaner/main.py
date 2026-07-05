import argparse

"""Main entry point: runs the cleaning pipeline."""

from cleaner.normalisers import clean_row
from cleaner.validators import validate_row
from cleaner.io_helpers import load_csv, write_csv, strip_internal_fields

CLEAN_FIELDS = ['name', 'email', 'phone', 'dob', 'suburb']
REVIEW_FIELDS = CLEAN_FIELDS + ['reason']


def process(input_path, clean_output, review_output):
    """Load, clean, validate and route rows. Returns (clean_count, review_count)."""
    rows = load_csv(input_path)

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

    write_csv(clean_output, clean_out, CLEAN_FIELDS)
    write_csv(review_output, review_out, REVIEW_FIELDS)

    return len(clean_rows), len(review_rows)

def main():
    parser = argparse.ArgumentParser(
        description="Clean and validate a customer CSV export for migration."
    )
    parser.add_argument("input", help="Path to the messy input CSV")
    parser.add_argument(
        "--clean-output",
        default="output/clean.csv",
        help="Path for the cleaned output file (default: output/clean.csv)"
    )
    parser.add_argument(
        "--review-output",
        default="output/review.csv",
        help="Path for the review output file (default: output/review.csv)"
    )

    args = parser.parse_args()

    clean_count, review_count = process(
        args.input,
        args.clean_output,
        args.review_output
    )

    print("=" * 50)
    print("MIGRATION CLEANER REPORT")
    print("=" * 50)
    print(f"Input file:      {args.input}")
    print(f"Clean output:    {args.clean_output} ({clean_count} rows)")
    print(f"Review output:   {args.review_output} ({review_count} rows)")
    print(f"Total processed: {clean_count + review_count} rows")
    print("=" * 50)

if __name__ == "__main__":
    main()