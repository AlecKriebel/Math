#!/usr/bin/env python3
"""Verify frozen bytes, complete inventory, portable checks, and optional inputs."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, subprocess, sys, zipfile

def require(condition, message):
    if not condition: raise RuntimeError(message)

def identity(data): return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def safe(name):
    p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p)==name, 'Unsafe path')
    return str(p)

def run(root, args):
    require(__debug__, 'Assertions must be active; do not use optimized Python')
    completed=subprocess.run([sys.executable,'-E','-B',*args],cwd=root,check=True,capture_output=True,text=True)
    return completed.stdout

def verify(root):
    require(__debug__, 'Assertions must be active; do not use optimized Python')
    manifest=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
    files=manifest['files']; names=[safe(e['path']) for e in files]
    require(len(names)==len(set(names)), 'Duplicate manifest path')
    require(not any(p.is_symlink() for p in root.rglob('*')), 'Symlink in payload')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual==set(names)|{'PUBLICATION_MANIFEST.json'}, 'Recursive inventory mismatch')
    for e in files:
        require(identity((root/e['path']).read_bytes())=={k:e[k] for k in ('bytes','sha256')},'File identity mismatch: '+e['path'])
    provenance=json.loads((root/'PUBLICATION_PROVENANCE.json').read_text())
    count=0
    for a in provenance['archives']:
        p=root/safe(a['path']);dest=root/safe(a['extracted_directory'])
        require(identity(p.read_bytes())=={k:a[k] for k in ('bytes','sha256')},'Archive identity mismatch')
        with zipfile.ZipFile(p) as z:
            members=z.namelist(); require(z.testzip() is None,'Archive CRC mismatch')
            require(len(members)==len(set(members))==a['member_count'],'Archive member count mismatch')
            actual={f.relative_to(dest).as_posix() for f in dest.rglob('*') if f.is_file()}
            require(set(members)==actual,'Archive recursive inventory mismatch')
            for name in members: require(z.read(name)==(dest/safe(name)).read_bytes(),'Archive member byte mismatch')
            count+=len(members)
    originals={p.relative_to(root/'author').as_posix() for p in (root/'author').rglob('*') if p.is_file()}
    preserved={p.relative_to(root/'audit/author').as_posix() for p in (root/'audit/author').rglob('*') if p.is_file()}
    require(originals==preserved,'Author copy inventory mismatch')
    for n in originals:require((root/'author'/n).read_bytes()==(root/'audit/author'/n).read_bytes(),'Author copy differs')
    require(run(root,['-c','import sys; print(__debug__)']).strip()=='True','Child assertions disabled')
    for s in ['author/verify_manifest.py','audit/verify_audit_manifest.py','audit/author/verify_manifest.py']:
        require(run(root,[str(root/s)]).startswith('PASS:'),'Frozen manifest check failed')
    return {'status':'PASS','payload_files':len(actual_payload(root)),'archive_members_byte_verified':count,'frozen_manifests':'PASS','author_snapshot_identical':True,'assertions_active':True}

def actual_payload(root): return [p for p in root.rglob('*') if p.is_file()]

def verify_queue(root, base_path, updated_path):
    d=json.loads((root/'QUEUE_DELTA.json').read_text());base=base_path.read_bytes();updated=updated_path.read_bytes()
    require(identity(base)==d['base'] and identity(updated)==d['updated'],'Queue identity mismatch')
    x=base.splitlines(keepends=True);y=updated.splitlines(keepends=True)
    require(len(x)==len(y),'Queue line count differs')
    matches=[i for i,l in enumerate(x) if b'| 30005755 / OWR-14298157-005 |' in l]
    require(len(matches)==1,'Queue target not unique');i=matches[0]
    require(i+1==d['row_line_1_based'],'Queue row position differs')
    require(x[:i]==y[:i] and x[i+1:]==y[i+1:],'Unrelated queue bytes changed')
    before=x[i].split(b'|');after=y[i].split(b'|')
    require(len(before)==len(after),'Queue cell count differs')
    require([j for j in range(len(before)) if before[j]!=after[j]]==[8,9],'Unexpected changed queue cells')
    require(before[1].strip()==after[1].strip()==b'801','Queue rank mismatch')
    require(before[8]==b' queued ' and before[9]==b' 0/5 ' and after[8]==b' unsolved ' and after[9]==b' 5/5 ','Queue disposition mismatch')
    return {'status':'PASS','changed_cells':['Status','Turns'],'all_other_bytes_preserved':True,'stale_header_preserved':True,'findings_unchanged':True}

def replay(root):
    result={}
    for label,script,expected in [('author','author/verification.py','author/expected_results.json'),('audit_author_copy','audit/author/verification.py','audit/author/expected_results.json'),('independent_audit','audit/audit_checks.py','audit/AUDIT_RESULTS.json')]:
        require(run(root,[str(root/script),'--check',str(root/expected)]).startswith('PASS:'),'Replay check failed')
        generated=json.loads(run(root,[str(root/script)]))
        require(generated==json.loads((root/expected).read_text()),'Regenerated result differs')
        result[label]={'status':'PASS','assertions_active':True,'stored_result_json_matches':True}
    return result

def verify_corpora(root, directory):
    entries=json.loads((root/'author/source_metadata.json').read_text())['public_corpus_verification']
    for e in entries:
        p=directory/safe(e['name']);require(identity(p.read_bytes())=={k:e[k] for k in ('bytes','sha256')},'Corpus identity mismatch: '+e['name'])
    return {'status':'PASS','hashes_and_sizes_verified':len(entries),'scope':'Full bytes hashed; source identity joins are historical audit evidence, not replayed here.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--replay',action='store_true');ap.add_argument('--queue-base',type=Path);ap.add_argument('--queue-updated',type=Path);ap.add_argument('--corpus-dir',type=Path);args=ap.parse_args()
    require(bool(args.queue_base)==bool(args.queue_updated),'Supply both queue paths')
    root=Path(__file__).resolve().parent;out=verify(root)
    out['queue']=verify_queue(root,args.queue_base,args.queue_updated) if args.queue_base else {'status':'NOT_RUN','reason':'Optional queue snapshots not supplied'}
    out['corpora']=verify_corpora(root,args.corpus_dir) if args.corpus_dir else {'status':'NOT_RUN','reason':'Optional public corpus directory not supplied'}
    out['replay']=replay(root) if args.replay else {'status':'NOT_RUN','reason':'Pass --replay for arithmetic checks'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
