"""Publish exact owned closed evidence; exclude active work and foreign bodies."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_publication_program_20260930';A=P/'audits'
owned=set();closures=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def add(p):
 assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
 owned.add(p.relative_to(R).as_posix())
def manifest(rel,pin):
 p=A/rel;raw=p.read_bytes();assert sha(raw)==pin;m=json.loads(raw);names=[]
 for z in m['files']:
  n=z['path'];assert not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
  f=p.parent/n;b=f.read_bytes();assert type(z.get('bytes',z.get('size'))) is int and len(b)==z.get('bytes',z.get('size')) and sha(b)==z['sha256'];add(f);names.append(n)
 assert len(names)==len(set(names));add(p);closures.append(dict(path=rel,sha256=pin,members=len(names)))
assert git('branch','--show-current').strip()==b'main'
assert git('rev-parse','HEAD').strip()==b'efd29c05204703acca9a0860812f54b94fae54b1'
assert not git('diff','--cached','--name-only').strip()
for rel,pin in [
 ('pr39_9500008/acceptance_static_adversary_family/MANIFEST.json','c782c65b31ef0f38c14bcf49577d11b66b8e19b63b0cce83718f651b3d6f0c9a'),
 ('pr39_9500008/acceptance_execution_preparation_family/integration_source_revision/PREPARATION_MANIFEST.json','522cf5062ffcb1aa9c60cb0054063b0f2801378446f2288d7f85e81ee9a70ae7'),
 ('pr39_9500008/acceptance_revised_static_adversary_family/MANIFEST.json','70659d55353c2fd7f3e44f327ff35bdbbd742d31a6d12b9dcc40da6cd850b508'),
 ('pr40_2814/acceptance_static_adversary_family/FIRST_PARTY_MANIFEST.json','84b0e1c5364fac20617c1242e36c0d5b9130ea2784de81d3557ae8cbe94ab526'),
 ('pr40_2814/acceptance_execution_preparation_family/integration_source_revision/PREPARATION_MANIFEST.json','65e71adae289b4243036f50be90b28bdeadca3dbd3fd99c5dfc605a72e053c0e'),
 ('pr41_9700035/primary_scope_family/FIRST_PARTY_MANIFEST.json','7d8318e0b7f7009ead1e19ae8c58008139da96c1b35ecfbbdf9fbe109ec830a8'),
 ('pr41_9700035/root_family_controls_actual_reproduction/MANIFEST.json','35f6efc31439e33795820b19d6df7a49451f649e6ccd71fac71956b4d0556840')]:manifest(rel,pin)
for n in ['ROOT_REVISED_ACCEPTANCE_SOURCE_REVIEW.json','ROOT_RESEARCH_LOG.md']:add(A/'pr39_9500008'/n)
add(A/'pr40_2814/ROOT_RESEARCH_LOG.md')
for n in ['ROOT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_CLOSED_FAMILY_INSPECTION.json','inspect_closed_evidence.py','capture_closed_evidence_inspection.py','reproduce_family_controls.py','ROOT_RESEARCH_LOG.md']:
 add(A/'pr41_9700035'/n)
for folder in ['root_closed_inspection_setup_failure','root_closed_evidence_inspection_actual_capture']:
 for f in (A/'pr41_9700035'/folder).rglob('*'):
  if f.is_file():add(f)
add(P/'RESEARCH_LOG.md');add(Path(__file__).resolve())
now=dt.datetime.now(dt.timezone.utc).isoformat()
notes={
 'pr39_9500008':'Acceptance97%; full target unsolved, exact random-origin discovery0%. Revised17+self acceptance source522cf506 and NEW independent15+self static review70659d55 are clean; root full five-source/contract reading and exact four-closure checks complete. Actual final sealer/integration pending. Original2/5,new0/audit0; original source/packages/science preserved.',
 'pr40_2814':'Acceptance94%; sourcehold partial valid, project discovery0%. Original12+self source and22+self defect audit preserved; separate15+self65e71ada source repairs six attribution/clock/capture/write/rebase/next-target issues. Fresh independent static rereview still active, excluded. Original13/current239/SOURCE_STATUS unchanged;0/5,new0/audit0.',
 'pr41_9700035':'Scientific review75%, full original discovery0%. Both closed independent families127/115 and root actual130/15 exact file/directory/whole byte/95JSON checks passed PID29333 exit0. Root211/3809 and1326/122 actual full results preserved. Earlier own inspector author-only field overrequirement retained with actual tool failure/null PID, fixed without scientific rerun. Complete mathematical certificate/read ledger published; source-only current prep and NEW source-first whole reviewer active, excluded. Original2/5,new0/audit0; conditional law only, full unconditional exterior gap remains open.'}
for folder,note in notes.items():
 with (A/folder/'ROOT_RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — '+note+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Program28/180=15.5556%; PR18/20 evidence holds preserved. '+' '.join(notes.values())+' No partial papers/newDOIs/tracker/release/outreach.\n')
records=[dict(path=n,bytes=len((R/n).read_bytes()),sha256=sha((R/n).read_bytes())) for n in sorted(owned)]
out=P/'checkpoints/CHECKPOINT_20261002_2137.json'
with out.open('x') as f:json.dump(dict(utc=now,head_before=git('rev-parse','HEAD').decode().strip(),completed=28,total=180,completion_percent=28/180*100,closed_manifests=closures,exact_owned_files=records,excluded='All active PR40 revised review, PR41 current prep/whole reviewer, root39 runner preparation, all foreign PDF/text/HTML/image/cache bodies, and both unrelated tracked referee logs.'),f,indent=2);f.write('\n')
add(out);names=sorted(owned)
for i in range(0,len(names),100):git('add','-f','--',*names[i:i+100])
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n};assert staged<=owned
pins={z['path']:z for z in records}
for n in staged:
 if n in pins:assert len((R/n).read_bytes())==pins[n]['bytes'] and sha((R/n).read_bytes())==pins[n]['sha256']
checked=0
for entry in git('ls-files','--stage','-z').split(b'\0'):
 if not entry:continue
 meta,literal=entry.split(b'\t',1);n=literal.decode()
 if n not in staged:continue
 mode,oid,stage=meta.split();assert mode in (b'100644',b'100755') and stage==b'0'
 b=(R/n).read_bytes();assert oid.decode()==hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest();checked+=1
assert checked==len(staged)
print(json.dumps(dict(status='EXACT_OWNED_CHECKPOINT_STAGED',members=len(staged),bytes=sum(len((R/n).read_bytes()) for n in staged),completion_percent=28/180*100)))
