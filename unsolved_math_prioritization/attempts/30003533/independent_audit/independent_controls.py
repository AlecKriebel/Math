#!/usr/bin/env python3
"""Independent exact and numerical controls; never imports the author verifier.
Finite checks are not an infinite-dimensional PDE proof. No in-place writes.
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, math
from fractions import Fraction as F
from itertools import product
from pathlib import Path

FROZEN = '2ed09ec9ba1d31bb913b84c6e63f3256394744c7635817ec2a1467cbcb124ec0'
NAMES = {'CLAIMS.json','GATE.md','LEDGER.json','PROOFS.md','REPLAY.json','RESULT.md','SOURCES.md','SOURCE_METADATA.json','VALIDATION.md','controls.py','selftest.py','verify.py'}
FALSE = {'original_target_resolved','novelty_claim','independent_audit_passed','finite_checks_prove_pde','smooth_counterexample_proved','polyhedral_counterexample_is_smooth','uniform_inverse_implies_coercivity','star_combined_equals_standard','deformation_bound_is_fixed_domain_high_frequency','acyclicity_without_contraction_suffices','source_liminf_display_is_well_formed','source_strong_nontrapping_is_formally_defined','full_current_literature_exhausted','publication_payload_contains_third_party_source_text'}
EXPECTED = {'schema_version':1,'problem_id':30003533,'status':'unsolved','substantive_attempts':5,'operator':'0.5 I + Dprime_k - i k eta S_k','space':'complex L2(Gamma, ds)','coupling':'eta > 0 fixed before k varies','coercivity':'inf over unit v of abs(inner(A_k v, v))','geometric_controls':{'r_min':'3/4','support_ball_radius':'3/8','curvature_at_pi_over_3':'-8/3','curvature_numerator_at_pi_over_3':'-9/8'},'matrix_A':[[1,2],[0,1]],'matrix_P':[[1,-1],[-1,3]],'zero_vector':[1,-1],'nilpotent_N2_counterexample_weight':2,'deformation_dimension':3,'deformation_growth_power':2}
EXPECTED.update({x:False for x in FALSE})
counts = {'integrity':0,'exact':0,'numerical':0}

def check(value, label, kind='exact'):
    counts[kind] += 1
    if not value:
        raise ValueError(label)

def pairs(items):
    result = {}
    for k,v in items:
        if k in result: raise ValueError('duplicate key')
        result[k] = v
    return result

def reject_constant(value):
    raise ValueError('non-finite JSON')

def read(path):
    return json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=reject_constant)

def typed_equal(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def integrity(root, digest):
    check(root.is_dir(),'missing packet','integrity')
    check({p.name for p in root.iterdir()} == NAMES|{'MANIFEST.json'},'inventory','integrity')
    for p in root.iterdir(): check(p.is_file() and not p.is_symlink(),'nonregular file','integrity')
    check(hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()==digest,'manifest pin','integrity')
    m=read(root/'MANIFEST.json')
    check(type(m) is dict and set(m)=={'schema_version','files'} and type(m['schema_version']) is int and m['schema_version']==1,'manifest schema','integrity')
    check(type(m['files']) is dict and set(m['files'])==NAMES,'manifest names','integrity')
    for name,entry in m['files'].items():
        check(type(entry) is dict and set(entry)=={'bytes','sha256'},'entry schema','integrity')
        data=(root/name).read_bytes()
        check(type(entry['bytes']) is int and entry['bytes']==len(data),'byte count','integrity')
        check(type(entry['sha256']) is str and entry['sha256']==hashlib.sha256(data).hexdigest(),'payload digest','integrity')
    check(typed_equal(read(root/'CLAIMS.json'),EXPECTED),'claim semantics','integrity')
    l=read(root/'LEDGER.json')
    check(type(l) is dict and type(l.get('problem_id')) is int and l['problem_id']==30003533,'ledger identity','integrity')
    check(l.get('rank')==1000 and type(l['rank']) is int and l.get('problem_number')=='OWR-15576-002','ledger rank','integrity')
    check(l.get('status')=='unsolved' and l.get('turns')=='5/5' and l.get('original_target_resolved') is False and l.get('independent_review')=='pending','ledger scope','integrity')
    a=l.get('attempts')
    check(type(a) is list and len(a)==5,'attempt count','integrity')
    for i,v in enumerate(a,1):
        check(type(v) is dict and type(v.get('turn')) is int and v['turn']==i,'attempt ordinal type/value','integrity')
        check(all(type(v.get(k)) is str and v[k] for k in ('method','derived_result','gap')),'attempt content','integrity')
    for name in ('REPLAY.json','SOURCE_METADATA.json'): read(root/name)

# Gaussian rationals represented by (real, imaginary), without floating point.
def z(a=0,b=0): return (F(a),F(b))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
def scale(q,a): return (q*a[0],q*a[1])
def inner(a,b):
    v=z()
    for x,y in zip(a,b): v=add(v,mul(x,conj(y)))
    return v
def norm(a): return inner(a,a)[0]
def mv(m,v):
    return [tuple(sum(mul(c,w)[j] for c,w in zip(row,v)) for j in (0,1)) for row in m]

def polyadd(a,b):
    n=max(len(a),len(b));return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(n)]
def polymul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def controls():
    # Global polynomial coefficient identity, rather than a finite-angle identity claim.
    r=[F(1),F(1,4)]; rp2=[F(9,16),0,F(-9,16)]; rpp=[0,F(-9,4)]
    curvature=polyadd(polyadd(polymul(r,r),[2*x for x in rp2]),[-x for x in polymul(r,rpp)])
    check(curvature==[F(17,8),F(11,4),F(-1,2)],'global curvature polynomial')
    check(sum(curvature[i]*(-1)**i for i in range(3))==F(-9,8),'negative curvature numerator')
    check(F(-9,8)/F(3,4)**3==F(-8,3),'marked curvature')
    check(F(9,4)**2/F(34)>F(3,8)**2,'strict support bound')
    # Boundary derivative cancellation with arbitrary nonzero tangential weight derivatives.
    for a,ap,kappa in product((F(1,3),F(1),F(7,2)),(F(-9),F(0),F(11)),(F(-8,3),F(-1,9))):
        tangent=(1,0);normal=(0,1);dn=(kappa,0)
        dz=tuple(ap*normal[i]+a*dn[i] for i in range(2))
        check(sum(tangent[i]*dz[i] for i in range(2))==a*kappa,'weight derivative vanishes tangentially')
    # Graph jets at p=0: X_t(u)=(u1,u2,t*(u1^2+2u2^2)/2).
    for t in (F(0),F(1,3),F(1),F(2)):
        for i,j in product(range(-6,7),repeat=2):
            u,v=F(i,12),F(j,12);rho2=u*u+v*v
            if not rho2: continue
            q=u*u+2*v*v; a=-t*q/2; at=-q/2; rsq=rho2+t*t*q*q/4
            check(abs(a)<=t*rho2 and abs(at)<=rho2,'quadratic normal jet')
            check(rho2<=rsq<=3*rho2,'uniform local separation')
    A=[[z(1),z(2)],[z(),z(1)]];P=[[z(1),z(-1)],[z(-1),z(3)]]
    for a,b,c,d in product(range(-2,3),repeat=4):
        v=[z(a,b),z(c,d)]
        check(inner(mv(P,mv(A,v)),v)[0]==norm(v),'complex weighted Hermitian identity')
        check(inner(mv(P,v),v)[0]>=0,'complex positive metric')
    check(inner(mv(A,[z(1),z(-1)]),[z(1),z(-1)])==z(),'original zero quadratic form')
    check(F(1)-F(1)*F(1)==0 and norm([z(1)])>0,'sufficient criterion is not necessary')
    # Complex weighted-shift telescoping and dilation-intertwining inner-product identity.
    for n in range(1,14):
        for trial in range(1,10):
            w=[F((trial+2*j)%7,6) for j in range(n-1)]
            v=[z(F((3*j+trial)%11-5,7),F((j+2*trial)%9-4,5)) for j in range(n)]
            defect=[F(1)]+[1-x*x for x in w]
            def T(v): return [scale(w[j],v[j+1]) for j in range(n-1)]+[z()]
            q=v;total=F(0);cross=z()
            for _ in range(n):
                tq=T(q)
                total+=sum(defect[j]*norm([q[j]]) for j in range(n))
                cross=add(cross,inner([scale(defect[j],tq[j]) for j in range(n)],q))
                q=tq
            check(norm(q)==0,'nilpotence')
            check(total==norm(v),'complex defect telescoping')
            check(cross==inner(T(v),v),'dilation intertwining form')
            check(norm(T(v))<=norm(v),'contractivity')
    for n in range(1,65):
        theta=math.pi/(n+1);v=[math.sin((j+1)*theta) for j in range(n)]
        lam=math.cos(theta)
        for j in range(n):
            lhs=((v[j-1] if j else 0)+(v[j+1] if j+1<n else 0))/2
            check(abs(lhs-lam*v[j])<=2e-14,'shift top eigenvector','numerical')
        check(1-lam+2e-15>=2/(n+1)**2,'escape polynomial comparison','numerical')
    # Block lower bounds with genuinely complex off-diagonal phases.
    for a,d,b,l in ((F(2),F(3),F(1),F(1)),(F(3,4),F(1,2),F(1,4),F(1,4))):
        check((a-l)*(d-l)>=b*b and a>=l and d>=l,'block lower determinant')
        h=scale(-b,z(F(3,5),F(4,5)));M=[[z(a),h],[conj(h),z(d)]]
        for x,y,s,t in product(range(-2,3),repeat=4):
            v=[z(x,y),z(s,t)]
            check(inner(mv(M,v),v)[0]>=l*norm(v),'complex block certificate')
    for n in range(2,66):
        gap=F(1,2**n)
        for weight in (F(0),F(1,7),F(1,2),F(5,7),F(1)):
            check(gap*weight+F(1,2)*(1-weight)>=gap,'rank-one gap minimum')

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent.parent/'public');p.add_argument('--manifest',default=FROZEN)
    a=p.parse_args();integrity(a.packet,a.manifest);controls()
    print(json.dumps({'status':'PASS_INDEPENDENT_FINITE_CONTROLS_ONLY','counts':counts,'pde_target_resolved':False},sort_keys=True,separators=(',',':')))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('INDEPENDENT_CONTROL_FAILED: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
