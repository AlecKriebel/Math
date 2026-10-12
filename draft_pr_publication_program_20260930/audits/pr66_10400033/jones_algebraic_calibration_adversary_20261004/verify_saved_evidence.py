"""Verify the genuine execution receipts and seal the owned audit artifacts."""
import datetime,hashlib,json,pathlib

ROOT=pathlib.Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
verified=[]; failures=[]
for receipt_path in sorted((ROOT/'receipts').glob('*/receipt.json')):
    if receipt_path.parent.name=='verify_saved_evidence': continue
    receipt=json.loads(receipt_path.read_text())
    assert receipt['pid']>0 and receipt['argv'] and receipt['cwd']==str(ROOT)
    assert datetime.datetime.fromisoformat(receipt['utc_started'])<=datetime.datetime.fromisoformat(receipt['utc_ended'])
    for stream in ('stdout','stderr'):
        metadata=receipt[stream]; body=pathlib.Path(metadata['path'])
        assert body.stat().st_size==metadata['bytes'] and sha(body)==metadata['sha256'],str(body)
    verified.append(str(receipt_path.relative_to(ROOT)))
    if receipt['exit_code']!=0: failures.append({'receipt':str(receipt_path.relative_to(ROOT)),'exit_code':receipt['exit_code']})
assert {pathlib.Path(r['receipt']).parent.name for r in failures}=={'crop_primary','independent_tl_first_run'}
seal=json.loads((ROOT/'first_conclusion_seal.json').read_text())
assert sha(ROOT/'FIRST_CONCLUSION.md')==seal['sha256']
artifacts=[]
for path in sorted(ROOT.rglob('*')):
    if not path.is_file(): continue
    relative=path.relative_to(ROOT)
    if relative.name=='artifact_manifest.json' or str(relative).startswith('receipts/verify_saved_evidence/'): continue
    artifacts.append({'path':str(relative),'bytes':path.stat().st_size,'sha256':sha(path)})
manifest={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only this family folder; excludes this manifest and its own future execution receipt to avoid a self-hash cycle.','verified_execution_receipts':len(verified),'expected_preserved_nonzero_exits':failures,'first_conclusion_seal_valid':True,'artifacts':artifacts}
(ROOT/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='artifacts'},indent=2))
print('owned_artifacts_hashed',len(artifacts))
