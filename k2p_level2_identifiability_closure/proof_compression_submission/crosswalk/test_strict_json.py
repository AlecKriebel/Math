#!/usr/bin/env python3
"""Focused syntax/canonicality mutations for the shared release JSON reader."""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path
from typing import Callable

STRICT_JSON_DIR = (
    Path(__file__).resolve().parents[2] / "work" / "final_theorem_release"
)
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (
    StrictJSONError,
    canonical_json_bytes,
    decode_json_document,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
    validate_release_json_member,
)


def compressed(data: bytes) -> bytes:
    return gzip.compress(data, compresslevel=6, mtime=0)


def require_rejection(
    case: str, expected: str, operation: Callable[[], object]
) -> str:
    try:
        operation()
    except StrictJSONError as error:
        if expected not in str(error):
            raise SystemExit(f"{case}:wrong diagnostic:{error}") from error
        return str(error)
    raise SystemExit(f"{case}:mutation survived")


def main() -> None:
    clean = {"nested": {"a": 1}, "status": "PASS"}
    clean_line = canonical_json_bytes(clean) + b"\n"
    clean_gzip = compressed(clean_line)
    if list(iter_canonical_gzip_jsonl(clean_gzip, label="clean.jsonl.gz")) != [clean]:
        raise SystemExit("clean JSONL replay mismatch")
    if load_canonical_gzip_json(clean_gzip, label="clean.json.gz") != clean:
        raise SystemExit("clean gzip JSON replay mismatch")

    mutations = 0
    for label, value in (("same", "PASS"), ("conflicting", "FAIL")):
        duplicate = (
            b'{"nested":{"a":1},"status":'
            + json.dumps(value).encode("utf-8")
            + b',"status":"PASS"}\n'
        )
        for suffix in ("jsonl.gz", "json.gz"):
            require_rejection(
                f"{label}-duplicate-{suffix}",
                "STRICT_JSON_DUPLICATE_NAME",
                lambda duplicate=duplicate, suffix=suffix: validate_release_json_member(
                    f"fixture.{suffix}", compressed(duplicate)
                ),
            )
            mutations += 1

    nested_duplicate = b'{"nested":{"a":1,"a":1},"status":"PASS"}'
    require_rejection(
        "recursive-duplicate-plain",
        "STRICT_JSON_DUPLICATE_NAME",
        lambda: decode_json_document(nested_duplicate, label="nested.json"),
    )
    mutations += 1
    for label, value in (("same", "PASS"), ("conflicting", "FAIL")):
        plain_duplicate = (
            b'{"nested":{"a":1},"status":'
            + json.dumps(value).encode("utf-8")
            + b',"status":"PASS"}'
        )
        require_rejection(
            f"{label}-duplicate-json",
            "STRICT_JSON_DUPLICATE_NAME",
            lambda plain_duplicate=plain_duplicate: validate_release_json_member(
                "fixture.json", plain_duplicate
            ),
        )
        mutations += 1
    long_name = "x" * 4096
    encoded_name = json.dumps(long_name).encode("utf-8")
    diagnostic = require_rejection(
        "bounded-duplicate-name-diagnostic",
        "STRICT_JSON_DUPLICATE_NAME",
        lambda: decode_json_document(
            b"{" + encoded_name + b":1," + encoded_name + b":2}",
            label="bounded.json",
        ),
    )
    if len(diagnostic) > 256:
        raise SystemExit("bounded-duplicate-name-diagnostic:unbounded diagnostic")
    mutations += 1
    require_rejection(
        "noncanonical-jsonl",
        "STRICT_JSON_NONCANONICAL_BYTES",
        lambda: list(
            iter_canonical_gzip_jsonl(
                compressed(b'{ "nested":{"a":1},"status":"PASS"}\n'),
                label="noncanonical.jsonl.gz",
            )
        ),
    )
    mutations += 1
    require_rejection(
        "noncanonical-gzip-document",
        "STRICT_JSON_NONCANONICAL_BYTES",
        lambda: load_canonical_gzip_json(
            compressed(b'{ "nested":{"a":1},"status":"PASS"}\n'),
            label="noncanonical.json.gz",
        ),
    )
    mutations += 1
    require_rejection(
        "missing-terminal-newline",
        "STRICT_JSON_TERMINAL_NEWLINE_FAIL",
        lambda: list(
            iter_canonical_gzip_jsonl(
                compressed(canonical_json_bytes(clean)), label="missing-newline.jsonl.gz"
            )
        ),
    )
    mutations += 1
    require_rejection(
        "line-bound",
        "STRICT_JSON_LINE_BYTE_LIMIT",
        lambda: list(
            iter_canonical_gzip_jsonl(
                clean_gzip, label="line-bound.jsonl.gz", max_line_bytes=8
            )
        ),
    )
    mutations += 1
    require_rejection(
        "total-bound",
        "STRICT_JSON_DECOMPRESSED_BYTE_LIMIT",
        lambda: list(
            iter_canonical_gzip_jsonl(
                clean_gzip,
                label="total-bound.jsonl.gz",
                max_total_bytes=len(clean_line) - 1,
            )
        ),
    )
    mutations += 1
    require_rejection(
        "document-bound",
        "STRICT_JSON_DECOMPRESSED_BYTE_LIMIT",
        lambda: load_canonical_gzip_json(
            clean_gzip,
            label="document-bound.json.gz",
            max_decompressed_bytes=len(clean_line) - 1,
        ),
    )
    mutations += 1
    for case, token in (
        ("nonfinite-NaN", b"NaN"),
        ("nonfinite-Infinity", b"Infinity"),
        ("nonfinite-exponent-overflow", b"1e999"),
    ):
        require_rejection(
            case,
            "STRICT_JSON_NONFINITE_NUMBER",
            lambda token=token: decode_json_document(
                b'{"value":' + token + b"}", label="nonfinite.json"
            ),
        )
        mutations += 1
    print(
        json.dumps(
            {
                "clean_documents": 2,
                "mutations_rejected": mutations,
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
