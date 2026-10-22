#!/usr/bin/env python3
"""Portable exact-package integrity and finite-replay checks. Python 3.10+."""
import argparse, hashlib, json, re, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath
EXPECTED = set(['PUBLICATION_MANIFEST.json', 'README.md', 'SCOPE_CLARIFICATIONS.md', 'archives/AUDIT_PACKET.zip', 'archives/AUTHOR_PACKET.zip', 'author/APPROACH_LOG.md', 'author/CONTROL_RESULTS.json', 'author/DATASET_VERIFICATION.json', 'author/LIMITATIONS.md', 'author/MANIFEST.json', 'author/PROOF.md', 'author/README.md', 'author/REPRODUCTION.json', 'author/SOURCES.md', 'author/SOURCE_METADATA.json', 'author/verify.py', 'independent-audit/AUDIT.md', 'independent-audit/AUDIT_CONTROL_RESULTS.json', 'independent-audit/BINDING.json', 'independent-audit/CLARIFICATIONS.md', 'independent-audit/MANIFEST.json', 'independent-audit/README.md', 'independent-audit/REPRODUCTION.json', 'independent-audit/verify_audit.py', 'verify_release.py'])
ARCHIVES = {
 'author': ('AUTHOR_PACKET.zip', 23418, '808dd53041a58e139590fd5eb31c85b8667f06637c6995024708256e8eddddce', 'safe/', 11),
 'independent-audit': ('AUDIT_PACKET.zip', 17570, '898f7920120de70ef4d6e93ab773e2ec15e0e0991a4f2b3d6f359b9ff9c6004c', 'audit/', 8)
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
    require(type(manifest['target_id']) is int and manifest['target_id']==10900010, 'target identity')
    require(type(manifest['rank']) is int and manifest['rank']==672, 'rank identity')
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

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def bind_manifest(root, directory, manifest_name, expected_hash, extra_files):
    base=root/directory
    require(sha(base/manifest_name)==expected_hash, 'frozen manifest hash: '+directory)
    m=read_json(base/manifest_name)
    expected={p[len(directory)+1:] for p in EXPECTED if p.startswith(directory+'/')}
    require({e['path'] for e in m['files']}==expected-set(extra_files), 'frozen manifest inventory')
    for e in m['files']:
        require(e['path'] in expected, 'unsafe frozen manifest path')
        data=(base/e['path']).read_bytes()
        require(len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'], 'frozen manifest content: '+e['path'])
    return m

def bindings(root):
    author_hash='94868f587e11bc5cf7e275beacd7cdec8beaf6b033dc8d48e557d83e1225559b'
    audit_hash='0a2749f0257c662f1a88bd5a1b6f4c1295a31d06851872debf648bfc60614423'
    author=bind_manifest(root,'author','MANIFEST.json',author_hash,['MANIFEST.json'])
    audit=bind_manifest(root,'independent-audit','MANIFEST.json',audit_hash,['MANIFEST.json'])
    require(author['target_id']==10900010 and author['rank']==672 and author['status']=='NO RESOLUTION' and author['approaches_completed']==5, 'author identity')
    require(audit['target_id']==10900010 and audit['rank']==672, 'audit identity')
    b=read_json(root/'independent-audit/BINDING.json')
    require(b['target_id']==10900010 and b['rank']==672 and b['classification']=='unsolved' and b['approaches_completed']==5, 'audit disposition')
    require(b['author_archive_sha256']==ARCHIVES['author'][2] and b['author_archive_bytes']==23418 and b['author_archive_members']==11 and b['author_manifest_sha256']==author_hash, 'audit author binding')
    require(b['verdict']=='PASS AS QUALIFIED PARTIAL RESULTS; NO GENERAL RESOLUTION' and b['optional_clarifications']==3 and b['theorem_breaking_defects_found']==0, 'audit verdict')
    require(sha(root/'SCOPE_CLARIFICATIONS.md')=='0dce495861c4e3ba4b6c0d7f85efa0b8d38fa7ef6f3c02f29d48b1b16be423e5', 'clarification supplement binding')
    return {'status':'PASS','optional_clarifications':3,'frozen_originals_unchanged':True}

def verify(root, integrity_only=False):
    result={'integrity':integrity(root),'bindings':bindings(root)}
    if not integrity_only:
        author=run(root/'author/verify.py')
        require(author==(root/'author/CONTROL_RESULTS.json').read_bytes(), 'author stdout differs from stored bytes')
        a=json.loads(author,object_pairs_hook=unique)
        require(a['all_pass'] is True and a['control_groups']==6 and len(a['results'])==6 and all(x['pass'] is True for x in a['results']), 'author groups')
        audit=run(root/'independent-audit/verify_audit.py',['--author-safe',root/'author','--author-archive',root/'archives/AUTHOR_PACKET.zip'])
        require(audit==(root/'independent-audit/AUDIT_CONTROL_RESULTS.json').read_bytes(), 'audit stdout differs from stored bytes')
        u=json.loads(audit,object_pairs_hook=unique)
        require(u['all_pass'] is True and len(u['independent_control_groups'])==6 and len(u['additional_adversarial_groups'])==5, 'audit groups')
        require(all(x['pass'] is True for x in u['independent_control_groups']+u['additional_adversarial_groups']), 'audit control failures')
        for name,data in [('author',author),('independent-audit',audit)]:
            r=read_json(root/name/'REPRODUCTION.json')
            require(len(data)==r['stdout_bytes'] and hashlib.sha256(data).hexdigest()==r['stdout_sha256'], 'reproduction output binding')
        result['author_replay']={'status':'PASS','byte_identical':True,'groups':6,'stdout_bytes':len(author)}
        result['independent_replay']={'status':'PASS','byte_identical':True,'independent_groups':6,'additional_groups':5,'stdout_bytes':len(audit)}
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--integrity-only',action='store_true')
    a=parser.parse_args()
    try: print(json.dumps(verify(a.root.resolve(),a.integrity_only),sort_keys=True))
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr); raise SystemExit(1)
