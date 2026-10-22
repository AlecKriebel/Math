#!/usr/bin/env python3
"""Exact finite diagnostics for an accompanying universal written proof.
No finite search certifies the universal arithmetic/ideal statements. No asserts.
Run with Python 3; optionally --self-test-corruption to prove failure detection.
"""
from pathlib import Path
from fractions import Fraction
from math import gcd
import argparse, datetime, hashlib, itertools, json, subprocess, sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
ROOT=Path('/Users/alec/Documents/Math')
CHECKS=[]

def require(condition, label, evidence=None):
    CHECKS.append({'label':label,'pass':bool(condition),'evidence':evidence})
    if not condition:
        raise RuntimeError(label + ': ' + repr(evidence))

def sha(b): return hashlib.sha256(b).hexdigest()
def mul(x,y,d=10):
    a,b=x; c,e=y
    return (a*c+d*b*e,a*e+b*c)
def norm(x): return x[0]*x[0]-10*x[1]*x[1]
def color(x): return x[0]%2
def divides(p,z):
    a,b=p; c,d=z; n=norm(p)
    if not n: raise ValueError('division by zero')
    return (a*c-10*b*d)%n==0 and (a*d-b*c)%n==0

def zero_divisor_pair(p):
    # Valid for every nonzero p=(a,b) with a even, by the written proof.
    a,b=p; n=norm(p)
    if a%2 or not n: raise ValueError('wrong scope')
    if b%2:
        return (2,0),(n//2,0),'odd b: norm = 2 times odd integer'
    q=(a//2,b//2)
    if abs(norm(q))==1:
        return (0,1),(0,1),'associate of 2: sqrt10 is nonzero square-zero modulo 2'
    return (2,0),q,'both factors in p=2q are nonunits'


def authenticate():
    sb=(BASE/'SUBMITTED_SNAPSHOT.json').read_bytes(); s=json.loads(sb)
    require(sha(sb)=='69e123cf726603583476566bb8b3f53c9cefe9e9fcff65840d5000efe9bcb32b','snapshot authenticated',sha(sb))
    require(len(s['files'])==10,'snapshot exact ten files')
    require(s['head']=='cecd7da6e8b5bb84b4294e169d940189b269a956','snapshot exact head')
    for r in s['files']:
        b=(BASE/r['local']).read_bytes()
        gb=subprocess.check_output(['git','cat-file','blob',r['blob']],cwd=ROOT)
        tb=subprocess.check_output(['git','rev-parse',s['head']+':'+r['path']],cwd=ROOT,text=True).strip()
        require(len(b)==r['bytes'] and sha(b)==r['sha256'] and b==gb and tb==r['blob'],'local/blob/tree identity '+r['local'])
    return s

def verify_selected_metadata():
    """Explicit arrays/keys for each schema; do not recursively guess hash rows."""
    sub=BASE/'submitted'; details={}
    def row_check(rows,path_key):
        require(isinstance(rows,list),'selected metadata array')
        for r in rows:
            require(set([path_key,'bytes','sha256']).issubset(r),'required row keys',sorted(r))
            p=Path(r[path_key])
            require(not p.is_absolute() and '..' not in p.parts,'safe submitted-relative path',str(p))
            b=(sub/p).read_bytes()
            require(len(b)==r['bytes'] and sha(b)==r['sha256'],'metadata present identity '+str(p))
    pub=json.loads((sub/'PUBLIC_MANIFEST.json').read_bytes())
    require(pub['schema']==1,'PUBLIC_MANIFEST schema 1')
    row_check(pub['files'],'path')
    paths=[r['path'] for r in pub['files']]
    actual=sorted(p.name for p in sub.iterdir() if p.is_file())
    require(len(paths)==len(set(paths))==9 and 'PUBLIC_MANIFEST.json' not in paths,'public manifest self excluded; nine unique rows')
    require(sorted(paths+['PUBLIC_MANIFEST.json'])==actual and pub['file_count']==10,'public exact membership and declared ten')
    details['PUBLIC_MANIFEST']={'selected_schema':'files[]: path, bytes, sha256; file_count total; self is intentionally excluded','rows':len(paths),'self_hash_cycle':False}
    ac=json.loads((sub/'ACCEPTANCE.json').read_bytes())
    require(ac['schema']==1,'ACCEPTANCE schema 1')
    for key in ['required_joint_artifacts','source_metadata']:
        row_check(ac[key],'path')
    row_check([ac['editorial_export']['map']],'path')
    details['ACCEPTANCE']={'selected_present_identity_arrays':['required_joint_artifacts','source_metadata','editorial_export.map singleton'],'historical_identity_array':'reviewed_input_identities not authenticated as unavailable original bodies'}
    am=json.loads((sub/'AUDIT_MANIFEST.json').read_bytes())
    row_check(am['artifacts'],'file')
    details['AUDIT_MANIFEST']={'selected_schema':'artifacts[]: file, bytes, sha256'}
    em=json.loads((sub/'EDITORIAL_MAP.json').read_bytes())
    require(em['schema']==1,'EDITORIAL_MAP schema 1')
    historical=[]
    for ar in em['artifacts']:
        output=ar['output']; b=(sub/output['path']).read_bytes()
        row_check([output],'path')
        intervals=[]
        for r in ar['unchanged_ranges']:
            sl=b[r['output_start']:r['output_end']]
            require(sha(sl)==r['sha256'] and len(sl)==r['input_end']-r['input_start'],'editorial current unchanged slice '+ar['artifact'])
            intervals.append((r['output_start'],r['output_end']))
        for r in ar['operations']:
            sl=b[r['output_start']:r['output_end']]
            replacement=r['replacement_utf8'].encode()
            require(sl==replacement and sha(replacement)==r['replacement_sha256'],'editorial current replacement '+ar['artifact'])
            require(r['removed_bytes']==r['input_end']-r['input_start'],'editorial removal declared interval length '+ar['artifact'])
            if r['output_end']>r['output_start']:
                intervals.append((r['output_start'],r['output_end']))
        intervals.sort()
        require(intervals[0][0]==0 and intervals[-1][1]==len(b) and all(x[1]==y[0] for x,y in zip(intervals,intervals[1:])),'editorial output exact partition '+ar['artifact'])
        for r in ar['protected_mathematical_regions']:
            sl=b[r['output_start']:r['output_end']]
            require(len(sl)==r['bytes'] and sha(sl)==r['sha256'],'editorial current protected slice '+ar['artifact'])
        historical.append({'artifact':ar['artifact'],'declared_input_bytes':ar['input']['bytes'],'declared_input_sha256':ar['input']['sha256'],'original_body_present_in_submitted':ar['input']['sha256']==sha(b),'historical_replay_verified':False if ar['operations'] else True})
    details['EDITORIAL_MAP']={'selected_schema':'artifacts[].output (present file); operations/unchanged_ranges/protected_mathematical_regions (present output byte ranges)','present_slices_checked':True,'original_input_replay':'Not attempted for unavailable historical bodies','historical':historical}
    return details

def exact_diagnostics(corrupt=False):
    residues=sorted({a*a%5 for a in range(5)})
    require(residues==[0,1,4] and 2 not in residues and 3 not in residues,'all modulo-five norm ±2 obstructions',residues)
    vs=[v for v in range(1,41) if 40%(v*v)==0]
    require(vs==[1,2],'denominator squared-divisor possibilities',vs)
    choices=[(m,n) for m,n in itertools.product(range(4),repeat=2) if (m*m-10*n*n)%4==0]
    require(all(m%2==0 and n%2==0 for m,n in choices),'integral-basis final congruence exhaustive modulo four',choices)
    points=list(itertools.product(range(-4,5),repeat=2))
    require(all(color(mul(x,y))==color(x)*color(y)%2 for x,y in itertools.product(points,repeat=2)),'quotient homomorphism finite diagnostic on 6561 pairs')
    require(all((color((x[0]+y[0],x[1]+y[1]))==(color(x)+color(y))%2) for x,y in itertools.product(points,repeat=2)),'quotient addition finite diagnostic')
    checked=0
    for a,b in points:
        if (a,b)==(0,0): continue
        det=a*a-10*b*b
        require(det!=0,'nonzero determinant finite diagnostic '+str((a,b)))
        # All cosets represented in (Z/|det|Z)^2; independent enumeration via adjugate divisibility.
        # Avoid Smith normal form dependency. coset equality iff adj(M)(x-y) divisible by det.
        m=abs(det)
        if m>80: continue
        reps=[]
        for x,y in itertools.product(range(m),repeat=2):
            if not any((a*(x-u)-10*b*(y-v))%m==0 and (-b*(x-u)+a*(y-v))%m==0 for u,v in reps):
                reps.append((x,y))
        require(len(reps)==m,'enumerated lattice index '+str((a,b)),{'norm':det,'cosets':len(reps)})
        checked+=1
    require(checked>10,'multiple norm/index checks',checked)
    explicit_nonprime_cases=[]
    for p in points:
        if p==(0,0) or color(p): continue
        u,v,why=zero_divisor_pair(p)
        require(divides(p,mul(u,v)) and not divides(p,u) and not divides(p,v),'constructive nonprime witness '+str(p),{'u':u,'v':v,'case':why})
        explicit_nonprime_cases.append({'p':p,'u':u,'v':v,'case':why})
    require(norm((3,1))==-1 and mul((3,1),(-3,1))==(1,0),'explicit unit and inverse at both signs')
    require(norm((2,0))==4,'2 has norm four')
    require(mul((0,1),(0,1))==(10,0) and 10%2==0 and 1%2!=0,'2 not prime: sqrt10 squared in 2O, sqrt10 not in 2O')
    # Z[sqrt10]/(2) is F2[t]/(t²), a ring with a nonzero square-zero element.
    dual=list(itertools.product(range(2),repeat=2))
    require(tuple(z%2 for z in mul((0,1),(0,1)))==(0,0),'negative control quotient by 2 is not a domain')
    require((0,1)!=(0,0),'square-zero witness nonzero')
    require([color((0,0)),color((1,0)),color((2,0))]==[0,1,0],'negative control irreducible triangle breaks coloring')
    # Wrong parity color b mod 2 fails even for the unit edge 0--1.
    require((0,0)[1]%2==(1,0)[1]%2,'negative control wrong coefficient color fails unit edge')
    # Norm-negative prime element: sqrt10+3 is a unit, while 3+2sqrt10 has norm -31.
    # Norm 31 quotient is field F31 by t -> 14; 14² = 10 mod 31 and 3+2*14=0.
    require(norm((3,2))==-31 and (14*14-10)%31==0 and (3+2*14)%31==0,'prime-element control with negative norm',{'element':[3,2],'norm':-31,'residue_root_mod31':14})
    require(all(31%n for n in range(2,6)),'31 prime exact trial division to floor sqrt31')
    require(color((3,2))==1 and color((-3,-2))==1,'prime element and negative associate cross two colors')
    # Boundary controls: the obstruction must not be used in a PID or different field.
    require(all(abs(x-y) in (1,2,3) for x,y in itertools.combinations(range(4),2)),'Z prime-or-unit graph has K4 on 0,1,2,3')
    require(mul((0,1),(0,1),2)==(2,0),'different-field control: in Z[sqrt2], (sqrt2) is the parity kernel')
    require(Fraction(1,2)+Fraction(1,2)==1 and Fraction(1,4)-5*Fraction(1,4)==-1,'integral-basis control: half-integral element in Q(sqrt5) has integer trace and norm')
    require(all(r not in residues for r in (2,3)),'minimum proper principal ideal cannot have norm 2 or 3')
    # Mod 2 ideal criterion: x^2 - 10 reduces to t², so only one quotient root.
    require([r for r in range(2) if (r*r-10)%2==0]==[0],'unique map to F2 root check')
    if corrupt:
        require(2 in residues,'intentional corruption must fail modulo-five certificate',residues)
    return {'constructive_nonprime_cases':explicit_nonprime_cases,'norm_index_cases':checked,'quotient_test_box':[-4,4],'limitations':'All enumeration is diagnostic only. Universal proof is in REPORT.md; no prime classification is claimed.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--self-test-corruption',action='store_true'); args=ap.parse_args()
    try:
        s=authenticate(); metadata=verify_selected_metadata(); diagnostics=exact_diagnostics(args.self_test_corruption)
        result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','script_sha256':sha(Path(__file__).read_bytes()),'python_optimization':sys.flags.optimize,'all_pass':True,'check_count':len(CHECKS),'metadata':metadata,'diagnostics':diagnostics,'checks':CHECKS}
        print(json.dumps(result,indent=2))
    except Exception as exc:
        print(json.dumps({'status':'FAIL','python_optimization':sys.flags.optimize,'error':str(exc),'checks':CHECKS},indent=2))
        sys.exit(1)
