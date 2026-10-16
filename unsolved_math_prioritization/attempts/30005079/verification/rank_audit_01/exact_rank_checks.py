#!/usr/bin/env python3
"""Independent exact Fraction arithmetic controls, standard library only.

Uses polynomial antiderivative recurrence, exact rational Taylor enclosures, and
formal leading-resultant coefficients. No numerical approximation proves rank.
"""
from fractions import Fraction as F
from math import factorial, gcd
from pathlib import Path
import hashlib, json, sys

ROOT=Path(__file__).resolve().parent
A=[(-1,0,[4,4,1]),(0,2,[4,-4,1])]
B=[(-1,1,[2,1])]

def integral_poly(coeffs,l,u):
    return sum((F(c,k+1)*(F(u)**(k+1)-F(l)**(k+1)) for k,c in enumerate(coeffs)), F(0))

def moment(pieces,n):
    return sum((integral_poly([0]*n+c,l,u) for l,u,c in pieces),F(0))

def deriv(c):
    return [F(i)*c[i] for i in range(1,len(c))]

def at(c,x):
    return sum((a*F(x)**i for i,a in enumerate(c)),F(0))

def elementary(pieces):
    # Integral of p(x)e^(-tx) has antiderivative
    # -e^(-tx) sum_{k>=0} p^(k)(x) t^(-k-1).
    ans={}
    for l,u,rho in pieces:
        p=[F(0)]+[F(c) for c in rho]
        k=0
        while p:
            for end,sgn in [(u,-1),(l,1)]:
                key=(-end,-k-1)
                ans[key]=ans.get(key,F(0))+sgn*at(p,end)
            p=deriv(p); k+=1
    return {k:v for k,v in ans.items() if v}

EA={(1,-1):F(-1),(1,-2):F(-1),(1,-3):F(2),(1,-4):F(6),(0,-3):F(-16),(-2,-3):F(-4),(-2,-4):F(-6)}
EB={(1,-1):F(-1),(1,-3):F(2),(-1,-1):F(-3),(-1,-2):F(-4),(-1,-3):F(-2)}
assert elementary(A)==EA
assert elementary(B)==EB
assert (moment(A,0),moment(A,1),moment(B,0),moment(B,1))==(F(5),F(5,12),F(4),F(2,3))

def abs_first(pieces):
    ans=F(0)
    for l,u,rho in pieces:
        p=[F(0)]+[F(c) for c in rho]
        for lo,hi,sign in [(l,min(u,0),-1),(max(l,0),u,1)]:
            if lo<hi: ans+=sign*integral_poly(p,lo,hi)
    return ans

def enclosure(pieces,t,radius,N=24):
    assert 0<t*radius<1
    center=sum(((-t)**k*moment(pieces,k+1)/factorial(k) for k in range(N+1)),F(0))
    # e<3 follows from n!>=2^(n-1), strict for n>=4.
    err=F(3)*abs_first(pieces)*(t*radius)**(N+1)/factorial(N+1)
    return center-err,center+err,err

brackets={}
for name,pieces,radius,lo,hi in [('a',A,2,F('0.27379184'),F('0.27379185')),('b',B,1,F('0.52761951'),F('0.52761953'))]:
    left=enclosure(pieces,lo,radius); right=enclosure(pieces,hi,radius)
    assert left[0]>0 and right[1]<0
    brackets[name]={'bracket':[str(lo),str(hi)],'left_lower_exact':str(left[0]),'left_upper_exact':str(left[1]),'right_lower_exact':str(right[0]),'right_upper_exact':str(right[1]),'taylor_error_left_exact':str(left[2]),'taylor_error_right_exact':str(right[2]),'abs_first_moment_exact':str(abs_first(pieces)),'N':24,'signs':[1,-1]}

