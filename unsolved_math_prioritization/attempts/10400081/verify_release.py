#!/usr/bin/env python3
"""Portable exact-package integrity and finite-replay checks. Python 3.10+."""
import argparse, hashlib, json, re, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath
EXPECTED = set(['PROOF_CORRECTED.md', 'PUBLICATION_MANIFEST.json', 'README.md', 'archives/AUDIT_PACKET.zip', 'archives/AUTHOR_PACKET.zip', 'author/APPROACH_LOG.md', 'author/CONTROL_RESULTS.json', 'author/LIMITATIONS.md', 'author/MANIFEST.json', 'author/PROOF.md', 'author/README.md', 'author/REPRODUCTION.json', 'author/SOURCES.md', 'author/SOURCE_METADATA.json', 'author/verify.py', 'independent-audit/ADVERSARIAL_RESULTS.json', 'independent-audit/AUDIT.md', 'independent-audit/AUDIT_BINDING.json', 'independent-audit/CORRECTIONS.json', 'independent-audit/REPLAY_CONTROL_RESULTS.json', 'independent-audit/SOURCE_RECHECK.json', 'independent-audit/adversarial_verify.py', 'receipts/AUDIT_RECEIPT.json', 'receipts/AUTHOR_RECEIPT.json', 'verify_release.py'])
ARCHIVES = {
 'author': ('AUTHOR_PACKET.zip', 23640, 'e876882ef9e4ae229fd4110bd1390e021db3726b7423ee44816c294efdbbb44d', '', 10),
 'independent-audit': ('AUDIT_PACKET.zip', 12415, '40b1c016b210d8405f9d6c1a29c059d9d595e754c695e0a23aed013480b47e57', '', 7)
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
    require(type(manifest['target_id']) is int and manifest['target_id']==10400081, 'target identity')
    require(type(manifest['rank']) is int and manifest['rank']==671, 'rank identity')
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
    author_hash='5f6837c610501e405a7698acb4e5b66a2535a397157aec35fbabae371e8c4479'
    audit_hash='50c718e7263390022c8f289e0c2f4d3901dc40552cb77b85f749d59ec4d7739a'
    author=bind_manifest(root,'author','MANIFEST.json',author_hash,['MANIFEST.json'])
    audit=bind_manifest(root,'independent-audit','AUDIT_BINDING.json',audit_hash,['AUDIT_BINDING.json'])
    require(author['problem_id']==10400081 and author['rank']==671 and author['recommended_status']=='unsolved' and author['substantive_approaches']==5, 'author identity')
    require(audit['problem_id']==10400081 and audit['rank']==671 and audit['recommended_status']=='unsolved' and audit['substantive_approaches']==5, 'audit identity')
    require(audit['author_manifest_sha256']==author_hash and audit['author_archive_sha256']==ARCHIVES['author'][2], 'audit author binding')
    require(audit['verdict']=='PASS_WITH_TWO_SCOPE_CORRECTIONS' and audit['required_corrections']==['C1','C2'] and audit['numbered_propositions_audited']==8, 'audit verdict')
    for group,name in [('author','AUTHOR_RECEIPT.json'),('independent-audit','AUDIT_RECEIPT.json')]:
        r=read_json(root/'receipts'/name)
        require(r['packet']==ARCHIVES[group][0] and r['bytes']==ARCHIVES[group][1] and r['sha256']==ARCHIVES[group][2], 'archive receipt')
        if group=='author': require(r['manifest_sha256']==author_hash and r['disposition']=='unsolved 5/5', 'author receipt binding')
        else: require(r['binding_sha256']==audit_hash and r['recommended_disposition']=='unsolved 5/5', 'audit receipt binding')
    c=read_json(root/'independent-audit/CORRECTIONS.json')
    require(c['source_manifest_sha256']==author_hash and c['source_proof_sha256']==sha(root/'author/PROOF.md'), 'correction source binding')
    require([x['id'] for x in c['corrections']]==['C1','C2'], 'mandatory correction inventory')
    s=(root/'author/PROOF.md').read_text()
    for change in c['corrections']:
        require(change['target']=='PROOF.md' and s.count(change['old'])==1, 'correction exact-match prerequisite')
        s=s.replace(change['old'],change['new'],1)
    data=s.encode('utf-8')
    require(data==(root/'PROOF_CORRECTED.md').read_bytes(), 'corrected proof differs from exact overlay')
    require(hashlib.sha256(data).hexdigest()==c['resulting_proof_sha256']=='1ce8ee0efaec73568f41379ae0c3a1a1e5537606c7e426c7910b6c06ecb000ea', 'corrected proof hash')
    require(c['disposition_after_corrections']=='unsolved 5/5', 'corrected disposition')
    return {'status':'PASS','corrections':['C1','C2'],'frozen_originals_unchanged':True}

def verify(root, integrity_only=False):
    result={'integrity':integrity(root),'bindings':bindings(root)}
    if not integrity_only:
        for key,script,reference,count in [
          ('author_replay','author/verify.py','author/CONTROL_RESULTS.json',7396),
          ('independent_replay','independent-audit/adversarial_verify.py','independent-audit/ADVERSARIAL_RESULTS.json',13864)]:
            actual=run(root/script)
            require(actual==(root/reference).read_bytes(),key+' stdout differs from stored bytes')
            parsed=json.loads(actual,object_pairs_hook=unique)
            require(parsed['status']=='PASS' and parsed['total_assertions']==count,key+' assertion count')
            if key=='author_replay': require(actual==(root/'independent-audit/REPLAY_CONTROL_RESULTS.json').read_bytes(),'audit author replay differs')
            result[key]={'status':'PASS','byte_identical':True,'assertions':count}
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--integrity-only',action='store_true')
    a=parser.parse_args()
    try: print(json.dumps(verify(a.root.resolve(),a.integrity_only),sort_keys=True))
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr); raise SystemExit(1)
