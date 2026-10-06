# Strand background pack — v34

Artwork for 324 Strand folders, with focus-driven and full-screen versions.
Browse the gallery at https://wepiii2.github.io/strand-backgrounds/.

Existing public `strand-art.otterschickens.com` image and download links redirect
to GitHub, so previously imported shelves keep working. Use the GitHub Pages
address for new setups; public artwork requests no longer use the old art server.

This public repository contains only artwork, its source catalog, and helper scripts.
It contains no personal Strand export, addon URLs, or credentials.

Download `Strand-Backgrounds-Self-Host-v7.zip` from the site, unzip it, then run:

```sh
python3 download_images.py --variant focus
# or: python3 download_images.py --variant full
```

The downloader saves art under `images/focus/` or `images/full/` and verifies
each file against the catalog. To use these images with your own Strand setup,
export your current setup and keep that export as a backup, then run:

```sh
python3 apply_to_strand.py "My Setup.strand" "My Setup Updated.strand" --base-url https://wepiii2.github.io/strand-backgrounds --variant focus
```

Use `--variant full` for a full-screen hero layout. Import the new `.strand`
file into Strand. On Apple TV, enable the shelf row's “Use Image as Background”
option. The helper changes only matching folders' background URLs. It matches folder IDs first, then normalized shelf/title pairs or a unique title, so renamed shelves and previously renamed collection titles work. Other settings and icons are preserved.

The underlying art and logos belong to their respective owners. Sources are
listed in `catalog.json`. This is an unofficial community pack, unaffiliated
with Strand, Trellis, or the brands shown.

The Film Collections shelf adds 11 genre-based poster collages, each available
as a 2400×720 focused hero or a 1920×1080 full-screen hero.

Version 34 uses consistent solid center title bands in both sizes, rebuilds focused collages as continuous panels, repairs Sci-Fi, and fills out Family and Fantasy. Original shelf icons are preserved.

## Helper compatibility fix - October 6, 2026

Re-download and extract the complete self-hosting pack before running the helper. The corrected apply_to_strand.py supports UTF-8 exports with or without a Windows byte-order mark, nested folder groups, and renamed shelves. It reports missing files and invalid exports without a traceback and includes image cache keys in the updated URLs.

Run the command from a terminal, rather than double-clicking the script. On Windows, use `py -3` in place of `python3` if needed. Quote filenames containing spaces. Pick a new output filename on every run; the helper deliberately refuses to overwrite your input or an existing output. Keep catalog.json beside the script, or pass `--catalog PATH`. For your own hosting, --base-url must point to the directory containing focus/ and full/ (for example https://art.example.com/images when hosting the downloader's images directory).
