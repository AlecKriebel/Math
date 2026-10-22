#!/usr/bin/env python3
"""Read-only exact arithmetic checks for the scoped foam-cell note.

No assertions, external dependencies, network calls, or file writes are used.
This checks identities and obstructions, not a geometric realization theorem.
"""
from fractions import Fraction as F
from itertools import combinations
import json
import math


class VerificationError(ValueError):
    pass


CHECKS = []
NEGATIVE_CONTROLS = []


def require(condition, name):
    if not condition:
        raise VerificationError(name)
    CHECKS.append(name)


def reject(operation, name):
    try:
        operation()
    except VerificationError:
        NEGATIVE_CONTROLS.append(name)
        return
    raise VerificationError("Negative control was not rejected: " + name)


def atan_bounds(x, n=40):
    if not 0 < x < 1 or n < 2:
        raise VerificationError("Invalid alternating arctangent input")
    s = sum(((-1) ** k * x ** (2*k+1) / (2*k+1) for k in range(n)), F(0))
    t = (-1) ** n * x ** (2*n+1) / (2*n+1)
    return min(s, s+t), max(s, s+t)


def cos_bounds(x, n=24):
    if not 0 <= x <= F(13, 10) or n < 2:
        raise VerificationError("Invalid decreasing cosine-series input")
    s = sum(((-1) ** k * x ** (2*k) / math.factorial(2*k)
             for k in range(n)), F(0))
    t = (-1) ** n * x ** (2*n) / math.factorial(2*n)
    return min(s, s+t), max(s, s+t)


def cubic_sphere_counts(f, e, v):
    if f < 4 or f-e+v != 2 or 2*e != 3*v:
        raise VerificationError("Not the required cubic sphere incidence counts")


# Arithmetic in Q(sqrt(3)), represented as (a,b) for a+b*sqrt(3).
def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def mul(x, y):
    return x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0]


ZERO = (F(0), F(0))
ONE = (F(1), F(0))


def vec_add(x, y):
    return tuple(add(a,b) for a,b in zip(x,y))


def dot(x, y):
    result = ZERO
    for a,b in zip(x,y):
        result = add(result, mul(a,b))
    return result


def validate_plateau_conormals(vectors):
    if len(vectors) != 3:
        raise VerificationError("Three conormals required")
    if any(dot(v,v) != ONE for v in vectors):
        raise VerificationError("Conormals not unit")
    if any(dot(a,b) != (-F(1,2), F(0)) for a,b in combinations(vectors,2)):
        raise VerificationError("Not a 120-degree junction")


def stellar_counts(n, total_faces, insertions):
    if n <= 0 or insertions < 0:
        raise VerificationError("Invalid subdivision counts")
    return n+insertions, total_faces+8*insertions


