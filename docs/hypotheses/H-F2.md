# H-F2: do unbalanced matches have fewer cards?

Written on 4 November 2026, before any calculation. The thresholds below do not change after the result.

## Why

The cards model uses the referee only. Over Rounds 11 to 13 it was level with a flat average (MAE 1.645 vs 1.605, 25 matches).
A common belief says that when one team is a clear favourite, it controls the game and there are fewer cards.
If that is true, it is a second signal known before kick-off, next to the referee.

What this test can NOT do: beat the bookmakers on cards. The same bookmakers set the 1X2 prices, so the favourite is most likely
already in the cards price. The goal is a more accurate model, not an edge.

## Data

- Closing 1X2 prices (market average) from football-data.co.uk, Ekstraklasa 2020/21 to 2026/27. Free, results and 1X2 odds only.
- Cards (yellow cards of players, as in the model) and the referee estimate from my own database.
- Imbalance I = |p_home - p_away|, where p are the closing 1X2 probabilities with the margin removed.
- Matches are joined by date and teams. A match that cannot be joined is listed, not guessed.

## Samples

- **Fit:** all seasons before 2026/27 that have cards and a referee estimate in my database.
- **Test:** 2026/27, Rounds 1 to 13 (already played, not used in the fit).
- **Forward:** Rounds 14 to 17, after each round is settled by the engine.

## Thresholds

- **H-F2a (direction, fit sample):** matches in the top third of I have at least 0.30 fewer cards than the bottom third,
  measured on the residual (cards minus referee estimate), so the referee effect is removed first.
- **H-F2b (test sample):** referee estimate + imbalance term (one slope, fitted on the fit sample only) has a lower MAE than the
  referee estimate alone by at least 0.05 cards per match on Rounds 1 to 13 of 2026/27.
- **H-F2c (forward):** on Rounds 14 to 17 the same model is not worse than the referee estimate alone (MAE difference >= 0).

## Verdict

- a fails: REFUTED, the belief does not hold in this league.
- a and b pass, c pending: PROMISING, nothing changes in the model yet.
- a, b and c pass: CONFIRMED. The imbalance term can enter the model only through a separate decision written before a round,
  as with every model change.
- a passes, b fails: the effect exists but is too small to help the prediction.
