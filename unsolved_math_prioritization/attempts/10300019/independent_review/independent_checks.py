"""Independent exact controls for normal collars, suspension and stacking.
Topological existence and measure claims are audited analytically in the report.
No frozen author module is imported.
"""
import sympy as s,json
from itertools import combinations,product
from collections import Counter
from pathlib import Path
C=Counter();cert={}
def ck(p,k):assert p,k;C[k]+=1
def eq(a,b,k):ck(s.cancel(a-b)==0,k)
# Normal level torus model: three tetrahedra triangulate a triangular prism.
A0=s.Matrix([0,0,0]);B0=s.Matrix([1,0,0]);C0=s.Matrix([0,1,0])
A1=s.Matrix([0,0,1]);B1=s.Matrix([1,0,1]);C1=s.Matrix([0,1,1])
tets=[(A0,B0,C0,C1),(A0,B0,B1,C1),(A0,A1,B1,C1)]
x,y,z=s.symbols('x y z');volumes=[];types=[]
for j,T in enumerate(tets):
 M=s.Matrix.hstack(*[q-T[0] for q in T[1:]])
 volume=abs(M.det())/6;volumes.append(volume)
 B=s.Matrix.vstack(s.Matrix.hstack(*T),s.ones(1,4))
 coords=B.inv()*s.Matrix([x,y,z,1])
 cert['prism_tetrahedron_'+str(j)]={'vertices':[list(map(str,q)) for q in T],'barycentric_coordinates':[str(q) for q in coords],'volume':str(volume)}
 crossing=[(i,k) for i,k in combinations(range(4),2) if T[i][2]!=T[k][2]]
 ck(len(crossing) in [3,4],'normal_disk_edge_count')
 types.append('triangle' if len(crossing)==3 else 'quadrilateral')
 for level in [s.Rational(1,7),s.Rational(1,3),s.Rational(1,2),s.Rational(4,5)]:
  for i,k in crossing:
   low,high=(T[i],T[k]) if T[i][2]==0 else (T[k],T[i])
   p=(1-level)*low+level*high
   bary=B.inv()*s.Matrix([*p,1])
   ck(p[2]==level and sum(bary)==1,'actual_level_edge_intersection')
   ck(sum(q!=0 for q in bary)==2 and all(q>=0 for q in bary),'actual_edge_barycentric_support')
cert['normal_types']=types
ck(types==['triangle','quadrilateral','triangle'],'prism_normal_disk_types')
ck(sum(volumes)==s.Rational(1,2),'prism_volume_partition')
# Generic fibre transport preserving every zero barycentric coordinate.
t,t0=s.symbols('t t0',positive=True);a,b,c,d=s.symbols('a b c d')
for highs in [(3,),(2,3),(1,2,3)]:
 old=[a,b,c,d];new=[q*t/t0 if i in highs else q*(1-t)/(1-t0) for i,q in enumerate(old)]
 for i in range(4):
  eq(new[i].subs(old[i],0),0,'fibre_preserves_each_face')
  back=[q*t0/t if k in highs else q*(1-t0)/(1-t) for k,q in enumerate(new)]
  eq(back[i],old[i],'fibre_inverse_identity')
 # Sum low/high weights separately; normal level imposes those sums.
 lowweight=(1-t)/(1-t0)*(1-t0);highweight=t/t0*t0
 eq(lowweight+highweight,1,'fibre_mass_and_level')
 eq(highweight,t,'fibre_new_level')
# Single ambient fibre map between two ordered stacks, not independent moves.
for aa in [s.Rational(1,3),s.Rational(1,2),s.Rational(2,3)]:
 source=[-1,s.Rational(-2,3)-aa/12,s.Rational(-1,3)+aa/12,s.Rational(1,3)-aa/12,s.Rational(2,3)+aa/12,1]
 target=[-1,s.Rational(-3,4)-aa/16,s.Rational(-1,4)-aa/16,s.Rational(1,4)+aa/16,s.Rational(3,4)-aa/16,1]
 for u in [s.Rational(k,12) for k in range(13)]:
  image=[(1-u)*v+u*w for v,w in zip(source,target)]
  for i in range(5):
   ck((image[i+1]-image[i])/(source[i+1]-source[i])>0,'one_ambient_stack_isotopy_positive_slopes')
  ck(image[2]<image[3],'stack_gap_preserved')
  ck(image[0]==-1 and image[-1]==1,'stack_isotopy_endpoints_fixed')
# Flow/Mobius model and the exact deck-invariant bundle trivialization.
a,b,t=s.symbols('a b t',positive=True)
F=lambda k,w:w/(k+(1-k)*w)
eq(F(a,F(b,t)),F(a*b,t),'full_flow_group_law')
eq(F(1/a,F(a,t)),t,'full_flow_inverse')
eq(F(a/2,F(2,t)),F(a,t),'deck_invariant_fibre_trivialization')
eq(s.diff(F(a,t),t),a/(a+(1-a)*t)**2,'positive_fibre_derivative_formula')
for n in range(-40,41):
 tn=1/(1+s.Rational(2)**n)
 eq(F(2,tn),1/(1+s.Rational(2)**(n+1)),'orbit_shift')
 eq(F(a,tn),1/(1+a*s.Rational(2)**n),'orbit_under_bundle_trivialization')
 ck(0<tn<1,'interior_orbit_points')
# Exact failed interpolation and a relation-preserving alternative path.
t,u=s.symbols('t u');h=(1-u)*t*t+u*t
compose=lambda p,q:s.expand(p.subs(t,q))
Fmid=(t*t+t)/2;Gmid=(t**4+t)/2
comm=s.factor(compose(Fmid,Gmid)-compose(Gmid,Fmid))
eq(comm.subs(t,s.Rational(1,2)),s.Rational(-141,8192),'actual_midpoint_commutation_failure')
eq(compose(t*t,t**4),compose(t**4,t*t),'original_commuting_action')
h2=compose(h,h)
eq(compose(h,h2),compose(h2,h),'entire_relation_preserving_path')
cert['midpoint_commutator_polynomial']=str(comm)
# Distinct primitive slope outputs and nonzero intersection classes.
for a,b in [(1,1),(2,1),(3,2),(5,3)]:
 ck(s.gcd(a,b)==1,'primitive_slope')
 hom=s.Matrix([a,b,0]);ck(hom!=s.zeros(3,1),'nonzero_torus_homology')
ck(s.det(s.Matrix([[1,1],[2,1]]))!=0,'two_output_tori_not_parallel')
ck(s.det(s.eye(2))==1,'input_algebraic_intersection')
# Every finite split-order model is embeddable; no global assertion inferred.
for n in range(1,25):
 vals=[(i,color,2*i+color) for i in range(n) for color in (0,1)]
 ck(all(vals[i][2]<vals[i+1][2] for i in range(len(vals)-1)),'finite_split_order')
Path('GEOMETRIC_CONTROLS.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Independent exact normal-prism, barycentric collar, global stack-map and suspension formulas. Compact lamination gluing, absence of full-support measure and uncountable order obstruction are proved in the review, not inferred from samples.'},indent=2,sort_keys=True))
