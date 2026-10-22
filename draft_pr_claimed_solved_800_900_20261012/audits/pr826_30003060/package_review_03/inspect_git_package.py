#!/usr/bin/env python3
"""Inspect actual immutable Git objects and all sealed bytes without writes to Git."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, stat, subprocess, zipfile
R=Path(__file__).resolve().parent;A=R.parent;C=A.parents[2]
S=json.loads((A/'PACKAGE_SEAL_R2.json').read_text());T=Path(S['assembly_tree']);P='unsolved_math_prioritization/attempts/30003060'
def need(c,m):
    if not c:raise RuntimeError(m)
def git(*args):return subprocess.check_output(['git',*args],cwd=C,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def sha(b):return hashlib.sha256(b).hexdigest()
def objects(commit,prefix):
    items=git('ls-tree','-r','-z',commit+':'+prefix).split(b'\0');items=[x for x in items if x]
    requests=[];modes={}
    for item in items:
        left,name=item.split(b'\t',1);mode,kind,oid=left.split();name=name.decode();need(kind==b'blob','nonblob');modes[name]=mode.decode();requests.append((name,oid.decode()))
    q=subprocess.run(['git','cat-file','--batch'],cwd=C,input=('\n'.join(oid for _,oid in requests)+'\n').encode(),capture_output=True,check=True)
    raw=q.stdout;offset=0;out={}
    for name,oid in requests:
        end=raw.index(b'\n',offset);head=raw[offset:end].split();n=int(head[2]);need(head[:2]==[oid.encode(),b'blob'],'batch identity');offset=end+1;out[name]=raw[offset:offset+n];offset+=n+1
    need(offset==len(raw),'batch extent');return out,modes
prepared,pm=objects(S['prepared_commit'],P);original,om=objects(S['original_head'],P)
need(len(prepared)==217 and len(original)==65,'Git counts')
assembled={p.relative_to(T).as_posix():p.read_bytes() for p in T.rglob('*') if p.is_file()}
need(prepared==assembled,'prepared tree equality');need(set(pm.values())=={'100644'},'prepared modes')
source=json.loads((A/'SOURCE_MANIFEST.json').read_text());inner=T/'publication_20261014/verification_package';pre=T/'publication_20261014/preprint'
for row in source['files']:
    b=original[row['path']];need(len(b)==row['bytes'] and sha(b)==row['sha256'],'original Git source pin');need(b==(A/'source'/row['path']).read_bytes()==(inner/'source'/row['path']).read_bytes(),'original source identity')
rawcommit=git('cat-file','-p',S['prepared_commit']).decode();parents=[s[7:] for s in rawcommit.splitlines() if s.startswith('parent ')]
receipt=json.loads((A/'PREPARED_GIT_BYTES_VALIDATION_R2.json').read_text());mainbase=receipt['main_base'];need(parents==[S['original_head'],mainbase],'prepared parents')
changed=git('diff-tree','--no-commit-id','--name-only','-r',mainbase,S['prepared_commit']).decode().splitlines();need(all(n.startswith(P+'/') or n=='unsolved_math_prioritization/QUEUE.md' for n in changed),'changed path scope')
before=git('show',mainbase+':unsolved_math_prioritization/QUEUE.md');after=git('show',S['prepared_commit']+':unsolved_math_prioritization/QUEUE.md')
is_target=lambda s:b'30003060' in s
brows=before.splitlines(keepends=True);arows=after.splitlines(keepends=True);target=[s for s in arows if is_target(s)];need(len(target)==1,'unique target queue row');need(b''.join(s for s in brows if not is_target(s))==b''.join(s for s in arows if not is_target(s)),'all other queue bytes')
need(b'claimed_solved' in target[0] and b'1/5' in target[0],'status and effort');need(b'10.' not in target[0],'blank DOI')
metadata=json.loads((A/'preprint/metadata.json').read_text());need(metadata==json.loads((pre/'metadata.json').read_text())==json.loads((inner/'metadata.json').read_text())==json.loads((A/'preprint/zenodo-deposit.json').read_text())['metadata']==json.loads((pre/'zenodo-deposit.json').read_text())['metadata']==json.loads((T/'PUBLICATION_METADATA.json').read_text())['zenodo_metadata'],'all metadata equality')
for row in S['core_files']:
    b=(A/'preprint'/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'canonical seal');need(b==(pre/row['path']).read_bytes(),'assembled core identity')
ziprows=[]
frozen=json.loads((A/'source/FROZEN_INPUTS.json').read_text())
for archive in frozen['archives']:
    zpath=A/'source'/archive['archive'];manifest=json.loads((A/'source'/archive['manifest']).read_text());b=zpath.read_bytes();need(sha(b)==archive['sha256']==manifest['archive']['sha256'] and len(b)==manifest['archive']['bytes'],'safe archive pin')
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist();need(len(names)==len(set(names)) and set(names)==set(manifest['members']),'safe archive inventory')
        for i in z.infolist():
            p=PurePosixPath(i.filename);need(str(p)==i.filename and not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and stat.S_ISREG(i.external_attr>>16),'safe member path/type');b=z.read(i);need(len(b)==manifest['members'][i.filename]['bytes'] and sha(b)==manifest['members'][i.filename]['sha256'],'member pins')
        ziprows.append({'archive':archive['archive'],'members':len(names),'sha256':sha(zpath.read_bytes())})
need(sum(x['members'] for x in ziprows)==55,'55members')
with zipfile.ZipFile(pre/'verification.zip') as z:
    names=z.namelist();need(len(names)==len(set(names))==140,'portable ZIP inventory');need(set(names)=={p.relative_to(inner).as_posix() for p in inner.rglob('*') if p.is_file()},'portable ZIP closed')
    for i in z.infolist():need(stat.S_ISREG(i.external_attr>>16) and z.read(i)==(inner/i.filename).read_bytes(),'portable ZIP member')
need(all(not any(s in n for s in ['/private_sources/','/renders/','.git/']) for n in prepared),'no primary-source cache paths')
need([n for n in prepared if n.endswith('.pdf')]==['publication_20261014/preprint/output/pdf/note.pdf','publication_20261014/verification_package/note.pdf'],'only authored PDFs')
branch=git('symbolic-ref','--short','HEAD').decode().strip();need(branch=='main','branch')
out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','branch':branch,'actual_prepared_git_blobs_read':len(prepared),'actual_original_git_blobs_read':len(original),'prepared_modes':sorted(set(pm.values())),'prepared_commit':S['prepared_commit'],'parents':parents,'main_base':mainbase,'changed_paths':changed,'all_other_queue_bytes_unchanged':True,'target_row':target[0].decode().strip(),'all_10_core_files_exact':True,'all_metadata_exact':True,'zip_archives':ziprows,'portable_members':140,'prepared_blob_sha256':{n:sha(b) for n,b in prepared.items()},'original_blob_sha256':{n:sha(b) for n,b in original.items()}}
(R/'GIT_PACKAGE_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','branch','actual_prepared_git_blobs_read','actual_original_git_blobs_read','target_row']}))
