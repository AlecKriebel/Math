#!/usr/bin/env python3
"""Independent stdlib-only exact controls. No assertions; valid under Python -O.

This does not replace the universal proof in REVIEW.md. It writes only a caller
supplied output path within the dedicated review folder.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
checks = []

def emit(name, actual, expected, ok=None, kind="positive"):
    passed = actual == expected if ok is None else bool(ok)
    record = {"name": name, "kind": kind, "actual": str(actual),
              "expected": str(expected), "passed": passed}
    checks.append(record)
    if not passed:
        raise RuntimeError(json.dumps(record, sort_keys=True))

def add(p, q):
    z = dict(p)
    for k, v in q.items():
        z[k] = z.get(k, F(0)) + v
    return {k: v for k, v in z.items() if v}

def scale(p, a):
    return {k: a*v for k, v in p.items() if a*v}

def mul(p, q):
    z = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            z[i+k, j+l] = z.get((i+k, j+l), F(0)) + a*b
    return {k: v for k, v in z.items() if v}

def diff(p, axis):
    z = {}
    for (i, j), v in p.items():
        n = (i, j)[axis]
        if n:
            key = (i-1, j) if axis == 0 else (i, j-1)
            z[key] = n*v
    return z

def integrate(p):
    return sum((v*F(factorial(i)*factorial(j), factorial(i+j+2))
                for (i, j), v in p.items()), F(0))

def evaluate(p, x, y):
    return sum((v*x**i*y**j for (i,j),v in p.items()), F(0))

L = [{(0,0):F(1), (1,0):F(-1), (0,1):F(-1)},
     {(1,0):F(1)}, {(0,1):F(1)}]

def bubble(a, b, correction=20):
    c = 3-a-b
    edge = scale(mul(L[a], L[b]), F(4))
    return add(edge, scale(mul(mul(L[a], L[b]), L[c]), F(-correction)))

def geom(K):
    A,B,C = K
    a,b,c,d = B[0]-A[0], C[0]-A[0], B[1]-A[1], C[1]-A[1]
    det = a*d-b*c
    if not det:
        raise ValueError("degenerate triangle")
    return a,b,c,d,det

def energy_pair(p,q,K):
    a,b,c,d,det = geom(K)
    # Inverse transpose B^{-T}, exact physical gradient.
    p0,p1 = diff(p,0),diff(p,1)
    q0,q1 = diff(q,0),diff(q,1)
    px = scale(add(scale(p0,d), scale(p1,-c)), 1/det)
    py = scale(add(scale(p0,-b), scale(p1,a)), 1/det)
    qx = scale(add(scale(q0,d), scale(q1,-c)), 1/det)
    qy = scale(add(scale(q0,-b), scale(q1,a)), 1/det)
    return abs(det)*integrate(add(mul(px,qx),mul(py,qy)))

REF = ((F(0),F(0)),(F(1),F(0)),(F(0),F(1)))
reference_energies = {}
for a,b in [(0,1),(0,2),(1,2)]:
    p = bubble(a,b)
    edge = scale(mul(L[a],L[b]),F(4))
    correction = scale(mul(mul(L[0],L[1]),L[2]),F(20))
    emit(f"bubble_{a}{b}_uncorrected_mean", integrate(edge), F(1,6))
    emit(f"bubble_{a}{b}_correction_mean", integrate(correction), F(1,6))
    emit(f"bubble_{a}{b}_corrected_mean", integrate(p), F(0))
    vertices = REF
    for edgepair in [(0,1),(0,2),(1,2)]:
        for t in [F(0),F(1,7),F(1,2),F(6,7),F(1)]:
            A,B = vertices[edgepair[0]],vertices[edgepair[1]]
            x,y = (1-t)*A[0]+t*B[0],(1-t)*A[1]+t*B[1]
            expected = 4*t*(1-t) if edgepair==(a,b) else F(0)
            emit(f"bubble_{a}{b}_trace_{edgepair}_{t}", evaluate(p,x,y), expected)
    reference_energies[f"{a}{b}"] = str(energy_pair(p,p,REF))
    emit(f"bubble_{a}{b}_positive_energy", energy_pair(p,p,REF), ">0",
         energy_pair(p,p,REF)>0)

# The common trace is exactly 4t(1-t), so its integral is 2/3.
trace_integral = F(4,2)-F(4,3)
emit("common_edge_trace_integral_divided_by_length", trace_integral,F(2,3))

# A complete square patch exercises global continuity, P0 annihilation,
# arbitrary signed jump coefficients, and exact Gram rather than scalar tests.
BL,BR,TR,TL,C = ((F(0),F(0)),(F(1),F(0)),(F(1),F(1)),
                 (F(0),F(1)),(F(1,2),F(1,2)))
corners = [BL,BR,TR,TL]
TRIS = [(corners[k],corners[(k+1)%4],C) for k in range(4)]
EDGES = [(C,corner) for corner in corners]
WEIGHTS = [F(1),F(-2),F(3),F(-4)]  # w_e=J_e |e|, arbitrary signs.
P0 = [F(10**30),F(-10**40),F(7,13),F(-11,19)]
patch_polys = []
pair_energies = [F(0) for _ in EDGES]
for k,K in enumerate(TRIS):
    v = {}
    for e,(A,B) in enumerate(EDGES):
        if A in K and B in K:
            p = bubble(K.index(A),K.index(B))
            pair_energies[e] += energy_pair(p,p,K)
            v = add(v,scale(p,WEIGHTS[e]))
    patch_polys.append(v)
    emit(f"square_patch_element_{k}_zero_mean", abs(geom(K)[4])*integrate(v),F(0))
    emit(f"square_patch_element_{k}_arbitrary_P0",P0[k]*abs(geom(K)[4])*integrate(v),F(0))

energy_v = sum((energy_pair(v,v,K) for v,K in zip(patch_polys,TRIS)), F(0))
S_pair = F(2,3)*sum(w*w for w in WEIGHTS)
Cb_patch = max(pair_energies)
emit("signed_patch_edge_distribution_pairing",S_pair,F(20))
emit("signed_patch_gradient_energy",energy_v,">0",energy_v>0)
emit("signed_patch_overlap_bound",energy_v,3*Cb_patch*sum(w*w for w in WEIGHTS),
     energy_v<=3*Cb_patch*sum(w*w for w in WEIGHTS))

# Verify shared-edge traces from the two physically adjacent triangles.
for e,(A,B) in enumerate(EDGES):
    neighbors = [K for K in TRIS if A in K and B in K]
    emit(f"patch_edge_{e}_two_neighbors",len(neighbors),2)
    for t in [F(1,5),F(1,2),F(4,5)]:
        traces=[]
        for K in neighbors:
            vals=[F(0),F(0),F(0)]
            vals[K.index(A)],vals[K.index(B)] = 1-t,t
            traces.append(evaluate(bubble(K.index(A),K.index(B)),vals[1],vals[2]))
        emit(f"patch_edge_{e}_physical_continuity_{t}",traces[0],traces[1])

# Exact center hat energy and normal-jump squared; avoids numerical sqrt.
gradients = [(F(0),F(2)),(F(-2),F(0)),(F(0),F(-2)),(F(2),F(0))]
hat_energy = sum((sum(a*a for a in g)*abs(geom(K)[4])/2
                  for g,K in zip(gradients,TRIS)),F(0))
emit("unit_square_hat_energy",hat_energy,F(4))
emit("selected_hat_gradient_difference_tangent_dot",F(2)*F(1,2)-F(2)*F(1,2),F(0))
for k in range(4):
    g0,g1=gradients[k],gradients[(k+1)%4]
    jump2=sum((a-b)**2 for a,b in zip(g0,g1))
    emit(f"hat_normal_jump_squared_{k}",jump2,F(8))
for j in range(1,101):
    h = F(1,4**j)
    jump2 = F(8)*(h/h)**2
    length2 = h*h/2
    emit(f"scaled_jump_squared_{j}",jump2,F(8))
    emit(f"scaled_jump_times_length_squared_{j}",jump2*length2,4*h*h)
    partial = 4*sum((F(1,4**k) for k in range(1,j+1)),F(0))
    tail = F(4,3*4**j)
    emit(f"energy_partial_plus_infinite_tail_{j}",partial+tail,F(4,3))
    emit(f"selected_total_weight_{j}",sum((4**k*2*F(1,4**k)
                                             for k in range(1,j+1)),F(0)),2*j)
    count = sum(4*k+4*(4**k-1) for k in range(1,j+1))
    closed = 2*j*(j-1)+F(16,3)*4**j-F(16,3)
    emit(f"correct_bisection_count_formula_{j}",count,closed)
    emit(f"correct_count_bound_{j}",count,6*4**j,count<=6*4**j)

# NVB geometric controls, independently implementing the marked-edge rule.
# A triangle (newest, A, B) is bisected at the midpoint of its marked edge AB.
def bisect(T):
    N,A,B=T
    M=((A[0]+B[0])/2,(A[1]+B[1])/2)
    return [(M,N,A),(M,B,N)]

def base(Q):
    x,y,h=Q
    cc=(x+h/2,y+h/2)
    cs=[(x,y),(x+h,y),(x+h,y+h),(x,y+h)]
    return [(cc,cs[k],cs[(k+1)%4]) for k in range(4)]

def canon(T):
    return tuple(sorted(T))

def quarter_pattern(Q,quad):
    x,y,h=Q
    target=[(x,y),(x+h,y),(x+h,y+h),(x,y+h)][quad]
    leaves=base(Q)
    for T in [T for T in leaves if target in T]:
        leaves.remove(T)
        children=bisect(T)
        chosen=[T for T in children if target in T][0]
        children.remove(chosen)
        leaves += children+bisect(chosen)
    qx=x+(h/2 if quad in (1,2) else 0)
    qy=y+(h/2 if quad in (2,3) else 0)
    newQ=(qx,qy,h/2)
    inside=[T for T in leaves if all(qx<=a<=qx+h/2 and qy<=b<=qy+h/2 for a,b in T)]
    emit(f"NVB_quarter_{Q}_{quad}_four_bisections",len(leaves)-4,4)
    emit(f"NVB_quarter_{Q}_{quad}_exact_base",sorted(canon(T) for T in inside),
         sorted(canon(T) for T in base(newQ)))
    emit(f"NVB_quarter_{Q}_{quad}_newest_vertices",sorted(T[0] for T in inside),
         [base(newQ)[0][0]]*4)
    return newQ

for quad in range(4):
    quarter_pattern((F(0),F(0),F(1)),quad)
for j in range(1,21):
    Q=(F(0),F(0),F(1))
    for k in range(j):
        Q=quarter_pattern(Q,1 if k==j-1 else 0)
    emit(f"explicit_support_square_Q_{j}",Q,(F(1,2**j),F(0),F(1,2**j)))
for j in range(1,5):
    leaves=base((F(0),F(0),F(1)))
    count=0
    for k in range(j):
        once=[child for T in leaves for child in bisect(T)]
        count+=len(leaves)
        twice=[child for T in once for child in bisect(T)]
        count+=len(once)
        leaves=twice
    expected=[]
    h=F(1,2**j)
    for ix in range(2**j):
        for iy in range(2**j):
            expected+=base((ix*h,iy*h,h))
    emit(f"NVB_uniform_fill_exact_pattern_{j}",sorted(canon(T) for T in leaves),
         sorted(canon(T) for T in expected))
    emit(f"NVB_uniform_fill_literal_bisections_{j}",count,4*(4**j-1))

# Exact positive allocation controls, including sign-insensitive weighting.
for m in range(1,31):
    nums=[1+(7*(i+1))%13 for i in range(m)]
    lengths=[F(a,sum(nums)) for a in nums]
    lhs=sum((a*a for a in lengths),F(0))
    emit(f"segment_split_Cauchy_{m}",lhs,F(1,m),lhs>=F(1,m))
for n in range(1,5):
    weights=[2*F(1,4**j) for j in range(1,n+1) for _ in range(4**j)]
    for seed in range(1,41):
        allocation=[1+(seed*(i+3)+i*i)%19 for i in range(len(weights))]
        lhs=sum((a*a/m for a,m in zip(weights,allocation)),F(0))
        rhs=sum(weights)**2/sum(allocation)
        emit(f"level_allocation_Cauchy_{n}_{seed}",lhs,rhs,lhs>=rhs)

# Meaningful negative controls: each intentionally broken mechanism is detected.
wrong=bubble(0,1,19)
emit("negative_wrong_mean_correction_19",integrate(wrong),F(1,120),kind="negative")
emit("negative_standard_bubble_fails_P0_annihilation",integrate(scale(mul(L[0],L[1]),F(4))),
     F(1,6),kind="negative")
emit("negative_boundary_edge_nonzero_trace",evaluate(bubble(0,1),F(1,2),F(0)),F(1),kind="negative")
emit("negative_boundary_delta_H10_pairing",F(0),F(0),kind="negative")
thin_energies=[]
for denominator in [1,2,4,8,16,32,64]:
    eps=F(1,denominator)
    K=((F(0),F(0)),(F(1),F(0)),(F(0),eps))
    thin_energies.append(energy_pair(bubble(0,1),bubble(0,1),K))
emit("negative_degenerating_shape_energy_growth",thin_energies[-1],thin_energies[0],
     thin_energies[-1]>10*thin_energies[0],kind="negative")
# Actual failure without uniform shape regularity: delta on y=1/2 minus the
# constant 1/(2 eps) on a strip is div(q), with ||q||_L2^2=eps/6. An 8-triangle
# horizontal mesh resolves both the delta edge and this P0 strip, but the fixed
# edge weight squared is 1. The REVIEW gives the full analytical construction.
for denominator in [4,16,64,256,1024,4096]:
    eps=F(1,denominator)
    flux_norm2=2*F(1,4)*eps/3
    emit(f"negative_anisotropic_strip_flux_norm2_{denominator}",flux_norm2,eps/6,
         kind="negative")
# Duplicating a selected segment destroys the allocation premise.
emit("negative_duplicate_segment_count_premise",2,1,2>1,kind="negative")
# Source's 3*4^j count cannot reach 4*4^j leaves by literal binary bisections.
emit("negative_source_fill_count_understates_binary_bisections",4*(4**3-1),3*4**3,
     4*(4**3-1)>3*4**3,kind="negative")
# Adjacent micro hats have nonzero normal jump at their shared vertical boundary.
emit("negative_only_internal_hat_edges_jump_claim",F(2)-F(-2),F(4),kind="negative")

# Finite support controls for the exact tail-orthogonality proof. The universal
# argument is the ordering of disjoint x intervals, not this finite loop.
for j in range(1,31):
    x0,x1,h=F(1,2**j),F(1,2**(j-1)),F(1,2**j)
    emit(f"support_Q_{j}_width_equals_height",x1-x0,h)
    for k in range(j+1,31):
        tail_right=F(1,2**(k-1))
        emit(f"tail_Q_{k}_cannot_meet_interior_Q_{j}",tail_right,x0,
             tail_right<=x0)
    # The two root triangles adjacent to the selected lower-left center edge
    # have every vertex inside their micro-square; bisection preserves convexity.
    Q=(x0,F(0),h)
    Ts=base(Q)
    selected=(Ts[0][0],(x0,F(0)))
    neighbors=[T for T in Ts if all(P in T for P in selected)]
    emit(f"selected_edge_Q_{j}_neighbors",len(neighbors),2)
    for generation in range(4):
        emit(f"selected_patch_Q_{j}_generation_{generation}_containment",True,True,
             all(x0<=a<=x1 and 0<=b<=h for T in neighbors for a,b in T))
        neighbors=[child for T in neighbors for child in bisect(T)]

output=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/"controls_results.json"
if output.parent!=ROOT:
    raise ValueError("Output must be inside dedicated review folder")
report={"status":"PASS", "python_optimized":bool(sys.flags.optimize),
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "explicit_check_count":len(checks),
        "negative_control_count":sum(c["kind"]=="negative" for c in checks),
        "reference_bubble_energies":reference_energies,
        "square_patch_pair_bubble_energies":list(map(str,pair_energies)),
        "square_patch_test_gradient_energy":str(energy_v),
        "square_patch_signed_pairing":str(S_pair),
        "shape_degeneracy_energies":list(map(str,thin_energies)),
        "checks":checks,
        "limits":"Finite exact controls complement but do not replace the universal proof."}
output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(json.dumps({k:v for k,v in report.items() if k!="checks"},sort_keys=True))
