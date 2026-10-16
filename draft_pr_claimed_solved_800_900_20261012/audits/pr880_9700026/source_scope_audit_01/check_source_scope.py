#!/usr/bin/env python3
"""Read-only identity and exact parameter checks for PR880 source-scope audit.

This checks byte identities, exact-ID provenance, and finite algebra. It cannot
certify the analytic persistence theorem or infer historical novelty.
Only sanitized metadata is printed. No source or corpus record is printed.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


PINS = {
    "catalog.json": (21735099, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566", 15458),
    "cache/problems.json": (68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf", 15458),
    "cache/research_results.json": (80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b", 6701),
}
PDF_PINS = {
    "cities-notes.pdf": (295226, "9cfbe9da2660fcea7e44d7ef013cb7a8a1604ff54a9e7734e71ef76959c38b89"),
    "1209.5120v1.pdf": (398185, "eeecb371b6e6c2860c01e1b73d812468b619ddb7e3c4cd1d0e3affc056e8a077"),
}
MANIFEST_SHA = "b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b"
PAIR_SHA = "7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193"
STATEMENT_SHA = "5544971834bd618005b3fdf611f753b4cf41bab24b857d0e96a7a067ee3f7b7e"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    results = []

    def check(name, condition, **metadata):
        results.append(dict(name=name, passed=bool(condition), **metadata))

    corpus = args.workspace / "unsolved_math_prioritization"
    selected = {}
    for name, (size, digest, count) in PINS.items():
        data = (corpus / name).read_bytes()
        records = json.loads(data)
        check("corpus_identity:" + name, len(data) == size and sha(data) == digest and len(records) == count,
              bytes=len(data), sha256=sha(data), record_count=len(records))
        if isinstance(records, list):
            matches = [r for r in records if str(r.get("id")) == "9700026"]
            check("exact_id_unique:" + name, len(matches) == 1, matching_records=len(matches))
            if len(matches) != 1:
                raise RuntimeError("Exact numeric target is not unique")
            selected[name] = matches[0]
        else:
            report = records.get("AMR-096-0026", {})
            check("exact_prior_report_present", bool(report), matching_reports=int(bool(report)))
            selected[name] = report
        del records, data
    record = selected["cache/problems.json"]
    catalog = selected["catalog.json"]
    pair = json.dumps([record, selected["cache/research_results.json"]], sort_keys=True).encode("utf-8")
    check("canonical_complete_pair", len(pair) == 4409 and sha(pair) == PAIR_SHA,
          bytes=len(pair), sha256=sha(pair))
    check("catalog_review_binding", catalog["review_hash"] == sha(pair))
    check("catalog_statement_binding", catalog["statement_hash"] == sha(record["statement"].encode()) == STATEMENT_SHA)
    for name, (size, digest) in PDF_PINS.items():
        data = (args.audit / "private_sources" / name).read_bytes()
        check("primary_pdf_identity:" + name, len(data) == size and sha(data) == digest,
              bytes=len(data), sha256=sha(data))
    manifest_bytes = (args.audit / "SOURCE_MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    check("frozen_source_manifest", sha(manifest_bytes) == MANIFEST_SHA, sha256=sha(manifest_bytes))
    expected = {r["path"] for r in manifest["files"]}
    source_root = args.audit / "source"
    actual = {str(p.relative_to(source_root)) for p in source_root.rglob("*") if p.is_file()}
    check("frozen_source_exact_members", actual == expected and len(actual) == 40, file_count=len(actual))
    failures = []
    total = 0
    for row in manifest["files"]:
        data = (source_root / row["path"]).read_bytes()
        total += len(data)
        if len(data) != row["bytes"] or sha(data) != row["sha256"]:
            failures.append(row["path"])
    check("frozen_source_all_hashes", not failures and total == 276581, total_bytes=total, failures=failures)

    # Exact exponent vectors: influence_(2,8) = influence_(1/2,2)^4.
    alpha, beta = F(2), F(8)
    alpha2, beta2, scale = F(1, 2), F(2), F(4)
    check("exact_same_cells_under_exponent_rescaling", alpha == scale * alpha2 and beta == scale * beta2)
    check("example_in_literal_32a_and_persistence_region", alpha > 1 and beta > 2 * alpha)
    check("same_vector_field_parameters_in_literal_32b", 0 < alpha2 < 1 and beta2 > 2 * alpha2)
    check("ratio_and_area_exponent", alpha / beta == alpha2 / beta2 == F(1, 4) and 2 * alpha / beta == F(1, 2))
    # No numeric integration or sampled area is used to certify dynamics.
    output = dict(
        audit="PR880 / 9700026 / source-scope family",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        all_passed=all(r["passed"] for r in results),
        check_count=len(results), checks=results,
        analytic_theorem_certified=False,
        semantic_source_reading_certified_by_code=False,
        novelty_certified=False,
    )
    print(json.dumps(output, indent=2))
    if not output["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
