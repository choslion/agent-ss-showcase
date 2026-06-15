---
description: Show SS usage stats (session-day count + streaks) as daily-use evidence
---

Show how consistently SS has been used — the "I actually use this daily" evidence.

Run this command and present the output to the user:

```
python scripts/usage_stats.py
```

Notes:
- The script reads the dated logs in `sessions/` (YYYY-MM-DD.md) and computes total
  session days, current streak, longest streak, this-month count, and the active span.
  Stdlib only — nothing to install, no network.
- Present the result as-is. If the user wants the one-liner for a README/portfolio,
  offer a summary like: "N session days, longest streak M days, since <start date>".
- These numbers only grow when sessions are actually logged with `/end`. Don't fabricate
  or pad them — the honesty is the point of the metric.
