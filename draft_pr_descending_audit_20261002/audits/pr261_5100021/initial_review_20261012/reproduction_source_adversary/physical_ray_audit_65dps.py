"""Independent Cartesian ray tracing; written before reading submitted scripts/proof.
No elliptic-function orbit or proof-specific area helper is used.
"""
from pathlib import Path
import sys,json,math,platform
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import mpmath as mp
mp.mp.dps=65
BASE=Path(__file__).parent

def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def mul(s,p):return (s*p[0],s*p[1])
def norm(p):return mp.sqrt(dot(p,p))
def unit(p):return mul(1/norm(p),p)
def launch(p,a,b,lam):
    # Linear transform to unit circle and solve tangent contact there.
    ac,bc=mp.sqrt(a*a-lam),mp.sqrt(b*b-lam)
    z=(p[0]/ac,p[1]/bc);r2=dot(z,z)
    h=mp.sqrt(r2-1)
    zt=((z[0]-z[1]*h)/r2,(z[1]+z[0]*h)/r2)
    return unit(sub((ac*zt[0],bc*zt[1]),p))
def flight(p,d,a,b):
    D=d[0]**2/a**2+d[1]**2/b**2
    t=-2*(p[0]*d[0]/a**2+p[1]*d[1]/b**2)/D
    assert t>0
    q=add(p,mul(t,d))
    n=(q[0]/a**2,q[1]/b**2)
    r=unit(sub(d,mul(2*dot(d,n)/dot(n,n),n)))
    return q,r

def trace(a,b,lam,N,theta=mp.mpf('0')):
    p=(a*mp.cos(theta),b*mp.sin(theta));d=launch(p,a,b,lam)
    vertices=[p];vel=[d];advance=mp.mpf(0)
    for _ in range(N):
        q,r=flight(p,d,a,b)
        z=(p[0]/a,p[1]/b);w=(q[0]/a,q[1]/b)
        ang=mp.atan2(det(z,w),dot(z,w))
        if ang<0:ang+=2*mp.pi
        advance+=ang
        vertices.append(q);vel.append(r);p,d=q,r
    return vertices,vel,advance

def closure_lam(a,b,N,w):
    lo=b*b*mp.mpf('1e-50');hi=b*b*(1-mp.mpf('1e-50'))
    target=2*mp.pi*w
    assert trace(a,b,lo,N)[2]<target<trace(a,b,hi,N)[2]
    for _ in range(215):
        mid=(lo+hi)/2
        if trace(a,b,mid,N)[2]<target:lo=mid
        else:hi=mid
    return (lo+hi)/2

def areas(P,M):
    Q=[];R=[];N=len(P);mindet=mp.inf
    for i in range(N):
        p,q=P[i],P[(i+1)%N];d=sub(q,p)
        Q.append(add(p,mul(dot(sub(M,p),d)/dot(d,d),d)))
        n1,n2=sub(p,M),sub(q,M)
        c1,c2=dot(n1,p),dot(n2,q);D=det(n1,n2)
        mindet=min(mindet,abs(D)/(norm(n1)*norm(n2)))
        R.append(((c1*n2[1]-c2*n1[1])/D,(n1[0]*c2-n2[0]*c1)/D))
    ar=lambda pts:sum(det(pts[i],pts[(i+1)%N]) for i in range(N))/2
    return ar(Q),ar(R),mindet

def diagnose(a,b,lam,N,w,theta):
    V,D,adv=trace(a,b,lam,N,theta);P=V[:-1]
    boundary=max(abs(p[0]**2/a**2+p[1]**2/b**2-1) for p in V)
    tangency=mp.mpf(0);reflection=mp.mpf(0)
    for i in range(N):
        p,q=V[i],V[i+1];d=unit(sub(q,p));ac2,bc2=a*a-lam,b*b-lam
        qa=d[0]**2/ac2+d[1]**2/bc2;qb=p[0]*d[0]/ac2+p[1]*d[1]/bc2;qc=p[0]**2/ac2+p[1]**2/bc2-1
        tangency=max(tangency,abs(qb*qb-qa*qc)/(qa*(1+abs(qc))))
        n=(q[0]/a**2,q[1]/b**2);r=unit(sub(d,mul(2*dot(d,n)/dot(n,n),n)))
        reflection=max(reflection,norm(sub(r,D[i+1])))
    closure=norm(sub(V[-1],V[0]))/a
    velocity_closure=norm(sub(D[-1],D[0]))
    primitive=min(norm(sub(P[k],P[0]))/a for k in range(1,N))
    central=max(norm(add(P[i],P[i+N//2]))/a for i in range(N//2))
    c=mp.sqrt(a*a-b*b)
    AP,AS,md=areas(P,(c,mp.mpf(0)));AP2,AS2,md2=areas(P,(-c,mp.mpf(0)))
    return dict(phase=str(theta),pedal=str(AP),antipedal=str(AS),product=str(AP*AS),opposite_product=str(AP2*AS2),focus_area_difference=str(max(abs(AP2-AP),abs(AS2-AS))),boundary=str(boundary),tangency=str(tangency),reflection=str(reflection),closure=str(closure),velocity_closure=str(velocity_closure),primitive_vertex_separation=str(primitive),central_symmetry=str(central),min_antipedal_normal_sine=str(min(md,md2)),winding_residual=str(abs(adv/(2*mp.pi)-w)))

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');args=parser.parse_args()
    specs=[('1.000001',4,1),('1.5',4,1),('2',8,1),('2',8,3),('3',12,1),('3',12,5),('1.2',16,3),('1.2',16,7),('1.5',20,3),('1.5',20,9),('5',24,5),('5',24,11),('10',12,5),('1.000001',32,15)]
    if args.quick:specs=specs[:4]
    phases=['0','0.07','0.31','0.79','1.19','1.53','2.41']
    out={'mechanism':'Cartesian tangent contact, quadratic ray flight, Euclidean reflection, closure by total boundary winding bisection; no Jacobi functions','python':sys.version,'mpmath':mp.__version__,'dps':mp.mp.dps,'cases':[]}
    for astr,N,w in specs:
        a,b=mp.mpf(astr),mp.mpf(1);lam=closure_lam(a,b,N,w)
        rows=[diagnose(a,b,lam,N,w,mp.mpf(t)) for t in phases]
        prods=[mp.mpf(r['product']) for r in rows];peds=[mp.mpf(r['pedal']) for r in rows];antis=[mp.mpf(r['antipedal']) for r in rows]
        spread=(max(prods)-min(prods))/max(1,max(abs(x) for x in prods))
        case={'a':astr,'b':'1','N':N,'winding':w,'gcd':math.gcd(N,w),'lambda':str(lam),'strict_caustic_minor_squared':str(1-lam),'product_relative_spread':str(spread),'pedal_spread':str(max(peds)-min(peds)),'antipedal_spread':str(max(antis)-min(antis)),'rows':rows}
        out['cases'].append(case)
        print(f'a={astr} N={N} w={w} lambda={mp.nstr(lam,15)} spread={mp.nstr(spread,4)} closure={mp.nstr(max(mp.mpf(r["closure"]) for r in rows),4)}',flush=True)
        (BASE/'PHYSICAL_RAY_65DPS_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    assert all(mp.mpf(c['product_relative_spread'])<mp.mpf('1e-35') for c in out['cases'])
    assert all(max(mp.mpf(r[k]) for r in c['rows'])<mp.mpf('1e-35') for c in out['cases'] for k in ('boundary','tangency','reflection','closure','velocity_closure','central_symmetry','winding_residual'))
if __name__=='__main__':main()
