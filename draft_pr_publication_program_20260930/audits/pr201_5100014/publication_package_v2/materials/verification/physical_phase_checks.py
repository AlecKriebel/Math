"""Independent physical Poncelet map, direct outer tangents and projections.

Only mpmath is imported from the shared software path. All geometry starts from
intersection/tangency equations; no candidate parameterization or formula.
Finite high-precision evidence, never an interval or universal proof.
"""
import sys,json,math,time
from pathlib import Path
import mpmath as mp
mp.mp.dps=85

def need(c,m):
    if not c: raise RuntimeError(m)

def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def shoelace(P): return sum(cross(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def scaleerr(v): return abs(v)/max(mp.mpf(1),abs(v))

def next_vertex(P,a,b,lam):
    # Contacts of tangents through P to x²/alpha²+y²/beta²=1:
    # in normalized caustic coordinates, q.v=1, q.q=1.
    alpha,beta=mp.sqrt(a*a-lam),mp.sqrt(b*b-lam)
    X,Y=P[0]/alpha,P[1]/beta
    r2=X*X+Y*Y; z=mp.sqrt(r2-1)
    candidates=[]
    for sign in (-1,1):
        Q=(alpha*(X-sign*z*Y)/r2,beta*(Y+sign*z*X)/r2)
        D=(Q[0]-P[0],Q[1]-P[1])
        u=-2*(P[0]*D[0]/a**2+P[1]*D[1]/b**2)/(D[0]**2/a**2+D[1]**2/b**2)
        T=(P[0]+u*D[0],P[1]+u*D[1])
        if cross((P[0]/a,P[1]/b),(T[0]/a,T[1]/b))>0:
            candidates.append(T)
    need(len(candidates)==1,'positive chord selection not unique')
    return candidates[0]

def orbit(a,b,lam,N,phase):
    P=(a*mp.cos(phase),b*mp.sin(phase)); vertices=[]; advance=mp.mpf(0)
    for i in range(N):
        vertices.append(P); Q=next_vertex(P,a,b,lam)
        inc=mp.atan2(cross((P[0]/a,P[1]/b),(Q[0]/a,Q[1]/b)),P[0]*Q[0]/a**2+P[1]*Q[1]/b**2)
        need(0<inc<mp.pi,'non-forward or central chord')
        advance+=inc; P=Q
    return vertices,P,advance

def root_caustic(a,b,N,k):
    lo=b*b*mp.mpf('1e-70');hi=b*b*(1-mp.mpf('1e-70'))
    target=2*mp.pi*k; phase=mp.mpf('.317')
    need(orbit(a,b,lo,N,phase)[2]<target<orbit(a,b,hi,N,phase)[2],'closure root not bracketed')
    for _ in range(245):
        mid=(lo+hi)/2
        if orbit(a,b,mid,N,phase)[2]<target:lo=mid
        else:hi=mid
    return (lo+hi)/2

def derived(P,a,b,M):
    lines=[(x/a**2,y/b**2,mp.mpf(1)) for x,y in P]
    out=[];feet=[];on_error=mp.mpf(0);perp_error=mp.mpf(0)
    for j,(x,y,h) in enumerate(lines):
        X,Y,H=lines[(j+1)%len(lines)]
        d=x*Y-y*X;need(abs(d)>mp.mpf('1e-70'),'consecutive outer tangents parallel')
        out.append(((h*Y-y*H)/d,(x*H-h*X)/d))
        q=(h-x*M[0]-y*M[1])/(x*x+y*y)
        f=(M[0]+q*x,M[1]+q*y);feet.append(f)
        on_error=max(on_error,abs(x*f[0]+y*f[1]-h))
        perp_error=max(perp_error,abs(cross((f[0]-M[0],f[1]-M[1]),(x,y))))
    return shoelace(out),shoelace(feet),on_error,perp_error

def textnum(x):return mp.nstr(x,50)
def case(a,N,k,expect_invariant=True):
    a,b=mp.mpf(a),mp.mpf(1);lam=root_caustic(a,b,N,k)
    phases=[mp.mpf(v) for v in ('0','.173','.719','1.37','2.19')]
    Ms=[(mp.mpf(0),mp.mpf(0)),(mp.mpf('.37'),mp.mpf('-.81')),(mp.mpf(17),mp.mpf(-23)),(mp.sqrt(a*a-b*b),mp.mpf(0))]
    products=[[] for _ in Ms]; maxclosure=mp.mpf(0);maxphysical=mp.mpf(0);signed=[]
    for phase in phases:
        P,last,advance=orbit(a,b,lam,N,phase)
        maxclosure=max(maxclosure,abs(last[0]-P[0][0]),abs(last[1]-P[0][1]),abs(advance-2*mp.pi*k))
        for j,p in enumerate(P):
            q=P[(j+1)%N]; nx,ny=p[1]-q[1],q[0]-p[0];h=nx*p[0]+ny*p[1]
            maxphysical=max(maxphysical,abs(p[0]**2/a**2+p[1]**2-1),abs((a*a-lam)*nx*nx+(b*b-lam)*ny*ny-h*h))
        for idx,M in enumerate(Ms):
            ap,am,on,perp=derived(P,a,b,M)
            need(max(on,perp)<mp.mpf('1e-65'),'direct foot constraint failed')
            products[idx].append(ap*am);signed.append(mp.sign(am))
    spreads=[max(abs(x-v[0]) for x in v)/max(1,max(map(abs,v))) for v in products]
    need(maxclosure<mp.mpf('1e-45') and maxphysical<mp.mpf('1e-45'),'physical closure/tangency failed')
    if expect_invariant:need(max(spreads)<mp.mpf('1e-45'),'target invariant changed across physical phases')
    return {'a':str(a),'b':'1','N':N,'winding':k,'primitive':math.gcd(N,k)==1,'lambda':textnum(lam),'max_closure_error':textnum(maxclosure),'max_boundary_and_tangency_error':textnum(maxphysical),'relative_phase_spread_by_M':list(map(textnum,spreads)),'M':[[textnum(x) for x in M] for M in Ms],'phase0_products':list(map(lambda x:textnum(x[0]),products)),'pedal_signs':sorted(set(map(int,signed))),'expected_invariant':expect_invariant},(a,b,lam)

def main():
    started=time.time(); records=[]
    # Every admissible primitive winding for every listed N, at each aspect ratio.
    for a in ('1.0001','1.3','2','5'):
        for N in (6,10,14,18,22):
            for k in range(1,N//2):
                if math.gcd(N,k)==1:
                    rec,_=case(a,N,k);records.append(rec)
    negative=[]
    for N,k in ((3,1),(4,1),(5,1),(8,1),(8,3),(12,1),(12,5)):
        rec,_=case('2',N,k,False);negative.append(rec)
    need(any(max(map(mp.mpf,r['relative_phase_spread_by_M']))>mp.mpf('1e-4') for r in negative),'negative period controls did not falsify')
    repeated_odd=[]
    for N,k in ((6,2),(10,2),(14,2),(18,2),(18,4),(22,2)):
        rec,_=case('2',N,k,False);repeated_odd.append(rec)
    need(all(max(map(mp.mpf,r['relative_phase_spread_by_M']))>mp.mpf('1e-10') for r in repeated_odd),'repeated odd-period control did not falsify')
    rec,(a,b,lam)=case('2',18,3);records.append(rec) # odd repetition of primitive6
    # N10 winding3 has signed pedal area crossing zero for real exterior M.
    rec,(a,b,lam)=case('2',10,3)
    P,_,_=orbit(a,b,lam,10,mp.mpf('.173'))
    A,C,_,_=derived(P,a,b,(0,0));_,B,_,_=derived(P,a,b,(1,0));q=B-C
    need(C>0 and q<0,'star pedal quadratic must cross zero')
    radius=mp.sqrt(-C/q);zero=[]
    for phase in (mp.mpf('.173'),mp.mpf('.719'),mp.mpf('1.37')):
        V,_,_=orbit(a,b,lam,10,phase)
        _,z,_,_=derived(V,a,b,(radius,0));need(abs(z)<mp.mpf('1e-45'),'zero-pedal sample not invariant')
        _,minus,_,_=derived(V,a,b,(radius*mp.mpf('.99'),0));_,plus,_,_=derived(V,a,b,(radius*mp.mpf('1.01'),0))
        need(minus>0 and plus<0,'pedal zero crossing failed')
        zero.append({'phase':str(phase),'residual':textnum(z),'below':textnum(minus),'above':textnum(plus)})
    report={'status':'PASS','precision_decimal_digits':mp.mp.dps,'optimization':sys.flags.optimize,'elapsed_seconds':time.time()-started,'method':'direct physical tangent contact and second ellipse intersection; direct outer tangent solves and perpendicular feet','scope':'finite non-interval numerical evidence; primitive stars only in target, repetitions tested separately','target_cases':records,'negative_period_controls':negative,'excluded_even_repetitions_of_odd_period':repeated_odd,'star_zero_pedal':{'M_x':textnum(radius),'samples':zero}}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
