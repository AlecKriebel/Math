from pathlib import Path
import hashlib,json,subprocess,sys
r=Path(__file__).resolve().parent
p=r.parent/'random_toda_lattice_8000011'/'packet'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
m=json.loads((r/'REVIEW_MANIFEST.json').read_text())
assert sha(p/'FROZEN_MANIFEST.json')==m['reviewed_packet_manifest_sha256']
for name,digest in m['files'].items():assert sha(r/name)==digest,name
frozen=json.loads((p/'FROZEN_MANIFEST.json').read_text())
for name,digest in frozen.items():assert sha(p/name)==digest,name
for turn in range(1,6):
 for name,digest in json.loads((p/'turns'/f'TURN_{turn}_MANIFEST.json').read_text()).items():
  assert sha(p/name)==digest,name
for script,out in [(p/'verify_packet.py',r/'author_replay.stdout.json'),(r/'audit_exact.py',r/'audit_exact.stdout.json'),(r/'audit_floating.py',r/'audit_floating.stdout.json')]:
 result=subprocess.run([sys.executable,str(script)],capture_output=True,check=True)
 assert result.stdout==out.read_bytes(),script
v=json.loads((r/'VERDICT.json').read_text())
assert v['original_problem_resolved'] is False and v['author_turns']==5
assert v['further_author_turns_performed']==0 and v['remote_writes'] is False
print(json.dumps({'status':'PASS','review_files':len(m['files']),'reviewed_packet_files':len(frozen),'author_turns':5,'original_problem_resolved':False,'exact_review_predicates':2049,'floating_review_predicates':47},indent=2))
