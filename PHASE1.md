# PHASE 1 — news-image-20261125

## Summary
- 36 stories, all researched 25 Nov 2026 (08:30–09:00 WIB) and dated
  Wednesday 25 November 2026: 3 heroes + 9 briefs + 24 numbered.
- Heroes: Trump readies sweeping new tariffs (Reuters/BBC); Nvidia
  bounce fades, shares slide 6% (Reuters Trading Day/BBC); Israeli
  strike kills Hamas internal security chief in Gaza (BBC).
- Playbook reproduced from 20261124 (submitted + accepted, kit 14/0/5):
  dense front page + world map, masthead "THE WORLD TODAY", dateline
  Wednesday 25 November 2026. `compose.py` written fresh in this session
  (same layout, new tariff / falling-chip / blast hero art, new stories,
  stats, markers, date check).
- No 20261124 stories or pixels reused; entry.png drawn fresh by compose.py.

## Files (~/workspace/makefun/entries/news-image-20261125/)
- STORIES.md — 36 stories with source + date each, plus DATE CHECK section
- compose.py — PIL renderer (deterministic)
- entry.png — 1024×1024, 151,873 bytes (≤1 MiB), sha256
  9d736b89200a107cfd96c8a0f052f5ce4b3d81583e4ef98ffa6b523f4201b15d
- main.ts — Node 22 stdlib only, copies entry.png to $MAKEFUN_OUTPUT_DIR
- README.md — badges + run instructions (Phase 2)

## Verification
- `python3 compose.py` → final y = 1015 (canvas 1024), no assertion
  failures (all 24 numbered headlines fit one line).
- Viewed entry.png at full size: masthead, ticker, stat strip, 3 heroes,
  9 briefs, world map with 12 red markers, DATE CHECK box, 24 numbered
  items, footer all legible; no overlapping or garbled text.
- Defect found and fixed: brief B3 headline "China launches mission with
  Pakistani astronaut" was cut to "China launches mission with Pakistani"
  by the 1-line cap. Shortened to "China flies Pakistani astronaut" and
  re-measured: all 9 brief headlines now fit one line (max 268.7px of
  278px); re-rendered and re-checked.
- Hero decks H1/H2/H3 all end cleanly at the 3-line cap (verified in the
  full-size view).
- `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts` → out/entry.png
  byte-identical to entry.png (sha256 match).
- Kit for this competition downloaded fresh (HTTP 200, 8,430,093 bytes)
  to ~/workspace/makefun/news-image-20261125-kit/ — no 503 fallback
  needed this time.

## Notes / needs fixing
- Dating caveat documented in STORIES.md: several items are Wednesday
  developments of Tuesday events (tariff probe, Nvidia fallout, Iowa
  explosives); the DATE CHECK box names the earlier events they follow.
  Near-misses caught and left out: Huang's reinstatement (Mon 23 Nov),
  Democrats' House majority (Tue 24 Nov), CrowdStrike–Zscaler (Mon
  23 Nov), Indonesia factory fire (Tue 24 Nov), COP31 collapse (Sun
  22 Nov).
- Phase 2 still to do: GitHub repo, badges/About, bundle, submit.
  (Not touched here per the task.)
