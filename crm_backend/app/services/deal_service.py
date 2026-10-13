from decimal import Decimal
from app.models.deal import DealStage

DEFAULT_PROBABILITIES = {
    DealStage.NEW: 10,
    DealStage.QUALIFICATION: 25,
    DealStage.PROPOSAL: 50,
    DealStage.NEGOTIATION: 75,
    DealStage.WON: 100,
    DealStage.LOST: 0,
}

def probability_for_stage(stage: DealStage, override: int | None = None) -> int:
    return override if override is not None else DEFAULT_PROBABILITIES[stage]

def pipeline_value(value: Decimal, probability: int) -> Decimal:
    return value * Decimal(probability) / Decimal(100)