def main():
    a0,a1 = atan_bounds(F(1,5))
    b0,b1 = atan_bounds(F(1,239))
    # Machin's exact identity pi = 16 atan(1/5) - 4 atan(1/239).
    plo,phi = 16*a0-4*b1, 16*a1-4*b0
    require(F(3141592653589793238,10**18) < plo < phi <
            F(3141592653589793239,10**18), "certified pi enclosure")
    tlo,thi = F(12309594173407746,10**16), F(12309594173407748,10**16)
    require(cos_bounds(tlo)[0] > F(1,3), "lower theta endpoint certified by cosine")
    require(cos_bounds(thi)[1] < F(1,3), "upper theta endpoint certified by cosine")
    require(0 < tlo < thi < plo, "cosine monotonicity interval")
    dlo,dhi = 3*tlo-phi, 3*thi-plo
    require(0 < dlo < dhi, "positive corner defect")
    flo,fhi = 2+2*plo/dhi, 2+2*phi/dlo
    require(13 < flo < fhi < 14, "13 < average threshold < 14")
    require(5*thi < 2*plo, "positive pentagonal-face deficit")

    deficits = {}
    for f in (4,12,13,14,100):
        e,v = 3*f-6, 2*f-4
        cubic_sphere_counts(f,e,v)
        require((4+v,-3*v) == (2*f,-6*(f-2)),
                "facewise and cellwise Gauss-Bonnet coefficients F="+str(f))
        lo,hi = 4*plo-v*dhi, 4*phi-v*dlo
        deficits[str(f)] = {"certified_lower_rational":str(lo),
                            "certified_upper_rational":str(hi),
                            "decimal_display":[float(lo),float(hi)]}
        if f <= 13:
            require(lo > 0, "positive cell deficit F="+str(f))
        elif f == 14:
            require(hi < 0, "14-face deficit has opposite sign")
    reject(lambda: cubic_sphere_counts(4,6,5), "wrong tetrahedral vertex count")
    reject(lambda: cubic_sphere_counts(12,30,19), "wrong dodecahedral vertex count")
    reject(lambda: cos_bounds(F(3)), "out-of-scope cosine remainder bound")

    eta = [((F(1),F(0)),ZERO,ZERO),
           ((-F(1,2),F(0)),ZERO,(F(0),F(1,2))),
           ((-F(1,2),F(0)),ZERO,(F(0),-F(1,2)))]
    validate_plateau_conormals(eta)
    require(vec_add(vec_add(eta[0],eta[1]),eta[2]) == (ZERO,ZERO,ZERO),
            "exact conormal cancellation")
    for i,j in combinations(range(3),2):
        q=vec_add(eta[i],eta[j])
        require(dot(q,q)==ONE, "cell edge conormal sum has norm one "+str((i,j)))
    kappa=((-F(1),F(0)),ZERO,ZERO)
    kg=[dot(kappa,v) for v in eta]
    require(kg == [(-F(1),F(0)),(F(1,2),F(0)),(F(1,2),F(0))],
            "local circular-junction geodesic curvatures")
    require(add(kg[1],kg[2]) == ONE, "one adjacent region has positive edge transport")
    require(add(kg[0],kg[1]) == (-F(1,2),F(0)),
            "another adjacent region has negative edge transport")
    require(F(4,3)-1-F(1,3)==0, "catenoid minimal ODE at common circle")
    reject(lambda: validate_plateau_conormals([eta[0],eta[0],eta[2]]),
           "duplicated sheet is not a Plateau junction")
    reject(lambda: validate_plateau_conormals([eta[0],eta[1]]),
           "missing third sheet")

    for n in range(1,15):
        m,s=stellar_counts(n,14*n,1)
        require((m,s)==(n+1,14*n+8), "stellar insertion incidence N="+str(n))
        average=F(s,m)
        require((average < flo) if n <= 8 else (average > fhi),
                "single-insertion average threshold N="+str(n))
    require(stellar_counts(1,14,6)==(7,62), "fully decorated Kelvin count 62/7")
    require(F(62,7)<flo, "full decoration violates minimal-foam average bound")
    require(F(134,10)>fhi and 4 < flo,
            "average arithmetic does not imply a per-cell lower bound")
    reject(lambda: stellar_counts(0,0,1), "empty starting decomposition")
    reject(lambda: stellar_counts(2,28,-1), "negative subdivision count")

    rho_lo=(14-fhi)/(fhi-8)
    rho_hi=(14-flo)/(flo-8)
    require(0 < rho_lo < rho_hi < 1, "certified admissible insertion-density interval")
    out={"status":"PASS", "checks":CHECKS, "negative_controls":NEGATIVE_CONTROLS,
         "check_count":len(CHECKS), "negative_control_count":len(NEGATIVE_CONTROLS),
         "arithmetic":"Exact rational enclosures and Q(sqrt(3)); floats are display only.",
         "geometric_scope":"No numerical or exact realization of a bounded foam cell is claimed.",
         "average_threshold_display":[float(flo),float(fhi)],
         "insertion_density_display":[float(rho_lo),float(rho_hi)],
         "cell_deficits":deficits}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
