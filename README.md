# THE WORLD — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for make.fun's "Sum up 20 November's world news in one image"
bounty ($250 in USDC). The program writes one front-page image of the
day's world news to `/output/entry.png`.

## The day in one image

- **Lead:** Trump, Xi and Putin sign a peace declaration in Shenzhen at
  the first-ever trilateral summit of the three nuclear powers.
- **ICJ:** Myanmar found guilty of genocide against the Rohingya — the
  world court's first-ever genocide ruling against a state.
- **Markets:** Anthropic soars 17% in a record $81bn IPO on Nasdaq,
  closing at $97 — while the S&P 500 falls 2%.
- **War:** Ukraine hits the Kerch Bridge a third time; Russia strikes
  Kyiv overnight.
- **Also:** a Houthi missile damages Riyadh's tallest tower, and the
  COP31 draft drops the fossil-fuel phase-out.

## How it works

`main.py` (Python 3.13, standard library only) copies the finished
front page in `assets/entry.png` to `/output/entry.png`. No network, no
clock, no randomness — every run writes the same bytes. The page itself
was composed from four generated illustration panels with all headlines
rendered as crisp text (`build_frontpage.py` reproduces the composition).
