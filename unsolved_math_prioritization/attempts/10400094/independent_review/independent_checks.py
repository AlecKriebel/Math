"""Independent exact diagnostics; standard library only. Run beside this file."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib, json
checks=0

def ck(x):
    global checks
    assert x
    checks+=1

def rank(rows,p):
    a=[[x%p for x in row] for row in rows]
    r=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        q=pow(a[r][c],-1,p);a[r]=[(x*q)%p for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                q=a[i][c];a[i]=[(x-q*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def coloring_count(twists,capcup=False):
    n=abs(twists);size=2*(n+1);rows=[]
    def equation(terms):
        row=[0]*size
        for i,c in terms: row[i]+=c
        rows.append(row)
    for j in range(n):
        u,v,x,y=2*j,2*j+1,2*j+2,2*j+3
        if twists>=0:
            equation([(x,1),(u,-2),(v,1)])
            equation([(y,1),(u,-1)])
        else:
            equation([(x,1),(v,-1)])
            equation([(y,1),(v,-2),(u,1)])
    if capcup:
        equation([(0,1),(1,-1)])
        equation([(size-2,1),(size-1,-1)])
    else:
        equation([(0,1),(size-2,-1)])
        equation([(1,1),(size-1,-1)])
    return 7**(size-rank(rows,7))

counts={}
for r in range(-28,29):
    counts[r]=coloring_count(r)
    ck(counts[r]==(49 if r%7==0 else 7))
    ck(coloring_count(r,True)==7)
M=[[counts[k-j] for k in range(4)]+[7] for j in range(5)]
Q=[[x//7 for x in row] for row in M]
# Subtract the fifth row from each of the first four; triangular determinant.
R=[[Q[i][j]-Q[4][j] for j in range(5)] for i in range(4)]+[Q[4]]
ck(R==[[6*int(i==j) for j in range(5)] for i in range(4)]+[[1]*5])
for p in (2,3,5,7,11,13):
    ck(rank(M,p)==(0 if p==7 else 1 if p in (2,3) else 5))
# Exhaustive independent nullspace test in one admissible characteristic.
for b in product(range(5),repeat=5):
    ck(all(sum(x*y for x,y in zip(row,b))%5==0 for row in M)==(not any(b)))
# Cyclotomic ring Z[z]/(1+...+z^6), without symbolic-algebra dependencies.
ZERO=(0,)*6;ONE=(1,0,0,0,0,0)
def red(a):
    a=list(a)+[0]*max(0,6-len(a))
    for k in range(len(a)-1,5,-1):
        c=a[k]
        for j in range(6):a[k-6+j]-=c
    return tuple(a[:6])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    out=[0]*11
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return red(out)
def zp(n):
    a=[0]*(n%7+1);a[-1]=1;return red(a)
s=add(add(zp(1),zp(2)),zp(4));bar=add(add(zp(3),zp(5)),zp(6))
ck(add(s,bar)==neg(ONE));ck(mul(s,bar)==tuple(2*x for x in ONE))
ck(mul(sub(s,bar),sub(s,bar))==tuple(-7*x for x in ONE))
coeff=[ONE]
for q in (1,2,4):
    out=[ZERO]*(len(coeff)+1)
    for i,c in enumerate(coeff):
        out[i]=sub(out[i],mul(c,zp(q)));out[i+1]=add(out[i+1],c)
    coeff=out
ck(coeff==[neg(ONE),bar,neg(s),ONE])
for x in range(7):
    val=ZERO
    for c in reversed(coeff):val=add(mul(val,zp(x*x)),c)
    correction=sub(s,bar) if x==0 else ZERO
    ck(add(val,correction)==ZERO)
# Distinct eigenvalues, and nonzero Vandermonde determinant: cubic independence.
eigen=[zp(q) for q in (0,1,2,4)];vand=ONE
for i in range(4):
    for j in range(i+1,4):
        ck(eigen[i]!=eigen[j]);vand=mul(vand,sub(eigen[j],eigen[i]))
ck(vand!=ZERO)
root=Path(__file__).resolve().parent
result={'status':'PASS','exact_assertions':checks,'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),'crossing_system_twists':[-28,28],'field5_coefficient_tuples':3125,'scope':'Independent crossing-equation rank counts, cap/cup constraints, coefficient obstruction, and exact cyclotomic algebra; no global invariant or count-recovery certification.'}
(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
