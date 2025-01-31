from datetime import timedelta, datetime, timezone

from email_validator import validate_email, EmailNotValidError


def is_valid_email(recipient: str) -> bool:
    """
    Check if the given recipient is a valid email address.
    """
    try:
        validate_email(recipient)
        return True
    except EmailNotValidError:
        return False


def is_valid_telegram_id(recipient: str) -> bool:
    """
    Check if the given recipient is a valid Telegram ID.
    """
    return recipient.isdigit() and 5 <= len(recipient) <= 15


def validate_recipients(recipients: list[str] | str) -> tuple[list[str], list[str], list[str]]:
    """Validate recipients and categorize them into emails, telegram IDs, and invalid."""
    if isinstance(recipients, str):
        recipients = [recipients]

    valid_emails = [r for r in recipients if is_valid_email(r)]
    valid_telegram_ids = [r for r in recipients if is_valid_telegram_id(r)]
    invalid_recipients = [r for r in recipients if r not in valid_emails + valid_telegram_ids]
    return valid_emails, valid_telegram_ids, invalid_recipients


def calculate_eta(delay: int) -> datetime:
    """Calculate eta in UTC"""
    eta = datetime.now(timezone.utc)
    if delay == 1:
        eta += timedelta(hours=1)
    elif delay == 2:
        eta += timedelta(days=1)
    return eta
