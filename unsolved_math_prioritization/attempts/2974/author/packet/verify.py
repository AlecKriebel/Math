#!/usr/bin/env python3
"""Read-only exact checks for the bounded claims in REPORT.md."""
import argparse
from collections import deque
from functools import reduce
import hashlib
import itertools
import json
from math import gcd
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def content(vectors):
    return reduce(gcd, (abs(x) for v in vectors for x in v), 0)


def torus_checks():
    rows = []
    for a, b in ((3, 12), (4, 9)):
        h, base, r = a*b+1, 2*a*b, 6*a*b
        require(r == base+4*h-4, "T4 Euler identity failed")
        rows.append({"a": a, "b": b, "genus": h, "base_points": base,
                     "critical_points": r, "divisibility": gcd(a, b)})
    require([r["genus"] for r in rows] == [37, 37], "Wrong pair genus")
    require([r["base_points"] for r in rows] == [72, 72], "Wrong pair base count")
    require([r["divisibility"] for r in rows] == [3, 1], "Divisibilities must differ")
    primes = [3, 5, 7, 11, 13, 17]
    families = []
    for k in range(1, len(primes)+1):
        pp = primes[:k]
        M = reduce(lambda x, y: x*y, pp, 1)
        divisors = [reduce(lambda x, y: x*y, s, 1)
                    for length in range(1, k+1)
                    for s in itertools.combinations(pp, length)]
        pairs = [(a, M*M//a) for a in divisors]
        require(len(pairs) == 2**k-1, "Family cardinality failed")
        require(len({gcd(a,b) for a,b in pairs}) == len(pairs), "Divisibilities collide")
        for a,b in pairs:
            require(a >= 3 and b >= 3 and a*b == M*M and b % a == 0,
                    "Product-polarization family failed")
            require((M*M) % (gcd(a,b)**2) == 0, "Square-divisor restriction failed")
        families.append({"k": k, "M": M, "genus": M*M+1,
                         "count": len(pairs)})
    alternating = ((0,4,0,0),(-4,0,0,0),(0,0,0,9),(0,0,-9,0))
    d1 = content(alternating)
    pfaffian = (alternating[0][1]*alternating[2][3]
                -alternating[0][2]*alternating[1][3]
                +alternating[0][3]*alternating[1][2])
    require(d1 == 1 and pfaffian == 36, "Product polarization type failed")
    return {"pair": rows, "families": families,
            "degree_4_9_polarization_type":[d1,pfaffian//d1]}


def multiply(a, b, p):
    """(F_p)^2 semidirect C2; involution negates first coordinate."""
    x,y,t = a
    u,v,s = b
    return ((x + (-u if t else u)) % p, (y+v) % p, (t+s) % 2)


def inverse(a, p):
    x,y,t = a
    return ((x if t else -x) % p, -y % p, t)


def subgroup(gens, p):
    unit = (0,0,0)
    moves = list(gens) + [inverse(g,p) for g in gens]
    seen, todo = {unit}, deque([unit])
    while todo:
        a = todo.popleft()
        for b in moves:
            ab = multiply(a,b,p)
            if ab not in seen:
                seen.add(ab)
                todo.append(ab)
    return seen


def conjugate(f, s, p):
    return multiply(multiply(f,s,p),inverse(f,p),p)


def semidirect_checks():
    checks = 0
    summary = []
    for p in (3,5,7,11):
        S = [(0,0,1),(0,1,0)]
        sizes = []
        for n in range(0,2*p+1):
            fn = (n % p,0,0)
            gn = subgroup(S+[conjugate(fn,s,p) for s in S],p)
            kernel = {g for g in gn if g[2] == 0}
            expected = {((2*n*a)%p,b,0) for a in range(p) for b in range(p)}
            require(kernel == expected, "Finite kernel-lattice model failed")
            # Test the exact normal-form factorization used in the proof.
            G0 = subgroup(S,p)
            a_s = [multiply(multiply(multiply(inverse(s,p),fn,p),s,p),inverse(fn,p),p)
                   for s in S]
            D = subgroup([conjugate(g,a,p) for g in G0 for a in a_s],p)
            normal_form = {multiply(d,g,p) for d in D for g in G0 if g[2] == 0}
            require(normal_form == kernel, "D(G0 intersect N) formula failed")
            require(all(multiply(multiply(g,a,p),inverse(g,p),p) in D
                        for g in G0 for a in D), "D not invariant under G0")
            # Adding initial e1 translation erases the n-dependence.
            Sfull = S+[(1,0,0)]
            full = subgroup(Sfull+[conjugate(fn,s,p) for s in Sfull],p)
            require(len({g for g in full if g[2] == 0}) == p*p,
                    "Saturated initial lattice should erase this distinction")
            sizes.append(len(kernel))
            checks += 1
        summary.append({"prime":p,"kernel_sizes":sizes})
    return {"parameter_cases":checks,"models":summary}


def lattice_checks():
    # Content is tested only under matrices with determinant +1 or -1.
    bases = [(1,0,0,1),(1,3,0,1),(0,1,1,0),(-1,0,0,1),(2,1,1,1)]
    cases = 0
    for n in range(0,31):
        vectors = [(2*n,0),(0,6*n),(4*n,8*n)]
        require(content(vectors) == 2*n, "Content scaling failed")
        for a,b,c,d in bases:
            require(abs(a*d-b*c) == 1, "Non-unimodular test matrix")
            image = [(a*x+b*y,c*x+d*y) for x,y in vectors]
            require(content(image) == content(vectors), "Content changed under basis change")
            cases += 1
    return {"unimodular_content_cases":cases,"quotient_content":"2n"}


def topology_checks():
    cp_rows = []
    previous = None
    for d in range(3,101):
        h = (d-1)*(d-2)//2
        base = d*d
        r = 3+base+4*h-4
        require(r == 3*(d-1)**2, "CP2 critical-point formula failed")
        require(2*h-2 == d*d-3*d, "CP2 adjunction failed")
        if previous is not None:
            require(h > previous, "CP2 genera not increasing")
        previous = h
        if d < 8:
            cp_rows.append({"degree":d,"genus":h,"base_points":base,"critical_points":r})
    for q in range(2,101):
        h,e,sigma = 2*q,8-4*q,-4
        r = e+4*h-4
        require(r == 4*q+4 and r+sigma == 4*q > 0,
                "Ruled-gadget defect failed")
    cases = 0
    for e,sigma,min_h in ((3,1,1),(0,0,2),(24,-16,1)):
        for h in range(min_h,12):
            for b in (1,4,9,16):
                ey,sy = e+b,sigma-b
                require(ey+sy == e+sigma, "Blowup invariant failed")
                for d in range(2,8):
                    eyd = d*ey+4*(d-1)*(h-1)
                    syd = d*sy
                    defect = eyd+syd-e-sigma
                    require(defect == (d-1)*(e+sigma+4*h-4) > 0,
                            "Base-change defect failed")
                    for k in (0,1,b,d*b):
                        require((eyd-k)+(syd+k)-e-sigma == defect,
                                "Ordinary blowdowns changed defect")
                    require(-d < -1, "Lifted section is not exceptional")
                    cases += 1
    return {"CP2_sample":cp_rows,"ruled_gadgets_checked":99,
            "base_change_cases":cases}


def check_manifest(path, trusted_hash):
    raw = path.read_bytes()
    require(sha256(raw) == trusted_hash.lower(), "External manifest hash mismatch")
    manifest = json.loads(raw)
    require(manifest.get("schema") == "lefschetz-pencils-2974-freeze-v1", "Wrong manifest schema")
    files = manifest.get("packet_files")
    require(isinstance(files,dict) and files, "Missing packet file inventory")
    root = Path(__file__).resolve().parent
    observed = {}
    for p in root.rglob("*"):
        require(not p.is_symlink(), "Symlinks are forbidden in packet")
        if p.is_file():
            observed[p.relative_to(root).as_posix()] = p
        else:
            require(p.is_dir(), "Nonregular packet item")
    require(set(observed) == set(files), "Packet file inventory mismatch")
    for name,p in observed.items():
        item = files[name]
        data = p.read_bytes()
        require(len(data) == item["bytes"], "File size mismatch: "+name)
        require(sha256(data) == item["sha256"], "File hash mismatch: "+name)
    return {"manifest_sha256":trusted_hash.lower(),"files":len(files),"verified":True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest",type=Path)
    parser.add_argument("--manifest-sha256")
    args = parser.parse_args()
    require(bool(args.manifest) == bool(args.manifest_sha256),
            "Use --manifest and --manifest-sha256 together")
    # Explicitly verify the exception guard is active, including under -O/-OO.
    rejected = False
    try:
        require(False,"sentinel")
    except ValueError:
        rejected = True
    require(rejected,"Runtime guard was disabled")
    result = {"schema":"lefschetz-pencils-2974-checks-v1",
              "problem_status":"unsolved_here",
              "scope":"finite arithmetic and illustrative group models only",
              "torus":torus_checks(),"semidirect":semidirect_checks(),
              "lattice":lattice_checks(),"topology":topology_checks()}
    if args.manifest:
        result["integrity"] = check_manifest(args.manifest,args.manifest_sha256)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("Verification failed: "+str(exc),file=sys.stderr)
        sys.exit(1)
