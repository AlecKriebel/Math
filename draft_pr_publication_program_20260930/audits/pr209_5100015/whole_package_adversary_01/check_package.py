"""Owned independent read-only package/native/receipt checks; writes this folder only."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile,stat,gzip

P=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint')
ROOT=Path(__file__).resolve().parent.parent
A=Path(__file__).resolve().parent
N=ROOT/'native_custody_01/archive'

def bind(q):
    b=q.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def rowscheck(base,manifest):
    rows=json.loads(manifest.read_text())['files'];names=[]
    for r in rows:
        rel=Path(r['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        q=base/rel
        assert q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(base.resolve())
        assert bind(q)=={'bytes':r['bytes'],'sha256':r['sha256']},str(q)
        names.append(r['path'])
    assert len(names)==len(set(names))
    return len(names)

out={'utc':datetime.now(timezone.utc).isoformat()}
out['source_manifest_bound_files']=rowscheck(P,P/'SOURCE_MANIFEST.json')
out['verification_manifest_bound_files']=rowscheck(P/'verification',P/'verification/MANIFEST.json')
out['prepared_current_packet_files']=rowscheck(P/'pr_update/5100015',P/'pr_update/5100015/CURRENT_PACKET_MANIFEST.json')
out['native_revised_packet_files']=rowscheck(N/'revised',N/'revised/CURRENT_PACKET_MANIFEST.json')
original=[f for f in (N/'original').rglob('*') if f.is_file()]
assert len(original)==23
out['original_files']=len(original);comparisons={}
for label,base in [('zip_verification_original',P/'verification/original_submission'),('zip_current_history',P/'pr_update/5100015/history/original_submission_20261016'),('native_revised_history',N/'revised/history/original_submission_20261016')]:
    for f in original:
        rel=f.relative_to(N/'original')
        assert f.read_bytes()==(base/rel).read_bytes(),str(base/rel)
    comparisons[label]={'byte_identical_original_files':len(original)}
out['original_preservation']=comparisons
with zipfile.ZipFile(P/'k303b-source-verification.zip') as z:
    ns=z.namelist()
    assert len(ns)==len(set(ns)) and z.testzip() is None
    expected={'k303b_outer_center_pedal_product/'+r['path'] for r in json.loads((P/'SOURCE_MANIFEST.json').read_text())['files']}|{'k303b_outer_center_pedal_product/SOURCE_MANIFEST.json'}
    assert set(ns)==expected
    for n in ns:
        assert not stat.S_ISLNK(z.getinfo(n).external_attr>>16)
        rel=Path(n).relative_to('k303b_outer_center_pedal_product')
        assert not rel.is_absolute() and '..' not in rel.parts
        assert z.read(n)==(P/rel).read_bytes(),n
    out['zip']={'members':len(ns),'duplicate_names':False,'symlinks':False,'exact_source_manifest_coverage':True,'all_members_equal_local_source':True}
assert json.loads((P/'metadata.json').read_text())==json.loads((P/'deposit.json').read_text())['metadata']
assert (P/'metadata.json').read_bytes()==(N/'revised/PUBLICATION_METADATA.json').read_bytes()
assert (P/'pr_update/5100015/PROOF.md').read_bytes()==(N/'revised/PROOF.md').read_bytes()
out['metadata_deposit_native_equality']=True
out['native_prepared_proof_equality']=True
b=gzip.decompress((P/'verification/audits/physical_geometry_adversary_01/FAILED_PROBE_01_COMPLETE.json.gz').read_bytes())
assert len(b)==72751 and hashlib.sha256(b).hexdigest()=='b74725bfa1ff239c31f73443898644c6fcf29cc044de4f30edc32c2c75333dbb'
out['failed_probe_lossless_recovery']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
replay=ROOT/'root_reproduction_01/isolated_replay/REPRODUCTION.json'
j=json.loads(replay.read_text())
assert j['status']=='PASS' and j['scientific_programs']==8 and j['verification_files_before']==j['verification_files_after']==149
for r in j['results']:
    assert r['status']=='PASS' and r['all_scientific_fields_identical'] and r['copied_program_byte_identical']
    assert hashlib.sha256((P/'verification'/r['source_program']).read_bytes()).hexdigest()==r['program_sha256']
out['root_actual_replay']={'binding':bind(replay),'eight_byte_bound_suites_PASS':True,'before_after149':True,'independently_rerun_by_this_audit':False}
out['ancillary_root_note']=bind(ROOT/'root_source_priority_01/ROOT_MATHEMATICAL_PRIORITY_AUDIT.md')
provider=ROOT/'root_provider_readback_01'
for receipt_name,body_name in [('ZENODO_INSPECT_RECEIPT.json','ZENODO_INSPECT_STDOUT.json'),('TRACKER_GET_RECEIPT.json','TRACKER_GET_STDOUT.json')]:
    receipt=json.loads((provider/receipt_name).read_text())
    assert receipt['returncode']==0 and receipt['read_only'] is True
    assert {k:receipt['stdout'][k] for k in ['bytes','sha256']}==bind(provider/body_name)
pub=json.loads((provider/'ZENODO_INSPECT_STDOUT.json').read_text())
assert pub['state']=='published' and pub['id']==23413614 and pub['doi_resolution']['http_status']==200
assert pub['metadata_normalizations']==[]
want={'k303b-outer-center-pedal-areas.pdf':bind(P/'manuscript.pdf'),'k303b-source-verification.zip':bind(P/'k303b-source-verification.zip')}
assert len(pub['files'])==2
for f in pub['files']:
    assert want[f['name']]=={'bytes':f['size'],'sha256':f['sha256']}
tracker=json.loads((provider/'TRACKER_GET_STDOUT.json').read_text())
matches=[(i+1,row) for i,row in enumerate(tracker['values']) if any('10.5281/zenodo.23413614' in str(cell) for cell in row)]
assert len(matches)==1 and matches[0][0]==121 and len(matches[0][1])==4
out['root_provider_receipts']={'zenodo':bind(provider/'ZENODO_INSPECT_STDOUT.json'),'tracker':bind(provider/'TRACKER_GET_STDOUT.json'),'existing_DOI':'10.5281/zenodo.23413614','unique_DOI_row':121,'row_cells':matches[0][1],'readbacks_executed_by':'Root; this audit independently inspected and byte-bound receipts only'}
out['status']='PASS'
(A/'INTEGRITY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='root_provider_receipts'},indent=2))
