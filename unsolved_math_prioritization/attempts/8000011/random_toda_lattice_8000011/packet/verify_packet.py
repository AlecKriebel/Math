from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
m=json.loads((root/'FROZEN_MANIFEST.json').read_text())
for name,sha in m.items():
 assert hashlib.sha256((root/name).read_bytes()).hexdigest()==sha,name
for stem in ['turn1_exact','turn3_exact','turn4_numerical','turn5_exact']:
 p=subprocess.run([sys.executable,str(root/'checks'/f'{stem}.py')],capture_output=True,check=True)
 assert p.stdout==(root/'checks'/f'{stem}.stdout.json').read_bytes(),stem
state=json.loads((root/'TURN_STATE.json').read_text())
assert state['author_turns']==5 and not state['original_problem_resolved']
assert state['status']=='exhausted_original_unsolved_pending_review'
print(json.dumps({'status':'PASS','bound_files':len(m),'exact_assertions':2559,'floating_diagnostics':4,'author_turns':5,'original_problem_resolved':False,'stopping_rule':'first simultaneous all-coupling crossing'},indent=2))
