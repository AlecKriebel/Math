#!/usr/bin/env python3
"""Fresh sparse-polynomial tests, standard library only; NOT a submitted program replay."""
from collections import defaultdict
from pathlib import Path
import json, datetime, platform

class P:
    def __init__(self, x=0):
        self.d = dict(x.d) if isinstance(x,P) else dict(x) if isinstance(x,dict) else ({():x} if x else {})
    def __add__(self,x):
        x=P(x); d=defaultdict(int,self.d)
        for m,c in x.d.items(): d[m]+=c
        return P({m:c for m,c in d.items() if c})
    __radd__=__add__
    def __neg__(self): return P({m:-c for m,c in self.d.items()})
    def __sub__(self,x): return self+-P(x)
    def __rsub__(self,x): return P(x)+-self
    def __mul__(self,x):
        d=defaultdict(int)
        for a,c in self.d.items():
            for b,e in P(x).d.items(): d[tuple(sorted(a+b))]+=c*e
        return P({m:c for m,c in d.items() if c})
    __rmul__=__mul__
    def __eq__(self,x): return self.d==P(x).d
    def derivative(self, which='u', jet=False):
        d=defaultdict(int)
        for m,c in self.d.items():
            for i,v in enumerate(m):
                if (jet and not v.startswith('D_')) or v==which:
                    rest=m[:i]+m[i+1:]
                    target=tuple(sorted(rest+('D_'+v,))) if jet else rest
                    d[target]+=c
        return P({m:c for m,c in d.items() if c})
    def at(self,u):
        d=defaultdict(int)
        for m,c in self.d.items():
            k=m.count('u'); d[tuple(v for v in m if v!='u')]+=c*u**k
        return P({m:c for m,c in d.items() if c})
    def __repr__(self):
        return ' + '.join(str(c)+'*'+('*'.join(m) or '1') for m,c in sorted(self.d.items())) or '0'

def sym(s): return P({(s,):1})
def zero(n,m=None): return [[P() for _ in range(n if m is None else m)] for _ in range(n)]
def cp(M): return [[P(x) for x in row] for row in M]
def add(M,N): return [[a+b for a,b in zip(r,s)] for r,s in zip(M,N)]
def neg(M): return [[-x for x in row] for row in M]
def mul(M,N):
    return [[sum((M[i][k]*N[k][j] for k in range(len(N))),P()) for j in range(len(N[0]) if N else 0)] for i in range(len(M))]
def scale(a,M): return [[a*x for x in row] for row in M]
def at(M,u): return [[x.at(u) for x in row] for row in M]
def derivative(M,jet=False): return [[x.derivative(jet=jet) for x in row] for row in M]
def ident(n): return [[P(int(i==j)) for j in range(n)] for i in range(n)]
def iszero(M): return all(x==0 for r in M for x in r)
def cols(M): return [[r[j] for r in M] for j in range(len(M))]
def matvec(M,v): return [sum((a*b for a,b in zip(row,v)),P()) for row in M]
def vsub(a,b): return [x-y for x,y in zip(a,b)]
def bracket(v,w,jet=False):
    return [v[-1]*x.derivative(jet=jet)-w[-1]*y.derivative(jet=jet) for y,x in zip(v,w)]
def torsion(L,jet=False):
    C=cols(L); E=cols(ident(len(L))); R={}
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            R[(i,j)]=vsub(vsub(bracket(C[i],C[j],jet),matvec(L,bracket(C[i],E[j],jet))),matvec(L,bracket(E[i],C[j],jet)))
    return R

def constraint(L):
    m=len(L)-1
    A=[row[:m] for row in L[:m]]; lam=L[-1][-1]
    return mul(add(A,scale(-lam,ident(m))),derivative(A)) if m else []

def comps(n):
    if n==0: yield ()
    else:
        for k in range(1,n+1):
            for tail in comps(n-k): yield (k,)+tail

def jordan(blocks):
    n=sum(r for r,mu in blocks); M=zero(n); offset=0
    for r,mu in blocks:
        for j in range(r):
            M[offset+j][offset+j]=mu
            if j+1<r: M[offset+j][offset+j+1]=P(1)
        offset+=r
    return M

