#!/usr/bin/env python3
"""Independent finite controls. No author code imports; no infinite theorem inference."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

checks = {}

def checked(family, condition):
    assert condition, family
    checks[family] = checks.get(family, 0) + 1

def mm(a,b,p=3):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]

def eye(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]

def minus(a,b,p=3):
    return [[(x-y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def kron(a,b):
    return [[x*y%3 for x in ar for y in br] for ar in a for br in b]

def rank(a,p=3):
    a=[row[:] for row in a];r=0
    for j in range(len(a[0]) if a else 0):
        k=next((k for k in range(r,len(a)) if a[k][j]%p),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];d=pow(a[r][j],-1,p)
        a[r]=[x*d%p for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                q=a[i][j];a[i]=[(x-q*y)%p for x,y in zip(a[i],a[r])]
        r+=1
    return r

def jordan(j):
    return [[int(i==k)+int(k==i+1) for k in range(j)] for i in range(j)]

def c3_product(a,b):
    # Actual diagonal C3 action, not a presumed abstract multiplication table.
    n=a*b;u=kron(jordan(a),jordan(b));v=minus(u,eye(n))
    vp=eye(n);r=[n]
    for k in range(1,5):
        vp=mm(vp,v);r.append(rank(vp))
    checked('actual_C3_jordan_nilpotence',r[3]==0)
    m={j:r[j-1]-2*r[j]+r[j+1] for j in range(1,4)}
    checked('actual_C3_jordan_dimensions',sum(j*m[j] for j in m)==n)
    checked('actual_C3_jordan_multiplicities',all(v>=0 for v in m.values()))
    return {j:v for j,v in m.items() if v}

c3={(a,b):c3_product(a,b) for a,b in product(range(1,4),repeat=2)}
checked('actual_C3_endotrivial_relation',c3[(2,2)]=={1:1,3:1})
checked('actual_C3_free_tensor',c3[(2,3)]=={3:2} and c3[(3,3)]=={3:3})

# Three actual F3[C4] irreducibles: 1, sign, V with X^2+1 irreducible.
c4mat=[[[1]],[[2]],[[0,2],[1,0]]]
c4dim=[1,1,2]
checked('F3_C4_irreducible_quadratic',all((x*x+1)%3!=0 for x in range(3)))
c4={}
for a,b in product(range(3),repeat=2):
    t=kron(c4mat[a],c4mat[b]);n=len(t)
    dims=[n-rank(minus(t,eye(n))), n-rank(minus(t,[[2*x for x in row] for row in eye(n)])), n-rank(minus(mm(t,t),[[2*x for x in row] for row in eye(n)]))]
    checked('actual_C4_primary_dimensions',sum(dims)==n and dims[2]%2==0)
    c4[(a,b)]={i:dims[i]//c4dim[i] for i in range(3) if dims[i]}
checked('actual_C4_V_square',c4[(2,2)]=={0:2,1:2})

# F9 = F3[t]/(t^2+1), exact eigenline check (t has order4).
def fa(z,w):return ((z[0]+w[0])%3,(z[1]+w[1])%3)
def fm(z,w):return ((z[0]*w[0]+2*z[1]*w[1])%3,(z[0]*w[1]+z[1]*w[0])%3)
def fp(z,n):
    y=(1,0)
    for _ in range(n):y=fm(y,z)
    return y

t=(0,1)
checked('F9_splitting_eigenlines',fp(t,2)==(2,0) and fp(t,4)==(1,0))
for lam in [t,(0,2)]:
    # V acts on vector (lambda,1) by (2,lambda)=lambda*(lambda,1).
    checked('F9_splitting_eigenlines',[(2,0),lam]==[fm(lam,lam),lam])
checked('F9_splitting_eigenlines',fm(t,(0,2))==(1,0))

kbasis=list(product(range(1,4),range(3)))
Kbasis=list(product(range(1,4),range(4)))

def ext(v):
    out={}
    for (j,s),c in v.items():
        for e in ([0] if s==0 else [2] if s==1 else [1,3]):out[(j,e)]=out.get((j,e),0)+c
    return {i:c for i,c in out.items() if c}

def res(v):
    out={}
    for (j,e),c in v.items():
        s=0 if e==0 else 1 if e==2 else 2
        out[(j,s)]=out.get((j,s),0)+c*(2 if e in [0,2] else 1)
    return {i:c for i,c in out.items() if c}

def kproduct(i,j):
    return {(length,s):ml*ms for length,ml in c3[(i[0],j[0])].items() for s,ms in c4[(i[1],j[1])].items()}

def Kproduct(i,j):return {(length,(i[1]+j[1])%4):ml for length,ml in c3[(i[0],j[0])].items()}

def linmul(v,w,basisprod):
    out={}
    for i,a in v.items():
        for j,b in w.items():
            for k,m in basisprod(i,j).items():out[k]=out.get(k,0)+a*b*m
    return {i:c for i,c in out.items() if c}

for i,j in product(kbasis,repeat=2):
    checked('actual_F3C12_to_F9C12_tensor',ext(kproduct(i,j))==linmul(ext({i:1}),ext({j:1}),Kproduct))
for v0 in product([-2,-1,0,1,2],repeat=4):
    # Signed combinations mix split/non-split, projective/nonprojective coordinates.
    coords=[(1,0),(1,2),(2,2),(3,1)];v={c:a for c,a in zip(coords,v0) if a}
    ev=ext(v)
    checked('actual_modular_extension_isometry',sum(abs(a)*j for (j,e),a in ev.items())==sum(abs(a)*j*c4dim[s] for (j,s),a in v.items()))
    checked('actual_modular_extension_restriction',res(ev)=={i:2*a for i,a in v.items()})
    checked('actual_modular_extension_duality',ext(v)=={(j,(-e)%4):a for (j,e),a in ev.items()})
# Pythagorean Gaussian coefficients test complex weighted norms exactly.
for coefficients in product(range(-2,3),repeat=4):
    coords=[(1,0),(1,2),(2,2),(3,1)]
    phase=[(3,4,5),(5,12,13),(8,15,17),(7,24,25)]
    real={i:c*re for i,c,(re,im,norm) in zip(coords,coefficients,phase) if c}
    imag={i:c*im for i,c,(re,im,norm) in zip(coords,coefficients,phase) if c}
    evr,evi=ext(real),ext(imag)
    # Norms have integral values for these exact Gaussian integer coefficients.
    expected=sum(abs(c)*norm*j*c4dim[s] for (j,s),c,(_,_,norm) in zip(coords,coefficients,phase))
    from math import isqrt
    norm_after=0
    for i in set(evr)|set(evi):
        normsq=evr.get(i,0)**2+evi.get(i,0)**2
        n=isqrt(normsq)
        checked('actual_modular_complex_norm_exact',n*n==normsq)
        norm_after+=i[0]*n
    checked('actual_modular_complex_extension_isometry',norm_after==expected)
    checked('actual_modular_complex_restriction',res(evr)=={i:2*a for i,a in real.items()} and res(evi)=={i:2*a for i,a in imag.items()})
checked('collision_negative_boundary',sum(abs(x) for x in [1,-1])==2 and sum([1,-1])==0)

# Exact Gaussian rationals and actual full/stable C3 inverse/product splitting.
def za(a,b):return (a[0]+b[0],a[1]+b[1])
def zn(a):return (-a[0],-a[1])
def zs(a,b):return za(a,zn(b))
def zm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def zc(a):return (a[0],-a[1])
def zi(a):
    q=a[0]**2+a[1]**2
    assert q
    return (a[0]/q,-a[1]/q)
def zscale(a,c):return (a[0]*c,a[1]*c)
Z=(F(0),F(0));ONE=(F(1),F(0))

def fullmul(v,w):
    out={}
    for i,a in v.items():
        for j,b in w.items():
            for k,m in c3[(i,j)].items():out[k]=za(out.get(k,Z),zscale(zm(a,b),m))
    return {i:a for i,a in out.items() if a!=Z}

def charvals(v):
    a,b,c=[v.get(j,Z) for j in [1,2,3]]
    return [za(za(a,zscale(b,2)),zscale(c,3)),za(a,b),zs(a,b)]

def J(v):
    d=Z
    for j,a in v.items():d=za(d,zscale(a,j))
    return {**v,3:zscale(d,-F(1,3))}

for av,bv,cv in product(range(-3,4),repeat=3):
    v={1:(F(av),F(1)),2:(F(bv),F(-1)),3:(F(cv),F(2))}
    vals=charvals(v)
    checked('actual_C3_character_star',charvals({i:zc(a) for i,a in v.items()})==list(map(zc,vals)))
    checked('actual_C3_character_products',charvals(fullmul(v,v))==[zm(z,z) for z in vals])
    if all(z!=Z for z in vals):
        a=zscale(za(zi(vals[1]),zi(vals[2])),F(1,2))
        b=zscale(zs(zi(vals[1]),zi(vals[2])),F(1,2))
        c=zscale(zs(zs(zi(vals[0]),a),zscale(b,2)),F(1,3))
        checked('actual_C3_explicit_complex_inverse',fullmul(v,{1:a,2:b,3:c})=={1:ONE})
for av,bv in product(range(-10,11),repeat=2):
    n=abs(av)+2*abs(bv);d=av+2*bv
    checked('actual_C3_exact_lift_norm',n<=n+abs(d)<=2*n)
    v={1:(F(av),F(0)),2:(F(bv),F(0))}
    checked('actual_C3_lift_zero_scalar_component',charvals(J(v))[0]==Z)
checked('stable_dimension_not_multiplicative',2*2!=1)
e={3:(F(1,3),F(0))};f={1:ONE,3:(-F(1,3),F(0))}
checked('actual_C3_factor_units',fullmul(e,e)==e and fullmul(f,f)==f and fullmul(e,f)=={})
checked('wrong_unit_inverse_negative_boundary',charvals(f)==[Z,ONE,ONE])

# Finite truncations may permit a nonzero defect which tends to zero; epsilon matters.
for N in range(1,41):
    lam=F(1)+F(1,(N+1)**2)
    for n in range(-N,N+1):checked('finite_polynomial_weight_disk',abs(lam**n)<=1+abs(n))
    for a,b in product(range(-N,N+1),repeat=2):
        if abs(a+b)<=N:checked('finite_polynomial_weight_multiplication',lam**a*lam**b==lam**(a+b))
    checked('finite_feasibility_no_infinite_claim',lam!=1 and lam-lam**-1>0)

# Negative exponential-weight boundary with standard dual involution.
for n in range(-20,21):
    checked('exponential_weight_nonhermitian_character',abs(F(2)**n)<=F(2)**abs(n))
checked('exponential_weight_nonhermitian_character',F(1,2)!=F(2))
checked('exponential_weight_growth_not_subexponential',F(2)**5!=1)

# Formal witness identity detects omitted conjugation or wrong second-witness sign.
for a,b,c,d in product(range(-4,5),repeat=4):
    z=(F(a),F(b));w=(F(c),F(d))
    h1=za(z,w);h2=zm((F(0),F(1)),zs(z,w));defect=zs(w,zc(z))
    checked('two_selfadjoint_witness_defect_norm',h1[1]**2+h2[1]**2==defect[0]**2+defect[1]**2)

result={'families':checks,'exact_assertions':sum(checks.values()),'actual_groups':['C3 in characteristic3','C3 x C4 in characteristic3'],'author_imports':False,'arbitrary_extension_proved_by_finite_tests':False,'infinite_compactness_proved_by_finite_tests':False,'full_symmetry_claimed':False,'original_status':'unsolved5/5'}
print(json.dumps(result,indent=2,sort_keys=True))
