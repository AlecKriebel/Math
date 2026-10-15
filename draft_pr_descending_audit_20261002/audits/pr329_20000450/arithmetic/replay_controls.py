#!/usr/bin/env python3
"""Read-only six-stream replay with complete actual native child metadata."""
from datetime import datetime,timezone
import hashlib,json,os
from pathlib import Path
import stat,subprocess,sys

base=Path(__file__).resolve().parent
ENV={'PATH':'/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
     'LANG':'C','LC_ALL':'C','TZ':'UTC','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'}
def utc():return datetime.now(timezone.utc).isoformat()
def verify_pin(v):
    p=Path(v['path']); data=p.read_bytes()
    assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256'],str(p)
    assert stat.S_IMODE(p.stat().st_mode)==v['mode'],str(p)+' mode'
def check_bindings():
    external=json.loads((base/'EXTERNAL_BINDINGS.json').read_text())
    runtime=json.loads((base/'RUNTIME_BINDINGS.json').read_text())
    for v in external['files']+runtime['files']+runtime['tools']:verify_pin(v)
    actual=set()
    for root in runtime['runtime_roots']:
        actual.update(str(p.resolve()) for p in Path(root).rglob('*') if p.is_file() and
                      '__pycache__' not in p.parts and p.suffix!='.pyc')
    assert actual=={v['path'] for v in runtime['files']},'dependency inventory'
    return len(external['files'])+len(runtime['files'])+len(runtime['tools'])
count=check_bindings()
runtime=base.parent/'geometry/.runtime/bin/python'
candidate=base.parent/'snapshot/unsolved_math_prioritization/attempts/20000450/verify_turn1.py'
jobs=[('candidate','018_candidate_reproduction',[str(runtime),'-B',str(candidate)],0),
      ('independent','019_independent_arithmetic',[sys.executable,'-B',str(base/'check_arithmetic.py')],0)]
for name,receipt in [('drop_twist','020_mutant_drop_twist'),('wrong_radical','021_mutant_wrong_radical'),
                     ('wrong_cyclotomic','022_mutant_wrong_cyclotomic'),('wrong_norm_degree','023_mutant_wrong_norm_degree')]:
    jobs.append((name,receipt,[sys.executable,'-B',str(base/'check_arithmetic.py'),'--mutant',name],1))
results=[]
for name,receipt,argv,exit_code in jobs:
    start=utc(); child=subprocess.run(argv,cwd=base,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    end=utc(); folder=base/'executions'/receipt
    assert child.returncode==exit_code,(name,child.returncode)
    assert child.stdout==(folder/'stdout.txt').read_bytes(),name+' full stdout'
    assert child.stderr==(folder/'stderr.txt').read_bytes(),name+' full stderr'
    results.append({'name':name,'actual_argv':argv,'actual_env':ENV,'actual_cwd':str(base),
                    'start_utc':start,'end_utc':end,'actual_exit_code':child.returncode,
                    'full_stdout':child.stdout.decode(),'full_stderr':child.stderr.decode(),
                    'matches_original_native_streams':True})
assert check_bindings()==count
print(json.dumps({'status':'PASS','replayed_mathematical_streams':len(results),
                  'binding_count_before_after':count,'all_bindings_unchanged':True,
                  'replay_interpreter':sys.executable,'replay_version':sys.version,'results':results},indent=2,sort_keys=True))
