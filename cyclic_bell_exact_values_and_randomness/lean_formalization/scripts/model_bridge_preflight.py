#!/usr/bin/env python3
"""Exact compiler-free tests of the NEW physical/model interfaces.

Uses an independent Gaussian-rational representation (Fraction pairs), not the
older cyclotomic implementation. All quantum arithmetic is exact. Finite tests
check conventions and witnesses; they do NOT prove Lean source, model-set
inclusion, topological closure, or any universal/supremum theorem.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

@dataclass(frozen=True)
class G:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))
    @staticmethod
    def coerce(z): return z if isinstance(z, G) else G(z)
    def __add__(self,z):
        z=self.coerce(z);return G(self.re+z.re,self.im+z.im)
    __radd__=__add__
    def __neg__(self):return G(-self.re,-self.im)
    def __sub__(self,z):return self+-self.coerce(z)
    def __rsub__(self,z):return self.coerce(z)+-self
    def __mul__(self,z):
        z=self.coerce(z)
        return G(self.re*z.re-self.im*z.im,self.re*z.im+self.im*z.re)
    __rmul__=__mul__
    def conj(self):return G(self.re,-self.im)
    def normsq(self):return self.re*self.re+self.im*self.im
    def __truediv__(self,z):
        z=self.coerce(z);n=z.normsq()
        if not n:raise ZeroDivisionError('Gaussian-rational division by zero')
        v=self*z.conj();return G(v.re/n,v.im/n)
    def __pow__(self,k):
        if k<0:return (G(1)/self)**(-k)
        b,r=self,G(1)
        while k:
            if k&1:r=r*b
            b=b*b;k//=2
        return r
Z=G();ONE=G(1);I=G(0,1)

def shape(A):
    if not A or not A[0] or any(len(row)!=len(A[0]) for row in A):
        raise ValueError('A nonempty rectangular matrix is required')
    return len(A),len(A[0])
def mm(A,B):
    r,n=shape(A);m,c=shape(B)
    if n!=m:raise ValueError('Matrix dimension mismatch')
    out=[[Z for _ in range(c)] for _ in range(r)]
    for i in range(r):
        for k in range(n):
            if A[i][k]==Z:continue
            for j in range(c):
                if B[k][j]!=Z:out[i][j]=out[i][j]+A[i][k]*B[k][j]
    return out
def adj(A):return [[x.conj() for x in row] for row in zip(*A)]
def transpose(A):return [list(row) for row in zip(*A)]
def add(A,B):
    if shape(A)!=shape(B):raise ValueError('Addition dimension mismatch')
    return [[x+y for x,y in zip(r,s)] for r,s in zip(A,B)]
def scale(z,A):return [[G.coerce(z)*a for a in row] for row in A]
def ident(n):return [[G(int(i==j)) for j in range(n)] for i in range(n)]
def diag(v):return [[G.coerce(v[i]) if i==j else Z for j in range(len(v))] for i in range(len(v))]
def zero(n):return scale(0,ident(n))
def tr(A):
    n,m=shape(A)
    if n!=m:raise ValueError('Trace requires a square matrix')
    return sum((A[i][i] for i in range(n)),Z)
def kron(A,B):
    r,n=shape(A);s,m=shape(B)
    return [[A[i][j]*B[k][l] for j in range(n) for l in range(m)]
            for i in range(r) for k in range(s)]
def mv(A,v):
    r,n=shape(A)
    if n!=len(v):raise ValueError('Vector dimension mismatch')
    return [sum((a*x for a,x in zip(row,v) if a!=Z and x!=Z),Z) for row in A]
def ip(v,w):
    if len(v)!=len(w):raise ValueError('Inner-product dimension mismatch')
    return sum((x.conj()*y for x,y in zip(v,w)),Z)
def vec(A):return [x for row in A for x in row]
def me(A,rho):return tr(mm(rho,A))
def sum_matrix(matrices,n):
    out=zero(n)
    for A in matrices:out=add(out,A)
    return out

def rotation(n,j,k,a,b,phase=I):
    if a*a+b*b!=1 or phase.normsq()!=1:raise ValueError('Unnormalized rotation')
    U=ident(n);U[j][j]=G(a);U[k][k]=G(a)
    U[j][k]=-G(b)*phase.conj();U[k][j]=G(b)*phase
    return U

def basis(n,seed):
    U=ident(n)
    for j in range(n-1):
        a,b=(F(3,5),F(4,5)) if (j+seed)%2 else (F(5,13),F(12,13))
        U=mm(U,rotation(n,j,j+1,a,b,I**(seed+j)))
    return U

def pvm(n,seed):
    U=basis(n,seed)
    return [mm(mm(U,diag([int((j+seed)%4==a) for j in range(n)])),adj(U)) for a in range(4)]
def encoding(M):return sum_matrix((scale(I**a,M[a]) for a in range(4)),len(M[0]))

class Checks:
    def __init__(self):self.checks=[];self.controls=[]
    def equal(self,name,a,b):
        if a!=b:raise AssertionError(name)
        self.checks.append(name)
    def truth(self,name,p):
        if not p:raise AssertionError(name)
        self.checks.append(name)
    def reject(self,name,bad,correct):
        if bad==correct:raise AssertionError('Mutation was not detected: '+name)
        self.controls.append(name)

def physical_case(C,na,nb,roots,name):
    n=na*nb
    if len(roots)!=n or sum(r*r for r in roots)!=1 or min(roots)<0:
        raise ValueError('Exact positive square-root eigenvalues required')
    U=basis(n,1)
    S=mm(mm(U,diag(roots)),adj(U))
    rho=mm(mm(U,diag([r*r for r in roots])),adj(U))
    V=vec(S)
    C.equal(name+': basis unitary',mm(adj(U),U),ident(n))
    C.equal(name+': positive root Hermitian',adj(S),S)
    C.equal(name+': root squares to density',mm(S,S),rho)
    C.equal(name+': root Gram equals density',mm(S,adj(S)),rho)
    C.equal(name+': density trace',tr(rho),ONE)
    C.equal(name+': vectorized state norm',ip(V,V),ONE)
    C.reject(name+': doubled purification',ip([2*v for v in V],[2*v for v in V]),ONE)
    C.reject(name+': trace-two density',tr(scale(2,rho)),ONE)
    T=[[G(F(i+2*j+1,7),F(2*i-j+1,11)) for j in range(n)] for i in range(n)]
    lhs=ip(V,mv(kron(T,ident(n)),V));rhs=me(T,rho)
    C.equal(name+': arbitrary COMPLEX expectation',lhs,rhs)
    C.equal(name+': vectorization left action',mv(kron(T,ident(n)),V),vec(mm(T,S)))
    if n>1 and len(set(roots))>1:
        C.reject(name+': omit inner conjugation',sum((x*y for x,y in zip(V,mv(kron(T,ident(n)),V))),Z),rhs)
        C.reject(name+': act on environment instead',ip(V,mv(kron(ident(n),T),V)),rhs)
        C.reject(name+': density transpose',me(T,transpose(rho)),rhs)
    A=[pvm(na,x) for x in range(4)]
    B=[pvm(nb,y+8) for y in range(5)]
    for side,measurements,nloc in [('A',A,na),('B',B,nb)]:
        for x,M in enumerate(measurements):
            C.equal(f'{name}: {side}{x} complete',sum_matrix(M,nloc),ident(nloc))
            for a in range(4):
                C.equal(f'{name}: {side}{x}/{a} Hermitian',M[a],adj(M[a]))
                C.equal(f'{name}: {side}{x}/{a} idempotent',mm(M[a],M[a]),M[a])
                for b in range(a+1,4):
                    C.equal(f'{name}: {side}{x}/{a},{b} orthogonal',mm(M[a],M[b]),zero(nloc))
            O=encoding(M)
            C.equal(f'{name}: {side}{x} unitary',mm(adj(O),O),ident(nloc))
            C.equal(f'{name}: {side}{x} fourth power',mm(mm(O,O),mm(O,O)),ident(nloc))
    EA=[encoding(m) for m in A];EB=[encoding(m) for m in B]
    moments={};tables={};wrong_phase_detected=False
    for x,y in product(range(4),range(5)):
        p=[]
        for a in range(4):
            row=[]
            for b in range(4):
                Txy=kron(A[x][a],B[y][b])
                born=me(Txy,rho)
                C.equal(f'{name}: Born {x},{y}/{a},{b} reality',born.im,F(0))
                C.truth(f'{name}: Born {x},{y}/{a},{b} nonnegative',born.re>=0)
                # The actual Hilbert-space product of lifted effects acts as M tensor N.
                LA=kron(A[x][a],ident(nb));LB=kron(ident(na),B[y][b])
                C.equal(f'{name}: commute {x},{y}/{a},{b}',mm(LA,LB),mm(LB,LA))
                C.equal(f'{name}: tensor product {x},{y}/{a},{b}',mm(LA,LB),Txy)
                C.equal(f'{name}: lifted Born {x},{y}/{a},{b}',
                        ip(V,mv(kron(Txy,ident(n)),V)),born)
                row.append(born.re)
            p.append(row)
        C.equal(f'{name}: normalized table {x},{y}',sum(map(sum,p)),F(1))
        for a in range(4):
            C.equal(f'{name}: Alice marginal {x},{y}/{a}',sum(p[a]),me(kron(A[x][a],ident(nb)),rho).re)
        for b in range(4):
            C.equal(f'{name}: Bob marginal {x},{y}/{b}',sum(p[a][b] for a in range(4)),me(kron(ident(na),B[y][b]),rho).re)
        corr=sum((I**(a+b)*p[a][b] for a,b in product(range(4),repeat=2)),Z)
        wrong=sum((I**(a-b)*p[a][b] for a,b in product(range(4),repeat=2)),Z)
        wrong_phase_detected|=(corr!=wrong)
        C.equal(f'{name}: full complex correlator {x},{y}',corr,me(kron(EA[x],EB[y]),rho))
        moments[x,y]=corr;tables[x,y]=p
    C.reject(name+': Bob-adjoint phase mutation',wrong_phase_detected,False)
    firstp=sum((moments[0,y]+I**y*moments[1,y]).re for y in range(4))
    firsto=sum(me(kron(add(EA[0],scale(I**y,EA[1])),EB[y]),rho).re for y in range(4))
    aligned=moments[0,4].re
    C.equal(name+': reduced first real behavior bridge',firstp,firsto)
    C.equal(name+': augmented first real behavior bridge',firstp+aligned,firsto+me(kron(EA[0],EB[4]),rho).re)
    C.equal(name+': deleting Bob input is restriction, not rescaling',firstp+aligned-firstp,aligned)
    if aligned:
        C.reject(name+': omitted augmentation',firstp,firstp+aligned)
    # The second trace/probability interface is linear for ANY coefficients.
    # These Gaussian-rational coefficients are NOT asserted to be source lambda.
    lam=[G(F(1,3)),G(0,F(2,5)),G(F(1,7),F(3,7)),G(F(-2,9),F(1,9))]
    secondp=sum((lam[l].conj()*sum((I**(l*y)*moments[l,y] for y in range(4)),Z)).re for l in range(4))
    secondo=F(0)
    for l in range(4):
        Bhat=sum_matrix((scale(I**(l*y),EB[y]) for y in range(4)),nb)
        secondo+=me(scale(lam[l].conj(),kron(EA[l],Bhat)),rho).re
    C.equal(name+': second coefficient-linear Born bridge',secondp,secondo)
    C.equal(name+': second augmented bridge',secondp+aligned,secondo+me(kron(EA[0],EB[4]),rho).re)
    return {'name':name,'alice_dimension':na,'bob_dimension':nb,'outcomes':4,
            'rank':sum(r>0 for r in roots),'density_dimension':n,
            'purification_dimension':n*n,'zero_effects_allowed':True}

def right_one_input_case(C):
    # All probabilities are squares of rational amplitudes, including a zero
    # marginal. This permits checking the actual sparse tripartite pure state.
    marginal_roots=[F(3,5),F(0),F(4,5)]
    amplitudes=[[[F(3,5),F(4,5)],[F(1),F(0)],[F(5,13),F(12,13)]],
                [[F(1,3),F(2,3),F(2,3)],[F(1),F(0),F(0)],[F(2,3),F(1,3),F(2,3)]],
                [[F(5,13),F(12,13)],[F(1),F(0)],[F(3,5),F(4,5)]]]
    sizes=[2,3,2]
    assignments=[(b,t) for b in range(3) for t in product(*(range(a) for a in sizes))]
    amp=[]
    for b,t in assignments:
        v=marginal_roots[b]
        for x,a in enumerate(t):v*=amplitudes[x][b][a]
        amp.append(v)
    mu=[v*v for v in amp]
    C.equal('right-one-input: actual pure-state norm',sum(mu),F(1))
    C.equal('right-one-input: zero marginal retained',sum(mu[i] for i,(b,t) in enumerate(assignments) if b==1),F(0))
    rhoE=diag(mu)
    for x,nout in enumerate(sizes):
        total=zero(len(mu));success=F(0)
        for a,b in product(range(nout),range(3)):
            selected=[int(t[x]==a and bob==b) for bob,t in assignments]
            # Sparse GHZ amplitudes have coincident A,B,E labels. Performing
            # both grouping projections then tracing AB yields this matrix.
            conditional=[[sum((G(amp[e]*amp[f]) for ab in range(len(mu))
                               if ab==e and ab==f and selected[ab]),Z)
                          for f in range(len(mu))] for e in range(len(mu))]
            expected=diag([mu[e]*selected[e] for e in range(len(mu))])
            C.equal(f'right-one-input: actual conditional {x}/{a},{b}',conditional,expected)
            born=tr(conditional).re
            p=(marginal_roots[b]*amplitudes[x][b][a])**2
            C.equal(f'right-one-input: complete behavior {x}/{a},{b}',born,p)
            guess=diag(selected)
            C.equal(f'right-one-input: Eve grouping idempotence {x}/{a},{b}',mm(guess,guess),guess)
            success+=tr(mm(guess,conditional)).re
            total=add(total,conditional)
        C.equal(f'right-one-input: complete instrument {x}',total,rhoE)
        C.equal(f'right-one-input: perfect Eve success {x}',success,F(1))
    return len(assignments)

def observed_uniform_is_not_privacy(C):
    # Four equally likely stored output pairs; observed behavior is uniform,
    # yet Eve reads the stored pair with certainty. This tests the lower-bound
    # semantics used by the binary componentwise-minimality statement.
    rho=diag([F(1,4)]*4);success=F(0)
    for a,b in product(range(2),repeat=2):
        j=2*a+b
        Q=diag([int(k==j) for k in range(4)])
        conditional=diag([F(int(k==j),4) for k in range(4)])
        C.equal(f'one-input uniform: observed {a},{b}',tr(conditional).re,F(1,4))
        C.reject(f'one-input uniform: false operator privacy {a},{b}',conditional,scale(F(1,4),rho))
        success+=tr(mm(Q,conditional)).re
    C.equal('one-input uniform: actual Eve success',success,F(1))
    C.reject('one-input uniform: observed uniformity substituted for privacy',success,F(1,4))

def run():
    C=Checks();cases=[]
    data=[(1,1,[F(1)],'singleton'),
          (1,4,[F(1,5),F(2,5),F(2,5),F(4,5)],'one-by-four-full'),
          (2,2,[F(1),F(0),F(0),F(0)],'two-by-two-rank-one'),
          (2,2,[F(3,5),F(4,5),F(0),F(0)],'two-by-two-rank-two'),
          (2,3,[F(1,10),F(1,10),F(2,10),F(2,10),F(3,10),F(9,10)],'two-by-three-full')]
    for na,nb,r,name in data:cases.append(physical_case(C,na,nb,r,name))
    hidden=right_one_input_case(C);observed_uniform_is_not_privacy(C)
    if len(C.checks)!=len(set(C.checks)) or len(C.controls)!=len(set(C.controls)):
        raise AssertionError('Duplicate check labels')
    return {'status':'exact_interface_regressions_passed_NOT_LEAN','kernel_checked':False,
            'universal_model_theorem_checked':False,'closure_or_supremum_checked':False,
            'arithmetic':'independent Gaussian rationals as pairs of fractions; no floating point',
            'checks':len(C.checks),'negative_controls':len(C.controls),'cases':cases,
            'right_one_input_hidden_dimension':hidden,'check_labels':C.checks,'negative_control_labels':C.controls,
            'scope':'finite interface/convention checks only; coefficients in second bridge are generic test data, not source lambda'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args();start=datetime.now(timezone.utc)
    result=run();result['started_utc']=start.isoformat();result['finished_utc']=datetime.now(timezone.utc).isoformat()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('check_labels','negative_control_labels')},indent=2))
