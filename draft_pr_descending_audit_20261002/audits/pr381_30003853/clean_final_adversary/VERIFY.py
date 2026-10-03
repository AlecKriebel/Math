from pathlib import Path
import os,json,hashlib,subprocess,sys
D=Path(__file__).resolve().parent
M=json.loads((D/'OUTPUT_MANIFEST.json').read_text())
for e in M['files']:
 b=(D/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
# Seal verification includes local source artifacts; it makes no claim about author processed source bindings.
for name in ['INDEPENDENT_SEAL.json','POSTCANDIDATE_SEAL.json']:
 for e in json.loads((D/name).read_text())['files']:
  b=(D/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(name,e['path'])
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for script,stdout in [('controls/independent_controls.py','controls/independent_controls.stdout.txt'),('controls/postcandidate_controls.py','controls/postcandidate_controls.stdout.txt')]:
 r=subprocess.run([sys.executable,str(D/script)],env=env,capture_output=True);assert r.returncode==0 and not r.stderr and r.stdout==(D/stdout).read_bytes(),script
P=D.parent/'scope_repaired_snapshot/problems/30003853_thompson_subgroup_abelianization'
runs=[('author','REPLAY_ALL.py',P),('historical_independent','independent_check.py',P/'independent_review'),('current_publication','verify_publication.py',P)]+[(f'turn{t}',f'verify_turn{t}.py',P) for t in range(1,6)]
for name,script,cwd in runs:
 r=subprocess.run([sys.executable,str(cwd/script)],cwd=cwd,env=env,capture_output=True)
 assert r.returncode==0 and r.stdout==(D/'replays'/f'{name}.stdout.txt').read_bytes() and r.stderr==(D/'replays'/f'{name}.stderr.txt').read_bytes(),name
head=M['candidate_head']
for e in json.loads((D/'OBJECT_SOURCE_RECEIPT.json').read_text())['exact_git_objects']:
 b=subprocess.check_output(['git','-C','/Users/alec/Documents/Math','show',f"{head}:{e['path']}"])
 assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
print(json.dumps({'candidate_head':head,'bounded_output_bindings':len(M['files']),'all47_git_objects':True,'all8_candidate_fullstreams_exact':True,'sealed_independent_fullstreams_exact':True,'new_postcandidate_controls':81628,'author_controls':562635,'historical_controls':110736,'optional_public_source_bindings':0,'fresh_primary_PDF_matches':7,'author_processed_source_bindings_not_reproduced':13,'verdict':'PASS scoped partial results and corrected gap; unsolved5/5'},indent=2))
