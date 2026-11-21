# makefun-news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/mgigin/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/mgigin/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

"The World in One Page" — Saturday 21 November 2026: one 1024×1024 image that
sums up the day's world news. A newspaper front page drawn with Pillow
primitives (no photographs, no copied artwork): the Russian missile strike on
Poland leads, with the Shenzhen three-way summit, the Iran war, Anthropic's
slide, the ICJ genocide-ruling backlash and Japan–India defence ties below,
plus four briefs. `main.ts` validates the PNG against the bounty gate
(signature, size, dimensions, whole chunk list with CRCs) and copies it to
the grader's output directory; `make_image.py` is the offline generator that
drew `entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=c6yw2yzb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards · Referral: https://make.fun/r/c6yw2yzb</sub>
