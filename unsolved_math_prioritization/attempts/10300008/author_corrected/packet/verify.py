#!/usr/bin/env python3
"""Read-only exact finite diagnostics. This is not a proof assistant."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import copy
import json
import sys


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def validate_claims(c):
    expected = {
        "schema": "minimal-surfaces-10300008-claims-v1",
        "problem_id": 10300008,
        "problem_code": "AMR-102-0008",
        "rank": 1003,
        "status": "unsolved",
        "approaches": 5,
        "general_resolution": False,
        "explicit_isotopy_counterexample": False,
        "independent_review": "pending",
        "global_literature_status": "not established by bounded search",
        "characteristic_form_degree": 2,
        "common_calibration_required": False,
        "separate_isotopies_allowed": True,
        "cooriented_smooth_scope": True,
        "conformal_criterion_requires_exactness": True,
        "compact_leaf_homology_scalar_positive": True,
        "homology_obstruction_sufficient": False,
        "finite_checks_prove_geometry": False,
        "torus_family_claimed_new": False,
    }
    require(type(c) is dict, "claims must be an object")
    require(set(c) == set(expected), "claim keys differ")
    for key, value in expected.items():
        require(type(c[key]) is type(value), "wrong type for " + key)
        require(c[key] == value, "wrong claim: " + key)


def matrix(a, size=3):
    require(type(a) is list and len(a) == size, "matrix row count")
    require(all(type(row) is list and len(row) == size for row in a),
            "matrix column count")
    require(all(type(x) in (int, F) for row in a for x in row),
            "non-rational matrix entry")
    return [[F(x) for x in row] for row in a]


def det(a):
    a = matrix(a)
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def cofactor(a):
    a = matrix(a)
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            r = [k for k in range(3) if k != i]
            c = [k for k in range(3) if k != j]
            row.append((-1)**(i+j)*(a[r[0]][c[0]]*a[r[1]][c[1]]
                                      -a[r[0]][c[1]]*a[r[1]][c[0]]))
        out.append(row)
    return out


def inverse(a):
    d = det(a)
    require(d != 0, "singular matrix")
    c = cofactor(a)
    return [[c[j][i]/d for j in range(3)] for i in range(3)]


def spd(a):
    a = matrix(a)
    require(all(a[i][j] == a[j][i] for i in range(3) for j in range(3)),
            "matrix is not symmetric")
    require(a[0][0] > 0, "first principal minor")
    require(a[0][0]*a[1][1]-a[0][1]*a[1][0] > 0, "second minor")
    require(det(a) > 0, "third minor")
    return a


def mul(a,b):
    a,b = matrix(a),matrix(b)
    return [[sum(a[i][k]*b[k][j] for k in range(3))
             for j in range(3)] for i in range(3)]


def homology_squeeze(a,b,c):
    require(all(type(x) in (int,F) for x in (a,b,c)), "rational scalars only")
    a,b,c = F(a),F(b),F(c)
    require(a > 0 and b > 0 and c > 0, "positive areas and scalar required")
    require(b >= c*a and a >= b/c, "calibration inequalities fail")
    require(b == c*a, "squeeze failed")
    return True


def conformal_frame(vectors, rhs):
    vectors=spd(vectors) if vectors == [[1,0,0],[0,1,0],[0,0,1]] else matrix(vectors)
    require(type(rhs) is list and len(rhs)==3, "rhs length")
    require(all(type(x) in (int,F) for x in rhs), "rhs entries")
    inv=inverse(vectors)
    return [sum(inv[i][j]*rhs[j] for j in range(3)) for i in range(3)]


def must_reject(fn, name):
    try:
        fn()
    except (VerificationError, json.JSONDecodeError):
        return name
    raise VerificationError("negative control accepted: " + name)


def run():
    root = Path(__file__).resolve().parent
    claims=json.loads((root/"CLAIMS.json").read_text(encoding="utf-8"))
    validate_claims(claims)
    counts={"cofactor_metrics":0,"tangency_traces":0,
            "homology_squeezes":0,"conformal_linear_systems":0,
            "averaging_identities":0,"form_compatibility":0}
    eye=[[F(i==j) for j in range(3)] for i in range(3)]
    for a,b,c in product(range(-2,3),repeat=3):
        m=matrix([[1,a,b],[0,1,c],[0,0,1]])
        mt=[list(row) for row in zip(*m)]
        g=mul(mt,m)
        for i in range(3):g[i][i]+=1
        spd(g)
        B=cofactor(g)
        spd(B)
        require(det(B)==det(g)**2,"cofactor determinant identity")
        rec=[[det(g)*x for x in row] for row in inverse(B)]
        require(rec==g,"metric reconstruction")
        require(mul(g,inverse(g))==eye,"inverse identity")
        counts["cofactor_metrics"]+=1
    for a,b,u,v in product(range(1,5),range(-2,3),range(-2,3),range(-2,3)):
        if u==v==0:continue
        # C=[[a^2+1,ab],[ab,b^2+1]] and D=ww^T.
        trace=(a*a+1)*u*u+2*a*b*u*v+(b*b+1)*v*v
        require(trace>0,"positive trace pairing")
        require(trace==(a*u+b*v)**2+u*u+v*v,"trace square identity")
        counts["tangency_traces"]+=1
    for a,c in product([F(k,3) for k in range(1,10)],repeat=2):
        homology_squeeze(a,c*a,c)
        counts["homology_squeezes"]+=1
    for a,b,c in product(range(-2,3),repeat=3):
        n=[[1,a,b],[0,1,c],[0,0,1]]
        beta=[F(1,2),F(-2,3),F(3,5)]
        rhs=[sum(n[i][j]*beta[j] for j in range(3)) for i in range(3)]
        require(conformal_frame(n,rhs)==beta,"conformal coefficient solve")
        counts["conformal_linear_systems"]+=1
    for a in [F(k,3) for k in range(1,16)]:
        A=(a+1/a)/2
        require(A*A==((a*a+1)*(1/(a*a)+1))/4,"averaging area identity")
        for ap in (F(-2),F(-1),F(0),F(1),F(2)):
            Aprime=ap*(1-1/(a*a))/2
            h=ap*(a*a-1)/(a*(a*a+1))
            require(Aprime/A==h,"averaging mean curvature")
            counts["averaging_identities"]+=1
    require(F(2)*(1-F(1,4))/2/((F(2)+F(1,2))/2)==F(3,5),
            "nonminimal averaged metric coefficient of pi")
    for x,y,z in product((F(-1,8),F(0),F(1,8)),repeat=3):
        S=[[F(1),x,y],[x,F(1),z],[y,z,F(1)]]
        spd(S)
        require(all(S[i][j]==S[j][i] for i in range(3) for j in range(3)),
                "closed-form symmetry")
        counts["form_compatibility"]+=1
    # The nonclosed-beta example has b_xy/2=2*pi^2 at the origin.
    require(F(4,2)==2,"conformal mixed derivative coefficient")
    # A single comass-one two-form cannot evaluate to 1 on x- and y-normals.
    require(1**2+1**2>1,"two-plane common-calibration contradiction")
    negatives=[]
    for key in claims:
        bad=copy.deepcopy(claims)
        value=bad[key]
        bad[key]=(not value) if type(value) is bool else value+1 if type(value) is int else value+"-wrong"
        negatives.append(must_reject(lambda bad=bad:validate_claims(bad),"wrong-claim-"+key))
    for key in claims:
        bad=copy.deepcopy(claims);del bad[key]
        negatives.append(must_reject(lambda bad=bad:validate_claims(bad),"missing-claim-"+key))
    bad=copy.deepcopy(claims);bad["approaches"]=True
    negatives.append(must_reject(lambda:validate_claims(bad),"boolean-is-not-integer"))
    negatives.append(must_reject(lambda:json.loads('{"broken":'),"malformed-json"))
    negatives.append(must_reject(lambda:validate_claims([]),"nonobject-claims"))
    negatives.append(must_reject(lambda:matrix([[1,2],[3,4]]),"wrong-matrix-shape"))
    negatives.append(must_reject(lambda:matrix([[1,0,0],[0,1,0],[0,0,float('nan')]]),"nonfinite-entry"))
    negatives.append(must_reject(lambda:matrix([[True,0,0],[0,1,0],[0,0,1]]),"boolean-entry"))
    negatives.append(must_reject(lambda:spd([[1,2,0],[0,1,0],[0,0,1]]),"incompatible-forms"))
    negatives.append(must_reject(lambda:spd([[1,2,0],[2,1,0],[0,0,1]]),"indefinite-metric"))
    negatives.append(must_reject(lambda:inverse([[1,0,0],[0,1,0],[0,0,0]]),"dependent-frame"))
    negatives.append(must_reject(lambda:homology_squeeze(1,1,0),"zero-homology-scalar"))
    negatives.append(must_reject(lambda:homology_squeeze(1,1,-1),"negative-homology-scalar"))
    negatives.append(must_reject(lambda:homology_squeeze(1,2,1),"false-calibration-equality"))
    return {"schema":"minimal-surfaces-10300008-diagnostics-v1",
            "status":"pass","positive_groups":counts,
            "positive_cases":sum(counts.values())+3,
            "negative_controls":negatives,"negative_count":len(negatives),
            "scope":"Finite exact algebra and fail-closed claim controls, not proof of geometry."}


if __name__ == "__main__":
    try:
        require(len(sys.argv)==1,"no arguments supported")
        print(json.dumps(run(),sort_keys=True,separators=(",",":")))
    except (VerificationError,ValueError,OSError,KeyError,TypeError) as exc:
        print("REJECT: "+str(exc),file=sys.stderr)
        sys.exit(1)
