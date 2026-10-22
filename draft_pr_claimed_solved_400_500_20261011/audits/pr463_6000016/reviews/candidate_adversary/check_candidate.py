#!/usr/bin/env python3
"""Read-only exact candidate controls; analytic universal and priority steps are prose."""
import hashlib,json,subprocess,sys
from pathlib import Path
import sympy as s
here=Path(__file__).resolve().parent
root=here.parent.parent
snapshot=root/'source_snapshot'
author=snapshot/'unsolved_math_prioritization/attempts/6000016'
checks=[]
def require(name,condition):
    if not condition:raise RuntimeError(name)
    checks.append(name)
def eq(name,actual,expected):
    r=actual-expected
    entries=list(r) if isinstance(r,s.MatrixBase) else [r]
    require(name,all(s.simplify(e)==0 for e in entries))
receipt=json.loads((root/'SOURCE_RECEIPT.json').read_bytes())
require('eligible_frozen_head',receipt['head_sha']=='982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649')
require('exact_claimed_solved_gate',receipt['scope_gate']=='exact claimed_solved')
require('14_frozen_records',len(receipt['files'])==14)
for e in receipt['files']:
    data=(snapshot/e['path']).read_bytes()
    require('source_size_'+e['path'],len(data)==e['bytes'])
    require('source_hash_'+e['path'],hashlib.sha256(data).hexdigest()==e['sha256'])
for mode in [[],['-O']]:
    label='optimized' if mode else 'normal'
    for script,output,extra,countfield,count in [
      ('check_exact.py','exact_results.json',[],'exact_identity_count',41),
      ('audit/check_audit.py','audit/audit_results.json',['--author-dir',str(author)],'audit_control_count',61)]:
        result=subprocess.run([sys.executable,*mode,str(author/script),*extra],cwd=here/'private_cases',capture_output=True,check=True)
        require(label+'_historical_byte_exact_'+script,result.stdout==(author/output).read_bytes())
        parsed=json.loads(result.stdout)
        require(label+'_historical_count_'+script,type(parsed[countfield]) is int and parsed[countfield]==count)
        require(label+'_historical_named_controls_'+script,len(parsed['checks'])==count and len(set(parsed['checks']))==count)
        require(label+'_historical_pass_'+script,parsed['status']=='PASS')
x,y,u,v,t=s.symbols('x y u v t',real=True)
a,b,c=s.symbols('a b c',real=True)
A,B,C=[s.Function(z)(x,y) for z in ('A','B','C')]
K=s.Matrix([[0,0],[t,0]])
G=s.Matrix([[A,B],[B,C]])
dxG=G.diff(x)-K.T*G-G*K
dyG=G.diff(y)
eq('arbitrary_metric_obstruction',dxG[1,0]-dyG[0,0],B.diff(x)-A.diff(y)-t*C)
eq('arbitrary_metric_second_Codazzi',dxG[1,1]-dyG[0,1],C.diff(x)-B.diff(y))
S=s.eye(2)+K
H=s.Matrix([[a,b],[b,c]])
eq('shear_parallel_metric_offdiagonal',((S.T*H*S)-H)[0,1],t*c)
eq('inverse_shear_parallel_metric_offdiagonal',((S.inv().T*H*S.inv())-H)[0,1],-t*c)
eq('constant_averaged_metric_obstruction',(-K.T*H-H*K)[1,0],-t*c)
eq('parallel_volume_trace',s.trace(K),0)
F=s.Matrix([x,y+t*x*x/2]);J=F.jacobian((x,y))
cover=J.T*J
eq('positive_cover_det',cover.det(),1)
eq('positive_cover_fails_descent',cover[0,1].subs(x,x+1)-cover[0,1],t)
Q=s.Matrix([[0,1],[1,0]])
Qd=-K.T*Q-Q*K
eq('indefinite_first_Codazzi',Qd[1,0],0)
eq('indefinite_second_Codazzi',Qd[1,1],0)
eq('indefinite_negative_det',Q.det(),-1)
phi=u*v-t*u**3/3
qh=s.hessian(phi,(u,v)).subs({u:F[0],v:F[1]},simultaneous=True)
eq('indefinite_potential_pullback',J.T*qh*J,Q)
eps=s.symbols('eps',positive=True)
potential=(x*x+y*y)/2-eps*s.cos(2*s.pi*x)/(4*s.pi**2)
nonparallel=s.diag(1+eps*s.cos(2*s.pi*x),1)
eq('given_metric_countercontrol_hessian',s.hessian(potential,(x,y)),nonparallel)
eq('given_metric_countercontrol_nonparallel',nonparallel.diff(x)[0,0],-2*s.pi*eps*s.sin(2*s.pi*x))
require('given_metric_countercontrol_derivative_not_identically_zero',s.simplify(nonparallel.diff(x)[0,0])!=0)
# c0>0 and det(Hessian(phi))=c0 imply determinant one after phi/sqrt(c0).
c0=s.symbols('c0',positive=True)
eq('two_dimensional_Monge_Ampere_rescaling',c0/(s.sqrt(c0)**2),1)
R,r0,t0=s.symbols('R r0 t0',positive=True)
eq('Jorgens_displayed_r_bound_limit',s.limit(24*(r0+t0)**2*r0**2/R**2,R,s.oo),0)
eq('Jorgens_displayed_t_bound_limit',s.limit(24*(r0+t0)**2*t0**2/R**2,R,s.oo),0)
print(json.dumps({'status':'PASS','exact_control_count':len(checks),'checks':checks,'analytic_limitations':'No finite control count proves compact positivity, global Poincare integration, the published PDE theorems, or historical novelty. These are explicitly reviewed in REPORT.md.','original_proof_search_attempts':0},indent=2,sort_keys=True))
