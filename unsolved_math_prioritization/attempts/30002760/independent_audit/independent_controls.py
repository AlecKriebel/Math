#!/usr/bin/env python3
"""Independent exact controls and fresh negative tests. Standard library only.
No imports from the reviewed implementation. Finite tests are not formal proofs.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import ast, copy, hashlib, itertools, json, math, subprocess, sys, tempfile

PIN='6881ffec2ec0cdf4c44f9aa0a1b5155efe171d31e4b801f21961afaa9166a260'
EXPECTED={'ATTEMPT_LEDGER.json','CHECK_RESULTS.json','CLAIMS.json','FAIL_CLOSED_RESULTS.json','INTEGRITY_RESULTS.json','PRIOR_ATTEMPT_GATE.md','README.md','SOURCE_METADATA.json','SOURCE_SCOPE.md',*[f'TURN_{i}.md' for i in range(1,6)],'test_fail_closed.py','test_integrity.py','verify_math.py','verify_packet.py'}
counts=Counter()
def check(value,group,label):
    if not value: raise ValueError(group+': '+label)
    counts[group]+=1

def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError('Duplicate key '+k)
        out[k]=v
    return out

def integ_product(a,b):
    return sum((x*y/Q(i+j+1) for i,x in a.items() for j,y in b.items()),Q(0))
def d(a): return {i-1:i*x for i,x in a.items() if i}
def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,c): return tuple(x*c for x in a)
def run(path,mode,*args):
    return subprocess.run([sys.executable,*mode,str(path),*map(str,args)],capture_output=True,text=True)

def main(packet):
    check(hashlib.sha256((packet/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()==PIN,'binding','external manifest pin')
    m=json.loads((packet/'FROZEN_MANIFEST.json').read_text(),object_pairs_hook=unique)
    check(set(m['files'])==EXPECTED,'binding','independent explicit allowlist')
    check({p.name for p in packet.iterdir()}==EXPECTED|{'FROZEN_MANIFEST.json'},'binding','directory allowlist')
    for name,b in m['files'].items():
        raw=(packet/name).read_bytes()
        check(len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'],'binding',name)
    for p in packet.glob('*.py'):
        check(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'binding','no optimizable assertions '+p.name)
    # Independent sparse-polynomial integration and scalar FEM solves.
    phi={1:Q(1),2:Q(-1)};psi={1:Q(-1,2),2:Q(3,2),3:Q(-1)}
    P=integ_product(d(phi),d(phi));S=integ_product(d(psi),d(psi));cross=integ_product(d(psi),d(phi));conv=integ_product(d(psi),phi)
    check((P,S,cross,conv)==(Q(1,3),Q(1,20),0,Q(1,60)),'galerkin','independent four integrals')
    for eps in {Q(i,j) for i in range(1,12) for j in range(1,20)}:
        c=conv/(eps*P)
        check(eps*(S+c*c*P)/(eps*S)==1+Q(1,60)/(eps*eps),'galerkin','all rational epsilon ratios')
    # Stable oblique projections with an exact zero restricted residual.
    vectors=[tuple(map(Q,v)) for v in itertools.product(range(-2,3),repeat=2) if v!=(0,0)]
    for v in vectors:
      for z in vectors:
        vz=dot(v,z)
        if not vz: continue
        beta2=vz*vz/(dot(v,v)*dot(z,z))
        for u in vectors[::3]:
            ut=mul(v,dot(u,z)/vz);e=sub(u,ut)
            best2=dot(u,u)-dot(u,v)**2/dot(v,v)
            check(dot(e,z)==0 and beta2>0,'finite_tests','stationarity and positive stability')
            check(beta2*dot(e,e)==best2,'finite_tests','sharp oblique-projection identity')
    # Generate dyadic leaf addresses directly by splitting one leaf, not Catalan recursion.
    level={('',)}
    for n in range(8):
        catalan=math.comb(2*n,n)//(n+1)
        check(len(level)==catalan,'trees','leaf-address enumeration')
        check(n==0 or len(level)>=2**(n-1),'trees','exponential count')
        level={tuple(sorted(part[:i]+part[i+1:]+(leaf+'0',leaf+'1'))) for part in level for i,leaf in enumerate(part)}
    for k in range(30):
      for s in range(1,5):
        size=2**(k+1)-1
        check(Q(1,(2**k+1)**s)<=Q(2**s,(size+1)**s),'overlay','rate constant orientation')
    # Reduction-to-marking inequality, without square roots.
    for a,r,kappa in itertools.product([Q(i,5) for i in range(11)],[Q(i,20) for i in range(1,20)],[Q(i,20) for i in range(1,20)]):
        endpoint=(kappa+a*r)**2+r*r
        if endpoint<1:
            check(r*r<Q(1)/(1+a*a),'marking','threshold necessity')
            for rr in (Q(0),r/3,2*r/3,r):
                check((kappa+a*rr)**2+rr*rr<=endpoint,'marking','monotonic contradiction')
    for q in (Q(1,4),Q(1,2),Q(3,4),Q(9,10)):
      for l in range(1,30):
        check(sum((q**j for j in range(1,l+1)),Q(0))<1/(1-q),'marking','geometric complexity')
    # Allocation optimum and integer conversion, alternative cases to reviewed controls.
    for p in (1,2,4):
      for qs in itertools.product((1,2,4),repeat=2):
        B=sum(qs);bs=[q**(p+1) for q in qs]
        for L in range(4,19):
            optimum=[Q((L-2)*q,B) for q in qs]
            rounded=[math.ceil(n) for n in optimum]
            obj=sum((Q(b)/n**p for b,n in zip(bs,optimum)),Q(0))
            check(obj==Q(B**(p+1),(L-2)**p),'allocation','exact Holder equality')
            check(sum(rounded)<=L and min(rounded)>0,'allocation','rounded budget')
            check(sum((Q(b,n**p) for b,n in zip(bs,rounded)),Q(0))<=Q(2**p*B**(p+1),L**p),'allocation','rounding factor')
            for n in range(1,L):
                check(Q(bs[0],n**p)+Q(bs[1],(L-n)**p)>=Q(B**(p+1),L**p),'allocation','global integer lower bound')
    # Polynomial energy residual tests with skew convection in a two-dimensional Hilbert space.
    def plus(a,b):
        return {i:a.get(i,Q(0))+b.get(i,Q(0)) for i in set(a)|set(b)}
    def scale(a,c): return {i:c*x for i,x in a.items()}
    def at(a,t): return sum((x*t**i for i,x in a.items()),Q(0))
    def int_square(a,t):
        return sum((x*y*t**(i+j+1)/Q(i+j+1) for i,x in a.items() for j,y in a.items()),Q(0))
    for i,j,c in itertools.product(range(-2,3),range(-2,3),(-3,0,4)):
        e1={0:Q(i),1:Q(j),2:Q(1)};e2={0:Q(j),1:Q(-i),2:Q(-2)}
        r1=plus(d(e1),plus(e1,scale(e2,-c)))
        r2=plus(d(e2),plus(e2,scale(e1,c)))
        for t in [Q(k,10) for k in range(11)]:
            lhs=at(e1,t)**2+at(e2,t)**2+int_square(e1,t)+int_square(e2,t)
            rhs=i*i+j*j+int_square(r1,t)+int_square(r2,t)
            check(lhs<=rhs,'energy','polynomial nonsymmetric residual inequality')
    # Nonsymmetric coercive 2x2 operator A=I+cJ: exact Euler error remains nonzero.
    for c in range(-10,11):
      for phi2 in vectors:
        denom=Q(4+c*c)
        w=((2*phi2[0]+c*phi2[1])/denom,(-c*phi2[0]+2*phi2[1])/denom)
        check((2*w[0]-c*w[1],c*w[0]+2*w[1])==phi2 and dot(w,w)>0,'time_error','coercive nonsymmetric exact error')
    # Fresh mutations: every numerical claim leaf, types/schema, and additional computation edits.
    base=json.loads((packet/'CLAIMS.json').read_text());mutations=[]
    for section,claims in base.items():
        if not isinstance(claims,dict): continue
        for key,val in claims.items():
            obj=copy.deepcopy(base);obj[section][key]=str(Q(val)+1) if isinstance(val,str) else val+1
            mutations.append((section+'.'+key,json.dumps(obj)))
    malformed=[('root_list','[]'),('null_root','null'),('boolean_id',json.dumps({**base,'problem_id':True})),('float_id',json.dumps({**base,'problem_id':30002760.0})),('solved',json.dumps({**base,'status':'solved'})),('missing_turn',json.dumps({k:v for k,v in base.items() if k!='turn_1'})),('unknown_root',json.dumps({**base,'extra':0}))]
    for val in (None,True,0,1.0,[],{},'NaN','1/0'):
        obj=copy.deepcopy(base);obj['turn_1']['convection_cross']=val
        malformed.append(('invalid_rational_'+repr(val),json.dumps(obj)))
    duplicate=json.dumps(base).replace('"convection_cross": "1/60"','"convection_cross": "0", "convection_cross": "1/60"')
    malformed.append(('nested_duplicate',duplicate))
    source=(packet/'verify_math.py').read_text()
    edits=[('def derivative(p):\n    return [i * p[i]','def derivative(p):\n    return [-i * p[i]'),('D=1+eps**2','D=2+eps**2'),('catalan=[1]','catalan=[2]'),('splits=sum(2**j for j in range(k+1))','splits=sum(2**j for j in range(k+1))+1')]
    with tempfile.TemporaryDirectory(prefix='independent_transport_audit_') as tmp:
      tmp=Path(tmp)
      for mode in ([],['-O'],['-OO']):
        result=run(packet/'verify_math.py',mode)
        check(result.returncode==0 and result.stdout==(packet/'CHECK_RESULTS.json').read_text(),'replay','math mode '+str(mode))
        for label,raw in mutations+malformed:
            path=tmp/'bad.json';path.write_text(raw)
            result=run(packet/'verify_math.py',mode,'--claims',path)
            check(result.returncode!=0,'fresh_rejections',label+' '+str(mode))
        for i,(old,new) in enumerate(edits):
            check(source.count(old)==1,'mutation_anchors',old)
            path=tmp/('bad'+str(i)+'.py');path.write_text(source.replace(old,new))
            result=run(path,mode,'--claims',packet/'CLAIMS.json')
            check(result.returncode!=0 and 'FAILED:' in result.stderr,'fresh_code_rejections',str(i)+' '+str(mode))
    check(hashlib.sha256((packet/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()==PIN,'binding','manifest unchanged')
    print(json.dumps({'status':'PASS_INDEPENDENT_CONTROLS','original_manifest_sha256':PIN,'bound_original_files':len(EXPECTED),'counts':dict(sorted(counts.items())),'total_checks':sum(counts.values()),'numeric_claim_mutation_cases_per_mode':len(mutations),'malformed_cases_per_mode':len(malformed),'new_code_mutation_cases_per_mode':len(edits),'scope':'Finite exact controls and fresh mutation rejections; analytic proofs audited separately; no formal verification or complete literature claim.'},indent=2,sort_keys=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True)
    args=parser.parse_args()
    try: main(args.packet.resolve())
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
