"""Checkpoint closed owned PR40 acceptance and PR41/42 audit evidence only."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_publication_program_20260930';A=P/'audits'
owned=set();closures=[];excluded=[]
def H(b):return hashlib.sha256(b).hexdigest()
def J(p):return json.loads(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def add(p,z=None):
    assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    if z is not None:
        b=p.read_bytes();assert type(z.get('bytes',z.get('size'))) is int and len(b)==z.get('bytes',z.get('size')) and H(b)==z['sha256'],str(p)
    owned.add(p.relative_to(R).as_posix())
def tree(p):
    for f in p.rglob('*'):
        assert not f.is_symlink()
        if f.is_file():add(f)
def manifest(p,pin):
    assert H(p.read_bytes())==pin;m=J(p);names=set()
    for z in m['files']:
        n=z['path'];assert n not in names and not n.startswith('/') and not set(n.split('/'))&{'','.','..'};names.add(n);add(p.parent/n,z)
    add(p);closures.append(dict(path=p.relative_to(R).as_posix(),sha256=pin,members=len(names)))
assert git('branch','--show-current').strip()==b'main'
assert git('rev-parse','HEAD').strip()==b'c44e1c83bd4aecc588bbc58ea14207e1275c7dd7'
assert not git('diff','--cached','--name-only').strip()
post=J(A/'pr40_2814/ROOT_ACTUAL_POST_INSPECTION.json');assert post['status']=='PASS' and post['actual_post_pid']==1567 and post['completed_primary_prs']==30
manifest(R/'unsolved_math_prioritization/attempts/2814/MANIFEST.json','2da4b4f1ae2610bc173b73e189a28af948fcc97cb409529fd68f215be5e30d09')
manifest(A/'pr40_2814/final_evidence_reconciliation/FINAL_MANIFEST.json','1ddda54331a71005754b1291f1ba84c0689f7b8c36bd601ba4624b735ed0f968')
for f in (A/'pr40_2814').iterdir():
    if f.is_file():add(f)
    elif f.name.startswith('root_') and f.name.endswith('_actual_capture'):tree(f)
for f in (A/'pr39_9500008').iterdir():
    if f.is_dir() and ((f.name.startswith('root_pr40_') and f.name.endswith('_actual_capture')) or f.name=='root_checkpoint_2234_push_actual_capture'):tree(f)
for name in ['integration_log_preimages']:
    if (A/'pr40_2814'/name).exists():tree(A/'pr40_2814'/name)
manifest(A/'pr41_9700035/acceptance_preparation_family/PREPARATION_MANIFEST.json','6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc')
manifest(A/'pr41_9700035/acceptance_static_adversary_family/FIRST_PARTY_MANIFEST.json','31c82a50855cf621859d6bfa182541ec07d77a3727d621ce4adc99597620c6c0')
Z=A/'pr42_2233'
manifest(Z/'current_preparation_family/PREPARATION_MANIFEST.json','af4f28f77df2b7541b099a47fb89a5a454dda5a64272be6e9b70254d17b5c5fa')
pins=J(Z/'current_preparation_family/INPUT_PINS.json')
for info in pins['retained_closures']:
    for z in info['files']:add(Z/info['directory']/z['path'],z)
for z in pins['auxiliary']:add(Z/z['path'],z)
snapshot=J(Z/'snapshot_manifest_v2.json')
for z in snapshot['files']:add(Z/'source_snapshot_v2'/z['path'],z)
add(Z/'snapshot_manifest_v2.json')
for name in ['ROOT_CLOSED_FAMILIES_INSPECTION.json','ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','inspect_closed_families.py','capture_root_command.py']:add(Z/name)
tree(Z/'root_closed_families_inspection_actual_capture')
L=Z/'literal_geometry_family';lp='ad900516fdf42696ecfdc29f4e8c775fffa13ae7f49239e2127d8c46e381daae'
assert H((L/'final_seal.json').read_bytes())==lp;lm=J(L/'final_seal.json')
for z in lm['first_party_closed_files']:
    if z['path']=='controls/primary_pdf_extract.stdout.txt':excluded.append(dict(path=(L/z['path']).relative_to(R).as_posix(),sha256=z['sha256'],reason='Full foreign PDF text derivative; individually retained but excluded from first-party checkpoint'));continue
    add(L/z['path'],z)
add(L/'final_seal.json');closures.append(dict(path=(L/'final_seal.json').relative_to(R).as_posix(),sha256=lp,owned_nonself_members=54,individually_excluded_foreign_and_derivative_members=26))
E=Z/'exact_spectrum_family';ep='8817acbf2645b271cf9e28e553de30344648eb4192bbbe075e569a93e1bf387a'
assert H((E/'OWN_CLOSED_MANIFEST.json').read_bytes())==ep;em=J(E/'OWN_CLOSED_MANIFEST.json')
for z in em['own_files_including_self']:
    p=Path(z['path']);assert p.is_relative_to(E)
    if p.name=='OWN_CLOSED_MANIFEST.json':assert z['bytes'] is None and z['sha256'] is None;add(p)
    else:add(p,z)
closures.append(dict(path=(E/'OWN_CLOSED_MANIFEST.json').relative_to(R).as_posix(),sha256=ep,owned_including_self=42,individual_foreign_local_exclusions=5))
now=dt.datetime.now(dt.timezone.utc).isoformat()
note=now+' — PR40 acceptance100%, discovery0%, actual original-head MERGEDc44e1c83 and final child86903/post1567/ROOTpost9358 PASS; entire247canonical0444/current239/dependencies216/native31targets37turns30primary/wholeprior30states/historyprefix preserved. Original0/5,new0/audit0; source-hold qualified partial; no paper/newDOI/tracker. Program30/180=16.6667%. PR41 current math/whole valid; NEW acceptance adversary31c82a found3 finite administrative source gaps, repairV2 active/excluded, original2/5/new0. PR42 independent families and ROOToriginal current18306/reviewed18306/independent1263 complete actual replaysPASS, whole149266659raw/15458SQL and absent-prior fallback verified; scoped construction lemmas accepted, fullEP653unsolved/discovery0%, workflow65%, original2/5/new0/audit0. Current preparation21closed/sourceauditor active/excluded. PR18/20 evidence holds preserved. No outside human contact.\n'
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+note)
with (A/'pr40_2814/ROOT_RESEARCH_LOG.md').open('a') as f:f.write('\n'+note)
with (Z/'ROOT_RESEARCH_LOG.md').open('x') as f:f.write(note)
add(P/'RESEARCH_LOG.md');add(A/'pr40_2814/ROOT_RESEARCH_LOG.md');add(Z/'ROOT_RESEARCH_LOG.md')
for n in ['state.json','history.jsonl']:add(R/'unsolved_math_prioritization'/n)
add(P/'inventory.json');add(Path(__file__).resolve())
records=[dict(path=n,bytes=len((R/n).read_bytes()),sha256=H((R/n).read_bytes())) for n in sorted(owned)]
out=P/'checkpoints/CHECKPOINT_20261002_2310.json'
with out.open('x') as f:json.dump(dict(utc=now,head_before=git('rev-parse','HEAD').decode().strip(),completed=30,total=180,completion_percent=30/180*100,closed_manifests=closures,exact_owned_files=records,individual_derivative_exclusions=excluded,excluded='Both unrelated tracked referee logs; active PR41 V2 and active PR42 source adversary; all individual foreign source/cache/media bodies. The pinned original PR42 RESEARCH_LOG.md is unchanged. Closure metadata preserves intentional empty directories that Git cannot represent.'),f,indent=2);f.write('\n')
add(out)
names=sorted(owned)
for i in range(0,len(names),100):git('add','-f','--',*names[i:i+100])
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n};assert staged<=owned
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if not entry:continue
    meta,name=entry.split(b'\t',1);n=name.decode()
    if n not in staged:continue
    mode,oid,stage=meta.split();assert stage==b'0' and mode in (b'100644',b'100755')
    b=(R/n).read_bytes();assert oid.decode()==hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
assert all(not n.startswith('paper_ii_') for n in staged)
print(json.dumps(dict(status='EXACT_OWNED_CHECKPOINT_STAGED',members=len(staged),bytes=sum(len((R/n).read_bytes()) for n in staged),completion_percent=30/180*100)))
