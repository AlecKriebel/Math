#!/usr/bin/env python3
"""Portable independent PR344 algebra verifier; Python standard library only.

No submitted checker, private path, network input, or historical result is used.
The mathematical universal coefficient proof is in semilinear_proof.md; finite
controls here verify implementation and deliberately reject known mistakes.
Assertions are explicit exceptions and remain active under python -O.
"""
import itertools
import json
from fractions import Fraction

COUNT = 0
def require(test, description):
    global COUNT
    COUNT += 1
    if not test:
        raise RuntimeError(description)

def matrix(n, entries=()):
    out = [[0 for _ in range(n)] for _ in range(n)]
    for row, col, value in entries:
        out[row][col] = value
    return out

def identity(n):
    return matrix(n, [(i,i,1) for i in range(n)])

def transpose(a):
    return [list(c) for c in zip(*a)]

def product(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))] if a else []

def columns(a, indices):
    return [[row[i] for i in indices] for row in a]

def append_columns(a,b):
    return [x+y for x,y in zip(a,b)]

def inverse(a):
    n=len(a)
    rows=[[Fraction(x) for x in a[i]]+[Fraction(int(i==j)) for j in range(n)]
          for i in range(n)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if rows[i][col])
        rows[col],rows[pivot]=rows[pivot],rows[col]
        d=rows[col][col]
        rows[col]=[v/d for v in rows[col]]
        for i in range(n):
            if i!=col:
                d=rows[i][col]
                rows[i]=[x-d*y for x,y in zip(rows[i],rows[col])]
    return [row[n:] for row in rows]

def determinant(a):
    if not a:
        return 1
    # The only non-permutation determinant tested has dimension six.
    total=0
    for permutation in itertools.permutations(range(len(a))):
        inversions=sum(permutation[i]>permutation[j]
                       for i in range(len(a)) for j in range(i+1,len(a)))
        term=(-1)**inversions
        for i,j in enumerate(permutation):
            term*=a[i][j]
        total+=term
    return total

def rank_prime(a,p):
    if not a:
        return 0
    rows=[[x%p for x in row] for row in a]
    pivot_row=0
    for col in range(len(rows[0])):
        choice=next((i for i in range(pivot_row,len(rows)) if rows[i][col]),None)
        if choice is None:
            continue
        rows[pivot_row],rows[choice]=rows[choice],rows[pivot_row]
        divisor=pow(rows[pivot_row][col],p-2,p)
        rows[pivot_row]=[(x*divisor)%p for x in rows[pivot_row]]
        for i in range(len(rows)):
            if i!=pivot_row:
                factor=rows[i][col]
                rows[i]=[(x-factor*y)%p for x,y in zip(rows[i],rows[pivot_row])]
        pivot_row+=1
        if pivot_row==len(rows):
            break
    return pivot_row

F=matrix(6,[(1,0,1),(2,1,1),(4,3,1)])
V=matrix(6,[(5,0,1),(2,3,1),(4,5,1)])
ZERO=matrix(6)
require(product(F,V)==ZERO and product(V,F)==ZERO,'mixed compositions')
F2,V2=product(F,F),product(V,V)
require(F2==matrix(6,[(2,0,1)]),'universal F^2 support certificate')
require(V2==matrix(6,[(4,0,1)]),'universal V^2 support certificate')
require(product(transpose(V),transpose(V))==matrix(6,[(0,4,1)]),'dual F^2 support')
require(product(transpose(F),transpose(F))==matrix(6,[(0,2,1)]),'dual V^2 support')
require(product(F,F2)==ZERO and product(V,V2)==ZERO,'nilpotence')

# Independently reconstruct the basis change, then calculate both actions.
T=transpose([[0,1,0,1,0,1], [0,0,1,0,1,0], [0,2,0,1,0,0],
             [0,0,1,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0]])
require(abs(determinant(T))==1,'qss basis has universal integral determinant')
Tinverse=inverse(T)
require(all(x.denominator==1 for row in Tinverse for x in row),'integral inverse')
Tinverse=[[int(x) for x in row] for row in Tinverse]
require(product(Tinverse,T)==identity(6),'independent basis inverse')
actions=[product(product(Tinverse,A),T) for A in [F,V]]
for action in actions:
    for size in [2,4]:
        require(all(action[i][j]==0 for i in range(size,6) for j in range(size)),
                'qss subspace invariance')
    for start in [0,2,4]:
        require([[action[start+i][start+j] for j in range(2)] for i in range(2)]
                ==[[0,0],[1,0]],'supersingular quotient action')

