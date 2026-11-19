# Native theme-aware motion

The same `scripts/render_cards.py` renders both light and dark variants into `cards/light` and `cards/dark`.

Animations are defined in `svg()` and per-project animations in `project_motion(i)`. The generator removes the solid canvas and solid illustration backplates so the SVGs float directly over GitHub's background.

The portrait remains embedded and the 3D-style wireframe cubes remain animated. Use `STATIC=1 python scripts/render_cards.py` to inspect stills, then run normally to restore animated SVGs.
