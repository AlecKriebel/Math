"""Independent Fraction CTMC reconstruction; written before packaged helper reading."""
from fractions import Fraction as F
from itertools import product
from math import ceil
from pathlib import Path
import datetime, hashlib, json, random

def require(ok, message):
    if not ok: raise RuntimeError(message)

def parameters(lam):
    beta=17*lam/8; q=F(7,8); c=2*(beta+4); m=4*c; theta=beta+c+4
    gamma=(theta+1)/(theta+2); eta=(1+gamma)/2; ell=1/(eta-gamma)
    weights=[F(1)]; mass=F(1); moment=F(0); R=0
    while R<1 or moment/mass<=theta or q*(R+1)<=beta+c+2:
        R+=1;weights.append(weights[-1]*gamma);mass+=weights[-1];moment+=R*weights[-1]
    mu=moment/mass
    prefix=F(0); t=[]
    for k in range(R):
        prefix+=weights[k]*(k-mu)
        t.append(prefix/(weights[k]*gamma*(k+1)))
    g=[F(0)]*(R+1)
    for k in range(R-1,-1,-1):g[k]=g[k+1]-t[k]
    G=g[0]
    N=max(R+2,3*(R+1),ceil((m+(1+eta)*R+eta)/(1-eta)),ceil(ell*G*(lam+4*(2*R+1))))
    B=(N+R+1)*(beta+c+G*(lam+2*(N+R))+1)
    return locals()

