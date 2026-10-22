from pathlib import Path
from datetime import datetime, timezone
import subprocess, sys, json, hashlib, runpy
BASE=Path(__file__).resolve().parent
PACKAGE=BASE.parent/'publication_package_v1'
VERIFIER=PACKAGE/'verification/portable_exact_verifier.py'
HARNESS=PACKAGE/'verification/run_negative_controls.py'
PINS={VERIFIER:'dfa1ff339e1f3a6004563aec9c01f6f14d6bb65a94e2437f3ba3a41e5b393d85',HARNESS:'bbf357e622d2f55d396eceeb1973628d53cb80b730fddf225e90f195ac0e4169'}
for path,pin in PINS.items():
    if hashlib.sha256(path.read_bytes()).hexdigest()!=pin: raise RuntimeError('pin mismatch')
RUNS=[]
def call(label, argv):
    start=datetime.now(timezone.utc).isoformat()
    r=subprocess.run(argv,cwd=BASE,capture_output=True,timeout=60)
    (BASE/(label+'.stdout')).write_bytes(r.stdout)
    (BASE/(label+'.stderr')).write_bytes(r.stderr)
    item={'label':label,'start_utc':start,'argv':argv,'cwd':str(BASE),'exit':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
    RUNS.append(item)
    (BASE/'EXECUTION_BINDINGS.json').write_text(json.dumps({'runtime':sys.version,'executable':sys.executable,'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_pins':{str(k):v for k,v in PINS.items()},'runs':RUNS},indent=2)+'\n')
    return r
flags=['-E','-S','-B','-P']
for mode,extra in [('normal',[]),('optimized',['-O'])]:
    r=call(mode,[sys.executable]+flags+extra+[str(VERIFIER),'--receipt',str(BASE/(mode+'.receipt.json'))])
    if r.returncode!=0 or r.stderr:raise RuntimeError(mode+' failed')
    if r.stdout!=(BASE/(mode+'.receipt.json')).read_bytes():raise RuntimeError('receipt mismatch')
    if r.stdout!=(PACKAGE/('verification/results_'+mode+'.json')).read_bytes():raise RuntimeError('published stdout mismatch')
r=call('negative',[sys.executable]+flags+[str(HARNESS)])
if r.returncode!=0 or r.stderr:raise RuntimeError('negative harness failed')
if r.stdout!=(PACKAGE/'verification/negative_control_results.json').read_bytes():raise RuntimeError('negative published stdout mismatch')
# No overwrite probes target only new own paths.
(BASE/'sentinel.txt').write_text('sentinel survives\n')
(BASE/'receipt_directory').mkdir()
(BASE/'receipt_symlink').symlink_to(BASE/'sentinel.txt')
(BASE/'receipt_dangling_symlink').symlink_to(BASE/'absent_target')
for name in ['sentinel.txt','receipt_directory','receipt_symlink','receipt_dangling_symlink']:
    r=call('collision_'+name.replace('.','_'),[sys.executable]+flags+[str(VERIFIER),'--receipt',str(BASE/name)])
    if r.returncode!=1 or json.loads(r.stdout)['status']!='FAIL' or r.stderr:raise RuntimeError('collision did not reject')
if (BASE/'sentinel.txt').read_text()!='sentinel survives\n' or (BASE/'absent_target').exists():raise RuntimeError('collision corrupted target')
for label,args in [('unknown_cli',['--bogus']),('missing_cli',['--receipt']),('duplicate_cli',['--fault','wrong-area','--fault','wrong-product']),('empty_cli',['--receipt',''])]:
    r=call(label,[sys.executable]+flags+[str(VERIFIER)]+args)
    if r.returncode!=1 or json.loads(r.stdout)['status']!='FAIL' or r.stderr:raise RuntimeError('malformed CLI did not reject')
# Read-only import of already inspected/authenticated source; no main or cache execution.
v=runpy.run_path(str(VERIFIER)); tests=[]
def reject(label,func):
    try:func()
    except Exception as e:tests.append({'label':label,'result':'rejected','exception':type(e).__name__,'message':str(e)})
    else:raise RuntimeError('accepted '+label)
from fractions import Fraction
class IntSubclass(int):pass
class FractionSubclass(Fraction):pass
for x in [True,False,1.0,float('nan'),float('inf'),IntSubclass(1),FractionSubclass(1)]:
    reject('exact_'+repr(x)+'_'+type(x).__name__,lambda x=x:v['exact'](x))
for x in [True,False,0,-1,Fraction(3),3.0]:reject('repetition_'+repr(x),lambda x=x:v['positive_integer'](x))
for x in [[],[(0,0)],[(0,0),(1,0),(0,0)],[(0,0),(1,0),(1,)],iter([(0,0),(1,0),(0,1)])]:reject('polygon_'+type(x).__name__,lambda x=x:v['polygon'](x))
reject('zero_denominator',lambda:v['exact'](0).inverse())
reject('bad_sqrt_7',lambda:v['sqrt_rational'](7))
reject('empty_ledger',lambda:v['Ledger']().finish())
reject('guard_integer',lambda:v['require'](1,'bad'))
reject('guard_false',lambda:v['require'](False,'bad'))
for r in [1,2,3,7,11]:
    pts=[(0,0),(2,0),(0,2)]
    if v['signed_area'](pts,r)!=2*r:raise RuntimeError('repeat law mismatch')
(BASE/'ADDED_API_REJECTIONS.json').write_text(json.dumps({'cases':tests,'rejection_count':len(tests),'additional_integer_repetitions':[1,2,3,7,11],'status':'PASS'},indent=2)+'\n')
print(json.dumps({'status':'PASS','runs':len(RUNS),'published_receipts_byte_reproduced':3,'api_rejections':len(tests),'source_pins':{str(k):v for k,v in PINS.items()}},indent=2))
