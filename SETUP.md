# Titanium OS — setup

1. Create a **public** GitHub repository named `titaniumfeather` under the GitHub account `titaniumfeather` (the profile README only works when account and repository names match).
2. Upload **all files**, including the hidden `.github/workflows/update-readme.yml` directory, to the repository root.
3. In GitHub repository **Settings → Actions → General**, enable workflows and set **Workflow permissions → Read and write permissions** if your organization/account allows it. The workflow uses `GITHUB_TOKEN`, which is provided automatically by GitHub Actions.
4. Go to **Actions → Update Titanium OS profile → Run workflow**. The workflow fetches real contribution data and commits regenerated SVG cards.
5. Edit `config.json` to change your name, headline, skills, theme, projects, and project URLs. Edit `README.md` anchor `href` attributes to match your real project URLs. The config's `projects[].url` values are intentionally blank because your repository links have not been verified.
6. For local rendering, run `python scripts/render_cards.py`. To fetch contributions locally, set `GH_TOKEN` to a GitHub token with access to your own public contribution data, then run `python scripts/fetch_github_data.py` followed by `python scripts/render_cards.py`.
7. For a static preview, run `STATIC=1 python scripts/render_cards.py`. Run again without `STATIC=1` before committing to restore animations.

## Notes

- All generated SVGs are standalone, require no external fonts, and use CSS animations. `prefers-reduced-motion` disables animations. Some GitHub clients may display a static frame.
- Contribution data is never fabricated. Before the first successful API refresh, analytics show a helpful unavailable state.
- `data/contributions.json` is refreshed daily by GitHub Actions. The GitHub GraphQL contribution calendar is based on GitHub's contribution counting rules, not raw commit totals.
- The ASCII art is an abstract feather, not a personal likeness. To replace it, edit `FEATHER` in `scripts/render_cards.py` or provide a photo for a custom portrait conversion.
- SVG text is rendered using system fonts for portability. For a bespoke embedded font, use a properly licensed WOFF subset encoded as a data URI; this implementation deliberately has no font redistribution requirement.
- If GitHub Actions reports a 403 on `git push`, verify workflow write permissions and repository branch protection settings.
- GitHub's scheduled workflows can be delayed, especially during high-load periods.
