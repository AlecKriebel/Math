"""Finite diagnostics for the explicit classical bridge, never an all-phase proof.
Run with the assigned existing scientific interpreter and -B. Writes JSON in this folder.
"""
from pathlib import Path
import json, math
import mpmath as mp
mp.mp.dps = 90
HERE = Path(__file__).resolve().parent
TOL = mp.mpf('1e-65')

def fmt(x): return mp.nstr(x, 25)
def rel(a,b): return abs(a-b)/max(mp.mpf(1),abs(a),abs(b))
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def area(P): return sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def norm(a): return mp.sqrt(a[0]**2+a[1]**2)

trace_rows=[]
for m in [mp.mpf(1)/5,mp.mpf(3)/5,mp.mpf(9)/10]:
    K=mp.ellipk(m); kp=mp.sqrt(1-m)
    sn=lambda z: mp.ellipfun('sn',z,m)
    cn=lambda z: mp.ellipfun('cn',z,m)
    dn=lambda z: mp.ellipfun('dn',z,m)
    for q in [1,3,5,7,9,15]:
        h=[2*K*j/q for j in range(q)]
        U=lambda z: sum(dn(z+x) for x in h)
        C=mp.fprod((cn(2*K*n/q)/sn(2*K*n/q))**2 for n in range(1,(q-1)//2+1))
        eta=1/U(0)
        mt=(m-2)*eta**2+2*eta**3*sum(dn(x)**3 for x in h)
        const=kp**q/C**2
        errors={'product_to_sum':mp.mpf(0),'trace_product':mp.mpf(0),'Landen':mp.mpf(0),
                'period_normalization':rel(mp.ellipk(mt),K/(q*eta)),
                'constant_normalization':rel(const,mp.sqrt(1-mt)/eta**2)}
        for z in [mp.mpf(0),K/7,K/2,mp.mpf('1.21')*K,K/5+mp.j/7,mp.j*mp.ellipk(1-m)/5]:
            vals=[dn(z+x) for x in h]
            errors['product_to_sum']=max(errors['product_to_sum'],rel(mp.fprod(vals),C*U(z)))
            errors['trace_product']=max(errors['trace_product'],rel(U(z)*U(z+K),const))
            errors['Landen']=max(errors['Landen'],rel(U(z),mp.ellipfun('dn',z/eta,mt)/eta))
        assert all(e<TOL for e in errors.values()),(m,q,errors)
        trace_rows.append({'m':fmt(m),'q':q,'phases':6,'constant':fmt(const),'max_errors':{k:fmt(v) for k,v in errors.items()}})

def family(m,N,tau):
    K=mp.ellipk(m); kp=mp.sqrt(1-m); v=2*tau*K/N
    sn=lambda z: mp.ellipfun('sn',z,m)
    cn=lambda z: mp.ellipfun('cn',z,m)
    dn=lambda z: mp.ellipfun('dn',z,m)
    a=dn(v)/cn(v); b=kp/cn(v); alpha=mp.mpf(1); beta=kp
    J=sn(v)*cn(v)/dn(v)
    f=lambda z: sn(z)*cn(z)/dn(z)
    P=lambda z:(-a*sn(z),b*cn(z))
    q=N//math.gcd(N,2); r=N//q
    C=mp.fprod((cn(2*K*n/q)/sn(2*K*n/q))**2 for n in range(1,(q-1)//2+1)) if q%2 else None
    predicted=(a*a*b*b/(alpha*beta))*f(v)*(2*f(v)-f(2*v))*r*r*kp**q/(4*J*J*C*C) if C is not None else None
    errors={key:mp.mpf(0) for key in ['reflection_foot','hodograph_phase','outer_trace','pedal_trace','product','reversal','repeat_three']}
    vals=[]
    for u in [0,K/7,mp.mpf('.43')*K,K,mp.mpf('2.13')*K]:
        pts=[P(u+2*i*v) for i in range(N)]
        normals=[(x/(a*a),y/(b*b)) for x,y in pts]
        feet=[(x/(x*x+y*y),y/(x*x+y*y)) for x,y in normals]
        outer=[]
        for i in range(N):
            ni=normals[i]; nj=normals[(i+1)%N]; den=det(ni,nj)
            outer.append(((nj[1]-ni[1])/den,(ni[0]-nj[0])/den))
        edges=[sub(pts[(i+1)%N],pts[i]) for i in range(N)]
        es=[(d[0]/norm(d),d[1]/norm(d)) for d in edges]
        for i in range(N):
            qi=((es[(i-1)%N][0]-es[i][0])/(2*J),(es[(i-1)%N][1]-es[i][1])/(2*J))
            errors['reflection_foot']=max(errors['reflection_foot'],rel(norm(sub(qi,feet[i])),0))
            Xi=(a*es[i][0],b*es[i][1]); target=P(u+(2*i+1)*v+K)
            errors['hodograph_phase']=max(errors['hodograph_phase'],rel(norm(sub(Xi,target)),0))
        T=lambda z:sum(dn(z+2*i*v) for i in range(N))
        ao=area(outer); aq=area(feet)
        errors['outer_trace']=max(errors['outer_trace'],rel(ao,a*a*b*b/(alpha*beta)*f(v)*T(u+v)))
        errors['pedal_trace']=max(errors['pedal_trace'],rel(aq,(2*f(v)-f(2*v))*T(u+v+K)/(4*J*J)))
        prod=ao*aq
        if predicted is not None: errors['product']=max(errors['product'],rel(prod,predicted))
        errors['reversal']=max(errors['reversal'],rel(area(outer[::-1])*area(feet[::-1]),prod))
        errors['repeat_three']=max(errors['repeat_three'],rel(area(outer*3)*area(feet*3),9*prod))
        vals.append(prod)
    assert all(e<TOL for e in errors.values()),(m,N,tau,errors)
    return {'m':fmt(m),'N':N,'tau':tau,'primitive':math.gcd(N,tau)==1,'phases':5,
            'predicted_product':None if predicted is None else fmt(predicted),
            'product_phase_spread':fmt(max(vals)-min(vals)),
            'max_errors':{k:fmt(v) for k,v in errors.items()}}

geom_rows=[]
for m in [mp.mpf(1)/4,mp.mpf(4)/5]:
    for N,tau in [(3,1),(5,1),(5,2),(6,1),(7,2),(9,4),(10,1),(10,3),(14,3),(14,5),(15,4),(15,7)]:
        geom_rows.append(family(m,N,tau))
negative_rows=[family(mp.mpf(3)/5,4,1),family(mp.mpf(3)/5,8,1)]
assert all(mp.mpf(row['product_phase_spread'])>mp.mpf('1e-6') for row in negative_rows)
result={'kind':'finite diagnostics; analytic all-phase bridge is CLASSICAL_BRIDGE.md','mpmath_version':mp.__version__,
        'digits':mp.mp.dps,'tolerance':str(TOL),'trace_family_count':len(trace_rows),'trace_phase_count':len(trace_rows)*6,
        'geometry_family_count':len(geom_rows),'geometry_phase_count':len(geom_rows)*5,
        'trace_results':trace_rows,'geometry_results':geom_rows,'excluded_even_q_negative_controls':negative_rows,
        'no_numeric_substitution_for_universal_proof':True}
(HERE/'bridge_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},indent=2))
