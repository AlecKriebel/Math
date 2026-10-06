#!/usr/bin/env python3
"""Independent exact adversarial diagnostics; no continuum theorem is inferred."""
import json
import sys
from fractions import Fraction as F
from itertools import product

if sys.flags.optimize:
    raise RuntimeError("Independent controls refuse optimized Python execution.")
if sys.argv[1:] not in ([], ["--negative-control"]):
    raise RuntimeError("Unexpected argument.")
counts = {}
def require(name, condition):
    if not condition:
        raise RuntimeError("Independent control failed: " + name)
    counts[name] = counts.get(name, 0) + 1
if sys.argv[1:] == ["--negative-control"]:
    require("intentional false statement", False)

# Disparate residual constants expose the erroneous substitution by the maximum ratio.
ma, mb, eps = F(1, 4), F(1, 40), F(1, 200)
ka, kb, delta, eta = F(1), F(1, 100), F(1), F(3, 25)
kappa = max(eps/ma, eps/mb)
require("counterexample_has_legal_apertures", eps < F(1, 160))
require("counterexample_has_both_legal_root_domains", ka*eta < (ma-eps)*delta/2 and kb*eta < (mb-eps)*delta/2)
require("common_maximum_5_over_8_bound_is_false", kappa*delta+ka*eta/ma == F(17,25) > F(5,8))
require("individual_ratio_5_over_8_bound_is_true", eps*delta/ma+ka*eta/ma == F(1,2) < F(5,8))
require("common_maximum_3_over_4_repair_is_true", kappa*delta+ka*eta/ma < F(3,4))

# Independent determinant coefficient expansion and its interpolation matrix.
def d2(m):
    return m[0][0]*m[1][1]-m[0][1]*m[1][0]
def d3(m):
    return sum((-1)**j*m[0][j]*d2([[m[1][k] for k in range(3) if k != j],
                                 [m[2][k] for k in range(3) if k != j]]) for j in range(3))
roots = [F(-17,5),F(0),F(1,10**15)]
V = [[1,z,z*z] for z in roots]
require("three_distinct_height_interpolation_is_invertible", d3(V) == (roots[1]-roots[0])*(roots[2]-roots[0])*(roots[2]-roots[1]) != 0)
for entries in product((F(-1),F(0),F(2)), repeat=8):
    a=[entries[:2],entries[2:4]];b=[entries[4:6],entries[6:]]
    mixed=a[0][0]*b[1][1]+b[0][0]*a[1][1]-a[0][1]*b[1][0]-b[0][1]*a[1][0]
    for z in (F(-3,7),F(0),F(5,2)):
        m=[[a[i][j]+z*b[i][j] for j in range(2)] for i in range(2)]
        require("independent_quadratic_coefficient_grid", d2(m)==d2(a)+z*mixed+z*z*d2(b))
        require("sweep_block_determinant", d3([m[0]+[F(7)],m[1]+[F(-2)],[F(0),F(0),F(1)]])==d2(m))

# Height parameter derivatives are solved from the plane equation directly.
for nx,ny,nz,z,u1,u2,v1,v2 in product((-1,1),repeat=8):
    direct=F(-nx*u1-ny*u2, nz)-F(z*(nx*v1+ny*v2), nz)
    compact=-F(nx*(u1+z*v1)+ny*(u2+z*v2),nz)
    require("planar_intersection_variation", direct==compact)

# The two-contact example really has two supporting halfspace inequalities.
for s,t,z in product((F(-1,2),F(0),F(1,2)),(F(-2,3),F(1,3)),(F(0),F(1))):
    x,y=z*t,(1-z)*s
    require("two_rectangle_support_planes_contain_line", x-t*z==0 and y+s*(z-1)==0)
require("two_contacts_sweep_positive_volume",4*(F(1,2)-F(1,3))==F(2,3)>0)
require("two_contact_roots_do_not_force_zero",F(1,2)*(F(1,2)-1)!=0)
print(json.dumps({"status":"PASS_INDEPENDENT_FINITE_CONTROLS","checks":sum(counts.values()),"categories":counts,"scope":"Exact rational adversarial diagnostics only, not a universal-proof oracle."},indent=2,sort_keys=True))
