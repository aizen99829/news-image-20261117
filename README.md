[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/aizen99829/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/aizen99829/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# news-image-20261117 — "The World in One Day"

One poster summing up **Tuesday 17 November 2026** in a single image.

- **Hero:** KERCH BRIDGE COLLAPSES — Ukraine's strike drops the road arch
  into the sea; rail runs on one track; 2 killed in Crimea. Hours earlier,
  Russia hit Kyiv's North & South bridges.
- **Iran:** drones target the US base in Bahrain — intercepted, no damage.
- **Nvidia:** $115.8BN revenue, up 103%; board will not reinstate Huang.
- **Measles:** US loses measles-free status after 26 years; 5,412 cases.
- **Trump:** in Manila for the Quad, then Shenzhen ahead of Thursday's
  first Trump–Xi–Putin trilateral.
- **Also today:** Pentagon 9th failed audit ($4.8T unverified), Russian
  An-12 crash in Siberia (19 dead), UK sanctions on 8 West Bank settlement
  firms, Japan scrambles jets over suspected Russian planes.

Facts verified against `../work-news-image-20261117/RESEARCH.md`
(≥2 independent sources per story).

## Build

`tools/render.py` (Python 3 + PIL, stdlib-style deterministic drawing, no
network, no randomness) renders `assets/poster.png` (1024×1024).

`main.ts` (Node stdlib only) copies `assets/poster.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`. Two runs produce byte-identical output.
