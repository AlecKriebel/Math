#!/usr/bin/env python3
"""Create independently resealed outer-manifest mutations in scratch."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    ).hexdigest()


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = canonical_hash(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    base = json.loads(args.source.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    def omit_bibliography(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"].pop(
            "proof_compression_submission/article/references.bib"
        )

    def stale_article_pdf(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"][
            "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf"
        ]["sha256"] = "a" * 64

    def stale_full_replay(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"][
            "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
        ]["sha256"] = "b" * 64

    def omit_portable_ledger(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"].pop(
            "output/referee/REFEREE_BUNDLE_CONTENTS.json"
        )

    mutations: dict[str, Callable[[dict[str, Any]], None]] = {
        "omit_bibliography": omit_bibliography,
        "stale_article_pdf": stale_article_pdf,
        "stale_full_replay": stale_full_replay,
        "omit_portable_ledger": omit_portable_ledger,
    }
    summary: dict[str, Any] = {}
    for name, mutate in mutations.items():
        value = copy.deepcopy(base)
        mutate(value)
        reseal(value)
        path = args.output_dir / f"{name}.json"
        encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
        path.write_text(encoded, encoding="utf-8")
        summary[name] = {
            "path": str(path),
            "bytes": len(encoded.encode()),
            "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            "payload_sha256": value["payload_sha256"],
        }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
