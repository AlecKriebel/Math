"""Small exact controls, not a proof of the imported reflection theorem."""
from pathlib import Path
import sympy as s
import os,json
from datetime import datetime,timezone
F=Path(__file__).resolve().parent
x,y,t,r,c,a,u=s.symbols('x y t r c a u',real=True)
z=x+s.I*y; f=(1+z)/2
phi=s.factor((1-x*x-y*y)*s.Rational(1,2)/(1-s.expand(f*s.conjugate(f))))
checks=[]
def eq(name,v,w):
    assert s.simplify(v-w)==0,(name,v,w)
    checks.append({'name':name,'observed':str(v),'expected':str(w),'passed':True})
eq('affine exact distortion',phi,2*(1-x*x-y*y)/(4-(1+x)**2-y*y))
eq('affine radial limit',s.limit(phi.subs({x:1-t,y:0}),t,0,dir='+'),1)
eq('affine fixed slope nontangential limit',s.limit(phi.subs({x:1-t,y:c*t}),t,0,dir='+'),1)
eq('tangential path disk deficit',s.expand(1-(1-t*t)**2-t*t),t*t*(1-t*t))
eq('affine tangential limit differs',s.limit(phi.subs({x:1-t*t,y:t}),t,0,dir='+'),s.Rational(2,3))
eq('affine positive angular derivative',s.diff((1+s.Symbol('w'))/2,s.Symbol('w')),s.Rational(1,2))
eq('affine circle image squared',s.simplify(((1+s.exp(s.I*t))/2)*((1+s.exp(-s.I*t))/2)),s.cos(t/2)**2)
eq('square defining-function quotient',s.cancel((1-r**4)/(1-r*r)),1+r*r)
eq('square unrestricted distortion',s.cancel(2*r/(1+r*r)),2*r/(1+r*r))
eq('square boundary derivative',s.diff(s.Symbol('w')**2,s.Symbol('w')).subs(s.Symbol('w'),1),2)
eq('singular family distortion boundary limit',s.limit(a*u/s.sinh(a*u),u,0),1)
eq('singular family arbitrary derivative',s.diff(s.exp(-a*(1-s.Symbol('w'))/(1+s.Symbol('w'))),s.Symbol('w')).subs(s.Symbol('w'),1),a/2)
eq('Hopf logarithmic barrier inward coefficient',s.limit(s.log(r/(r-t))/t,t,0,dir='+'),1/r)
q={'schema':'pr49-whole-exact-target-controls/v1','actual_pid':os.getpid(),'created_utc':datetime.now(timezone.utc).isoformat(),'sympy_version':s.__version__,'status':'PASS','cases':checks,'scope':'Exact symbolic identities and limits supporting written universal reasoning; no finite controls certify imported journal proof, topology gate, or future acceptance','new_substantive_attempts':0,'audit_turns':0}
(F/'TARGET_CONTROL_RESULTS.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_pid':os.getpid(),'exact_controls':len(checks)}))
