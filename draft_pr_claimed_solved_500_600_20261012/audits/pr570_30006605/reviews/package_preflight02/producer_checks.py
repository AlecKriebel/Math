#!/usr/bin/env python3
"""Relocated deterministic producer, guarded paths, and independent rebuild checks."""
from pathlib import Path
import subprocess,os,json,shutil,hashlib,sys
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PUB=AUDIT/'publication'
WORK=HERE/'.cache'/'producer'
WORK.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
expected=(PUB/'verification_package.zip').read_bytes()
records=[]
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(HERE/'.cache'/'tmp'))
def checkout(name):
    dest=WORK/name
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(AUDIT,dest,ignore=shutil.ignore_patterns('.cache','qa','__pycache__','scratch','receipts','package_preflight*'))
    return dest

def run(dest):
    return subprocess.run([sys.executable,str(dest/'publication/make_package.py')],capture_output=True,text=True,env=ENV)

def log(case,p,**kw):
    records.append({'case':case,'returncode':p.returncode,'stderr':p.stderr,**kw})

for name in ('ordinary/checkout','.cache/checkout','scratch/checkout'):
    dest=checkout(name);p=run(dest)
    assert p.returncode==0,p.stderr
    actual=(dest/'publication/verification_package.zip').read_bytes()
    assert actual==expected
    assert (dest/'publication/PACKAGE_MANIFEST.json').read_bytes()==(PUB/'PACKAGE_MANIFEST.json').read_bytes()
    log(name,p,status='PASS',zip_sha256=sha(actual),byte_equal=True)

for forbidden in ('.cache','sources','scratch','qa','.secrets'):
    dest=checkout('lexical_'+forbidden.lstrip('.'))
    # Expose an allowed internal file through a parent symlink whose lexical name is forbidden.
    folder=dest/'reviews/oracle01'
    (folder/'exposed').mkdir()
    (folder/'exposed'/'leak.md').write_text('sentinel: forbidden lexical payload route\n')
    (folder/forbidden).symlink_to('exposed',target_is_directory=True)
    seal=folder/'SHA256SUMS'
    content=(folder/'exposed/leak.md').read_bytes()
    seal.write_text(seal.read_text()+sha(content)+'  '+forbidden+'/leak.md\n')
    p=run(dest)
    accepted=p.returncode==0
    log('internal_parent_symlink_forbidden_'+forbidden,p,status='ACCEPTED' if accepted else 'REJECTED',lexical_source='reviews/oracle01/'+forbidden+'/leak.md',resolved_source='reviews/oracle01/exposed/leak.md')
    if accepted:
        import zipfile
        with zipfile.ZipFile(dest/'publication/verification_package.zip') as z:
            name='weighted_centers_verification/reviews/oracle01/'+forbidden+'/leak.md'
            assert z.read(name)==content
        records[-1]['forbidden_name_in_output_archive']=True

for tag,mode,reason in [('external_parent','parent','Source escapes the audit'),('leaf','leaf','Invalid or duplicate source')]:
    dest=checkout(tag)
    outside=WORK/(tag+'_outside');outside.mkdir(exist_ok=True)
    (outside/'sentinel.json').write_text('{}\n')
    if mode=='parent':
        shutil.rmtree(dest/'root_reproduction')
        (dest/'root_reproduction').symlink_to(outside,target_is_directory=True)
    else:
        pth=dest/'publication/weighted_centers.tex';pth.unlink();pth.symlink_to(outside/'sentinel.json')
    p=run(dest);assert p.returncode!=0 and reason in p.stderr,p.stderr
    log(tag,p,status='REJECTED_AS_REQUIRED')

for tag,rel,reason in [('forbidden_payload','.cache/guard.txt','Excluded source'),('traversal','../guard.txt','Invalid relative path'),('private','guard.private.md','Invalid or duplicate source')]:
    dest=checkout(tag)
    snap=dest/'ORIGINAL_SNAPSHOT.json';obj=json.loads(snap.read_text())
    source=dest/'original'/rel;source.parent.mkdir(parents=True,exist_ok=True);source.write_text('guard\n')
    obj['files'].append({'path':rel,'size':6,'sha256':sha(b'guard\n')})
    snap.write_text(json.dumps(obj))
    p=run(dest);assert p.returncode!=0 and reason in p.stderr,p.stderr
    log(tag,p,status='REJECTED_AS_REQUIRED')

out={'expected_zip_sha256':sha(expected),'canonical_inputs_modified':False,'checks':records,'known_repair_F01':'Relocation under .cache and scratch ancestors byte-identical: PASS','remaining_symlink_exclusion_test':'See five explicitly recorded accepted/rejected cases'}
(HERE/'PRODUCER_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
