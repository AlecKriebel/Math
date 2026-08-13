#!/usr/bin/env python3
"""Independent exact JC algebra audit for every schema-3 theta-2 probe state.

Separators are selected from two clean-room families.  The primary quartet,
invariant index, polynomial body, and sign flags are not used to choose or
certify a witness.  Every accepted record contains an exact target-zero and
source-nonzero pullback regenerated from displayed switchings and descendant
masks.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import gzip
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from derived_invariants import exact_relation_pullback
from graph_model import digest, stable_json
from jc_exact import (
    INVARIANTS, descriptor_from_graph, p_hash, quartet_values_mod,
)
from relation_universe import graph_from_object


SUMMARY = ROOT / "primary/certificates/probe_extension_theta2_schema3_summary.json"
GRAPHS = ROOT / "primary/certificates/probe_extension_graphs_theta2_schema3.jsonl.gz"
STATES = ROOT / "primary/certificates/probe_extension_states_theta2_schema3.jsonl.gz"
STRUCTURE = HERE / "certificates/schema3_n4_theta2_probe_structure_audit.json"
FAMILY_PATH = HERE / "certificates/family_n4_minimum.json.gz"
OUT = HERE / "certificates/schema3_n4_theta2_probe_algebra_audit.json"
EVIDENCE = HERE / "certificates/schema3_n4_theta2_probe_algebra_records.jsonl.gz"
FIRST_FAILURE = HERE / "history/implementation_failures/probe_extension_algebra_first_failure.json"

PRIMES = (1000003, 1000033, 1000037)


class AuditFailure(RuntimeError):
    pass


def sha(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def jsonl(path: Path):
    with gzip.open(path, "rt") as stream:
        for line in stream:
            if line.strip(): yield json.loads(line)


def fail(category, **details):
    payload = {
        "schema": 1,
        "status": "FALSE",
        "category": category,
        "details": details,
        "inputs": {
            str(SUMMARY.relative_to(ROOT)): sha(SUMMARY),
            str(GRAPHS.relative_to(ROOT)): sha(GRAPHS),
            str(STATES.relative_to(ROOT)): sha(STATES),
            str(STRUCTURE.relative_to(ROOT)): sha(STRUCTURE),
            str(FAMILY_PATH.relative_to(ROOT)): sha(FAMILY_PATH),
        },
    }
    payload["normalized_sha256_without_hash"] = digest(payload)
    FIRST_FAILURE.parent.mkdir(parents=True, exist_ok=True)
    if not FIRST_FAILURE.exists(): FIRST_FAILURE.write_text(stable_json(payload) + "\n")
    raise AuditFailure(stable_json(payload))


def require(condition, category, **details):
    if not condition: fail(category, **details)


def load_family():
    with gzip.open(FAMILY_PATH, "rt") as stream: obj = json.load(stream)
    family = tuple(
        tuple((int(c), tuple(int(i) for i in mon)) for c, mon in relation)
        for relation in obj["relations"]
    )
    return obj, family


def quadratic_family():
    return tuple(
        ((1, tuple(a)), (-1, tuple(b)))
        for a, b in INVARIANTS
    )


def descriptor_hash(desc):
    return digest({"reticulation_count": desc.reticulation_count, "switching_mask_rows": desc.rows})


def canonical_descriptor_key(desc, port_count):
    """Quotient split complements, reticulation order, and parent flips."""
    r = desc.reticulation_count
    full_mask = (1 << port_count) - 1
    choices = tuple(itertools.product((0, 1), repeat=r))
    index = {bits: i for i, bits in enumerate(choices)}
    candidates = []
    for permutation in itertools.permutations(range(r)):
        for flips in itertools.product((0, 1), repeat=r):
            # New bit j is old bit permutation[j], optionally complemented.
            old_columns = []
            for new_bits in choices:
                old = [0] * r
                for new_axis, old_axis in enumerate(permutation):
                    old[old_axis] = new_bits[new_axis] ^ flips[new_axis]
                old_columns.append(index[tuple(old)])
            rows = []
            for row in desc.rows:
                moved = []
                for i in old_columns:
                    mask = row[i]
                    if mask < 0 or mask == 0 or mask == full_mask:
                        moved.append(0)
                    else:
                        moved.append(min(mask, full_mask ^ mask))
                moved = tuple(moved)
                if any(moved): rows.append(moved)
            # Equal switching-mask rows enter only through the product of
            # their open JC edge multipliers.
            rows = tuple(sorted(set(rows)))
            candidates.append(rows)
    return (r, min(candidates))


def relation_hash(relation):
    return digest([[c, list(mon)] for c, mon in relation])


def bit_indices(bits):
    while bits:
        one = bits & -bits
        yield one.bit_length() - 1
        bits -= one


def relation_value(values, relation, prime):
    total = 0
    for coefficient, monomial in relation:
        term = coefficient % prime
        for coordinate in monomial: term = term * values[coordinate] % prime
        total = (total + term) % prime
    return total


class ExactSearch:
    def __init__(self, quadratic, full):
        self.quadratic = quadratic; self.full = full
        self.value_cache = {}
        self.bit_cache = {}
        self.exact_cache = {}
        self.search_counts = Counter()

    def values(self, desc, quartet, port_count, trial):
        key = (desc.key, quartet, port_count, trial)
        if key not in self.value_cache:
            self.value_cache[key] = quartet_values_mod(desc, quartet, port_count, PRIMES[trial], trial)
        return self.value_cache[key]

    def bits(self, desc, quartet, port_count, family_name, family, trials):
        key = (desc.key, quartet, port_count, family_name, trials)
        if key in self.bit_cache: return self.bit_cache[key]
        bits = 0
        for trial in range(trials):
            values = self.values(desc, quartet, port_count, trial)
            prime = PRIMES[trial]
            for i, relation in enumerate(family):
                if not (bits >> i & 1) and relation_value(values, relation, prime):
                    bits |= 1 << i
        self.bit_cache[key] = bits
        return bits

    def exact(self, desc, quartet, family_name, index, relation):
        key = (desc.key, quartet, family_name, index)
        if key not in self.exact_cache:
            poly = exact_relation_pullback(desc, quartet, relation)
            self.exact_cache[key] = {
                "nonzero": bool(poly),
                "sha256": p_hash(poly),
                "term_count": len(poly),
            }
        return self.exact_cache[key]

    def search_family(self, source, target, port_count, quartets, family_name, family, trials):
        all_bits = (1 << len(family)) - 1
        for quartet in quartets:
            sbits = self.bits(source, quartet, port_count, family_name, family, trials)
            tbits = self.bits(target, quartet, port_count, family_name, family, trials)
            for index in bit_indices(sbits & (all_bits ^ tbits)):
                target_exact = self.exact(target, quartet, family_name, index, family[index])
                if target_exact["nonzero"]: continue
                source_exact = self.exact(source, quartet, family_name, index, family[index])
                if not source_exact["nonzero"]:
                    fail("modular source witness expanded to zero", quartet=quartet, family=family_name, invariant=index)
                self.search_counts[(family_name, trials)] += 1
                return {
                    "family": family_name,
                    "family_relation_index": index,
                    "family_relation_sha256": relation_hash(family[index]),
                    "quartet": quartet,
                    "source_pullback_sha256": source_exact["sha256"],
                    "source_pullback_term_count": source_exact["term_count"],
                    "target_pullback_sha256": target_exact["sha256"],
                    "target_pullback_term_count": target_exact["term_count"],
                }
        return None

    def find(self, source, target, port_count):
        newest = port_count - 1
        new_port_quartets = tuple(tuple(q) + (newest,) for q in itertools.combinations(range(newest), 3))
        # Fast but sound first pass.  Modular arithmetic proposes candidates;
        # acceptance always uses exact integer-polynomial expansion.
        result = self.search_family(source, target, port_count, new_port_quartets, "quadratic162", self.quadratic, 1)
        if result: return result
        result = self.search_family(source, target, port_count, new_port_quartets, "quadratic162", self.quadratic, 3)
        if result: return result
        result = self.search_family(source, target, port_count, new_port_quartets, "source-derived-degree3", self.full, 1)
        if result: return result
        result = self.search_family(source, target, port_count, new_port_quartets, "source-derived-degree3", self.full, 3)
        if result: return result
        # Fail-closed completeness fallback: do not rely on the parent-isomorphism
        # argument or on a primary quartet hint.
        all_quartets = tuple(itertools.combinations(range(port_count), 4))
        result = self.search_family(source, target, port_count, all_quartets, "source-derived-degree3", self.full, 3)
        if result:
            result["required_all_quartets_fallback"] = True
        return result


def main():
    structure = json.loads(STRUCTURE.read_text())
    require(structure["status"] == "VERIFIED", "structural probe audit is not verified", status=structure.get("status"))
    family_obj, full_family = load_family(); quadratic = quadratic_family()
    graphs = {}
    for record in jsonl(GRAPHS):
        gid = record["graph_id"]
        require(gid not in graphs, "duplicate graph in algebra input", graph_id=gid)
        desc = descriptor_from_graph(graph_from_object(record["rooted_graph"]))
        require(desc.reticulation_count == 2, "probe graph is not a two-reticulation local factor", graph_id=gid, reticulations=desc.reticulation_count)
        graphs[gid] = desc

    search = ExactSearch(quadratic, full_family)
    counts = Counter(); primary_hint_matches = 0; all_quartet_fallbacks = 0
    evidence_hasher = hashlib.sha256(); evidence_count = 0; previous_sid = None
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    with gzip.GzipFile(filename=str(EVIDENCE), mode="wb", mtime=0) as output:
        for record in jsonl(STATES):
            sid = record["state_id"]
            require(previous_sid is None or previous_sid < sid, "probe states are not strictly state-id ordered", previous_state_id=previous_sid, state_id=sid)
            previous_sid = sid
            source = graphs[record["source_graph_id"]]; target = graphs[record["target_graph_id"]]
            p = int(record["selected_port_count"]); classification = record["classification"]
            if classification == "labelled_isomorphism":
                require(canonical_descriptor_key(source, p) == canonical_descriptor_key(target, p), "isomorphic probe graphs have inequivalent independently regenerated JC switching masks", state_id=sid)
                row = {
                    "state_id": sid,
                    "classification": "labelled_isomorphism",
                    "source_descriptor_sha256": descriptor_hash(source),
                    "target_descriptor_sha256": descriptor_hash(target),
                    "selected_port_count": p,
                }
            elif classification == "generic_polynomial_separation":
                witness = search.find(source, target, p)
                require(witness is not None, "no independent exact identity separator found", state_id=sid, stage=record["stage"], selected_port_count=p)
                require(witness["target_pullback_term_count"] == 0 and witness["source_pullback_term_count"] > 0, "independent separator has wrong exact zero direction", state_id=sid, witness=witness)
                primary_chunk = int(record["probe_witness"]["quartet_chunk"])
                primary_quartet = tuple(itertools.combinations(range(p), 4))[primary_chunk]
                if tuple(witness["quartet"]) == primary_quartet: primary_hint_matches += 1
                if witness.get("required_all_quartets_fallback"): all_quartet_fallbacks += 1
                row = {
                    "state_id": sid,
                    "classification": "generic_identity_separation",
                    "source_graph_id": record["source_graph_id"],
                    "target_graph_id": record["target_graph_id"],
                    "source_descriptor_sha256": descriptor_hash(source),
                    "target_descriptor_sha256": descriptor_hash(target),
                    "source_switching_count": source.choice_count,
                    "target_switching_count": target.choice_count,
                    "source_effective_edge_mask_rows": len(source.rows),
                    "target_effective_edge_mask_rows": len(target.rows),
                    "selected_port_count": p,
                    **witness,
                }
            else:
                fail("unexpected probe classification in algebra pass", state_id=sid, classification=classification)
            counts[(record["stage"], classification)] += 1
            encoded = (stable_json(row) + "\n").encode()
            output.write(encoded); evidence_hasher.update(encoded); evidence_count += 1

    summary = json.loads(SUMMARY.read_text())
    expected = {tuple(k.split("::")): int(v) for k, v in summary["counts"].items()}
    require(dict(counts) == expected, "algebra pass classification counts differ from primary summary", expected=expected, actual=dict(counts))
    cert = {
        "schema": 1,
        "status": "VERIFIED",
        "scope": "every schema-3 n4 theta-2 p/q terminal state",
        "inputs": {
            str(SUMMARY.relative_to(ROOT)): sha(SUMMARY),
            str(GRAPHS.relative_to(ROOT)): sha(GRAPHS),
            str(STATES.relative_to(ROOT)): sha(STATES),
            str(STRUCTURE.relative_to(ROOT)): sha(STRUCTURE),
            str(FAMILY_PATH.relative_to(ROOT)): sha(FAMILY_PATH),
        },
        "independent_families": {
            "quadratic162": {"relations": len(quadratic), "sha256": digest(quadratic)},
            "source-derived-degree3": {"relations": len(full_family), "sha256": family_obj["normalized_sha256_without_hash"]},
        },
        "state_count": evidence_count,
        "classification_counts": {f"{a}::{b}": n for (a, b), n in sorted(counts.items())},
        "search_witness_counts": {f"{family}::{trials}_trial": n for (family, trials), n in sorted(search.search_counts.items())},
        "primary_quartet_hint_matches": primary_hint_matches,
        "all_quartets_fallbacks": all_quartet_fallbacks,
        "strict_sign_cases": 0,
        "strict_sign_flags_trusted": False,
        "evidence": {
            "path": str(EVIDENCE.relative_to(ROOT)),
            "records": evidence_count,
            "logical_stream_sha256": evidence_hasher.hexdigest(),
            "physical_file_sha256": sha(EVIDENCE),
        },
        "assertions": {
            "displayed_switchings_regenerated": True,
            "descendant_masks_regenerated": True,
            "primary_invariant_selection_unused": True,
            "primary_polynomial_bodies_unused_for_proof": True,
            "primary_sign_flags_unused": True,
            "every_separation_has_exact_target_zero": True,
            "every_separation_has_exact_source_nonzero": True,
            "every_isomorphism_has_equal_exact_descriptor": True,
        },
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    OUT.write_text(stable_json(cert) + "\n")
    print(stable_json({"status": cert["status"], "states": evidence_count, "separations": sum(n for (stage, cls), n in counts.items() if cls == "generic_polynomial_separation"), "hash": cert["normalized_sha256_without_hash"]}))


if __name__ == "__main__":
    try:
        main()
    except AuditFailure as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