def stages(parts,chosen):
    # Physically permute whole blocks to put chosen chain last; retain independent symbols.
    items=[(r,sym('mu'+str(i))) for i,r in enumerate(parts)]
    last=items[chosen]; blocks=items[:chosen]+items[chosen+1:]+[last]
    J=jordan(blocks); n=len(J); m=n-1; current=cp(J); u=sym('u'); emitted=[]
    def emit(S,tag):
        nonlocal current
        assert at(S,0)==current, ('start',parts,chosen,tag)
        assert iszero(constraint(S)), ('constraint',parts,chosen,tag)
        if n<=4: assert all(all(x==0 for x in v) for v in torsion(S).values())
        emitted.append(tag); current=at(S,1)
    S=cp(current)
    for i in range(m): S[i][-1]=S[i][-1]*(1-u)
    emit(S,'detach b')
    angular=blocks[:-1]+([(last[0]-1,last[1])] if last[0]>1 else [])
    if not angular:
        S=cp(current); S[-1][-1]=S[-1][-1]*(1-u); emit(S,'empty A lambda drift')
    offset=0
    for r,mu in angular:
        S=cp(current); S[-1][-1]=current[-1][-1]*(1-u)+mu*u; emit(S,'align lambda')
        for j in range(r-1):
            S=cp(current); S[offset+j][offset+j+1]=1-u; emit(S,'ordered arrow '+str(j+1))
        S=cp(current)
        for j in range(r): S[offset+j][offset+j]=mu*(1-u)
        S[-1][-1]=mu*(1-u); emit(S,'matched scalar drift')
        offset+=r
    assert iszero(current), ('final',parts,chosen)
    return len(emitted)

def main():
    results={'run_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'arithmetic':'Integer-coefficient sparse polynomials in independent formal symbols; exact, no sampling/tolerance','submitted_program_replayed':False}
    components=0
    for n in range(1,6):
        m=n-1; L=zero(n)
        for i in range(m):
            for j in range(m): L[i][j]=sym('A_'+str(i)+'_'+str(j))
            L[i][-1]=sym('b_'+str(i))
        L[-1][-1]=sym('lambda')
        T=torsion(L,jet=True)
        A=[row[:m] for row in L[:m]]
        expected=mul(add(A,scale(-L[-1][-1],ident(m))),derivative(A,jet=True)) if m else []
        for (i,j),v in T.items():
            want=[expected[k][i] for k in range(m)]+[P()] if j==m else [P()]*n
            assert v==want, (n,i,j,v,want)
            components+=n
    results['arbitrary_independent_jet_torsion']={'dimensions':[1,2,3,4,5],'scalar_components_compared':components,'pass':True,'b_and_lambda_derivatives_unrestricted':True}
    families=stages_count=0; per_n={}
    for n in range(1,8):
        f=s=0
        for partition in comps(n):
            for chosen in range(len(partition)):
                k=stages(partition,chosen); f+=1; s+=k
        families+=f; stages_count+=s; per_n[n]={'families':f,'stages':s}
    additional=[]
    for p,c in [((12,),0),((20,),0),((1,3,1,4,2),3),((5,1,5),0)]:
        k=stages(p,c); families+=1; stages_count+=k; additional.append({'ordered_blocks':p,'distinguished_index':c,'stages':k})
    results['ordered_partition_and_distinguished_block_families']={'all_compositions_dimensions_1_through_7':per_n,'additional_large_mixed_families':additional,'families':families,'stages':stages_count,'checks':['exact initial endpoints','every stage starts at previous exact endpoint','left ordered constraint zero','direct all-pair bracket torsion for n<=4','exact zero final matrix'],'pass':True,'equal_and_zero_eigenvalues':'Polynomial identities admit every equality/zero specialization, without division.'}
    u=sym('u'); mu=sym('mu'); negative={}
    L=zero(4); L[0][1]=P(1); L[1][2]=1-u
    R=constraint(L); assert R[0][2]==-1; negative['reversed_arrow_order']=repr(R[0][2])
    L=zero(4); L[0][1]=u; L[1][2]=u
    R=constraint(L); assert R[0][2]==u; negative['single_cutoff_of_angular_J3']=repr(R[0][2])
    L=zero(2); L[0][0]=mu*(1-u); L[1][1]=mu
    R=constraint(L); assert R[0][0]==mu*mu*u; negative['unmatched_scalar_drift']=repr(R[0][0])
    L=zero(4); L[0][1]=1-u; L[1][2]=P(1)
    A=[row[:3] for row in L[:3]]; wrong=mul(derivative(A),A)
    assert iszero(constraint(L)) and wrong[0][2]==-1
    negative['reversing_product_rejects_valid_path']=repr(wrong[0][2])
    results['negative_controls']={'pass':True,'detected_residuals':negative}
    L=zero(3); L[0][0]=P(2); L[1][1]=P(3); L[2][2]=u*u
    L[0][2]=u*u*u+u; L[1][2]=u*u+2*u
    assert all(all(x==0 for x in v) for v in torsion(L).values())
    results['false_bprime_or_lambdaprime_requirement']={'pass':True,'example':'A=diag(2,3), b=(u^3+u,u^2+2u), lambda=u^2 has identically zero torsion despite nonzero b-prime and lambda-prime.'}
    results['overall']='PASS'
    output=Path(__file__).with_name('CONTROL_RESULTS.json'); output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
