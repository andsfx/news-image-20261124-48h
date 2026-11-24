[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/andsfx/news-image-20261124-48h/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/andsfx/news-image-20261124-48h/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single 1024x1024 image that summarises the world news of 24 November 2026. Six panels cover the United States, Ukraine, the Middle East, Senegal, Vietnam and business, each with a simple geometric icon and a short, readable label. `main.py` copies the prebuilt PNG into the required output directory.

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Why this image sums up the day

The date is spelled out in the header, and every panel reports a story reported on 24 November 2026: US plans for tariffs on 16 trading partners, the Russian strike on Zaporizhzhia that killed 2 and wounded 40, the Israeli strike that killed Hamas internal security chief Naim Abu Nahal, about 175 migrants unaccounted for after a boat left Dakar, the Hanoi explosion that killed 6 and injured 10, and Sanofi's $41 billion takeover of Insmed.

Sources: Reuters, AP, Politico, Sanofi press release, Times of Israel. The image is generated offline by `make_image.py`, and the entry program only copies a fixed byte-for-byte PNG.
