#!/usr/bin/env python3
"""Apply matching hero backgrounds to a Strand export without changing its other settings."""

import argparse
import json
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


def normalized(value):
    """Treat capitalization, spacing, and typographic apostrophes consistently."""
    if not isinstance(value, str):
        return ""
    text = unicodedata.normalize("NFKC", value).casefold()
    for mark in ("\u2018", "\u2019", "\u02bc"):
        text = text.replace(mark, "'")
    return " ".join(text.split())


def read_json(path):
    # utf-8-sig also accepts files saved with a Windows UTF-8 byte-order mark.
    with path.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def unique(rows):
    return rows[0] if len(rows) == 1 else None


def apply_backgrounds(setup, catalog, origin, variant):
    by_id = defaultdict(list)
    by_group_title = defaultdict(list)
    by_title = defaultdict(list)
    field = variant + "File"
    for row in catalog:
        if not isinstance(row, dict) or not isinstance(row.get(field), str):
            raise ValueError("The catalog has an invalid image entry. Re-download the complete pack.")
        if row.get("id"):
            by_id[normalized(row["id"])].append(row)
        key = (normalized(row.get("group")), normalized(row.get("title")))
        by_group_title[key].append(row)
        by_title[key[1]].append(row)

    matched = 0
    unmatched = []

    def visit(value, group_name=""):
        nonlocal matched
        if isinstance(value, list):
            for child in value:
                visit(child, group_name)
        elif isinstance(value, dict):
            sources = value.get("contentSources")
            if isinstance(sources, list):
                group_name = value.get("title") or group_name
                for folder in sources:
                    if not isinstance(folder, dict):
                        continue
                    title = normalized(folder.get("title"))
                    row = unique(by_id.get(normalized(folder.get("id")), []))
                    if row is None:
                        row = unique(by_group_title.get((normalized(group_name), title), []))
                    if row is None and title:
                        # Imported/re-created shelves may have new IDs or custom shelf names.
                        # Only use a global title when it identifies one catalog entry.
                        row = unique(by_title.get(title, []))
                    if row is not None:
                        url = origin + "/" + row[field].lstrip("/")
                        checksum = row.get(variant + "SHA256")
                        if checksum:
                            url += "?v=" + checksum[:16]
                        folder["backgroundImageURL"] = url
                        matched += 1
                    elif folder.get("title"):
                        unmatched.append(folder["title"])
                    visit(folder, group_name)
                for key, child in value.items():
                    if key != "contentSources":
                        visit(child, group_name)
            else:
                # A renamed shelf provides context for nested group sources without
                # assuming that every shelf uses the same Swift enum wrapper.
                context = value.get("title") or group_name
                for child in value.values():
                    visit(child, context)

    visit(setup)
    return matched, unmatched


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Your current .strand export")
    parser.add_argument("output", type=Path, help="New .strand file to create")
    parser.add_argument("--base-url", required=True,
                        help="HTTPS folder containing focus/ and full/, e.g. https://art.example.com/images")
    parser.add_argument("--variant", choices=("focus", "full"), required=True,
                        help="Match your Strand hero layout")
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog.json",
                        help="Catalog file (default: catalog.json beside this script)")
    args = parser.parse_args()
    origin = args.base_url.rstrip("/")
    parsed = urlsplit(origin)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.query or parsed.fragment
            or parsed.username or parsed.password):
        parser.error("--base-url must be an HTTPS folder URL without credentials, a query, or a fragment")
    if args.input.resolve() == args.output.resolve() or args.output.exists():
        parser.error("output must be a new file separate from input; choose a different output filename")
    if not args.input.is_file():
        parser.error("input export was not found; check the path and quote filenames containing spaces")
    if not args.catalog.is_file():
        parser.error("catalog.json was not found; extract the whole ZIP before running this script, or use --catalog PATH")
    if not args.output.parent.is_dir():
        parser.error("the output directory does not exist; choose an existing folder")
    try:
        catalog = read_json(args.catalog)
        if not isinstance(catalog, list):
            raise ValueError("The catalog must contain an artwork list.")
        setup = read_json(args.input)
        if not isinstance(setup, (dict, list)):
            raise ValueError("The input does not contain a Strand setup or shelf export.")
        matched, unmatched = apply_backgrounds(setup, catalog, origin, args.variant)
        if not matched:
            parser.error("no matching folders found; use a shelf export with folders listed in this pack's gallery")
        text = json.dumps(setup, indent=2, ensure_ascii=False) + "\n"
        # Exclusive creation keeps an existing output file safe, even if it appeared
        # between the initial check and this write.
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(text)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print("Added {} background URLs. Original export was not changed.".format(matched))
    if unmatched:
        print("Skipped {} unmatched folders; their existing settings were preserved.".format(len(unmatched)))


if __name__ == "__main__":
    main()
