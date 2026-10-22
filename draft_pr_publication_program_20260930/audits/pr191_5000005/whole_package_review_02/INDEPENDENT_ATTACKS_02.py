"""Reviewer attacks: actual first-hit tracers used only as geometric oracles.
Small exact counterexamples reject wrong science; these do not prove universality.
"""
from pathlib import Path
from fractions import Fraction
import json,runpy
D=Path(__file__).resolve().parent
P=runpy.run_path(str(D/'private/extracted/verification-package/checks/pentagon_geometry.py'))
H=runpy.run_path(str(D/'private/extracted/verification-package/checks/reflection_geometry.py'))
def need(ok,message):
 if not ok: raise RuntimeError(message)
records=[]
k,q,j=P['trace'](P['P'][2]); kp,qp,jp=P['trace'](P['rotate_small'](P['P'][2],1))
need((k,q,j,kp,qp,jp)==(1,1,2,0,1,1),'independent direct pentagon oracle')
need(kp!=(k+1)%3,'wrong ell sign must fail')
records.append({'attack':'replace -ell by +ell','n':5,'base_vertex':2,'ell':1,'epsilon':1,'actual_type':kp,'wrong_type':(k+1)%3,'all_hits_one_segment':q==qp==1})
v=P['reflection'](P['P'][2],P['e0']);v=P['rotate_small'](v,3)
kr,qr,jr=P['trace'](v)
need((kr,qr,jr)==(2,1,3),'reflected pentagon oracle')
need(kr!=(k-3)%3,'wrong epsilon sign must fail')
records.append({'attack':'replace epsilon*k by -epsilon*k','n':5,'base_vertex':2,'ell':3,'epsilon':-1,'actual_type':kr,'wrong_type':(k-3)%3})
kh,qh,jh=H['trace'](6,H['polygon'](6)[2]);wrong=(5-(3+1)//2)%4
need((kh,qh,jh)==(1,1,2) and wrong!=kh,'terminal supplement must fail')
records.append({'attack':'replace beta by pi-beta','n':6,'base_vertex':2,'actual_alpha_units':3,'actual_beta_units':5,'wrong_beta_units':1,'actual_type':kh,'wrong_type':wrong})
need(P['inward'](P['rotate_small'](P['P'][2],10)) and not P['unwrapped'](P['P'][2],10,1),'angle wrap must be rejected')
records.append({'attack':'admit alpha+2pi by direction reduction','n':5,'ell':10,'epsilon':1,'same_physical_ray':True,'literal_angle_admitted':False})
need(not H['admissible'](6,H['polygon'](6)[2],1),'even odd ell forbidden')
records.append({'attack':'remove even-ell restriction','n':6,'ell':1,'admitted':False})
# Bare type-zero obstruction uses source angles and no intrinsic endpoint labels.
for n in range(5,1001):
 N=n-2; a=Fraction(1); b=Fraction(3); ell=2; eps=-1
 need(a==ell+eps*a and b-a==2 and (-2)%N!=0,'bare shorthand obstruction')
records.append({'attack':'force direct-diagonal bare A0 globally','n_range':[5,1000],'family':'alpha=rho,beta=3rho,ell=2,epsilon=-1 fixes ray but demands -2 != 0 mod n-2'})
result={'status':'PASS','all_six_wrong_science_attacks_rejected':True,'records':records,'limits':'Geometric tracers are supplied checks inspected by reviewer, not a second independently implemented tracer. These small exact attacks are finite controls; analytic reasoning is in REVIEW_02.md.'}
(D/'INDEPENDENT_ATTACKS_02.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
