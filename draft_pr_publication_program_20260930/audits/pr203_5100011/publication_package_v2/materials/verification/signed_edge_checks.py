"""Supplement to physical_audit: fixed zero/negative pedal points across phase."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
import physical_audit as p
mp=p.mp
rows=[]
a=mp.mpf(2);b=mp.mpf(1)
for N,w in [(8,3),(12,5)]:
    lam=p.find_lambda(a,b,N,w)
    pts=p.orbit(a,b,lam,mp.mpf('0.217'),N)[0][:-1]
    B0=p.pedal(pts,(0,0));B1=p.pedal(pts,(a,b));Bm=p.pedal(pts,(-a,-b));q=(B1+Bm)/2-B0
    root=mp.sqrt(-B0/q);Mzero=(root*a,root*b);Mnegative=(2*root*a,2*root*b)
    ref=p.area(pts)*p.pedal(pts,Mnegative)
    for phase in [mp.mpf(t) for t in ['0','0.173','0.731','1.417']]:
        pts=p.orbit(a,b,lam,phase,N)[0][:-1];A=p.area(pts)
        p.near('fixed_zero_M_all_phases',p.pedal(pts,Mzero),abs(B0))
        Bnegative=p.pedal(pts,Mnegative)
        p.require('fixed_negative_M_all_phases',Bnegative<0)
        p.near('fixed_negative_M_invariant',A*Bnegative-ref,abs(ref))
        p.near('odd_repeat_product',p.area(pts*3)*p.pedal(pts*3,Mnegative)-9*A*Bnegative,abs(ref))
        # Coefficients of the quadratic pedal area, independently recovered by six-point interpolation.
        samples=[p.pedal(pts,M) for M in [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1)]]
        c=samples[0];lx=(samples[1]-samples[2])/2;ly=(samples[3]-samples[4])/2
        xx=(samples[1]+samples[2])/2-c;yy=(samples[3]+samples[4])/2-c;xy=samples[5]-c-lx-ly-xx-yy
        coefficients=[A*z for z in [c,lx,ly,xx,xy,yy]]
        if phase==0:reference=coefficients
        for got,want in zip(coefficients,reference):p.near('all_M_coefficients',got-want,max(1,abs(want)))
    rows.append({'N':N,'w':w,'Mzero':[mp.nstr(t,35) for t in Mzero],'Mnegative':[mp.nstr(t,35) for t in Mnegative],'negative_AB':mp.nstr(ref,35)})
result={'utc':datetime.now(timezone.utc).isoformat(),'optimized':sys.flags.optimize,'counts':p.COUNTS,'max_relative_residuals':{k:mp.nstr(v,14) for k,v in p.MAX.items()},'rows':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'physical_audit_sha256':hashlib.sha256(Path(p.__file__).read_bytes()).hexdigest()}
label='optimized' if sys.flags.optimize else 'ordinary'
(Path(__file__).parent/f'signed_edges_{label}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':sum(p.COUNTS.values()),'optimized':sys.flags.optimize,'counts':p.COUNTS}))
