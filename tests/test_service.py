from unittest.mock import Mock
import pytest
from app.service import IPRecord, IPRepository, ReputationService


def test_get_reputation_reads_repository_once():
    # ARRANGE
    repository = Mock(spec=IPRepository)
    repository.get_by_ip.return_value = IPRecord(
        verified_reports=2, is_tor=False, is_vpn=True,
        asn=15169, provider="Example ISP"
    )
    service = ReputationService(repository)

    # ACT
    result = service.get_reputation("8.8.8.8")

    # ASSERT
    assert result["ip"] == "8.8.8.8"
    assert result["risk_score"] == 45
    assert result["asn"] == 15169
    repository.get_by_ip.assert_called_once_with("8.8.8.8")


def test_missing_ip_returns_none():
    repository = Mock(spec=IPRepository)
    repository.get_by_ip.return_value = None
    result = ReputationService(repository).get_reputation("8.8.4.4")
    assert result is None
    repository.get_by_ip.assert_called_once_with("8.8.4.4")


def test_invalid_ip_does_not_call_repository():
    repository = Mock(spec=IPRepository)
    with pytest.raises(ValueError):
        ReputationService(repository).get_reputation("invalid-ip")
    repository.get_by_ip.assert_not_called()
