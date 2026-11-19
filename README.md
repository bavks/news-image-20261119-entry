[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/bavks/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/bavks/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# news-image-20261119 — the world on Thursday, in one image

Entry for the make.fun bounty **"Sum up 19 November's world news in one
image"** (news-image-20261119).

## What it does

`main.py` copies the committed `entry.png` to the output directory
(`/output` by default, or `$MAKEFUN_OUTPUT_DIR` when set). It uses only
the Python standard library, needs no network, and writes byte-identical
output on every run.

## The image

A newspaper front page in colour for **Thursday, 19 November 2026**,
typeset as "The Daily Meridian": a deep-red masthead and dateline over
one lead story (the first-ever Xi–Trump–Putin trilateral summit in
Shenzhen) and five more stories in ruled columns, each with a short
headline and one factual sub-line. The illustrations are drawn in code
in flat newsprint colours, and all lettering was typeset
programmatically (no generative text), so nothing is garbled and the
page stays legible shrunk to 300 px across. `render_image.py` is the
renderer that produces `entry.png`.

## The six stories, as reported on the day

1. **Xi, Trump and Putin meet in Shenzhen** — The leaders of China,
   Russia and the United States held their first-ever three-way
   meeting on Thursday in Shenzhen, on the sidelines of the APEC
   summit; Xi called the encounter of groundbreaking significance and
   Trump called it already a win, with nuclear arms, Iran and Ukraine
   on the table and no agreement expected.
   *Sources: Reuters, 18–19 Nov 2026; HK Businesswire, 19 Nov 2026;
   Particle News, 19 Nov 2026.*
2. **Ukraine hits Crimean Bridge again** — Ukraine struck the bridge
   linking Russia and Crimea for the third time in a week, forcing a
   suspension of train services, Russian authorities said, hours
   before President Putin was due to meet the leaders of China and
   the US.
   *Source: Reuters, 19 Nov 2026.*
3. **Houthi missile menaces Riyadh** — A Saudi-led coalition said on
   Thursday it had dealt with a missile threat launched by Yemen's
   Houthis towards Riyadh, after a loud boom was heard in the Saudi
   capital; debris fell and material damage was reported.
   *Source: Reuters, 19 Nov 2026.*
4. **Anthropic debuts at $1.5 trillion** — Anthropic priced its IPO at
   $83 a share, raising a record $81.3 billion, and its shares began
   trading on the Nasdaq on Thursday under the ticker ANT, at a fully
   diluted valuation of roughly $1.5 trillion.
   *Sources: Bloomberg via Moneyweb, 19 Nov 2026; PYMNTS, 19 Nov
   2026; FinanceFeeds, 19 Nov 2026.*
5. **UNHCR halts Malaysia registration** — The UN refugee agency said
   its Malaysian office has stopped its registration and documentation
   activities following a decision by the government to build its own
   system for managing asylum seekers.
   *Source: Reuters, 19 Nov 2026.*
6. **GTA VI arrives after 13 years** — Grand Theft Auto VI was
   released at midnight around the world on Thursday, ending the
   13-year wait for a new instalment of the game.
   *Source: BBC, 19 Nov 2026.*

Stories considered and dropped after date-checking: the International
Court of Justice's judgment in The Gambia v. Myanmar (Rohingya
genocide case) was being read at the Peace Palace as this entry was
built, with no verdict published yet, so no outcome could be stated
truthfully; Denmark's parliamentary vote on the Greenland security
deal was scheduled for Thursday morning with the result likewise
unpublished at build time; and a global Microsoft 365 outage
circulating in 19 November roundups actually began on Thursday
12 November, so it was excluded as recycled.
