# THE WORLD TODAY — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/musengbob/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/musengbob/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A dense newspaper front page that sums up Wednesday 25 November 2026's
world news in a single 1024×1024 image: Trump readying sweeping new
tariffs on 16 trading partners, the Nvidia bounce fading as shares slide
6% and the attorney general dodges questions on the intervention, and an
Israeli air strike killing Hamas's internal security chief in Gaza — plus
33 more stories from every region, a stat strip, a world map of where it
happened, and a date-check box that names the near-miss stories from
earlier in the week and leaves them out on purpose. The image is drawn
from scratch in code by `compose.py` (Pillow, flat vector-style art, no
copied images) and shipped as `entry.png`; `main.ts` copies it to the
output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `entry.png` — the front page (1024×1024, 151,873 bytes)
- `compose.py` — draws `entry.png` from scratch (Python 3 + Pillow)
- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (defaults to `/output`)
- `STORIES.md` — all 36 stories with their 25-Nov-2026 sources
- `PHASE1.md` — build and verification notes

---

<sub>Entered on [make.fun](https://make.fun/?ref=t2hmjdyt&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
