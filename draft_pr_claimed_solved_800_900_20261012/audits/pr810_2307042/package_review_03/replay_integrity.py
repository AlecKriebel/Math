from pathlib import Path
import subprocess,json,datetime,shutil,sys
out=Path('.').resolve();s=out/'verification_extracted/source';rows=[]
def run(name,cmd,expect):
 r=subprocess.run(cmd,text=True,capture_output=True,cwd=out)
 try:j=json.loads(r.stdout)
 except Exception:j={'stdout':r.stdout,'stderr':r.stderr}
 rows.append({'name':name,'exit_code':r.returncode,'expected_success':expect,'result':j,'met_expectation':(r.returncode==0)==expect})
for opt in [[],['-O']]:
 for kind,stem,tree in [('author','AUTHOR_SAFE_FREEZE','author'),('audit','INDEPENDENT_AUDIT_SAFE','independent_audit')]:
  ext='AUTHOR_EXTERNAL_MANIFEST' if kind=='author' else 'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST'
  run(kind+(' optimized' if opt else ' normal'),[sys.executable,*opt,str(s/'FUNCTION_THEORY_2307042_INDEPENDENT_VERIFY.py'),kind,str(s/f'FUNCTION_THEORY_2307042_{stem}.zip'),str(s/f'FUNCTION_THEORY_2307042_{ext}.json'),'--tree',str(s/tree)],True)
 run('second-review'+(' optimized' if opt else ' normal'),[sys.executable,*opt,str(s/'FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_BOOTSTRAP.py'),str(s/'FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_SAFE.zip'),str(s/'FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_EXTERNAL_MANIFEST.json')],True)
fixture=out/'replay_negative';fixture.mkdir(exist_ok=True)
p=s/'FUNCTION_THEORY_2307042_AUTHOR_SAFE_FREEZE.zip';b=bytearray(p.read_bytes());b[50]^=1;(fixture/'mutated.zip').write_bytes(b)
run('author mutated archive rejected',[sys.executable,str(s/'FUNCTION_THEORY_2307042_INDEPENDENT_VERIFY.py'),'author',str(fixture/'mutated.zip'),str(s/'FUNCTION_THEORY_2307042_AUTHOR_EXTERNAL_MANIFEST.json')],False)
p=s/'FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_SAFE.zip';b=bytearray(p.read_bytes());b[50]^=1;(fixture/'second-mutated.zip').write_bytes(b)
run('second mutated archive rejected',[sys.executable,str(s/'FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_BOOTSTRAP.py'),str(fixture/'second-mutated.zip'),str(s/'FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_EXTERNAL_MANIFEST.json')],False)
(out/'SUPPLIED_INTEGRITY_REPLAY.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(r['met_expectation'] for r in rows) else 'FAIL','scope':'six positive normal/optimized runs and two archive-byte negative controls; not regeneration of historical full fixture suites; mathematics unproved by this replay','runs':rows},indent=2)+'\n')
print(json.dumps([{'name':r['name'],'pass':r['met_expectation']} for r in rows],indent=2))
