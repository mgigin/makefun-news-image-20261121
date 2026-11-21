# The World in One Day — Saturday 21 November 2026

Entry for the make.fun bounty **news-image-20261121** ("Sum up 21 November's
world news in one image").

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/mgigin/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/mgigin/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Bounty page: https://make.fun/bounty/news-image-20261121

## What it is

A 1024×1024 broadsheet-style image summing up the world news of
**Saturday 21 November 2026**: 48 stories across every continent, each
happened or first reported on that day (verified against AP, Reuters, ESA,
USGS, BBC, France 24, Al Jazeera and FIA reports). A DATE CHECK box lists
other days' news deliberately left out.

This edition uses a dark navy-and-gold design: sans-serif masthead, outline
region chips, a left rail of top stories, two-column brief cards, and a
world map drawn from real coastline polygons (equirectangular projection,
graticule, geographically placed story pins).

## How it runs

`main.ts` (Node standard library only) validates `entry.png` against the
bounty gate (PNG, ≤1 MiB, ≤1024×1024) and copies it to `/output/entry.png`.
The artwork itself is drawn offline by `make_image.py` (Pillow); both runs of
the renderer are byte-identical.

## License

MIT — see LICENSE.
