#!/usr/bin/env python3
"""Checkpoint completed first-party evidence only, preserving shared foreign work."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
P=Path(__file__).absolute().parents[1]
R=P.parent
names=set()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def git(*argv):
    return subprocess.check_output(['git',*argv],cwd=R)

def add(p):
    assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    assert p.stat().st_size<100*1024*1024
    assert p.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.webp','.gif','.db'}
    if p.suffix=='.sqlite':
        assert p.read_bytes()==b'private\n'
    names.add(p.relative_to(R).as_posix())

def tree(d):
    assert d.is_dir() and not d.is_symlink()
    for p in d.rglob('*'):
        assert not p.is_symlink()
        if p.is_file(): add(p)

def closed(d,n):
    m=json.loads((d/n).read_bytes())
    for r in m['files']:
        p=d/r['path']; b=p.read_bytes()
        assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
        if r.get('publication_allowed',True) is True: add(p)
    add(d/n)

assert git('branch','--show-current')==b'main\n' and not git('diff','--cached','--name-only')
head=git('rev-parse','HEAD').decode().strip()
old=json.loads((P/'checkpoints/CHECKPOINT_20261003_0441.json').read_bytes())
A45=P/'audits/pr45_9900007'
A46=P/'audits/pr46_30004438'
A47=P/'audits/pr47_2849'
A48=P/'audits/pr48_2961'
# Restrict A45 to already explicitly reviewed ownership and completed ROOT siblings.
for r in old['owned_files']:
    if r['path'].startswith(A45.relative_to(R).as_posix()+'/'): add(R/r['path'])
for p in A45.iterdir():
    if p.is_file() and (p.name.startswith('ROOT_') or p.name.startswith('capture_')): add(p)
    if p.is_dir() and p.name.startswith('root_'): tree(p)
# These two roots contain closed first-party corpora; active reviewer subtrees are excluded.
for a,excluded in [(A46,{'current_whole_adversary_family'}),(A47,{'current_source_adversary_family'})]:
    for p in a.iterdir():
        if p.name in excluded: continue
        if p.is_file(): add(p)
        elif p.is_dir(): tree(p)
# Enforce all newly completed scientific/self-only closures before publication.
for d,n in [
    (A46/'current_preparation_family_v2','PREPARATION_MANIFEST.json'),
    (A46/'current_source_adversary_family_v2','MANIFEST.json'),
    (A46/'reviewed_candidate','MANIFEST.json'),
    (A47/'cover_algebra_family','SELF_MANIFEST.json'),
    (A47/'gauge_geometry_family','SELF_MANIFEST.json'),
    (A47/'root_original_actual_reproduction','MANIFEST.json'),
    (A47/'current_preparation_family','PREPARATION_MANIFEST.json'),
    (A48,'ORIGINAL_PREPARATION_MANIFEST.json')]: closed(d,n)
tree(A48/'original_preparation_closure_actual_capture')
add(A48/'capture_ROOT_original_closure.py')
for p in (P/'checkpoints').iterdir():
    if p.is_file(): add(p)
add(P/'inventory.json')
utc=dt.datetime.now(dt.timezone.utc).isoformat()
note='\n'+utc+' — Completed-evidence checkpoint:35/180=19.444444444444446%, current46. PR46 known-result math/original reproduction complete; V2 SOURCE123files closure10748 repaired false inner-afterexit chronology, new independent SOURCE190files closure80723 and ROOTpostread83132 PASS29095private controls627full bodies; ROOTauthor85337 trueboundedprerequisites, actualfreeze85728 under85727 exit0; reviewed946+self/142dirs SHA66239699390b279235c4064208e63134049a5804884818de9176d377476a189d; ROOT90961 complete45finalinnercommands/fullstreams (43frozenprefix),826dependencies/stable9/native4proposal PASS. Different whole-current adversary active, futureacceptancepending. PR47 mathcover144files/gauge72files and ROOT220files complete; actualknownSU2abelianSeifertdegeneracy falsifies universal normalH1vanishingroute, corrected operativeglobalpresentations close route and retainactualFloergap; SOURCE157+self actualROOTclosure87649 exit0, allROOTapprovalsfalse/null, freshSOURCEadversaryactive. ROOT unchanged114/duplicate114/100 controls/fullraw15458rows verified; targetunsolved1/5,new0audit0. PR48 original575files plus sixexternal actualROOTclosure87065/87064 all444,17science/18pathactualmergebase60292...,2/5JSONL, sourcesbothABSENT{}fallback/no priorfile; independent algebra/cocycle and smoothgeometry families active. Activefamilies/foreignPDFtextpixels/cacheSQLactualbodies/index/mainotherchatchanges excluded. No newpaperDOItrackerreleaseoroutreach.\n'
for p in [P/'RESEARCH_LOG.md',A46/'ROOT_RESEARCH_LOG.md',A47/'ROOT_RESEARCH_LOG.md']:
    with p.open('a') as h:
        h.write(note); h.flush(); os.fsync(h.fileno())
    add(p)
foreign=[]
for n in git('diff','--name-only','-z').decode().split('\0'):
    if n and n not in names:
        p=R/n; b=p.read_bytes(); foreign.append(dict(path=n,bytes=len(b),sha256=sha(b)))
rows=[]
for n in sorted(names):
    p=R/n; b=p.read_bytes(); rows.append(dict(path=n,bytes=len(b),sha256=sha(b),observed_full_mode=stat.S_IMODE(p.stat().st_mode)))
cp=P/'checkpoints/CHECKPOINT_20261003_0524.json'
with cp.open('x') as h:
    json.dump(dict(schema='ROOT_exact_completed_owned_checkpoint/v2',utc=utc,actual_pid=os.getpid(),main_before=head,
        owned_files=rows,foreign_dirty_before=foreign,foreign_bodies_included=False,active_families_included=False,
        completed_count=35,current_pr=46,total=180,completion_estimate_percent=35/180*100),h,indent=2); h.write('\n')
add(cp)
assert git('rev-parse','HEAD').decode().strip()==head
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(names)),check=True)
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}
assert staged<=names and not staged&{r['path'] for r in foreign}
entries={}
for line in git('ls-files','--stage','-z').decode().split('\0'):
    if line:
        info,n=line.split('\t'); mode,oid,stage=info.split()
        if n in staged:
            assert stage=='0' and mode in {'100644','100755'}; entries[n]=(mode,oid)
assert set(entries)==staged
ordered=sorted(staged)
child=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
data,err=child.communicate(b''.join((entries[n][1]+'\n').encode() for n in ordered))
assert child.returncode==0 and not err
offset=0
for n in ordered:
    end=data.index(b'\n',offset); oid,kind,size=data[offset:end].decode().split()
    assert oid==entries[n][1] and kind=='blob'
    count=int(size); start=end+1; body=data[start:start+count]
    assert data[start+count:start+count+1]==b'\n' and body==(R/n).read_bytes()
    offset=start+count+1
assert offset==len(data) and git('rev-parse','HEAD').decode().strip()==head
print(json.dumps(dict(status='PASS_EXACT_COMPLETED_CHECKPOINT_STDIN_STAGE',main_before=head,actual_pid=os.getpid(),owned=len(names),staged=len(staged),actual_blob_batch_pid=child.pid,all_staged_bodies_and_exact_scope_verified=True,foreign_staged=0,active_families_staged=False,completed=35,total=180,completion_percent=35/180*100)))
