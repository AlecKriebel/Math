#!/usr/bin/env python3
"""Stdlib finite-Fock controls only; not a continuum proof or a PDE validation."""
import cmath
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOL = 3e-11
CHECKS = []

def dot(x, y):
    return sum(a.conjugate()*b for a,b in zip(x,y))

def norm(x):
    return math.sqrt(max(0.0, dot(x,x).real))

def eye(n):
    return [[complex(i==j) for j in range(n)] for i in range(n)]

def adj(a):
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]

def mm(a,b):
    c=[[0j]*len(b[0]) for _ in a]
    for i,row in enumerate(a):
        for k,v in enumerate(row):
            if v:
                for j,w in enumerate(b[k]):
                    if w:
                        c[i][j] += v*w
    return c

def mv(a,x):
    return [sum(v*w for v,w in zip(row,x)) for row in a]

def residual(a,b):
    return max(abs(a[i][j]-b[i][j]) for i in range(len(a)) for j in range(len(a[0])))

def record(name,value,limit=TOL,detail=None):
    ok=value <= limit
    CHECKS.append({'name':name,'observed_residual':value,'allowed_residual':limit,'pass':ok,'detail':detail})
    if not ok:
        raise AssertionError(CHECKS[-1])

def basis(d,i):
    return [complex(j==i) for j in range(d)]

def random_unitary(d,rng):
    cols=[]
    for _ in range(d):
        v=[complex(rng.uniform(-1,1),rng.uniform(-1,1)) for _ in range(d)]
        for u in cols:
            z=dot(u,v)
            v=[x-z*y for x,y in zip(v,u)]
        r=norm(v)
        cols.append([x/r for x in v])
    return [[cols[j][i] for j in range(d)] for i in range(d)]

def col(a,j):
    return [row[j] for row in a]

def projection(gs,d):
    return [[sum(g[i]*g[j].conjugate() for g in gs) for j in range(d)] for i in range(d)]

def create_vec(g,v):
    d=len(g)
    out=[0j]*(1<<d)
    for mask,z in enumerate(v):
        if z:
            for i,gi in enumerate(g):
                if gi and not mask & (1<<i):
                    sign=(-1)**((mask & ((1<<i)-1)).bit_count())
                    out[mask | (1<<i)] += gi*sign*z
    return out

def wedge(gs,d):
    v=[0j]*(1<<d)
    v[0]=1
    for g in reversed(gs):
        v=create_vec(g,v)
    return v

def creation(g):
    size=1<<len(g)
    cols=[create_vec(g,basis(size,j)) for j in range(size)]
    return [[cols[j][i] for j in range(size)] for i in range(size)]

def dg(q):
    d=len(q); size=1<<d
    a=[[0j]*size for _ in range(size)]
    for mask in range(size):
        for j in range(d):
            if mask & (1<<j):
                r=mask ^ (1<<j)
                sj=(-1)**((mask & ((1<<j)-1)).bit_count())
                for i in range(d):
                    if not r & (1<<i):
                        si=(-1)**((r & ((1<<i)-1)).bit_count())
                        a[r | (1<<i)][mask] += sj*si*q[i][j]
    return a

def gamma(u):
    d=len(u); size=1<<d
    cols=[wedge([col(u,j) for j in range(d) if mask & (1<<j)],d) for mask in range(size)]
    return [[cols[j][i] for j in range(size)] for i in range(size)]

def det(a):
    a=[row[:] for row in a]
    z=1+0j
    for k in range(len(a)):
        pivot=max(range(k,len(a)),key=lambda j:abs(a[j][k]))
        if abs(a[pivot][k]) < 1e-15:
            return 0j
        if pivot!=k:
            a[pivot],a[k]=a[k],a[pivot]; z=-z
        z*=a[k][k]
        for i in range(k+1,len(a)):
            fac=a[i][k]/a[k][k]
            for j in range(k+1,len(a)):
                a[i][j]-=fac*a[k][j]
    return z

def one_body_group(s,energies,t):
    return [[sum(s[i][k]*cmath.exp(1j*t*energies[k])*s[j][k].conjugate() for k in range(len(s)))
             for j in range(len(s))] for i in range(len(s))]

