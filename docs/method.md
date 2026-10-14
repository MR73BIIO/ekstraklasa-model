# Method

## The question

Before a match: how many yellow cards and how many fouls should we expect?
After the match: was the expectation better than a simple constant, and better than the bookmakers' line?

## Data

- **Match pages** (public): referee, line-ups with player IDs, events with minutes (cards, goals, substitutions), team statistics, weather.
- **Player profiles** (public): 434 players with fouls, cards, duels, tackles, passes, minutes, age, market value.
- **League history:** several past seasons of Ekstraklasa matches with referee and cards, used for training and for the hold-out test.
- **Coaches:** tenure in months and points per match, updated by hand when a coach changes.
- **Odds:** over/under lines for cards from 5 Polish bookmakers, saved before the match and at kick-off. Odds for cards appear only after the referee is announced.
- **A paid statistics service** for fouls per player per match, used to check my own player numbers. The two sources agree within about 0.2 fouls for most players.

Everything goes into one SQLite database on my server. Each match has one ID built from the round and the team names.

## What counts as a card

- `cards` = yellow cards of players.
- A second yellow is counted by the source as a red card, so it is not in the yellow count.
- Cards for coaches and staff do not count.
- Checked on 79 matches: 0 differences between my count and the match statistics.

The bookmakers' "cards" line usually counts yellow and red together. So the model is never compared with the market without the red cards added. One early "edge" disappeared exactly because of this.

## The cards model

1. **Referee λ:** average cards per match in the referee's history, shrunk towards the league average when he has few matches.
2. **Season correction:** the current season is lower than the history. The baseline is λ − 1.0. This correction is re-calculated from the database (last check: 76 matches, −0.998), never taken from memory.
3. **Prediction** = corrected λ of the referee.

Team and player layers were tested on top of the referee. On cards they made the hold-out result worse, so they are not in the cards model.

## The fouls model

Referee + both teams, and in the next step the fouls of the players who actually start. On fouls the teams do help on the hold-out, unlike on cards.

## Testing

- **Time split:** trained on older seasons, tested on a season the model has not seen.
- **No look-ahead:** only information available before kick-off. Every value has the time it became known.
- **Baseline first:** every new signal is compared with the referee alone and with a flat league average.
- **Market test:** the model's probability is compared with the bookmakers' price before the match, and with the price at kick-off (closing line value). This is the only number that says whether there is an edge.
- **Forward test:** a prediction for a match is written down before the match and checked after it. A context idea (coach, derby, cup, weather) enters a match card as a hypothesis before kick-off, never as a rule fitted afterwards.

## The match card

For every match one card with 8 inputs: referee and baseline, card-prone players in the squads, fouls per player, scorers, young players, table position and form, coach and his situation, weather.

Two voices on the card:
- **Host** marks coincidences: a coach under pressure, a card-prone player, a strict or lenient referee, heat over 28 °C.
- **Judge** checks them: is it one match or a sample, is something counted twice, is the market already pricing it.

The card describes a match. It does not give a betting tip.

## Rules written before a round

Each round has its rule for what happens with each result, written before the matches. Example before round 11: if round 11 again has about 4.5 cards per match with normal results, the season correction is changed. If not, the model stays.
