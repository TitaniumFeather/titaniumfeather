# Titanium OS — Editorial Layout V3

Four featured projects now use alternating image/text placement and distinct accent treatments. Each project SVG is 1200 × 535 with 64px of transparent top breathing room and extra bottom spacing; this ensures separation on GitHub even if Markdown image margins collapse.

To change spacing, edit `project()` in `scripts/render_cards.py`. Change `w,h=1200,535` for overall spacing, `translate(0 64)` for top inset, and the `tx`/`left_art` values for column alignment. Run `python scripts/render_cards.py` and commit the regenerated assets.
