"""Functions that clean and normalise raw field values."""

import phonenumbers


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