#!/usr/bin/env python3
"""Entire rational certificate verification using indexed 3-regular-tree geometry.
Python >=3.10, standard library only; no numerical solver, claimant script,
network or file writes. Finite certificate proof is completed by the manuscript's
Thomson/Kirchhoff/free-exhaustion transfer.
Original code: Alec Kriebel, 2026. SPDX-License-Identifier: MIT.
"""
from pathlib import Path
import gzip
import hashlib
import json
from fractions import Fraction as F

PIN = "6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f"
D = 10**9
ENERGY = 3208526010913748780

def require(test, message):
    if not test:
        raise RuntimeError(message)

def toward_root(i):
    return 0 if i <= 3 else (i-2)//2

def tree_adj(i):
    # Breadth-first indices: root children 1,2,3; i>=1 children 2i+2,2i+3.
    return [1,2,3] if i == 0 else [toward_root(i),2*i+2,2*i+3]

def on_end_ray(i):
    # The distinguished ray is 0,1,4,10,22,...; classify without a depth cutoff.
    if i == 0:
        return True
    while i > 1:
        if i % 2:
            return False
        i = (i-2)//2
    return i == 1

def parent(i):
    if i == 0:
        return 1
    return 2*i+2 if on_end_ray(i) else toward_root(i)

def infinite_G_adj(i):
    children = [j for j in tree_adj(i) if j != parent(i)]
    require(len(children) == 2, "two end-oriented children")
    grandchildren = [z for j in children for z in tree_adj(j) if z != i]
    result = {parent(i),parent(parent(i)),*children,*grandchildren}
    require(len(result) == 8 and i not in result, "eight distinct G neighbors")
    return result

def finite_graph(radius):
    n = 1+3*(2**radius-1)
    a = [set() for _ in range(n)]
    # Generate only the defining ancestor edges, then make them unoriented.
    for i in range(n):
        for j in (parent(i),parent(parent(i))):
            if j < n:
                require(i != j, "no loop")
                a[i].add(j);a[j].add(i)
    require(all(a[i] == {j for j in infinite_G_adj(i) if j < n}
                for i in range(n)), "full endpoint-restricted G")
    h = [set(nei) for nei in a]
    for i in range(n):
        for j in a[i]:
            h[i].update(a[j])
        h[i].discard(i)
    require(all(i in h[j] for i in range(n) for j in h[i]), "square undirected")
    edges = sorted((i,j) for i in range(n) for j in h[i] if i < j)
    return n,a,h,edges

def inspect_flow(row, edges, n, source, denominator=D):
    require(type(source) is int and 0 < source < n, "source")
    require(type(row) is list and len(row) == len(edges), "flow length")
    div = [0]*n
    energy = 0
    for v,(i,j) in zip(row,edges):
        require(type(v) is int, "actual integer current, not bool/float")
        div[i] += v
        div[j] -= v
        energy += v*v
    for i,v in enumerate(div):
        expected = denominator if i == source else (-denominator if i == 0 else 0)
        require(v == expected, "divergence at vertex "+str(i))
    return energy

def must_fail(call, why):
    try:
        call()
    except RuntimeError:
        return
    raise RuntimeError("deliberate corruption escaped: "+why)

def check(data):
    require(type(data) is dict, "certificate object")
    require(data["q"] == 2 and type(data["q"]) is int and
            data["radius"] == 10 and type(data["radius"]) is int, "parameters")
    n,a,h,edges = finite_graph(10)
    require(n == 3070 and len(edges) == 19931 and data["vertices"] == n,
            "finite graph dimensions")
    require(data["edge_order"] == [list(e) for e in edges], "complete edge order")
    for edge in data["edge_order"]:
        require(type(edge) is list and len(edge) == 2 and
                all(type(v) is int for v in edge), "actual integer endpoints")
    N = infinite_G_adj(0)
    full = set(N)
    for j in N:
        full.update(infinite_G_adj(j))
    full.discard(0)
    require(len(N) == 8 and len(full) == 40 and h[0] == full,
            "all infinite square neighbors, not a selected subset")
    targets = sorted(full)
    require(data["root_neighbors"] == targets and
            all(type(i) is int for i in data["root_neighbors"]), "terminal order")
    require(type(data["denominator"]) is int and data["denominator"] == D,
            "common denominator")
    require(len(data["flows"]) == 40 and len(data["energy_numerators"]) == 40,
            "all forty flows and energies")
    energies = [inspect_flow(row,edges,n,v) for v,row in zip(targets,data["flows"])]
    require(all(type(v) is int for v in data["energy_numerators"]) and
            energies == data["energy_numerators"], "all exact energies")
    require(type(data["total_energy_numerator"]) is int and
            sum(energies) == data["total_energy_numerator"] == ENERGY,
            "total energy")
    require(type(data["total_energy_denominator"]) is int and
            data["total_energy_denominator"] == D*D, "energy denominator")
    require(100*ENERGY < 321*D*D, "strict square bound 321/100")
    require(F(73,50)**2 > 2 and (F(24)-F(73,50))/7 == F(161,50),
            "radical-free lower bound")
    require((F(161,50)-F(321,100))/2 == F(1,200), "strict b_F gap")
    # Recover original tree and parent intrinsically at the root.
    require(sorted(len(N & infinite_G_adj(j)) for j in N) == [1]*5+[3]*3,
            "triangle distinction")
    tn = set(tree_adj(0))
    require({j:len(tn & infinite_G_adj(j)) for j in tn} == {1:2,2:1,3:1},
            "unique parent in induced K_1,2")
    # Actual parser/feasibility controls on entire genuine rows, not fake energies.
    bad = data["flows"][0].copy();bad[0] += 1
    must_fail(lambda:inspect_flow(bad,edges,n,targets[0]), "one changed current")
    must_fail(lambda:inspect_flow(data["flows"][0],edges,n,targets[1]), "wrong source")
    badtype = data["flows"][0].copy();badtype[0] = True
    must_fail(lambda:inspect_flow(badtype,edges,n,targets[0]), "boolean numerator")
    must_fail(lambda:inspect_flow(data["flows"][0][:-1],edges,n,targets[0]), "missing entry")
    return {"status":"PASS","graph_vertices":n,"graph_edges":len(edges),
            "root_degree_G":8,"root_degree_Gsquare":40,
            "currents_verified":40*len(edges),"divergences_verified":40*n,
            "denominator":D,"targets":targets,"energy_numerators":energies,
            "total_energy_numerator":sum(energies),"total_energy_denominator":D*D,
            "strict_G_lower":"161/50","strict_square_upper":"321/100",
            "strict_bF_gap":"1/200","corruptions_rejected":4,
            "verification_method":"Independent indexed-tree generation; every current/divergence/energy exact.",
            "limits":"The finite certificate becomes an infinite FREE-FUSF upper bound "
                     "by the manuscript's written finite-flow/exhaustion transfer. "
                     "It does not calculate an exact infinite-square expectation or certify priority."}

def main():
    path = Path(__file__).resolve().with_name("square_flow_certificate.json.gz")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PIN, "exact certificate SHA256")
    result = check(json.loads(gzip.decompress(raw)))
    result["certificate_sha256"] = PIN
    result["claimant_programs_executed"] = False
    return result

if __name__ == "__main__":
    print(json.dumps(main(),sort_keys=True,indent=2))
