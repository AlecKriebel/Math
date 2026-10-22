#!/usr/bin/env python3
"""Bind complete external corpora without emitting their contents."""
from pathlib import Path
import hashlib
import json
import sys

class Rejected(Exception):
    pass

def require(condition, message):
    if not condition:
        raise Rejected(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(items):
    value = {}
    for k, v in items:
        require(k not in value, "duplicate JSON key")
        value[k] = v
    return value

def bad_constant(value):
    raise Rejected("nonfinite JSON constant")

def parse(raw):
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad_constant)

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True).encode("utf-8")

def ordinary_file(path):
    require(not path.is_symlink() and path.is_file(), "external input must be a regular file")
    return path.read_bytes()

def run():
    require(len(sys.argv) == 3, "usage: verify_corpus.py problems.json research_results.json")
    root = Path(__file__).resolve().parent
    pins = parse(ordinary_file(root / "CORPUS_BINDINGS.json"))
    require(pins["schema"] == "transverse-surgery-corpus-bindings-v1", "binding schema")
    parsed = []
    for arg, key in zip(sys.argv[1:], ("problems", "research_results")):
        raw = ordinary_file(Path(arg))
        expected = pins["corpora"][key]
        require(type(expected["bytes"]) is int and len(raw) == expected["bytes"], key + " byte count")
        require(sha(raw) == expected["sha256"], key + " hash mismatch")
        value = parse(raw)
        require(len(value) == expected["records"], key + " record count")
        parsed.append(value)
    problems, research = parsed
    require(type(problems) is list and type(research) is dict, "corpus types")
    matches = [x for x in problems if type(x) is dict and type(x.get("id")) is int
               and x["id"] == 10300034]
    require(len(matches) == 1, "unique target record")
    record = matches[0]
    require(record["problem_number"] == "AMR-102-0034", "target alias")
    report = research["AMR-102-0034"]
    require(sha(canonical(record)) == pins["record_sha256"], "record mismatch")
    require(sha(canonical(report)) == pins["research_record_sha256"], "research mismatch")
    require(sha(canonical({"problem": record, "research": report})) == pins["pair_sha256"], "pair mismatch")
    require(sha(record["statement"].encode("utf-8")) == pins["statement_sha256"], "statement mismatch")
    return {"schema": "transverse-surgery-corpus-replay-v1", "status": "pass", "problem_id": 10300034,
            "pair_sha256": pins["pair_sha256"], "contents_emitted": False}

if __name__ == "__main__":
    if sys.argv[1:] == ["--help"]:
        print("usage: verify_corpus.py problems.json research_results.json")
        sys.exit(0)
    try:
        print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
    except (Rejected, OSError, ValueError, TypeError, KeyError) as exc:
        print("REJECT: " + str(exc), file=sys.stderr)
        sys.exit(1)