rng=random.Random(30006191)
for case in range(10):
    d=5 if case<5 else 6
    n=2 if d==5 else 3
    occupied=random_unitary(d,rng)
    qbasis=random_unitary(d,rng)
    gs=[col(occupied,j) for j in range(n)]
    q=projection([col(qbasis,j) for j in range(3)],d)
    record(f'projection_identity_{case}',residual(mm(q,q),q))
    psi=wedge(gs,d)
    record(f'normalized_exterior_{case}',abs(norm(psi)-1))
    m=dg(q); mpsi=mv(m,psi)
    mean=dot(psi,mpsi).real
    second=dot(mpsi,mpsi).real
    compression=[[dot(gi,mv(q,gj)) for gj in gs] for gi in gs]
    lam=sum(compression[i][i].real for i in range(n))
    trc2=sum(compression[i][j]*compression[j][i] for i in range(n) for j in range(n)).real
    variance=lam-trc2
    record(f'mean_trace_{case}',abs(mean-lam))
    record(f'second_trace_{case}',abs(second-(lam*lam+variance)))
    record(f'variance_upper_{case}',max(0.0,variance-lam))
    u=0.37+0.03*case
    r=[[complex(i==j)+(cmath.exp(1j*u)-1)*q[i][j] for j in range(d)] for i in range(d)]
    lhs=dot(psi,wedge([mv(r,g) for g in gs],d))
    c=[[complex(i==j)+(cmath.exp(1j*u)-1)*compression[i][j] for j in range(n)] for i in range(n)]
    record(f'exterior_counting_determinant_{case}',abs(lhs-det(c)))

# Full CAR and covariance with an arbitrary one-particle mixing unitary.
d=6; size=1<<d
cs=[creation(basis(d,i)) for i in range(d)]
ans=[adj(c) for c in cs]
car_res=0.0
for i in range(d):
    for j in range(d):
        a=mm(ans[i],cs[j]); b=mm(cs[j],ans[i])
        expected=eye(size) if i==j else [[0j]*size for _ in range(size)]
        car_res=max(car_res,residual([[a[r][s]+b[r][s] for s in range(size)] for r in range(size)],expected))
record('full_Fock_CAR',car_res)
s=random_unitary(d,rng); energies=[0.3*(j+1)**2 for j in range(d)]
f=basis(d,0); A=cs[0]
u=one_body_group(s,energies,0.137); G=gamma(u)
record('second_quantization_unitarity',residual(mm(G,adj(G)),eye(size)))
record('free_covariance_plus_sign',residual(mm(mm(G,A),adj(G)),creation(mv(u,f))))
occupied_overlap=math.sqrt(sum(abs(u[j][0])**2 for j in (1,2)))
CHECKS.append({'name':'evolved_orbital_has_nonzero_occupied_overlap','pass':occupied_overlap>0.02,'occupied_overlap':occupied_overlap})
assert occupied_overlap>0.02
phase_plus=cmath.exp(1j*0.137*4)*dot(f,mv(u,f))
phase_minus=cmath.exp(-1j*0.137*4)*dot(f,mv(u,f))
CHECKS.append({'name':'negative_control_number_phase_minus_sign_rejected','pass':abs(phase_plus-phase_minus)>0.05,'observed_difference':abs(phase_plus-phase_minus)})
assert abs(phase_plus-phase_minus)>0.05
wrong_sign=residual(mm(mm(G,A),adj(G)),creation(mv(adj(u),f)))
CHECKS.append({'name':'negative_control_covariance_minus_sign_rejected','pass':wrong_sign>0.05,'observed_difference':wrong_sign})
assert wrong_sign>0.05

# Reference phase at generic time detects its sign; prescribed time detects coefficient.
for sigma in (0,1):
    for n in (1,2,3,4,5):
        psi=wedge([basis(d,j) for j in range(1,n+1)],d)
        xi=create_vec(f,psi)
        for tag,t in [('generic',0.137),('chosen',math.pi/(2*n+1-sigma))]:
            u=one_body_group(s,energies,t); G=gamma(u)
            UK=[[cmath.exp(1j*t*r.bit_count()*(r.bit_count()-sigma))*G[r][c] for c in range(size)] for r in range(size)]
            FH=dot(xi,mv(UK,mv(A,mv(adj(UK),psi))))
            expected=cmath.exp(1j*t*(2*n+1-sigma))*dot(f,mv(u,f))
            record(f'reference_phase_sigma{sigma}_N{n}_{tag}',abs(FH-expected))
            overlap=dot(xi,create_vec(mv(u,f),psi))
            record(f'overlap_without_evolved_orthogonality_sigma{sigma}_N{n}_{tag}',abs(overlap-dot(f,mv(u,f))))
            if tag=='chosen':
                record(f'exact_minus_one_phase_sigma{sigma}_N{n}',abs(cmath.exp(1j*t*(2*n+1-sigma))+1))
                # Zero kinetic reference isolates the exact norm-2 annihilation witness.
                U0=[[cmath.exp(1j*t*r.bit_count()*(r.bit_count()-sigma))*complex(r==c) for c in range(size)] for r in range(size)]
                B=[[v-A[i][j] for j,v in enumerate(row)] for i,row in enumerate(mm(mm(U0,A),adj(U0)))]
                z=mv(adj(B),xi)
                record(f'adjoint_maximal_witness_sigma{sigma}_N{n}',norm([zj+2*pj for zj,pj in zip(z,psi)]))
                record(f'variable_vector_state_value_four_sigma{sigma}_N{n}',abs(dot(z,z).real-4))

