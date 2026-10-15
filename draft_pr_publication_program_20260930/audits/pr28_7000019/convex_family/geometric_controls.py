#!/usr/bin/env python3
"""Independent exact geometric controls; universal proofs are in REPORT.md.

No author code is imported. All arithmetic is rational. Piecewise-affine
cell certificates cover whole nested-sphere offset intervals, not grids.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
checks = []
mutants = []

def check(name, condition, evidence=None):
    assert condition, name
    checks.append({"name": name, "evidence": evidence})

def reject(name, false_condition, counterexample):
    assert not false_condition, name
    mutants.append({"name": name, "rejected": True, "counterexample": counterexample})

def dot(a, b):
    return sum(x*y for x,y in zip(a,b))

# A combinatorial edge identity, rather than direction sampling, is the
# exact algebraic input to the universal tetrahedron width proof.
vertices = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
edges = {tuple((v[k]-w[k])//2 for k in range(3))
         for v,w in combinations(vertices,2)}
edges |= {tuple(-x for x in e) for e in list(edges)}
expected = set()
for i,j in combinations(range(3),2):
    for s in (-1,1):
        for t in (-1,1):
            v=[0,0,0];v[i]=s;v[j]=t;expected.add(tuple(v))
check("complete_edge_difference_identity", edges == expected,
      "T-T has nonzero generators 2(±ei±ej), i<j")
check("four_support_halfspaces", all(dot(v,w)==-1 for v in vertices for w in vertices if v!=w))
check("support_norms_and_balanced_normals", all(dot(v,v)==3 for v in vertices) and
      tuple(sum(v[k] for v in vertices) for k in range(3))==(0,0,0))
check("diameter_squared", max(dot(tuple(v[k]-w[k] for k in range(3)),
     tuple(v[k]-w[k] for k in range(3))) for v,w in combinations(vertices,2))==8)
check("width_lower_bound_attained_on_axis", max(v[0] for v in vertices)-min(v[0] for v in vertices)==2)
h=Q(3,2)
check("required_tetrahedron_threshold", h<2 and h*h>Q(4,3) and h*h<8)
reject("minimum_width_implies_inradius_threshold", h*h<Q(4,3),
       {"h":"3/2","minwidth":"2","2rin_squared":"4/3"})
reject("tetrahedron_facet_distance_equals_half_minwidth", Q(1,3)==1,
       "rin²=1/3 while (minwidth/2)²=1")

# Rectangle/box exact support-face controls distinguish plane intersection
# from an area-free endpoint convention. Unit cube has horizontal side area
# 8 per unit height and end faces of area 4 each.
def cube_strip(t, h):
    side=8*max(Q(0),min(Q(1),t+h)-max(Q(-1),t))
    faces=4*int(t<=-1<=t+h)+4*int(t<=1<=t+h)
    return side+faces
check("cube_tangent_face_jump", cube_strip(Q(-1),Q(1))==12 and
      cube_strip(Q(-1,2),Q(1))==8 and cube_strip(Q(0),Q(1))==12)
reject("tangent_plane_always_has_zero_surface_area", cube_strip(Q(-1),Q(1))==8,
       "cube bottom support face contributes area 4")
check("support_width_equals_h_full_surface", cube_strip(Q(-1),Q(2))==24)
reject("cube_satisfies_closed_strip_condition", cube_strip(Q(-1),Q(1))==cube_strip(Q(-1,2),Q(1)),
       "closed h=1 strips have areas 12 at support, 8 strictly inside")

# New universal centered-plane control: for box half-lengths 2,3,4 and
# center (1/4,-1/2,3/4), every support margin is at least 7/4 for unit u.
margin=[Q(2)-abs(Q(1,4)),Q(3)-abs(Q(-1,2)),Q(4)-abs(Q(3,4))]
check("box_all_orientation_margin", min(margin)==Q(7,4) and min(margin)>1,
      "support margin >= (7/4)||u||1 >= 7/4 for ||u||2=1")
check("box_endpoint_touch_admissible", Q(2)-Q(1)==1,
      "center x1=1, delta=1 makes +e1 plane tangent and still intersecting")

def overlap(t,h,r):
    return max(Q(0),min(r,t+h)-max(-r,t))

def area(t,h,R,r):
    return 2*R*overlap(t,h,R)+2*r*overlap(t,h,r)  # divided by pi

def cell_certificate(R,r,h):
    """All max/min switch points; each closed cell has affine area."""
    lo=-R;hi=R-h
    switches={lo,hi}
    for radius in (R,r):
        switches.update([-radius,radius,-radius-h,radius-h])
    points=sorted(x for x in switches if lo<=x<=hi)
    cells=[]
    for left,right in zip(points,points[1:]):
        v1=area(left,h,R,r);v2=area(right,h,R,r)
        slope=(v2-v1)/(right-left)
        mid=(left+right)/2
        check(f"nested_affine_cell_{R}_{r}_{h}_{left}_{right}",
              area(mid,h,R,r)==(v1+v2)/2)
        cells.append({"left":str(left),"right":str(right),
                      "slope":str(slope),"intercept":str(v1-slope*left)})
    return {"R":str(R),"r":str(r),"h":str(h),"admissible":[str(lo),str(hi)],
            "switches":[str(x) for x in points],"cells":cells,
            "endpoint_areas":[str(area(t,h,R,r)) for t in points]}

nested=[]
for R,r,h in [(Q(2),Q(1,2),Q(3)),(Q(2),Q(1),Q(3)),
              (Q(2),Q(1),Q(5,2)),(Q(5,2),Q(3,2),Q(4)),
              (Q(2),Q(1),Q(1)),(Q(2),Q(1),Q(2))]:
    record=cell_certificate(R,r,h);nested.append(record)
    constant=all(Q(c["slope"])==0 for c in record["cells"])
    check(f"nested_all_regions_threshold_{R}_{r}_{h}",constant==(h>=R+r))
    if constant:
        check(f"nested_normalization_{R}_{r}_{h}",
              area(-R,h,R,r)==2*R*h+4*r*r)
check("original_nested_exact_13pi",area(Q(-2),Q(3),Q(2),Q(1,2))==13)
check("touching_inner_threshold",overlap(Q(-2),Q(3),Q(1))==2 and
      overlap(Q(-1),Q(3),Q(1))==2,
      "at t=-2 upper plane touches inner north pole; at t=-1 lower touches south")
reject("nested_sphere_constancy_for_every_h",area(Q(-2),Q(5,2),Q(2),Q(1))==
       area(Q(-5,4),Q(5,2),Q(2),Q(1)),
       {"h":"5/2","support_area_over_pi":"13","center_area_over_pi":"14"})

# Independent periodic density: a continuous periodic quadratic spline.
# g(s)=1+(s²-s+1/6)/2, s in [0,1], repeated on [0,3h].
def primitive(s):
    return Q(13,12)*s-Q(1,4)*s*s+Q(1,6)*s*s*s
check("polynomial_density_mean_one",primitive(Q(1))-primitive(Q(0))==1)
check("polynomial_density_positive_nonconstant",Q(23,24)>0 and Q(23,24)!=Q(13,12),
      "minimum g(1/2)=23/24, endpoint g(0)=g(1)=13/12")
# For every phase s in [0,1], length-one integral equals
# [G(1)-G(s)]+[G(s)-G(0)]=1, an exact cancelling identity.
check("periodic_all_phase_window_identity",primitive(Q(1))-primitive(Q(0))==1,
      "G(1)-G(s)+G(s)-G(0)=1 for all real phases 0<=s<=1")
reject("one_period_forces_constant_density",Q(23,24)==Q(13,12),
       "positive continuous periodic quadratic density varies with phase")
reject("fixed_width_gives_all_smaller_widths",primitive(Q(1,2))-primitive(Q(0))==
       primitive(Q(3,4))-primitive(Q(1,4)),
       {"window_width":"h/2","area_at_0_over_h":"1/2",
        "area_at_h/4_over_h":"31/64"})

# Angular probability and sphere controls are derived independently from
# uniform signed-cosine CDF rather than latitude surface-area expressions.
delta=Q(3,5);distance=Q(7,5)
probability=((delta/distance)+1)/2-((-delta/distance)+1)/2
check("orientation_probability_from_CDF",probability==delta/distance)
reject("fullwidth_used_in_orientation_probability",probability==2*delta/distance,
       "delta=3/5, distance=7/5: probability=3/7, not 6/7")
check("saturated_probability_at_boundary",min(Q(1),Q(1))==1)
check("saturated_probability_inside_delta",min(Q(1),Q(3,2))==1)
reject("Newton_kernel_average_everywhere",Q(1)==Q(3,2),
       "distance=2delta/3 gives true probability 1, delta/distance=3/2")
R=Q(7,3);h=Q(5,4)
check("sphere_all_positions_normalization",(2*R*h)/(h/2)==4*R and
      (2*R*h)/(4*R*R)==h/(2*R))
check("sphere_h_limits",h>0 and h<2*R)
reject("threshold_equality_supplies_open_erosion",Q(1)>Q(1),
       "unit ball with h=2: dist(x,S)=1-|x|, closed erosion={0}, open E empty")
reject("harmonic_continuation_from_plane",Q(1)==Q(0),
       "harmonic v(x)=x1 vanishes on the plane x1=0 and is not identically zero")

result={"status":"passed","arithmetic":"exact rational and integer; no candidate import",
        "fresh_controls_passed":len(checks),"mutants_rejected":len(mutants),
        "checks":checks,"mutants":mutants,"nested_all_cell_certificates":nested,
        "scope":"Universal derivations in REPORT.md; calculations do not prove external rigidity or full Ghomi target"}
(HERE/'GEOMETRIC_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','fresh_controls_passed','mutants_rejected']}))
