---
description: End a session — save summary and update state
---

End the session. Do the following:

1. Summarize what happened this session: completed work, decisions made, new tasks, unresolved items.
2. Save it to `sessions/YYYY-MM-DD.md` (if this is the second session of the day, append a `## Session 2` section to the existing file):

```markdown
# Session Log — YYYY-MM-DD

## Done
- ...

## Decisions
- ...

## Next Up
- ...
```

3. Update `state/current.md` — so that the next session can continue from this file alone.
4. Add new tasks to `state/todos.md` and check off completed items.
5. If important decisions were made, record them in `state/decisions.md` with the date and reasoning.
6. Sync memory to GitHub: `git add -A`, commit with message `session: YYYY-MM-DD`, and `git push`.
   (This keeps other machines up to date. If push fails, tell the user — don't force-push.)
7. Show the user a 3–5 line session summary and say goodbye.
