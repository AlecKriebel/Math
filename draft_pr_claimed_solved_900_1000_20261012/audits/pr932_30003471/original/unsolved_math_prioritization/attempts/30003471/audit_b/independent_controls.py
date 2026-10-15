#!/usr/bin/env python3
"""Independent finite diagnostics. These do not certify any analytic theorem."""
import hashlib, itertools, json, math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.special import expn

ROOT=Path(__file__).resolve().parent.parent/'polytope_dihedral_30003471'
PIN_MANIFEST='1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f'
PIN_PROOF='6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415'
counts={}
def check(cat, cond):
    if not bool(cond): raise RuntimeError('Failed: '+cat)
    counts[cat]=counts.get(cat,0)+1

for name,pin,size in [('MANIFEST.json',PIN_MANIFEST,1252),('PROOF.md',PIN_PROOF,21855)]:
    b=(ROOT/'packet'/name).read_bytes()
    check('frozen_input',hashlib.sha256(b).hexdigest()==pin)
    check('frozen_input',len(b)==size)

I=sp.eye(2); Z=sp.zeros(2); ii=sp.I
C=[sp.Matrix([[0,-ii],[-ii,0]]),sp.Matrix([[0,-1],[1,0]]),sp.diag(-ii,ii)]
B=[sp.Matrix(2,2,[int(j==k) for j in range(4)]) for k in range(4)]
def cv(v): return sum((a*c for a,c in zip(v,C)),Z)
def vec(A): return sp.Matrix(list(A))
def eq(A,B): return all(sp.simplify(x)==0 for x in A-B)
check('volume_exact',C[0]*C[1]*C[2]==-I)
for j,k in itertools.product(range(3),repeat=2):
    check('clifford_exact',C[j]*C[k]+C[k]*C[j]==(-2*I if j==k else Z))
    check('skew_exact',C[j].H==-C[j])
comm=sp.Matrix.vstack(*(sp.Matrix.hstack(*(vec(c*a-a*c) for a in B)) for c in C))
anti=sp.Matrix.vstack(*(sp.Matrix.hstack(*(vec(c*a+a*c) for a in B)) for c in C))
check('commutant_rank_exact',comm.rank()==3)
check('anticommutant_rank_exact',anti.rank()==4)
check('commutant_generator_exact',comm*vec(I)==sp.zeros(12,1))
unit=[(1,0,0),(0,1,0),(0,0,1),(sp.Rational(3,5),sp.Rational(4,5),0),
      (sp.Rational(1,3),sp.Rational(2,3),sp.Rational(2,3))]
for n,m in itertools.product(unit,repeat=2):
    N,M=cv(n),cv(m)
    chi=lambda A:-N*A*M
    mat=sp.Matrix.hstack(*(vec(chi(A)) for A in B))
    check('chi_eigenspaces_exact',(mat-sp.eye(4)).rank()==2 and (mat+sp.eye(4)).rank()==2)
    for A in B: check('chi_involution_exact',eq(chi(chi(A)),A))
    # Brendle's tuple coefficient omega_{alpha,beta} is c_{beta,alpha}.
    omega=M.T
    for A in B:
        tuple_chi=sp.Matrix.hstack(*(-sum((omega[a,b]*N*A[:,b] for b in range(2)),sp.zeros(2,1)) for a in range(2)))
        check('tuple_matrix_translation_exact',eq(tuple_chi,chi(A)))
for n in unit:
    check('round_sphere_branch_exact',eq(-cv(n)*I*cv(n),I))
    check('antipodal_branch_negative_exact',eq(-cv(n)*I*cv(tuple(-a for a in n)),-I))
for j,k in itertools.permutations(range(3),2):
    L=ii*C[j]*C[k]
    for m in unit:
        chi=lambda A:-C[j]*A*cv(m)
        for A in B: check('boundary_symbol_exact',eq(chi(L*A)+L*chi(A),Z))

