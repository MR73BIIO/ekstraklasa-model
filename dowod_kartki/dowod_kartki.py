#!/usr/bin/env python3
"""
DOWÓD KARTKI — samodzielny backtest sygnału referee->cards.
Nie dotyka VORO. Czyta lipcowy plik predykcji, bierze holdout
2025/2026, stosuje regułę decyzyjną na p_ref (model TYLKO-sędzia),
porównuje z realnym 'over', i mierzy przewagę NAD baseline ligi.

Anti-leak: p_ref policzone anti-leak w holdoutcie, 'over' to
wynik PO meczu. Zero wycieku.
"""
import csv
from pathlib import Path

CSV = Path("/root/audit/models/etapA_predykcje_cards.csv")
HOLDOUT_SEASON = "2025/2026"

# Reguła decyzyjna na p_ref (prawdopodobieństwo OVER z modelu):
#   p_ref > GORNY  -> stawiamy OVER
#   p_ref < DOLNY  -> stawiamy UNDER
#   pomiędzy       -> ABSTAIN
GORNY = 0.60
DOLNY = 0.40


def main():
    n_all = 0
    over_total = 0                       # ile meczów realnie poszło OVER (baseline)
    bet_over = bet_over_hit = 0
    bet_under = bet_under_hit = 0
    abstain = abstain_over = 0

    with open(CSV, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["Season"] != HOLDOUT_SEASON:
                continue
            if row["over"].strip() == "":   # mecz nierozstrzygnięty
                continue
            try:
                p = float(row["p_ref"])
                over = int(float(row["over"]))
            except (ValueError, KeyError):
                continue

            n_all += 1
            over_total += over

            if p > GORNY:
                bet_over += 1
                bet_over_hit += (over == 1)
            elif p < DOLNY:
                bet_under += 1
                bet_under_hit += (over == 0)
            else:
                abstain += 1
                abstain_over += (over == 1)

    bets = bet_over + bet_under
    hits = bet_over_hit + bet_under_hit
    bet_acc = hits / bets if bets else 0.0

    # BASELINE: tło ligi. Skoro model stawia prawie zawsze OVER,
    # uczciwe porównanie = "co gdybym stawiał ZAWSZE OVER na wszystkich meczach".
    base_over_rate = over_total / n_all if n_all else 0.0

    print("=" * 52)
    print("  DOWÓD KARTKI — holdout", HOLDOUT_SEASON)
    print("=" * 52)
    print(f"Mecze w holdoutcie        : {n_all}")
    print(f"Prog OVER (p_ref >)       : {GORNY}")
    print(f"Prog UNDER (p_ref <)      : {DOLNY}")
    print("-" * 52)
    print(f"Postawione (BET)          : {bets}")
    print(f"  trafione                : {hits}")
    print(f"  TRAFNOSC BET            : {bet_acc:.1%}")
    print(f"  z tego OVER             : {bet_over}"
          + (f"  (traf {bet_over_hit}/{bet_over} = {bet_over_hit/bet_over:.1%})"
             if bet_over else ""))
    print(f"  z tego UNDER            : {bet_under}"
          + (f"  (traf {bet_under_hit}/{bet_under} = {bet_under_hit/bet_under:.1%})"
             if bet_under else ""))
    print("-" * 52)
    print(f"Wstrzymane (ABSTAIN)      : {abstain}")
    if abstain:
        print(f"  z tego realnie OVER     : {abstain_over}"
              f"  ({abstain_over/abstain:.1%})")
        print("  (~50% = slusznie unikane, model wie ze nie wie)")
    print("=" * 52)
    print("  BASELINE — tlo ligi")
    print("=" * 52)
    print(f"Realny odsetek OVER (cala liga) : {base_over_rate:.1%}")
    print(f"Trafnosc gdybys stawial ZAWSZE OVER na WSZYSTKICH: {base_over_rate:.1%}")
    print("-" * 52)
    edge = bet_acc - base_over_rate
    print(f"PRZEWAGA MODELU (BET - baseline) : {edge:+.1%}")
    print("=" * 52)
    if edge >= 0.05:
        print("WERDYKT: przewaga REALNA — model bije tlo ligi")
        print("o wiecej niz szum. Selekcja meczow ma sens.")
    elif edge > 0.0:
        print("WERDYKT: przewaga CIENKA — model lekko nad tlem,")
        print("ale blisko granicy szumu. Ostroznie.")
    else:
        print("WERDYKT: BRAK przewagi — trafiasz tyle, co stawiajac")
        print("na slepo OVER. Sygnal to tlo ligi, nie edge.")
    print("=" * 52)


if __name__ == "__main__":
    main()
