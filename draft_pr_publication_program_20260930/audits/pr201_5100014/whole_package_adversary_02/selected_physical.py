"""Selected signed/star/boundary diagnostics, no full historical sweep."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys
f=Path(__file__).resolve().parent.parent/'publication_package_v2/materials/verification/physical_phase_checks.py'
spec=importlib.util.spec_from_file_location('read_only_physical',f);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
records=[]
for a,N,k in [('2',10,3),('1.0001',14,5),('5',22,9)]:
    r,pars=p.case(a,N,k);records.append(r)
r,pars=p.case('2',6,2,False)
p.need(max(map(p.mp.mpf,r['relative_phase_spread_by_M']))>p.mp.mpf('1e-10'),'excluded repeated triangle must fail');repeated=r
a,b,lam=p.mp.mpf(2),p.mp.mpf(1),p.root_caustic(p.mp.mpf(2),p.mp.mpf(1),10,3)
V,_,_=p.orbit(a,b,lam,10,p.mp.mpf('.173'));ap,B0,_,_=p.derived(V,a,b,(0,0));_,B1,_,_=p.derived(V,a,b,(1,0));coef=B1-B0
p.need(B0>0 and coef<0,'signed star zero coefficient signs');radius=p.mp.sqrt(-B0/coef);zs=[]
for phase in ('.173','.719','1.37'):
    V,_,_=p.orbit(a,b,lam,10,p.mp.mpf(phase))
    outer,zero,_,_=p.derived(V,a,b,(radius,0));_,below,_,_=p.derived(V,a,b,(radius*p.mp.mpf('.99'),0));_,above,_,_=p.derived(V,a,b,(radius*p.mp.mpf('1.01'),0))
    p.need(abs(zero)<p.mp.mpf('1e-45') and below>0 and above<0,'signed zero crossing')
    rp,rb,_,_=p.derived(V[::-1],a,b,(radius*p.mp.mpf('1.01'),0));p.need(abs(rp+outer)<p.mp.mpf('1e-45') and abs(rb+above)<p.mp.mpf('1e-45'),'signed physical reversal')
    zs.append({'phase':phase,'zero':p.textnum(zero),'below':p.textnum(below),'above':p.textnum(above)})
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','optimization':sys.flags.optimize,'target_selected':records,'excluded_twice_triangle':repeated,'zero_radius':p.textnum(radius),'signed_zero_samples':zs,'scope':'Selected noninterval physical diagnostics only, not universal proof.'},indent=2))
