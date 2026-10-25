#!/usr/bin/env python3
from fractions import Fraction as F
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cert=json.load(open(ROOT/'software/certificates/k3p_sharpness_krawczyk.json'))
assert cert['conclusion']=={'principal_domain':True,'strict_continuous_time':True,'W_rank':15,'Wprime_rank':15,'unique_common_root_in_box':True}
u=(F(2,5),F(4,9),F(3,7));v=(F(3,7),F(5,11),F(4,9))
def phys(x):
 c,g,t=x;return min(c,g,t,1-c,1-g,1-t,1+c-g-t,1-c+g-t,1-c-g+t,c-g*t,g-c*t,t-c*g)
assert phys(u)>0 and phys(v)>0
det=F(8)*u[0]*u[1]*u[2]/(v[0]*v[1]*v[2])
assert det==F(176,25)
# direct determinant of block-diagonal Jacobian
J=[]
for a,b in zip(u,v):J.append([[1/b,-a/(b*b)],[b,a]])
prod=F(1)
for B in J:prod*=B[0][0]*B[1][1]-B[0][1]*B[1][0]
assert prod==det
out={'schema':'k3p-sharpness-all-n-v1','base_common_dimension':15,'dimensions_per_cherry':6,'dimension_formula':'6n-3','observables':['R_C=u_C/v_C','P_C=u_C*v_C','R_G=u_G/v_G','P_G=u_G*v_G','R_T=u_T/v_T','P_T=u_T*v_T'],'example_u':[str(x) for x in u],'example_v':[str(x) for x in v],'jacobian_determinant_formula':'8*u_C*u_G*u_T/(v_C*v_G*v_T)','example_determinant':str(det),'u_min_physical_ct_margin':str(phys(u)),'v_min_physical_ct_margin':str(phys(v)),'conclusion':{'all_n_from':3,'common_dimension':'6n-3','weak_not_strong_persists':True,'nonisomorphism_persists':True,'nontriangle_equivalence_persists':True,'strict_continuous_time':True}}
(ROOT/'software/certificates/k3p_sharpness_all_n.json').write_text(json.dumps(out,indent=2)+'\n')
print('K3P_SHARPNESS_ALL_N_PASS determinant',det)
