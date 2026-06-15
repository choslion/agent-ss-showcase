---
description: Show the current market situation for my stock-pro watchlist
---

Show the current market situation for my stock-pro watchlist.

Run this command and present the output to the user:

```
python "<path-to>/stock-pro/scripts/brief_quotes.py"
```

Notes:
- This is a personal integration with the separate [stock-pro](https://github.com/choslion/stock-pro)
  project. The script reads the shared watchlist (`src/config/watchlist.json`) and reuses the
  backend's `get_watchlist()` directly — no server needs to be running.
- It scrapes live KR/US quotes, so it can take 10–30 seconds.
- Present the result as-is; it already lists the biggest movers first.
- If the user only wants meaningful moves (e.g. "1% 이상만"), append a threshold: `... --min 1.0`.
- If the script errors (network, scraping) or stock-pro isn't present, tell the user plainly.
  Never invent prices.
