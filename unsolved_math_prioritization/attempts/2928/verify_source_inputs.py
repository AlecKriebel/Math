#!/usr/bin/env python3
"""Authenticate complete local corpus/PDF inputs for ID 2928; emit metadata only.

The immutable pins below are from the independently authenticated release.
This verifies input identity, not source-paper mathematics or current status.
No source text, corpus contents, or input filesystem paths are emitted.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

CORPUS_PINS = {
    "catalog": ("catalog.json", 21735099, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"),
    "problems": ("problems.json", 68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
    "reports": ("research_results.json", 80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
}
PDF_PINS = {
    "K3": ("k3.pdf", 6578041, "ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f"),
    "KNV": ("knv_v2.pdf", 618249, "afd0a973619a871ca6043984891f82f0185ebefb4e4cae0002c03b1a4c654e83"),
    "HU": ("hu_v1.pdf", 626364, "83e2b04b9ef499601b72ddfd4efca6841b469bce262452e8ec85aff77a84b800"),
    "KP": ("kp_v2.pdf", 419996, "7847135916536ec12d52d1490ffa0d7394d72bd7c0d3264bba1cf974789a276f"),
    "HKPR": ("hkpr_v1.pdf", 1274741, "943da4dadb5f29c7c080a6476376067354957fff64d7a831505556ca0f482f61"),
    "KL": ("kl_v3.pdf", 336056, "8dc347e82326122edce0b42e3c41964f4d658b5477065540c5b2b8513331cd6f"),
    "KL-v2-historical": ("kl_v2.pdf", 291289, "97c1856dd985f2cb0de1b024d3c766c0eef012198963263e0218eccf5c13dc72"),
    "KT-audit": ("kt_v1.pdf", 266657, "1858e3190f0dd1bb6b64c7513aee5c3cbf1716157b6ea5806dc55ed774ffe7b1"),
}
STATEMENT_SHA256 = "e1c2fc3f4719c4aa4fccd0bd7874dff67288523a5a3b82158093b6c24bb8fa1e"
PAIRED_RECORD_SHA256 = "d97f40398ba42a49e0499ac4d5ed0a4919e31facd4956cf65b62535b2b9c1bc9"
PROBLEM_ID = 2928
PROBLEM_NUMBER = "KP-4.52"
RANK = 919


class VerificationError(Exception):
    """Only fixed, public-safe failure labels may be passed to this exception."""


def require(condition, code):
    if not condition:
        raise VerificationError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def authenticate(path, pin, label):
    filename, expected_bytes, expected_hash = pin
    try:
        require(path.is_file() and not path.is_symlink(), label + ": input_not_regular_file")
        data = path.read_bytes()
    except OSError:
        raise VerificationError(label + ": input_unreadable") from None
    require(len(data) == expected_bytes, label + ": byte_count_mismatch")
    require(digest(data) == expected_hash, label + ": sha256_mismatch")
    return data, {"id": label, "filename": filename, "bytes": len(data),
                  "sha256": expected_hash, "matched": True}


def parse_json(data, label):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, label + ": duplicate_json_key")
            result[key] = value
        return result
    try:
        return json.loads(data, object_pairs_hook=unique)
    except (ValueError, UnicodeError):
        raise VerificationError(label + ": invalid_json") from None


def exact_record(items, expected_id, label):
    require(type(items) is list, label + ": not_array")
    require(all(type(item) is dict for item in items), label + ": nonobject_record")
    candidates = [item for item in items
                  if item.get("id") in (PROBLEM_ID, str(PROBLEM_ID))
                  or item.get("problem_number") == PROBLEM_NUMBER]
    require(len(candidates) == 1, label + ": target_not_unique")
    item = candidates[0]
    require(type(item.get("id")) is type(expected_id) and item["id"] == expected_id,
            label + ": target_id_mismatch")
    require(item.get("problem_number") == PROBLEM_NUMBER, label + ": target_code_mismatch")
    return item


def verify(args):
    # Authenticate every complete input before parsing or using its metadata.
    corpus_bytes = {}
    corpus_results = []
    for label, pin in CORPUS_PINS.items():
        data, result = authenticate(getattr(args, label), pin, label)
        corpus_bytes[label] = data
        corpus_results.append(result)
    pdf_results = []
    for label, pin in PDF_PINS.items():
        path = args.kt_pdf if label == "KT-audit" else args.pdf_directory / pin[0]
        data, result = authenticate(path, pin, label)
        require(data.startswith(b"%PDF-"), label + ": missing_pdf_header")
        result["historical_only"] = label == "KL-v2-historical"
        pdf_results.append(result)
    catalog = parse_json(corpus_bytes["catalog"], "catalog")
    problems = parse_json(corpus_bytes["problems"], "problems")
    reports = parse_json(corpus_bytes["reports"], "reports")
    selected = exact_record(catalog, "2928", "catalog")
    record = exact_record(problems, PROBLEM_ID, "problems")
    require(type(selected.get("rank")) is int and selected["rank"] == RANK,
            "catalog: rank_mismatch")
    require(type(reports) is dict, "reports: not_object")
    require(PROBLEM_NUMBER not in reports, "reports: unexpected_target_key")
    report = reports.get(PROBLEM_NUMBER, {})
    require(report == {}, "reports: nonempty_target_report")
    require(type(record.get("statement")) is str, "problems: statement_not_string")
    statement_hash = digest(record["statement"].encode("utf-8"))
    require(statement_hash == STATEMENT_SHA256, "problems: statement_hash_mismatch")
    pair_hash = digest(json.dumps([record, report], sort_keys=True).encode("utf-8"))
    require(pair_hash == PAIRED_RECORD_SHA256, "problems: complete_pair_hash_mismatch")
    return {
        "result": "PASS", "problem_id": PROBLEM_ID, "problem_number": PROBLEM_NUMBER,
        "rank": RANK, "complete_corpus_inputs_authenticated": corpus_results,
        "public_pdf_inputs_authenticated": pdf_results,
        "identity": {"unique_catalog_record": True, "unique_problem_record": True,
                     "catalog_id_type": "string", "problem_id_type": "integer",
                     "statement_sha256": statement_hash,
                     "paired_record_sha256": pair_hash,
                     "paired_record_serialization": "json.dumps([complete_record, reports.get(problem_number,{})], sort_keys=True) with default Python JSON formatting",
                     "associated_report_key_present": False, "associated_report_empty": True},
        "scope": "Complete pinned input bytes and selected identity metadata only; no mathematical proof certification or fresh online source-status verification",
        "source_contents_included": False, "dataset_contents_included": False,
        "local_paths_included": False,
    }


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        raise VerificationError("arguments: missing_or_invalid_argument")


def main():
    parser = SafeParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--problems", required=True, type=Path)
    parser.add_argument("--reports", required=True, type=Path)
    parser.add_argument("--pdf-directory", required=True, type=Path)
    parser.add_argument("--kt-pdf", required=True, type=Path)
    try:
        result = verify(parser.parse_args())
    except VerificationError as error:
        print(json.dumps({"result": "FAIL", "problem_id": PROBLEM_ID, "reason": str(error)}, sort_keys=True))
        return 1
    except Exception:
        # Do not disclose source content, unexpected exception text, or local paths.
        print(json.dumps({"result": "FAIL", "problem_id": PROBLEM_ID, "reason": "unexpected_verification_error"}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
