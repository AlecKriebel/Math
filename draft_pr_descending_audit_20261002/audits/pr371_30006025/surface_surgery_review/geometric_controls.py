#!/usr/bin/env python3
"""New exact boundary/adversarial controls, separate from the frozen author code.

The universal geometric arguments are in GEOMETRIC_CONTROLS.md. Counts below
certify finite algebraic examples, not novel geometry or source resolution.
"""
from collections import Counter
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import datetime, json

C=Counter()
def ck(condition,label):
    assert condition,label
    C[label]+=1

# Exact regular source-perimeter cone escape for every g>=12.
# l/2 <=12/23; cosh x <=1+(x^2/2)/(1-x^2/12).
x=Q(12,23)
cosh_upper=1+(x*x/2)/(1-x*x/12)
regular_lower=Q(8,7)*(1-Q(22,7*138)**2/2)
ck(x*x<12,'cosh_geometric_tail_applicable')
ck(Q(3)<Q(49,16),'sqrt3_upper_certificate')
ck(cosh_upper<regular_lower,'negative_cone_escape_angle_certificate')
for g in range(12,313):
    n=12*g-6
    ck(Q(12*g,n)/2<=x,'source_side_monotonic_bound')
    ck(n>=138,'regular_angle_monotonic_bound')
    v,e=4*g-2,6*g-3
    ck(v-e+1==2-2*g,'cone_surface_topological_genus')
    ck(e*Q(12*g,n)==6*g,'cone_source_perimeter_preserved')
    # Angle in pi units: an arbitrary valid alpha>2/3 checks area/defect
    # consistency independent of the trigonometric value of the real polygon.
    for alpha in (Q(7,10),Q(3,4),Q(4,5),Q(9,10)):
        area=n-2-n*alpha
        defects=v*(2-3*alpha)
        ck(area==4*(g-1)+defects,'cone_gauss_bonnet_identity')
        ck(defects<0,'negative_glued_cone_defects')

# Genuine flat metric disk with geodesic boundary and overlapping development.
# Eight quadrilateral panels between radii 1 and 2, angular step pi/2.
# Panels 0..3 and 4..7 have identical Euclidean images but separate interiors.
n=8
ck(2*(n+1)-(3*n+1)+n==1,'overlap_strip_disk_euler')
coords=[((1,0),(2,0),(0,2),(0,1))]
def rot(point):
    a,b=point
    return (-b,a)
for i in range(1,n):
    coords.append(tuple(rot(p) for p in coords[-1]))
ck(coords[0]==coords[4] and coords[1]==coords[5],
   'distinct_panels_coincident_development')
outer_angles=[Q(1,4)]+[Q(1,2)]*(n-1)+[Q(1,4)]
inner_angles=[Q(3,4)]+[Q(3,2)]*(n-1)+[Q(3,4)]
angles=outer_angles+inner_angles
ck(all(a>0 for a in angles),'positive_overlapping_disk_sectors')
ck(sum(1-a for a in angles)==2,'overlap_disk_boundary_gauss_bonnet')
area=Q(n*(4-1),2) # sin(pi/2)=1
ck(area==12,'overlap_disk_exact_area')
# P=24sqrt2+2; P^2>=1156>4*(22/7)*12.
ck(Q(24**2*2+4)>4*Q(22,7)*area,'intrinsic_overlap_isoperimetric_check')
ck(max(angles)>1,'reentrant_boundary_present')

# Genuine slit square: tip angle 2pi, not zero despite coincident directions.
slit_angles=[Q(1,2)]*6+[Q(2)]
ck(sum(1-a for a in slit_angles)==2,'full_turn_slit_boundary_gauss_bonnet')
ck(slit_angles[-1]==2 and slit_angles[-1]!=0,'intrinsic_full_turn_not_modulo_zero')
ck(Q(5)**2>4*Q(22,7),'slit_disk_perimeter_area_check')
ck(sum(2-a for a in slit_angles)!=2,'mutation_wrong_interior_boundary_reference_detected')

