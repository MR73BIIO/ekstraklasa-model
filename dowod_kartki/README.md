# Referee → cards: holdout check, season 2025/26

Standalone check from 8.08.2026, kept exactly as it ran on the VPS.

**Data:** `etapA_predykcje_cards.csv` holds out-of-sample predictions for Ekstraklasa 2025/26. The model was trained on 2023/24 and 2024/25 and uses referee features only.

**Rule, fixed before looking at the result:**
- p_ref > 0.60 → OVER
- p_ref < 0.40 → UNDER
- anything in between → ABSTAIN

## Result

| Threshold | Calls | Hit rate | Over league base rate |
|---|---|---|---|
| 0.60 | 204 of 297 | 66.2% | +5.2 pts |
| 0.65 | 107 | 72.0% | +11.0 pts |
| 0.70 | 57 | 79% | +18.0 pts |

- The league base rate is 60.9%.
- In the 93 ABSTAIN matches the real over rate was 49.5%, so the model held back where the outcome was a coin flip.
- Calibration: the real over rate rises with p_ref, and p_ref sits slightly above it.
- Stability: the edge was positive in all three parts of the season (+6.6 / +7.2 / +1.6). The last third is thin.

## What this is not

This measures hit rate against the league base rate, not against a bookmaker line. The referee signal is public, so this file says nothing about beating the market.

## Files

- `dowod_kartki.py`: the check at threshold 0.60
- `robustnosc_kartki.py`: stability, calibration and the threshold curve
- `etapA_predykcje_cards.csv`: input predictions

Polski · Deutsch · Русский · English
