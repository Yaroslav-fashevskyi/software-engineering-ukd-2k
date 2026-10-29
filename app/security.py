from datetime import datetime
from ipaddress import ip_address


def is_valid_ip(value: str) -> bool:
    try:
        ip_address(value)
    except ValueError:
        return False
    return True


def can_manage_accounts(role: str) -> bool:
    return role == "admin"


def is_api_key_valid(is_active: bool, expires_at: datetime, now: datetime) -> bool:
    return is_active and now < expires_at
