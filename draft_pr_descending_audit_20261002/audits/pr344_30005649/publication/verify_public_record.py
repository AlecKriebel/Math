"""Read-only unauthenticated whole public record/file comparison after publication."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit
import hashlib,json,subprocess,sys

D=Path(__file__).resolve().parent;A=D.parent
label=sys.argv[1] if len(sys.argv)>1 else 'public_readback_001'
assert Path(label).name==label and label.startswith('public_readback_')
P=D/'private_public_downloads'/label
assert not P.exists();P.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(p.read_bytes())
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance
current_clearance()
published=load(D/'inspect_published_receipt.json')
assert published['state']=='published' and published['environment']=='production'
local=load(A/'preprint/zenodo-deposit.json')
assert published['title']==local['metadata']['title']
def fetch(label,url):
    parts=urlsplit(url)
    assert parts.scheme=='https' and parts.netloc=='zenodo.org' and not parts.query and not parts.fragment
    args=['curl','--fail','--silent','--show-error','--location','--max-time','60',
          '--user-agent','Math-Zenodo-Deposit-Tool/1.0',url]
    start=utc();r=subprocess.run(args,capture_output=True)
    for stream,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        (P/(label+'.'+stream)).write_bytes(b)
    rec={'argv':args,'started_utc':start,'finished_utc':utc(),'exit_code':r.returncode,
         'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),
         'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'automatic_retry':False}
    (P/(label+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    assert r.returncode==0 and not r.stderr,rec
    return r.stdout,rec
api='https://zenodo.org/api/records/'+str(published['id'])
body,api_rec=fetch('record',api);record=json.loads(body)
assert record['id']==published['id'] and record['doi']==published['doi']
metadata=record['metadata'];checked=[]
for key,value in local['metadata'].items():
    if key=='license':actual=metadata['license']['id']
    elif key=='upload_type':actual=metadata['resource_type']['type']
    elif key=='publication_type':actual=metadata['resource_type']['subtype']
    else:actual=metadata[key]
    assert actual==value,('Public metadata changed',key)
    checked.append(key)
assert len(checked)==len(local['metadata'])==11 and metadata['doi']==published['doi']
names={r['name'] for r in published['files']}
assert {r['key'] for r in record['files']}==names and len(record['files'])==2
rows=[]
for remote in record['files']:
    name=remote['key'];assert Path(name).name==name
    url=remote['links']['self'];parts=urlsplit(url)
    assert parts.path==f'/api/records/{record["id"]}/files/{name}/content'
    raw,native=fetch('file_'+name,url);b=(A/'preprint'/name).read_bytes()
    assert raw==b and len(b)==remote['size']
    md5=hashlib.md5(b).hexdigest();assert remote['checksum']=='md5:'+md5
    known=next(r for r in published['files'] if r['name']==name)
    assert sha(b)==known['sha256'] and len(b)==known['size']
    rows.append({'name':name,'bytes':len(b),'sha256':sha(b),'md5':md5,
                 'entire_public_download_equals_reviewed_local_file':True,'native':native})
receipt={'utc':utc(),'status':'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES',
         'record_id':record['id'],'doi':record['doi'],'public_api':api,
         'all_reviewed_metadata_keys_compared':checked,'metadata_semantics_changed':False,
         'only_public_schema_mapping':['license.id','resource_type.type','resource_type.subtype'],
         'all_file_bytes':rows,'doi_resolution':published['doi_resolution'],
         'public_record_native':api_rec,'private_capture_directory':str(P),
         'no_mutation_or_person_contact':True}
(D/'PUBLIC_RECORD_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='all_file_bytes'},indent=2))