# Honda identities have permutation-matrix witnesses, independent of p.
L=columns(identity(6),[0,3,5])
image_F_basis=columns(identity(6),[1,2,4])
require(abs(determinant(append_columns(image_F_basis,L)))==1,'Honda complement')
require(product(V,L)==columns(identity(6),[5,2,4]),'V on Honda subspace')

# Pre-exposure n=4 control; it rejects an erroneously universal self-duality claim.
Fc=matrix(8,[(4,0,1),(5,1,1),(6,2,1),(7,3,1),(0,1,1),(2,3,1)])
Vc=matrix(8,[(4,0,1),(5,1,1),(6,2,1),(5,2,1),(7,3,1),
             (4,5,-1),(6,7,-1),(5,7,-1)])
require(product(Fc,Vc)==matrix(8) and product(Vc,Fc)==matrix(8),'source-only control valid')
require(product(Fc,product(Fc,Fc))==matrix(8),'source-only control F^3 zero')
require(product(Vc,product(Vc,Vc))==matrix(8,[(4,3,1)]),'source-only control V^3 nonzero')

# Perturbation controls: mixed compositions and filtration are independently tested.
badV=[row[:] for row in V]
badV[0][1]=1
require(product(badV,F)!=ZERO,'mixed-relation mutation rejected')
bad_flag=[row[:] for row in actions[1]]
bad_flag[5][0]=1
require(any(bad_flag[i][j] for i in range(2,6) for j in range(2)),
        'filtration mutation rejected')

for p in [5,7,11,101]:
    for n in [3,4,9]:
        f,v=matrix(2*n),matrix(2*n)
        for i,j in itertools.product(range(6),repeat=2):
            f[i][j],v[i][j]=F[i][j],V[i][j]
        for i in range(6,2*n,2):
            f[i+1][i]=v[i+1][i]=1
        fd,vd=transpose(v),transpose(f)
        require(rank_prime(f,p)==rank_prime(v,p)==n,'deformable direct sum ranks')
        require(product(f,v)==product(v,f)==matrix(2*n),'direct sum complex')
        require(rank_prime(append_columns(product(f,f),product(v,v)),p)==2,
                'independent original square images')
        require(rank_prime(append_columns(product(fd,fd),product(vd,vd)),p)==1,
                'coincident dual square images')
    # Small-rank controls are concrete split examples, not a classification proof.
    for n in [0,1,2]:
        f=matrix(2*n,[(i+1,i,1) for i in range(0,2*n,2)])
        swap=matrix(2*n,[(i,i+1,1) for i in range(0,2*n,2)]
                         +[(i+1,i,1) for i in range(0,2*n,2)])
        require(product(swap,f)==product(transpose(f),swap),
                'split small-rank positive self-duality control')

