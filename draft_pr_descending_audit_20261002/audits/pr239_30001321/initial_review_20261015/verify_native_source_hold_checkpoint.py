"""Read back all owned Git blobs plus critical native content; no mutations."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
import subprocess

ROOT=Path('/Users/alec/Documents/Math')
D=Path(__file__).resolve().parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
receipt=json.loads((D/'PRIORITY_SOURCE_HOLD_PUBLICATION_RECEIPT.json').read_text())
commit=receipt['commit']
prefix=D.relative_to(ROOT).as_posix()+'/'


def get(path):
    run=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+path],capture_output=True,timeout=60)
    assert run.returncode==0,run.stderr.decode()
    return json.loads(run.stdout)


parent=D.parent.relative_to(ROOT).as_posix()
listing=get('contents/'+parent+'?ref='+commit)
subtree=[row for row in listing if row['name']==D.name]
assert len(subtree)==1 and subtree[0]['type']=='dir'
tree=get('git/trees/'+subtree[0]['sha']+'?recursive=1')
assert not tree.get('truncated')
native={row['path']:row for row in tree['tree'] if row['type']=='blob'}
verified=[]
other=[]
for row in receipt['owned_files']:
    path=ROOT/row['path']
    data=path.read_bytes()
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if row['path'].startswith(prefix):
        short=row['path'][len(prefix):]
        assert native[short]['sha']==blob and native[short]['mode']=='100644'
        verified.append(dict(path=row['path'],bytes=len(data),git_blob_sha1=blob,sha256=row['sha256']))
    else:
        other.append(row)


def full_readback(row):
    remote=get('contents/'+row['path']+'?ref='+commit)
    actual=base64.b64decode(remote['content'])
    expected=(ROOT/row['path']).read_bytes()
    assert actual==expected
    return dict(path=row['path'],bytes=len(actual),sha256=hashlib.sha256(actual).hexdigest())


critical={'ROOT_PRIORITY_SOURCE_HOLD.md','CURRENT_AUDIT_STATE.json','ROOT_FINAL_PRIORITY_VALIDATION.json',
          'priority_local_limit_01/PUBLIC_AUTHORED_MANIFEST.json',
          'priority_synthesis_adversary_01/PUBLIC_AUTHORED_MANIFEST.json',
          'priority_bmp_archival_01/authored_manifest.json'}
extra=other+[row for row in receipt['owned_files'] if row['path'].startswith(prefix) and row['path'][len(prefix):] in critical]
with ThreadPoolExecutor(max_workers=6) as pool:
    direct=list(pool.map(full_readback,extra))
pr=get('pulls/239')
assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==receipt['original_PR_head_unchanged']
ref=get('git/ref/heads/main')['object']['sha']
if ref!=commit:
    assert get('compare/'+commit+'...'+ref)['status']=='ahead'
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',commit=commit,
            owned_files_verified=len(verified)+len(other),owned_subtree_git_blob_verifications=verified,
            direct_native_byte_readbacks=direct,PR_open_draft_head_unchanged=pr['head']['sha'],
            main_readback=ref,whole_third_party_sources_published=False,local_git_or_index_mutation=False,
            disposition='Mathematical PASS; material original-source priority hold; no preprint/deposit/tracker/merge')
(D/'ROOT_SOURCE_HOLD_NATIVE_READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['owned_subtree_git_blob_verifications','direct_native_byte_readbacks']},indent=2))
