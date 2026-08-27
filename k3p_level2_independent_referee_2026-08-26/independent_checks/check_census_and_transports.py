#!/usr/bin/env python3
"""Independent streaming census and representative transport checks.

This is deliberately narrower than a regeneration of the restoration/probe
producers.  It recomputes ledger counts, ordered roots, self-hashes, references,
physical witness margins, and literal mixed-edge compatibility of every stored
transport.  It does not reconstruct every child graph from topology inputs.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path


PKG=Path("../package_copy/proof_package")


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def ordered_add(root,row):
    return sha({"previous":root,"row_sha256":sha(row)})


def iter_gz(path):
    with gzip.open(path,"rt") as f:
        for line in f:
            yield json.loads(line)


def ct_margin(triple):
    c,g,t=map(Q,triple)
    return min(c,g,t,1-c,1-g,1-t,1+c-g-t,1-c+g-t,1-c-g+t,
               c-g*t,g-c*t,t-c*g)


def validate_transport(row):
    rid=row["record_id"]; rec=row["record"]
    public=dict(rec);ordinary=public.pop("ordinary_triangle_arrowhead_witness",None)
    claimed=public.pop("transport_sha256")
    assert rid==claimed==sha(public)
    vm=dict(public["vertex_map"])
    assert len(vm)==len(public["vertex_map"])==len(set(vm.values()))
    source_edges=set();target_edges=set()
    for source,target in public["mixed_edge_map"]:
        source_edges.add(tuple(source));target_edges.add(tuple(target))
        assert {vm[source[0]],vm[source[1]]}==set(target)
    assert len(source_edges)==len(public["mixed_edge_map"])
    assert len(target_edges)==len(public["mixed_edge_map"])
    relation=public["relation"]
    if relation=="isomorphic":
        assert public["source_triangle_edges"] is None and public["target_triangle_edges"] is None and ordinary is None
    else:
        assert relation=="triangle" and ordinary is not None
        for side in ("source","target"):
            tri=public[f"{side}_triangle_edges"]
            headed=ordinary[f"{side}_headed_edges"]
            common=ordinary[f"{side}_common_reticulation"]
            assert len(tri)==3 and len(headed)==2
            assert all(common in e and e in tri for e in headed)
    return relation


def main():
    # Restoration registry and all ledger rows.
    rdir=PKG/"restoration"
    manifest=json.loads((rdir/"RESTORATION_MANIFEST.json").read_text())
    registry=json.load(gzip.open(rdir/"restoration_proof_registry.json.gz","rt"))
    logical=dict(registry); claimed=logical.pop("payload_sha256")
    assert claimed==sha(logical)
    prefixes={"displayed_quartet_mismatch":"Q:","k3p_tree_sunlet_sos":"K3P-TS:",
              "k3p_exact_multihomogeneous_quadratic":"K3P-Q2:","k3p_direct_marginal_quartic":"K3P-M4:"}
    min_witness_margin=None
    proof_ids=set()
    proof_checks=Counter()
    for kind,proofs in registry["proofs"].items():
        for pid,cert in proofs.items():
            assert pid==prefixes[kind]+sha(cert)
            proof_ids.add(pid);proof_checks[kind]+=1
            if kind=="displayed_quartet_mismatch":
                assert cert["source_splits"]!=cert["target_splits"]
            elif kind=="k3p_tree_sunlet_sos":
                assert {cert["tree_on"],cert["sunlet_on"]}=={"source","target"}
                assert cert["sunlet_nonzero_circuit_count"]>0
            else:
                assert cert["target_pullback_term_count"]==0<cert["source_pullback_term_count"]
                witness=cert["strict_source_witness"]
                margin=min([ct_margin(x) for x in witness["edge_triples"]]+[min(Q(x),1-Q(x)) for x in witness["inheritance"]])
                assert margin>0 and Q(witness["evaluation"])!=0
                min_witness_margin=margin if min_witness_margin is None else min(min_witness_margin,margin)

    rest_counts=Counter();layers=Counter();roots=set();row_hashes=[];used=set();second_parents=Counter()
    restoration_samples=[]
    for number,row in enumerate(iter_gz(rdir/"restoration_ledger.jsonl.gz")):
        public=dict(row); claimed=public.pop("row_sha256")
        assert claimed==sha(public) and row["edge_index"]==number
        row_hashes.append(claimed);rest_counts[row["proof_kind"]]+=1;layers[row["layer"]]+=1
        roots.add(row["root_id"]);used.add(row["proof_id"]);assert row["proof_id"] in proof_ids
        if row["layer"]==2: second_parents[row["parent_first_row_sha256"]]+=1
        if number in (0,36567,36568,36823):
            restoration_samples.append({"edge_index":number,"row_sha256":claimed,"proof_id":row["proof_id"],"layer":row["layer"]})
    assert sha(row_hashes)==manifest["ledger"]["ordered_row_hash_root"]
    assert layers==Counter({1:36568,2:256}) and set(second_parents.values())=={8} and len(second_parents)==32
    assert used==proof_ids

    # Probe registries: validate every transport/restriction self-hash and
    # literal endpoint action, retaining several representative IDs.
    pdir=PKG/"probes"; cert=json.loads((pdir/"K3P_PROBE_COHERENCE_CERTIFICATE.json").read_text())
    transports={};transport_counts=Counter();transport_root=sha([]);transport_samples=[]
    for n,row in enumerate(iter_gz(pdir/"exact_transport_ledger.jsonl.gz")):
        relation=validate_transport(row);rid=row["record_id"]
        assert rid not in transports;transports[rid]=relation;transport_counts[relation]+=1
        transport_root=ordered_add(transport_root,row)
        if (relation=="isomorphic" and not any(x["relation"]==relation for x in transport_samples)) or (relation=="triangle" and not any(x["relation"]==relation for x in transport_samples)):
            transport_samples.append({"record_index":n,"record_id":rid,"relation":relation,
                                      "vertex_count":len(row["record"]["vertex_map"]),"edge_count":len(row["record"]["mixed_edge_map"])})
    assert transport_root==cert["registries"]["exact_transports"]["ordered_records"]["ordered_hash_root"]

    restrictions=set();restriction_root=sha([])
    for row in iter_gz(pdir/"parent_restriction_ledger.jsonl.gz"):
        rid=row["record_id"]; assert rid=="R:"+sha(row["record"]);restrictions.add(rid)
        restriction_root=ordered_add(restriction_root,row)
    assert restriction_root==cert["registries"]["parent_restrictions"]["ordered_records"]["ordered_hash_root"]

    sep=json.load(gzip.open(pdir/"separation_proof_registry.json.gz","rt"))
    topological=sep["separation_proof_registry"]
    k3p=sep["k3p_tree_sunlet_registry"]["certificates"]
    assert all(pid=="Q:"+sha(x) for pid,x in topological.items())
    assert all(pid=="K3P-TS:"+sha(x) for pid,x in k3p.items())

    one_counts=Counter();one_origin=Counter();one_root=sha([]);one_equalities=[];one_samples={}
    for n,row in enumerate(iter_gz(pdir/"one_port_ledger.jsonl.gz")):
        one_root=ordered_add(one_root,row);status=row["status"];one_counts[status]+=1;one_origin[(row["origin"],status)]+=1
        assert row["source_parent_restriction_id"] in restrictions and row["target_parent_restriction_id"] in restrictions
        if status in ("isomorphic","triangle"):
            assert row["transport_id"] in transports and transports[row["transport_id"]]==status
            one_equalities.append(f"P1:{row['parent_anchor_id']}:{row['source_site_index']}:{row['target_site_index']}")
        else:
            assert row["proof_id"] in (topological if status=="displayed_quartet_mismatch" else k3p)
        one_samples.setdefault(status,{"row":n,"digest":sha(row),"parent":row["parent_anchor_id"]})
    assert one_root==cert["one_port"]["ordered_ledger"]["ordered_hash_root"]
    assert dict(one_counts)==cert["one_port"]["counts"] and len(one_equalities)==2107

    parent_ids=[];parent_root=sha([]);raw_second=0;profile_type_counts=Counter()
    for n,row in enumerate(iter_gz(pdir/"two_port_parent_inventory.jsonl.gz")):
        parent_root=ordered_add(parent_root,row);pid=row["one_port_parent_id"];parent_ids.append(pid)
        assert pid==one_equalities[n]
        for side in ("source_candidate_profile","target_candidate_profile"):
            p=row[side];assert p["site_count"]==2*p["port_count"]+3*p["reticulation_count"]-3==len(p["sites"])
            assert p["ordered_site_hash_root"]==sha([sha(x) for x in p["sites"]])
            profile_type_counts.update(p["site_type_census"])
        pairs=row["source_candidate_profile"]["site_count"]*row["target_candidate_profile"]["site_count"]
        assert pairs==row["raw_second_probe_pairs"];raw_second+=pairs
    assert parent_root==cert["two_port"]["ordered_parent_inventory"]["ordered_hash_root"] and raw_second==544571

    two_counts=Counter();two_root=sha([]);two_samples={};reverse_counts=Counter()
    for n,row in enumerate(iter_gz(pdir/"two_port_ledger.jsonl.gz")):
        two_root=ordered_add(two_root,row);status=row["status"];two_counts[status]+=1
        assert row["source_parent_restriction_id"] in restrictions and row["target_parent_restriction_id"] in restrictions
        if status in ("isomorphic","triangle"):
            assert row["transport_id"] in transports and transports[row["transport_id"]]==status
            reverse=row["reverse_order_certificate"];assert reverse["reverse_parent_transport_id"] in transports
            assert reverse["same_base_anchor_id"]==row["base_anchor_id"]
            reverse_counts[reverse["reverse_parent_relation"]]+=1
        else:
            assert row["proof_id"] in (topological if status=="displayed_quartet_mismatch" else k3p)
        two_samples.setdefault(status,{"row":n,"digest":sha(row),"parent":row["one_port_parent_id"]})
    assert two_root==cert["two_port"]["ordered_ledger"]["ordered_hash_root"]
    assert dict(two_counts)==cert["two_port"]["counts"]

    result={
      "restoration":{"rows":sum(layers.values()),"layers":dict(layers),"proof_use":dict(rest_counts),
        "unique_proofs":len(used),"unique_roots":len(roots),"ordered_root":sha(row_hashes),
        "minimum_checked_CT_witness_margin":str(min_witness_margin),"samples":restoration_samples},
      "probes":{"one_counts":dict(one_counts),"one_ordered_root":one_root,"one_samples":one_samples,
        "two_counts":dict(two_counts),"two_ordered_root":two_root,"two_samples":two_samples,
        "one_equality_survivors":len(one_equalities),"parent_inventory":len(parent_ids),"raw_second_pairs":raw_second,
        "transport_records":len(transports),"transport_relations":dict(transport_counts),"transport_ordered_root":transport_root,
        "restriction_records":len(restrictions),"restriction_ordered_root":restriction_root,
        "transport_samples":transport_samples,"reverse_relation_counts":dict(reverse_counts)},
      "limitations":"All stored rows were streamed and their structural/hash/reference invariants checked. This does not independently regenerate the restoration forest, probe candidate graphs, or every polynomial pullback; representative separator mathematics is checked in the other independent scripts."
    }
    Path("census_and_transport_results.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":main()
