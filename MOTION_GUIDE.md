# Titanium OS — Cinematic Motion Edition

Run `python -m pip install Pillow` then `python scripts/render_cards.py`.

The generator is `scripts/render_cards.py`. Project-specific animations are in `project_motion(i)`; global animation timing and easing are in the `<style>` assembled by `svg()`. Font assets in `fonts/` are embedded directly into each SVG, so GitHub does not need to fetch external fonts.

Animations: hero name reveal and gold gradient sweep; floating wireframe cubes; portrait ASCII texture; LunaraOS staged window boot; MedScope rotating scan reticles and scan beam; BeneficentTrade moving crosshair and drawn price lines; PixelPerfect staged UI build and shine. Motion is CSS and SVG-based and does not need JavaScript. GitHub may render motion differently depending on client/browser and accessibility settings.

`STATIC=1 python scripts/render_cards.py` produces non-animated cards for screenshots. Re-run normally before committing animated assets. The SVGs have reduced-motion fallbacks.

To update your already-cloned repository on Windows, extract the ZIP and copy the **contents** of the ZIP's top level into your clone (not a parent directory). Then `git add -A`, `git commit -m "Upgrade cinematic animations"`, `git push origin main`.
