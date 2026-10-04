"""Verify an actual published repository-kit receipt and exact public files."""
from pathlib import Path
import datetime as dt
import hashlib
import importlib.util
import json
import os
import sys
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]
C=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p.read_bytes())}
def load(p): return json.loads(p.read_bytes())
def save(p,v):
    with p.open('x') as f: json.dump(v,f,indent=2); f.write('\n')
if sys.flags.optimize: raise RuntimeError('Optimization forbidden')
(F/'PUBLICATION_VERIFICATION_SOURCE.py').write_bytes(Path(__file__).read_bytes())
manifest=A/'publication_package_v1/zenodo-deposit.json'
assert sha(manifest.read_bytes())=='65bfdc7ac06bde958e1d700499cd6ec8b29e244a0d93b62227a26d99a19da6ba'
spec=importlib.util.spec_from_file_location('kit',R/'zenodo_deposit_tool/zenodo.py')
kit=importlib.util.module_from_spec(spec); spec.loader.exec_module(kit)
metadata,files=kit.load_manifest(manifest)
upload=C/'root_pr57_zenodo_publish_20261004_actual_capture/stdout.bin'
inspection=C/'root_pr57_zenodo_published_inspection_20261004_actual_capture/stdout.bin'
for receipt in (upload,inspection):
    capture=load(receipt.parent/'CAPTURE.json'); value=load(receipt)
    assert capture['status']=='PASS' and capture['stdout']['sha256']==sha(receipt.read_bytes())
    assert value['environment']=='production' and value['state']=='published' and value['id']==23131374
    assert value['doi']=='10.5281/zenodo.23131374' and value['title']==metadata['title']
    assert value['files']==[{'name':f['name'],'size':f['size'],'sha256':f['sha256']} for f in files]
value=load(inspection)
assert value['doi_resolution']['status']=='resolved' and value['doi_resolution']['http_status']==200
client=kit.ZenodoClient('production',kit.token_for('production'))
start=dt.datetime.now(dt.timezone.utc).isoformat()
deposit=client.get(23131374); kit.validate_record(deposit,23131374)
assert deposit['submitted'] is True
norms=kit.verify(deposit,metadata,files)
projection={k:deposit[k] for k in ('id','submitted','metadata','files','doi','created','modified') if k in deposit}
save(F/'AUTHENTICATED_PUBLISHED_METADATA_AND_FILES.json',{'actual_pid':os.getpid(),'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'operation':'Repository Zenodo kit read-only get and exact verify','metadata_normalizations':norms,'published_projection':projection})
readbacks=[]
for item in files:
    url='https://zenodo.org/records/23131374/files/'+quote(item['name'],safe='')+'?download=1'
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    request=Request(url,headers={'User-Agent':'Math-PR-Publication-Review/1.0'},method='GET')
    with urlopen(request,timeout=30) as response:
        assert urlsplit(response.url).scheme=='https' and urlsplit(response.url).hostname=='zenodo.org'
        body=response.read(item['size']+1)
        row={'name':item['name'],'url':url,'HTTP_status':response.status,'final_url':response.url,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'bytes':len(body),'sha256':sha(body),'md5':hashlib.md5(body).hexdigest(),'authentication_sent':False}
    assert row['HTTP_status']==200 and len(body)==item['size'] and sha(body)==item['sha256'] and body==item['path'].read_bytes()
    readbacks.append(row)
record={'schema':'pr57-ordered-publication-verification/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'DOI':value['doi'],'record_id':23131374,'record_url':'https://zenodo.org/records/23131374','published':True,'all_public_bytes_identical':True,'public_file_readbacks':readbacks,'DOI_resolution':value['doi_resolution'],'manifest':bind(manifest),'inspection_receipt':bind(inspection),'upload_receipt':bind(upload),'repository_upload_kit_used':True,'intended_metadata_identical':True,'metadata_normalizations':norms,'metadata_readback':bind(F/'AUTHENTICATED_PUBLISHED_METADATA_AND_FILES.json'),'bounded_priority_audit_clearance':True,'absolute_historical_priority_certified':False,'PR50_priority_exception_extended':False,'tracker_row_written':False,'native_merged':False,'new_central_proof_attempts':0,'PR57_ordered_workflow_percent':90,'dated_completed_program_fraction_percent':5/99*100,'goal_complete':False}
save(F/'PUBLICATION_VERIFICATION.json',record)
print(json.dumps(record,indent=2))
