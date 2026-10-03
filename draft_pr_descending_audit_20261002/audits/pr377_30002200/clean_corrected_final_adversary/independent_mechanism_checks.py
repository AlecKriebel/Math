from itertools import combinations
from math import comb
import sys
import sympy as s

def boundary(n,q,values,signed=True):
    source=list(combinations(range(n),q)); target=list(combinations(range(n),q-1))
    idx={j:i for i,j in enumerate(target)}
    a=s.zeros(len(target),len(source))
    for c,j in enumerate(source):
        for p,i in enumerate(j):
            a[idx[j[:p]+j[p+1:]],c]=(-1 if signed and p%2 else 1)*values[i]
    return a

def mu(lengths):
    n=len(lengths); total=sum(lengths)
    masks=range(1<<n)
    sums=[sum(lengths[i] for i in range(n) if j>>i&1) for j in masks]
    walls=[j for j in masks if 2*sums[j]==total]
    if walls: return None,len(walls)
    cross=[]
    for j in masks:
        if 2*sums[j]>total:
            facets=[i for i in range(n) if j>>i&1 and 2*(sums[j]-lengths[i])<total]
            if facets: cross.append((len(facets),j,facets))
    return min(x[0] for x in cross),0

def jacobian(lengths,u,z):
    n=len(lengths); a=s.zeros(n+2,4*n)
    for i in range(n):
        a[i,4*i]=2*u[i][0]; a[i,4*i+1]=2*u[i][1]
        a[i,4*i+2]=2*z[i][0]; a[i,4*i+3]=2*z[i][1]
        a[n,4*i]=lengths[i]; a[n+1,4*i+1]=lengths[i]
    return a

print('INDEPENDENT MECHANISM CHECKS; Python',sys.version.split()[0],'SymPy',s.__version__)
for n in range(1,8):
    d={q:boundary(n,q,list(range(1,n+1))) for q in range(1,n+1)}
    for q,a in d.items():
        rank=a.rank(); assert rank==comb(n-1,q-1)
        if q>1: assert d[q-1]*a==s.zeros(d[q-1].rows,a.cols)
        prev=0 if q==n else d[q+1].rank()
        assert a.cols-rank==prev
    residue=[boundary(n,q,[0]*n) for q in range(1,n+1)]
    assert all(a.is_zero_matrix for a in residue)
    assert residue[-1].cols==1
    print('Koszul rank/exactness/residue Tor: n=',n,'ranks=',[d[q].rank() for q in d], 'top residue dimension=1')
    if n>=2:
        bad=boundary(n,1,list(range(1,n+1)),False)*boundary(n,2,list(range(1,n+1)),False)
        assert not bad.is_zero_matrix
        print('Unsigned differential rejected:',n,'nonzero d^2=',sum(x!=0 for x in bad))
for r in range(1,13):
    m=(r-1)//2; active=2*m+1; lengths=[0]*(r-active)+[1]*active
    actual,walls=mu(lengths); assert actual==m+1 and walls==0
    a=jacobian(lengths,[(0,0)]*r,[(1,0)]*r)
    assert a.rank()==r+2
    print('Zero-extension / odd maximal family:',lengths,'mu=',actual,'Jacobian rank=',a.rank(),'dimension=',4*r-a.rank())
for n in [2,4,6,8]:
    actual,walls=mu([1]*n); assert actual is None and walls==comb(n,n//2)
    u=[(1,0)]*(n//2)+[(-1,0)]*(n//2)
    a=jacobian([1]*n,u,[(0,0)]*n)
    assert a.rank()==n+1
    print('Balanced nongeneric control:',n,'wall subsets=',walls,'deficient Jacobian rank=',a.rank())
for n in [3,5,7,9]:
    lengths=[1]*(n-1)+[n+1]
    actual,walls=mu(lengths); assert actual==1 and walls==0
    print('Dominant-length chamber control:',lengths,'mu=',actual,'predicted syzygy order=0')
for lengths,expected in [([1,1,1,2,2],1),([0,0,1,1,1],2),([1,1,1,1,1],3)]:
    actual,walls=mu(lengths); assert actual==expected and not walls
    print('Nonuniform / lower-order control:',lengths,'mu=',actual)
print('ALL CHECKS PASS; bounded computation only; universal identification remains a cited theorem.')
