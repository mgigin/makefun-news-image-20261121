# The World in One Day — Saturday 21 November 2026

Entry for the make.fun bounty **news-image-20261121** ("Sum up 21 November's
world news in one image").

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/mgigin/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/mgigin/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Bounty page: https://make.fun/bounty/news-image-20261121

Referral: https://make.fun/r/c6yw2yzb

## What it is

A 1024×1024 cream broadsheet summing up the world news of
**Saturday 21 November 2026**: 48 stories across six regions, each happened
or first reported on that day (verified against AP, Reuters, AFP, BBC,
Al Jazeera, Kyiv Post, USGS, ESA and FIA reports). A DATE CHECK box lists
other days' news deliberately left out.

Layout: serif masthead, six-stat band, region chips, three illustrated lead
panels, ten brief cards with original spot illustrations, a world map drawn
from real coastline polygons (equirectangular projection, graticule,
geographically placed story pins), and a numbered list of 35 further
stories. All artwork is original, drawn in code.

Fact notes from verification: the Kryvyi Rih toll is 2 killed / 58 injured
(42 was the stale Friday-night count); three ballistic missiles were
downed over Riyadh early Saturday (the Jazan pair was Friday evening);
Verstappen inherited Las Vegas pole after Antonelli's grid penalty; India
closed day three at Wellington on 486/4 with Rahul on 136.

## How it runs

`main.ts` (Node standard library only) validates `entry.png` against the
bounty gate (PNG, ≤1 MiB, ≤1024×1024) and copies it to `/output/entry.png`.
The artwork itself is drawn offline by `make_image.py` (Pillow); both runs of
the renderer are byte-identical.

## License

MIT — see LICENSE.