# Polygon integrals can be done from width y+2 and center x=y/2.
assert integral_poly([2,1],-1,1)==4
assert integral_poly([0,2,1],-1,1)==F(2,3)
assert integral_poly([0,1,F(1,2)],-1,1)==F(1,3)
normals=[(1,0),(0,1),(-1,1),(0,-1)]
assert [normals[i][0]*normals[(i+1)%4][1]-normals[i][1]*normals[(i+1)%4][0] for i in range(4)]==[1]*4
# Independent all-p,q RESULTANT proof is algebraic and appears in ANALYTIC_FREEZE.md.
# Here actual small Sylvester determinants provide finite controls only.
def trim(a):
    a=list(a)
    while a and not a[-1]: a.pop()
    return a

def padd(a,b):
    return trim([(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(max(len(a),len(b)))])

def neg(a): return [-x for x in a]

def pmul(a,b):
    if not a or not b: return []
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)

def pdiv(a,b):
    assert b
    a=trim(a); q=[F(0)]*max(0,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        i=len(a)-len(b); v=a[-1]/b[-1]; q[i]+=v
        a=padd(a,neg([F(0)]*i+[v*x for x in b]))
    assert not a, 'Bareiss nonexact polynomial division'
    return trim(q)

def resultant(p,q):
    r=F(p,q); m=3*p; n=2*q; size=m+n
    f=[[] for _ in range(m+1)]; g=[[] for _ in range(n+1)]
    f[0]=[F(6),4*r]; f[2*p]=[F(0),16*r]; f[3*p]=[F(-6),-2*r,r*r,r**3]
    g[0]=[F(2),F(4),F(3)]; g[n]=[F(-2),F(0),F(1)]
    # Rows have descending Z coefficients.
    rows=[]
    for i in range(n): rows.append([[]]*i+f[::-1]+[[]]*(n-i-1))
    for i in range(m): rows.append([[]]*i+g[::-1]+[[]]*(m-i-1))
    M=[[list(x) for x in row] for row in rows]
    prev=[F(1)]; sign=1
    for k in range(size-1):
        if not M[k][k]:
            pivot=next(i for i in range(k+1,size) if M[i][k])
            M[k],M[pivot]=M[pivot],M[k]; sign*=-1
        pivot=M[k][k]
        for i in range(k+1,size):
            for j in range(k+1,size):
                M[i][j]=pdiv(padd(pmul(M[i][j],pivot),neg(pmul(M[i][k],M[k][j]))),prev)
        for i in range(k+1,size): M[i][k]=[]
        prev=pivot
    return [sign*x for x in M[-1][-1]]

controls=[]
for p,q in [(1,1),(1,2),(2,1),(2,3),(3,2)]:
    res=resultant(p,q); r=F(p,q)
    assert len(res)-1==6*(p+q)
    assert res[-1]==r**(6*q)*3**(3*p)
    controls.append({'p':p,'q':q,'actual_T_degree':len(res)-1,'actual_leading_coefficient_exact':str(res[-1])})

# Input-byte check, read-only: these are original source receipts rather than acceptance.
base=ROOT.parent
receipt=json.loads((base/'SOURCE_MANIFEST.json').read_text())
for f in receipt['files']:
    b=(base/'source'/f['path']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']

out={'python':sys.version.split()[0],'arithmetic':'fractions.Fraction only','source_files_matching_receipt':len(receipt['files']),'elementary_moment_integrals':{'A_identity_verified':True,'B_identity_verified':True,'masses':['5','4'],'first_moments':['5/12','2/3']},'rational_root_brackets':brackets,'toric':{'fan_determinants':[1,1,1,1],'area':'4','centroid':['1/12','1/6'],'reflection':'(x,y) -> (y-x,y)'},'resultant_leading_coefficient_controls':controls,'scope':'Exact identity/sign controls and input integrity. Irrationality/rank require the separate general proof, not these finite controls.'}
(ROOT/'EXACT_RANK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':'PASS','source_files':len(receipt['files']),'signs':{k:v['signs'] for k,v in brackets.items()},'resultant_controls':len(controls)},indent=2))
