from pathlib import Path
import sys,subprocess,shutil,json,hashlib,os
sys.dont_write_bytecode=True
R=Path(__file__).absolute().parent
sys.path.insert(0,str(R/'extracted/verification'))
import self_test as S
scratch=R/'small_control_fixtures';scratch.mkdir(exist_ok=True)
good=S.fixture(scratch/'base')
checks=[]
def run(label,mutate,needle):
 p=scratch/label;shutil.copytree(good,p);mutate(p)
 before=S.snapshot(scratch)
 for optimized in [False,True]:
  q=S.invoke(p/'verification/verify_all.py',optimized)
  if q.returncode==0 or needle not in q.stderr.decode() or S.snapshot(scratch)!=before:raise ValueError(label+' control failed '+q.stderr.decode())
  checks.append({'case':label,'mode':'optimized' if optimized else 'normal','exit':q.returncode,'last_error':q.stderr.decode().splitlines()[-1],'no_write':True})
 shutil.rmtree(p)
def allow(p,fn):
 a=p/'verification/AUDIT_MEMBERS.json';x=json.loads(a.read_bytes());fn(x);a.write_bytes(S.encoded(x))
run('duplicate_json',lambda p:(p/'verification/AUDIT_MEMBERS.json').write_text('{"a":1,"a":2}'),'duplicate JSON key')
run('bool_pin',lambda p:allow(p,lambda x:x['authored-note.md'].update(bytes=True)),'invalid authored-member pin')
run('uppercase_hash',lambda p:allow(p,lambda x:x['authored-note.md'].update(sha256='A'*64)),'invalid authored-member pin')
run('case_collision',lambda p:allow(p,lambda x:x.update({'AUTHORED-NOTE.MD':x['authored-note.md']})),'case-colliding audit member')
run('reserved_path',lambda p:allow(p,lambda x:x.update({'NUL.json':x['authored-note.md']})),'nonportable member component')
run('backslash_path',lambda p:allow(p,lambda x:x.update({'a\\b':x['authored-note.md']})),'noncanonical/nonportable')
run('unsafe_plan',lambda p:(p/'verification/CONTROL_PLAN.json').write_text('{"diagnostic":"../../escape"}'),'control-plan schema mismatch')
shutil.rmtree(scratch)
(R/'OWN_CONTROLS.json').write_bytes(S.encoded({'status':'PASS','small_synthetic_fixture':True,'checks':checks,'count':len(checks)}))
