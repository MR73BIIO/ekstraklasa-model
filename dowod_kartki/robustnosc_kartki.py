#!/usr/bin/env python3
"""
ROBUSTNOŚĆ KARTKI — stress-test przewagi +5.2 z dowod_kartki.py.
Te same rozegrane mecze 25/26. Sprawdza 3 rzeczy, których headline nie mówi:
 1. STABILNOŚĆ w czasie (podział sezonu na 3 części) — czy edge trzyma
    wszędzie, czy to jeden szczęśliwy odcinek.
 2. KALIBRACJA — czy wyższe p_ref realnie oznacza więcej over (jakość sygnału).
 3. KRZYWA PROGU — jak zmienia się liczba typów i trafność przy podnoszeniu progu.
Nie tyka progów headline'u; pokazuje pełny obraz, nie dobiera pod wynik.
"""
import csv
from pathlib import Path

CSV = Path("/root/audit/models/etapA_predykcje_cards.csv")
SEASON = "2025/2026"


def load():
    rows = []
    with open(CSV, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r.get("Season") != SEASON:
                continue
            if (r.get("over") or "").strip() == "":
                continue
            try:
                rows.append((r["Date"][:10], float(r["p_ref"]), int(float(r["over"]))))
            except (ValueError, KeyError):
                continue
    rows.sort(key=lambda x: x[0])
    return rows


def acc_edge(subset, thr=0.60):
    n = len(subset)
    if n == 0:
        return 0, 0, 0.0, 0.0, 0.0
    base = sum(o for _, _, o in subset) / n
    bets = [(p, o) for _, p, o in subset if p > thr]
    nb = len(bets)
    acc = sum(o for _, o in bets) / nb if nb else 0.0
    return n, nb, base, acc, (acc - base)


def main():
    rows = load()
    N = len(rows)
    print("=" * 60)
    print(f"  ROBUSTNOŚĆ KARTKI — sezon {SEASON}, {N} meczów")
    print("=" * 60)

    # 1. STABILNOŚĆ W CZASIE (3 równe części)
    print("\n[1] STABILNOŚĆ — sezon podzielony na 3 części po dacie")
    print("-" * 60)
    k = N // 3
    parts = [rows[:k], rows[k:2*k], rows[2*k:]]
    labels = ["Część 1 (start)", "Część 2 (środek)", "Część 3 (końcówka)"]
    for lab, part in zip(labels, parts):
        n, nb, base, acc, edge = acc_edge(part)
        print(f"  {lab:22} n={n:3}  zakł={nb:3}  "
              f"traf={acc:.1%}  tło={base:.1%}  edge={edge:+.1%}")
    print("  (edge dodatni we WSZYSTKICH 3 = przewaga stabilna,")
    print("   nie jeden szczęśliwy odcinek)")

    # 2. KALIBRACJA — czy wyższe p_ref = więcej realnych over
    print("\n[2] KALIBRACJA — realny odsetek over wg przedziału p_ref")
    print("-" * 60)
    buckets = [(0.0, 0.40), (0.40, 0.50), (0.50, 0.60),
               (0.60, 0.70), (0.70, 1.01)]
    for lo, hi in buckets:
        sub = [(p, o) for _, p, o in rows if lo <= p < hi]
        n = len(sub)
        if n == 0:
            print(f"  p_ref [{lo:.2f},{hi:.2f})  n=  0  —")
            continue
        real = sum(o for _, o in sub) / n
        mid = (lo + hi) / 2
        flag = "OK" if abs(real - mid) < 0.10 else "rozjazd"
        print(f"  p_ref [{lo:.2f},{hi:.2f})  n={n:3}  "
              f"model~{mid:.0%}  realnie over={real:.1%}  [{flag}]")
    print("  (realny over rosnący z przedziałem = sygnał niesie informację)")

    # 3. KRZYWA PROGU
    print("\n[3] KRZYWA PROGU — im wyżej próg, tym mniej ale pewniej?")
    print("-" * 60)
    base_all = sum(o for _, _, o in rows) / N
    print(f"  tło ligi (baseline): {base_all:.1%}")
    for thr in [0.55, 0.60, 0.65, 0.70]:
        _, nb, _, acc, edge = acc_edge(rows, thr)
        print(f"  próg {thr:.2f}  zakł={nb:3}  traf={acc:.1%}  edge={edge:+.1%}")
    print("  (jeśli traf rośnie z progiem = model dobrze rankuje pewność)")
    print("=" * 60)


if __name__ == "__main__":
    main()
