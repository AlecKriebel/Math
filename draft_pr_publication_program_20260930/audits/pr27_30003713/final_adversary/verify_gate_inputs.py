"""Read-only hash/closure verification of the exact input to this gate."""
from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;A=P.parent;R=P.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
cur=A/'reviewed_candidate';mbytes=(cur/'MANIFEST.json').read_bytes()
assert sha(mbytes)=='2bb662fe662ac51380e57ecb03a8b404591ba7761d7e57cd6f6dab7520ec2a69'
m=json.loads(mbytes)
assert len(m['files'])==22
for x in m['files']:
 b=(cur/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
assert {x['path'] for x in m['files']}=={x.relative_to(cur).as_posix() for x in cur.rglob('*') if x.is_file() and x.name!='MANIFEST.json'}
d=json.loads((cur/'CURRENT_PROOF_DEPENDENCIES.json').read_text());assert len(d['supporting_first_party_files'])==65
for x in d['supporting_first_party_files']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
for family,manifest in [('character_family','artifact_manifest.json'),('homological_family','FIRST_PARTY_SHA256_MANIFEST.json'),('primary_scope_family','FIRST_PARTY_SHA256_MANIFEST.json')]:
 F=A/family;v=json.loads((F/manifest).read_text());rows=[{'path':k,**z} for k,z in v['artifacts'].items()] if 'artifacts' in v else v['files']
 excluded={'tmp','tmp_sources','tmp_replay','__pycache__'}
 assert {z['path'] for z in rows}=={x.relative_to(F).as_posix() for x in F.rglob('*') if x.is_file() and x.name!=manifest and not set(x.relative_to(F).parts)&excluded}
 for z in rows:
  b=(F/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
frozen=json.loads((A/'snapshot_manifest.json').read_text());assert len(frozen['files'])==13
for x in frozen['files']:
 b=subprocess.check_output(['git','show',frozen['head']+':unsolved_math_prioritization/attempts/30003713/'+x['path']],cwd=R)
 assert b==(A/'source_snapshot'/x['path']).read_bytes() and sha(b)==x['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob_sha1']
assert subprocess.check_output(['git','diff','--name-only',frozen['actual_merge_base'],frozen['head']],cwd=R).decode().splitlines()==frozen['changed_paths']
assert len(frozen['changed_paths'])==14
print('PASS: exact22/currentmanifest,65support,54closedfamily,13originalGit and14changedpaths')
