#!/usr/bin/env python3
"""Independent exact controls. Does not import, execute, or alter author code.

Uses symbolic polynomial differentiation, a global determinantal syzygy, and
exhaustive exact strict-linear feasibility, rather than the author's grid and
coordinate-difference checks. No control proves the general dimension conjecture.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

DIM = 20
ZERO = (0,) * DIM
CHECKS = []
NEGATIVES = []

def check(value, name):
    if not value:
        raise ValueError(name)
    CHECKS.append(name)

def reject(call, name, category):
    try:
        call()
    except ValueError:
        NEGATIVES.append({'name': name, 'category': category, 'rejected': True})
        return
    raise ValueError('Accepted negative control: ' + name)

def add(*polys):
    out = {}
    for poly in polys:
        for m, c in poly.items():
            out[m] = out.get(m, F(0)) + c
            if not out[m]:
                del out[m]
    return out

def scale(poly, c):
    return {m: v*c for m,v in poly.items() if v*c}

def mul(a,b):
    out = {}
    for x,c in a.items():
        for y,d in b.items():
            z = tuple(s+t for s,t in zip(x,y))
            out[z] = out.get(z,F(0)) + c*d
            if not out[z]:
                del out[z]
    return out

def const(n):
    return {ZERO: F(n)} if n else {}

def var(j):
    m = list(ZERO); m[j] = 1
    return {tuple(m): F(1)}

def value(poly, point):
    return sum(c * prod(point[j]**e for j,e in enumerate(m)) for m,c in poly.items())

def prod(values):
    out = F(1)
    for v in values:
        out *= v
    return out

def derivative(poly, j):
    out = {}
    for m,c in poly.items():
        if m[j]:
            q = list(m); q[j] -= 1
            out[tuple(q)] = c*m[j]
    return out

def parity(p):
    return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))

def pdet(matrix):
    terms = []
    for p in permutations(range(len(matrix))):
        t = const(parity(p))
        for i,j in enumerate(p):
            t = mul(t,matrix[i][j])
        terms.append(t)
    return add(*terms)

def det(matrix):
    return sum(F(parity(p))*prod(F(matrix[i][j]) for i,j in enumerate(p))
               for p in permutations(range(len(matrix))))

def echelon_rank(matrix):
    rows = [list(map(F,r)) for r in matrix]
    active = 0
    for col in range(len(rows[0]) if rows else 0):
        pivot = next((r for r in range(active,len(rows)) if rows[r][col]),None)
        if pivot is None:
            continue
        rows[active],rows[pivot] = rows[pivot],rows[active]
        for k in range(active+1,len(rows)):
            c = rows[k][col]/rows[active][col]
            rows[k] = [a-c*b for a,b in zip(rows[k],rows[active])]
        active += 1
        if active == len(rows):
            break
    return active

def strict_feasible(rows):
    """Exact Fourier-Motzkin, inequalities sum(a_i*x_i)+constant > 0."""
    rows = [tuple(map(F,r)) for r in rows]
    while rows and len(rows[0])>1:
        pos = [r for r in rows if r[0]>0]
        neg = [r for r in rows if r[0]<0]
        keep = [r[1:] for r in rows if r[0]==0]
        for p in pos:
            for n in neg:
                keep.append(tuple((-n[0])*p[j]+p[0]*n[j] for j in range(1,len(p))))
        rows = list(set(keep))
    return all(r[0]>0 for r in rows)

LINES = [(1,0,0),(0,1,0),(1,1,-1),(1,-1,0),(1,3,-1),(2,1,-1)]

def labels(signs):
    x,y,s,t,u,v = signs
    return [x>0 and y>0 and s<0,
            y<0 and t>0 and u<0,
            s>0 and u>0 and v>0,
            x<0 and t<0 and v<0]

def digest(data):
    return hashlib.sha256(data).hexdigest()

ZIP_HASH = '966970b14c7350553393b14ca378ad764d8ae2cd38b47cb00556fd6c51bf4e81'
MANIFEST_HASH = 'b09ba6fceaad28780e2dea06cbc24bfd07ac7205149ff8358659655bfc0b9018'
EXPECTED_NAMES = {'EXACT_RESULTS.json','MANIFEST.json','PROOF.md','README.md',
                  'RESEARCH_LOG.md','SOURCE_VERIFICATION.json','STATUS.json','verify.py'}

def verify_identity(zip_bytes, manifest_bytes):
    check(len(zip_bytes)==23424 and digest(zip_bytes)==ZIP_HASH,'Frozen ZIP identity')
    check(digest(manifest_bytes)==MANIFEST_HASH,'Frozen manifest identity')

def scope(s):
    check(s.get('problem_id')=='30001893','Problem identity')
    check(s.get('status')=='partial' and s.get('full_source_solved') is False,'Partial only')
    check(s.get('approaches_completed')==5,'Five completed approaches')
    for field in ['novelty_claimed','current_global_openness_verified',
                  'live_target_statement_inspected','raw_upstream_ai_corpora_inspected']:
        check(s.get(field) is False,'Scope guard '+field)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--author-release',type=Path,default=Path(__file__).resolve().parent.parent/'release')
    ap.add_argument('--author-zip',type=Path,default=Path(__file__).resolve().parent.parent/'AUTHOR_SAFE_FREEZE.zip')
    args = ap.parse_args()
    root = args.author_release
    zb = args.author_zip.read_bytes(); mb = (root/'MANIFEST.json').read_bytes()
    verify_identity(zb,mb)
    check({p.name for p in root.iterdir()}==EXPECTED_NAMES,'Exact author directory inventory')
    mf = json.loads(mb)
    check({e['path'] for e in mf['files']}==EXPECTED_NAMES-{'MANIFEST.json'},'Manifest payload inventory')
    binding = []
    with zipfile.ZipFile(args.author_zip) as z:
        check(len(z.namelist())==8 and set(z.namelist())==EXPECTED_NAMES,'ZIP member inventory')
        check(z.testzip() is None,'ZIP CRC integrity')
        for name in sorted(EXPECTED_NAMES):
            p = root/name
            check(p.is_file() and not p.is_symlink(),'Regular author file '+name)
            b = p.read_bytes()
            check(z.read(name)==b,'ZIP/author byte match '+name)
            if name!='MANIFEST.json':
                e = next(e for e in mf['files'] if e['path']==name)
                check(e['bytes']==len(b) and e['sha256']==digest(b),'Author manifest binding '+name)
            binding.append({'path': name,'bytes': len(b),'sha256': digest(b)})
    status = json.loads((root/'STATUS.json').read_text())
    scope(status)

    # Symbolically expand the six determinants, then differentiate them.
    vertices = [[var(3*i+j) for j in range(3)] for i in range(4)]
    a,b,c,d,e,f,g,h = [var(j) for j in range(12,20)]
    rays = [[const(1),a,b],[const(-1),c,d],[e,const(-1),f],[g,h,const(-1)]]
    pairs = list(combinations(range(4),2))
    polynomials = [pdet([[add(vertices[j][k],scale(vertices[i][k],-1)),rays[i][k],rays[j][k]]
                        for k in range(3)]) for i,j in pairs]
    point = list(map(F,[4,4,4,-4,0,0,0,-4,0,0,0,-4,1,1,0,0,0,0,0,0]))
    check([value(p,point) for p in polynomials]==[0]*6,'All six incidence equations')
    jac = [[value(derivative(p,j),point) for j in range(DIM)] for p in polynomials]
    rank = echelon_rank(jac)
    check(rank==5,'Independent symbolic Jacobian rank five')
    check(all(sum(row[j] for row in jac)==0 for j in range(DIM)),'Left-null vector is all ones')
    cols = [0,1,4,5,6]
    minor = det([[jac[i][j] for j in cols] for i in range(5)])
    check(minor==1,'Leibniz five-by-five determinant +1')

    # Independent polynomial relation, valid for arbitrary vertex and ray coordinates.
    alpha = [scale(pdet([[rays[j][k] for j in range(4) if j!=i] for k in range(3)]),(-1)**i)
             for i in range(4)]
    check(all(not add(*(mul(alpha[i],rays[i][k]) for i in range(4))) for k in range(3)),
          'Symbolic signed-minor ray dependence')
    syzygy = add(*(mul(mul(alpha[i],alpha[j]),p) for (i,j),p in zip(pairs,polynomials)))
    check(not syzygy,'Global polynomial weighted planarity identity')
    alpha_base = [value(p,point) for p in alpha]
    check(alpha_base==[-1]*4,'All signed ray minors nonzero at base')

    # Exhaust all open chambers of all six boundary lines; no point-grid sampling.
    feasible = []
    for signs in product((-1,1),repeat=6):
        rows = [[s*v for v in line] for s,line in zip(signs,LINES)]
        if strict_feasible(rows):
            check(sum(labels(signs))==1,'Exact feasible chamber '+''.join('+' if s>0 else '-' for s in signs))
            feasible.append(signs)
    check(len(feasible)==19,'Nineteen feasible strict arrangement chambers')
    witnesses = [(F(1,4),F(1,4)),(F(1,2),-1),(1,1),(-1,F(1,2))]
    for i,(x,y) in enumerate(witnesses):
        sg = [1 if a*x+b*y+c>0 else -1 if a*x+b*y+c<0 else 0 for a,b,c in LINES]
        check(labels(sg)==[j==i for j in range(4)],'Nonempty open region '+str(i))
    cycle = [[1,-1,0],[1,3,-1],[2,1,-1]]
    cycle_det = det(cycle)
    check(cycle_det==-1,'Independent outer-cycle determinant -1')
    check(det([[1,-1,0],[1,2,-1],[2,1,-1]])==0,'Concurrent cycle zero-determinant control')

    # Infinitesimal fiber check, not substituted for the manuscript's all-n argument.
    functions = [[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,F(1,4),F(1,4),F(1,4)]]
    edges = list(combinations(range(5),2))
    fiber = []
    for q,(i,j) in enumerate(edges):
        for k in range(4):
            row = [F(0)]*30
            row[4*i+k]=1; row[4*j+k]=-1
            row[20+q]=-(functions[i][k]-functions[j][k])
            fiber.append(row)
    fiber_rank = echelon_rank(fiber)
    check(fiber_rank==25,'Five-dimensional infinitesimal affine-plus-scale fiber')

    # Adversarial controls are deliberately separated into mathematical and scope/binding guards.
    reject(lambda: check(rank==6,'Six-independent-equation mutation'),'Rank six','mathematical')
    reject(lambda: check(20-rank==14,'False local dimension mutation'),'Local dimension fourteen','mathematical')
    reject(lambda: check(minor==-1,'Wrong minor sign'),'Minor sign reversal','mathematical')
    reject(lambda: check(cycle_det==0,'False regularity certificate'),'Zero nonregular determinant','mathematical')
    altered = point.copy(); altered[12] += F(1,7)
    reject(lambda: check(all(value(p,altered)==0 for p in polynomials),'Invalid perturbed incidence'),
           'Uncompensated ray movement','mathematical')
    altered_identity = add(syzygy,polynomials[0])
    reject(lambda: check(not altered_identity,'Altered symbolic identity'),'Wrong syzygy weight','mathematical')
    reject(lambda: check(strict_feasible([(1,0,0),(-1,0,0)]),'Impossible strict opposite signs'),
           'Contradictory strict halfplanes','mathematical')
    reject(lambda: check(strict_feasible([(0,0,0)]),'Empty strict zero halfspace'),
           'Zero strict inequality','mathematical')
    reject(lambda: check(4*1-5==0,'Out-of-range n=1 formula'),'Extending regular formula to n=1','range')
    reject(lambda: check(2*(2*5-4)==15,'Fixed versus moving apex'),'Counting translations with fixed apex','range')
    reject(lambda: check(4*5-5==4*5-1,'Old count substitution'),'Using printed old count as corrected theorem','range')
    reject(lambda: check(30-fiber_rank==1,'Missing common-affine gauge'),'Ignoring common-affine fiber','mathematical')
    reject(lambda: verify_identity(zb+b'\n',mb),'Appended ZIP bytes','binding')
    reject(lambda: verify_identity(zb,mb+b'\n'),'Appended manifest bytes','binding')
    for key,new in [('problem_id','30001894'),('status','solved'),('full_source_solved',True),
                    ('approaches_completed',4),('novelty_claimed',True),
                    ('current_global_openness_verified',True),('live_target_statement_inspected',True),
                    ('raw_upstream_ai_corpora_inspected',True)]:
        changed = dict(status); changed[key]=new
        reject(lambda changed=changed: scope(changed),'Claim mutation '+key,'scope guard')

    out = {'problem_id':'30001893','verdict':'PASS_PARTIAL_ONLY','author_zip_sha256':ZIP_HASH,
           'author_manifest_sha256':MANIFEST_HASH,'author_files':binding,
           'independent_check_count':len(CHECKS),'checks':CHECKS,
           'jacobian':[[int(x) for x in row] for row in jac],
           'jacobian_rank':rank,'minor_rows':[0,1,2,3,4],'minor_columns':cols,'minor_value':int(minor),
           'weighted_syzygy_identically_zero':not syzygy,'signed_ray_minors_at_base':[int(x) for x in alpha_base],
           'local_incidence_dimension':20-rank,'strict_arrangement_chambers':len(feasible),
           'nonregular_cycle_determinant':int(cycle_det),'infinitesimal_fiber_dimension':30-fiber_rank,
           'negative_controls':NEGATIVES,'negative_controls_rejected':len(NEGATIVES),
           'full_source_solved':False,'general_dimension_conjecture_proved':False,
           'scope':'Exact authored examples and byte/scope controls. Universal bounds use the audited analytic proofs.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
