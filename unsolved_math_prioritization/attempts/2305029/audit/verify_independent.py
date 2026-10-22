#!/usr/bin/env python3
"""Independently pinned byte/inventory check for the reviewed seven-file packet.

This is not an analytic proof checker. Obtain this checker from a trusted audit
publication; replacing its code replaces its trust anchor. Use stable inputs.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import re
import sys

ORIGINAL_MANIFEST_SHA256 = "cf5f178a46b580701522ce59ff4707c4179963ec5d2f8848a759261b1d974206"
EXPECTED_FILES = {'ACCEPTANCE_REPORT.md': (6530, 'ddca6860d6b51a422d90e282eacf93021c8c62df7331e1136cede15296ccd1a5'), 'MANIFEST.json': (961, 'cf5f178a46b580701522ce59ff4707c4179963ec5d2f8848a759261b1d974206'), 'REPRODUCIBILITY.md': (2453, '4d64f4b98761519b366b20f4e9f45ff9ceaad23b5b2e915e1e788a4d4d880e82'), 'RESULT.json': (1084, 'e4c95918e40475ccd21b86cd6b09346c50514e8649452df08ba902df4504666b'), 'SOURCES.json': (3061, '1925dd3c63bd56fff5a77d271bc639ba3135a2ab783b268e857cee31b309b69f'), 'VALIDATION.json': (772, '8fbc46e3f24c142fab1930d1b6959a3738e938c3febf40664c90b57e8340ec92'), 'verify_packet.py': (2848, 'd6e4afbaf3a7ff9766124220e5ebc9c258b150b6336ea61d4485816dab2a229e')}
EXPECTED_SOURCES = {'danielyan2016_published.pdf': (105706, 'c8af7e41c2c56dd7b8a5d71d8d5181da6fb32dafce8dc2a3fad35a4dc2f2cea5'), 'danielyan2016_v1.pdf': (89195, '24f0b7979e1a52cd43aa297b80eb78738d0ee76e28028c40219ffcca93bf09c9'), 'hayman2018_v2.pdf': (1706228, '8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0')}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_pinned_file(path, expected):
    size, digest = expected
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "Nonregular member: " + path.name)
    require(before.st_size == size, "Byte count mismatch: " + path.name)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as stream:
        opened = os.fstat(stream.fileno())
        require(stat.S_ISREG(opened.st_mode), "Nonregular open file: " + path.name)
        require((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
                "File changed while opening: " + path.name)
        data = stream.read(size + 1)
    require(len(data) == size, "Byte count mismatch: " + path.name)
    require(hashlib.sha256(data).hexdigest() == digest, "SHA-256 mismatch: " + path.name)
    return data


def strict_json(raw):
    def reject_constant(value):
        raise ValueError("Nonfinite JSON number")

    def finite_float(value):
        parsed = float(value)
        require(math.isfinite(parsed), "Nonfinite JSON number")
        return parsed

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=reject_constant, parse_float=finite_float)


def validate_manifest(manifest):
    require(type(manifest) is dict and set(manifest) == {"schema", "problem_id", "files"},
            "Unexpected manifest schema fields")
    require(type(manifest["schema"]) is int and manifest["schema"] == 1,
            "Invalid manifest schema version")
    require(type(manifest["problem_id"]) is int and manifest["problem_id"] == 2305029,
            "Invalid manifest problem ID")
    rows = manifest["files"]
    require(type(rows) is list, "Manifest files must be a list")
    seen = set()
    for row in rows:
        require(type(row) is dict and set(row) == {"name", "bytes", "sha256"},
                "Unexpected manifest row fields")
        name = row["name"]
        require(type(name) is str and name in EXPECTED_FILES and name != "MANIFEST.json",
                "Invalid manifest member name")
        require(name not in seen, "Duplicate manifest member")
        seen.add(name)
        require(type(row["bytes"]) is int and row["bytes"] >= 0,
                "Invalid manifest byte count")
        require(type(row["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]),
                "Invalid manifest digest")
        require((row["bytes"], row["sha256"]) == EXPECTED_FILES[name],
                "Manifest row differs from reviewed identity")
    require(seen == set(EXPECTED_FILES) - {"MANIFEST.json"}, "Incomplete reviewed manifest inventory")


def validate_sources(sources):
    require(type(sources) is dict and set(sources) == {"schema", "retrieved_date_utc", "pdfs", "inspection", "status", "search_scope"},
            "Unexpected source schema fields")
    require(type(sources["schema"]) is int and sources["schema"] == 1, "Invalid source schema version")
    require(type(sources["retrieved_date_utc"]) is str, "Invalid retrieval date")
    require(type(sources["inspection"]) is list and type(sources["status"]) is dict
            and type(sources["search_scope"]) is dict, "Invalid source metadata container types")
    require(type(sources["pdfs"]) is list, "Source PDFs must be a list")
    seen = set()
    for row in sources["pdfs"]:
        require(type(row) is dict and set(row) == {"url", "final_url", "bytes", "sha256", "retrieved_utc", "filename"},
                "Unexpected source row fields")
        name = row["filename"]
        require(type(name) is str and name in EXPECTED_SOURCES and name not in seen,
                "Invalid or duplicate source name")
        seen.add(name)
        require(type(row["bytes"]) is int and row["bytes"] >= 0, "Invalid source byte count")
        require(all(type(row[key]) is str for key in ("url", "final_url", "sha256", "retrieved_utc")),
                "Invalid source string field")
        require((row["bytes"], row["sha256"]) == EXPECTED_SOURCES[name], "Source row differs from reviewed identity")
    require(seen == set(EXPECTED_SOURCES), "Incomplete reviewed source inventory")


def verify(packet, pin, sources=None):
    require(pin == ORIGINAL_MANIFEST_SHA256, "Pin differs from independently reviewed original")
    require(stat.S_ISDIR(packet.lstat().st_mode), "Packet root must be a nonsymlink directory")
    packet = packet.resolve(strict=True)
    wanted = set(EXPECTED_FILES)
    require({p.name for p in packet.iterdir()} == wanted, "Unexpected or missing packet member")
    parsed = {}
    for name, expected in EXPECTED_FILES.items():
        data = read_pinned_file(packet / name, expected)
        if name.endswith(".json"):
            parsed[name] = strict_json(data)
    validate_manifest(parsed["MANIFEST.json"])
    validate_sources(parsed["SOURCES.json"])
    require({p.name for p in packet.iterdir()} == wanted, "Packet inventory changed during read")
    result = {"packet_integrity": "PASS", "packet_files": len(EXPECTED_FILES),
              "manifest_sha256": ORIGINAL_MANIFEST_SHA256,
              "source_identity": "not_requested", "mathematical_proof_check": "not_performed"}
    if sources is not None:
        require(stat.S_ISDIR(sources.lstat().st_mode), "Source root must be a nonsymlink directory")
        for name, expected in EXPECTED_SOURCES.items():
            read_pinned_file(sources / name, expected)
        result.update(source_identity="PASS", source_files=len(EXPECTED_SOURCES))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-dir", type=Path, required=True)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.packet_dir, args.expected_manifest_sha256, args.source_dir), sort_keys=True))
    except (ValueError, OSError, TypeError) as error:
        # Avoid emitting caller-specific filesystem locations in reusable receipts.
        message = str(error) if isinstance(error, ValueError) else type(error).__name__
        print("FAIL: " + message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
