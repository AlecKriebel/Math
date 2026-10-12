"""Compare direct reflection data with Stachel canonical parametrization and both focal feet."""
from pathlib import Path
import json,mpmath as mp
mp.mp.dps=100
from independent_billiard import sub,dot,foot,tfoot,n_at
root=Path(__file__).resolve().parent
rows=json.loads((root/'independent_billiard_results.json').read_text())['results']
checks=[]
for row in rows:
 a=mp.mpf(row['a']);b=mp.mpf(row['b']);lam=mp.mpf(row['lambda']);alpha=mp.sqrt(a*a-lam);beta=mp.sqrt(b*b-lam);k=mp.sqrt(a*a-b*b)/alpha;kp=beta/alpha;mod=k*k;N=row['N'];tau=row['winding'];K=mp.ellipk(mod);v=2*K*tau/N;delta=2*v
 sn=mp.ellipfun('sn');cn=mp.ellipfun('cn');dn=mp.ellipfun('dn');ascaled=a/alpha;bscaled=b/alpha
 vertices=[tuple(mp.mpf(x) for x in p) for p in row['vertices']]
 x,y=vertices[0][0]/a,vertices[0][1]/b;phi=mp.atan2(-x,y);u0=mp.ellipf(phi,mod)
 worst={'axis_formula':max(abs(ascaled-dn(v,mod)/cn(v,mod)),abs(bscaled-kp/cn(v,mod))),'vertex_formula':mp.mpf(0),'contact_chord_incidence':mp.mpf(0),'chord_foot_formula':mp.mpf(0),'outer_foot_formula':mp.mpf(0)}
 for i in range(N):
  u=u0+i*delta;ucontact=u+v;s=sn(u,mod);ct=cn(u,mod);sc=sn(ucontact,mod);cc=cn(ucontact,mod)
  p=(-a*s,b*ct);raw=vertices[i];worst['vertex_formula']=max(worst['vertex_formula'],mp.sqrt(dot(sub(p,raw),sub(p,raw))))
  n=(-sc/alpha,cc/beta)
  for rawend in [vertices[i],vertices[(i+1)%N]]:worst['contact_chord_incidence']=max(worst['contact_chord_incidence'],abs(dot(n,rawend)-1))
  f=(k*alpha,mp.mpf(0));q=foot(f,vertices[i],vertices[(i+1)%N]);qpred=(alpha*(k-sc)/(1-k*sc),alpha*kp*cc/(1-k*sc));Q=tfoot(f,n_at(raw,a,b));Qpred=(alpha*ascaled*(k-ascaled*s)/(ascaled-k*s),alpha*ascaled*bscaled*ct/(ascaled-k*s))
  worst['chord_foot_formula']=max(worst['chord_foot_formula'],mp.sqrt(dot(sub(q,qpred),sub(q,qpred))))
  worst['outer_foot_formula']=max(worst['outer_foot_formula'],mp.sqrt(dot(sub(Q,Qpred),sub(Q,Qpred))))
 checks.append({'a':row['a'],'N':N,'tau':tau,'r':row['r_phase'],'max_checks':{k:mp.nstr(x,85) for k,x in worst.items()}})
result={'evidence':'Finite NONINTERVAL high precision100dps; 85-digit stored input causes conditioning loss near degenerate caustics','rows':len(checks),'global_maxima':{k:mp.nstr(max(mp.mpf(row['max_checks'][k]) for row in checks),85) for k in checks[0]['max_checks']},'checks':checks}
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2));(root/'canonical_vs_direct_results.json').write_text(json.dumps(result,indent=2)+'\n')
