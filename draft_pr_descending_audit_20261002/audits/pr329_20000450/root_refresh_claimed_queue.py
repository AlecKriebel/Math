"""After clean review, refresh only PR329 using immutable objects; keep main checkout."""
import os, subprocess, time
from pathlib import Path
from root_submission_gate import *

window();clear=current_clearance()
assert not (A/'queue_repair_receipt.json').exists()
assert not (A/'BRANCH_REFRESH_ATTEMPT.json').exists(),'Inspect any prior uncertain branch mutation before retry.'
cap=Capture('branch_refresh')
assert cap.git('branch','--show-current')==b'main\n'
assert not cap.git('diff','--cached','--raw','-z')
assert cap.run('no_active_merge',['git','rev-parse','-q','--verify','MERGE_HEAD'],ok=(1,)).returncode==1
index=Path(cap.git('rev-parse','--git-path','index').decode().strip())
if not index.is_absolute():index=R/index
index_before=index.read_bytes();local=cap.git('rev-parse','HEAD').decode().strip()
def dirty():
    out={}
    for n in cap.git('diff','--name-only','-z').split(b'\0'):
        if n:
            p=R/n.decode();out[n.decode()]=(p.exists(),p.read_bytes() if p.is_file() else None,p.stat().st_mode&0o7777 if p.exists() else None)
    return out
dirty_before=dirty()
pr=json.loads(cap.run('pr_before',['gh','pr','view','329','--json','state,isDraft,headRefOid,headRefName']).stdout)
assert pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==ORIGINAL_HEAD and pr['headRefName']==BRANCH
window();cap.run('main_fetch',['git','fetch','origin','main'])
base=cap.git('rev-parse','origin/main').decode().strip();assert base==local
original=load(A/'snapshot_manifest.json');assert original['head']==ORIGINAL_HEAD and len(original['files'])==22
for e in original['files']:
    b=cap.git('show',ORIGINAL_HEAD+':'+e['path']);assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert cap.git('ls-tree',ORIGINAL_HEAD,'--',e['path']).split(b'\t',1)[0].split()==[b'100644',b'blob',e['git_blob_sha'].encode()]
def ownrow(lines):
    found=[i for i,b in enumerate(lines) if len(b.split(b'|'))>11 and b.split(b'|')[2].strip().split(b' / ')[0]==b'20000450']
    assert len(found)==1;return found[0]
frozen=cap.git('show',ORIGINAL_HEAD+':'+QUEUE).splitlines(keepends=True)
fc=frozen[ownrow(frozen)].split(b'|');assert [fc[j].strip() for j in (8,9)]==[b'claimed_solved',b'1/5']
raw=cap.git('show',base+':'+QUEUE);lines=raw.splitlines(keepends=True);i=ownrow(lines);before=lines[i];cells=before.split(b'|')
assert [cells[j].strip() for j in (8,9)]==[b'queued',b'0/5']
for j in (8,9):cells[j]=fc[j]
cells[11]=b' '+cells[11].strip()+b' Accepted exact full 25-point fifth-torsion and division-field computation for the specified regular-pentagon pencil over Q(sqrt(5)); research note and verification package ready after successive new full AI reviews and global source-attribution repair. Classical Fisher/Verdure/Morton inputs credited; bounded priority, unrefereed. '
assert [j for j,(a,b) in enumerate(zip(before.split(b'|'),cells)) if a!=b]==[8,9,11]
lines[i]=b'|'.join(cells);new=b''.join(lines)
tree=cap.git('show','-s','--format=%T',base).decode().strip()
def replace(t,parts,blob):
    entries={}
    for item in cap.git('ls-tree','-z',t).split(b'\0'):
        if item:
            meta,name=item.split(b'\t',1);entries[name]=tuple(meta.split())
    name=parts[0].encode();prior=entries.get(name)
    if len(parts)==1:
        if prior:assert prior[:2]==(b'100644',b'blob')
        entries[name]=(b'100644',b'blob',blob.encode())
    else:
        if prior:assert prior[:2]==(b'040000',b'tree');child=prior[2].decode()
        else:child=cap.git('mktree','-z',input=b'').decode().strip()
        entries[name]=(b'040000',b'tree',replace(child,parts[1:],blob).encode())
    window()
    return cap.git('mktree','-z',input=b''.join(b' '.join(entries[n])+b'\t'+n+b'\0' for n in sorted(entries))).decode().strip()
for e in original['files']:
    if e['path']!=QUEUE:
        assert not cap.git('ls-tree',base,'--',e['path']),'Original attempt already present: independently reconcile current state.'
        tree=replace(tree,e['path'].split('/'),e['git_blob_sha'])
