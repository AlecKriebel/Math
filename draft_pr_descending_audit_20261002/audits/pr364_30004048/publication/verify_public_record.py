"""Independent unauthenticated verification of public metadata and both files."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
from urllib.parse import urlsplit
D=Path(__file__).resolve().parent;A=D.parent
published=json.loads((D/'inspect_published_receipt.json').read_bytes())
local=json.loads((A/'preprint/zenodo-deposit.json').read_bytes())
record=json.loads((D/'public_record.stdout').read_bytes())
assert record['id']==published['id'] and record['doi']==published['doi']
metadata=record['metadata'];expected=local['metadata'];checked=[]
for key,value in expected.items():
 if key=='license':actual=metadata['license']['id']
 elif key=='upload_type':actual=metadata['resource_type']['type']
 elif key=='publication_type':actual=metadata['resource_type']['subtype']
 else:actual=metadata[key]
 assert actual==value,('public metadata mismatch',key)
 checked.append(key)
assert metadata['doi']==published['doi']
names={r['name'] for r in published['files']}
assert {r['key'] for r in record['files']}==names and len(record['files'])==2
private=D/'private_public_downloads';private.mkdir(exist_ok=True)
rows=[]
for remote in record['files']:
 name=remote['key'];url=remote['links']['self'];parts=urlsplit(url)
 assert parts.scheme=='https' and parts.netloc=='zenodo.org' and not parts.query and not parts.fragment
 assert parts.path==f'/api/records/{record["id"]}/files/{name}/content'
 start=datetime.now(timezone.utc).isoformat()
 r=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','60','--user-agent','Math-Zenodo-Deposit-Tool/1.0',url],capture_output=True)
 (private/name).write_bytes(r.stdout);(private/(name+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and r.stderr==b''
 b=(A/'preprint'/name).read_bytes();assert r.stdout==b and len(b)==remote['size']
 sha=hashlib.sha256(b).hexdigest();md5=hashlib.md5(b).hexdigest()
 assert remote['checksum']=='md5:'+md5
 known=next(x for x in published['files'] if x['name']==name)
 assert sha==known['sha256'] and len(b)==known['size']
 rows.append({'name':name,'url':url,'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'bytes':len(b),'sha256':sha,'md5':md5,'entire_public_download_equals_reviewed_local_file':True,'exit_code':0,'stderr_bytes':0})
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES','record_id':record['id'],'doi':record['doi'],'public_api':'https://zenodo.org/api/records/'+str(record['id']),'all_reviewed_metadata_keys_compared':checked,'metadata_semantics_changed':False,'only_public_schema_mapping':['license.id','resource_type.type','resource_type.subtype'],'all_file_bytes':rows,'doi_resolution':published['doi_resolution'],'no_mutation_or_person_contact':True}
(D/'PUBLIC_RECORD_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='all_file_bytes'},indent=2))
