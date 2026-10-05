# Strand background pack — v29

Artwork for 312 Strand folders, with focus-driven and full-screen versions.
Browse the gallery at https://wepiii2.github.io/strand-backgrounds/.

This public repository contains only artwork, its source catalog, and helper scripts.
It contains no personal Strand export, addon URLs, or credentials.

Download `Strand-Backgrounds-Self-Host-v4.zip` from the site, unzip it, then run:

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
option. The helper changes only matching folders' background URLs.

The underlying art and logos belong to their respective owners. Sources are
listed in `catalog.json`. This is an unofficial community pack, unaffiliated
with Strand, Trellis, or the brands shown.
