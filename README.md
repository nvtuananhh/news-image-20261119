# THE WORLD IN ONE PAGE — 19 November 2026

A newspaper front page summing up Thursday 19 November 2026 in one
image, built for the [make.fun](https://make.fun/bounty/news-image-20261119)
`news-image-20261119` competition.

## What the poster shows

- **Lead story — first-ever Trump–Xi–Putin summit, Shenzhen:** the
  presidents of the US, China and Russia meet today on the sidelines of
  the APEC summit, the first time all three have ever met together.
  Agenda: nuclear arms control (after New START expired in February),
  Ukraine, Iran, trade and AI. Xi hosts; Trump and Putin attend.
- **GTA VI is here:** global rollout begins today after a 13-year wait
  since GTA V — back to Vice City, Leonida, on PS5 and Xbox Series X|S.
  $1.65bn in pre-orders; 99 on Metacritic.
- **Jeffries makes history:** House Democrats nominated Hakeem Jeffries
  for Speaker, 251 votes to 11. If confirmed by the full House in
  January, he becomes the first Black Speaker in US history.
- **Cyclone Akvan bears down:** a very severe cyclone heads for the
  Andhra Pradesh and Odisha coasts; landfall expected about 20 Nov,
  winds about 145 km/h.
- **Voyager 1, one light-day away:** crossed one light-day from Earth
  on 18 Nov — 25.9 billion km, 173 times the Earth–Sun distance. A radio
  signal now takes a full 24 hours to reach it.
- **In brief:** EU proposes a €45bn loan to Ukraine (repaid after Russia
  pays reparations); Ebola in DR Congo — 11,000+ cases, 5,400 deaths
  (UN); US–Iran strikes continue (Qeshm Island, Bahrain, Kuwait);
  Gaza rain — 46,000+ households displaced.
- **Markets:** S&P 500 –1.03%; gold ~$3,767, a 14-month low. NVIDIA:
  earlier pay raises and more stock grants promised; H-series shipments
  to China stopped. Fed minutes: most officials expect further rate
  hikes if inflation stays hot.

Every number and fact on the poster matches the competition brief's
verified news list for 19 November 2026; nothing was invented.

## Files

- `gen_poster.py` — deterministic generator of `poster.png`
  (Python 3, Pillow; draws at 2048×2048 and downsamples to 1024×1024)
- `poster.png` — the poster, 1024×1024, under 1 MiB
- `main.py` — stdlib-only entry point: copies `poster.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`)

## How to run

```sh
python3 gen_poster.py        # regenerate poster.png (byte-identical)
MAKEFUN_OUTPUT_DIR=/output python3 main.py   # writes /output/entry.png
```

The generator uses no network, no timestamps and no randomness, so
two runs produce byte-identical output.

## License

MIT — see `LICENSE`.
