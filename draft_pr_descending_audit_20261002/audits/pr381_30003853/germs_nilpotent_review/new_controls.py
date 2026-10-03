#!/usr/bin/env python3
"""Independent exact models; no imported candidate code or finite-proof oracle."""
from fractions import Fraction as F
from itertools import product
import json

checks = 0
def ck(p):
    global checks
    assert p
    checks += 1

# A PL map uses affine segments (left, right, slope, intercept), unlike the
# author's vertex representation. Every calculation is exact rational.
class PL:
    def __init__(self, segments):
        out = []
        for lo, hi, a, b in segments:
            lo, hi, a, b = map(F, (lo, hi, a, b))
            assert lo < hi and a > 0
            if out and out[-1][2:] == (a, b):
                out[-1] = (out[-1][0], hi, a, b)
            else:
                out.append((lo, hi, a, b))
        assert out[0][0] == 0 and out[-1][1] == 1
        assert out[0][3] == 0 and out[-1][2] + out[-1][3] == 1
        for u, v in zip(out, out[1:]):
            assert u[1] == v[0] and u[2]*u[1]+u[3] == v[2]*v[0]+v[3]
        self.s = tuple(out)
    @classmethod
    def vertices(cls, pairs):
        p = [tuple(map(F, z)) for z in pairs]
        return cls([(x, X, (Y-y)/(X-x), y-(Y-y)*x/(X-x))
                    for (x,y),(X,Y) in zip(p,p[1:])])
    def __eq__(self, other): return self.s == other.s
    def at(self, x):
        x = F(x)
        for lo, hi, a, b in self.s:
            if lo <= x <= hi: return a*x+b
        raise ValueError(x)
    def inverse(self):
        return PL([(a*lo+b,a*hi+b,1/a,-b/a) for lo,hi,a,b in self.s])
    def after(self, g):
        cuts = {lo for lo,hi,a,b in g.s}|{F(1)}
        gi = g.inverse()
        cuts |= {gi.at(lo) for lo,hi,a,b in self.s}
        out=[]
        for lo, hi in zip(sorted(cuts),sorted(cuts)[1:]):
            q=(lo+hi)/2
            gs=next(z for z in g.s if z[0]<q<z[1])
            y=g.at(q)
            fs=next(z for z in self.s if z[0]<y<z[1])
            out.append((lo,hi,fs[2]*gs[2],fs[2]*gs[3]+fs[3]))
        return PL(out)
    def power(self, n):
        a = self if n>=0 else self.inverse()
        r = identity
        for _ in range(abs(n)): r = r.after(a)
        return r
    def support(self):
        cuts={lo for lo,hi,a,b in self.s}|{F(1)}
        for lo,hi,a,b in self.s:
            if a!=1 and lo<-b/(a-1)<hi: cuts.add(-b/(a-1))
        out=[]
        for lo,hi in zip(sorted(cuts),sorted(cuts)[1:]):
            q=(lo+hi)/2
            if self.at(q)!=q:
                if out and out[-1][1]==lo and self.at(lo)!=lo:
                    out[-1]=(out[-1][0],hi)
                else: out.append((lo,hi))
        return out
    def germ(self, x, right=True):
        x=F(x)
        return next(a for lo,hi,a,b in self.s if
                    (lo<=x<hi if right else lo<x<=hi))
    def is_F(self):
        def dyadic(q): return q.denominator & (q.denominator-1)==0
        def two_power(q): return (q.numerator & (q.numerator-1)==0
                                 and q.denominator & (q.denominator-1)==0)
        return all(dyadic(lo) and dyadic(hi) and dyadic(a*lo+b)
                   and two_power(a) for lo,hi,a,b in self.s)

identity=PL([(0,1,1,0)])
def bump(lo,hi):
    lo,hi=F(lo),F(hi);d=hi-lo
    p=[(0,0),(lo,lo),(lo+d/2,lo+d/4),(lo+3*d/4,lo+d/2),(hi,hi),(1,1)]
    return PL.vertices([z for i,z in enumerate(p) if not i or z!=p[i-1]])
def comm(x,y): return x.after(y).after(x.inverse()).after(y.inverse())
def conjugate(t,x): return t.after(x).after(t.inverse())