window();queue_blob=cap.git('hash-object','-w','--stdin',input=new).decode().strip()
tree=replace(tree,QUEUE.split('/'),queue_blob)
release=(
    '# Verified research note for McCallum Question 17 / 20000450\n\n'
    'The accepted result gives all 25 geometric fifth-torsion points and the full division field of the explicitly normalized regular-pentagon quintic pencil, with origin [0:1:0], over K=Q(sqrt(5)). It proves the exact elliptic range, both birational maps, a residual degree-ten polynomial, both ordinate branches, all nonsingular specialization cases, splitting degrees and Galois action. The allowed cuspidal plane member is included through its smooth normalization.\n\n'
    'The original source already identifies the infinity subgroup and leaves ground field, scaling and origin unspecified. The note fixes those choices. It does not claim to resolve nonregular or star-polygon variants, arbitrary torsors, local-solubility or Tate-Shafarevich constructions. The universal Tate formulas, full-level modular cover, full-torsion specialization criterion and radical coordinates are credited to Fisher, Verdure and Morton. The contribution is the explicit bridge from this specified plane pencil to the classical family and its resulting complete computation. The bounded priority audit does not certify first discovery, first application or worldwide continuing openness.\n\n'
    'Independent mathematical approach families and successive NEW whole-preprint adversaries were used. The first review found a minor source-attribution error; the current paper and matching priority prose were repaired globally, the PDF and archive rebuilt and reverified. The final new full reviewer closed with no unresolved findings and its independent computations were reproduced by the root reviewer. Historical adverse records and original author history remain preserved. AI tools were used extensively; this is an unrefereed preprint without independent external human peer review or proof-assistant certification.\n\n'
    'All 21 original attempt files are byte-identical to submitted head '+ORIGINAL_HEAD+'. The author turn count remains 1/5. The current cleared package has 50 payload files plus its manifest and includes eleven verification programs, four false mathematical variants and portable integrity/optimization controls. Production publication and tracker registration are recorded separately after successful execution.\n\n'
    'Author: Alec Kriebel, Independent researcher, ORCID 0009-0001-9320-500X. License: CC BY 4.0.\n\n'
    'Cleared formal artifacts:\n'+''.join('- '+n+': '+str(e['bytes'])+' bytes; SHA256 '+e['sha256']+'\n' for n,e in clear['formal_submission_files'].items())
).encode()
assert not cap.git('ls-tree',base,'--',RELEASE)
window();release_blob=cap.git('hash-object','-w','--stdin',input=release).decode().strip();tree=replace(tree,RELEASE.split('/'),release_blob)
expected={e['path'] for e in original['files']}|{RELEASE};assert len(expected)==23
assert set(cap.git('diff','--name-only',base,tree).decode().splitlines())==expected
assert cap.git('show',tree+':'+QUEUE)==new
for e in original['files']:
    if e['path']!=QUEUE:
        b=cap.git('show',tree+':'+e['path']);assert len(b)==e['bytes'] and sha(b)==e['sha256']
for n,e in clear['formal_submission_files'].items():
    p=str((O/n).relative_to(R));b=cap.git('show',tree+':'+p)
    assert b==(O/n).read_bytes() and cap.git('show',base+':'+p)==b
current_clearance();assert cap.git('rev-parse','HEAD').decode().strip()==local and index.read_bytes()==index_before and dirty()==dirty_before
remote=json.loads(cap.run('main_before_push',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert remote['object']['sha']==base
window();commit=cap.git('commit-tree',tree,'-p',ORIGINAL_HEAD,'-p',base,
    input=b'Refresh PR329 on current main; preserve original mathematics and accept reviewed preprint\n').decode().strip()
(A/'BRANCH_REFRESH_ATTEMPT.json').write_text(json.dumps(dict(utc=utc(),original_head=ORIGINAL_HEAD,base=base,commit=commit,tree=tree,capture_directory=str(cap.directory)),indent=2)+'\n')
window();cap.run('branch_push',['git','push','origin',commit+':refs/heads/'+BRANCH])
assert cap.git('rev-parse','HEAD').decode().strip()==local and index.read_bytes()==index_before and dirty()==dirty_before
for j in range(6):
    after=json.loads(cap.run('pr_after_'+str(j),['gh','pr','view','329','--json','state,headRefOid,headRefName']).stdout)
    if after['headRefOid']==commit:break
    time.sleep(.5)
assert after['state']=='OPEN' and after['headRefOid']==commit and after['headRefName']==BRANCH
files=[];S=A/'repaired_snapshot';assert not S.exists()
for p in sorted(expected):
    b=cap.git('show',commit+':'+p);f=S/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b);f.chmod(0o644)
    meta=cap.git('ls-tree',commit,'--',p).split(b'\t',1)[0].split();assert meta[:2]==[b'100644',b'blob']
    files.append(dict(path=p,bytes=len(b),sha256=sha(b),git_blob_sha=meta[2].decode(),mode='100644'))
(A/'repaired_snapshot_manifest.json').write_text(json.dumps(dict(pr=329,head=commit,base=base,original_frozen_head=ORIGINAL_HEAD,utc=utc(),files=files),indent=2)+'\n')
receipt=dict(utc=utc(),status='PASS_CLAIMED_SOLVED_QUEUE_REFRESH',pr=329,original_head=ORIGINAL_HEAD,repaired_head=commit,base=base,tree=tree,parents=[ORIGINAL_HEAD,base],original21_unchanged=True,formal4_preexisting_exact=True,old_row=before.decode(),new_row=lines[i].decode(),queue_only_pipe_cells=[8,9,11],all_other_queue_bytes_preserved=True,main_checkout_index_dirty_bodies_modes_unchanged=True,nonforce_branch_push=True,capture_directory=str(cap.directory),workflow_percent=80)
(A/'queue_repair_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
