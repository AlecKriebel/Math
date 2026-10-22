#!/usr/bin/env python3
"""Exact sphere/plane controls; no configuration-space search or holding certificate."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as sp
N=0;families={}
def ck(v,f):
 global N
 assert bool(v),f
 N+=1;families[f]=families.get(f,0)+1
R=sp.Rational
# The diagnostic begins with an admissible outer ring, and its smaller ring escapes.
r=R(1,5);outer=sp.S(1);inner=outer-r;z0=sp.sqrt(11)/5;z1=R(3,5)
ck(outer**2+z0**2==(1+r)**2,'outer_initial_admissibility')
ck(inner**2+z0**2==R(27,25)>1,'inner_initial_clearance')
ck(inner**2+z1**2==1,'inner_contact_at_turnaround')
ck(outer**2+z1**2==R(34,25)<(1+r)**2,'radial_lift_failure')
ck(z0<1+r and z0<1,'initial_disks_attached')
for j in range(41):
 t=R(j,40)
 z=z0+2*t*(z1-z0) if t<=R(1,2) else z1+(2*t-1)*(2-z1)
 ck(sp.simplify(z-z1)>=0,'inner_path_height')
 ck(sp.simplify(inner**2+z*z-1)>=0,'inner_path_no_collision')
ck(2>1+r,'both_final_disks_disjoint')
# Actual outer-ring escape: go directly upward instead of lifting the detour.
for j in range(21):
 z=z0+R(j,20)*(2-z0)
 ck(sp.simplify(outer**2+z*z-(1+r)**2)>=0,'outer_direct_escape')
# An outer-attached ring whose plane misses the core; normal escape applies.
z=R(11,10);rad=R(1,2)
ck(z>1 and z<1+r,'outside_core_plane')
ck(rad*rad+z*z>(1+r)**2,'outside_core_ring_admissible')
for t in [R(j,10) for j in range(21)]:
 ck((z+t)**2>=z*z,'normal_away_distance_monotone')
# Exact algebraic controls on the concentric smaller-disk necessary condition.
for rr in (R(1,5),R(1,2),sp.S(1)):
 for zz in (sp.S(0),R(3,5),R(4,5),R(9,10)):
  section=sp.sqrt(1-zz*zz);parallel=sp.sqrt((1+rr)**2-zz*zz)
  for lateral in (sp.S(0),R(1,3),sp.S(2)):
   outer_radius=lateral+parallel
   ck(sp.simplify(outer_radius-rr-lateral-section)>=0,'smaller_section_disk')
   ck(outer_radius>rr,'positive_smaller_radius')
# A specified positive-clearance path stays valid for a definite thickening.
for j in range(31):
 z=R(4,5)+R(j,30)*(2-R(4,5))
 ck(1+z*z>(1+r)**2,'positive_clearance_certificate')
# Polynomial forms underlying normal translation and the parallel support shift.
a,b,t=sp.symbols('a b t',real=True)
ck(sp.expand((a+t)**2-a*a-(2*a*t+t*t))==0,'normal_translation_identity')
h,shift=sp.symbols('h shift',real=True)
ck(sp.expand((b-(h+shift))-((b-h)-shift))==0,'support_shift_identity')
# Exact unit-sphere signed clearance identity at selected radial coordinates.
for norm in (R(1,4),sp.S(1),R(7,5),sp.S(3)):
 ck((norm-(1+r))==(norm-1)-r,'sphere_signed_clearance_shift')
root=Path(__file__).resolve().parent
out={'problem_id':30001883,'artifact_sha256':hashlib.sha256((root/'OBSTRUCTION.md').read_bytes()).hexdigest(),
 'exact_assertions':N,'families':families,'status':'PASS',
 'counterexample_to_original_question':False,'global_escape_claim_certified_by_finite_computation':False,
 'scope':'Finite exact diagnostics for the written clearance lemmas and a failed radial-path lift; both diagnostic bodies are balls.'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
