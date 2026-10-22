#!/usr/bin/env python3
"""Portable exact-package integrity and finite-replay checks. Python 3.10+."""
import argparse, hashlib, json, re, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath
EXPECTED = set(['PUBLICATION_MANIFEST.json', 'README.md', 'archives/rank667-30001155-authored-packet.zip', 'archives/rank667-30001155-independent-audit.zip', 'author/APPROACH_LOG.md', 'author/DATA_PROVENANCE.json', 'author/MANIFEST.json', 'author/PROOF_AND_PARTIALS.md', 'author/README.md', 'author/REPLAY_ENVIRONMENT.json', 'author/SOURCE_VERIFICATION.json', 'author/exact_results.json', 'author/numerical_challenge.py', 'author/numerical_results.json', 'author/refine_stadium.py', 'author/stadium_refinement.json', 'author/verify_exact.py', 'author/verify_manifest.py', 'independent-audit/AUDIT.md', 'independent-audit/AUDIT_MANIFEST.json', 'independent-audit/AUDIT_RESULT.json', 'independent-audit/AUDIT_SOURCE_METADATA.json', 'independent-audit/CORRECTIONS.md', 'independent-audit/REPLAY_RECEIPT.json', 'independent-audit/verify_audit.py', 'verify_release.py'])
ARCHIVES = {'author': ('rank667-30001155-authored-packet.zip', 25174, '02d7ebf85303b54d4643a79c266f0273d7881d80cddc0ddd215db2be2d35e6d9', 'packet/', 14), 'independent-audit': ('rank667-30001155-independent-audit.zip', 13179, '36542ded137aa3171c48f46a9bd659534cbf4d9567f2d3f4bb411a5551971b46', 'audit/', 7)}
def require(ok, message):
    if not ok: raise ValueError(message)
def unique(pairs):
    out={}
    for k,v in pairs:
        require(k not in out, 'duplicate JSON key: '+k)
        out[k]=v
    return out
def read_json(path): return json.loads(path.read_text(), object_pairs_hook=unique)
def integrity(root):
    items=list(root.rglob('*'))
    require(not any(p.is_symlink() for p in items), 'symlink forbidden')
    actual={p.relative_to(root).as_posix() for p in items if p.is_file()}
    require(actual==EXPECTED, 'unexpected/missing file: '+repr(sorted(actual^EXPECTED)))
    directories={str(PurePosixPath(p).parent) for p in EXPECTED}
    directories.discard('.')
    require({p.relative_to(root).as_posix() for p in items if p.is_dir()}==directories, 'unexpected/missing directory')
    manifest=read_json(root/'PUBLICATION_MANIFEST.json')
    require(set(manifest)=={'format','target_id','rank','status','turns','files'}, 'manifest schema')
    require(type(manifest['format']) is int and manifest['format']==1, 'manifest format')
    require(type(manifest['target_id']) is int and manifest['target_id']==30001155, 'target identity')
    require(type(manifest['rank']) is int and manifest['rank']==667, 'rank identity')
    require(manifest['status']=='unsolved' and manifest['turns']=='5/5', 'disposition')
    require(isinstance(manifest['files'],list), 'files must be list')
    seen=set()
    for e in manifest['files']:
        require(isinstance(e,dict) and set(e)=={'path','bytes','sha256'}, 'entry schema')
        p=e['path']; require(isinstance(p,str), 'path type')
        pp=PurePosixPath(p)
        require(not pp.is_absolute() and str(pp)==p and '\\' not in p and all(t not in ('','.','..') for t in p.split('/')), 'unsafe path')
        require(p in EXPECTED-{'PUBLICATION_MANIFEST.json'} and p not in seen, 'unexpected/duplicate path')
        seen.add(p)
        require(type(e['bytes']) is int and e['bytes']>=0, 'invalid byte count')
        require(isinstance(e['sha256'],str) and re.fullmatch('[0-9a-f]{64}', e['sha256']) is not None, 'invalid hash')
        b=(root/p).read_bytes()
        require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'], 'content mismatch: '+p)
    require(seen==EXPECTED-{'PUBLICATION_MANIFEST.json'}, 'incomplete inventory')
    counts={}
    for directory,(filename,size,digest,prefix,count) in ARCHIVES.items():
        path=root/'archives'/filename; b=path.read_bytes()
        require(len(b)==size and hashlib.sha256(b).hexdigest()==digest, 'frozen archive mismatch')
        with zipfile.ZipFile(path) as z:
            names=z.namelist(); require(len(names)==count and len(set(names))==count, 'archive member count')
            expected={directory+'/'+n[len(prefix):] for n in names if n.startswith(prefix)}
            require(len(expected)==count and expected=={p for p in EXPECTED if p.startswith(directory+'/')}, 'archive member list')
            for name in names:
                require(z.read(name)==(root/directory/name[len(prefix):]).read_bytes(), 'expanded archive member mismatch: '+name)
        counts[directory]=count
    return {'status':'PASS','files':len(EXPECTED),'manifest_entries':len(seen),'frozen_files':counts}
def run(script,args=()):
    p=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],cwd=script.parent,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=900)
    require(p.returncode==0, 'replay failed: '+script.name+' '+p.stderr.decode(errors='replace'))
    return p.stdout

def verify(root, integrity_only=False, numerical=False):
    result={'integrity':integrity(root)}
    if not integrity_only:
        run(root/'author/verify_manifest.py')
        manifest=read_json(root/'independent-audit/AUDIT_MANIFEST.json')
        require(manifest['problem_id']==30001155, 'audit identity')
        for e in manifest['files']:
            data=(root/'independent-audit'/e['path']).read_bytes()
            require(len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'], 'audit manifest mismatch')
        exact=run(root/'author/verify_exact.py')
        require(exact==(root/'author/exact_results.json').read_bytes(), 'author exact output differs')
        require(json.loads(exact)['assertions']==2031, 'exact assertion count')
        args=['--packet',root/'author','--archive',root/'archives/rank667-30001155-authored-packet.zip']
        if numerical: args.append('--numerical')
        replay=json.loads(run(root/'independent-audit/verify_audit.py',args), object_pairs_hook=unique)
        expected=read_json(root/'independent-audit/REPLAY_RECEIPT.json')
        if not numerical: expected['numerical_replay']=None
        require(replay==expected, 'independent replay differs')
        result.update(author_exact_assertions=2031,author_output_byte_identical=True,independent_replay='PASS: exact JSON match',numerical_replay=replay['numerical_replay'])
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--integrity-only',action='store_true')
    parser.add_argument('--numerical',action='store_true')
    a=parser.parse_args()
    try: print(json.dumps(verify(a.root.resolve(),a.integrity_only,a.numerical),sort_keys=True))
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr); raise SystemExit(1)
