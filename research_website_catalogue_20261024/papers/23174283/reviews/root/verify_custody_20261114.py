"""Root hash/recorded-evidence closure without repeating scientific campaigns."""
from pathlib import Path,PurePosixPath
import json,hashlib,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent.parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
J=lambda p:json.loads(p.read_bytes())
def need(v,m):
    if not v:raise RuntimeError(m)
pins={'scope':('FINAL_SEAL.json','b69b7f92373fdeedbde150f131276a941259fa0c8727a262e0feedf362007416'),'analytic':('SEAL.json','09ca0cf2cbee02b9038b63e4e73ef4ab1a02eb99c8fe87fac2ad0313af7ff540'),'adversarial':('SEAL.json','9ade8b3d145db3fd856faed59ce07cd9ee270ab673f0b5f0c54c0a2b004af86b')}
for lane,(f,pin) in pins.items():need(H(R/lane/f)==pin,'exact sealed lane '+lane)
S=R/'scope';m=J(S/'ARTIFACT_MANIFEST.json');seal=J(S/'FINAL_SEAL.json')
need(H(S/'ARTIFACT_MANIFEST.json')==seal['artifact_manifest_sha256'],'scope manifest seal')
names=set()
for x in m['entries']:
    q=PurePosixPath(x['path']);need(not q.is_absolute() and '..' not in q.parts and x['path'] not in names,'safe owned path');names.add(x['path']);p=S/x['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==x['bytes'] and H(p)==x['sha256'],'owned scope binding '+str(p))
need({str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}==names|{'ARTIFACT_MANIFEST.json','FINAL_SEAL.json'},'scope exact owned set')
inputs=J(S/'INPUT_MANIFEST.json')
for x in inputs['source_files']+inputs['foreign_primary_objects']:
    p=Path(x['path']);need(p.is_file() and not p.is_symlink() and p.stat().st_size==x['bytes'] and H(p)==x['sha256'],'scope external '+str(p))
run=J(S/'supplied_replay/RESULT.json');need(run['successful_controls']==4 and run['expected_mathematical_rejections']==5,'stored supplied scope')
need(all(x['reaped'] and not x['timed_out'] and x['error'] is None and x['exit']==x['expected_exit'] for x in run['full_process_results']),'recorded process outcomes')
need(J(S/'INDEPENDENT_RESULT.json')==J(S/'INDEPENDENT_OPTIMIZED_RESULT.json'),'stored source-interface modes identical')
executions=[]
for path in [R/'analytic/verify_read_only.py',R/'adversarial/VERIFY_READ_ONLY.py']:
    args=[sys.executable,'-E','-B',str(path)];r=subprocess.run(args,capture_output=True,text=True,timeout=60);need(r.returncode==0 and not r.stderr,'actual read-only closure '+str(path));executions.append({'args':args,'script_sha256':H(path),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
print(json.dumps({'status':'PASS_ROOT_THREE_SEALED_LANES_AND_NATIVE_CUSTODY_WITHOUT_SCIENTIFIC_REPLAY','scope_owned_payloads':len(names),'scope_source_bindings':len(inputs['source_files']),'scope_foreign_primary_bindings':len(inputs['foreign_primary_objects']),'actual_read_only_executions':executions,'scientific_programs_or_old_campaigns_reexecuted':False,'source_or_old_review_mutation':False,'infinite_theorem_proved_by_counts_or_hashes':False},indent=2))
