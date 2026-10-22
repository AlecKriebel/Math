#!/usr/bin/env python3
"""Fresh fault controls; uses exceptions so controls remain active under -O."""
from pathlib import Path
import ast, json, hashlib, tempfile, shutil, subprocess, datetime, stat
from fractions import Fraction
D=Path(__file__).resolve().parent;C=D/'frozen/candidate'
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
rows=[]
def package_case(name,mutate,target='verify_package.py',expect_success=False):
    with tempfile.TemporaryDirectory(prefix='fault_',dir=D) as tmp:
        P=Path(tmp);allow=json.loads((C/'ALLOWLIST.json').read_text())['members']
        for f in allow+['MANIFEST.json']:
            p=P/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(C/f,p)
        mutate(P)
        p=subprocess.run(['python3','-I','-B','-O',str(P/'scripts'/target)],capture_output=True)
        require((p.returncode==0)==expect_success,name+' wrong fault result')
        rows.append({'name':name,'target':target,'optimized_python':True,'expected_success':expect_success,'exit':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()[-1500:]})
def update_manifest(P,name):
    m=json.loads((P/'MANIFEST.json').read_text());b=(P/name).read_bytes()
    for row in m['entries']:
        if row['path']==name:row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    (P/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
def change_json(P,name,fun,rehash=True):
    p=P/name;x=json.loads(p.read_text());fun(x);p.write_text(json.dumps(x,indent=2)+'\n')
    if rehash:update_manifest(P,name)
package_case('tamper mathematics source',lambda P:(P/'paper/matroid_rank_obstruction.tex').write_text('tampered'))
package_case('remove one of nine originals',lambda P:(P/'evidence/submitted/REPORT.md').unlink())
package_case('metadata mismatch after updating ordinary manifest hash',lambda P:change_json(P,'.zenodo.json',lambda x:x.update(title='Fault title')))
package_case('false publication-ready state after updating ordinary manifest hash',lambda P:change_json(P,'CURRENT_REVIEW_STATE.json',lambda x:x.update(publication_ready=True)))
package_case('weaken adaptation identity after manifest rehash',lambda P:change_json(P,'CHECKER_ADAPTATION.json',lambda x:x.update(after=x['before'])))
package_case('incorrect evidence-copy hash after manifest rehash',lambda P:change_json(P,'EVIDENCE_COPY_MAP.json',lambda x:x['copies'][0].update(sha256='0'*64)))
def traversal(P):
    change_json(P,'ALLOWLIST.json',lambda x:x['members'].append('../outside'),False)
package_case('builder traversal path rejected',traversal,'build_supportkit.py')
package_case('builder duplicate allowlist rejected',lambda P:change_json(P,'ALLOWLIST.json',lambda x:x['members'].append(x['members'][0]),False),'build_supportkit.py')
def symlink(P):
    p=P/'README.md';p.unlink();p.symlink_to('SUPPLEMENT.md')
package_case('builder symlink file rejected',symlink,'build_supportkit.py')
def nonregular(P):
    p=P/'README.md';p.unlink();p.mkdir()
package_case('builder directory-as-member rejected',nonregular,'build_supportkit.py')
package_case('extra local reproduction output intentionally accepted',lambda P:(P/'EXTRA_LOCAL_REPRODUCTION.txt').write_text('excluded by explicit allowlist'),expect_success=True)

# Execute the actual extracted checker function bodies on independently chosen faults.
tree=ast.parse((C/'scripts/check_mathematics.py').read_text())
names={'require','card','exact_basis_exchange','rank_from_bases','validate_rank_axioms','sqrt_factor_squared','rational_values','rational_factor'}
module=ast.Module(body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names],type_ignores=[])
ns={'Fraction':Fraction};exec(compile(module,'actual-checker-functions','exec'),ns)
require(not ns['exact_basis_exchange']((0b0011,0b1100)),'basis exchange accepted disjoint incompatible bases')
require(ns['exact_basis_exchange']((0b101,0b110)),'valid nonuniform bases rejected')
good=ns['rank_from_bases'](3,(0b101,0b110));ns['validate_rank_axioms'](3,good)
for name,bad in [('empty rank corruption',(1,)+good[1:]),('upper rank bound corruption',good[:1]+(2,)+good[2:]),('monotonicity corruption',(0,1,1,0,1,2,2,2)),('submodularity corruption',(0,1,1,1,1,1,1,2))]:
    try:ns['validate_rank_axioms'](3,bad)
    except RuntimeError as e:rows.append({'name':name,'actual_checker_function':'validate_rank_axioms','detected':True,'error':str(e)})
    else:raise RuntimeError('fault accepted '+name)
require(ns['sqrt_factor_squared'](3,(0,)*8) is None,'loops not rejected')
require(ns['rational_factor'](3,(0,)*8,ns['rational_values'](3,2)) is None,'rational loops not rejected')
rows.append({'name':'actual checker basis-exchange and loop controls','invalid_basis_family_rejected':True,'valid_nonuniform_basis_family_accepted':True,'both_loop_factors_return_none':True,'explicit_exceptions_survive_O':True})

# Additional arithmetic checks, independently authored rather than copied algebra.
cases=0
for m in range(1,51):
    n=m*m
    for k in range(n+1):
        g=Fraction(0) if not k else Fraction(m+k-1,m)
        rank=(m-1)*min(k,1)+k
        require(Fraction(rank,m)==g,'copied-element rank formula')
        cases+=1
for n in range(1,61):
    d=[Fraction(n+1-i,n+1) for i in range(1,n+1)]
    c=[d[i]-d[i+1] if i<n-1 else d[i] for i in range(n)]
    for k in range(n+1):require(sum(c[i]*min(k,i+1) for i in range(n))==sum(d[:k]),'finite difference decomposition')
rows.append({'name':'fresh copy-domain and coefficient arithmetic','rational_m_range':'1..50','copy_block_size_cases':cases,'concave_decomposition_n_range':'1..60','status':'PASS'})
(D/'FAULT_CONTROLS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'explicit_exceptions_used':True,'controls':rows,'status':'PASS'},indent=2)+'\n')
print(json.dumps({'status':'PASS','controls':len(rows),'python_optimization_active':not __debug__}))
