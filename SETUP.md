# Titanium OS — Native Edition

Transparent SVGs blend with GitHub's actual canvas. Separate `cards/light` and `cards/dark` variants are selected by the README's `<picture>` elements, based on the viewer's preferred color scheme.

## Edit and regenerate

1. Edit `config.json` for project descriptions. Edit the root `README.md` to change the clickable project links.
2. Run `python -m pip install Pillow` once.
3. Run `python scripts/render_cards.py` to regenerate all 16 SVGs.
4. Commit and push the changes. The GitHub Action also regenerates cards when source files change.

## Windows PowerShell update from ZIP

Save `titanium-os-native.zip` in Downloads. These commands update an existing local clone at `Desktop\titaniumfeather`:

```powershell
$zip = "$HOME\Downloads\titanium-os-native.zip"
$repo = "$HOME\Desktop\titaniumfeather"
$temp = Join-Path $env:TEMP "titanium-native-update"
Expand-Archive -Path $zip -DestinationPath $temp -Force
Copy-Item "$temp\*" -Destination $repo -Recurse -Force
Copy-Item "$temp\.github" -Destination $repo -Recurse -Force
Set-Location $repo
git add -A
git commit -m "Add transparent theme-adaptive Titanium OS cards"
git push origin main
```

If Git says `nothing to commit`, confirm the ZIP was extracted to the correct path and that you copied the contents rather than an extra wrapper folder.

## Notes

- SVG backgrounds are transparent. The browser renders GitHub's actual page background beneath them.
- Light/dark switching uses GitHub's documented README `<picture>` technique. It does not detect arbitrary custom color palettes.
- The portrait PNG is embedded in the SVG, while the typography and vector artwork switch colors.
- `STATIC=1` disables animations for snapshots; regenerate normally before committing.
- SVG animation support varies between clients and reduced-motion settings.