def pl_controls():
    t=bump(0,1); a=bump(F(1,2),F(3,4))
    lamps={i:conjugate(t.power(i),a) for i in range(-8,9)}
    for i,b in lamps.items():
        ck(b.is_F());ck(b.support()==[(t.power(i).at(F(1,2)),t.power(i).at(F(3,4)))])
        ck(b.after(b.inverse())==identity)
    for i,j in product(lamps,repeat=2): ck(comm(lamps[i],lamps[j])==identity)
    # r = a_1 a_0^{-1}; r^m is the actual commutator [t,a_0^m].
    r=lamps[1].after(lamps[0].inverse())
    torsion=[]
    for m in (2,3,4,6,8,12):
        s=a.power(m)
        ck(r.power(m)==comm(t,s));ck(r!=identity);ck(comm(t,r)!=identity)
        ck(r.germ(0)==r.germ(1,False)==1)
        torsion.append({'m':m,'relation':'r^m=[t,a_0^m]','exact_class_order':m,
                        'finite_presentation':'not certified by this model'})
    # This r has two support components meeting at a fixed point. Its own
    # right germ at 1/4 is nontrivial, even though the H orbital germs vanish.
    ck(r.support()==[(F(1,4),F(1,2)),(F(1,2),F(3,4))])
    ck(r.germ(F(1,4))==F(1,2));ck(t.at(F(1,4))!=F(1,4))
    # Genuine F element with an isolated nondyadic common fixed point.
    f=PL.vertices([(0,0),(F(1,4),F(1,8)),(F(3,8),F(5,8)),(F(1,2),F(3,4)),(1,1)])
    nd=F(7,24);ck(f.is_F());ck(f.at(nd)==nd)
    ck(f.support()==[(F(0),nd),(nd,F(1))]);ck(f.germ(nd)==4)
    for n in range(-9,10): ck(f.power(n).germ(nd)==F(4)**n)
    # A common endpoint character is defined separately on each component.
    left=bump(F(1,8),F(1,4));right=bump(F(1,2),F(3,4))
    ck(comm(left,right)==identity)
    ck(left.after(right).support()==[(F(1,8),F(1,4)),(F(1,2),F(3,4))])
    for i,j in product(range(-4,5),repeat=2):
        w=left.power(i).after(right.power(j))
        ck(w.germ(F(1,8))==F(1,2)**i)
        ck(w.germ(F(1,2))==F(1,2)**j)
    return {'torsion_witness_models':torsion,'witness_support':[[str(x),str(y)] for x,y in r.support()],
            'witness_internal_germ':'1/2','witness_global_germs':['1','1'],
            'nondyadic_F_fixed_point':str(nd),'nondyadic_right_germ':'4'}

# Matrix implementation is independent of the candidate's triple product.
I=((1,0,0),(0,1,0),(0,0,1))
def mm(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def mi(A):
    u,v,w=A[0][1],A[1][2],A[0][2]
    return ((1,-u,u*v-w),(0,1,-v),(0,0,1))
def mp(A,n):
    r=I; B=A if n>=0 else mi(A)
    for _ in range(abs(n)): r=mm(r,B)
    return r
def mc(A,B):return mm(mm(mm(A,B),mi(A)),mi(B))
def M(m,a,b,c):return ((1,m*a,c),(0,1,b),(0,0,1))
def coords(m,A):return (A[0][1]//m,A[1][2],A[0][2])
def nilpotent_controls():
    p=list(product(range(-2,3),repeat=3));results=[]
    for m in (1,2,3,4,6,8,12):
        x,y,z=M(m,1,0,0),M(m,0,1,0),M(m,0,0,1)
        ck(mc(x,y)==mp(z,m));ck(mc(x,z)==I);ck(mc(y,z)==I)
        for a,b,c in p:
            A=M(m,a,b,c)
            ck(mm(mm(mp(x,a),mp(y,b)),mp(z,c-m*a*b))==A)
            ck(mm(A,mi(A))==I)
            for n in (-5,-3,-1,0,1,2,4):
                ck(mp(A,n)==M(m,n*a,n*b,n*c+m*n*(n-1)*a*b//2))
            for d,e,f in p:
                B=M(m,d,e,f)
                ck(mm(A,B)==M(m,a+d,b+e,c+f+m*a*e))
                ck(mc(A,B)==M(m,0,0,m*(a*e-d*b)))
                ck((coords(m,mm(mm(mi(B),A),B))>(0,0,0))==((a,b,c)>(0,0,0)))
                if (a,b,c)>(0,0,0) and (d,e,f)>(0,0,0):ck(coords(m,mm(A,B))>(0,0,0))
                # Reproducible signed balanced-power controls.
                for pp,qq in ((1,2),(-1,1),(2,-2),(-2,-2)):
                    relation=mm(mm(mi(B),mp(A,pp)),B)==mp(A,qq)
                    ck(not relation or A==I or pp==qq)
        for n in (1,2,3,4): ck(len({mp(M(m,*u),n) for u in p})==len(p))
        # z -> 1 mod m is a homomorphism from the presentation; all commutators
        # are multiples of m. Together these certify exact order, including m=1.
        ck(mc(x,y)==M(m,0,0,m))
        results.append({'m':m,'z_infinite_order':True,'z_class_order':m,
                        'abelianization':'Z^2 + Z/'+str(m),
                        'nonembedding_PL':'proved by one-bump centralizer, not finite tests'})
    return results

if __name__=='__main__':
    pl=pl_controls();nil=nilpotent_controls()
    print(json.dumps({'assertions':checks,'PL':pl,'nilpotent':nil,
                      'scope':'bounded exact model checks; general conclusions require the separate proofs'},sort_keys=True,indent=2))
