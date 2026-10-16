#!/usr/bin/env python3
"""Publish owned closed evidence only; active reviews and all foreign caches excluded."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_publication_program_20260930';A=P/'audits'
owned=set();closed=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def add(path):
 assert path.is_file() and not path.is_symlink() and not any(q.is_symlink() for q in path.parents)
 owned.add(path.relative_to(R).as_posix())
def manifest(path,expected):
 raw=path.read_bytes();assert sha(raw)==expected
 obj=json.loads(raw);rows=obj['files'];assert type(rows) is list
 names=[]
 for row in rows:
  name=row['path'];assert not name.startswith('/') and all(p not in ('','.','..') for p in name.split('/'))
  q=path.parent/name;data=q.read_bytes();assert len(data)==row.get('bytes',row.get('size')) and sha(data)==row['sha256'];names.append(name);add(q)
 assert len(names)==len(set(names));add(path)
 closed.append(dict(path=path.relative_to(R).as_posix(),members=len(rows),sha256=expected))
assert git('branch','--show-current').strip()==b'main'
assert not git('diff','--cached','--name-only').strip()
assert git('rev-parse','HEAD').strip()==b'33a08009b078d43c4e560c144cf75361bd0f4c0a'
manifest(A/'pr39_9500008/acceptance_preparation_family/PREPARATION_MANIFEST.json','f66df61cb4b57ae63cc007fed3c4dabf9e67e027f1d428d4e0ffbc75a6332fca')
manifest(A/'pr40_2814/acceptance_preparation_family/PREPARATION_MANIFEST.json','a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b')
manifest(A/'pr41_9700035/network_tail_measure_family/FIRST_PARTY_MANIFEST.json','1b99b3ad334b970985ed3ba5f11d113fc4ed77793f7922b7b0142479821b750d')
manifest(A/'pr41_9700035/root_original_actual_reproduction/MANIFEST.json','d8fb8a576676a690f9cb365f426bf3f344780bc1d03fbdc02f8534a44f3487f7')
for name in ('inspect_acceptance_preparation.py','ROOT_ACCEPTANCE_PREPARATION_INSPECTION.json','execute_root_acceptance.py','ROOT_RESEARCH_LOG.md'):
 add(A/'pr39_9500008'/name)
add(A/'pr40_2814/ROOT_RESEARCH_LOG.md')
for name in ('ROOT_PRIMARY_ACQUISITION.json','ROOT_PARTIAL_SCOPE_CERTIFICATE.md','reproduce_original_checks.py','ROOT_RESEARCH_LOG.md'):
 add(A/'pr41_9700035'/name)
add(P/'RESEARCH_LOG.md');add(Path(__file__).resolve())
now=dt.datetime.now(dt.timezone.utc).isoformat()
notes={
 'pr39_9500008':'Acceptance about96%, scientific current/whole review clean. Source-only preparation closed15+self f66df61c and independent root byte/type/closure check6022unique/133844737bytes/14exactnegative inputs passed. New static adversary identified exclusive-file publication race and capture clock/name validation qualifications; adjacent repair is pending, originals untouched and no actual sealer or merge run. Original2/5,new0/audit0; full exact random-origin discovery0%.',
 'pr40_2814':'Acceptance about94%, mathematical sourcehold current/whole review clean. Closed12+self a7bbde5e acceptance preparation remains source-only. New static adversary caught wrong attribution of nonorientable cusp coverage to Kuhlmann instead of Xia; scoped source revision and complete re-review required before execution. Original13/SOURCE_STATUS/current239 and imported fullproof qualifications unchanged. Original0/5,new0/audit0; no project full theorem/novelty or paper.',
 'pr41_9700035':'Audit about65%, root independently reconstructed entire interior/dePoisson/exterior/ordered-tail proof and read operative primary sources. Conditional partial passes; full unconditional discovery0%. Original211 and3809 unchanged-helper checks actually reproduced with entire saved/actual JSON objects equal; full16/17/raw149MB/all15458SQL/presentprior data replay passed. Root130+self d8fb8a57 records real3outer runs/source/streams/PIDs/clocks; original16/main/native13 unchanged. Network-measure independent115+self closed1b99b3ad with122ownchecks/fourcorruption rejections/tenmanifest rejects. Primary family/currentpreparation stillactive and excluded. Kahn printed-proof qualifications repaired analytically without promoting model imports or adding research turns. Original2/5,new0/audit0; no paper/DOI.'}
for folder,note in notes.items():
 with (A/folder/'ROOT_RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — '+note+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Program28/180=15.5556% accepted; PR18/20 evidence holds preserved. '+' '.join(notes.values())+'\n')
records=[dict(path=n,bytes=len((R/n).read_bytes()),sha256=sha((R/n).read_bytes())) for n in sorted(owned)]
output=P/'checkpoints/CHECKPOINT_20261002_1330.json';assert not output.exists()
output.write_text(json.dumps(dict(utc=now,head_before=git('rev-parse','HEAD').decode().strip(),accepted=28,total=180,completion_percent=28/180*100,
 closed_manifests=closed,exact_owned_files=records,
 excluded='All active39/40static reviews and future revisions; active41primary/currentprep; all foreign primary PDFs/text/images/HTML/caches/private fixtures and both unrelated tracked referee logs.'),indent=2)+'\n');add(output)
names=sorted(owned)
for i in range(0,len(names),100):git('add','-f','--',*names[i:i+100])
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n};assert staged<=owned
pins={x['path']:x for x in records}
for name in staged:
 assert not name.startswith('paper_ii_simultaneous_amplification_referee_audit_2026-08-22/')
 if name in pins:assert len((R/name).read_bytes())==pins[name]['bytes'] and sha((R/name).read_bytes())==pins[name]['sha256']
checked=0
for entry in git('ls-files','--stage','-z').split(b'\0'):
 if not entry:continue
 metadata,literal=entry.split(b'\t',1);name=literal.decode()
 if name not in staged:continue
 mode,oid,stage=metadata.split();assert mode in (b'100644',b'100755') and stage==b'0'
 raw=(R/name).read_bytes();assert oid.decode()==hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest();checked+=1
assert checked==len(staged)
print(json.dumps(dict(status='EXACT_OWNED_CHECKPOINT_STAGED',owned=len(owned),staged=len(staged),bytes=sum(len((R/n).read_bytes()) for n in staged),accepted=28,completion_percent=28/180*100)))
