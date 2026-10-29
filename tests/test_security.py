from datetime import datetime, timedelta, timezone
from app.security import can_manage_accounts, is_api_key_valid, is_valid_ip


def test_ipv4_and_ipv6_are_valid():
    assert is_valid_ip("8.8.8.8")
    assert is_valid_ip("2001:4860:4860::8888")


def test_invalid_ip_rejected():
    assert not is_valid_ip("999.8.8.8")


def test_admin_can_manage_accounts():
    assert can_manage_accounts("admin")


def test_user_cannot_manage_accounts():
    assert not can_manage_accounts("user")


def test_active_unexpired_key_allowed():
    now = datetime(2026, 10, 29, tzinfo=timezone.utc)
    assert is_api_key_valid(True, now + timedelta(days=1), now)


def test_inactive_or_expired_key_rejected():
    now = datetime(2026, 10, 29, tzinfo=timezone.utc)
    assert not is_api_key_valid(False, now + timedelta(days=1), now)
    assert not is_api_key_valid(True, now - timedelta(seconds=1), now)
