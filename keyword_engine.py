
def calculate_opportunity_score(
    demand_score,
    competition_score,
    trend_score,
    buyer_intent_score,
    design_score
):
    """
    Scores are normalized from 0 to 100.
    Higher competition_score means more competition.
    """

    demand = max(0, min(100, demand_score))
    competition = max(0, min(100, competition_score))
    trend = max(0, min(100, trend_score))
    buyer_intent = max(0, min(100, buyer_intent_score))
    design = max(0, min(100, design_score))

    score = (
        demand * 0.30
        + (100 - competition) * 0.25
        + trend * 0.20
        + buyer_intent * 0.15
        + design * 0.10
    )

    return round(score, 1)
