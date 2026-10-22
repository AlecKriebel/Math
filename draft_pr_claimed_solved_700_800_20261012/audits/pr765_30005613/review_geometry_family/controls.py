"""Independent finite controls: diagnostics, never a PDE/pure-point certificate."""
from fractions import Fraction as F
from itertools import product
import json, math
def inside_cube(point, center, half):
    return abs(point[0]-center) < half and all(abs(z) < half for z in point[1:])
checks = []
for d in (2,3,4,6):
    a1, a2, x1, p, delta = F(1), F(5,2), F(1), F(2), F(1,8)
    x2 = p+a2
    tested=face_added=off_face_old=0
    for off in product((F(-3,4),F(-1,2),F(0),F(1,2),F(3,4)), repeat=d):
        point=(p+delta*off[0],)+tuple(delta*z for z in off[1:])
        in0=inside_cube(point,x1,a1) or inside_cube(point,x2,a2)
        incon=inside_cube(point,p,delta)
        assert incon
        assert in0 == (off[0] != 0)
        tested+=1
        face_added += not in0
        off_face_old += in0
    checks.append(dict(d=d,tested=tested,face_added=face_added,off_face_already_in_cubes=off_face_old,pass_=True))
# The exact elementary radial profiles used as capacity diagnostics.
capacity = []
for k in (2,4,8,16,32,64):
    r=math.exp(-k)
    e_log2=2*math.pi/k
    e_linear2=3*math.pi
    e_linear3=28*math.pi*r/3
    e_linear1=2/r
    capacity.append(dict(k=k,r=r,d2_log_energy=e_log2,d2_linear_energy=e_linear2,d3_linear_energy=e_linear3,d1_linear_energy=e_linear1,d2_log_support_L2_bound=math.pi*r*r))
assert all(capacity[i+1]["d2_log_energy"] < capacity[i]["d2_log_energy"] for i in range(len(capacity)-1))
assert capacity[-1]["d2_linear_energy"] == capacity[0]["d2_linear_energy"]
assert capacity[-1]["d1_linear_energy"] > capacity[0]["d1_linear_energy"]
# d=1 negative control: for all delta>0 the two touching intervals plus
# connector are (0,2); at delta=0 the removed midpoint enforces a new trace.
# f=sin(pi*x/2) has trace f(1)=1 and is not in H01((0,1) union (1,2)).
d1=dict(connected_lowest=math.pi**2/4,disconnected_lowest=math.pi**2,midpoint_trace=1,positive_norm_resolvent_gap_lower_bound=1/(1+math.pi**2/4)-1/(1+math.pi**2),diagnostic="point-capacity-zero assumption is essential")
assert d1["positive_norm_resolvent_gap_lower_bound"]>0
# Fixed-width resonance: d=2, old halfwidth 1, new halfwidth 2.
# Old (1,1) and new (2,2) have exactly the same coefficient of pi^2.
old=F(1**2+1**2,4*1**2)
new=F(2**2+2**2,4*2**2)
assert old==new
resonance=dict(d=2,old_halfwidth=1,new_halfwidth=2,old_multiindex=[1,1],new_multiindex=[2,2],lambda_over_pi_squared=str(old),direct_sum_eigenspace_rank_at_least=2,diagnostic="nonresonant next-cube choice prevents new-cube contamination")
result=dict(status="PASS_DIAGNOSTICS_ONLY",geometry=checks,capacity=capacity,negative_dimension_one=d1,resonance=resonance,limitations=["Finite geometry grids do not prove set identities; the report proves them for arbitrary points.","Capacity arithmetic does not prove Mosco convergence; the report supplies the variational proof.","No discretized Laplacian, aperture modulus, infinite construction, or pure-point completeness is certified by this script."])
print(json.dumps(result,sort_keys=True,indent=2))
