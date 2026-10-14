# Timeline

## July 2026: the question and the first trap
- Start: can the referee and the teams predict cards and fouls better than a coin flip?
- Several seasons of history, a statistical model per target. Hold-out on a season the model has not seen.
- Result: the referee survives on cards, referee and teams on fouls, corners show nothing (used as a negative control).
- An xG strategy showed +96% ROI. The xG was measured after the match. Without the leak it did not work. Lesson: first check what was known before kick-off.
- Another league tested: player features did not help (difference below the standard error).

## August 2026: real prices and the pipeline
- Odds for cards from 5 Polish bookmakers found on public match pages and saved automatically before the match and at kick-off.
- Rounds 1 to 3 on real prices: a small positive start that disappeared round by round.
- The pipeline built step by step: seed of the round, referees, odds, results, statistics, consolidation, settlement.
- Round 6: first round with odds captured on time, first clean measurement of closing line value: about 0. Verdict: no edge on the cards market.

## September 2026: players and context
- Player IDs found in the line-up pages. Line-ups, events with minutes and 434 player profiles linked by ID.
- Four fixes of the line-up parser (IDs, duplicates on pages after the match, Polish inflection of team names, artefact IDs).
- Rounds 7 to 9 confirm the verdict: one sharp round, one quiet, one calm. The model aims at the middle.
- Match card with Host and Judge. Rules written from forward tests: a yellow is not a red, context works only with material.
- Coaches, weather and table position added as context, not as model inputs.
- Hypothesis about young players tested in four variants and rejected.

## October 2026: checks and automation
- Three more hypotheses rejected on 599 matches: national team break, rule change between seasons, coaches taking off booked players.
- The season correction checked against an independent source of referee averages: correct.
- Fouls per player per match from a second source, matched with my profiles by name.
- The match pages changed their structure mid-weekend. The scrapers were fixed, and a match is now saved only after the final whistle.
- One script per round: `stan` shows what is complete, `rozlicz` runs the whole settlement.
- Round 10: 9 of 9 matches complete. Model 3.61 cards per match, reality 4.89. A rule for round 11 was written before it: if round 11 is again about 4.5 per match, the season correction changes.
- Round 11 (17–18 October): first round where the whole chain should run by itself, from the match list to the verdict.
