from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import physical_ray_audit as ray
mp=ray.mp;B=Path(__file__).parent
# Explicitly probe a nonprimitive padded-list interpretation of the source row.
mp.mp.dps=110
rows=[]
a,b=mp.mpf('1.5'),mp.mpf(1);lam=ray.closure_lam(a,b,6,1)
for t in ('0','0.31','0.79'):
 V,D,w=ray.trace(a,b,lam,6,mp.mpf(t));P=V[:-1];F=(mp.sqrt(a*a-b*b),0)
 AP,AS,_=ray.areas(P,F);AP12,AS12,_=ray.areas(P+P,F)
 assert abs(AP12-2*AP)<mp.mpf('1e-60') and abs(AS12-2*AS)<mp.mpf('1e-60')
 rows.append({'phase':t,'primitive_N6_product':str(AP*AS),'repeated_N12_product':str(AP12*AS12)})
assert abs(mp.mpf(rows[0]['repeated_N12_product'])-mp.mpf(rows[1]['repeated_N12_product']))>mp.mpf('1e-10')
# Locate a zero antipedal area in the actual primitive N8 family.
# Numeric root evidence, not interval certification or an exact zero proof.
def anti_axis(a):
 lam=ray.closure_lam(a,b,8,1);P=ray.trace(a,b,lam,8)[0][:-1]
 return ray.areas(P,(mp.sqrt(a*a-1),mp.mpf(0)))[1]
a0=mp.findroot(anti_axis,(mp.mpf('1.5'),mp.mpf('2')),solver='secant',tol=mp.mpf('1e-55'))
lam0=ray.closure_lam(a0,b,8,1)
zero_rows=[ray.diagnose(a0,b,lam0,8,1,mp.mpf(t)) for t in ('0','0.31','0.79','1.19')]
# Traversal reversal, Euclidean translation, and length scaling controls.
a,b=mp.mpf(2),mp.mpf(1);lam=ray.closure_lam(a,b,8,3);P=ray.trace(a,b,lam,8,mp.mpf('.31'))[0][:-1];F=(mp.sqrt(3),0)
AP,AS,_=ray.areas(P,F);Ar,Br,_=ray.areas(list(reversed(P)),F)
assert abs(Ar+AP)<mp.mpf('1e-55') and abs(Br+AS)<mp.mpf('1e-55')
scale=mp.mpf('1.4');trans=(mp.mpf('3.1'),mp.mpf('-1.7'))
PP=[ray.add(ray.mul(scale,p),trans) for p in P];FF=ray.add(ray.mul(scale,F),trans);At,Bt,_=ray.areas(PP,FF)
assert abs(At*Bt-scale**4*AP*AS)<mp.mpf('1e-50')
out={'scope':'Numerical strict elliptical-caustic primitive/padded-list distinction and zero/sign/rigid transformation controls','dps':mp.mp.dps,'padded_N12_from_N6':{'a':'1.5','b':'1','lambda':str(ray.closure_lam(mp.mpf('1.5'),mp.mpf(1),6,1)),'rows':rows},'zero_primitive_N8':{'a':str(a0),'b':'1','lambda':str(lam0),'rows':zero_rows,'limitation':'Non-interval numerical root; tests vicinity of zero product without asserting exact algebraic root'},'reversal_residual':str(max(abs(Ar+AP),abs(Br+AS))),'scaling_translation_residual':str(abs(At*Bt-scale**4*AP*AS))}
(B/'BOUNDARY_DIAGNOSTICS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
