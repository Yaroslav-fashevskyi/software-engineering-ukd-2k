import pytest
from app.risk import calculate_risk_score


def test_tor_ip_with_three_reports_has_score_85():
    # Arrange
    reports, is_tor, is_vpn = 3, True, False
    # Act
    score = calculate_risk_score(reports, is_tor, is_vpn)
    # Assert
    assert score == 85


def test_score_capped_at_100():
    assert calculate_risk_score(10, True, True) == 100


def test_empty_risk_is_zero():
    assert calculate_risk_score(0, False, False) == 0


def test_negative_reports_rejected():
    with pytest.raises(ValueError, match="negative"):
        calculate_risk_score(-1, False, False)
