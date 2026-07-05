"""Functions that check whether a cleaned row is safe to import."""


def is_valid_email(email):
    """Check if an email looks valid."""
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