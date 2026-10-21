"""Exact construction distinctions for the priority audit; no k404 counterexample."""
from fractions import Fraction as Q
from pathlib import Path
import json

def dot(u, v): return sum(a*b for a,b in zip(u,v))
def det(u, v): return u[0]*v[1]-u[1]*v[0]
def area(vertices): return sum(det(vertices[i],vertices[(i+1)%len(vertices)]) for i in range(len(vertices)))/Q(2)

# Ellipse x^2/25+y^2/9=1, original focus F=(4,0).
f=(Q(4),Q(0)); vertices=[(Q(5),Q(0)),(Q(0),Q(3))]
normals=[tuple(p[i]-f[i] for i in range(2)) for p in vertices]
squared=[dot(u,u) for u in normals]
assert squared==[Q(1),Q(25)]
assert squared[0]!=squared[1]
# The polar of the unit-focus-inverted point is the actual antipedal line.
for p,u,r2 in zip(vertices,normals,squared):
 inverted=tuple(x/r2 for x in u)
 assert dot(inverted,u)==1
 assert dot(u,u)==r2

# A shared circular vertex locus alone does not force equal polygon areas.
# These two controls are not claimed to be billiard orbits with one caustic.
square=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(-1),Q(0)),(Q(0),Q(-1))]
other=[(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(-1),Q(0)),(Q(0),Q(-1))]
assert all(dot(p,p)==1 for p in square+other)
assert area(square)==2 and area(other)==Q(9,5)
result={'result':'PASS_CONSTRUCTION_DISTINCTIONS','ellipse_semiaxes':[5,3],'focus':[4,0],
 'squared_focal_distances':[str(x) for x in squared],
 'one_fixed_circle_cannot_polarize_both_original_vertices_into_actual_antipedal_lines':True,
 'polar_of_unit_focus_inverse_matches_actual_antipedal_line':True,
 'circle_locus_controls_signed_areas':[str(area(square)),str(area(other))],
 'controls_are_not_billiard_counterexamples':True,'k404_truth_is_not_tested_by_this_script':True}
path=Path(__file__).resolve().with_name('construction_check_result.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
