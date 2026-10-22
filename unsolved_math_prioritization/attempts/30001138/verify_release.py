#!/usr/bin/env python3
"""Portable exact-package integrity and finite-replay checks. Python 3.10+."""
import argparse, hashlib, json, re, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath
EXPECTED = set(['PUBLICATION_MANIFEST.json', 'README.md', 'archives/rank666-30001138-authored-packet.zip', 'archives/rank666-30001138-independent-audit.zip', 'author/APPROACH_LOG.md', 'author/DATA_PROVENANCE.json', 'author/MANIFEST.json', 'author/PROOF_AND_PARTIALS.md', 'author/README.md', 'author/SOURCE_VERIFICATION.json', 'author/exploration/facial_test.py', 'author/exploration/minor_search.json', 'author/exploration/search_minors.py', 'author/exploration/truncation_results.json', 'author/exploration/truncation_test.py', 'author/minor_certificates.json', 'author/petersen_family_certificates.json', 'author/verification_results.json', 'author/verify.py', 'author/verify_manifest.py', 'independent-audit/AUDIT.md', 'independent-audit/AUDIT_BINDING.json', 'independent-audit/AUDIT_MANIFEST.json', 'independent-audit/CORRECTIONS.md', 'independent-audit/README.md', 'independent-audit/SOURCE_AUDIT.json', 'independent-audit/author_replay.json', 'independent-audit/independent_results.json', 'independent-audit/independent_verify.py', 'independent-audit/verify_binding.py', 'verify_release.py'])
ARCHIVES = {
 'author': ('rank666-30001138-authored-packet.zip', 26737, '78cdf14fddfa360a5cbb27d1b571e88bd4eed6e7410c6296de628b19f9770719', 'packet/', 16),
 'independent-audit': ('rank666-30001138-independent-audit.zip', 18717, '01d47732e475622e70a9eb05a90ba20d874878eaa70f3da648398a463fc99b2d', 'audit/', 10)
}
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
    require(type(manifest['target_id']) is int and manifest['target_id']==30001138, 'target identity')
    require(type(manifest['rank']) is int and manifest['rank']==666, 'rank identity')
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
    p=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],cwd=script.parent,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    require(p.returncode==0, 'replay failed: '+script.name+' '+p.stderr.decode(errors='replace'))
    return p.stdout

def verify(root, integrity_only=False):
    result={'integrity':integrity(root)}
    if not integrity_only:
        run(root/'author/verify_manifest.py')
        run(root/'independent-audit/verify_binding.py',[root/'archives/rank666-30001138-authored-packet.zip'])
        for key,script,args,reference in [
          ('author_replay','author/verify.py',[],'author/verification_results.json'),
          ('independent_replay','independent-audit/independent_verify.py',[root/'author'],'independent-audit/independent_results.json')]:
            actual=json.loads(run(root/script,args),object_pairs_hook=unique)
            require(actual==read_json(root/reference),key+' differs from stored result')
            if key=='author_replay': require(actual==read_json(root/'independent-audit/author_replay.json'),'audit author replay differs')
            result[key]='PASS: exact JSON match'
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--integrity-only',action='store_true')
    a=parser.parse_args()
    try: print(json.dumps(verify(a.root.resolve(),a.integrity_only),sort_keys=True))
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr); raise SystemExit(1)
