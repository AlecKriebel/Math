"""Exact-rational checks of the actual six-rate chain and cutoff certificate.

These finite controls supplement, rather than replace, TURN_4.md's all-state proof.
No floating-point quantity is used in an assertion.
"""
from fractions import Fraction as F
from collections import Counter
from functools import lru_cache
import json, random, sys
sys.set_int_max_str_digits(0)
counts=Counter()
def ck(p,label):
    if not p: raise AssertionError(label)
    counts[label]+=1
def ceil(x): return -((-x.numerator)//x.denominator) if isinstance(x,F) else x

def transitions(s,la):
    a,b,x,y=s; D=x+y+1
    return [("arr_A",(a+1,b,x,y),la/2),("arr_B",(a,b+1,x,y),la/2),
            ("first_A",(a-1,b,x+1,y),F(a*(x+1),D)),
            ("first_B",(a,b-1,x,y+1),F(b*(y+1),D)),
            ("dep_X",(a,b,x-1,y),F(x*(y+1),D)),
            ("dep_Y",(a,b,x,y-1),F(y*(x+1),D))]

class Certificate:
    def __init__(self,la):
        self.la=la; self.beta=17*la/8; self.q=F(7,8)
        self.c=2*(self.beta+4); self.m=4*self.c
        self.theta=self.beta+self.c+4
        self.ga=(self.theta+1)/(self.theta+2)
        self.eta=(1+self.ga)/2; self.ell=1/(self.eta-self.ga)
        z=F(1); z1=F(0); power=F(1); R=0
        while True:
            R+=1; power*=self.ga; z+=power; z1+=R*power
            mu=z1/z
            if mu>self.theta and self.q*(R+1)>self.beta+self.c+2: break
        self.R=R; self.mu=mu
        ds=[]; prefix=F(0); power=F(1)
        for k in range(R):
            prefix+=power*(k-mu)
            ds.append(prefix/(self.ga*power*(k+1)))
            power*=self.ga
        gs=[F(0)]*(R+1)
        for k in reversed(range(R)): gs[k]=gs[k+1]-ds[k]
        self.gs=gs; self.G=gs[0]
        self.N=ceil(max(F(R+2),F(3*(R+1)),
            (self.m+(1+self.eta)*R+self.eta)/(1-self.eta),
            self.ell*self.G*(la+4*(2*R+1))))
        self.B=(self.N+R+1)*(self.beta+self.c+self.G*(la+2*(self.N+R))+1)
    def g(self,k):
        assert k>=0
        return self.gs[k] if k<self.R else F(0)
    def f(self,t): return min(F(1),max(F(0),(t-self.ga)*self.ell))
    def h(self,z):
        return F(z*z,1)/(2*self.m)+self.m/2 if abs(z)<=self.m else F(abs(z))
    def hp(self,z): return min(F(1),max(F(-1),F(z)/self.m))
    def W(self,s): a,b,x,y=s; return 2*(a+b)+x+y
    def Z(self,s): a,b,x,y=s; return a+x-b-y
    def fs(self,s):
        a,b,x,y=s; D=x+y+1
        return self.f(F(b,D)),self.f(F(a,D))
    def js(self,s):
        p,q=self.fs(s); a,b,x,y=s
        return p*self.g(y),q*self.g(x)
    def J(self,s): return sum(self.js(s))
    def V(self,s): return self.W(s)+self.c*self.h(self.Z(s))+self.J(s)
    def gen(self,s,h):
        hs=h(s)
        return sum(rate*(h(t)-hs) for _,t,rate in transitions(s,self.la) if rate)
    def check_state(self,s,region=None):
        a,b,x,y=s; D=x+y+1; z=self.Z(s)
        u=F(a*(x+1)+b*(y+1),D); d=F(2*x*y+x+y,D)
        ck(self.gen(s,self.W)==2*self.la-u-d,'exact_workload_identity')
        ck(self.gen(s,self.Z)==F(y-x,D),'exact_imbalance_identity')
        lh=self.gen(s,lambda t:self.h(self.Z(t)))
        ck(lh<=self.hp(z)*F(y-x,D)+(self.la+d)/(2*self.m),'rounded_imbalance_bound')
        fs=self.fs(s)
        lg_y=self.gen(s,lambda t:self.g(t[3]))
        lg_x=self.gen(s,lambda t:self.g(t[2]))
        lj=self.gen(s,self.J)
        ck(lj<=fs[0]*lg_y+fs[1]*lg_x+self.ell*self.G*(self.la+4*d)/D,'global_product_interface_bound')
        ck(lj<=self.G*(self.la+2*d),'bounded_visible_correction_bound')
        if y<=self.R:
            ck(fs[0]*lg_y<=fs[0]*(y-self.mu),'cutoff_poisson_bound_y')
        if x<=self.R:
            ck(fs[1]*lg_x<=fs[1]*(x-self.mu),'cutoff_poisson_bound_x')
        for typ,t,rate in transitions(s,self.la):
            if not rate: continue
            if typ.startswith('first'):
                ck(all(p<=q for p,q in zip(self.fs(t),fs)),'first_download_cutoffs_nonincreasing')
                ck(all(p<=q for p,q in zip(self.js(t),self.js(s))),'first_download_products_nonincreasing')
            if typ.startswith('dep'):
                ck(all(F(0)<=p-q<=2*self.ell/D for p,q in zip(self.fs(t),fs)),'departure_cutoff_bound')
        lv=self.gen(s,self.V)
        ck(self.V(s)>=sum(s),'coercivity')
        if min(x,y)>=self.R+1:
            ck(lj==0,'large_both_exact_vanishing')
            ck(lv<-2,'region_I_negative_drift')
        elif max(x,y)>=self.N:
            ck(lv<=-3,'region_II_negative_drift')
        elif a+b>self.B:
            ck(lv<=-1,'region_III_negative_drift')
        if x+y>self.N+self.R or a+b>self.B:
            ck(lv<=-1,'outside_finite_set_negative_drift')


def run():
    rng=random.Random(30001608); reports=[]
    for la in [F(1,2),F(1),F(2),F(5),F(10)]:
        c=Certificate(la); R=c.R
        for k in range(R+1):
            val=(c.ga*(k+1)*(c.g(k+1)-c.g(k)) if k<R else 0)+(k*(c.g(k-1)-c.g(k)) if k else 0)
            ck(val==k-c.mu,'finite_poisson_equation_all_states')
            ck(c.g(k)>=0,'nonnegative_corrector')
            if k<R: ck(c.g(k+1)<c.g(k),'strict_decreasing_corrector')
        for z in [F(0),c.m,c.m-1,c.m+1,-c.m,-c.m+1,-c.m-1,F(ceil(c.m))]:
            for v in [F(-1),F(1),F(1,2)]:
                ck(c.h(z+v)-c.h(z)<=c.hp(z)*v+v*v/(2*c.m),'rounded_scalar_bound_at_interfaces')
        states=set()
        for a in range(4):
            for b in range(4):
                for x in range(4):
                    for y in range(4):states.add((a,b,x,y))
        for _ in range(100): states.add(tuple(rng.randrange(2*R+4) for j in range(4)))
        # Boundary, ramp, saturation, and very unequal waiting rooms.
        for y in [0,1,R//2,R-1,R]:
            for x in [c.N,c.N+1,2*c.N]:
                D=x+y+1
                bs={0,ceil(c.ga*D)-1,ceil(c.ga*D),ceil((c.ga+c.eta)*D/2),ceil(c.eta*D)-1,ceil(c.eta*D),2*D}
                for b in bs:
                    for a in [0,1,2*D]:
                        states.add((a,b,x,y)); states.add((b,a,y,x))
        # Large both, just outside the support, and bounded-visible huge waiting.
        for x in [R+1,R+2,2*R,c.N]:
            for y in [R+1,R+2,2*R]:
                for a,b in [(0,0),(1,1),(c.N,2*c.N)]:states.add((a,b,x,y))
        big=ceil(c.B)+1
        for x,y in [(0,0),(0,R),(R,0),(R,R),(c.N-1,0),(1,1)]:
            for a,b in [(big,0),(0,big),(big,big)]:states.add((a,b,x,y))
        for s in sorted(states):c.check_state(s)
        reports.append({'lambda':str(la),'R':R,'N':c.N,'B_ceiling':ceil(c.B),
                        'G_approx':float(c.G),'mu_approx':float(c.mu),'state_checks':len(states)})
        print('finished lambda='+str(la)+' states='+str(len(states)),file=sys.stderr,flush=True)
    return {'status':'PASS','assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),
            'parameter_examples':reports,'scope':'Finite exact rational controls of every displayed interface and generator bound; the universal proof is TURN_4.md.'}
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