wrong_normal_shift=abs(cmath.exp(1j*(math.pi/4)*5)+1)
wrong_half=abs(cmath.exp(1j*math.pi/2)+1)
CHECKS.append({'name':'negative_control_omitted_normal_shift_rejected','pass':wrong_normal_shift>0.1,'observed_difference':wrong_normal_shift})
CHECKS.append({'name':'negative_control_half_pair_coefficient_rejected','pass':wrong_half>0.1,'observed_difference':wrong_half})
assert wrong_normal_shift>0.1 and wrong_half>0.1

# Density product and ordered distinct pairs in a 3-mode bounded cell analogue.
inside=(0,1,2)
L=dg([[complex(i==j and i in inside) for j in range(d)] for i in range(d)])
density=mm(L,L)
normal=[[0j]*size for _ in range(size)]
for i in inside:
    for j in inside:
        if i!=j:
            term=mm(mm(mm(cs[i],cs[j]),ans[j]),ans[i])
            for r in range(size):
                for c in range(size):
                    normal[r][c] += term[r][c]
record('density_minus_normal_equals_diagonal_number',residual([[density[i][j]-normal[i][j] for j in range(size)] for i in range(size)],L))
record('ordered_pairs_no_half_coefficient',residual(normal,mm(L,[[L[i][j]-complex(i==j) for j in range(size)] for i in range(size)])))
record('vacuum_sector_density_zero',abs(density[0][0]))
record('one_particle_normal_ordered_zero',max(abs(normal[1<<i][1<<i]) for i in range(d)))
record('one_particle_density_inside_one',abs(density[1][1]-1))

# Negative controls expose invalid general-state and one-sided replacements.
n=4; eps=1/16
mean=n*eps; var=n*n*eps*(1-eps)
assert var>mean
CHECKS.append({'name':'negative_control_arbitrary_state_variance_rejected','pass':True,'mean':mean,'variance':var,'n':n,'outside_probability':eps})
psi=wedge([basis(d,1),basis(d,2)],d); xi=create_vec(f,psi)
UK=eye(size)
UH=[[complex(i==j)*(-1 if i.bit_count()==3 else 1) for j in range(size)] for i in range(size)]
EN=norm([a-b for a,b in zip(mv(UH,psi),psi)])
EN1=norm([a-b for a,b in zip(mv(UH,xi),xi)])
FH=dot(mv(UH,xi),mv(A,mv(UH,psi))); FK=dot(xi,mv(A,psi))
record('two_vector_bound_control',max(0.0,abs(FH-FK)-EN-EN1))
assert EN==0 and abs(FH-FK)>1.99
CHECKS.append({'name':'negative_control_one_sector_error_rejected','pass':True,'N_error':EN,'N_plus_one_error':EN1,'matrix_element_difference':abs(FH-FK)})
# Growth-gap and Duhamel exponents are checked symbolically with exact rational arithmetic.
from fractions import Fraction
record('Duhamel_sqrt_term_exponent',abs(float(Fraction(11,6)-2+Fraction(1,6))))
record('Duhamel_mean_term_exponent',abs(float(Fraction(8,3)-3+Fraction(1,3))))

assert all(c['pass'] for c in CHECKS)
result={'scope':'Independent finite-dimensional CAR/exterior algebra controls; these do not prove continuum propagation, self-adjointness, or the infinite-N limit. Those have analytic derivations in the review.','implementation':'Python 3 standard library only; deterministic seed 30006191. No original validation code imported.','checks_count':len(CHECKS),'all_pass':True,'checks':CHECKS}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks_count':len(CHECKS),'all_pass':True,'max_positive_control_residual':max(c.get('observed_residual',0) for c in CHECKS),'output':'CHECK_RESULTS.json'},indent=2))
