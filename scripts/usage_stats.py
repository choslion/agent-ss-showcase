#!/usr/bin/env python3
"""SS usage statistics — proof of daily use, derived from session logs.

Parses the dated session logs in sessions/ (YYYY-MM-DD.md) and reports total
session days, current streak, longest streak, this-month count, and span.
Stdlib only — no external dependencies.

Usage:
    python scripts/usage_stats.py
"""
import re
import sys
from datetime import date
from pathlib import Path

# Force UTF-8 output so Korean renders on Windows consoles (cp949 default).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = ROOT / "sessions"
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")


def load_session_dates():
    dates = []
    for f in SESSIONS_DIR.glob("*.md"):
        m = DATE_RE.match(f.name)
        if m:
            dates.append(date(int(m[1]), int(m[2]), int(m[3])))
    return sorted(set(dates))


def longest_streak(dates):
    best = run = 0
    prev = None
    for d in dates:
        run = run + 1 if prev and (d - prev).days == 1 else 1
        best = max(best, run)
        prev = d
    return best


def current_streak(dates):
    """Consecutive days counting back from the most recent session date."""
    streak = 1
    for earlier, later in zip(reversed(dates[:-1]), reversed(dates[1:])):
        if (later - earlier).days == 1:
            streak += 1
        else:
            break
    return streak


def main():
    dates = load_session_dates()
    if not dates:
        print("[SS 사용 통계] 아직 기록된 세션이 없습니다 (sessions/ 비어 있음).")
        return

    today = date.today()
    first, last = dates[0], dates[-1]
    cur = current_streak(dates)
    gap = (today - last).days
    if gap == 0:
        status = "오늘까지 active"
    elif gap == 1:
        status = "어제까지 (오늘 이어가면 유지)"
    else:
        status = f"{gap}일 전 끊김 (마지막 {last})"

    this_month = sum(1 for d in dates if (d.year, d.month) == (today.year, today.month))

    print("[SS 사용 통계]")
    print(f"  총 세션일 : {len(dates)}일")
    print(f"  현재 연속 : {cur}일 — {status}")
    print(f"  최장 연속 : {longest_streak(dates)}일")
    print(f"  이번 달   : {this_month}일")
    print(f"  기간      : {first} → {last}")


if __name__ == "__main__":
    main()