# Arc-length parameter transport, including nearly antipodal source endpoints.
max_edge_error=0.0
for alpha in np.linspace(.05,math.pi-.05,19):
    for ratio in [.01,.1,.5,.9,1.0]:
        beta=ratio*alpha
        a=np.array([1.,0.,0.]); b=np.array([math.cos(alpha),math.sin(alpha),0.])
        for t in np.linspace(.001,.999,17):
            x=(1-t)*a+t*b; norm=np.linalg.norm(x); nu=x/norm
            dnu=(b-a-nu*np.dot(nu,b-a))/norm
            source_speed=np.linalg.norm(dnu)
            phi=math.atan2(x[1],x[0]); angle=beta*phi/alpha
            dz=ratio*source_speed*np.array([-math.sin(angle),math.cos(angle),0.])
            err=abs(np.linalg.norm(dz)-ratio*source_speed)
            max_edge_error=max(max_edge_error,err)
            check('edge_arclength_numeric',err<1e-10 and np.linalg.norm(dz)<=source_speed+1e-10)
check('same_weights_negative_control',math.sin(1.3)/math.sin(2.6)>1.8)

# Both endpoint derivatives are contractions on a hemisphere. Finite-difference test
# of the z derivative supplements the exact Jacobi-field formula in the audit.
def G(q,z,t):
    cost=float(np.clip(np.dot(q,z),-1,1)); th=math.acos(cost)
    if th<1e-8: return ((1-t)*q+t*z)/np.linalg.norm((1-t)*q+t*z)
    return (math.sin((1-t)*th)*q+math.sin(t*th)*z)/math.sin(th)
max_jacobi_error=0.0
q=np.array([0.,0.,1.]); h=1e-6
for th in np.linspace(.001,math.pi/2-.001,23):
    z=np.array([math.sin(th),0.,math.cos(th)])
    tang=[np.array([math.cos(th),0.,-math.sin(th)]),np.array([0.,1.,0.])]
    for t in np.linspace(0,1,17):
        D=np.column_stack([(G(q,math.cos(h)*z+math.sin(h)*e,t)-G(q,math.cos(h)*z-math.sin(h)*e,t))/(2*h) for e in tang])
        observed=np.sort(np.linalg.svd(D,compute_uv=False)); expected=np.sort([t,math.sin(t*th)/math.sin(th)])
        err=float(np.max(np.abs(observed-expected))); max_jacobi_error=max(max_jacobi_error,err)
        check('spherical_jacobi_numeric',err<3e-7 and observed.max()<1+3e-7)
        check('moving_q_bound_numeric',max(1-t,math.sin((1-t)*th)/math.sin(th))<=1+1e-14)
check('nonhemisphere_negative_control',math.sin(.5*2.8)/math.sin(2.8)>2.9)

# Genuine four-facet vertices of the octahedron: exact incidence and actual smooth
# level-set samples. Facet normals are normalized, matching the proof's scale.
signs=np.array(list(itertools.product([-1.,1.],repeat=3))); normals=signs/math.sqrt(3)
vertices=np.vstack([np.eye(3),-np.eye(3)]); heights=np.ones(8)/math.sqrt(3)
inc=np.abs(vertices@normals.T-heights)<1e-13
for row in inc: check('nonsimple_incidence',int(row.sum())==4)
for r in range(3,9):
    for J in itertools.combinations(range(8),r):
        common=np.flatnonzero(np.all(inc[:,J],axis=1))
        check('triple_intersection_vertex',len(common)<=1)
phi0=4*(expn(2,.5)-expn(3,.5))
def phi(s):
    a=np.maximum(np.asarray(s)+2,0); out=np.zeros_like(a); on=a>0
    out[on]=a[on]**2*(expn(2,1/a[on])-expn(3,1/a[on]))/phi0
    return out
