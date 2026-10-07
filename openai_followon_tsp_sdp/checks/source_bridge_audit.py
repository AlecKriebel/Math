#!/usr/bin/env python3
"""Source-scope audit and independent finite checks. Pure Python; no external packages."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import argparse, hashlib, json, math, os, random, re, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = Path(os.environ.get('TSP_UPSTREAM_DIR', str(ROOT / 'sources/upstream-math')))
LEAN = UPSTREAM / 'lean'
SNAP = ROOT / 'checks/source_bridge_lean_snapshot'

def source_scope():
    # Only actual OAI proof imports are followed. ComparatorChallenges are not proofs.
    pending = ['OAI.Combinatorics.MatchingPSD.Main', 'OAI.Combinatorics.MatchingPSD.AffineLift']
    seen, unsupported, external = {}, [], set()
    while pending:
        module = pending.pop()
        if module in seen: continue
        rel = Path(*module.split('.')).with_suffix('.lean')
        src = LEAN / rel
        if not src.exists():
            unsupported.append(module); continue
        data = src.read_bytes()
        text = data.decode()
        seen[module] = {'path': str(rel), 'sha256': hashlib.sha256(data).hexdigest()}
        (SNAP / rel).parent.mkdir(parents=True, exist_ok=True)
        (SNAP / rel).write_bytes(data)
        # Strip comments, then look for proof placeholders and custom axioms.
        code = re.sub(r'/\-.*?\-/', '', text, flags=re.S)
        code = re.sub(r'--[^\n]*', '', code)
        bad = re.findall(r'\b(?:sorry|axiom)\b', code)
        if bad: unsupported.append({'module': module, 'tokens': bad})
        for imp in re.findall(r'^\s*import\s+([^\n]+)', code, flags=re.M):
            for dep in imp.split():
                if dep.startswith('OAI.'): pending.append(dep)
                else: external.add(dep)
    for rel in ['lean-toolchain', 'lake-manifest.json', 'docs/126.md']:
        src = LEAN / rel
        if src.exists():
            (SNAP / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, SNAP / rel)
    # Minimal, independent Lake project for optional reproduction at exact upstream mathlib pin.
    (SNAP / 'lakefile.lean').write_text('''import Lake\nopen Lake DSL\npackage SourceBridgeAudit where\n  leanOptions := #[⟨`autoImplicit, false⟩]\nrequire mathlib from git\n  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"\nlean_lib OAI\n''')
    # The copied upstream manifest belongs to its original multi-library project;
    # do not pretend it is our minimal project's resolved manifest.
    if (SNAP / 'lake-manifest.json').exists():
        (SNAP / 'lake-manifest.json').rename(SNAP / 'upstream-lake-manifest.json')
    return {'source_commit': subprocess.check_output(['git', '-C', str(UPSTREAM), 'rev-parse', 'HEAD'], text=True).strip(),
            'actual_proof_modules_copied': len(seen), 'modules': seen,
            'placeholder_or_missing_findings': unsupported, 'external_imports': sorted(external),
            'upstream_build_cache_exists': (LEAN / '.lake').exists(),
            'scope': 'Superpolynomial unshifted matching slack rank and exact affine lift size only; no exponential or positive-shift theorem.'}

def zeros(n,m): return [[0.0]*m for _ in range(n)]
def eye(n): return [[float(i==j) for j in range(n)] for i in range(n)]
def tr(a): return sum(a[i][i] for i in range(len(a)))
def transpose(a): return [list(x) for x in zip(*a)]
def add(a,b,sgn=1): return [[a[i][j]+sgn*b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def mul(a,b):
    bt=transpose(b)
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]
def scale(a,c): return [[c*x for x in row] for row in a]
def frob2(a): return sum(x*x for row in a for x in row)
def compress(a,basis): return mul(transpose(basis),mul(a,basis))
def embed(a,basis): return mul(basis,mul(a,transpose(basis)))

def jacobi(a):
    a=[row[:] for row in a]; n=len(a); v=eye(n)
    for _ in range(max(1,100*n*n)):
        pairs=[(abs(a[i][j]),i,j) for i in range(n) for j in range(i+1,n)]
        if not pairs: break
        mag,p,q=max(pairs)
        if mag <= 1e-14 * max(1.0,max(abs(a[i][i]) for i in range(n))): break
        phi=0.5*math.atan2(2*a[p][q],a[q][q]-a[p][p])
        c,s=math.cos(phi),math.sin(phi)
        rot=eye(n);rot[p][p]=rot[q][q]=c;rot[p][q]=s;rot[q][p]=-s
        a=mul(transpose(rot),mul(a,rot));v=mul(v,rot)
    return [a[i][i] for i in range(n)],v

def subbasis(v,indices): return [[row[j] for j in indices] for row in v]
def splitting(arr):
    n=len(arr[0])
    if len(arr)==1: return [eye(n)]
    total=zeros(n,n)
    for a in arr[1:]:total=add(total,a)
    eigen,v=jacobi(add(arr[0],total,-1))
    pp=[i for i,e in enumerate(eigen) if e>=0]
    qq=[i for i,e in enumerate(eigen) if e<0]
    bp,bq=subbasis(v,pp),subbasis(v,qq)
    p=mul(bp,transpose(bp)) if pp else zeros(n,n)
    if not qq: return [p]+[zeros(n,n) for _ in arr[1:]]
    inner=splitting([compress(a,bq) for a in arr[1:]])
    return [p]+[embed(a,bq) for a in inner]

def splitting_check():
    rng=random.Random(12620261006); cases=0; max_ratio=0.; max_projector_error=0.; two_max=0.
    for n in range(1,9):
        for count in range(2,7):
            for iteration in range(8):
                arr=[]
                for z in range(count):
                    k=rng.randint(1,n)
                    x=[[rng.uniform(-2,2) for _ in range(k)] for _ in range(n)]
                    arr.append(scale(mul(x,transpose(x)),10.**rng.randint(-2,2)))
                ps=splitting(arr)
                lhs=sum(frob2(mul(p,mul(a,p))) for z,a in enumerate(arr) for s,p in enumerate(ps) if s!=z)
                overlap=sum(tr(mul(a,b)) for z,a in enumerate(arr) for zz,b in enumerate(arr) if z!=zz)
                bound=2.**(count-1)*overlap
                assert lhs <= bound + 1e-8*max(1.,bound), (n,count,lhs,bound)
                max_ratio=max(max_ratio,lhs/bound if bound else 0.)
                summed=zeros(n,n)
                for p in ps:
                    summed=add(summed,p)
                    max_projector_error=max(max_projector_error,math.sqrt(frob2(add(mul(p,p),p,-1))))
                max_projector_error=max(max_projector_error,math.sqrt(frob2(add(summed,eye(n),-1))))
                if count==2:
                    # Source's stronger two-matrix estimate has unordered overlap tr(A B).
                    two_bound=tr(mul(arr[0],arr[1]))
                    assert lhs <= two_bound+1e-8*max(1.,two_bound)
                    two_max=max(two_max,lhs/two_bound if two_bound else 0.)
                cases+=1
    return {'seed':12620261006,'noncommuting_psd_cases':cases,'source_bound_max_ratio':max_ratio,
            'two_matrix_bound_max_ratio':two_max,'max_projector_error':max_projector_error,
            'status':'pass; floating point falsification checks, not proof'}

def pairings(vertices):
    if not vertices: yield (); return
    a=vertices[0]
    for i,b in enumerate(vertices[1:],1):
        rest=vertices[1:i]+vertices[i+1:]
        for p in pairings(rest):yield ((a,b),)+p

def local_trace_check():
    results=[]
    # Exact rational T*T Frobenius trace against the printed combinatorial formula.
    for k in (4,6,8):
        d=2
        for b in (0,1):
            w=k//2 if k//2%2==b else k//2+1
            cuts=[frozenset(c) for c in combinations(range(k),w)]
            ni=len(cuts); count=k*(k-1)*math.prod(range(1,k-d,2))
            for y in ((0,0),(1,1)) if b==0 else ((0,1),(1,0)):
                s=sum(y);h=(k-d)//2;g=(w-s)//2
                if not 0<=g<=h:continue
                supportsize=math.comb(h,g)
                # Ordinary K entries equal N/|M| * sum_m pi_y^m(a)pi_y^m(a').
                kk=[[0]*ni for _ in range(ni)]
                marg=[0]*ni;actual=0
                for v1 in range(k):
                    for v2 in range(k):
                        if v1==v2:continue
                        rem=tuple(i for i in range(k) if i not in (v1,v2))
                        for p in pairings(rem):
                            support=[j for j,a in enumerate(cuts) if ((v1 in a)==bool(y[0])) and ((v2 in a)==bool(y[1])) and all((u in a)==(v in a) for u,v in p)]
                            assert len(support)==supportsize
                            for j in support:
                                marg[j]+=1
                                for z in support:kk[j][z]+=1
                            actual+=1
                assert actual==count
                assert all(Fraction(x,count*supportsize)==Fraction(1,ni) for x in marg)
                fac=Fraction(ni,count*supportsize**2)
                direct=sum((fac*x)**2 for row in kk for x in row)
                formula=sum(Fraction(math.comb(g,j)**2*math.comb(h-g,j)**2*math.comb(k,w),math.comb(h,g)**2*math.comb(w,2*j)*math.comb(k-w,2*j)) for j in range(min(g,h-g)+1))
                assert direct==formula
                results.append({'k':k,'b':b,'y':list(y),'rows':ni,'local_data':count,'trace_K2':str(direct)})
    return {'cases':results,'status':'pass; exact rational marginal and kernel-trace checks'}

def shift_check():
    # Exact rational fixtures validate the block-diagonal construction itself.
    f=[[Fraction(2),Fraction(1)],[Fraction(1),Fraction(2)]]
    g=[[Fraction(1),Fraction(-1,2)],[Fraction(-1,2),Fraction(1)]]
    rho=Fraction(1,2)
    ff=[f[0]+[Fraction(0)],f[1]+[Fraction(0)],[Fraction(0),Fraction(0),rho]]
    gg=[g[0]+[Fraction(0)],g[1]+[Fraction(0)],[Fraction(0),Fraction(0),Fraction(1)]]
    assert tr(mul(ff,gg))==tr(mul(f,g))+rho
    return {'rho':str(rho),'unshifted_pairing':str(tr(mul(f,g))),'shifted_pairing':str(tr(mul(ff,gg))),
            'status':'pass; exact block-diagonal identity'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--finite-only',action='store_true');args=parser.parse_args()
    receipt={'shift':shift_check(),'orthogonal_splitting':splitting_check(),'local_kernel':local_trace_check()}
    if not args.finite_only: receipt['scope']=source_scope()
    output='source_bridge_finite_results.json' if args.finite_only else 'source_bridge_receipt.json'
    (ROOT/'checks'/output).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:({'actual_proof_modules_copied':v['actual_proof_modules_copied'],'placeholder_or_missing_findings':v['placeholder_or_missing_findings'],'external_imports':v['external_imports']} if k=='scope' else v) for k,v in receipt.items()},indent=2))
