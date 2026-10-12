#!/usr/bin/env python3
"""Candidate-free exact controls for quotient stable norms and integral torsion."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm
import json, random
from pathlib import Path

OUT=Path(__file__).resolve().parent

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def rows_of(cols,d): return [[F(c[i]) for c in cols] for i in range(d)]
def rref(A):
    A=[[F(x) for x in row] for row in A]; piv=[]; r=0
    for c in range(len(A[0]) if A else 0):
        p=next((i for i in range(r,len(A)) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]; z=A[r][c]; A[r]=[v/z for v in A[r]]
        for i in range(len(A)):
            if i!=r:
                z=A[i][c]; A[i]=[v-z*w for v,w in zip(A[i],A[r])]
        piv.append(c);r+=1
        if r==len(A):break
    return A,piv

def solve(A,b,ncols=None):
    ncols = len(A[0]) if A else ncols
    E,piv=rref([row+[v] for row,v in zip(A,b)])
    if any(all(not v for v in row[:ncols]) and row[ncols] for row in E): return None
    x=[F(0)]*ncols
    for row,c in zip(E,piv):
        if c<ncols:x[c]=row[ncols]
    return x

def nullspace(A,d):
    if not A:return [[F(i==j) for i in range(d)] for j in range(d)]
    E,piv=rref(A);free=[j for j in range(d) if j not in piv];ans=[]
    for j in free:
        x=[F(0)]*d;x[j]=1
        for row,c in zip(E,piv):x[c]=-row[j]
        ans.append(x)
    return ans

def diagonalize(cols,d):
    """Unimodular row+column Euclidean diagonalization, no external algebra imports."""
    A=[[int(c[i]) for c in cols] for i in range(d)];n=len(cols)
    U=[[int(i==j) for j in range(d)] for i in range(d)]
    def swaprow(i,j):A[i],A[j]=A[j],A[i];U[i],U[j]=U[j],U[i]
    def swapcol(i,j):
        for row in A:row[i],row[j]=row[j],row[i]
    def subtractrow(i,j,q):
        A[i]=[x-q*y for x,y in zip(A[i],A[j])];U[i]=[x-q*y for x,y in zip(U[i],U[j])]
    k=0
    while k<min(d,n):
        nz=[(abs(A[i][j]),i,j) for i in range(k,d) for j in range(k,n) if A[i][j]]
        if not nz:break
        _,i,j=min(nz);swaprow(k,i);swapcol(k,j)
        while True:
            changed=False
            for i in range(k+1,d):
                if A[i][k]:
                    q=A[i][k]//A[k][k];subtractrow(i,k,q)
                    if A[i][k]:swaprow(k,i)
                    changed=True;break
            if changed:continue
            for j in range(k+1,n):
                if A[k][j]:
                    q=A[k][j]//A[k][k]
                    for row in A:row[j]-=q*row[k]
                    if A[k][j]:swapcol(k,j)
                    changed=True;break
            if not changed:break
        if A[k][k]<0:subtractrow(k,k,2)
        k+=1
    assert all(not A[i][j] for i in range(d) for j in range(n) if i!=j)
    D=[A[i][i] if i<n else 0 for i in range(d)]
    return D,U

def key(v,D,U):
    w=[dot(row,v) for row in U]
    return tuple(x%z if z else x for x,z in zip(w,D))
def member(v,D,U):return not any(key(v,D,U))

def primal_dual(R,S,v):
    d=len(v);B=nullspace(R,d);q=len(B);P=[tuple(dot(b,s) for b in B) for s in S];w=[dot(b,v) for b in B]
    if q==0:return F(0),[F(0)]*len(S),[F(0)]*d,0
    signed=[(j,z,tuple(z*x for x in p)) for j,p in enumerate(P) for z in [1,-1]]
    primal=[];dual=[];count=0
    for inds in combinations(range(len(signed)),q):
        selected=[signed[i] for i in inds];C=rows_of([x[2] for x in selected],q)
        _,pv=rref(C)
        if len(pv)!=q:continue
        t=solve(C,w)
        if min(t)>=0:
            a=[F(0)]*len(S)
            for (j,z,_),c in zip(selected,t):a[j]+=z*c
            primal.append((sum(t),a))
        # The signed vectors are rows of active dual equations.
        y=solve([list(x[2]) for x in selected],[1]*q)
        if all(abs(dot(y,p))<=1 for p in P):
            ell=[sum(y[i]*B[i][j] for i in range(q)) for j in range(d)]
            dual.append((dot(y,w),ell))
        count+=1
    assert primal and dual,'requires real spanning'
    value,a=min(primal,key=lambda p:p[0]); dv,ell=max(dual,key=lambda p:p[0]);assert value==dv
    assert all(dot(ell,r)==0 for r in R) and all(abs(dot(ell,s))<=1 for s in S)
    assert dot(ell,v)==value
    return value,a,ell,count

def cert(R,S,v,a):
    d=len(v);res=[F(v[i])-sum(a[j]*S[j][i] for j in range(len(S))) for i in range(d)]
    c=solve(rows_of(R,d),res,len(R));assert c is not None
    m=lcm(*(x.denominator for x in list(a)+list(c)))
    assert all((m*x).denominator==1 for x in list(a)+list(c))
    assert all(m*v[i]==sum(m*a[j]*S[j][i] for j in range(len(S)))+sum(m*c[j]*R[j][i] for j in range(len(R))) for i in range(d))
    return m,c

def distances(R,S,targets,maxradius=30):
    d=len(targets[0]);D,U=diagonalize(R,d);zero=key([0]*d,D,U);wanted={key(v,D,U) for v in targets};dist={zero:0};front={zero}
    steps=[key([z*x for x in s],D,U) for s in S for z in [1,-1]]
    for radius in range(1,maxradius+1):
        if wanted<=dist.keys():break
        nxt=set()
        for x in front:
            for s in steps:
                y=tuple((a+b)%c if c else a+b for a,b,c in zip(x,s,D))
                if y not in dist:dist[y]=radius;nxt.add(y)
        front=nxt
    assert wanted<=dist.keys(),'word targets not reached in finite control radius'
    return [dist[key(v,D,U)] for v in targets]

def run_case(name,R,S,v,wordcheck=True):
    d=len(v);D,U=diagonalize(R+S,d)
    assert all(member([int(i==j) for i in range(d)],D,U) for j in range(d)), 'failed integral generator validation'
    value,a,ell,bases=primal_dual(R,S,v);m,c=cert(R,S,v,a)
    D,U=diagonalize(R,d);torsion=all(not dot(b,v) for b in nullspace(R,d))
    assert (value==0)==torsion
    if torsion:assert member([m*x for x in v],D,U)
    lengths=[]; error_bound=None
    if wordcheck:
        powers=list(range(1,13));targets=[[n*x for x in v] for n in powers]
        lengths=distances(R,S,targets,maxradius=max(42,12*sum(abs(x) for x in v)))
        assert all(F(k)>=n*value for n,k in zip(powers,lengths))
        block=distances(R,S,[[m*x for x in v]],maxradius=max(42,int(m*value))) [0]
        assert F(block)==m*value
        if m<=30:
            remainders=distances(R,S,[[r*x for x in v] for r in range(m)],maxradius=max(42,m*sum(abs(x) for x in v)))
            error_bound=max(F(k)-r*value for r,k in enumerate(remainders))
            assert all(F(k)<=n*value+error_bound for n,k in zip(powers,lengths))
    return {'name':name,'relations':R,'generators':S,'element':v,'lp':str(value),'primal':[str(x) for x in a],'dual':[str(x) for x in ell],'block_power':m,'relator_coefficients':[str(x) for x in c],'basis_count':bases,'word_lengths_n_1_to_12':lengths,'torsion_in_abelianization':torsion,'additive_error_bound':None if error_bound is None else str(error_bound)}

def main():
    cases=[
      ('Z_fractional_cost',[],[[2],[3]],[1]),
      ('finite_C6',[[6]],[[1]],[1]),
      ('mixed_C6_times_Z',[[6,0]],[[1,0],[0,1]],[1,2]),
      ('unsaturated_coupled_relation',[[2,4]],[[1,0],[0,1]],[1,2]),
      ('coupled_relation_nontorsion',[[2,4]],[[1,0],[0,1]],[3,-1]),
      ('torsion_residual_requires_relation_denominator',[[2,0]],[[1,1],[0,1]],[1,0]),
      ('dependent_relators',[[2,4],[4,8],[-6,-12]],[[1,0],[0,1]],[1,3]),
      ('rank_zero_element',[],[[1,0],[0,1]],[0,0]),
      ('finite_full_rank',[[4,2],[0,6]],[[1,0],[0,1]],[1,1]),
      ('nonstandard_generators_mixed',[[5,0]],[[2,0],[0,2],[0,3]],[1,1]),
      ('redundant_generator',[],[[1,0],[0,1],[3,2]],[2,1]),
    ]
    ans=[run_case(*x) for x in cases]
    rng=random.Random(38020261002)
    # Arbitrary small integral relation families with identity generators ensure genuine integral generation.
    for n in range(120):
        d=rng.choice([1,2,3]);R=[[rng.randrange(-5,6) for _ in range(d)] for _ in range(rng.randrange(d+2))]
        S=[[int(i==j) for i in range(d)] for j in range(d)]+[[rng.randrange(-3,4) for _ in range(d)]]
        v=[rng.randrange(-2,3) for _ in range(d)]
        ans.append(run_case('seeded_integral_%03d'%n,R,S,v,wordcheck=n<20 and d<=2))
    # Unimodular changes of coordinates preserve all exact LP and lattice conclusions.
    changed=[]
    for n in range(40):
        R=[[rng.randrange(-5,6),rng.randrange(-5,6)] for _ in range(rng.randrange(3))]
        S=[[1,0],[0,1],[rng.randrange(-3,4),rng.randrange(-3,4)]];v=[rng.randrange(-3,4),rng.randrange(-3,4)]
        k=rng.randrange(-7,8)
        def transform(x):return [x[0]+k*x[1],x[1]]
        a=run_case('pre_transform_%d'%n,R,S,v,False);b=run_case('post_transform_%d'%n,list(map(transform,R)),list(map(transform,S)),transform(v),False)
        assert a['lp']==b['lp'] and a['torsion_in_abelianization']==b['torsion_in_abelianization'];changed.append({'before':a,'after':b})
    # Negative controls: each incorrect shortcut must fail on a concrete exact fixture.
    negatives={}
    negatives['rational_lp_equals_one_step_integer_length_rejected']=ans[0]['lp']=='1/3' and ans[0]['word_lengths_n_1_to_12'][0]==2
    negatives['rational_zero_means_identity_rejected']=ans[3]['lp']=='0' and ans[3]['word_lengths_n_1_to_12'][0]>0
    v=[1,0];R=[[2,0]];S=[[1,1],[0,1]]
    val,a,ell,_=primal_dual(R,S,v);res=[F(v[i])-sum(a[j]*S[j][i] for j in range(2)) for i in range(2)]
    m_coeff=lcm(*(x.denominator for x in a));D,U=diagonalize(R,2)
    negatives['clear_only_primal_denominator_rejected']=not member([int(m_coeff*x) for x in res],D,U)
    D,U=diagonalize([[2]],1)
    negatives['real_spanning_implies_integral_generating_rejected']=not member([1],D,U)
    # Klein bottle model (a,b) with multiplication (u,v)*(x,y)=(u+(-1)^v*x,v+y).
    def mul(x,y):return (x[0]+(-1 if x[1]%2 else 1)*y[0],x[1]+y[1])
    a=(1,0);b=(0,1);bi=(0,-1)
    negatives['torsion_abelianization_means_finite_order_rejected']=mul(mul(b,a),bi)==(-1,0) and all((n,0)!=(0,0) for n in range(1,41))
    assert all(negatives.values())
    results={'candidate_imports':[],'source_first':True,'exact_arithmetic':'fractions.Fraction and independent unimodular Euclidean diagonalization','seed':38020261002,'cases':ans,'unimodular_pairs':changed,'negative_controls':negatives,'total_lp_instances':len(ans)+2*len(changed),'total_basis_enumerations':sum(x['basis_count'] for x in ans)+sum(p['before']['basis_count']+p['after']['basis_count'] for p in changed),'all_passed':True}
    (OUT/'independent_exact_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:results[k] for k in ['source_first','total_lp_instances','total_basis_enumerations','negative_controls','all_passed']},indent=2))
if __name__=='__main__':main()
