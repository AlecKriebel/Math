from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import physical_ray_audit as ray
mp=ray.mp;B=Path(__file__).parent;mp.mp.dps=110
inp=json.loads((B/'PHYSICAL_RAY_RECEIPT.json').read_text());rows=[]
for case in inp['cases']:
 a,b,lam=map(mp.mpf,(case['a'],case['b'],case['lambda']));N,tau=case['N'],case['winding']
 alpha=mp.sqrt(a*a-lam);k2=(a*a-b*b)/(a*a-lam);K=mp.ellipk(k2);v=2*K*tau/N;delta=2*v
 sn=lambda x:mp.ellipfun('sn',x,k2);cn=lambda x:mp.ellipfun('cn',x,k2);dn=lambda x:mp.ellipfun('dn',x,k2)
 axes=max(abs(alpha*dn(v)/cn(v)-a),abs(alpha*mp.sqrt(1-k2)/cn(v)-b))/a
 theta=mp.mpf('.31');w=mp.ellipf(theta-mp.pi/2,k2);P=ray.trace(a,b,lam,N,theta)[0][:-1]
 vertices=max(ray.norm(ray.sub(p,(-a*sn(w+j*delta),b*cn(w+j*delta))))/a for j,p in enumerate(P))
 assert axes<mp.mpf('1e-60') and vertices<mp.mpf('1e-60')
 rows.append({'a':case['a'],'N':N,'winding':tau,'physical_to_canonical_k2':str(k2),'axis_formula_residual':str(axes),'all_vertices_residual':str(vertices)})
out={'scope':'Cross-check of canonical Stachel/Jacobi axes and all vertices against independent physically root-closed Cartesian trajectories. Added after independent construction completed and submitted scripts exposed.','dps':110,'rows':rows}
(B/'CANONICAL_BRIDGE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
