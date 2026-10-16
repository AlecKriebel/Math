"""Independent Euclidean billiard checks; no Jacobi functions or author formulas.

Replay: bundled-python -E -B -P independent_geometry.py
Only explicitly pinned local runtime_packages is added to the module path.
Every substantive check uses an explicit exception, and survives Python -O.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "runtime_packages"))
import mpmath as mp
import json
from math import gcd
from datetime import datetime, timezone

mp.mp.dps = 180
ROOT = Path(__file__).resolve().parent
TOL = mp.mpf("1e-65")
metrics = {}
counts = {}

def check(label, condition):
    counts[label] = counts.get(label, 0) + 1
    if not condition:
        raise RuntimeError("independent check failed: " + label)

def residual(label, value, tolerance=TOL):
    value = abs(value)
    metrics[label] = max(value, metrics.get(label, mp.mpf(0)))
    check(label, value < tolerance)

def dot(p, q): return p[0]*q[0] + p[1]*q[1]
def sub(p, q): return (p[0]-q[0], p[1]-q[1])
def norm(p): return mp.sqrt(dot(p, p))
def unit(p):
    r = norm(p)
    return (p[0]/r, p[1]/r)
def cross(p, q): return p[0]*q[1]-p[1]*q[0]

def second_hit(p, d, a, b):
    t = -2*(p[0]*d[0]/a**2 + p[1]*d[1]/b**2)/(d[0]**2/a**2+d[1]**2/b**2)
    return (p[0]+t*d[0], p[1]+t*d[1])

def initial_direction(p, a, b, lam):
    """Contact point by affine reduction of the caustic to a unit circle."""
    aa, bb = mp.sqrt(a*a-lam), mp.sqrt(b*b-lam)
    x, y = p[0]/aa, p[1]/bb
    r2 = x*x+y*y
    h = mp.sqrt(r2-1)
    contact = (aa*(x-y*h)/r2, bb*(y+x*h)/r2)
    d = sub(contact, p)
    if cross((p[0]/a,p[1]/b), (d[0]/a,d[1]/b)) < 0:
        contact = (aa*(x+y*h)/r2, bb*(y-x*h)/r2)
        d = sub(contact, p)
    return unit(d)

def reflected(d, p, a, b):
    n = (p[0]/a**2, p[1]/b**2)
    f = 2*dot(d,n)/dot(n,n)
    return (d[0]-f*n[0], d[1]-f*n[1])

def orbit(a,b,lam,theta,N,geometric_checks=False):
    p = (a*mp.cos(theta), b*mp.sin(theta))
    points = [p]
    d = initial_direction(p,a,b,lam)
    advance = mp.mpf(0)
    for j in range(N):
        q = second_hit(p,d,a,b)
        u, v = (p[0]/a,p[1]/b), (q[0]/a,q[1]/b)
        angle = mp.atan2(cross(u,v),dot(u,v))
        if angle < 0: angle += 2*mp.pi
        advance += angle
        if geometric_checks:
            residual("outer_ellipse", q[0]**2/a**2+q[1]**2/b**2-1)
            ell = (q[1]-p[1],p[0]-q[0])
            tangency = (a*a-lam)*ell[0]**2+(b*b-lam)*ell[1]**2-dot(ell,p)**2
            residual("chord_caustic_tangency", tangency/(a*a*dot(ell,ell)))
            direct = initial_direction(q,a,b,lam)
            nextd = unit(reflected(d,q,a,b))
            residual("reflection_vs_new_tangent", norm(sub(direct,nextd)))
            check("positive_angular_step", 0 < angle < mp.pi)
        points.append(q)
        d = reflected(d,q,a,b)
        p = q
    return points, advance

def resonant_lambda(a,b,N,tau):
    """Monotone geometric shooting; closure is separately retested by phase."""
    lo, hi = mp.mpf("1e-105")*b*b, (1-mp.mpf("1e-105"))*b*b
    target = 2*mp.pi*tau
    lval = orbit(a,b,lo,0,N)[1]-target
    hval = orbit(a,b,hi,0,N)[1]-target
    check("shooting_bracket", lval < 0 and hval > 0)
    for _ in range(540):
        mid = (lo+hi)/2
        value = orbit(a,b,mid,0,N)[1]-target
        if value < 0: lo=mid
        else: hi=mid
    return (lo+hi)/2

def intersections(points,a,b):
    result=[]
    for p,q in zip(points,points[1:]):
        determinant = p[0]*q[1]-p[1]*q[0]
        check("finite_tangent_intersection", determinant != 0)
        x = a*a*(q[1]-p[1])/determinant
        y = b*b*(p[0]-q[0])/determinant
        residual("first_tangent_equation",x*p[0]/a**2+y*p[1]/b**2-1)
        residual("second_tangent_equation",x*q[0]/a**2+y*q[1]/b**2-1)
        result.append((x,y))
    return result

def focal_logproduct(outer,a,b,sign):
    c = mp.sqrt(a*a-b*b)
    return mp.fsum(mp.log(norm((q[0]-sign*c,q[1]))) for q in outer)

PHASES = [mp.mpf(0),mp.pi/2,mp.pi/7,mp.pi*mp.mpf("0.384123")]

def one_case(a,b,N,tau,target=True,lam_override=None):
    check("primitive_winding_coprime",gcd(N,tau)==1)
    lam = resonant_lambda(a,b,N,tau) if lam_override is None else lam_override
    values=[]
    minsep=mp.inf
    for phase in PHASES:
        points,angle=orbit(a,b,lam,phase,N,True)
        residual("closed_orbit",norm(sub(points[-1],points[0]))/a)
        residual("winding_number",angle/(2*mp.pi)-tau)
        sep=min(norm(sub(p,points[0]))/a for p in points[1:-1])
        minsep=min(minsep,sep)
        check("primitive_distinct_from_start",sep > mp.mpf("1e-70"))
        outer=intersections(points,a,b)
        plus=focal_logproduct(outer,a,b,1)
        minus=focal_logproduct(outer,a,b,-1)
        if N%2==0:
            residual("antipodal_foci_product",plus-minus)
        if target:
            residual("both_foci_equal_target",plus-minus)
        values.append((plus,minus))
    variation=max(abs(x[0]-values[0][0]) for x in values)
    if target: residual("phase_invariance_target",variation)
    record={"a":str(a),"b":str(b),"N":N,"tau":tau,
            "lambda":mp.nstr(lam,125),"lambda_fraction":mp.nstr(lam/(b*b),18),
            "boundary_gap_fraction":mp.nstr(1-lam/(b*b),10),
            "maximum_logproduct_phase_difference":mp.nstr(variation,12),
            "minimum_primitive_separation_scaled":mp.nstr(minsep,10),
            "logproducts_plus":[mp.nstr(x[0],85) for x in values]}
    record["resonance_source"]="fresh geometric shooting" if lam_override is None else "prior independent shooting checkpoint, retested geometrically"
    print(json.dumps(record),flush=True)
    return record,lam,values

def main():
    results=[]
    cache={}
    if "--resume" in sys.argv:
        for line in (ROOT/"independent_geometry_attempt1_stdout.txt").read_text().splitlines():
            if line.startswith('{"a":'):
                row=json.loads(line)
                cache[(row['a'],row['b'],row['N'],row['tau'])]=mp.mpf(row['lambda'])
    choices=[(4,1),(8,1),(8,3),(12,1),(12,5),(16,1),(16,7),(32,1),(32,15),(64,1),(64,31)]
    for ratio in ["1.0001","1.5","3","10"]:
        a,b=mp.mpf(ratio),mp.mpf(1)
        for N,tau in choices:
            record,lam,values=one_case(a,b,N,tau,lam_override=cache.get((str(a),str(b),N,tau)))
            results.append(record)
    negatives=[]
    for N,tau in [(3,1),(5,1),(6,1),(7,2),(10,3),(14,5)]:
        record,lam,values=one_case(mp.mpf(3),mp.mpf(1),N,tau,False)
        check("wrong_parity_detects_variation",mp.mpf(record["maximum_logproduct_phase_difference"])>mp.mpf("1e-9"))
        record["control"]="primitive_wrong_parity"
        # Every primitive wrong-parity orbit is retested after enough traversals
        # to make the nominal number of factors divisible by four.
        repetitions=4//gcd(N,4)
        repeated=[]
        for phase,(reference,_) in zip(PHASES,values):
            points,_=orbit(mp.mpf(3),mp.mpf(1),lam,phase,N*repetitions)
            value=focal_logproduct(intersections(points,mp.mpf(3),mp.mpf(1)),mp.mpf(3),mp.mpf(1),1)
            residual("repeated_cover_is_power",value-repetitions*reference)
            repeated.append(value)
        variation=max(abs(v-repeated[0]) for v in repeated)
        check("repetition_does_not_cure_variation",variation>mp.mpf("1e-9"))
        record["repetitions_to_0_mod_4"]=repetitions
        record["repeated_logproduct_variation"]=mp.nstr(variation,12)
        negatives.append(record)
    a,b=mp.mpf(3),mp.mpf(1)
    for N,tau in [(4,1),(8,1),(12,5)]:
        lam=resonant_lambda(a,b,N,tau)
        lam2=lam*(1+mp.mpf("0.0001"))
        if lam2>=b*b: lam2=lam*(1-mp.mpf("0.0001"))
        vals=[];closure=[]
        for phase in PHASES:
            points,_=orbit(a,b,lam2,phase,N,True)
            closure.append(norm(sub(points[-1],points[0]))/a)
            vals.append(focal_logproduct(intersections(points,a,b),a,b,1))
        variation=max(abs(v-vals[0]) for v in vals)
        check("perturbed_caustic_detects_variation",variation>mp.mpf("1e-9"))
        check("perturbed_caustic_detects_nonclosure",max(closure)>mp.mpf("1e-9"))
        negatives.append({"control":"perturbed_nonresonant_caustic","N":N,"tau":tau,
                          "lambda":mp.nstr(lam2,50),"variation":mp.nstr(variation,12),
                          "maximum_closure_error":mp.nstr(max(closure),12)})
    summary={"status":"PASS","finished_utc":datetime.now(timezone.utc).isoformat(),
             "precision_digits":mp.mp.dps,"threshold":str(TOL),"case_count":len(results),
             "target_cases":results,"negative_controls":negatives,"check_counts":counts,
             "maximum_residuals":{k:mp.nstr(v,12) for k,v in metrics.items()},
             "limitations":"Finite numerical evidence only. Resonances from geometric shooting; no Jacobi functions used. Runtime packages pinned separately."}
    (ROOT/"independent_geometry_results.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("target_cases","negative_controls")},indent=2))

if __name__=="__main__": main()
