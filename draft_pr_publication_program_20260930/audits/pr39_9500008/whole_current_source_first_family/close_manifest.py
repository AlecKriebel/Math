"""Close this family's evidence by exact relative path, excluding only itself."""
from pathlib import Path
import hashlib
import json

FOREIGN = {
    "open_mathjax.html": "independently acquired author HTML",
    "forward_1302.6958v4.pdf": "independently acquired primary PDF",
    "forward_1302.6958v4.txt": "Poppler text extraction of primary PDF",
    "forward_page20.png": "Poppler primary PDF page20 rendering",
    "forward_page21.png": "Poppler primary PDF page21 rendering",
    "pitman_tang_Slepian.pdf": "independently acquired contextual PDF",
    "morters_peres_bmbook.pdf": "independently acquired standard Brownian primary text",
    "morters_peres_bmbook.txt": "Poppler extraction of standard Brownian primary text",
}


def inventory(root, foreign, manifest_relative="MANIFEST.json"):
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError("symlink forbidden: " + relative)
        if not path.is_file() or relative == manifest_relative:
            continue
        blob = path.read_bytes()
        rows.append({
            "path": relative,
            "kind": "foreign_cache" if relative in foreign else "first_party",
            "description": foreign.get(relative, "reviewer-authored retained evidence"),
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
        })
    missing = set(foreign).difference(row["path"] for row in rows)
    if missing:
        raise ValueError("missing separately bound foreign caches: " + repr(sorted(missing)))
    return rows


def verify_inventory(root, retained_rows, foreign):
    actual = inventory(root, foreign)
    assert actual == retained_rows, "exact path/size/hash/kind closure mismatch"
    return True


if __name__ == "__main__":
    root = Path(__file__).parent
    foreign_rows = [r for r in inventory(root, FOREIGN) if r["kind"] == "foreign_cache"]
    foreign_packet = {"schema": "separately-bound-foreign-cache-v1", "files": foreign_rows,
                      "symlinks_allowed": False, "exact_paths_only": True}
    (root / "FOREIGN_CACHE_MANIFEST.json").write_text(json.dumps(foreign_packet, indent=2)+"\n")
    rows = inventory(root, FOREIGN)
    out = {
        "schema": "independent-family-exact-path-closure-v1",
        "self_exclusion": "MANIFEST.json",
        "symlinks_allowed": False,
        "basename_exclusions": False,
        "first_party_only": True,
        "first_party": [r for r in rows if r["kind"] == "first_party"],
        "foreign_cache_manifest": "FOREIGN_CACHE_MANIFEST.json",
        "foreign_material_exact_paths": sorted(FOREIGN),
    }
    (root / "MANIFEST.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"first_party_count": len(out["first_party"]),
                      "foreign_cache_count": len(foreign_rows)}))