def test(lam):
    p=parameters(lam)
    beta,q,c,m,theta,gamma,eta,ell,R,mu,G,N,B=(p[k] for k in ['beta','q','c','m','theta','gamma','eta','ell','R','mu','G','N','B'])
    def g(k):return p['g'][k] if k<R else F(0)
    def f(v):return max(F(0),min(F(1),ell*(v-gamma)))
    def h(z):return F(z*z)/(2*m)+m/2 if abs(z)<=m else F(abs(z))
    def hp(z):return max(F(-1),min(F(1),F(z)/m))
    def W(s):a,b,x,y=s;return 2*a+2*b+x+y
    def Z(s):a,b,x,y=s;return a+x-b-y
    def J(s):a,b,x,y=s;D=x+y+1;return f(F(b,D))*g(y)+f(F(a,D))*g(x)
    def V(s):return W(s)+c*h(Z(s))+J(s)
    def events(s):
        a,b,x,y=s;D=x+y+1
        moves=[((1,0,0,0),lam/2),((0,1,0,0),lam/2),((-1,0,1,0),F(a*(x+1),D)),((0,-1,0,1),F(b*(y+1),D)),((0,0,-1,0),F(x*(y+1),D)),((0,0,0,-1),F(y*(x+1),D))]
        return [(tuple(si+vi for si,vi in zip(s,v)),rate,v) for v,rate in moves if rate]
    def drift(s,fn):return sum((r*(fn(t)-fn(s)) for t,r,_ in events(s)),F(0))
    for k in range(R+1):
        v=(gamma*(k+1)*(g(k+1)-g(k)) if k<R else F(0))+(k*(g(k-1)-g(k)) if k else F(0))
        require(v==k-mu,'Poisson terminal/interior')
        require(g(k)>=0 and (k==R or g(k)>=g(k+1)),'Monotone corrector')
    require(g(R)==g(R+1)==0 and q*(R+1)>beta+c+2 and mu>theta,'Constants')
    cases=set(product(range(4),repeat=4))
    pivots=[0,1,R-1,R,R+1,R+2,N-1,N,N+1]
    for x,y in product(pivots,repeat=2):
        D=x+y+1
        waits={0,1,ceil(gamma*D)-1,ceil(gamma*D),ceil(eta*D)-1,ceil(eta*D),ceil(eta*D)+1}
        for b in waits:
            cases.add((0,b,x,y));cases.add((b,0,y,x))
    for x,y in [(0,0),(R,0),(0,R),(R,R),(N-1,R),(R,N-1)]:
        for b in [0,1,ceil(B),ceil(B)+1]:
            cases.add((b,0,x,y));cases.add((0,b,x,y))
    rng=random.Random(23524971)
    for _ in range(100):
        x=rng.choice(pivots);y=rng.choice(pivots);D=x+y+1
        a=rng.randrange(0,3*D+1);b=rng.randrange(0,3*D+1)
        cases.add((a,b,x,y))
    hits={'balanced':0,'x_corner':0,'y_corner':0,'finite_xy_large_wait':0,'inside_F':0}
    max_jump=F(0); outside_max=None
    for s in sorted(cases):
        a,b,x,y=s;D=x+y+1;n=sum(s);z=Z(s);u=F(a*(x+1)+b*(y+1),D);d=F(2*x*y+x+y,D)
        require(drift(s,W)==2*lam-u-d,'LW identity')
        require(drift(s,Z)==F(y-x,D),'LZ identity')
        base=drift(s,lambda t:W(t)+c*h(Z(t)))
        rhs4=beta-u-q*d+c*hp(z)*F(y-x,D)
        require(base<=rhs4,'Rounded drift4')
        lg_y=drift(s,lambda t:g(t[3]));lg_x=drift(s,lambda t:g(t[2]))
        if y<=R and F(b,D)>=gamma:require(lg_y<=y-mu,'Lg y')
        if x<=R and F(a,D)>=gamma:require(lg_x<=x-mu,'Lg x')
        if y>R:require(lg_y==0,'Terminal y successor')
        if x>R:require(lg_x==0,'Terminal x successor')
        lj=drift(s,J)
        require(lj<=f(F(b,D))*lg_y+f(F(a,D))*lg_x+ell*G*(lam+4*d)/D,'Interface8')
        require(lj<=G*(lam+2*d),'Coarse interface9')
        vv=V(s);require(W(s)<=vv<=(1+c)*W(s)+c*m/2+2*G,'Coercivity17')
        for successor,r,move in events(s):
            require(min(successor)>=0 and r>0,'Boundary/legal event')
            dv=abs(V(successor)-vv);max_jump=max(max_jump,dv)
            require(dv<=2+c+2*G,'Bounded jump')
            if move in [(-1,0,1,0),(0,-1,0,1)]:require(J(successor)<=J(s),'First download monotonicity')
        lv=base+lj
        if min(x,y)>=R+1:
            hits['balanced']+=1;require(lv<-2,'Balanced region')
        elif y<=R and x>=N:
            hits['x_corner']+=1;require(lv<=-3,'X corner')
        elif x<=R and y>=N:
            hits['y_corner']+=1;require(lv<=-3,'Y corner')
        elif a+b>B:
            hits['finite_xy_large_wait']+=1;require(x+y<=N+R and lv<=-1,'Remaining region')
        else:hits['inside_F']+=1
        if x+y>N+R or a+b>B:
            require(lv<=-1,'Final all-region bound')
            outside_max=lv if outside_max is None else max(outside_max,lv)
    # A missing quadratic-variation d/8 cannot pass this interior identity.
    s=(0,0,1,1);D=3;d=F(4,3)
    actual=drift(s,lambda t:W(t)+c*h(Z(t)))
    mutated_rhs=beta-d
    require(actual>mutated_rhs,'Negative control missing d/8 not detected')
    # A bounded-total-seed reading contradicts the actual rates at this boundary.
    seed_state=(2,3,0,0)
    internal=sum(r for _,r,v in events(seed_state) if v not in [(1,0,0,0),(0,1,0,0)])
    require(internal==5 and internal>1,'Capacity-one transfer negative control')
    return {'load':str(lam),'R':R,'N':N,'B_ceiling':ceil(B),'mu_greater_theta':True,'poisson_states_checked':R+1,'finite_states_checked':len(cases),'regions':hits,'outside_drift_max_exact':str(outside_max),'max_observed_jump_below_bound':max_jump<=2+c+2*G,'negative_controls':{'missing_departure_quadratic_variation_rejected':True,'bounded_aggregate_seed_interpretation_rejected':True},'all_controls_pass':True}

if __name__=='__main__':
    output={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mechanism':'Fresh literal Fraction generator; direct V differences and independent constant construction; no submitted imports','results':[],'limitation':'Finite rational-load corroboration only. Universal all-real-load proof is independent written analysis.'}
    for lam in [F(1,8),F(1),F(4)]:
        r=test(lam);output['results'].append(r)
        print(json.dumps({'load':r['load'],'R':r['R'],'states':r['finite_states_checked'],'regions':r['regions']}),flush=True)
    p=Path(__file__).with_name('fresh_exact_results.json')
    output['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    p.write_text(json.dumps(output,indent=2)+'\n')
