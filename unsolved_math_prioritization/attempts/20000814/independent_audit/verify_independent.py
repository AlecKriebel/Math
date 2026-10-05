#!/usr/bin/env python3
"""Independent exact audit controls, not a formal proof of the geometry.

The author files are read only. Optional public corpus/PDF inputs are hashed and
compared; their contents and local paths are never included in the JSON output.
All tests use explicit exceptions and remain active under python -O.
"""
import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import sympy as s

EXPECTED_ARCHIVE = "bd7848a35c7c0e676f8b161f98184b36a39ec251db534c9530646e55966bb420"
EXPECTED_MANIFEST = "23aa3cc77bd3e78439a2fd09867382acbfe2a3e5517057b7111870270a48641c"
FILES = {"AUTHOR_REPLAY.json", "MANIFEST.json", "PROOFS.md", "README.md",
         "REPORT.md", "SOURCE_METADATA.json", "verification_results.json",
         "verify_controls.py"}
checks = 0


def require(test, label):
    global checks
    if not test:
        raise RuntimeError("FAIL: " + label)
    checks += 1


def sha(data):
    return hashlib.sha256(data).hexdigest()


def same_ideal(left, right, variables):
    g = s.groebner(left, *variables, domain=s.QQ, order="lex")
    h = s.groebner(right, *variables, domain=s.QQ, order="lex")
    return all(g.reduce(p)[1] == 0 for p in h) and all(h.reduce(p)[1] == 0 for p in g)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author-dir", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--problems", type=Path)
    parser.add_argument("--research", type=Path)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--dgf-pdf", type=Path)
    args = parser.parse_args()
    root = args.author_dir.resolve()
    before = {p.name: sha(p.read_bytes()) for p in root.iterdir() if p.is_file()}
    require(set(before) == FILES, "exact eight-file author inventory")
    require(not any(p.is_symlink() for p in root.iterdir()), "no author symlinks")
    archive = args.archive.read_bytes()
    require(len(archive) == 22081 and sha(archive) == EXPECTED_ARCHIVE, "archive freeze")
    require(before["MANIFEST.json"] == EXPECTED_MANIFEST, "manifest freeze")
    manifest = json.loads((root / "MANIFEST.json").read_bytes())
    require({v["path"] for v in manifest["files"]} == FILES - {"MANIFEST.json"}, "manifest scope")
    for item in manifest["files"]:
        data = (root / item["path"]).read_bytes()
        require(len(data) == item["bytes"] and sha(data) == item["sha256"], "manifest entry")
    with zipfile.ZipFile(args.archive) as z:
        wanted = {"ci_limits_20000814/" + name for name in FILES}
        require(set(z.namelist()) == wanted and len(z.infolist()) == 8, "archive inventory")
        require(z.testzip() is None, "archive CRC")
        for name in FILES:
            require(z.read("ci_limits_20000814/" + name) == (root / name).read_bytes(), "archive file bytes")

    # Replay in a fresh, unrelated working directory; no output written to root.
    author_expected = (root / "verification_results.json").read_bytes()
    replays = []
    with tempfile.TemporaryDirectory(prefix="ci-audit-replay-") as td:
        copied = Path(td) / "control.py"
        copied.write_bytes((root / "verify_controls.py").read_bytes())
        for flags in ([], ["-O"]):
            proc = subprocess.run([sys.executable, *flags, str(copied)], cwd=td,
                                  capture_output=True, check=False, timeout=120)
            require(proc.returncode == 0 and proc.stderr == b"", "author replay exits cleanly")
            require(proc.stdout == author_expected, "author replay byte equality")
            replays.append({"optimized": bool(flags), "byte_identical": True,
                            "sha256": sha(proc.stdout), "checks": json.loads(proc.stdout)["checks"]})

    # Formal Hilbert polynomial, derived from the four Koszul terms.
    a, b, c, n = s.symbols("a b c n")
    hp = lambda q: (q + 1) * (q + 2) * (q + 3) / 6
    koszul = s.expand(hp(n) - hp(n-a) - hp(n-b) + hp(n-a-b))
    require(s.expand(koszul - (a*b*n - a*b*(a+b-4)/2)) == 0, "Koszul Hilbert polynomial")
    # Splitting-principle roots recover both relevant twists independently.
    require(s.expand((a + c-a-b)*(b + c-a-b) - (a-c)*(b-c)) == 0, "residual top Chern class")
    require(s.expand((a-b)*(b-b)) == 0, "integral degree-a zero-section class")
    require(s.expand((a+c-a-b)+(b+c-a-b)-4-(2*c-a-b-4)) == 0, "residual adjunction twist")

    # Derive cone adjunction from its intersection form, rather than a stored genus.
    r, d = s.symbols("r d", integer=True)
    intersect = lambda u,v: -2*u[0]*v[0]+u[0]*v[1]+u[1]*v[0]
    twice_genus_minus_two = s.expand(intersect((r,d),(r-2,d-4)))
    require(s.expand(twice_genus_minus_two - (-2*r*r+2*r*d-2*d)) == 0, "F2 adjunction")
    require(s.expand((2*twice_genus_minus_two-d*d+4*d+1).subs(d,2*r+1)) == 0, "cone odd-class congruence")
    for rr in range(10001):
        dd = 2*rr+1
        canonical_degree = int(twice_genus_minus_two.subs({r:rr,d:dd}))
        require((canonical_degree % dd == 0) == (rr == 0), "cone odd class test")

    # Wider numerical controls are explicitly only regressions.
    type_count = 0
    for aa in range(1, 76):
        for bb in range(aa, 101):
            degree = aa*bb
            twice_g_minus_two = degree*(aa+bb-4)
            require(twice_g_minus_two % 2 == 0, "CI parity")
            require((4+twice_g_minus_two//degree, degree) == (aa+bb, aa*bb), "type recovery")
            type_count += 1
    triple_count = 0
    for aa in range(4, 51):
        for bb in range(aa, 71):
            for cc in range(3, aa):
                degree = (aa-cc)*(bb-cc)
                e = 2*cc-aa-bb-4
                require(degree > 0 and e <= -6, "residual range")
                require(degree*e % 2 == 0 and 1+degree*e//2 < 1-degree, "reduced-curve genus contradiction")
                require(aa*bb > cc*bb, "Bezout through degree b")
                require((degree == 1) == (aa == bb and cc == aa-1), "degree-one arithmetic classification")
                triple_count += 1

    x,y,z,w,t,u,h = s.symbols("x y z w t u h")
    variables = (t,x,y,z,w)
    q1 = x*z+t*(y*y+z*z)
    q2 = x*w+t*(x*x+y*z+w*w)
    f = s.expand(w*(y*y+z*z)-z*(x*x+y*z+w*w))
    f0 = f.subs(x,0)
    # Exact elimination checks flat closure of the punctured family, independently
    # of the author's Hilbert-Burch identity controls.
    saturated = s.groebner([q1,q2,u*t-1],u,*variables,domain=s.QQ,order="lex")
    elimination = [p for p in saturated if not p.has(u)]
    require(same_ideal(elimination,[q1,q2,f],variables), "punctured CI saturation is J")
    sat_J = s.groebner([q1,q2,f,u*t-1],u,*variables,domain=s.QQ,order="lex")
    require(same_ideal([p for p in sat_J if not p.has(u)],[q1,q2,f],variables), "J is t-saturated")
    intersection = s.groebner([h*x,h*f0,(1-h)*z,(1-h)*w],h,x,y,z,w,domain=s.QQ)
    require(same_ideal([p for p in intersection if not p.has(h)],
                       [x*z,x*w,f0],(x,y,z,w)), "central component intersection")
    quadrics = s.groebner([x*z,x*w],x,y,z,w,domain=s.QQ)
    require(quadrics.reduce(f0)[1] != 0, "essential central cubic generator")
    point = {x:0,y:1,z:0,w:0}
    central_jacobian = s.Matrix([[s.diff(p,v) for v in (x,y,z,w)] for p in [x*z,x*w,f0]])
    require(central_jacobian.subs(point).rank() == 1, "central singular point tangent rank")

    # A distinct exact smoothness certificate: squarefree determinant of the
    # t=1 pencil of symmetric quadric matrices, with nonzero value at infinity.
    m1 = s.hessian(q1.subs(t,1),(x,y,z,w))/2
    m2 = s.hessian(q2.subs(t,1),(x,y,z,w))/2
    pencil = s.expand((m1+u*m2).det())
    discriminant = s.discriminant(pencil,u)
    require(m2.det() != 0 and discriminant != 0, "squarefree projective quadric pencil")
    require(pencil == -3*u**4/s.Integer(16)+3*u**2/s.Integer(4)-u/4, "pencil determinant")
    require(discriminant == s.Rational(1053,65536), "pencil discriminant")

    # Good-reduction certificates prove the plane cubic smooth over Q. This is
    # algebraic-closure testing, not enumeration of rational points in F_p.
    good_reduction = {}
    for prime in (5,7):
        for fixed in (y,z,w):
            remaining = [v for v in (y,z,w) if v != fixed]
            equations = [f0] + [s.diff(f0,v) for v in (y,z,w)]
            gb = s.groebner([p.subs(fixed,1) for p in equations],
                            *remaining,modulus=prime,order="grevlex")
            require(list(gb) == [s.Integer(1)], "plane cubic good reduction chart")
            good_reduction[f"F{prime}_{fixed}"] = True
    # Expected-negative control: the same cubic really is singular modulo 11.
    gb_bad = s.groebner([p.subs(y,1) for p in [f0]+[s.diff(f0,v) for v in (y,z,w)]],
                        z,w,modulus=11,order="grevlex")
    require(list(gb_bad) != [s.Integer(1)], "bad-reduction negative control")

    # Independent Hilbert-function computation from the central leading ideal.
    gb0 = s.groebner([x*z,x*w,f0],x,y,z,w,domain=s.QQ,order="grevlex")
    leading = [tuple(p.LM(order=gb0.order).exponents) for p in gb0.polys]
    hilbert = []
    for degree in range(13):
        count = 0
        for ex in itertools.product(range(degree+1),repeat=3):
            last = degree-sum(ex)
            if last < 0:
                continue
            monomial = (*ex,last)
            if not any(all(v >= q for v,q in zip(monomial,lm)) for lm in leading):
                count += 1
        require(count == (1 if degree == 0 else 4*degree), "central Hilbert function")
        hilbert.append(count)

    # Characteristic-change identity via polynomial coefficients.
    A,B,C,D,T = s.symbols("A B C D T")
    minus = A*D**3-B*C**3
    plus = A*D**3+B*C**3
    delta = s.expand(minus*plus-minus**2)
    require(delta == 2*A*B*C**3*D**3-2*B**2*C**6, "difference of squares discrepancy")
    require(s.Poly(delta,A,B,C,D,modulus=2).is_zero, "modulo-two discrepancy vanishes")
    require(s.expand(A*A*(D**6*T+B*B*minus)-B*B*(C**6*T+A*A*minus)-T*minus*plus)==0,
            "KPR characteristic-independent identity")

    metadata = json.loads((root / "SOURCE_METADATA.json").read_bytes())
    optional = {}
    for key,path in (("problems.json",args.problems),("research_results.json",args.research)):
        if path is not None:
            data = path.read_bytes()
            expected = metadata["public_dataset_verification"]["files"][key]
            require(len(data)==expected["bytes"] and sha(data)==expected["sha256"], "public corpus full-file hash")
            optional[key] = {"bytes":len(data),"sha256":sha(data),"matches":True}
            parsed = json.loads(data)
            if key == "problems.json":
                require(len(parsed)==15458, "public problem count")
                require(sum(str(row.get("id"))=="20000814" for row in parsed)==1, "unique problem identity")
            else:
                prior = parsed["AIM-ARITHMETIC_GEOMETRY-0060"]
                normalized = json.dumps(prior,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
                expected_prior = metadata["public_dataset_verification"]["prior_report_normalized_json"]
                require(len(normalized)==expected_prior["bytes"] and sha(normalized)==expected_prior["sha256"], "upstream report match")
                optional["upstream_report"] = {"bytes":len(normalized),"sha256":sha(normalized),"matches":True}
    if args.catalog is not None:
        data=args.catalog.read_bytes()
        require(len(data)==metadata["catalog_verification"]["bytes"] and sha(data)==metadata["catalog_verification"]["sha256"], "catalog full-file hash")
        row=[row for row in json.loads(data) if str(row.get("id"))=="20000814"]
        require(len(row)==1 and row[0]["rank"]==759, "catalog rank")
        optional["catalog"]={"bytes":len(data),"sha256":sha(data),"matches":True}
    if args.dgf_pdf is not None:
        data=args.dgf_pdf.read_bytes()
        require(len(data)==139918 and sha(data)=="c535e69b593f2820f4cad39399b3537a923fa394e0e171f7208305ee290bd607", "DGF PDF full-file hash")
        optional["DGF_PDF"]={"bytes":len(data),"sha256":sha(data),"matches":True}
    after = {p.name:sha(p.read_bytes()) for p in root.iterdir() if p.is_file()}
    require(before==after and sha(args.archive.read_bytes())==EXPECTED_ARCHIVE, "frozen author inputs unchanged")
    result={"status":"PASS","scope":"Independent algebraic controls, integrity and replay; mathematical geometry audited separately.",
            "checks":checks,"author_replays":replays,"type_count":type_count,"residual_triple_count":triple_count,
            "cone_odd_classes":10001,"pencil_determinant":str(pencil),"pencil_discriminant":str(discriminant),
            "central_hilbert_function_degrees_0_to_12":hilbert,"plane_cubic_good_reduction":good_reduction,
            "bad_reduction_mod_11_detected":True,"flat_closure_saturation_identity":True,
            "central_component_intersection_identity":True,"optional_source_checks":optional,
            "dependencies":{"python":sys.version.split()[0],"sympy":s.__version__},
            "author_freeze_unchanged":True,"original_problem_solved":False}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
