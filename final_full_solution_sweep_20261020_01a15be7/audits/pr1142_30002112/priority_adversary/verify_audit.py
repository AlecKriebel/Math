#!/usr/bin/env python3
"""Read-only offline custody and finite bridge diagnostics; not a theorem prover."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    count = 0
    for item in manifest["authored_files"]:
        relative = Path(item["path"])
        require(not relative.is_absolute() and ".." not in relative.parts, "unsafe authored path")
        file = root / relative
        require(file.is_file() and not file.is_symlink(), "missing or symlink authored file")
        require(file.stat().st_size == item["bytes"], "authored byte count mismatch")
        require(digest(file) == item["sha256"], "authored hash mismatch")
        count += 1

    known = {
        "petiard2017": "eb73f36a4f035c48eb0b47916cd52b5b604a69ae8ec405306911f9e83e029eba",
        "petiard2019thesis": "081c31a93198b740e641c213c38197e6c24da900703f2cc069b76fc7db0c2ad0",
        "petiard2019metadata": "e9a25391137049b6962ef03219482fdc0e6be11006cfe0dc1b280a189148437d",
        "colbois2017survey": "0e55a2ab4dbb07f0b2fed518badef8d5eb3012cb3fb1fc910d0ea31529183154",
        "cde2009": "a2bc60b7f1b00009ef39ac1260ee6b9cb4a3464d3617f0f3944a9aee5fa6bb35",
        "ceg2011": "68238e41cde092efed54e5743e4af35fd512e7913c6d557ec7809a1a43d74888",
        "cp2021": "eafb2777bec224cb07b7465e81870ee5414bc7f1e86596f56a26126e9212ac9a",
        "owr2012": "20d5708e6ab0ccee4e8944d8e11c514221c2642a4e15c878067eed34405bc8e9",
        "nashprecise": "22ca78b5750848189dee869f3fc8895c0b935c4af5316450132164aba87e0ddc",
    }
    retrieval = json.loads((root / "SOURCE_RETRIEVAL.json").read_text())
    seen = set()
    captures = 0
    for item in retrieval:
        path = Path(item["path"])
        require(not path.is_absolute() and ".." not in path.parts and path.parts[0] == "private", "source escaped private storage")
        file = root / path
        require(file.is_file() and not file.is_symlink(), "source file missing or symlink")
        require(file.stat().st_size == item["bytes"] and digest(file) == item["sha256"], "source capture changed")
        captures += 1
        if item["name"] in known:
            require(item["status"] == 200 and item["sha256"] == known[item["name"]], "primary source pin failed")
            seen.add(item["name"])
    require(seen == set(known), "missing primary source pin")
    proof = root / "private/CANDIDATE_PROOF.md"
    require(proof.stat().st_size == 10412, "wrong candidate proof size")
    require(digest(proof) == "c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658", "wrong candidate blob")
    private_manifest = json.loads((root / "CAPTURE_MANIFEST.json").read_text())
    for item in private_manifest["files"]:
        relative = Path(item["path"])
        require(not relative.is_absolute() and ".." not in relative.parts and relative.parts[0] == "private", "unsafe capture manifest path")
        file = root / relative
        require(file.is_file() and not file.is_symlink(), "missing private capture")
        require(file.stat().st_size == item["bytes"] and digest(file) == item["sha256"], "private capture hash mismatch")
    metadata = json.loads((root / "private/petiard2019metadata.json").read_text())["metadata"]
    require(metadata["dc.date.issued"][0]["value"] == "2019", "wrong issue date")
    require(metadata["dc.date.accessioned"][0]["value"].startswith("2025-09-12"), "wrong accession date")
    require(metadata["dc.identifier.doi"][0]["value"] == "10.35662/unine-thesis-2749", "wrong thesis DOI")

    # These integer checks are equivalent to the index inequalities after raising
    # both nonnegative sides to m; no floating point powers are used.
    inequalities = 0
    for m in range(2, 81):
        p = Fraction(2, m)
        require(0 < p <= 1, "dimension exponent failed")
        for j in range(1, 201):
            require((j + 1) ** 2 <= 2 ** m * j ** 2, "one-based source shift failed")
            require((j + 2) ** 2 <= 3 ** m * j ** 2, "punctured shift bound failed")
            inequalities += 2

    # Exact multiset accounting in a representative finite window, with a tie.
    source = [0, 5, 7, 7, 20]
    union = sorted(source + [0, 100, 100, 100])
    for j in range(1, len(source)):
        require(union[j + 1] == source[j], "one extra zero shift failed")
    require(union[1] != source[1], "negative-control wrong shift was not detected")
    # A large first sphere eigenvalue is essential; this deliberate low mode
    # must destroy the asserted identity at some index.
    bad_union = sorted(source + [0, 1, 1, 1])
    require(any(bad_union[j + 1] != source[j] for j in range(1, len(source))), "negative-control low sphere modes not detected")
    # Harmless thesis equality slip: equality is false, correct bound survives.
    require(1 ** 2 + 1 != (1 + 1) ** 2, "equality-slip negative control failed")
    for n in range(1, 20):
        for x in range(0, 20):
            require(x ** n + 1 <= (x + 1) ** n, "finite ceiling direction failed")

    external = json.loads((root / "EXTERNAL_RECORD_CHECK.json").read_text())
    require(external["eulersolve_alias_status"] == 404 and external["eulersolve_index_status"] == 200, "provider status mismatch")
    require(external["eulersolve_index_heading_count"] == 374, "index size changed")
    require(all(q["status"] == 200 for q in external["zenodo_queries"]), "uncorrected public query failure")
    require(not external["new_record_created"], "new record not permitted by this audit")
    recovery = json.loads((root / "PREPARATION_RECOVERY.json").read_text())
    require(not recovery["original_scripts_executed"], "captured script execution alleged")
    require(recovery["earlier_skip_disposition"] == "earlier_full_target_resolution", "wrong recovery decision")
    require((root / ".gitignore").read_text().splitlines()[0] == "private/", "private exclusion missing")
    print(json.dumps({
        "ok": True,
        "python_optimized": bool(sys.flags.optimize),
        "python_isolated": bool(sys.flags.isolated),
        "authored_files": count,
        "primary_pins": len(seen),
        "captures_checked": captures,
        "all_private_pins": len(private_manifest["files"]),
        "exact_index_inequalities": inequalities,
        "spectral_multiset_and_negative_controls": "pass",
        "manifest_sha256": digest(root / "MANIFEST.json"),
        "scope": "offline read-only custody and finite diagnostics only; external theorem truth is supported by the authored primary-source review"
    }, sort_keys=True))


if __name__ == "__main__":
    main()
