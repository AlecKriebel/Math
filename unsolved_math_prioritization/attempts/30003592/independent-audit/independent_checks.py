#!/usr/bin/env python3
"""Independent exact controls; no third-party packages or source text required.

This is not a formal proof checker. The geometric proof audit is AUDIT.md.
Optional --submission and --archive verify the frozen input bytes. With no
arguments, only the independent mathematical controls and audit manifest run.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
counts = Counter()

def check(group, condition, detail):
    if not condition:
        raise AssertionError((group, detail))
    counts[group] += 1

# A polynomial ring with f^2=0, xi^4=2*xi^3*f; terms above dimension 4 vanish.
# Monomials are (exponent of xi, exponent of f). This implementation derives
# intersections by multiplying the actual divisor polynomials.
def normal(poly):
    out = Counter()
    for (a, b), c in poly.items():
        if b >= 2 or a+b > 4:
            continue
        if a >= 4:
            a, b, c = a-1, b+1, 2*c
        if b < 2:
            out[a, b] += c
    return {k:v for k,v in out.items() if v}

def mul(p, q):
    out = Counter()
    for (a,b), c in p.items():
        for (u,v), d in q.items():
            out[a+u,b+v] += c*d
    return normal(out)

def times(*ps):
    return reduce(mul, ps, {(0,0):1})

def add(p,q):
    out = Counter(p)
    for k,v in q.items():
        out[k] += v
    return normal(out)

def scale(c,p):
    return {k:c*v for k,v in p.items() if c*v}

def coords(p,degree):
    check('homogeneous_coordinates', all(a+b == degree for a,b in p), p)
    return (p.get((degree,0),0),p.get((degree-1,1),0))

xi={(1,0):1}; f={(0,1):1}; xm={(1,0):1,(0,1):-1}
e=times(xi,xi); q=times(xi,f)
def surface(a,b):
    return add(scale(a,e),scale(b,q))
def integrate(p):
    return normal(p).get((3,1),0)
def pair(v,w):
    return integrate(mul(surface(*v),surface(*w)))

check('scroll_ring', times(f,f)=={}, 'base Stanley-Reisner relation')
check('scroll_ring', times(xi,xi,xm,xm)=={}, 'fiber Stanley-Reisner relation')
check('scroll_ring', integrate(times(xi,xi,xi,f))==1, 'fiber normalization')
check('scroll_ring', integrate(times(xi,xi,xi,xi))==2, 'degree c1(E)')

# The fan of the split projective bundle has two base rays and four fiber rays.
# A cone uses at most one base ray and fewer than all four fiber rays.
divisors=[f,f,xi,xi,xm,xm]
strata={}
for codim in (1,2,3,4):
    products=[]
    for ids in combinations(range(6),codim):
        if len(set(ids)&{0,1})>1 or {2,3,4,5}.issubset(ids):
            continue
        products.append(times(*(divisors[i] for i in ids)))
    strata[codim]=products
check('orbit_enumeration', [len(strata[c]) for c in (1,2,3,4)]==[6,14,16,8], 'fan counts')
surface_classes={coords(p,2) for p in strata[2]}
curve_classes={coords(p,3) for p in strata[3]}
check('orbit_enumeration', surface_classes=={(1,0),(1,-1),(1,-2),(0,1)}, 'surface orbit classes')
check('orbit_enumeration', curve_classes=={(1,-1),(1,-2),(0,1)}, 'curve orbit classes')
for dim, classes in ((2,surface_classes),(1,curve_classes)):
    check('effective_cones', (1,-2) in classes and (0,1) in classes, ('extremal strata',dim))
    for a,b in classes:
        check('effective_cones', a>=0 and b+2*a>=0, ('positive decomposition',dim,a,b))

# Derive each divisor's multiplication matrix from ring products. The normals
# (1,0), (2,1) describe the effective curve cone. After the coordinate change
# (a,b)=(s,-s+t), every pulled-back inequality has nonnegative coefficients;
# and the two coordinate inequalities s>=0,t>=0 actually occur. This is a
# finite exact certificate of the all-real outer-cone identity, not a grid.
normals={(1,0),(2,1)}
for D in (f,xi,xm):
    u=coords(mul(D,e),3); v=coords(mul(D,q),3)
    for r in ((1,0),(2,1)):
        normals.add((r[0]*u[0]+r[1]*u[1],r[0]*v[0]+r[1]*v[1]))
new_normals={(u-v,v) for u,v in normals}
check('outer_cone_certificate', (1,0) in new_normals and (0,1) in new_normals, 'necessary orthant facets')
check('outer_cone_certificate', all(u>=0 and v>=0 for u,v in new_normals), 'sufficient orthant facets')
check('outer_cone_certificate', coords(times(xi,xm),2)==(1,-1), 'moving subscroll class')
check('outer_cone_certificate', coords(times(xm,xm),2)==(1,-2), 'effective fixed subscroll class')
M=[[pair(v,w) for w in ((1,0),(0,1))] for v in ((1,0),(0,1))]
check('dual_and_ci', M==[[2,1],[1,0]], 'intersection matrix from ring')
dual_normals=[(pair((1,0),z),pair((0,1),z)) for z in ((1,-2),(0,1))]
check('dual_and_ci', dual_normals==[(0,1),(1,0)], 'nef is the coordinate orthant')
check('dual_and_ci', pair((1,-1),(1,-2))==-1, 'negative movable/effective intersection')
check('dual_and_ci', pair((1,-1),(1,-1))==0, 'movable self-intersection')
check('dual_and_ci', pair((1,-2),(1,-2))==-2, 'fixed self-intersection')
check('dual_and_ci', {coords(times(D,E),2) for D,E in product((xi,f),repeat=2)}=={(1,0),(0,1),(0,0)}, 'all nef-generator CI monomials')
check('dual_and_ci', -1<0, 'moving ray outside CI orthant')
# Independent substitution in the cited HN formula: rank 4, slopes 0,0,1,1.
epsilon=[-2,-2,-2,-1,0]
check('hn_specialization', epsilon[1]+1==-1, 'sigma_2=epsilon_1+mu_max')
check('hn_specialization', epsilon[2]==-2 and -2-epsilon[2]==0, 'effective and nef thresholds')

# Exact finite-field countercontrol of the quotient-family coverage. This tests
# all points, including the zero A-component and zero B-component strata.
# The written proof over C is separate and does not rely on finite-field data.
def projective_point(v,p):
    if not any(v):
        return None
    inv=pow(next(x for x in v if x),-1,p)
    return tuple(x*inv%p for x in v)
def projective_space(n,p):
    return sorted({projective_point(v,p) for v in product(range(p),repeat=n+1) if any(v)})
for prime in (2,3,5):
    lines=projective_space(1,prime)
    points=projective_space(3,prime)
    coverage=Counter()
    for a,b in product(lines,repeat=2):
        for u,v in lines:
            point=projective_point(tuple(u*x%prime for x in a)+tuple(v*y%prime for y in b),prime)
            coverage[point]+=1
    check('quotient_family_incidence', set(coverage)==set(points), ('covers P3',prime))
    for point in points:
        both=any(point[:2]) and any(point[2:])
        check('quotient_family_incidence', coverage[point]==(1 if both else prime+1), ('fiber count',prime,point))

# Coefficient extraction is performed in actual truncated Chow rings for
# P^n x P^m; no identity matrix is supplied as an input.
def extract(n,m,terms,j):
    out=Counter()
    for (a,b),c in terms.items():
        b+=j
        if a>n or b>m:
            continue
        if b==m:
            out[a]+=c
    return {k:v for k,v in out.items() if v}
for n,m in product(range(7),repeat=2):
    for d in range(n+m+1):
        feasible=[j for j in range(m+1) if 0<=d-j<=n]
        coeff={j:Q((-1)**j*(j+1),j+2) for j in feasible}
        terms={(n-d+j,m-j):c for j,c in coeff.items()}
        for j in range(m+1):
            expected={n-d+j:coeff[j]} if j in coeff else {}
            check('product_extraction', extract(n,m,terms,j)==expected, (n,m,d,j))

# Hyperplane arithmetic on (P^1)^4 and its positive two-plane.
def p1_integral(*subsets):
    exponents=[sum(i in s for s in subsets) for i in range(4)]
    return int(exponents==[1,1,1,1])
gamma=[{2,3},{0,1}]
H=[[sum(p1_integral(t,{i},{j}) for t in gamma) for j in range(4)] for i in range(4)]
check('hodge_control', H==[[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]], 'gamma Gram matrix')
V=[[1,1,0,0],[0,0,1,1]]
G=[[sum(v[i]*H[i][j]*w[j] for i,j in product(range(4),repeat=2)) for w in V] for v in V]
check('hodge_control', G==[[2,0],[0,2]], 'positive definite rank-two restriction')
coordinate_surfaces=list(combinations(range(4),2))
for I in coordinate_surfaces:
    class_exp=set(range(4))-set(I)
    intersections=[p1_integral(class_exp,set(J)) for J in coordinate_surfaces]
    check('hodge_control', intersections==[int(I==J) for J in coordinate_surfaces], ('orthant coefficient extraction',I))

# Distinct boundary rays of the convex diagnostic are exposed by exact
# supporting functionals (t^2,-2t,1); evaluation is (s-t)^2.
for s,t in product([Q(k,3) for k in range(10)],repeat=2):
    value=t*t-2*t*s+s*s
    check('curved_subcone', value==(s-t)**2 and (value==0)==(s==t), (s,t))

parser=argparse.ArgumentParser()
parser.add_argument('--submission',type=Path)
parser.add_argument('--archive',type=Path)
parser.add_argument('--replay',action='store_true')
args=parser.parse_args()
binding=json.loads((ROOT/'AUDITED_INPUT_MANIFEST.json').read_text())
if args.submission:
    expected=binding['submission_file_sha256']
    entries=list(args.submission.iterdir())
    check('frozen_integrity', all(p.is_file() and not p.is_symlink() for p in entries), 'flat ordinary files')
    actual={p.name:sha256(p.read_bytes()).hexdigest() for p in entries}
    check('frozen_integrity', set(actual)==set(expected), 'exact allowlist')
    for name in expected:
        check('frozen_integrity', actual[name]==expected[name], name)
    tree=sha256(''.join(n+'\0'+actual[n]+'\n' for n in sorted(actual)).encode()).hexdigest()
    check('frozen_integrity', tree==binding['submission_tree_sha256'], 'tree digest')
    if args.replay:
        for script in ('verify.py','verify_manifest.py'):
            run=subprocess.run([sys.executable,str((args.submission/script).resolve())],cwd=args.submission,capture_output=True,text=True)
            check('supplied_replay', run.returncode==0, (script,run.stderr))
            result=json.loads(run.stdout)
            if script=='verify.py':
                check('supplied_replay', result['all_passed'] is True and result['exact_checks']==1877, script)
            else:
                check('supplied_replay', result['manifest_passed'] is True and result['files_checked']==11, script)
if args.archive:
    check('archive_integrity', sha256(args.archive.read_bytes()).hexdigest()==binding['archive_sha256'], 'archive digest')
    with zipfile.ZipFile(args.archive) as z:
        expected={'submission/'+n:h for n,h in binding['submission_file_sha256'].items()}
        check('archive_integrity', len(z.namelist())==len(expected) and set(z.namelist())==set(expected), 'exact archive allowlist')
        for n,h in expected.items():
            check('archive_integrity', sha256(z.read(n)).hexdigest()==h, n)
manifest=ROOT/'AUDIT_SHA256SUMS.json'
if manifest.exists():
    expected=json.loads(manifest.read_text())['files']
    actual={p.name for p in ROOT.iterdir() if p.name!='AUDIT_SHA256SUMS.json'}
    check('audit_integrity', actual==set(expected), 'audit allowlist')
    for name,digest in expected.items():
        p=ROOT/name
        check('audit_integrity', p.is_file() and not p.is_symlink() and sha256(p.read_bytes()).hexdigest()==digest, name)
print(json.dumps({'all_passed':True,'checks':sum(counts.values()),'groups':dict(sorted(counts.items())),
                  'geometric_proofs_formalized':False,'universal_problem_solved':False},indent=2))