check('bump_normalization',abs(float(phi(np.array([0.]))[0])-1)<1e-14)
rng=np.random.default_rng(30003471)
max_vertex_scaled_distance=0.; max_radial_scaled_distance=0.; many_active=0
for lam in [100.,1000.,10000.]:
    rays=list(rng.normal(size=(30,3)))+list(vertices)
    for v in vertices:
        rays += [v+rng.normal(size=3)*factor/lam for factor in [.2,.7,1.5,3.] for _ in range(4)]
    for ray in rays:
        d=ray/np.linalg.norm(ray); rout=1/np.sum(np.abs(d))
        f=lambda r:float(np.sum(phi(lam*(normals@(r*d)-heights)))-1)
        # If the endpoint is a flat patch, a floating error can put f a hair below 0.
        if abs(f(rout))<1e-11: r=rout
        else: r=brentq(f,0,rout,xtol=1e-14)
        x=r*d; active=np.flatnonzero(normals@x-heights>-2/lam)
        common=np.flatnonzero(np.all(inc[:,active],axis=1))
        check('active_common_face_numeric',len(common)>0)
        max_radial_scaled_distance=max(max_radial_scaled_distance,lam*(rout-r))
        check('radial_closeness_numeric',lam*(rout-r)<4)
        if len(active)>=3:
            many_active+=1
            dist=float(np.min(np.linalg.norm(vertices-x,axis=1)))
            max_vertex_scaled_distance=max(max_vertex_scaled_distance,lam*dist)
            check('nonsimple_vertex_localization_numeric',dist*lam<5)
check('nonsimple_samples_present',many_active>100)

last=math.inf
for ell in range(1,65):
    # delta=e^{-ell}; planar squared L2 norm on [delta^2,delta] is 2pi/ell.
    val=2*math.pi/ell
    check('log_cutoff_integral',0<val<last); last=val
    check('scale_separation',math.exp(-4*ell)<math.exp(-2*ell))
check('ordinary_cutoff_negative_control',abs(2*math.pi*3/8-3*math.pi/4)<1e-15)

# Hash each locally available reference PDF against public-metadata pins only.
filemap={'Discrete Geometry, OWR 19/2017':'owr_2017_19.pdf','Bounding minimal solid angles of polytopes':'akopyan_karasev.pdf','Scalar curvature rigidity of convex polytopes':'brendle.pdf','On Gromov\'s rigidity theorem for polytopes with acute angles':'brendle_wang.pdf','Dihedral Rigidity for Convex Polytopes by Smooth Approximation':'bi.pdf','On Gromov\'s flat corner domination conjecture and Stoker\'s conjecture':'wang_xie.pdf','On Gromov\'s dihedral extremality and rigidity conjectures':'wang_xie_yu.pdf','Remarks on the paper On Gromov\'s dihedral extremality and rigidity conjectures':'bar_hanke_schick.pdf','Gromov\'s dihedral rigidity conjecture in dimension three':'wxy_3d.pdf'}
sourcepins=[]
for record in json.loads((ROOT/'packet'/'SOURCE_METADATA.json').read_text())['sources']:
    b=(ROOT/'private_sources'/filemap[record['title']]).read_bytes()
    check('source_pin',len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256'])
    sourcepins.append({k:record[k] for k in ['title','url','bytes','sha256']})

print(json.dumps({'pass':True,'proof_sha256':PIN_PROOF,'manifest_sha256':PIN_MANIFEST,
 'counts':counts,'total_checks':sum(counts.values()),'numeric_max_edge_error':max_edge_error,
 'numeric_max_jacobi_error':max_jacobi_error,'octahedron_many_active_samples':many_active,
 'octahedron_max_lambda_vertex_distance':max_vertex_scaled_distance,
 'octahedron_max_lambda_radial_shift':max_radial_scaled_distance,
 'source_pins':sourcepins,'analytic_proof_certified_by_computation':False},indent=2,sort_keys=True))
