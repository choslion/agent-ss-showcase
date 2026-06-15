---
description: Start a session — brief on current state
---

Start the session. Proceed in this order:

1. Run `git pull` to get the latest memory (another machine may have updated it).
   If it fails or there are conflicts, tell the user instead of guessing.
2. Read `state/current.md`, `state/todos.md`, and `state/goals.md`.
3. Read the most recent log in the `sessions/` folder.
4. Check today's date.
5. (Optional, personal integration) Pull a watchlist market summary and fold it into the brief:
   `python "<path-to>/stock-pro/scripts/brief_quotes.py" --min 1.0`
   This only works if the separate stock-pro project is present. If it errors or is missing, skip it.
6. Give a briefing:
   - What was in progress last session and what wasn't finished
   - Upcoming deadlines or items needing attention
   - A one-line watchlist market summary (notable movers only), if available
   - 1–3 recommended priorities for today

Keep the briefing under 10 lines. End with "What should we start with today?"
