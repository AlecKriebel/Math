"""Capture actual process receipts and require both normal/-O behavior."""
import datetime, hashlib, json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parent
PYTHON='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
ENV={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
MUTANTS=('omit_third_pair_swap','paired_equals_blocked','third_internal_plus_sign','ambient_c1',
         'strict_constraints','drop_generator_rows','redundant_fourth_generator','nonnegative_is_positive')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(condition,message):
    if not condition: raise RuntimeError(message)
def pin(path):
    b=path.read_bytes(); return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
all_receipts=[]; baseline=[]
for optimized in (False,True):
    mode='optimized' if optimized else 'normal'
    for mutant in (None,)+MUTANTS:
        argv=[PYTHON,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(ROOT/'verify_bridge.py')]
        if mutant: argv+=['--mutant',mutant]
        start=utc(); p=subprocess.run(argv,cwd=ROOT,env=ENV,capture_output=True,check=False); stop=utc()
        label=f'{mode}_{mutant or "baseline"}'
        stdout=ROOT/f'{label}.stdout.json'; stderr=ROOT/f'{label}.stderr.json'
        stdout.write_bytes(p.stdout); stderr.write_bytes(p.stderr)
        receipt={'label':label,'argv':argv,'cwd':str(ROOT),'environment':ENV,'started_at':start,
                 'finished_at':stop,'exit_code':p.returncode,'expected_exit_code':2 if mutant else 0,
                 'stdout':pin(stdout),'stderr':pin(stderr)}
        all_receipts.append(receipt)
        (ROOT/'CHECK_PROCESS_RECEIPTS.json').write_text(json.dumps({'processes':all_receipts},indent=2)+'\n')
        require(p.returncode==(2 if mutant else 0),f'{label} exited {p.returncode}; diagnostic preserved')
        if mutant:
            output=json.loads(p.stderr)
            require(output['status']=='rejected',f'{label} lacks rejection diagnostic')
        else:
            baseline.append(json.loads(p.stdout))
        print(json.dumps({'label':label,'exit_code':p.returncode,'expected_exit_code':receipt['expected_exit_code']}),flush=True)
for result in baseline: result.pop('debug_enabled')
require(baseline[0]==baseline[1],'normal and optimized validation results differ')
require(baseline[0]['status']=='pass','baseline did not pass')
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps({'verified_at':utc(),'normal_and_optimized_identical':True,
    'baseline':baseline[0],'expected_failure_processes':16,'unexpected_failure_processes':0},indent=2)+'\n')
inputs=[ROOT.parent/'root_priority_audit_20261006'/'ROOT_PROPOSED_DISPOSITION.md',
        ROOT.parent/'root_priority_audit_20261006'/'PROPOSED_CLOSURE_COMMENT.md']
(ROOT/'DISPOSITION_INPUTS.json').write_text(json.dumps({'read_after_checkpoint':True,'captured_at':utc(),
    'inputs':[pin(p) for p in inputs]},indent=2)+'\n')