class CubicField:
    """F_p[t]/(t^3+t+1); construction is used only at p=5 and p=7."""
    def __init__(self,p):
        self.p,self.q=p,p**3
        require(all((x**3+x+1)%p for x in range(p)),'cubic irreducible: no roots')
        self.digits=[(a%p,(a//p)%p,a//p**2) for a in range(self.q)]
        self.sums=[[self.encode([(x+y)%p for x,y in zip(self.digits[a],self.digits[b])])
                    for b in range(self.q)] for a in range(self.q)]
        self.products=[[self.raw_product(a,b) for b in range(self.q)] for a in range(self.q)]
        self.sigma=[self.power(a,p) for a in range(self.q)]
        self.sigma_inverse=[self.power(a,p**2) for a in range(self.q)]
        self.inverses=[0]+[self.power(a,self.q-2) for a in range(1,self.q)]
        require(all(self.products[a][self.inverses[a]]==1 for a in range(1,self.q)),
                'field inversion certificates')
        require(all(self.sigma[self.sigma_inverse[a]]==a for a in range(self.q)),
                'Frobenius inverse certificates')
        require(self.sigma[p]!=self.sigma_inverse[p],'degree-three distinguishes sigma/inverse')

    def encode(self,a):
        return sum(x*self.p**i for i,x in enumerate(a))

    def raw_product(self,a,b):
        coefficients=[0]*5
        for i,x in enumerate(self.digits[a]):
            for j,y in enumerate(self.digits[b]):
                coefficients[i+j]+=x*y
        for degree in [4,3]:
            value=coefficients[degree]
            coefficients[degree-2]-=value  # t^3=-t-1
            coefficients[degree-3]-=value
        return self.encode([c%self.p for c in coefficients[:3]])

    def power(self,a,n):
        answer=1
        while n:
            if n&1:
                answer=self.products[answer][a]
            a=self.products[a][a]
            n//=2
        return answer

    def apply(self,A,x,sigma):
        result=[]
        for row in A:
            total=0
            for coefficient,value in zip(row,x):
                total=self.sums[total][self.products[coefficient][sigma[value]]]
            result.append(total)
        return result

    def field_product(self,A,B):
        output=[]
        for row in A:
            output_row=[]
            for col in zip(*B):
                total=0
                for a,b in zip(row,col):
                    total=self.sums[total][self.products[a][b]]
                output_row.append(total)
            output.append(output_row)
        return output

extension_results=[]
for p in [5,7]:
    field=CubicField(p)
    sig,invsig=field.sigma,field.sigma_inverse
    mul,add=field.products,field.sums
    scales=[p+(i%p) for i in range(6)] # all are nonzero/nonprime
    def change(A,twist):
        return [[mul[field.inverses[scales[i]]][mul[A[i][j]%p][twist[scales[j]]]]
                 for j in range(6)] for i in range(6)]
    f,v=change(F,sig),change(V,invsig)
    fd=[[sig[x] for x in row] for row in transpose(v)]
    vd=[[invsig[x] for x in row] for row in transpose(f)]
    require(field.field_product(f,[[sig[x] for x in row] for row in v])==ZERO,
            'nonprime basis mixed FV')
    require(field.field_product(v,[[invsig[x] for x in row] for row in f])==ZERO,
            'nonprime basis mixed VF')
    b=p+2
    failures_wrong_coeff=failures_wrong_inverse=0
    for i,j in itertools.product(range(6),repeat=2):
        for a in range(field.q):
            leftF=mul[mul[fd[i][j]][sig[b]]][a]
            rightF=sig[mul[b][mul[v[j][i]][invsig[a]]]]
            leftV=mul[mul[vd[i][j]][invsig[b]]][a]
            rightV=invsig[mul[b][mul[f[j][i]][sig[a]]]]
            require(leftF==rightF,'F dual pairing over degree-three field')
            require(leftV==rightV,'V dual pairing over degree-three field')
            failures_wrong_coeff += mul[mul[v[j][i]][sig[b]]][a] != rightF
            failures_wrong_inverse += mul[mul[vd[i][j]][sig[b]]][a] != rightV
    require(failures_wrong_coeff>0,'omitted coefficient Frobenius mutation rejected')
    require(failures_wrong_inverse>0,'sigma-for-inverse mutation rejected')
    # Actual dual maps also satisfy both semilinear complex relations.
    require(field.field_product(fd,[[sig[x] for x in row] for row in vd])==ZERO,
            'dual FV under nonprime coefficient change')
    require(field.field_product(vd,[[invsig[x] for x in row] for row in fd])==ZERO,
            'dual VF under nonprime coefficient change')
    extension_results.append({'field_size':field.q,'polynomial':'t^3+t+1',
                              'basis_change':'nonprime diagonal',
                              'wrong_coefficient_mutation_failures':failures_wrong_coeff,
                              'wrong_inverse_mutation_failures':failures_wrong_inverse})

print(json.dumps({'status':'pass','checks':COUNT,
                  'universal_certificate':'forced columns 2 and 4 share the dual e0 line',
                  'integer_qss_basis_determinant':determinant(T),
                  'prime_controls':[5,7,11,101], 'n_controls':[0,1,2,3,4,9],
                  'preexposure_n4_control':'F^3 zero, V^3 nonzero',
                  'extensions':extension_results,
                  'limitations':'Finite controls supplement the written all-perfect-field proof; source classification is not re-proved.'},indent=2))
