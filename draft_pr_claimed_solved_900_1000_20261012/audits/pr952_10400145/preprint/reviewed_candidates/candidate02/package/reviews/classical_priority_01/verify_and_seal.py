"""Read-only original authentication and explicitly source-free public payload seal."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, stat
P=Path(__file__).resolve().parent
A=P.parent.parent
pins=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_text())
snapshot=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
repository=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=A,text=True).strip())
checks=[]
for relative,pin in pins['files'].items():
    path=A/'original'/relative
    body=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    head_body=subprocess.check_output(['git','cat-file','blob',pins['head']+':'+relative],cwd=A)
    gitmode=subprocess.check_output(['git','ls-tree',pins['head'],'--',relative],cwd=repository,text=True).split()[0]
    observed={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'git_blob':blob,'git_mode':gitmode,'disk_mode':f'{stat.S_IMODE(path.stat().st_mode):04o}'}
    checks.append({'path':relative,'observed':observed,'matches_record':observed==pin,'matches_snapshot':observed['sha256']==snapshot['files'][relative],'matches_head_body':body==head_body})
receipt={'utc':datetime.now(timezone.utc).isoformat(),'head':pins['head'],'branch':subprocess.check_output(['git','branch','--show-current'],cwd=A,text=True).strip(),'count':len(checks),'all_pass':all(c['matches_record'] and c['matches_snapshot'] and c['matches_head_body'] for c in checks),'checks':checks}
assert receipt['all_pass'] and receipt['count']==33 and receipt['branch']=='main'
(P/'END_AUTH.json').write_text(json.dumps(receipt,indent=2)+'\n')
private=P/'private'
private.chmod(0o700)
inventory=[]
for f in sorted(private.iterdir()):
    if f.is_file():
        f.chmod(0o600)
        b=f.read_bytes()
        inventory.append({'private_path':str(f.relative_to(P)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':f'{stat.S_IMODE(f.stat().st_mode):04o}'})
(P/'PRIVATE_EVIDENCE_INVENTORY.json').write_text(json.dumps({'utc':receipt['utc'],'private_directory_mode':'0700','raw_primary_evidence_publicly_excluded':True,'files':inventory},indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:
    f.write(f"\n- {receipt['utc']}: END checkpoint: 33/33 original body/hash/blob/Git-mode/disk-mode pins and bound-head comparisons pass; branch main. Public report and stable findings completed; all raw source bodies, extracts, screenshots and search-result bodies remain private0700/0600. Completion estimate100% of the assigned bounded audit. Exact historical absence, originality, unpublished history and intended correction remain unresolved. No external communication, outreach draft, Git mutation or publication performed by this reviewer.\n")
public=[
'APPROACH_FAMILIES.json','BIBLIOGRAPHY.md','END_AUTH.json','FINDINGS.json',
'INITIAL_PRIORITY_PLAN.md','PDF_METADATA.json','PRIVATE_EVIDENCE_INVENTORY.json',
'READING_SCOPES.json','REPORT.md','RESEARCH_LOG.md','RETRIEVALS.json','SEARCH_LOG.json',
'START_AUTH.json','SEAL_ATTEMPTS.json','retrieve.py','verify_and_seal.py'
]
payload=[]
for name in public:
    f=P/name
    b=f.read_bytes()
    assert not b.startswith(b'%PDF')
    assert not b.lstrip().lower().startswith((b'<!doctype html', b'<html'))
    if name.endswith('.json'):json.loads(b)
    payload.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'schema':'classical-priority-audit-seal-v1','utc':receipt['utc'],'bound_head':pins['head'],'public_payload_policy':'Only reviewer-authored reasoning, bibliography, query strings, scopes and verification metadata. No raw third-party text, PDF, HTML, extraction or screenshots. MANIFEST itself is externally hashed.','public_payloads':payload,'private_exclusion':'private/** contains raw primary bodies/extracts/screenshots/search bodies; never include it in public payloads. PRIVATE_EVIDENCE_INVENTORY lists hashes and modes only.','start_auth_all_pass':json.loads((P/'START_AUTH.json').read_text())['all_pass'],'end_auth_all_pass':receipt['all_pass'],'original_count':33,'search_batches':len(json.loads((P/'SEARCH_LOG.json').read_text())),'real_queries':sum(len(r['queries']) for r in json.loads((P/'SEARCH_LOG.json').read_text())),'priority_verdict':json.loads((P/'FINDINGS.json').read_text())['verdict'],'completion_percent':100}
(P/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
b=(P/'MANIFEST.json').read_bytes()
for item in payload:
    f=P/item['path'];actual=f.read_bytes()
    assert len(actual)==item['bytes'] and hashlib.sha256(actual).hexdigest()==item['sha256']
print(json.dumps({'manifest_bytes':len(b),'manifest_sha256':hashlib.sha256(b).hexdigest(),'public_payload_count':len(payload),'private_evidence_files':len(inventory),'start_all_pass':manifest['start_auth_all_pass'],'end_all_pass':manifest['end_auth_all_pass'],'original_count':33,'real_queries':manifest['real_queries'],'completion_percent':100},indent=2))
