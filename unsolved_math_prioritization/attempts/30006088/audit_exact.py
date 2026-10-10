#!/usr/bin/env python3
"""Independent finite/combinatorial audit. No source bodies or network required.

Run without --mutant for the positive suite. Named mutations deliberately replace
mathematical semantics; the same checks must reject them under every Python mode.
High-precision formula diagnostics are labeled separately from exact checks.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import argparse
import json
import os
from pathlib import Path
import sys

MUTANTS = {
    "single_missing_fugacity": "lattice",
    "edge_instead_of_vertex_deletion": "lattice",
    "ordered_pair_halved": "lattice",
    "pair_ratio_inverted": "lattice",
    "low_fugacity_sign": "lattice",
    "independent_realizations": "campbell",
    "diagonal_included": "campbell",
    "per_realization_normalization": "campbell",
    "unbiased_palm": "campbell",
    "adjacent_only": "resolvent",
    "identity_generation_included": "resolvent",
    "generation_mark_shifted": "resolvent",
    "modulus_marginals_suffice": "conditional",
    "wrong_dilute_parameter": "symbolic",
    "wrong_kappa4_prefactor": "symbolic",
    "wrong_laplace_scale": "numeric",
    "wrong_ars_generation": "numeric",
    "wrong_ars_sine_factor": "numeric",
    "first_moment_controls_pairs": "ui",
}
MUTANT = None
COUNTS = Counter()


def check(condition, family, message):
    COUNTS[family] += 1
    if not condition:
        raise RuntimeError("CHECK_FAILED[" + family + "]: " + message)


def cycles_dfs(edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    out = set()
    for root in sorted(adj):
        def walk(path):
            for v in adj[path[-1]]:
                if v == root and len(path) >= 3:
                    out.add(frozenset(tuple(sorted(e)) for e in zip(path, path[1:] + [root])))
                elif v > root and v not in path:
                    walk(path + [v])
        walk([root])
    return sorted(out, key=lambda c: sorted(c))


def vset(c):
    return frozenset(v for e in c for v in e)


def direct_edge_configurations(edges):
    """Independent oracle: connected components of degree-0/2 edge sets."""
    configs = []
    for mask in range(1 << len(edges)):
        selected = frozenset(e for j, e in enumerate(edges) if (mask >> j) & 1)
        degrees = Counter(v for e in selected for v in e)
        if any(d != 2 for d in degrees.values()):
            continue
        remaining = set(selected)
        components = []
        while remaining:
            todo = [remaining.pop()]
            component = set(todo)
            vertices = set(todo[0])
            while todo:
                todo.pop()
                added = {e for e in remaining if vertices.intersection(e)}
                if added:
                    component.update(added)
                    remaining.difference_update(added)
                    vertices.update(v for e in added for v in e)
                    todo.extend(added)
            components.append(frozenset(component))
        configs.append(tuple(components))
    return configs


def test_graph(name, edges, detailed=True):
    edges = sorted({tuple(sorted(e)) for e in edges})
    cycles = cycles_dfs(edges)
    configs = direct_edge_configurations(edges)
    check(set(cycles) == {c for conf in configs for c in conf}, "lattice", name + " independent cycle enumerators")
    vs = {c: vset(c) for c in cycles}
    allv = frozenset(v for e in edges for v in e)
    totals = Counter((len(conf), sum(map(len, conf))) for conf in configs)
    by_single = {c: Counter() for c in cycles}
    by_pair = {}
    for conf in configs:
        powers = (len(conf), sum(map(len, conf)))
        for c in conf:
            by_single[c][powers] += 1
        for c, d in combinations(conf, 2):
            by_pair.setdefault(frozenset((c, d)), Counter())[powers] += 1
    for n, x in ((F(2, 5), F(3, 7)), (F(7, 3), F(5, 4))):
        def evaluate(poly):
            return sum((coeff * n**a * x**b for (a, b), coeff in poly.items()), F(0))
        @lru_cache(None)
        def rec(allowed):
            if not allowed:
                return F(1)
            v = min(allowed)
            # Either v is empty, or it belongs to its unique occupied cycle.
            return rec(allowed - {v}) + sum((n*x**len(c)*rec(allowed-vs[c]) for c in cycles if v in vs[c] and vs[c] <= allowed), F(0))
        z = evaluate(totals)
        check(rec(allv) == z, "lattice", name + " independent partition recurrence")
        singles = {}
        for c in cycles:
            deleted = rec(allv-vs[c])
            if MUTANT == "edge_instead_of_vertex_deletion":
                deleted = sum((n**len(conf)*x**sum(map(len,conf)) for conf in configs if all(not(c & d) for d in conf)), F(0))
            formula = (F(1) if MUTANT == "single_missing_fugacity" else n)*x**len(c)*deleted/z
            direct = evaluate(by_single[c])/z
            check(formula == direct, "lattice", name + " marked single")
            singles[c] = direct
        for c, d in combinations(cycles, 2):
            direct = evaluate(by_pair.get(frozenset((c, d)), {}))/z
            if vs[c] & vs[d]:
                check(direct == 0, "lattice", name + " exclusion")
                continue
            marked = n*n*x**(len(c)+len(d))*rec(allv-vs[c]-vs[d])/z
            if MUTANT == "ordered_pair_halved":
                marked /= 2
            check(direct == marked, "lattice", name + " ordered distinct pair")
            ratio = z*rec(allv-vs[c]-vs[d])/(rec(allv-vs[c])*rec(allv-vs[d]))
            if MUTANT == "pair_ratio_inverted":
                ratio = 1/ratio
            check(direct == ratio*singles[c]*singles[d], "lattice", name + " pair ratio")
            def linear(allowed):
                return sum((x**len(a) for a in cycles if vs[a] <= allowed), F(0))
            coeff = linear(allv)+linear(allv-vs[c]-vs[d])-linear(allv-vs[c])-linear(allv-vs[d])
            if MUTANT == "low_fugacity_sign":
                coeff = -coeff
            both = sum((x**len(a) for a in cycles if vs[a]&vs[c] and vs[a]&vs[d]), F(0))
            check(coeff == both, "lattice", name + " fugacity coefficient")
    return {"name": name, "vertices": len(allv), "edges": len(edges), "cycles": len(cycles), "configurations": len(configs)}


def lattice():
    triangle_pair = [(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4)]
    bowtie = [(0,1),(1,2),(0,2),(0,3),(3,4),(0,4)]
    graphs = [("linked_triangles",triangle_pair),("bowtie",bowtie)]
    if MUTANT is None:
        for v in range(5):
            possible = list(combinations(range(v),2))
            for mask in range(1 << len(possible)):
                graphs.append(("labeled_"+str(v)+"_"+str(mask), [e for i,e in enumerate(possible) if (mask>>i)&1]))
        graphs.extend([
            ("K5",list(combinations(range(5),2))),
            ("K6",list(combinations(range(6),2))),
            ("cube",[(v,v^(1<<b)) for v in range(8) for b in range(3) if v < (v^(1<<b))]),
            ("three_bridged_triangles",[(3*j+i,3*j+(i+1)%3) for j in range(3) for i in range(3)]+[(2,3),(5,6)]),
        ])
    return [test_graph(name,edges) for name,edges in graphs]


def campbell():
    laws = [(frozenset(),F(1,4)),(frozenset("a"),F(1,4)),(frozenset("abc"),F(1,2))]
    nu = {a:sum((p for conf,p in laws if a in conf),F(0)) for a in "abc"}
    for a in "abc":
        for b in "abc":
            direct = sum((p for conf,p in laws if a in conf and b in conf and a != b),F(0))
            palm = sum((p/nu[a] for conf,p in laws if a in conf and b in conf and a != b),F(0))
            candidate = nu[a]*palm
            if MUTANT == "independent_realizations":
                candidate = nu[a]*nu[b]
            elif MUTANT == "diagonal_included":
                candidate = sum((p for conf,p in laws if a in conf and b in conf),F(0))
            elif MUTANT == "unbiased_palm":
                candidate = nu[a]*sum((p for conf,p in laws if b in conf and a != b),F(0))
            elif MUTANT == "per_realization_normalization":
                candidate = sum((p/(len(conf)*(len(conf)-1)) for conf,p in laws if a != b and a in conf and b in conf),F(0))
            check(candidate == direct,"campbell","same-configuration Campbell/Palm at "+a+b)
    check(sum((p*len(c)*(len(c)-1) for c,p in laws),F(0)) == 3,"campbell","factorial mass")


def resolvent():
    import sympy as s
    q = s.Matrix([[s.Rational(1,3),s.Rational(1,6)],[s.Rational(1,5),s.Rational(1,4)]])
    identity = s.eye(2)
    for z in (s.Rational(0),s.Rational(1,2),s.Rational(1)):
        result = q*(identity-z*q).inv()
        if MUTANT == "adjacent_only":
            result = q
        elif MUTANT == "identity_generation_included":
            result = (identity-z*q).inv()
        elif MUTANT == "generation_mark_shifted":
            result = z*q*(identity-z*q).inv()
        check(result-q-z*q*result == s.zeros(2),"resolvent","R=Q+zQR")
        finite = sum((z**(j-1)*q**j for j in range(1,9)),s.zeros(2))
        tail = z**8*q**9*(identity-z*q).inv()
        check(result == finite+tail,"resolvent","exact finite sum plus tail")


def conditional():
    # Two embedded-shape states at each modulus. Equal modulus laws do not
    # imply a modulus-only Radon-Nikodym derivative.
    mu = [F(1,4)]*4
    good = [F(1,8),F(1,8),F(3,8),F(3,8)]
    bad = [F(3,8),F(1,8),F(1,8),F(3,8)]
    for law, expected in ((good,True),(bad,False)):
        ratios = [law[i]/mu[i] for i in range(4)]
        is_modulus_density = ratios[0] == ratios[1] and ratios[2] == ratios[3]
        if MUTANT == "modulus_marginals_suffice":
            is_modulus_density = all(sum(law[i:i+2]) > 0 for i in (0,2))
        check(is_modulus_density == expected,"conditional","embedded-shape conditional law")
        marg = [sum(law[i:i+2]) for i in (0,2)]
        conditionals_agree = all(law[i]/marg[i//2] == F(1,2) for i in range(4))
        check(conditionals_agree == expected,"conditional","disintegration converse")
    # Four exact boundary points certify that z+z²/4 does not map S¹ to a circle.
    import sympy as s
    eps=s.Rational(1,4)
    points=[(1+eps,0),(-1+eps,0),(-eps,1),(-eps,-1)]
    matrix=s.Matrix([[x*x+y*y,x,y,1] for x,y in points])
    check(matrix.det() != 0,"conditional","four nonconcyclic image points")
    check(2*eps < 1,"conditional","injectivity bound")


def symbolic():
    import sympy as s
    k=s.symbols("k",positive=True)
    charge=(6-k)*(3*k-8)/(2*k)
    check(s.simplify(charge-(1-6*(1-4/k)**2/(4/k))) == 0,"symbolic","central charge")
    dilute=2*s.cos(s.pi*(1-(k/4 if MUTANT == "wrong_dilute_parameter" else 4/k)))
    check(s.simplify(dilute.subs(k,3)) == 1,"symbolic","n=1 at kappa=3")
    for kval in (s.Rational(8,3),s.Rational(3),s.Rational(4)):
        check(s.simplify((3*k/32+2/k-1)-(k*(4/k-1)**2/8-k/32)) == 0,"symbolic","ARS threshold algebra")
        check((3*k/32+2/k-1).subs(k,kval) <= 0,"symbolic","positive lambda in theorem range")
    pref=s.limit((4/k-1)/s.sin(s.pi*(1-k/4)),k,4)
    if MUTANT == "wrong_kappa4_prefactor":
        pref *= s.pi
    check(pref == 1/s.pi,"symbolic","kappa4 removable prefactor")
    r,z,H=s.symbols("r z H")
    check(s.simplify(H*r/(1-z*r)-H*r-z*r*(H*r/(1-z*r))) == 0,"symbolic","scalar renewal identity")
    u=s.symbols("u",positive=True)
    check(s.simplify(s.sin(s.I*u)/(s.I*u)/(s.cos(s.I*u)-1)-s.sinh(u)/(u*(s.cosh(u)-1))) == 0,"symbolic","kappa4 resolvent")


def numeric():
    import mpmath as m
    m.mp.dps=70
    def source(k,lam,j):
        a=4/k-1
        s=m.sqrt(a*a-8*lam/k)
        quotient=k*m.pi/4 if abs(s)<m.mpf("1e-60") else m.sin(k*m.pi*s/4)/s
        return a*m.cos(m.pi*a)**j/m.sin(m.pi*(1-k/4))*quotient/m.cos(m.pi*s)**j
    def report(k,lam,j):
        if MUTANT == "wrong_laplace_scale":
            lam /= 2*m.pi
        a=4/k-1
        s=m.sqrt(a*a-8*lam/k)
        quotient=k*m.pi/4 if abs(s)<m.mpf("1e-60") else m.sin(k*m.pi*s/4)/s
        H=a*quotient/m.sin(m.pi*(1-k/4))
        if MUTANT == "wrong_ars_sine_factor":
            H=a*(m.pi if abs(s)<m.mpf("1e-60") else m.sin(m.pi*s)/s)/m.sin(m.pi*(1-k/4))
        r=m.cos(m.pi*a)/m.cos(m.pi*s)
        return H*r**(j-1 if MUTANT == "wrong_ars_generation" else j),H,r
    rows=[]
    for k in map(m.mpf,("2.7","3","3.5","3.99")):
        threshold=k*(4/k-1)**2/8
        for lam in (threshold/2,threshold,m.mpf("0.1"),m.mpf("2")):
            for j in (1,2,5):
                value,H,r=report(k,lam,j)
                check(abs(value-source(k,lam,j))<m.mpf("1e-60"),"numeric","independent source transcription")
                check(abs(m.im(value))<m.mpf("1e-60") and 0<m.re(value)<1,"numeric","positive probability transform")
                check(abs(m.im(r))<m.mpf("1e-60") and 0<m.re(r)<1,"numeric","strict geometric convergence")
                for z in (m.mpf(0),m.mpf("0.4"),m.mpf(1)):
                    finite=m.fsum(z**(l-1)*source(k,lam,l) for l in range(1,31))
                    tail=H*r*(z*r)**30/(1-z*r)
                    check(abs(H*r/(1-z*r)-finite-tail)<m.mpf("1e-55"),"numeric","geometric sum with explicit tail")
            rows.append({"kappa":str(k),"lambda":str(lam),"j1_transform":str(m.re(source(k,lam,1)))})
    for lam in map(m.mpf,("0.01","0.3","2")):
        u=m.pi*m.sqrt(2*lam)
        k=4-m.mpf("1e-30")
        for j in (1,2,5):
            endpoint=m.sinh(u)/(u*m.cosh(u)**j)
            check(abs(source(k,lam,j)-endpoint)<m.mpf("1e-27"),"numeric","kappa4 continuous endpoint")
    return rows


def ui():
    for m in range(2,101):
        p=F(1,m*m)
        first=p*m
        factorial=p*m*(m-1)
        candidate=first*first if MUTANT == "first_moment_controls_pairs" else factorial
        check(first == F(1,m),"ui","vanishing first intensity")
        check(candidate == F(m-1,m),"ui","nonvanishing pair intensity")
        # Exact tail defeats uniform integrability at any threshold below m(m-1).
        check(factorial >= F(1,2),"ui","factorial moment tail")
    check(sum((F(1,m*m) for m in range(2,101)),F(0))<1,"ui","summable rare events, finite partial check")


def readonly_probe():
    check(os.geteuid()!=0,"environment","must run as actual nonroot")
    path=Path(__file__).resolve().parent/"audit_write_probe.tmp"
    try:
        with path.open("x") as handle:
            handle.write("unexpected write")
    except PermissionError:
        return {"effective_uid":os.geteuid(),"directory_write_denied":True}
    else:
        path.unlink()
        raise RuntimeError("CHECK_FAILED[environment]: audit directory is writable")


def main():
    global MUTANT
    parser=argparse.ArgumentParser()
    parser.add_argument("--mutant",choices=sorted(MUTANTS))
    parser.add_argument("--require-readonly",action="store_true")
    args=parser.parse_args()
    MUTANT=args.mutant
    environment=readonly_probe() if args.require_readonly else {"effective_uid":os.geteuid()}
    outputs={}
    for family,func in (("lattice",lattice),("campbell",campbell),("resolvent",resolvent),("conditional",conditional),("symbolic",symbolic),("numeric",numeric),("ui",ui)):
        if MUTANT is None or MUTANTS[MUTANT]==family:
            outputs[family]=func()
    print(json.dumps({"status":"PASS","mutant":MUTANT,"environment":environment,"counts":dict(COUNTS),"outputs":outputs,"continuum_theorem_proved":False},indent=2))


if __name__ == "__main__":
    main()
