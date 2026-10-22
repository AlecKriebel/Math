"""Externally pinned source-free integrity/replay verifier. Trusted Python and OS."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECTED: use python -I -S -B [ -O | -OO ] verify_publication.py PIN PACKET')
from pathlib import Path, PurePosixPath
import hashlib, json, os, stat, subprocess, tempfile, zipfile, io

AUTHOR = {'CONTROL_RECEIPT.json','CORPUS_FINGERPRINTS.json','LEDGER.json','MANIFEST.json','README.md','REPORT.md','SOURCE_METADATA.json','controls.py','verify.py'}
AUDIT = {'AUDIT_REPORT.md','MANIFEST.json','README.md','REPLAY_RECEIPT.json','SOURCE_CHECKS.json','replay_audit.py'}
FILES = {f'author/{n}' for n in AUTHOR} | {f'audit/{n}' for n in AUDIT} | {
    'AUTHOR_FREEZE.json','AUTHOR_PACKET.zip','AUDIT_FREEZE.json','AUDIT_PACKET.zip',
    'README.md','ACCEPTANCE.md','RESEARCH_LOG.md','verify_publication.py','mutation_tests.py'}
DIRS = {'author','audit'}
PINS = {
    'author/MANIFEST.json':'56c934a8949d90e0558849578e1421826b9e66520c0a9899a8745eebe7223ef2',
    'author/verify.py':'ac53854fdf7f99f902da3461929d03dec1c31c2891afa9df96bfc56efe9153fb',
    'AUTHOR_PACKET.zip':'02a24cc8994a462d65de1471ba73a7d2cca63b51e3f562278db9866d9012ee58',
    'audit/MANIFEST.json':'0dd57e0bbbce6ad8ce678c17824c8d035fc267d1f28af6fcfab09fe77b83c8c5',
    'audit/replay_audit.py':'565d36698e3bd60a3f649b5827f8f25f01a084b6c5e5f20a7b4b4cfb89ab43f0',
    'AUDIT_PACKET.zip':'418f8311ecff7c8e971d7cacff79c865019e0a2632f388326e23436942fc3923',
}

def require(ok, message):
    if not ok: raise ValueError(message)
def digest(data): return hashlib.sha256(data).hexdigest()
def no_duplicate_keys(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'Duplicate JSON key')
        result[key]=value
    return result
def parse(raw): return json.loads(raw,object_pairs_hook=no_duplicate_keys)
def valid_path(name):
    return isinstance(name,str) and name and '\\' not in name and not name.startswith('/') and all(p not in ('','.', '..') for p in name.split('/')) and PurePosixPath(name).as_posix()==name

def integrity(root,pin):
    require(isinstance(pin,str) and len(pin)==64 and all(c in '0123456789abcdef' for c in pin),'Malformed pin')
    require(not root.is_symlink() and root.is_dir(),'Invalid or linked root')
    files=set();dirs=set()
    def walk(directory):
        for entry in os.scandir(directory):
            p=Path(entry.path);rel=p.relative_to(root).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(rel in DIRS,'Unexpected directory: '+rel);dirs.add(rel);walk(p)
            else:
                require(stat.S_ISREG(mode),'Linked or special entry: '+rel);files.add(rel)
    walk(root)
    require(files==FILES|{'PUBLIC_MANIFEST.json'} and dirs==DIRS,'Closed inventory mismatch')
    raw=(root/'PUBLIC_MANIFEST.json').read_bytes();require(digest(raw)==pin,'Manifest pin mismatch')
    manifest=parse(raw)
    require(set(manifest)=={'schema','problem_id','files'} and manifest['schema']=='unitary-multiplicity-publication-v1' and manifest['problem_id']==30001738,'Manifest schema/target mismatch')
    rows=manifest['files'];require(isinstance(rows,list) and len(rows)==len(FILES),'Invalid manifest size')
    names=[];snapshot={}
    for row in rows:
        require(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'Invalid entry')
        name=row['path'];require(valid_path(name) and name in FILES and name not in names,'Invalid/duplicate path');names.append(name)
        b=(root/name).read_bytes();require(type(row['bytes']) is int and len(b)==row['bytes'] and digest(b)==row['sha256'],'Payload mismatch: '+name);snapshot[name]=b
    require(set(names)==FILES,'Manifest allowlist mismatch')
    for name,value in PINS.items():require(digest(snapshot[name])==value,'Frozen pin mismatch: '+name)
    for sub,expected in [('author',AUTHOR),('audit',AUDIT)]:
        child=parse(snapshot[sub+'/MANIFEST.json']);entries=child['files']
        require(len(entries)==len(expected)-1 and {r['path'] for r in entries}==expected-{'MANIFEST.json'},'Nested inventory mismatch')
        for row in entries:
            b=snapshot[sub+'/'+row['path']];require(len(b)==row['bytes'] and digest(b)==row['sha256'],'Nested payload mismatch')
        archive_name='AUTHOR_PACKET.zip' if sub=='author' else 'AUDIT_PACKET.zip'
        with zipfile.ZipFile(io.BytesIO(snapshot[archive_name])) as z:
            require(len(z.namelist())==len(expected) and set(z.namelist())==expected,'Archive inventory mismatch')
            require(z.testzip() is None,'Archive CRC mismatch')
            for name in expected:require(z.read(name)==snapshot[sub+'/'+name],'Archive member mismatch')
    af=parse(snapshot['AUTHOR_FREEZE.json']);bf=parse(snapshot['AUDIT_FREEZE.json'])
    require(af['manifest_sha256']==PINS['author/MANIFEST.json'] and af['archive_sha256']==PINS['AUTHOR_PACKET.zip'] and af['archive_bytes']==len(snapshot['AUTHOR_PACKET.zip']),'Author freeze mismatch')
    require(bf['audit_manifest_sha256']==PINS['audit/MANIFEST.json'] and bf['archive_sha256']==PINS['AUDIT_PACKET.zip'] and bf['archive_bytes']==len(snapshot['AUDIT_PACKET.zip']),'Audit freeze mismatch')
    return snapshot

def replay(snapshot):
    opt=['-O']*sys.flags.optimize
    with tempfile.TemporaryDirectory(prefix='unitary-publication-') as td:
        root=Path(td)
        for name,b in snapshot.items():
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        results={}
        cases=[('author',['author/verify.py',PINS['author/MANIFEST.json'],str(root/'author')]),
               ('audit',['audit/replay_audit.py',str(root/'author'),str(root/'AUTHOR_PACKET.zip')])]
        for label,argv in cases:
            argv[0]=str(root/argv[0])
            process=subprocess.run([sys.executable,'-I','-S','-B',*opt,*argv],cwd=root,capture_output=True,timeout=180)
            require(process.returncode==0,label+' replay failed: '+process.stderr.decode(errors='replace'))
            result=parse(process.stdout)
            if label=='author':
                require(result=={'status':'pass','verified_files':8,'manifest_sha256':PINS['author/MANIFEST.json'],'controls':parse(snapshot['author/CONTROL_RECEIPT.json'])},'Author full receipt mismatch')
            else:require(result==parse(snapshot['audit/REPLAY_RECEIPT.json']),'Audit full receipt mismatch')
            results[label]={'status':'pass','receipt_sha256':digest(process.stdout)}
        return results

def main():
    require(len(sys.argv)==3,'Expected external manifest pin and packet path')
    pin=sys.argv[1];root=Path(os.path.abspath(sys.argv[2]));snapshot=integrity(root,pin)
    result={'schema':'unitary-publication-replay-v1','problem_id':30001738,'status':'pass','python_optimization':sys.flags.optimize,'manifest_sha256':pin,'verified_payload_files':len(snapshot),'replays':replay(snapshot),'author_checks':3044,'synthetic_multisets':494,'audit_integrity_rejections':22,'audit_semantic_rejections':16,'limits':'Byte integrity and finite diagnostics, not proof of the cited analytic theorem.'}
    require(integrity(root,pin)==snapshot,'Input changed during replay')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(1)