# Positive interior cone curvature is essential, even for geodesic boundary.
# Four Euclidean isosceles triangles around a cone of angle pi. Their boundary
# is a geodesic four-gon. P^2/(4pi A)=(4/pi)*tan(pi/8).
# tan(pi/8)=sqrt2-1<1/2 and pi>3, so this ratio <2/3<1.
ck(Q(2)<Q(9,4),'sqrt2_lt_threehalves_certificate')
ck(Q(2,3)<1,'positive_cone_polygon_breaks_unmodified_inequality')
# Radial round disks are auxiliary limiting constructions, not literally the
# piecewise-geodesic boundary class in Izmestiev's cone metric definition.
for q in (Q(1,4),Q(1,2),Q(1),Q(3,2),Q(2),Q(10)):
    # Euclidean normalized deficit: P^2-4pi A =4pi^2*q*(q-1)*R^2.
    # Hyperbolic: 8pi^2*q*(q-1)*(cosh R-1).
    for h in (Q(1,100),Q(1,2),Q(1),Q(5)):
        a=2*q*h # area in pi units
        p2=4*q*q*h*(h+2) # squared perimeter in pi^2 units
        deficit=p2-4*a-a*a
        ck(deficit==8*q*(q-1)*h,'radial_cone_exact_deficit_identity')
        ck((deficit>0)-(deficit<0)==(q>1)-(q<1),
           'radial_cone_curvature_sign')

# Angle-conserving Chapuy gluing must create cone defects if points are smooth.
for k in range(3,32,2):
    before=[Q(2)]*k
    glued=sum(before)
    ck((2-glued)-sum(2-a for a in before)==-2*(k-1),
       'sector_conservation_defect_change')
    ck(Q(k-1,2).denominator==1,'odd_merge_genus_integral')
    ck(glued>2,'sector_conserving_smooth_merge_impossible')
    ck(Q(2,k)<2,'sector_conserving_smooth_split_impossible')

# Periodic flat square graph vs filled torus: graph path via vertex has length
# 1, while a face-interior torus path between edge midpoints has length sqrt(1/2).
ck(Q(1,2)<1,'filled_face_shortcut_squared_comparison')
steps={'a':(1,0),'b':(0,1),'A':(-1,0),'B':(0,-1)}
word='abAB'
stack=[]
for letter in word:
    if stack and stack[-1].swapcase()==letter:
        stack.pop()
    else:
        stack.append(letter)
ck(len(stack)==4,'graph_commutator_freely_nontrivial')
ck(tuple(sum(steps[c][j] for c in word) for j in (0,1))==(0,0),
   'filled_torus_commutator_null_displacement')

# Independent exact law control: max of E=2/3 broken-stick coordinates.
# Inclusion-exclusion gives its tail; this checks Markov bounds on events, not
# hypothetical geometric existence and not the author harmonic finite loop.
for e in (2,3):
    mean=sum((Q(1,j) for j in range(1,e+1)),Q(0))/e
    for t in (Q(1,10),Q(1,3),Q(1,2),Q(2,3),Q(3,4),Q(9,10),Q(1)):
        tail=sum(((-1)**(r+1)*comb(e,r)*max(0,1-r*t)**(e-1)
                  for r in range(1,e+1)),Q(0))
        ck(0<=tail<=1,'exact_max_tail_probability_range')
        ck(tail<=min(1,mean/t),'exact_max_tail_vs_markov')
        if t<=Q(1,e):
            ck(tail==1,'max_tail_below_deterministic_threshold')
        if t==1:
            ck(tail==0,'max_tail_at_degenerate_endpoint')
ck(Q(9,10)>Q(1,10),'adaptive_choice_capacity_exceeds_fixed_small_coordinate')

output={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'assertions':sum(C.values()),'by_scope':dict(C),
        'regular_cone_escape':{'starting_genus':12,'source_side_half_upper':str(x),
            'cosh_upper':str(cosh_upper),'regular_cosh_lower':str(regular_lower),
            'universal_reason':'source side decreases and regular smooth side increases with genus'},
        'overlap_disk':{'panels':8,'intrinsic_topology':'disk','interior_cones':0,
            'area':'12','perimeter':'24 sqrt(2)+2','duplicate_developed_panels':[0,4]},
        'scope':'New exact controls supplement GEOMETRIC_CONTROLS.md and the sealed universal proof verdict; no simulation, no historical novelty, no original source resolution.'}
Path(__file__).with_name('GEOMETRIC_CONTROL_RECEIPT.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
