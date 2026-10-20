# Findings

Every finding has its sample size. Small samples are marked as hypotheses.

## 1. What survived

### The referee moves the number of cards
- 28 referees, on average about 21 matches of history each.
- From 3.94 to 5.51 cards per match: a spread of 1.57 cards between the most lenient and the strictest referee.
- Hold-out season (297 matches): with the rule "over if the model probability > 0.60, under if < 0.40, otherwise no decision" the model made 204 decisions and was right in 66.2%. The league base rate was 60.9%.
- The higher the confidence, the better: threshold 0.65 → 107 decisions, 72.0%; threshold 0.70 → 57 decisions, 79%.
- When the model did not decide (93 matches), the real over rate was 49.5%. It knows when it does not know.
- Calibration is good but slightly too high: when the model said about 65%, the real rate was 61.2%.
- The edge was positive in all three parts of the season, but weak in the last third.

### The correction for the current season is right
- History says 4.66 cards per match, the current season says 3.66. The correction of −1.0 brings the referees down to this season.
- Checked against an independent source of referee averages per season: the numbers match (for several referees exactly).
- Almost changed by mistake: the first comparison was against old seasons and looked like "baseline too low". One extra query showed the mistake. Measure before you believe.

### Fouls are not cards
- Matches with 28 to 33 fouls ended with 1 to 4 cards.
- A referee with 31 fouls per match had fewer cards than a referee with 26 fouls per match.
- A team with 17 fouls and 1.4 cards per match, another with 11.3 fouls and 2.67 cards.

### Cards: referee alone. Fouls: referee and teams.
- On the hold-out, teams make the cards prediction worse (overfit), but make the fouls prediction better.
- That the best model depends on the target in a way that makes sense is a sign of a real signal, not noise.

## 2. What did not survive

### No edge over the bookmakers
- Round 6, first clean test with prices before the match: 28 bets, closing line value raw −0.2%, adjusted −0.4%. Rounds 7 to 9: the same picture.
- The market margin on cards is about 8.8%, and the bookmakers agree with each other within 1 to 3 percentage points.
- A small test on rounds 1 to 3 showed how small samples lie: ROI on the line 3.5 went +20% → −2% → −26%. The first round looked like an edge.

### Two false edges caught before they were believed
- A model that was not calibrated gave +41% "edge" against prices. It was a disagreement of a wrong model with the price, not information.
- One bookmaker's cards market did not count second yellows and bench cards. Different definition, higher over prices, a false +64%. That bookmaker is excluded.

### Rejected hypotheses
| Hypothesis | Test | Result |
|---|---|---|
| Young players (≤21) get more cards | 4 variants | Grouped 0.255 vs 0.179 yellow per 90 looks like a signal, but by year of age it is not monotonic: everything comes from the 21-year-olds (n=10). Young late substitutes: 0 cards in 58 appearances. Rejected. |
| More cards after a national team break | 599 matches, 2 seasons | 4.32 vs 4.42. No effect. |
| A rule change makes a step between seasons | 2 seasons | 4.30 vs 4.38. No effect. Only a weak pattern: early rounds a bit higher than late rounds. |
| Coaches take off booked players | substitutions by position | Crude 33.3% vs 24.6% falls to 29.1% vs 27.7% when the position is controlled. Rejected. |
| xG strategy with +96% ROI | check of the data | The xG was from after the match. Without the leak the strategy does not work. |
| Player features on fouls in another league | 759 test matches | Referee alone MAE 4.24, full model 4.16. The difference is below the standard error. |

### The model does not "systematically underestimate"
- After round 7 (5.25 cards per match) it looked like the model is too low by 1.4. Round 6 had 2.56, round 8 had 3.1. The model aims at the middle, and that is the best it can do. A higher correction would have fixed round 7 and broken round 8.

## 3. Hypotheses still open (small samples)

| Idea | What I saw | n |
|---|---|---|
| Context works only with material | Derby + card-prone squad → 7 cards. Derby + two clean squads + new coach → 4 cards, exactly the baseline. | 2 |
| A strict referee needs a physical match | Baseline 4.25 → 7 cards in a physical match (27 fouls). Baseline 4.17 → 3 cards when one team dominated calmly (68% possession, 7 fouls). | 2 |
| Coach under pressure, two directions | Coach close to dismissal at home → careful game, 2 cards. On the road at the leader → 6 cards. | small |
| Heat cools the game | Same referee at ≥ 28 °C: about 0.5 cards fewer than in moderate weather. Found backwards, to be tested forward. | 12 |
| Cup match in the week cools | Two teams after a European match: below baseline (−1.8 and −0.7). | 2 |
| Referee alone on fouls | Round 10: did not beat a flat average (3.77 vs 3.79). The players on the pitch are needed. | 7 |

These are tested forward, match by match. None of them is in the model.

## 4. Players and scouting

- 434 player profiles with fouls, cards, duels, tackles, passes and minutes, linked to line-ups and events by player ID.
- Card risk is a property of the player (yellow per 90 + fouls per 90, min. 180 minutes), not of age.
- A ranking of young players by minutes exists. The next step is a real question from a club or an academy, not more model.

## 5. Round 11: common-sample audit

Round 11 (9 matches) was fully settled: 9/9 matches, no missing outcomes.
The prediction and context checksums passed.

### Cards
- On the 8 matches with a closing-market value, model MAE was 1.30, compared with 1.38 for the constant baseline and 1.54 for the closing market.
- The model's log-loss on the market line was 0.6728, compared with 0.7959 for the market (8 matches).
- One match was excluded from this comparison because its closing-market average was missing.

### Fouls
- On the 8 matches with a referee foul prediction, constant-baseline MAE was 4.62, full-model MAE was 4.77, and referee-only MAE was 5.49.
- One match was excluded from this comparison because the referee foul prediction was missing.

These are small-sample results from one round. They do not establish a durable model advantage or an edge over bookmakers. The model was not changed: the pre-defined R1 condition was not met (3.22 actual cards per match, below the 4.5 threshold).
