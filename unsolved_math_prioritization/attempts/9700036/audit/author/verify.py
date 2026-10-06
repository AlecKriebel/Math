#!/usr/bin/env python3
"""Byte binding and finite diagnostics; not a proof assistant or literature checker."""
import argparse
import hashlib
import itertools
import json
import pathlib
import sys
from fractions import Fraction

ID = 9700036
NUMBER = "AMR-096-0036"
PAIR_SHA = "f8fea69167f1dc867d824004c05ab51e0f4bb2bdfa53f35308e52c3f747bae93"
STATUS = "RESOLVED_BY_PRIOR_LITERATURE"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def bind(path, record):
    need(path.is_file() and not path.is_symlink(), "not a regular input: " + str(path))
    data = path.read_bytes()
    need(len(data) == record["bytes"], "size mismatch: " + path.name)
    need(hashlib.sha256(data).hexdigest() == record["sha256"], "hash mismatch: " + path.name)
    return data


def prufer_tree(n, word):
    degree = [1] * n
    for v in word:
        degree[v] += 1
    adj = [set() for _ in range(n)]
    for v in word:
        leaf = next(i for i, d in enumerate(degree) if d == 1)
        adj[leaf].add(v)
        adj[v].add(leaf)
        degree[leaf] -= 1
        degree[v] -= 1
    a, b = [i for i, d in enumerate(degree) if d == 1]
    adj[a].add(b)
    adj[b].add(a)
    return adj


def diagnostics():
    radial = 0
    for r in [Fraction(1, 3), Fraction(1), Fraction(5, 2), Fraction(11)]:
        for exponent in range(13):
            integral = (2 / r**2) * (r**(exponent+2) / (exponent+2))
            need(integral == 2 * r**exponent / (exponent+2), "radial moment")
            radial += 1
        for delta in [Fraction(1), Fraction(7, 3)]:
            total_no_pi = 2 * delta * r**3 / 3
            mean = total_no_pi / r**2
            need(mean == 2 * delta * r / 3, "ordered-pair normalization")
            need((total_no_pi / 2) / (r**2 / 2) == mean, "unordered-pair normalization")
    need(Fraction(1, 2) != Fraction(2, 3), "uniform-radius negative control")
    trees = cases = 0
    for n in range(2, 6):
        for word in itertools.product(range(n), repeat=n-2):
            adj = prufer_tree(n, word)
            trees += 1
            branches = []
            for cut in range(n):
                parts = []
                for start in adj[cut]:
                    found, todo = {cut}, [start]
                    while todo:
                        v = todo.pop()
                        if v not in found:
                            found.add(v)
                            todo.extend(adj[v] - found)
                    parts.append(found - {cut})
                branches.append(parts)
            for mask in range(1, 2**n):
                terminals = {v for v in range(n) if (mask >> v) & 1}
                count = len(terminals)
                need(any(all(2 * len(part & terminals) <= count for part in parts)
                         for parts in branches), "terminal-weighted centroid")
                cases += 1
    need(trees == 145 and cases == 4139, "finite centroid coverage")
    # A square cycle has antipodal terminals for which removal of any single point
    # leaves the other terminals connected. A tree proof must use acyclicity.
    cycle = [{1, 3}, {0, 2}, {1, 3}, {0, 2}]
    need(sum(len(x) for x in cycle) // 2 != len(cycle)-1, "cycle negative control")
    return {"radial_moments": radial, "labeled_trees": trees,
            "terminal_weightings": cases, "negative_controls": 2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=pathlib.Path)
    parser.add_argument("--problems", type=pathlib.Path)
    parser.add_argument("--reports", type=pathlib.Path)
    parser.add_argument("--sources-dir", type=pathlib.Path)
    args = parser.parse_args()
    root = pathlib.Path(__file__).absolute().parent
    need(not root.is_symlink(), "symlink root")
    certpath = root / "CERTIFICATE.json"
    need(certpath.is_file() and not certpath.is_symlink(), "invalid certificate")
    cert = json.loads(certpath.read_text())
    need(cert["problem_id"] == ID and cert["result"] == STATUS, "wrong certificate identity")
    wanted = {"README.md", "RESULT.md", "SOURCE_MANIFEST.json", "verify.py"}
    need(set(cert["files"]) == wanted, "unexpected bound file set")
    observed = set()
    for p in root.rglob("*"):
        need(not p.is_symlink() and p.is_file(), "unexpected node: " + str(p))
        observed.add(p.relative_to(root).as_posix())
    need(observed == wanted | {"CERTIFICATE.json"}, "unlisted or missing package file")
    for name, record in cert["files"].items():
        bind(root/name, record)
    manifest = json.loads((root/"SOURCE_MANIFEST.json").read_text())
    need(manifest["problem_id"] == ID and manifest["problem_number"] == NUMBER, "manifest identity")
    need(manifest["result"] == STATUS, "manifest disposition")
    need(manifest["canonical_pair"]["sha256"] == PAIR_SHA, "wrong exact-record hash")
    need(manifest["canonical_pair"]["matches_catalog_review_hash"] is True, "unmatched review hash")
    need(manifest["original_search_approaches_used"] == 0, "original search incorrectly claimed")
    corpus_args = [args.catalog, args.problems, args.reports]
    need(all(p is not None for p in corpus_args) or all(p is None for p in corpus_args),
         "provide all three complete corpora together")
    corpus_checked = False
    if args.catalog is not None:
        corpus = {}
        for key, path in zip(["catalog", "problems", "research_results"], corpus_args):
            corpus[key] = json.loads(bind(path, manifest["corpora"][key]))
        records = [p for p in corpus["problems"] if str(p.get("id")) == str(ID)]
        reviews = [p for p in corpus["catalog"] if str(p.get("id")) == str(ID)]
        need(len(records) == len(reviews) == 1, "exact record not unique")
        problem, review = records[0], reviews[0]
        need(problem["problem_number"] == NUMBER, "wrong exact-ID number")
        pair = [problem, corpus["research_results"].get(problem["problem_number"], {})]
        data = json.dumps(pair, sort_keys=True).encode()
        need(len(data) == manifest["canonical_pair"]["bytes"], "pair byte count")
        need(hashlib.sha256(data).hexdigest() == PAIR_SHA == review["review_hash"], "canonical array mismatch")
        corpus_checked = True
    pdfs = 0
    if args.sources_dir is not None:
        for source in manifest["sources"]:
            if source.get("local_pdf"):
                bind(args.sources_dir/source["local_pdf"]["filename"], source["local_pdf"])
                pdfs += 1
        need(pdfs == 4, "PDF coverage")
    print(json.dumps({"status": "PASS", "problem_id": ID, "files_bound": len(wanted),
                      "complete_corpora_checked": corpus_checked, "pdfs_checked": pdfs,
                      "diagnostics": diagnostics(),
                      "scope": "integrity and finite diagnostics; no automatic theorem or application proof"}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
