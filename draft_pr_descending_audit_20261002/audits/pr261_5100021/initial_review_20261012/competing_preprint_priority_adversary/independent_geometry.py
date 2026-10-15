"""High precision corroboration from geometric constructions, not area formulas.

No imports from either researcher's checkers. Families are generated from
Stachel's canonical parametrization with fixed caustic modulus and period.
This is rounded numerical evidence, not a validated interval proof.
"""
from pathlib import Path
import json, math
import mpmath as mp
mp.mp.dps=80

def det(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def sub(x,y):return tuple(x[i]-y[i] for i in range(2))
def area(poly):return sum(det(p,poly[(i+1)%len(poly)]) for i,p in enumerate(poly))/2
def meet(n,r,m,s):
    den=det(n,m)
    return ((r*m[1]-n[1]*s)/den,(n[0]*s-r*m[0])/den)
def rel(x,y):return abs(x-y)/max(mp.mpf(1),abs(x),abs(y))
def family(N,tau,ktext,phase):
    k=mp.mpf(ktext);m=k*k;kk=mp.ellipk(m);delta=2*tau*kk/N
    sn=lambda u:mp.ellipfun('sn',u,m)
    cn=lambda u:mp.ellipfun('cn',u,m)
    dn=lambda u:mp.ellipfun('dn',u,m)
    ac=1/mp.sqrt(1-m);bc=mp.mpf(1)
    a=ac*dn(delta)/cn(delta);b=bc/cn(delta)
    al=a*a;be=b*b;lam=be-bc*bc;c=mp.sqrt(al-be)
    P=[(-a*sn((phase+mp.mpf(4*i*tau)/N)*kk),b*cn((phase+mp.mpf(4*i*tau)/N)*kk)) for i in range(N)]
    D=al*be;L=D-(al+be)*lam;J=(al-lam)*(be-lam)
    K=mp.sqrt(J)*(be-lam)/be**2
    R=(D*(3*be-al)+lam*(al-be)**2)/(2*D*(be-lam))
    F=(c,mp.mpf(0));ped=[];out=[];anti=[];errs=[];reflection=[]
    ds=[];fs=[];tangency=[]
    for i,p in enumerate(P):
        q=P[(i+1)%N];v=sub(q,p);w=sub(p,F)
        foot=tuple(p[j]-dot(w,v)*v[j]/dot(v,v) for j in range(2));ped.append(foot)
        np=(p[0]/al,p[1]/be);nq=(q[0]/al,q[1]/be)
        out.append(meet(np,1,nq,1))
        u=sub(p,F);vv=sub(q,F);anti.append(meet(u,dot(u,u),vv,dot(vv,vv)))
        ds.append(det(p,q));fs.append(det(u,vv))
        # Chord line normal n has support h, tangency to inner ellipse.
        nn=(-v[1],v[0]);hh=dot(nn,p)
        tangency.append(rel(hh*hh,(al-lam)*nn[0]**2+(be-lam)*nn[1]**2))
        incoming=sub(p,P[(i-1)%N]);incoming=tuple(x/mp.sqrt(dot(incoming,incoming)) for x in incoming)
        outgoing=tuple(x/mp.sqrt(dot(v,v)) for x in v)
        norm=tuple(x/mp.sqrt(dot(np,np)) for x in np)
        reflected=tuple(incoming[j]-2*dot(incoming,norm)*norm[j] for j in range(2))
        reflection.append(max(abs(reflected[j]-outgoing[j]) for j in range(2)))
    A=area(P);T=area(out);p=area(ped);q=area(anti)
    W=[be*(pt[0]/a)**2+al*(pt[1]/b)**2 for pt in P]
    S1=sum(mp.sqrt(w-lam)/w for w in W);S2=sum(mp.sqrt(w-lam)/w**2 for w in W)
    residuals={'p_equals_KT':rel(p,K*T),'q_equals_RA':rel(q,R*A),
               'velocity_telescope':rel(2*D*S2,(al+be)*S1),
               'reflection':max(reflection),'confocal_tangency':max(tangency)}
    if N%4==0:
        residuals['quarter_shift']=max(rel(W[(i+N//4)%N],(lam*w+L)/(w-lam)) for i,w in enumerate(W))
    return {'N':N,'tau':tau,'caustic_modulus':ktext,'phase_over_K':str(phase),
            'a':str(a),'b':str(b),'lambda':str(lam),'A':str(A),'T':str(T),
            'p':str(p),'q':str(q),'AT':str(A*T),'pq':str(p*q),'R':str(R),
            'min_original_edge_det':str(min(ds)),'min_focal_normal_det':str(min(fs)),
            'residuals':{n:str(x) for n,x in residuals.items()}}, A*T,p*q

rows=[];phase_spreads=[]
for N,tau in [(4,1),(8,1),(8,3),(12,1),(12,5),(16,3),(20,7)]:
    for ktext in ['0.01','0.8','0.97']:
        ats=[];pqs=[]
        for phase in [mp.mpf(0),mp.mpf(1)/7,mp.mpf(4)/11,mp.mpf(3)/2]:
            row,at,pq=family(N,tau,ktext,phase);rows.append(row);ats.append(at);pqs.append(pq)
            assert max(mp.mpf(x) for x in row['residuals'].values())<mp.mpf('1e-65'),row
        phase_spreads.append({'N':N,'tau':tau,'k':ktext,
                             'AT_relative_spread':str(rel(max(ats),min(ats))),
                             'pq_relative_spread':str(rel(max(pqs),min(pqs)))})
control=[family(6,1,'0.8',p)[0] for p in [mp.mpf(0),mp.mpf(1)/7]]
assert abs(mp.mpf(control[0]['pq'])-mp.mpf(control[1]['pq']))>mp.mpf('1e-8')
report={'mpmath_version':mp.__version__,'decimal_precision':80,
        'proof_status':'rounded corroboration only; not interval validated',
        'target_family_phase_count':len(rows),'target_cases':rows,'phase_spreads':phase_spreads,
        'N6_outside_target_negative_control':control,
        'maximum_target_identity_relative_residual':str(max(mp.mpf(v) for row in rows for v in row['residuals'].values())),
        'maximum_product_phase_relative_spread':str(max(mp.mpf(r['pq_relative_spread']) for r in phase_spreads))}
Path(__file__).with_name('INDEPENDENT_GEOMETRY.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['target_cases','N6_outside_target_negative_control','phase_spreads']},indent=2))
