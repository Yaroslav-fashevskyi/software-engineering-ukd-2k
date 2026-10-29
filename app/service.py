from dataclasses import dataclass
from ipaddress import ip_address
from typing import Protocol

from .risk import calculate_risk_score


@dataclass(frozen=True)
class IPRecord:
    verified_reports: int
    is_tor: bool
    is_vpn: bool
    asn: int
    provider: str


class IPRepository(Protocol):
    def get_by_ip(self, ip: str) -> IPRecord | None: ...


class ReputationService:
    def __init__(self, repository: IPRepository):
        self.repository = repository

    def get_reputation(self, ip: str) -> dict | None:
        ip_address(ip)  # ValueError for invalid IPv4/IPv6 before repository access
        record = self.repository.get_by_ip(ip)
        if record is None:
            return None
        return {
            "ip": ip,
            "risk_score": calculate_risk_score(
                record.verified_reports, record.is_tor, record.is_vpn
            ),
            "asn": record.asn,
            "provider": record.provider,
        }
