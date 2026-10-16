from pathlib import Path
import importlib.util,json,os,shutil,subprocess,sys,tempfile
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent/'preprint/verification'
manifest=HERE/'CANDIDATE_MANIFEST.json'
rows=[]
def record(name,ok,details):
    if not ok:raise AssertionError(name+': '+str(details))
    rows.append({'check':name,'pass':True,'details':details})
def execute(args,env=None):
    e=dict(os.environ);e['PYTHONDONTWRITEBYTECODE']='1';e.update(env or {})
    return subprocess.run([sys.executable,'-B']+args,cwd=HERE,env=e,capture_output=True,text=True)
r=execute(['-O',str(BASE/'run_verification.py'),'--manifest',str(manifest),'--integrity-only'])
record('optimized execution refused',r.returncode!=0 and 'Refusing -O/-OO' in r.stderr,{'exit_code':r.returncode})
with tempfile.TemporaryDirectory(prefix='wrong-lib-',dir=HERE) as root:
    d=Path(root);(d/'sympy.py').write_text("__version__='0.0.0'\n")
    r=execute([str(BASE/'run_verification.py'),'--manifest',str(manifest),'--run','root_projective'],{'PYTHONPATH':str(d)})
    record('wrong scientific library refused',r.returncode!=0 and 'Requires exactly SymPy 1.14.0 and mpmath 1.3.0' in r.stderr,{'exit_code':r.returncode,'fake_sympy_version':'0.0.0'})
with tempfile.TemporaryDirectory(prefix='integrity-negative-',dir=HERE) as root:
    d=Path(root)/'verification';shutil.copytree(BASE,d);shutil.copyfile(manifest,d/'MANIFEST.json')
    target=d/'scope_controls/root_priority_projective_control.py';target.write_bytes(target.read_bytes()+b'\n# simulated tamper\n')
    r=execute([str(d/'run_verification.py'),'--integrity-only'])
    record('modified scientific script refused',r.returncode!=0 and 'Integrity/inventory mismatch' in r.stderr and 'scope_controls/root_priority_projective_control.py' in r.stderr,{'exit_code':r.returncode})
    shutil.copyfile(BASE/'scope_controls/root_priority_projective_control.py',target)
    (d/'unexpected.json').write_text('{}\n')
    r=execute([str(d/'run_verification.py'),'--integrity-only'])
    record('unexpected payload refused',r.returncode!=0 and 'unexpected.json' in r.stderr,{'exit_code':r.returncode})
    (d/'unexpected.json').unlink();(d/'scope_controls/forbidden_link').symlink_to(target)
    r=execute([str(d/'run_verification.py'),'--integrity-only'])
    record('symlink payload refused',r.returncode!=0 and 'Forbidden payload/symlink' in r.stderr,{'exit_code':r.returncode})
sys.path.insert(0,str(BASE))
from run_verification import differences,normalize
record('scientific scalar mismatch retained',bool(differences({'value':'1e-80'},{'value':'2e-80'})),{'mismatch_path':'$.value','no_tolerance_in_comparison':True})
a={'python':'one','x':{'python':'scientific nested value'}};b={'python':'two','x':{'python':'changed'}}
record('metadata exclusion is top-level only',differences(normalize(a,'source_domain'),normalize(b,'source_domain'))==['$.x.python'],{'mismatch_path':'$.x.python'})
record('boolean/integer type mismatch retained',bool(differences({'value':True},{'value':1})),{'mismatch_path':'$.value (type)'})
record('ordered row mismatch retained',bool(differences([1,2],[2,1])),{'ordering_is_scientific':True})
out={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Adversarial harness safeguards, not whole-manuscript review','checks':rows,'all_pass':True}
(HERE/'HARNESS_SAFEGUARD_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(rows),'all_pass':True},indent=2))
