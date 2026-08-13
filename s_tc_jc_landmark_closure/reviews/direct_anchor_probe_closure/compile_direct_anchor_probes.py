#!/usr/bin/env python3
"""Compile exactly the one-/two-port extensions of the 62 direct n=3 anchors.

The scope is theorem-forced and bounded.  This program does not enumerate
networks or generators.  It reads the frozen 62 direct residual relations,
reconstructs their selected rooted graph pairs, proves their unique labelled
isomorphism/ordinary-T transports, and inserts at most two new ports on every
admissible internal blob arc.  Every non-topological child receives an exact
graph-derived JC Fourier separator.

No module from ``primary`` is imported.  Primary files are data inputs only.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import argparse
import copy
import gzip
import hashlib
import itertools
import json
import math

from exact_engine import (
    GL22, ONE, RootedGraph, admissible_internal_blob_arcs, classify_topology,
    delete_port, digest, graph_variables, insert_port, invariant_pullback,
    jc_reps, padd, peval, pmul, poly_digest, poly_json, pscale, pvar,
    quartet_tensor, root_is_lsa, standard_mixed, triangles, validate_rooted,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RELATIONS = PROJECT / "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_relations.jsonl.gz"
GRAPHS = PROJECT / "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_graphs.jsonl.gz"
FAMILY = PROJECT / "reviews/final_hard_cover_cleanroom/certificates/family_n3.json.gz"
HARD_COVER = PROJECT / "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz"
OUT = HERE / "certificates"

PRIMES = (1_000_003, 1_000_033, 1_000_037)
ALLOWED = {"labelled_isomorphism", "ordinary_T"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def stable(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def jsonl_gz(path: Path):
    with gzip.open(path, "rt") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def write_jsonl_gz(path: Path, rows) -> tuple[int, str]:
    rows = list(rows)
    logical = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
            for row in rows:
                encoded = (stable(row) + "\n").encode()
                stream.write(encoded)
                logical.update(encoded)
    return len(rows), logical.hexdigest()


def graph_sha(g: RootedGraph) -> str:
    return digest(g.to_json())


def local_strong(g: RootedGraph) -> bool:
    """The locked semidirected no-omnian criterion.

    Every tail of a retained reticulation edge must be incident with exactly
    two undirected edges after root suppression.
    """
    m = standard_mixed(g)
    undirected_degree = Counter()
    for u, v, hu, hv in m["edges"]:
        if not hu and not hv:
            undirected_degree[u] += 1
            undirected_degree[v] += 1
    for u, v, hu, hv in m["edges"]:
        if hu and not hv and undirected_degree[v] != 2:
            return False
        if hv and not hu and undirected_degree[u] != 2:
            return False
        if hu and hv:
            return False
    return True


def validate_locked(g: RootedGraph) -> None:
    problems = validate_rooted(g, require_tree_child=True)
    if problems:
        raise RuntimeError(f"rooted graph is invalid: {problems}")
    if not root_is_lsa(g):
        raise RuntimeError("root is not the lowest stable ancestor")
    if not local_strong(g):
        raise RuntimeError("standard mixed graph violates the locked strong criterion")
    if len(g.reticulations) > 2:
        raise RuntimeError("graph exceeds level two")


def edge_attributes(m):
    return {(u, v): (hu, hv) for u, v, hu, hv in m["edges"]}


def classify_fixed(source: RootedGraph, target: RootedGraph, mapping: dict[int, int]):
    """Check one fixed old-vertex transport without a permutation search."""
    sm, tm = standard_mixed(source), standard_mixed(target)
    sv, tv = set(sm["vertices"]), set(tm["vertices"])
    if set(mapping) != sv or set(mapping.values()) != tv:
        return None
    if any(sm["labels"].get(v) != tm["labels"].get(mapping[v]) for v in sv):
        return None
    se, te = edge_attributes(sm), edge_attributes(tm)
    if len(se) != len(te):
        return None
    mismatches = []
    for (u, v), attr in se.items():
        a0, b0 = mapping[u], mapping[v]
        a, b = sorted((a0, b0))
        if (a, b) not in te:
            return None
        moved = attr if a0 <= b0 else (attr[1], attr[0])
        if moved != te[(a, b)]:
            mismatches.append(((u, v), (a, b)))
    if not mismatches:
        return "labelled_isomorphism"
    st, tt = triangles(sm), triangles(tm)
    if len(st) != 1 or len(tt) != 1:
        return None
    sts, tts = set(st[0]), set(tt[0])
    if {mapping[v] for v in sts} != tts:
        return None
    if any(not ({u, v} <= sts and {a, b} <= tts) for (u, v), (a, b) in mismatches):
        return None
    return "ordinary_T"


def transport_record(source: RootedGraph, target: RootedGraph, mapping: dict[int, int], classification: str):
    sm, tm = standard_mixed(source), standard_mixed(target)
    target_edge_index = {(u, v): i for i, (u, v, _hu, _hv) in enumerate(tm["edges"])}
    edge_transport = []
    for i, (u, v, _hu, _hv) in enumerate(sm["edges"]):
        a, b = sorted((mapping[u], mapping[v]))
        edge_transport.append([i, target_edge_index[(a, b)]])
    st, tt = triangles(sm), triangles(tm)
    source_rets = set(source.reticulations)
    target_rets = set(target.reticulations)
    redirected_source = set(st[0]) if classification == "ordinary_T" else set()
    return {
        "classification": classification,
        "vertex_transport": [[u, mapping[u]] for u in sorted(mapping)],
        "edge_transport": edge_transport,
        "port_transport": [[label, label] for label in sorted(source.label_map.values())],
        "source_triangle": list(st[0]) if classification == "ordinary_T" else None,
        "target_triangle": list(tt[0]) if classification == "ordinary_T" else None,
        "reticulation_transport_outside_redirected_triangle": [
            [r, mapping[r]] for r in sorted(source_rets - redirected_source)
            if mapping[r] in target_rets
        ],
    }


def extend_mapping(parent: dict[int, int], source_insert, target_insert) -> dict[int, int]:
    out = dict(parent)
    out[int(source_insert["subdivision"])] = int(target_insert["subdivision"])
    out[int(source_insert["leaf"])] = int(target_insert["leaf"])
    return out


def relation_id(payload) -> str:
    return digest({
        "direct_anchor_id": payload["direct_anchor_id"],
        "parent_relation_id": payload["parent_relation_id"],
        "stage": payload["stage"],
        "new_label": payload["new_label"],
        "source_arc": payload["source_arc"],
        "target_arc": payload["target_arc"],
        "direction": payload["direction"],
    })


def load_family():
    with gzip.open(FAMILY, "rt") as stream:
        obj = json.load(stream)
    relations = tuple(
        tuple((int(c), tuple(int(i) for i in monomial)) for c, monomial in relation)
        for relation in obj["relations"]
    )
    return obj, relations


def family_relation_hash(relation) -> str:
    return digest([[c, list(m)] for c, m in relation])


def family_to_invariant(relation):
    terms = []
    for coefficient, monomial in relation:
        powers = Counter(monomial)
        terms.append({
            "coefficient": coefficient,
            "coordinate_powers": [[i, powers[i]] for i in sorted(powers)],
        })
    return {"terms": terms}


def deterministic_value(graph_id: str, variable: str, trial: int, prime: int) -> int:
    raw = hashlib.sha256(f"{graph_id}|{variable}|{trial}".encode()).digest()
    return 2 + int.from_bytes(raw[:8], "big") % (prime - 3)


@lru_cache(maxsize=8192)
def numeric_tensor(g: RootedGraph, selected: tuple[str, ...], trial: int):
    """Evaluate the JC orbit tensor directly in a finite field."""
    prime = PRIMES[trial]
    graph_id = graph_sha(g)
    variables = graph_variables(g)
    values = {v: deterministic_value(graph_id, v, trial, prime) for v in variables}
    incoming = {
        r: tuple(sorted((u, r) for u, v in g.arcs if v == r))
        for r in g.reticulations
    }
    labels_at = g.label_map
    switching_rows = []
    for bits in itertools.product((0, 1), repeat=len(incoming)):
        keep = set(g.arcs)
        weight = 1
        for r, bit in zip(sorted(incoming), bits):
            inc = incoming[r]
            keep.remove(inc[1 - bit])
            lam = values[f"l:{r}"]
            weight = weight * (lam if bit == 0 else 1 - lam) % prime
        children = defaultdict(list)
        for u, v in keep:
            children[u].append(v)
        order, seen = [], set()
        def dfs(v):
            if v in seen:
                return
            seen.add(v)
            for w in children[v]:
                dfs(w)
            order.append(v)
        dfs(g.root)
        descendants = {}
        for v in order:
            labels = {labels_at[v]} if v in labels_at else set()
            for w in children[v]:
                labels |= descendants[w]
            descendants[v] = labels
        switching_rows.append((weight, tuple((e, frozenset(descendants[e[1]])) for e in sorted(keep))))
    ans = []
    for assignment in jc_reps(len(selected)):
        chars = dict(zip(selected, assignment))
        total = 0
        for weight, rows in switching_rows:
            term = weight
            for edge, descendants in rows:
                char = 0
                for label in descendants:
                    char ^= chars.get(label, 0)
                if char:
                    term = term * values[f"x:{edge[0]}>{edge[1]}"] % prime
            total = (total + term) % prime
        ans.append(total)
    return tuple(ans)


def relation_value(values, relation, prime):
    total = 0
    for coefficient, monomial in relation:
        term = coefficient % prime
        for coordinate in monomial:
            term = term * values[coordinate] % prime
        total = (total + term) % prime
    return total


@lru_cache(maxsize=2048)
def exact_tensor(g: RootedGraph, quartet: tuple[str, ...]):
    return quartet_tensor(g, quartet)


def polynomial_from_relation(tensor, relation):
    return invariant_pullback(tensor, family_to_invariant(relation))


def sparse_from_sympy(poly, symbols):
    out = {}
    for powers, coeff in poly.terms():
        c = int(coeff)
        monomial = tuple((str(symbol), int(power)) for symbol, power in zip(symbols, powers) if power)
        if c:
            out[monomial] = c
    return out


def bernstein_sign(poly) -> tuple[int, list[int]] | None:
    """Return strict open-cube sign from exact Bernstein coefficients."""
    variables = sorted({v for monomial in poly for v, _power in monomial})
    if not variables:
        c = poly.get((), 0)
        return ((1 if c > 0 else -1), []) if c else None
    index = {v: i for i, v in enumerate(variables)}
    terms = []
    degrees = [0] * len(variables)
    for monomial, coefficient in poly.items():
        alpha = [0] * len(variables)
        for v, power in monomial:
            alpha[index[v]] = power
            degrees[index[v]] = max(degrees[index[v]], power)
        terms.append((tuple(alpha), coefficient))
    coefficients = []
    for beta in itertools.product(*(range(d + 1) for d in degrees)):
        value = Fraction(0)
        for alpha, coefficient in terms:
            if all(a <= b for a, b in zip(alpha, beta)):
                ratio = Fraction(coefficient)
                for a, b, d in zip(alpha, beta, degrees):
                    ratio *= Fraction(math.comb(b, a), math.comb(d, a))
                value += ratio
        coefficients.append(value)
    if all(c >= 0 for c in coefficients) and any(c > 0 for c in coefficients):
        return 1, degrees
    if all(c <= 0 for c in coefficients) and any(c < 0 for c in coefficients):
        return -1, degrees
    return None


def factor_sign_certificate(poly):
    import sympy as sp
    variables = sorted({v for monomial in poly for v, _power in monomial})
    if not variables:
        value = poly.get((), 0)
        return {"content": value, "factors": [], "sign": 1 if value > 0 else -1} if value else None
    symbols = sp.symbols("z0:" + str(len(variables)))
    by_name = dict(zip(variables, symbols))
    expr = 0
    for monomial, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for variable, power in monomial:
            term *= by_name[variable] ** power
        expr += term
    content, factors = sp.Poly(expr, *symbols, domain=sp.ZZ).factor_list()
    result = []
    total_sign = 1 if int(content) > 0 else -1
    for factor, multiplicity in factors:
        sparse_local = sparse_from_sympy(factor, symbols)
        # Restore the original variable names.
        sparse = {}
        for monomial, coefficient in sparse_local.items():
            restored = tuple((variables[int(v[1:])], power) for v, power in monomial)
            sparse[restored] = coefficient
        signed = bernstein_sign(sparse)
        if signed is None:
            return None
        sign, degrees = signed
        if multiplicity % 2:
            total_sign *= sign
        result.append({
            "multiplicity": int(multiplicity),
            "terms": poly_json(sparse),
            "sha256": poly_digest(sparse),
            "bernstein_sign": sign,
            "degrees": degrees,
        })
    return {"content": int(content), "factors": result, "sign": total_sign}


class SeparatorSearch:
    def __init__(self, family):
        self.family = family
        self.cache = {}
        self.exact_candidates = 0
        self.strict_candidates = 0

    def find(self, source: RootedGraph, target: RootedGraph, newest_label: str):
        pair_key = (graph_sha(source), graph_sha(target), newest_label)
        if pair_key in self.cache:
            return self.cache[pair_key]
        labels = tuple(sorted(source.label_map.values()))
        quartets = list(itertools.combinations(labels, 4))
        quartets.sort(key=lambda q: (newest_label not in q, q))
        for quartet in quartets:
            source_values = [numeric_tensor(source, quartet, trial) for trial in range(len(PRIMES))]
            target_values = [numeric_tensor(target, quartet, trial) for trial in range(len(PRIMES))]
            for index, relation in enumerate(self.family):
                sv = [relation_value(source_values[t], relation, PRIMES[t]) for t in range(len(PRIMES))]
                tv = [relation_value(target_values[t], relation, PRIMES[t]) for t in range(len(PRIMES))]
                if all(v == 0 for v in tv) and any(v != 0 for v in sv):
                    self.exact_candidates += 1
                    spoly = polynomial_from_relation(exact_tensor(source, quartet), relation)
                    tpoly = polynomial_from_relation(exact_tensor(target, quartet), relation)
                    if spoly and not tpoly:
                        witness = self._record(source, target, quartet, index, relation, spoly, tpoly,
                                               "source_nonzero_target_zero", None)
                        self.cache[pair_key] = witness
                        return witness
                if all(v == 0 for v in sv) and any(v != 0 for v in tv):
                    self.strict_candidates += 1
                    spoly = polynomial_from_relation(exact_tensor(source, quartet), relation)
                    tpoly = polynomial_from_relation(exact_tensor(target, quartet), relation)
                    if not spoly and tpoly:
                        sign = factor_sign_certificate(tpoly)
                        if sign is not None:
                            witness = self._record(source, target, quartet, index, relation, spoly, tpoly,
                                                   "source_zero_target_strict", sign)
                            self.cache[pair_key] = witness
                            return witness
        raise RuntimeError(f"no exact separator for pair {pair_key}")

    def _record(self, source, target, quartet, index, relation, spoly, tpoly, orientation, sign):
        payload = {
            "source_graph_sha256": graph_sha(source),
            "target_graph_sha256": graph_sha(target),
            "quartet": list(quartet),
            "family_relation_index": index,
            "family_relation_sha256": family_relation_hash(relation),
            "orientation": orientation,
            "source_pullback_sha256": poly_digest(spoly),
            "source_pullback_term_count": len(spoly),
            "target_pullback_sha256": poly_digest(tpoly),
            "target_pullback_term_count": len(tpoly),
            "target_strict_sign_certificate": sign,
        }
        payload["witness_id"] = digest(payload)
        return payload


def make_child_record(anchor_id, parent_id, stage, label, source, target, source_arc, target_arc,
                      parent_mapping, separator_search):
    source_child, source_insert = insert_port(source, tuple(source_arc), label)
    target_child, target_insert = insert_port(target, tuple(target_arc), label)
    mapping = extend_mapping(parent_mapping, source_insert, target_insert)
    classification = classify_fixed(source_child, target_child, mapping)
    record = {
        "schema": 1,
        "direct_anchor_id": anchor_id,
        "parent_relation_id": parent_id,
        "stage": stage,
        "new_label": label,
        "direction": "source_precedes_target",
        "source_arc": list(source_arc),
        "target_arc": list(target_arc),
        "source_graph_sha256": graph_sha(source_child),
        "target_graph_sha256": graph_sha(target_child),
        "source_deletion_exact_parent": delete_port(source_child, label)[0] == source,
        "target_deletion_exact_parent": delete_port(target_child, label)[0] == target,
    }
    record["relation_id"] = relation_id(record)
    if classification in ALLOWED:
        record["classification"] = classification
        record["transport"] = transport_record(source_child, target_child, mapping, classification)
        record["witness_id"] = None
    else:
        witness = separator_search.find(source_child, target_child, label)
        record["classification"] = (
            "generic_polynomial_separation" if witness["orientation"] == "source_nonzero_target_zero"
            else "strict_open_cube_separation"
        )
        record["transport"] = None
        record["witness_id"] = witness["witness_id"]
    return record, source_child, target_child, mapping


def compile_package():
    OUT.mkdir(parents=True, exist_ok=True)
    family_obj, family = load_family()
    all_relations = list(jsonl_gz(RELATIONS))
    direct = [r for r in all_relations if r.get("classification") == "isomorphism_or_T"]
    if len(all_relations) != 10_466 or len(direct) != 62:
        raise RuntimeError("frozen relation inventory is not the audited 10,466/62 universe")
    needed = {r["source_graph_id"] for r in direct} | {r["target_selected_graph_id"] for r in direct}
    graphs = {}
    primary_graph_rows = {}
    for row in jsonl_gz(GRAPHS):
        if row["graph_id"] in needed:
            graph = RootedGraph.from_json(row["rooted_graph"])
            graphs[row["graph_id"]] = graph
            primary_graph_rows[row["graph_id"]] = row
    if set(graphs) != needed:
        raise RuntimeError("a direct-anchor selected graph is missing")

    # Existing terminal families begin with at least five ports.  The direct
    # anchors have four, so there is no exact anchor-level representation.
    terminal_port_counts = Counter()
    terminal_count = 0
    for row in jsonl_gz(HARD_COVER):
        if row.get("terminal_classification") in {
            "support_prefix_labelled_isomorphism", "support_prefix_ordinary_T"
        }:
            terminal_count += 1
            terminal_port_counts[int(row["selected_port_count"])] += 1
    if terminal_count != 144 or min(terminal_port_counts) != 5:
        raise RuntimeError("existing terminal-family scope changed")

    anchors, p_records, q_records = [], [], []
    graph_catalog = {}
    witnesses = {}
    search = SeparatorSearch(family)

    for relation in sorted(direct, key=lambda r: r["relation_id"]):
        source = graphs[relation["source_graph_id"]]
        target = graphs[relation["target_selected_graph_id"]]
        validate_locked(source)
        validate_locked(target)
        candidates = classify_topology(source, target)
        if len(candidates) != 1:
            raise RuntimeError(f"direct anchor lacks a unique canonical transport: {relation['relation_id']}")
        classification, mapping = candidates[0]
        if classification not in ALLOWED:
            raise RuntimeError("direct anchor is neither isomorphism nor ordinary T")
        anchor = {
            "schema": 1,
            "direct_anchor_id": relation["relation_id"],
            "direction": relation["direction"],
            "port_correspondence": relation["port_correspondence"],
            "binding_sha256": relation["binding_sha256"],
            "raw_coverage_sha256": digest(relation["raw_coverage"]),
            "source_input_graph_id": relation["source_graph_id"],
            "target_selected_input_graph_id": relation["target_selected_graph_id"],
            "target_completion_input_graph_id": relation["target_completion_graph_id"],
            "source_graph_sha256": graph_sha(source),
            "target_graph_sha256": graph_sha(target),
            "selected_port_count": len(source.labels),
            "classification": classification,
            "transport": transport_record(source, target, mapping, classification),
        }
        anchor["anchor_certificate_id"] = digest(anchor)
        anchors.append(anchor)
        graph_catalog[graph_sha(source)] = source
        graph_catalog[graph_sha(target)] = target

        p_survivors = []
        for source_arc in admissible_internal_blob_arcs(source):
            for target_arc in admissible_internal_blob_arcs(target):
                record, sc, tc, child_mapping = make_child_record(
                    relation["relation_id"], relation["relation_id"], "A_plus_p", "L_4",
                    source, target, source_arc, target_arc, mapping, search,
                )
                p_records.append(record)
                graph_catalog[graph_sha(sc)] = sc
                graph_catalog[graph_sha(tc)] = tc
                if record["witness_id"]:
                    witnesses[record["witness_id"]] = search.cache[(graph_sha(sc), graph_sha(tc), "L_4")]
                else:
                    p_survivors.append((record, sc, tc, child_mapping))
        for parent, source_p, target_p, parent_mapping in p_survivors:
            for source_arc in admissible_internal_blob_arcs(source_p):
                for target_arc in admissible_internal_blob_arcs(target_p):
                    record, sc, tc, _child_mapping = make_child_record(
                        relation["relation_id"], parent["relation_id"], "A_plus_p_plus_q", "L_5",
                        source_p, target_p, source_arc, target_arc, parent_mapping, search,
                    )
                    q_records.append(record)
                    graph_catalog[graph_sha(sc)] = sc
                    graph_catalog[graph_sha(tc)] = tc
                    if record["witness_id"]:
                        witnesses[record["witness_id"]] = search.cache[(graph_sha(sc), graph_sha(tc), "L_5")]

    anchors.sort(key=lambda r: r["direct_anchor_id"])
    p_records.sort(key=lambda r: r["relation_id"])
    q_records.sort(key=lambda r: r["relation_id"])
    graph_rows = [
        {"graph_sha256": gid, "rooted_graph": graph_catalog[gid].to_json()}
        for gid in sorted(graph_catalog)
    ]
    witness_rows = [witnesses[k] for k in sorted(witnesses)]

    streams = {}
    for name, rows in (
        ("anchors", anchors), ("p_relations", p_records), ("q_relations", q_records),
        ("graphs", graph_rows), ("witnesses", witness_rows),
    ):
        path = OUT / f"{name}.jsonl.gz"
        count, logical = write_jsonl_gz(path, rows)
        streams[name] = {
            "path": str(path.relative_to(PROJECT)),
            "records": count,
            "logical_sha256": logical,
            "physical_sha256": sha256_file(path),
        }

    p_counts = Counter(r["classification"] for r in p_records)
    q_counts = Counter(r["classification"] for r in q_records)
    anchor_counts = Counter(r["classification"] for r in anchors)
    summary = {
        "schema": "direct-anchor-probe-closure-v1",
        "status": "EXACTLY_COMPUTED",
        "scope": "theorem-forced A+p/A+p+q extensions of the 62 direct n3 residual anchors",
        "inputs": {
            str(RELATIONS.relative_to(PROJECT)): sha256_file(RELATIONS),
            str(GRAPHS.relative_to(PROJECT)): sha256_file(GRAPHS),
            str(FAMILY.relative_to(PROJECT)): sha256_file(FAMILY),
            str(HARD_COVER.relative_to(PROJECT)): sha256_file(HARD_COVER),
        },
        "coverage_determination": {
            "all_direct_anchors_represented_by_existing_terminal_families": False,
            "reason": "all 62 direct anchors have four selected ports; every existing path-bound terminal anchor has at least five",
            "direct_anchor_selected_port_count": 4,
            "existing_terminal_anchor_port_counts": {str(k): v for k, v in sorted(terminal_port_counts.items())},
            "resolution": "compiled the complete direct-anchor extension family independently",
        },
        "family": {
            "relations": len(family),
            "normalized_sha256_without_hash": family_obj["normalized_sha256_without_hash"],
        },
        "counts": {
            "anchors": len(anchors),
            "anchor_classifications": dict(sorted(anchor_counts.items())),
            "A_plus_p": len(p_records),
            "A_plus_p_classifications": dict(sorted(p_counts.items())),
            "A_plus_p_survivors": sum(p_counts[k] for k in ALLOWED),
            "A_plus_p_plus_q": len(q_records),
            "A_plus_p_plus_q_classifications": dict(sorted(q_counts.items())),
            "A_plus_p_plus_q_survivors": sum(q_counts[k] for k in ALLOWED),
            "unique_separator_witnesses": len(witness_rows),
            "unique_graphs": len(graph_rows),
        },
        "separator_search": {
            "exact_candidate_expansions": search.exact_candidates,
            "strict_candidate_expansions": search.strict_candidates,
            "unresolved": [],
        },
        "streams": streams,
    }
    summary["normalized_sha256_without_hash"] = digest(summary)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    summary = compile_package()
    print(stable({"status": summary["status"], **summary["counts"]}))


if __name__ == "__main__":
    main()
