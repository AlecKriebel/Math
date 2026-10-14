"""Fresh reviewer-owned execution harness; candidate bytes remain read-only."""
from pathlib import Path
from zipfile import ZipFile
import datetime, hashlib, json, subprocess, sys, time

R=Path(__file__).resolve().parent
A=R.parent
STD='/opt/homebrew/opt/python@3.14/bin/python3.14'
SYM=str(A/'gv_algebra_reproduction_adversary/private/control_env/bin/python')
P=R/'private/extracted_controls'
P.mkdir(parents=True,exist_ok=True)
(R/'receipts').mkdir(exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.datetime.now(datetime.UTC).isoformat()
def run(label,path,symbolic=False,optimized=False,expected_error=None):
    argv=[SYM if symbolic else STD,'-E']+([] if symbolic else ['-S'])+['-B','-P']+(['-O'] if optimized else [])+[str(path)]
    started=utc(); t=time.monotonic()
    p=subprocess.run(argv,cwd=P,capture_output=True,timeout=180)
    out=R/'receipts'/f'{label}.stdout.txt';err=R/'receipts'/f'{label}.stderr.txt'
    out.write_bytes(p.stdout);err.write_bytes(p.stderr)
    rec={'label':label,'started_utc':started,'finished_utc':utc(),'argv':argv,'script_sha256':sha(path.read_bytes()),'returncode':p.returncode,'seconds':time.monotonic()-t,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'expected_error':expected_error}
    if expected_error:
        rec['accepted']=p.returncode==1 and expected_error.encode() in p.stderr and b'RuntimeError' in p.stderr and b'SyntaxError' not in p.stderr and b'ModuleNotFoundError' not in p.stderr
    else:
        rec['accepted']=p.returncode==0
        if p.returncode==0:rec['output']=json.loads(p.stdout)
    print(label,p.returncode,rec['accepted'],flush=True)
    return rec

with ZipFile(A/'publication_package_v2/verification-package.zip') as z:
    for name in ['verify_forms.py','independent_symbolic_checks.py','independent_integrable_controls.py','finite_sampling_counterexample.py']:
        (P/name).write_bytes(z.read('controls/'+name))
if (R/'FRESH_EXECUTION.json').exists():
    baseline=json.loads((R/'FRESH_EXECUTION.json').read_text())['runs']
    for rec in baseline:
        if rec['script_sha256']!=sha(Path(rec['argv'][-1]).read_bytes()):
            raise RuntimeError('Baseline binding changed')
else:
    baseline=[]
    for p in sorted(P.glob('*.py')):
        for opt in [False,True]:
            baseline.append(run(p.stem+('_optimized' if opt else '_ordinary'),p,'symbolic' in p.name,opt))
    (R/'FRESH_EXECUTION.json').write_text(json.dumps({'created_utc':utc(),'environment_independent':False,'source':'exact reviewed ZIP, extracted only four controls into own private directory','runs':baseline},indent=2)+'\n')

mutations=[
 ('poly_false','verify_forms.py','    if not b:\n','    if True:\n','Exact differential-form control'),
 ('poly_GV_sign','verify_forms.py','density=add(mul(qz,der(pz,2)),scale(mul(pz,der(qz,2)),-1))','density=scale(add(mul(qz,der(pz,2)),scale(mul(pz,der(qz,2)),-1)),-1)','Exact differential-form control'),
 ('poly_Jacobian','verify_forms.py','scale(subz(density,a,l),1/l)','scale(subz(density,a,l),1)','Exact differential-form control'),
 ('sym_false','independent_symbolic_checks.py','    if not value:\n','    if True:\n','Exact symbolic control failed: universal_Frobenius_coefficient'),
 ('sym_GV_sign','independent_symbolic_checks.py','G=s.diff(q,z)*s.diff(p,z,2)-s.diff(p,z)*s.diff(q,z,2)','G=-(s.diff(q,z)*s.diff(p,z,2)-s.diff(p,z)*s.diff(q,z,2))','Exact symbolic control failed: universal_GV_coefficient'),
 ('sym_Jacobian','independent_symbolic_checks.py','g.subs(sub)/length','g.subs(sub)','Exact symbolic control failed: compression_GV_density'),
 ('jet_false','independent_integrable_controls.py',' if not b:raise RuntimeError(label)',' if True:raise RuntimeError(label)','actual integrable alpha: Frobenius'),
 ('jet_GV_sign','independent_integrable_controls.py','value(dot(e,curl(e)))==rho','value(dot(e,curl(e)))==-rho','independently derived rational GV density'),
 ('jet_Jacobian','independent_integrable_controls.py','value(dot(ee,curl(ee)))==rho/ell','value(dot(ee,curl(ee)))==rho','density scales by reciprocal positive length'),
 ('sampling_wrong_value','finite_sampling_counterexample.py','negative!=Q(-62,63)','negative!=Q(-61,63)','negative unsampled value changed'),
 ('sampling_false_grid','finite_sampling_counterexample.py','if min(values)<=0:','if True:','grid no longer strictly positive'),
]
M=R/'private/mutations';M.mkdir(exist_ok=True)
negative=[]
for label,source,old,new,error in mutations:
    s=(P/source).read_text()
    if old not in s:raise RuntimeError('Mutation anchor missing: '+label)
    dest=M/(label+'.py');dest.write_text(s.replace(old,new))
    compile(dest.read_text(),str(dest),'exec')
    for opt in [False,True]:
        negative.append(run(label+('_optimized' if opt else '_ordinary'),dest,'sym_' in label,opt,error))
        (R/'NEGATIVE_ENFORCEMENT.json').write_text(json.dumps({'created_utc':utc(),'mutation_count':len(mutations),'executions':len(negative),'all_intended_failures':all(r['accepted'] for r in negative),'runs':negative},indent=2)+'\n')
(R/'NEGATIVE_ENFORCEMENT.json').write_text(json.dumps({'created_utc':utc(),'mutation_count':len(mutations),'executions':len(negative),'all_intended_failures':all(r['accepted'] for r in negative),'runs':negative},indent=2)+'\n')
if not all(r['accepted'] for r in baseline+negative):raise RuntimeError('Execution acceptance failed')
