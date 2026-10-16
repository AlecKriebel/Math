#!/usr/bin/env python3
"""Small exact diagnostics for PROOF.md; these do not verify its global proof.
Standard library only. All checks remain active under python -O.
"""
from fractions import Fraction as Q
import json

COUNT = 0

def require(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(message)


def zero(n): return [Q(0)] * n

def add(x, y): return [a+b for a,b in zip(x,y)]

def neg(x): return [-a for a in x]

def sub(x,y): return add(x,neg(y))

def basis(n): return [[Q(i==j) for i in range(n)] for j in range(n)]

def columns(v): return [list(row) for row in zip(*v)]

def identity(n): return columns(basis(n))

def apply(a,x): return [sum(t*u for t,u in zip(r,x)) for r in a]

def mm(a,b): return columns([apply(a,c) for c in zip(*b)])

def madd(a,b): return [add(x,y) for x,y in zip(a,b)]

def mneg(a): return [neg(x) for x in a]

def msub(a,b): return madd(a,mneg(b))

def rank(a):
    a=[list(map(Q,row)) for row in a]
    r=0
    for c in range(len(a[0]) if a else 0):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        pivot=a[r][c]; a[r]=[t/pivot for t in a[r]]
        for i in range(len(a)):
            if i!=r:
                t=a[i][c]; a[i]=[u-t*v for u,v in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r


def det(a):
    a=[list(map(Q,row)) for row in a]
    d=Q(1)
    for c in range(len(a)):
        p=next((i for i in range(c,len(a)) if a[i][c]),None)
        if p is None: return Q(0)
        if p!=c: a[c],a[p]=a[p],a[c]; d=-d
        v=a[c][c]; d*=v
        for i in range(c+1,len(a)):
            q=a[i][c]/v
            for j in range(c+1,len(a)): a[i][j]-=q*a[c][j]
    return d


def sl2(x,y):
    e,f,h=x; E,F,H=y
    return [2*(h*E-e*H),2*(f*H-h*F),e*F-f*E]


def direct_sl2(x,y):
    return sum((sl2(x[i:i+3],y[i:i+3]) for i in range(0,len(x),3)),[])


def traces(bracket,n):
    e=basis(n)
    return [sum(bracket(x,e[j])[j] for j in range(n)) for x in e]


def derived_rank(bracket,n):
    e=basis(n)
    return rank(columns([bracket(x,y) for x in e for y in e]))


def verify_pa(name,n,target,product):
    e=basis(n)
    source=lambda x,y:add(target(x,y),sub(product(x,y),product(y,x)))
    for x in e:
        for y in e:
            require(sub(product(x,y),product(y,x))==sub(source(x,y),target(x,y)),name+': PA1')
            for z in e:
                require(product(source(x,y),z)==sub(product(x,product(y,z)),product(y,product(x,z))),name+': PA2')
                require(product(x,target(y,z))==add(target(product(x,y),z),target(y,product(x,z))),name+': PA3')
                jac=add(source(x,source(y,z)),add(source(y,source(z,x)),source(z,source(x,y))))
                require(jac==zero(n),name+': Jacobi')
    return source


def inv2(p):
    require(det(p)==1,'SL2 determinant')
    a,b=p[0];c,d=p[1]
    return [[d,-b],[-c,a]]


def adjoint(p):
    pinv=inv2(p)
    def act(x):
        e,f,h=x; v=mm(mm(p,[[h,e],[f,-h]]),pinv)
        return [v[0][1],v[1][0],v[0][0]]
    a=columns([act(x) for x in basis(3)])
    require(det(a)==1,'det Ad_SL2')
    return a


def blockdiag(a,b):
    return [r+zero(len(b)) for r in a]+[zero(len(a))+r for r in b]


def bp(p,j1,j2): return msub(mm(adjoint(inv2(p)),j1),j2)

def bp2(p,q,j1,j2): return msub(mm(blockdiag(adjoint(inv2(p)),adjoint(inv2(q))),j1),j2)


def main():
    report={}
    I=identity(3); Z=[zero(3) for _ in range(3)]
    cases={'zero_R':Z,'minus_identity_R':mneg(I),'triangular_R':[[Q(-1),0,0],[0,0,0],[0,0,Q(-1)]]}
    matrices=[[[Q(1),Q(0)],[Q(0),Q(1)]],[[Q(0),Q(-1)],[Q(1),Q(0)]]]
    for t in [-2,-1,0,1,2]:
        for a in [Q(1,2),Q(1),Q(2)]:
            matrices.append([[a,Q(t)],[Q(1),Q(t+1)/a]])
    for name,R in cases.items():
        prod=lambda x,y:sl2(apply(R,x),y)
        source=verify_pa(name,3,sl2,prod)
        j1=madd(R,I);j2=R
        for x in basis(3):
            for y in basis(3):
                require(apply(j1,source(x,y))==sl2(apply(j1,x),apply(j1,y)),name+': j1 hom')
                require(apply(j2,source(x,y))==sl2(apply(j2,x),apply(j2,y)),name+': j2 hom')
        fs=[det(bp(p,j1,j2)) for p in matrices]
        if name=='triangular_R':
            require(fs==[p[0][0]**2 for p in matrices],'triangular determinant is a^2')
            require(traces(source,3)==[0,0,-2],'triangular nonunimodularity')
            require(fs[0]==1 and fs[1]==0,'nonunimodular negative control')
            # Check full covariance, retaining the nontrivial modular factor.
            for r in [Q(1,2),Q(1),Q(2)]:
                l=[[Q(1),Q(0)],[Q(2),Q(1)]]
                b=[[r,Q(3)],[Q(0),1/r]]
                T=msub(mm(adjoint(l),j1),mm(adjoint(b),j2))
                # Equivalently multiply covariance by T, avoiding inversion.
                for p in matrices:
                    moved=mm(mm(l,p),inv2(b))
                    require(mm(bp(moved,j1,j2),T)==mm(adjoint(b),bp(p,j1,j2)),'triangular covariance')
                    require(det(bp(moved,j1,j2))*det(T)==det(bp(p,j1,j2)),'modular factor')
        else:
            require(all(v==1 for v in fs),name+': determinant is one')
            require(traces(source,3)==zero(3),name+': unimodularity')
        report[name]={'dimension':3,'derived_rank':derived_rank(source,3),'adjoint_traces':list(map(str,traces(source,3))),'group_points':len(matrices)}
    # A genuinely nonzero, nonsplitting R on sl2 direct sum sl2: R(a,b)=(0,a).
    R=columns([zero(3)+x[:3] for x in basis(6)])
    j1=madd(identity(6),R);j2=R
    source=verify_pa('mixed_semisimple',6,direct_sl2,lambda x,y:direct_sl2(apply(R,x),y))
    require(mm(R,R)==[zero(6) for _ in range(6)],'R squared zero')
    require(rank(R)==3,'R nonzero rank')
    for x in basis(6):
        for y in basis(6):
            require(apply(j1,source(x,y))==direct_sl2(apply(j1,x),apply(j1,y)),'mixed source isomorphism')
            require(apply(j2,source(x,y))==direct_sl2(apply(j2,x),apply(j2,y)),'mixed j2 homomorphism')
    F=j1; Finv=msub(identity(6),R)
    for i,p in enumerate(matrices):
        q=matrices[(i+3)%len(matrices)];u=matrices[(i+5)%len(matrices)];v=matrices[(i+7)%len(matrices)]
        T=mm(mm(Finv,blockdiag(adjoint(u),adjoint(v))),F)
        movedp=mm(u,p);movedq=mm(mm(v,q),inv2(u))
        B=bp2(p,q,j1,j2); Bm=bp2(movedp,movedq,j1,j2)
        require(mm(Bm,T)==mm(blockdiag(I,adjoint(u)),B),'mixed covariance')
        require(det(B)==1 and det(Bm)==1 and det(T)==1,'mixed constant determinant')
    report['mixed_semisimple']={'dimension':6,'derived_rank':derived_rank(source,6),'adjoint_traces':list(map(str,traces(source,6))),'group_points':len(matrices)}
    # Reductive-target boundary case, credited to Burde et al., Example 3.13.
    def reductive(x,y): return sl2(x[:3],y[:3])+zero(2)
    def natural_product(x,y):
        e,f,h=x[:3];v,w=y[3:]
        return zero(3)+[h*v+e*w,f*v-h*w]
    source=verify_pa('reductive_target',5,reductive,natural_product)
    require(derived_rank(source,5)==5,'perfect source')
    require(derived_rank(reductive,5)==3,'target not semisimple')
    require(traces(source,5)==zero(5),'perfect source unimodular')
    for x in basis(5):
        for y in basis(5)[3:]:require(source(x,y)[:3]==zero(3),'nonzero abelian ideal')
    for x in basis(5)[3:]:
        for y in basis(5)[3:]:require(source(x,y)==zero(5),'radical abelian')
    report['reductive_target']={'dimension':5,'source_derived_rank':5,'target_derived_rank':3,'abelian_radical_dimension':2}
    # A bad choice R=I must fail the homomorphism condition: do not merely test successes.
    bad_source=lambda x,y:[3*z for z in sl2(x,y)]
    violations=sum(bad_source(x,y)!=sl2(x,y) for x in basis(3) for y in basis(3))
    require(violations>0,'invalid R negative control must fail')
    report['invalid_R_identity_detected']=True
    report['checks']=COUNT
    report['scope']='Exact finite diagnostics only; not a verification of integration, covering theory, or homology.'
    return report

if __name__=='__main__': print(json.dumps(main(),indent=2,sort_keys=True))
