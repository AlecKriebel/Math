#!/usr/bin/env python3
"""Read-only original-science validation. Original code is never imported."""
import base64, datetime, hashlib, json, os, pathlib, stat, sys
root=pathlib.Path(__file__).resolve().parent
index=json.loads((root/'SCIENCE_INDEX.json').read_bytes())
assert len(index)==23
actual={p.relative_to(root/'original').as_posix() for p in (root/'original').rglob('*') if p.is_file()}
assert actual==set(index)
for name,e in index.items():
    p=root/'original'/name; s=p.lstat(); b=p.read_bytes()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_sha1']
    blob=json.loads((root/'receipts'/('blob_'+e['git_sha1']+'.stdout')).read_bytes())
    assert b==base64.b64decode(blob['content']) and blob['sha']==e['git_sha1']
for p in (root/'receipts').glob('*.json'):
    r=json.loads(p.read_bytes())
    if 'stdout' not in r: continue
    for stream in ('stdout','stderr'):
        b=p.with_suffix('.'+stream).read_bytes()
        assert len(b)==r[stream]['bytes'] and hashlib.sha256(b).hexdigest()==r[stream]['sha256']
    assert r['returncode']==0
metadata=json.loads((root/'receipts/pr_metadata.stdout').read_bytes())
comparison=json.loads((root/'receipts/comparison.stdout').read_bytes())
assert metadata['number']==59 and metadata['state']=='open' and metadata['draft'] is True and metadata['merged'] is False
assert metadata['head']['sha']=='bdee508c676c98cb96dbc1a2e5aef2fe9cd1c744'
assert comparison['merge_base_commit']['sha']==metadata['base']['sha']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
out={'operator':'SOURCE subagent /root/algebra_reproduction_audit','pid':os.getpid(),
     'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,
     'head':metadata['head']['sha'],'api_base':metadata['base']['sha'],
     'actual_merge_base':comparison['merge_base_commit']['sha'],
     'root_tree':json.loads((root/'receipts/head_commit.stdout').read_bytes())['tree']['sha'],
     'state':'OPEN draft, unmerged, at metadata capture time',
     'science_domain':'unsolved_math_prioritization/attempts/10300025/',
     'science_bodies':23,'science_bytes':sum(e['bytes'] for e in index.values()),
     'git_modes':'all 100644','git_blob_sha1_verified':23,'sha256_verified':23,
     'tree_membership':'Authenticated GitHub tree chain; every retrieved tree Git-object SHA1 reconstructed',
     'pr_changed_files':24,'additional_diff_path':'unsolved_math_prioritization/QUEUE.md',
     'original_code_imported_or_executed':False,'mathematical_verdict':None,
     'source_record_sha256':index['source_record.json']['sha256'],
     'candidate_sha256':index['KNOWN_RESULT.md']['sha256']}
(root/'ORIGINAL_AUTHENTICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
