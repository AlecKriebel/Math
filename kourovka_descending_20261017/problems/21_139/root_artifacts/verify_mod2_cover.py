"""Exact independent chain computation for the mod-2 rose cover.
No candidate-author code or third-party math packages are imported.
"""
from fractions import Fraction
from math import gcd,lcm
from functools import reduce
import json,sys

def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mpow(a,n):
    r=[[int(i==j) for j in range(len(a))] for i in range(len(a))]
    while n:
        if n&1:r=matmul(r,a)
        a=matmul(a,a);n//=2
    return r

def rref(a):
    a=[[Fraction(x) for x in row] for row in a]
    order=list(range(len(a))); piv=[]; row=0
    for col in range(len(a[0])):
        p=next((i for i in range(row,len(a)) if a[i][col]),None)
        if p is None:continue
        a[row],a[p]=a[p],a[row];order[row],order[p]=order[p],order[row]
        v=a[row][col];a[row]=[x/v for x in a[row]]
        for i in range(len(a)):
            if i!=row and a[i][col]:
                v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[row])]
        piv.append(col);row+=1
        if row==len(a):break
    return a,piv,order[:row]

def det(a):
    a=[[Fraction(x) for x in row] for row in a]; ans=Fraction(1)
    for j in range(len(a)):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None:return 0
        if p!=j:a[p],a[j]=a[j],a[p];ans=-ans
        z=a[j][j];ans*=z
        for i in range(j+1,len(a)):
            w=a[i][j]/z
            for k in range(j+1,len(a)):a[i][k]-=w*a[j][k]
    assert ans.denominator==1
    return int(ans)

def deck(v):
    return (2 if v&1 else 0)^(4 if v&2 else 0)^(3 if v&4 else 0)

# Edges (v,i), numbered 3*v+i, oriented v -> v xor (1<<i).
d=[[0]*24 for _ in range(8)]
for v in range(8):
    for i in range(3):
        d[v][3*v+i]-=1;d[v^(1<<i)][3*v+i]+=1
# phi(a)=b, phi(b)=c, phi(c)=ab. Lift fixing the zero vertex.
t=[[0]*24 for _ in range(24)]
words=[(1,),(2,),(0,1)]
for v in range(8):
    for i,w in enumerate(words):
        at=deck(v)
        for letter in w:
            t[3*at+letter][3*v+i]+=1;at^=1<<letter
        assert at==deck(v^(1<<i))
m=[[int(i==deck(j)) for j in range(8)] for i in range(8)]
assert matmul(d,t)==matmul(m,d)
assert mpow(m,7)==[[int(i==j) for j in range(8)] for i in range(8)]
assert all(mpow(m,k)!=mpow(m,7) for k in range(1,7))
power=int(sys.argv[1]) if len(sys.argv)>1 else 14
assert power in (2,14)
tn=mpow(t,power)
assert matmul(d,tn)==matmul(mpow(m,power),d)
a=d+[[tn[i][j]-int(i==j) for j in range(24)] for i in range(24)]
e,piv,rows=rref(a);free=[j for j in range(24) if j not in piv]
kernel=[]
for j in free:
    v=[Fraction(0) for _ in range(24)];v[j]=1
    for i,c in enumerate(piv):v[c]=-e[i][j]
    scale=lcm(*(x.denominator for x in v));v=[int(x*scale) for x in v]
    common=reduce(gcd,(abs(x) for x in v));v=[x//common for x in v]
    assert all(sum(x*y for x,y in zip(row,v))==0 for row in a)
    kernel.append(v)
minor=[[a[i][j] for j in piv] for i in rows]
minor_det=det(minor)
assert minor_det!=0 and len(piv)+len(kernel)==24
assert len(rref(kernel)[1])==len(kernel)
assert (len(piv),len(kernel))==({2:(23,1),14:(17,7)}[power])
assert len(rref(d)[1])==7
out={'cover_vertices':8,'cover_edges':24,'deck_map_order':7,
     'base_cover_free_rank':17,'monodromy_power':power,'mapping_torus_index':8*power,
     'boundary_rank':7,'stacked_matrix_rank':len(piv),'second_betti':len(kernel),
     'rank_lower_certificate':{'row_indices':rows,'column_indices':piv,'determinant':minor_det},
     'rank_upper_certificate':{'independent_integer_kernel_vectors':kernel},
     'chain_map_verified':True,'arithmetic':'integer matrices and exact Fraction elimination',
     'scope':'finite exact cover calculation only; hyperbolicity/specialness require separate primary-source proof'}
print(json.dumps(out,indent=2))
