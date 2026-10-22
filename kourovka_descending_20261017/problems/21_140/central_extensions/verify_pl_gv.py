#!/usr/bin/env python3
"""Exact-rational checks for the mirrored-clone homology-zero embedding.

These finite checks support the written derivation; they do not establish the
universal identities or the imported homology theorem.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
import json
import random


@dataclass(frozen=True)
class PL:
    points: tuple

    def __post_init__(self):
        assert self.points[0] == (Q(0), Q(0))
        assert self.points[-1] == (Q(1), Q(1))
        assert all(x < z and y < w for (x,y),(z,w) in zip(self.points,self.points[1:]))

    def __call__(self, x):
        x=Q(x)
        for (a,b),(c,d) in zip(self.points,self.points[1:]):
            if a <= x <= c:
                return b+(x-a)*(d-b)/(c-a)
        raise ValueError(x)

    def inv(self):
        return PL(tuple((y,x) for x,y in self.points))

    def __mul__(self, h):
        # g*h = g o h. Include pullbacks of every breakpoint of g.
        xs=sorted({x for x,y in h.points} | {h.inv()(x) for x,y in self.points})
        return PL(tuple((x,self(h(x))) for x in xs)).reduce()

    def reduce(self):
        pts=[]
        for p in self.points:
            pts.append(p)
            while len(pts)>2:
                (a,b),(c,d),(e,f)=pts[-3:]
                if (d-b)*(e-c) != (f-d)*(c-a):
                    break
                pts.pop(-2)
        return PL(tuple(pts))

    def slopes_at(self, x):
        # Derivatives on S^1: the left derivative at zero is at 1-.
        x=Q(x)
        slopes=[(d-b)/(c-a) for (a,b),(c,d) in zip(self.points,self.points[1:])]
        if x==0:
            return slopes[-1],slopes[0]
        for i,((a,b),(c,d)) in enumerate(zip(self.points,self.points[1:])):
            if a < x < c:
                return slopes[i],slopes[i]
            if x==c:
                return slopes[i],slopes[(i+1)%len(slopes)]
        raise ValueError(x)

    def reflect(self):
        return PL(tuple((1-x,1-y) for x,y in reversed(self.points)))

    def clone(self, a, b):
        a,b=Q(a),Q(b)
        pts={(Q(0),Q(0)),(Q(1),Q(1))}
        pts.update((a+(b-a)*x,a+(b-a)*y) for x,y in self.points)
        return PL(tuple(sorted(pts))).reduce()


ONE=PL(((Q(0),Q(0)),(Q(1),Q(1))))
A=PL(((Q(0),Q(0)),(Q(1,2),Q(1,4)),(Q(3,4),Q(1,2)),(Q(1),Q(1))))
B=A.clone(Q(1,2),Q(1))


def log2q(x):
    assert x>0
    n,d=x.numerator,x.denominator
    assert n & (n-1)==0 and d & (d-1)==0
    return n.bit_length()-d.bit_length()


def gv(g,h):
    gh=g*h
    total=0
    for x in sorted(({x for x,y in h.points}|{x for x,y in gh.points})-{Q(1)}):
        hl,hr=map(log2q,h.slopes_at(x))
        pl,pr=map(log2q,gh.slopes_at(x))
        total += hr*(pr-pl)-pr*(hr-hl)
    return total


def mirrored(f):
    k=f.clone(Q(1,8),Q(3,8))
    return k*k.reflect()


def main():
    u=A*B.inv()
    v=A.inv()*B*A
    assert u*v==v*u
    eta1=gv(u,v)-gv(v,u)
    v2=A.inv()*A.inv()*B*A*A
    eta2=gv(u,v2)-gv(v2,u)
    assert eta1==0 and eta2==-2
    left=A.clone(0,Q(1,4))
    right=A.clone(Q(3,4),1)
    endpoint_gv=gv(left,right)-gv(right,left)
    assert endpoint_gv==-2
    adjacent_left=A.clone(Q(1,4),Q(1,2))
    adjacent_right=A.clone(Q(1,2),Q(3,4))
    assert adjacent_left*adjacent_right==adjacent_right*adjacent_left
    adjacent_gv=gv(adjacent_left,adjacent_right)-gv(adjacent_right,adjacent_left)
    assert adjacent_gv==2
    rng=random.Random(21140)
    gens=[A,B,A.inv(),B.inv()]
    samples=[ONE,A,B,A.inv(),B.inv(),u,v]
    for _ in range(50):
        f=ONE
        for _ in range(rng.randrange(1,18)):
            f=f*rng.choice(gens)
        samples.append(f)
    checks={'reflection':0,'clone_additivity':0,'mirrored_zero':0,'homomorphism':0,'cocycle':0}
    for _ in range(300):
        f,g,h=(rng.choice(samples) for _ in range(3))
        assert gv(f.reflect(),g.reflect())==-gv(f,g)
        checks['reflection']+=1
        kf=f.clone(Q(1,8),Q(3,8)); kg=g.clone(Q(1,8),Q(3,8))
        assert gv(kf*kf.reflect(),kg*kg.reflect())==gv(kf,kg)+gv(kf.reflect(),kg.reflect())
        checks['clone_additivity']+=1
        assert gv(mirrored(f),mirrored(g))==0
        checks['mirrored_zero']+=1
        assert mirrored(f*g)==mirrored(f)*mirrored(g)
        checks['homomorphism']+=1
        assert gv(g,h)-gv(f*g,h)+gv(f,g*h)-gv(f,g)==0
        checks['cocycle']+=1
    print(json.dumps({'arithmetic':'fractions.Fraction; no floating point','random_seed':21140,
      'sample_count':len(samples),'source_eta1_circle_gv':eta1,'source_eta2_circle_gv':eta2,
      'separated_endpoint_cycle':{'cup':-1,'circle_gv':endpoint_gv},
      'adjacent_interior_cycle':{'cup':0,'circle_gv':adjacent_gv},
      'checks_passed':checks},indent=2))

if __name__=='__main__':
    main()
