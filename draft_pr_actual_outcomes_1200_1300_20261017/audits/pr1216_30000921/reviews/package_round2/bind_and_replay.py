from pathlib import Path
import hashlib,json,zipfile,subprocess,sys,datetime
R=Path(__file__).resolve().parent
P=R.parent.parent/'publication'
def b(p):
 d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
inputs=['Polynomial_Multipliers_Note_v1.0.pdf','Polynomial_Multipliers_Verification_v1.0.zip','manuscript/main.tex','zenodo-deposit.json','BUILD_RECEIPT.json','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','CURRENT_SIMULTANEOUS_PROOF.md','prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py','WORKFLOW_REGRESSION_RECEIPT.json']
current={n:b(P/n) for n in inputs}
out=R/'INPUT_BINDINGS.json'
if out.exists():
 previous=json.loads(out.read_text())['inputs']
 if current!=previous:raise RuntimeError('Review input drift')
 print('All exact inputs unchanged')
else:out.write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':current},indent=2)+'\n')
E=R/'_local/extracted'
with zipfile.ZipFile(P/inputs[1]) as z:
 names=z.namelist()
 if len(set(names))!=len(names) or any(Path(n).is_absolute() or '..' in Path(n).parts for n in names):raise RuntimeError('unsafe zip')
 z.extractall(E)
 inventory={n:b(E/n) for n in names}
package={p.relative_to(P/'verification').as_posix():b(p) for p in (P/'verification').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
if inventory!=package:raise RuntimeError('zip vs current staging mismatch')
runs=[]
for flags in [[],['-O'],['-OO']]:
 proc=subprocess.run([sys.executable,'-B',*flags,str(E/'verify.py')],capture_output=True,text=True)
 if proc.returncode:raise RuntimeError(proc.stderr)
 runs.append({'flags':flags,'result':json.loads(proc.stdout)})
if not all(r['result']==runs[0]['result'] for r in runs):raise RuntimeError('optimization drift')
(R/'REPLAY_RECEIPT.json').write_text(json.dumps({'zip_members':len(names),'zip_exactly_matches_current_staging':True,'runs':runs},indent=2)+'\n')
print(json.dumps({'inputs':len(inputs),'zip_members':len(names),'replays':len(runs),'result':runs[0]['result']}))
