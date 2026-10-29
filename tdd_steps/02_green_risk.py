def calculate_risk_score(verified_reports, is_tor, is_vpn):
    return min(100, verified_reports * 15 + int(is_tor) * 40 + int(is_vpn) * 15)
