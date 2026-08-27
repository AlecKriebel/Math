#!/usr/bin/env python3
"""Independent exact spot checks of representative four-port obstructions.

The compiler below starts from the literal rooted graphs in the frozen orbit
lock and implements the article's switching formula.  It does not import the
atlas compiler or its verifier.  It checks three quartic separators and two
families of directed-rank obstructions, including the H21 saturation factors.
This is representative evidence, not an independent enumeration of all 14
orbits.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import permutations, product
import json
from pathlib import Path
import random


ART = Path("../package_copy/proof_package/input_frozen/k3p_cloud_artifacts")
CH4 = tuple(p + (p[0] ^ p[1] ^ p[2],) for p in product(range(4), repeat=3))
CH3 = tuple(p + (p[0] ^ p[1],) for p in product(range(4), repeat=2))


@dataclass(frozen=True)
class Descriptor:
    edge_count: int
    retic_count: int
    outputs: tuple
    signatures: tuple


class Graph:
    def __init__(self, literal):
        self.nodes = {x["id"]: x for x in literal["nodes"]}
        self.arcs = tuple(sorted((x["tail"], x["head"]) for x in literal["arcs"]))
        self.inc = defaultdict(list)
        for u, v in self.arcs:
            self.inc[v].append(u)


def descendants(graph, kept):
    children = defaultdict(list)
    for u, v in kept:
        children[u].append(v)
    memo = {}

    def visit(v):
        if v in memo:
            return memo[v]
        label = graph.nodes[v].get("label")
        mask = (1 << label) if isinstance(label, int) else 0
        for w in children[v]:
            mask |= visit(w)
        memo[v] = mask
        return mask

    for node in graph.nodes:
        visit(node)
    return {e: memo[e[1]] for e in kept}


def sector(mask, chars):
    out = 0
    i = 0
    while mask:
        if mask & 1:
            out ^= chars[i]
        i += 1
        mask >>= 1
    return out


def inheritance_expansion(bits):
    out = {0: 1}
    for j, selected_second_parent in enumerate(bits):
        nxt = defaultdict(int)
        for mask, coefficient in out.items():
            if selected_second_parent:
                nxt[mask | (1 << j)] += coefficient
            else:
                nxt[mask] += coefficient
                nxt[mask | (1 << j)] -= coefficient
        out = {m: c for m, c in nxt.items() if c}
    return tuple(sorted(out.items()))


def compile_variant(graph, retics, parent_orders):
    selected_arms = {
        e for e in graph.arcs
        if graph.nodes[e[1]]["role"] == "leaf" and isinstance(graph.nodes[e[1]].get("label"), int)
    }
    switchings = []
    for bits in product((0, 1), repeat=len(retics)):
        removed = set()
        for j, r in enumerate(retics):
            keep = parent_orders[j][bits[j]]
            removed.update((p, r) for p in graph.inc[r] if p != keep)
        kept = tuple(e for e in graph.arcs if e not in removed)
        switchings.append((bits, kept, descendants(graph, kept)))

    raw_signatures, internal = [], []
    for edge in graph.arcs:
        if edge in selected_arms:
            continue
        signature = []
        for _, kept, masks in switchings:
            if edge not in masks:
                signature.extend((0,) * len(CH4))
            else:
                signature.extend(sector(masks[edge], chars) for chars in CH4)
        if any(signature):
            internal.append(edge)
            raw_signatures.append(tuple(signature))
    signatures = tuple(sorted(set(raw_signatures)))
    class_of = {s: i for i, s in enumerate(signatures)}
    edge_class = {e: class_of[s] for e, s in zip(internal, raw_signatures)}

    outputs = []
    n = 3 * len(signatures) + len(retics)
    for chars in CH4:
        poly = defaultdict(Q)
        for bits, kept, masks in switchings:
            exponent = [0] * n
            for edge in kept:
                if edge not in edge_class:
                    continue
                h = sector(masks[edge], chars)
                if h:
                    exponent[3 * edge_class[edge] + h - 1] += 1
            for mask, coefficient in inheritance_expansion(bits):
                term = exponent.copy()
                for j in range(len(retics)):
                    if (mask >> j) & 1:
                        term[3 * len(signatures) + j] += 1
                poly[tuple(term)] += coefficient
        outputs.append(tuple(sorted((e, c) for e, c in poly.items() if c)))
    return Descriptor(len(signatures), len(retics), tuple(outputs), signatures)


def compile_graph(literal):
    graph = Graph(literal)
    retic_set = tuple(sorted(n for n, d in graph.nodes.items() if d["role"] == "retic"))
    variants = []
    for retics in permutations(retic_set):
        pairs = [tuple(sorted(graph.inc[r])) for r in retics]
        for flips in product((0, 1), repeat=len(retics)):
            orders = tuple((pair[f], pair[1-f]) for pair, f in zip(pairs, flips))
            variants.append(compile_variant(graph, retics, orders))
    return min(variants, key=lambda d: (d.retic_count, d.edge_count, d.outputs, d.signatures))


def all_parameter_conventions(literal):
    """All harmless reticulation-variable order/complement conventions."""
    graph = Graph(literal)
    retic_set = tuple(sorted(n for n, d in graph.nodes.items() if d["role"] == "retic"))
    variants = []
    for retics in permutations(retic_set):
        pairs = [tuple(sorted(graph.inc[r])) for r in retics]
        for flips in product((0, 1), repeat=len(retics)):
            orders = tuple((pair[f], pair[1-f]) for pair, f in zip(pairs, flips))
            variants.append(compile_variant(graph, retics, orders))
    return variants


def poly_dict(output):
    return dict(output)


def add(*terms):
    out = defaultdict(Q)
    for coefficient, poly in terms:
        for exponent, value in poly.items():
            out[exponent] += Q(coefficient) * value
    return {e: c for e, c in out.items() if c}


def mul(*polys):
    if not polys:
        return {(): Q(1)}
    out = polys[0]
    for right in polys[1:]:
        nxt = defaultdict(Q)
        for e, c in out.items():
            for f, d in right.items():
                nxt[tuple(x+y for x, y in zip(e, f))] += c*d
        out = {e: c for e, c in nxt.items() if c}
    return out


def variable(n, i):
    return {tuple(int(j == i) for j in range(n)): Q(1)}


def one(n):
    return {(0,) * n: Q(1)}


def quartic_pullback(desc, terms):
    outputs = [poly_dict(x) for x in desc.outputs]
    return add(*[(coefficient, mul(*(outputs[i] for i in indices)))
                 for coefficient, indices in terms])


def evaluate(poly, point):
    out = Q(0)
    for exponent, coefficient in poly.items():
        term = coefficient
        for x, power in zip(point, exponent):
            if power:
                term *= x ** power
        out += term
    return out


def jacobian_at(desc, rows, point):
    matrix = []
    for oi in rows:
        row = []
        for j in range(len(point)):
            value = Q(0)
            for exponent, coefficient in desc.outputs[oi]:
                if not exponent[j]:
                    continue
                term = coefficient * exponent[j]
                for k, power in enumerate(exponent):
                    adjusted = power - int(k == j)
                    if adjusted:
                        term *= point[k] ** adjusted
                value += term
            row.append(value)
        matrix.append(row)
    return matrix


def rref_rank_and_pivots(matrix):
    a = [list(row) for row in matrix]
    rows, cols = len(a), len(a[0])
    pivots = []
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        v = a[r][c]
        a[r] = [x/v for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [x-f*y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return r, pivots


def independent_minor(matrix):
    rank, columns = rref_rank_and_pivots(matrix)
    narrowed = [[row[j] for j in columns[:rank]] for row in matrix]
    _, rows = rref_rank_and_pivots([list(x) for x in zip(*narrowed)])
    rows = rows[:rank]
    square = [[matrix[i][j] for j in columns[:rank]] for i in rows]
    det = determinant(square)
    assert det
    return rank, rows, columns[:rank], det


def determinant(matrix):
    a = [list(row) for row in matrix]
    ans = Q(1)
    for c in range(len(a)):
        p = next((i for i in range(c, len(a)) if a[i][c]), None)
        if p is None:
            return Q(0)
        if p != c:
            a[c], a[p] = a[p], a[c]
            ans = -ans
        v = a[c][c]
        ans *= v
        for i in range(c+1, len(a)):
            if a[i][c]:
                f = a[i][c]/v
                for j in range(c+1, len(a)):
                    a[i][j] -= f*a[c][j]
    return ans


def ct_margin(triple):
    c, g, t = triple
    return min(c, g, t, 1-c, 1-g, 1-t,
               1+c-g-t, 1-c+g-t, 1-c-g+t,
               c-g*t, g-c*t, t-c*g)


def own_point(desc, seed):
    rng = random.Random(seed)
    point, margins = [], []
    for _ in range(desc.edge_count):
        while True:
            den = rng.choice((17, 19, 23, 29, 31))
            triple = tuple(Q(rng.randint(4, den-4), den) for _ in range(3))
            m = ct_margin(triple)
            if m > 0:
                point.extend(triple)
                margins.append(m)
                break
    for _ in range(desc.retic_count):
        den = rng.choice((11, 13, 17))
        x = Q(rng.randint(2, den-2), den)
        point.append(x)
        margins.append(min(x, 1-x))
    return point, min(margins)


QHA = ((1,(0,24,44,52)),(-1,(0,28,36,56)),(-1,(4,24,32,60)),(1,(4,28,40,48)),
       (1,(8,16,36,60)),(-1,(8,20,44,48)),(-1,(12,16,40,52)),(1,(12,20,32,56)))
Q20 = ((1,(0,10,35,61)),(-1,(0,11,34,61)),(1,(0,14,41,51)),(-1,(0,15,41,50)),
       (-1,(1,10,35,60)),(1,(1,11,34,60)),(-1,(1,14,40,51)),(1,(1,15,40,50)))
Q23 = ((1,(0,8,45,53)),(1,(0,9,37,60)),(-1,(0,12,37,57)),(-1,(0,13,40,53)),
       (-1,(5,8,45,48)),(-1,(5,9,32,60)),(1,(5,12,32,57)),(1,(5,13,40,48)))


def verify_h21_factorization(desc):
    n = 3*desc.edge_count + desc.retic_count
    assert (desc.edge_count, desc.retic_count) == (8, 2)
    out = [poly_dict(x) for x in desc.outputs]
    E = [[variable(n, 3*i+s) for s in range(3)] for i in range(8)]
    l0, l1 = variable(n, 24), variable(n, 25)
    m0, m1 = add((1,one(n)),(-1,l0)), add((1,one(n)),(-1,l1))
    a,b,c,d,f,h,i,j = [E[x][2] for x in range(8)]
    U,V,Z,D,I0 = mul(a,l0),mul(j,m0),mul(c,d,i),mul(d,i),i
    A0,B0 = mul(h,b,l1),mul(h,f,m1)
    A,B = mul(E[2][0],E[3][0],E[6][0]),mul(E[2][1],E[3][1],E[6][1])
    e2C,e2G = E[2][0],E[2][1]
    rhs3=mul(V,add((1,mul(D,A0)),(1,mul(I0,I0,B0))))
    rhs12=mul(U,add((1,mul(D,A0)),(1,B0)))
    rhs51=mul(Z,add((1,A0),(1,mul(D,B0))))
    rhs63=mul(V,Z,add((1,mul(I0,I0,A0)),(1,mul(D,B0))))
    identities = (
        add((1,mul(I0,out[3])),(-1,mul(I0,U)),(-1,rhs3)),
        add((1,out[12]),(-1,rhs12),(-1,mul(V,I0))),
        add((1,out[15]),(-1,mul(D,A0)),(-1,B0)),
        add((1,out[20]),(-1,A)),
        add((1,mul(e2G,out[27])),(-1,mul(e2G,B0,A)),(-1,mul(A0,e2C,B))),
        add((1,mul(e2C,out[39])),(-1,mul(e2C,B0,B)),(-1,mul(A0,e2G,A))),
        add((1,out[40]),(-1,B)),
        add((1,mul(I0,out[48])),(-1,mul(I0,U,out[51])),(-1,mul(V,Z))),
        add((1,mul(D,out[51])),(-1,rhs51)),
        add((1,out[60]),(-1,Z)),
        add((1,mul(D,I0,out[63])),(-1,mul(D,I0,U,Z)),(-1,rhs63)),
    )
    assert all(not x for x in identities)
    return {
        "identity_count": len(identities),
        "rational_generators": ["U","V","Z","D","I","A0","B0","A","B","rho=e2C/e2G"],
        "divisors": ["e2C","e2G","D=d*i","I=i"],
        "saturation_sound_on_strict_Dplus": True,
    }


def compress_for_omitted_port(desc, omitted):
    rows = [i for i, chars in enumerate(CH4) if chars[omitted] == 0]
    occurrences = {}
    for ci in range(desc.edge_count):
        sig = []
        for oi in rows:
            for exponent, _ in desc.outputs[oi]:
                sig.extend(exponent[3*ci:3*ci+3])
        occurrences[ci] = tuple(sig)
    groups = defaultdict(list)
    for ci, sig in occurrences.items():
        groups[sig].append(ci)
    active = sorted((x for sig,x in groups.items() if any(sig)), key=min)
    invisible = [x for sig,x in groups.items() if not any(sig)]
    assert len(active) == 4
    retics = [j for j in range(desc.retic_count)
              if any(any(e[3*desc.edge_count+j] for e,_ in desc.outputs[oi]) for oi in rows)]
    assert len(retics) == 1
    compressed=[]
    for oi in rows:
        poly=defaultdict(Q)
        for exponent, coefficient in desc.outputs[oi]:
            new=[0]*13
            for ai,group in enumerate(active):
                vals=[exponent[3*ci:3*ci+3] for ci in group]
                assert all(x==vals[0] for x in vals)
                new[3*ai:3*ai+3]=vals[0]
            new[12]=exponent[3*desc.edge_count+retics[0]]
            poly[tuple(new)]+=coefficient
        compressed.append({e:c for e,c in poly.items() if c})
    return compressed,rows,active,invisible,retics[0]


def canonical_sunlet(edge_map, flip, port_perm):
    n=13; E=[[variable(n,3*i+s) for s in range(3)] for i in range(4)]
    lam=variable(n,12); m=add((1,one(n)),(-1,lam))
    ea,eb,U,V=[E[i] for i in edge_map]
    A=[mul(m if flip else lam,ea[s]) for s in range(3)]
    B=[mul(lam if flip else m,eb[s]) for s in range(3)]
    ans=[]; deps=[]
    for x,y,z in CH3:
        if x==y==z==0: p=one(n); dep=set()
        elif x==0: p=add((1,A[y-1]),(1,mul(V[y-1],B[y-1]))); dep={('A',y),('V',y),('B',y)}
        elif y==0: p=mul(U[x-1],add((1,mul(V[x-1],A[x-1])),(1,B[x-1]))); dep={('U',x),('V',x),('A',x),('B',x)}
        elif z==0: p=mul(U[x-1],V[x-1]); dep={('U',x),('V',x)}
        else: p=mul(U[x-1],add((1,mul(V[x-1],A[z-1])),(1,mul(V[y-1],B[z-1])))); dep={('U',x),('V',x),('A',z),('V',y),('B',z)}
        ans.append(p);deps.append(dep)
    index={x:i for i,x in enumerate(CH3)}
    transport=[index[tuple(chars[port_perm[i]] for i in range(3))] for chars in CH3]
    return [ans[i] for i in transport],[deps[i] for i in transport]


def verify_sunlet_upper(desc, omitted, selected_rows):
    comp,rows,active,invisible,retic=compress_for_omitted_port(desc,omitted)
    found=None
    for edge_map in permutations(range(4)):
        for flip in (False,True):
            for port_perm in permutations(range(3)):
                candidate,deps=canonical_sunlet(edge_map,flip,port_perm)
                if comp==candidate:
                    found=(edge_map,flip,port_perm,deps);break
            if found:break
        if found:break
    assert found
    row_index={r:i for i,r in enumerate(rows)}
    used=set().union(*(found[3][row_index[r]] for r in selected_rows))
    return {"omitted_port":omitted,"generator_count":len(used),"generators":sorted(map(str,used)),
            "active_edge_groups":active,"invisible_edge_groups":invisible,"inheritance_index":retic}


def main():
    lock=json.loads((ART/"K3P_14_ORBIT_LOCK.json").read_text())
    records={r["orbit_id"]:r for r in lock["records"]}
    desc={}
    for oid in {"H21-01","H21-02","L20-01","L20-02","L21a-02","L23-02"}:
        r=records[oid]
        desc[(oid,"source")]=compile_graph(r["source_literal_graph"])
        desc[(oid,"target")]=compile_graph(r["target_literal_graph"])

    separators=[]
    for seed,(oid,body) in enumerate((("H21-01",QHA),("L20-01",Q20),("L23-02",Q23)),1001):
        ps=quartic_pullback(desc[(oid,"source")],body)
        pt=quartic_pullback(desc[(oid,"target")],body)
        assert ps and not pt
        point,margin=own_point(desc[(oid,"source")],seed)
        value=evaluate(ps,point)
        assert value
        separators.append({"orbit":oid,"source_terms":len(ps),"target_terms":len(pt),
                           "own_strict_CT_margin":str(margin),"own_source_value":str(value)})

    rank_rows={
        "H21-02":[3,12,15,20,27,39,40,48,51,60,63],
        "L20-02":[5,10,15,17,20,27,30,34,39,40,45,51,54,57,60],
        "L21a-02":[5,15,17,20,27,39,40,45,51,57,60],
    }
    rank=[]
    for seed,oid in enumerate(rank_rows,2001):
        rows=rank_rows[oid]
        item={"orbit":oid,"rows":rows}
        for side in ("source","target"):
            D=desc[(oid,side)] if (oid,side) in desc else compile_graph(records[oid][f"{side}_literal_graph"])
            point,margin=own_point(D,seed+(0 if side=="source" else 100))
            J=jacobian_at(D,rows,point)
            r,pivot_rows,piv,det=independent_minor(J)
            item[side]={"sample_rank":r,"pivot_rows_within_selected_order":pivot_rows,
                        "pivot_columns":piv,"pivot_determinant":str(det),"margin":str(margin)}
        rank.append(item)
    assert rank[0]["source"]["sample_rank"]==11 and rank[0]["target"]["sample_rank"]==10
    assert rank[1]["source"]["sample_rank"]>=14 and rank[1]["target"]["sample_rank"]<=12
    assert rank[2]["source"]["sample_rank"]==11 and rank[2]["target"]["sample_rank"]==10

    # The ten-generator formulas use a particular ordering and complementation
    # of the two inheritance variables.  Search all eight equivalent literal
    # conventions instead of trusting the package's canonical choice.
    h21=None
    for candidate in all_parameter_conventions(records["H21-02"]["target_literal_graph"]):
        try:
            h21=verify_h21_factorization(candidate)
            break
        except AssertionError:
            pass
    assert h21 is not None
    sunlet20=verify_sunlet_upper(desc[("L20-02","target")],3,rank_rows["L20-02"])
    sunlet21=verify_sunlet_upper(desc[("L21a-02","target")],3,rank_rows["L21a-02"])
    assert sunlet20["generator_count"]==12 and sunlet21["generator_count"]==10

    result={
        "accounting_spot_check":{"canonical_records":len(lock["records"]),
            "raw_member_sum":sum(len(r["raw_members"]) for r in lock["records"]),
            "unique_orbit_ids":len(set(records)),"claimed_prelock_count":len(lock["prelock_exact_separations"])},
        "quartic_separators":separators,
        "directed_rank_samples":rank,
        "H21_exact_rational_factorization":h21,
        "sunlet_factorizations":{"L20-02":sunlet20,"L21a-02":sunlet21},
        "limitations":"Three quartic and three rank orbits were checked. Orbit completeness and all raw mixed-graph double cosets were not independently regenerated here. Sample target ranks alone are not upper bounds; the exact 10-generator H21 and 12/10-generator sunlet factorizations supply those upper bounds."
    }
    Path("four_port_spot_results.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
