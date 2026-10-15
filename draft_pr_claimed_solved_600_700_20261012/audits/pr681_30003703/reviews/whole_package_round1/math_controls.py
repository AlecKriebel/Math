#!/usr/bin/env python3
"""Fresh whole-review controls, with no native or audit code imports."""
import itertools
import json
from sympy import Matrix, symbols, expand


def need(x, label):
    if not x: raise RuntimeError(label)


def br(x,y): return x*y-y*x
def p(x,y,z): return br(br(br(x,y),br(x,z)),x)
def invword(w): return tuple(-x for x in reversed(w))
def comm(a,b): return a+b+invword(a)+invword(b)


def mm(a,b,add=lambda x,y:x+y,mul=lambda x,y:x*y):
    n=len(a);out=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):out[i][j]=add(out[i][j],mul(a[i][k],b[k][j]))
    return out


def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def plus(a,b,sgn=1):return [[x+sgn*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def unipotent_inverse(a):
    n=len(a);delta=plus(a,eye(n),-1);power=eye(n);out=eye(n)
    need(all(delta[i][j]==0 for i in range(n) for j in range(i+1)),'upper nilpotence')
    for k in range(1,n):power=mm(power,delta);out=plus(out,power,(-1)**k)
    need(mm(a,out)==mm(out,a)==eye(n),'two sided inverse')
    return out


def evalword(w,images):
    inverses=[unipotent_inverse(a) for a in images];out=eye(len(images[0]))
    for s in w:out=mm(out, images[s-1] if s>0 else inverses[-s-1])
    return out


def ring_p(x,y,z,add,mul,negative):
    def minus(a,b):return [[add(u,negative(v)) for u,v in zip(r,s)] for r,s in zip(a,b)]
    def bracket(a,b):return minus(mm(a,b,add,mul),mm(b,a,add,mul))
    return bracket(bracket(bracket(x,y),bracket(x,z)),x)


def main():
    checks={}
    mats=[Matrix(2,2,symbols(f'{name}0:4')) for name in ['a','b','c']]
    x,y,z=mats
    checks['P_all_twelve_independent_commuting_entries']=all(expand(t)==0 for t in p(x,y,z))
    checks['Q_all_eight_independent_commuting_entries']=all(expand(t)==0 for t in p(x,y,br(x,y)))
    X,Y,Z=symbols('X Y Z',commutative=False)
    P=expand(p(X,Y,Z));Q=expand(p(X,Y,br(X,Y)))
    checks['integral_P_target_coefficient']=P.as_coefficients_dict()[X*X*Y*X*Z]==-1
    checks['integral_Q_target_coefficient']=Q.as_coefficients_dict()[X*X*X*Y*X*Y]==1
    checks['P_Q_nonconstant_term_counts']=len(P.as_ordered_terms())==12 and len(Q.as_ordered_terms())==10
    # Characteristic two exhaustive M2 triples (all 4096 triples).
    mats2=[[[a,b],[c,d]] for a,b,c,d in itertools.product(range(2),repeat=4)]
    for a,b,c in itertools.product(mats2,repeat=3):
        need(ring_p(a,b,c,lambda u,v:u^v,lambda u,v:u&v,lambda u:u)==[[0,0],[0,0]],'F2 P')
    checks['all_4096_M2_F2_triples']=True
    # Encoded dual numbers a+eps*b in F2[eps]/eps^2, so eps is nonzero nilpotent.
    dual_mul=lambda u,v:((u&1)*(v&1)) ^ (2*((((u&1)*(v>>1))^((u>>1)*(v&1)))&1))
    for k in range(128):
        m=[[[(((k+1)*(2*h+1)+17*h)>>(2*(2*i+j)))&3 for j in range(2)] for i in range(2)] for h in range(3)]
        need(ring_p(*m,lambda u,v:u^v,dual_mul,lambda u:u)==[[0,0],[0,0]],'dual P')
    checks['128_nonreduced_F2_dual_number_triples']=True
    for k in range(128):
        m=[[[(((k+1)*(2*h+1)+17*h)>>(2*(2*i+j)))&3 for j in range(2)] for i in range(2)] for h in range(3)]
        need(ring_p(*m,lambda u,v:(u+v)%4,lambda u,v:(u*v)%4,lambda u:(-u)%4)==[[0,0],[0,0]],'Z4 P')
    checks['128_Z_mod_4_triples_no_division']=True
    gx,gy,gz=(1,),(2,),(3,)
    w=comm(comm(comm(gx,gy),comm(gx,gz)),gx)
    v=comm(comm(comm(gx,gy),comm(gx,comm(gx,gy))),gx)
    witnesses={}
    for name,word,rank,target,sign in [('w',w,3,(1,1,2,1,3),-1),('v',v,2,(1,1,1,2,1,2),1)]:
        d=len(target)+1;images=[eye(d) for _ in range(rank)]
        for i,color in enumerate(target):images[color-1][i][i+1]=1
        found=evalword(word,images);want=eye(d);want[0][-1]=sign
        need(found==want,name+' exact full witness')
        checks[name+'_integer_UT_full_matrix']=True
        witnesses[name]=found
    H=Matrix.diag(1,-1,0);E=Matrix([[0,1,0],[0,0,0],[0,0,0]]);F=Matrix([[0,0,0],[0,0,1],[0,0,0]])
    checks['SL3_extension_fails']=p(H,E,F)==Matrix([[0,0,2],[0,0,0],[0,0,0]])
    need(all(checks.values()),str({k:v for k,v in checks.items() if not v}))
    print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'UT_witnesses':witnesses,
                     'P_free_expansion':str(P),'Q_free_expansion':str(Q),
                     'no_parent_code_imported':True,'role':'Independent exact controls; universal proof is in DERIVATION.md'},indent=2,sort_keys=True))


if __name__=='__main__':main()
