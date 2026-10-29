POINTS_PER_REPORT = 15
TOR_POINTS = 40
VPN_POINTS = 15
MAX_RISK_SCORE = 100


def calculate_risk_score(verified_reports: int, is_tor: bool, is_vpn: bool) -> int:
    if verified_reports < 0:
        raise ValueError("verified_reports must not be negative")
    score = (verified_reports * POINTS_PER_REPORT
             + (TOR_POINTS if is_tor else 0)
             + (VPN_POINTS if is_vpn else 0))
    return min(score, MAX_RISK_SCORE)
