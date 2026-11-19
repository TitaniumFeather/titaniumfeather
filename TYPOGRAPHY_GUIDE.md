# Typography and spacing — V2

This edition increases heading sizes, body readability and vertical breathing room while preserving transparent GitHub theme-aware SVGs and existing animations.

Edit `scripts/render_cards.py` to tune sizes. `hero()` controls the main heading; `statement()` controls About; `section()` controls the project heading; `project()` controls card text; `footer()` controls the closing statement.

Run `python -m pip install Pillow` and `python scripts/render_cards.py` to regenerate all light/dark SVGs.

GitHub caches images, so a hard refresh or waiting briefly may be needed after pushing.
