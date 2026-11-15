"""Root custody adoption only; no repeated mathematical programs or campaigns."""
from pathlib import Path, PurePosixPath
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent.parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
J=lambda p:json.loads(p.read_bytes())
def need(v,m):
    if not v:raise RuntimeError(m)
expected={'scope':('SEAL.json','bb5f6f9d541764a9556679e7aa331824679593a2725fce60d55cb17b9150b514'),
          'analytic':('FINAL_SEAL.json','9edc315ab6e3b36ababfa5cb284d8d75c76082a909c400f3966233156db2feb2'),
          'adversarial':('FINAL_SEAL.json','54a70bf0acfa72540517f65bd7f315c0cc4e9822a389609baba0dd0417ef1ef3')}
for lane,(name,pin) in expected.items():need(H(R/lane/name)==pin,'exact sealed lane '+lane)
A=R/'analytic';m=J(A/'FINAL_MANIFEST.json');s=J(A/'FINAL_SEAL.json')
need(H(A/'FINAL_MANIFEST.json')==s['manifest_sha256'],'analytic manifest seal')
names=set()
for row in m['files']:
    q=PurePosixPath(row['path']);need(not q.is_absolute() and '..' not in q.parts and row['path'] not in names,'safe unique analytic path')
    names.add(row['path']);p=A/row['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==row['bytes'] and H(p)==row['sha256'],'analytic payload '+row['path'])
need({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}==names|{'FINAL_MANIFEST.json','FINAL_SEAL.json'},'exact analytic file set')
executions=[]
for path in [R/'scope/verify_read_only.py',A/'verify_custody.py',R/'adversarial/verify_packet.py']:
    args=[sys.executable,'-B',str(path)];r=subprocess.run(args,capture_output=True,text=True,timeout=60)
    need(r.returncode==0 and not r.stderr,'actual read-only verifier '+str(path))
    executions.append({'args':args,'script_sha256':H(path),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
need(J(A/'INDEPENDENT_NORMAL.json')==J(A/'INDEPENDENT_OPTIMIZED.json'),'recorded exact modes identical')
need((A/'SUPPLIED_REPLAY.json').read_bytes()==(R.parent/'sources/published-source/kourovka-21-149/exact_constructions_result.json').read_bytes(),'stored native exact output identity')
print(json.dumps({'status':'PASS_ROOT_SEALED_REVIEW_SOURCE_AND_RECORDED_RESULTS_WITHOUT_SCIENTIFIC_REPLAY','analytic_owned_payloads':len(names),'actual_read_only_executions':executions,'scientific_campaign_reexecuted':False,'old_source_or_review_mutation':False,'proof_replaced_by_hashes_or_counts':False},indent=2))
