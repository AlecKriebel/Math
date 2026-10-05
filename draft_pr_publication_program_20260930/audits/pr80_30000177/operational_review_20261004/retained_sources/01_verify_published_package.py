"""Read-only exact publication readback; accepts no provisional release."""
import datetime, hashlib, importlib.util, json, os
from pathlib import Path
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
A=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr80_30000177')
R=A.parents[2]
F=Path(__file__).parent
def load(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
gate=load(A/'ROOT_FINAL_PACKAGE_GATE_20261004.json')
assert gate['publication_clearance'] is True
snapshot=load(A/'PUBLICATION_PACKAGE_V2_REVIEW_SNAPSHOT_20261004.json')
P=Path(snapshot['package_directory'])
for item in snapshot['files']:
    body=(P/item['path']).read_bytes()
    assert len(body)==item['bytes'] and sha(body)==item['sha256']
spec=importlib.util.spec_from_file_location('zenodo_kit',R/'zenodo_deposit_tool/zenodo.py')
kit=importlib.util.module_from_spec(spec); spec.loader.exec_module(kit)
metadata,files=kit.load_manifest(P/'zenodo-deposit.json')
published=load(F/'process_evidence/zenodo_publish_v2/stdout.bin')
inspected=load(F/'process_evidence/zenodo_inspect_published_v2/stdout.bin')
for value in (published,inspected):
    assert value['state']=='published' and value['environment']=='production'
    assert value['files']==[{'name':f['name'],'size':f['size'],'sha256':f['sha256']} for f in files]
    assert value['title']==metadata['title']
assert published['id']==inspected['id'] and published['doi']==inspected['doi']
ID=inspected['id']
client=kit.ZenodoClient('production',kit.token_for('production'))
deposit=client.get(ID)
kit.validate_record(deposit,ID)
assert deposit['submitted'] is True
normalizations=kit.verify(deposit,metadata,files)
projection={k:deposit[k] for k in ('id','submitted','metadata','files','doi','created','modified') if k in deposit}
(F/'PUBLISHED_AUTHENTICATED_PROJECTION.json').write_text(json.dumps(projection,indent=2)+'\n')
checks=[]
for item in files:
    url=f'https://zenodo.org/records/{ID}/files/'+quote(item['name'],safe='')+'?download=1'
    request=Request(url,headers={'User-Agent':'Math-PR-Publication-Review/1.0'},method='GET')
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urlopen(request,timeout=30) as response:
        assert response.status==200 and urlsplit(response.url).hostname=='zenodo.org'
        data=response.read(item['size']+1)
        assert len(data)==item['size'] and sha(data)==item['sha256'] and data==item['path'].read_bytes()
        checks.append({'name':item['name'],'bytes':len(data),'sha256':sha(data),'md5':hashlib.md5(data).hexdigest(),'HTTP_status':response.status,'final_url':response.url,'start_UTC':start,'end_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authentication_sent':False})
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'status':'PUBLISHED_EXACT_METADATA_AND_PUBLIC_PAYLOAD_BYTES_VERIFIED','record_id':ID,'DOI':inspected['doi'],'record_url':f'https://zenodo.org/records/{ID}','all8_public_bytes_identical':True,'intended_metadata_exact':True,'metadata_normalizations':normalizations,'public_file_checks':checks,'DOI_resolution':inspected['doi_resolution'],'tracker_written':False,'native_merged':False,'workflow_percent':85,'program_completed':'9/99','original_budget':'1/5','new_central_proof_search_turns':0}
with (A/'ROOT_PUBLICATION_VERIFICATION_20261004.json').open('x') as f: f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
