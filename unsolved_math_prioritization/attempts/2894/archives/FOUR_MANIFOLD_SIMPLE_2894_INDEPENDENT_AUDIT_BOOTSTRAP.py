#!/usr/bin/env python3
"""Verify exact independent-audit artifact and replay its bound acceptance checks."""
import hashlib,json,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path
MANIFEST='FOUR_MANIFOLD_SIMPLE_2894_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'
MANIFEST_SHA='3e3f1b1b18b82726222749ca66c8d49739adfbd8b9f8bd4ac6ec4d61c23b2cfa'
ARCHIVE='FOUR_MANIFOLD_SIMPLE_2894_INDEPENDENT_AUDIT_SAFE.zip'
ARCHIVE_SHA='0f80d3891fcb60409ffcd6e43dc262a3c0ef2df2beaa8a2702d8c88a73681f1d'
ARCHIVE_BYTES=53146

def require(ok,msg):
    if not ok: raise ValueError(msg)
def h(b): return hashlib.sha256(b).hexdigest()
def main():
    require(len(sys.argv)<=2,'Usage: bootstrap.py [ARTIFACT_DIRECTORY]')
    root=Path(sys.argv[1]) if len(sys.argv)==2 else Path(__file__).resolve().parent
    mp=root/MANIFEST; zp=root/ARCHIVE
    require(mp.is_file() and not mp.is_symlink(),'Invalid manifest')
    require(h(mp.read_bytes())==MANIFEST_SHA,'External audit manifest pin mismatch')
    m=json.loads(mp.read_text())
    require(zp.is_file() and not zp.is_symlink(),'Invalid archive')
    require(zp.stat().st_size==ARCHIVE_BYTES and h(zp.read_bytes())==ARCHIVE_SHA,'Audit archive pin mismatch')
    require(m['zip']['sha256']==ARCHIVE_SHA and m['zip']['bytes']==ARCHIVE_BYTES,'Archive binding contradiction')
    names=[r['path'] for r in m['files']]
    require(len(names)==len(set(names))==22,'Invalid manifest inventory')
    require(all(n==Path(n).name and n not in ('','.','..') for n in names),'Unsafe manifest name')
    with tempfile.TemporaryDirectory(prefix='four manifold exact audit ') as td:
        out=Path(td)
        with zipfile.ZipFile(zp) as z:
            entries=z.infolist(); actual=[x.filename for x in entries]
            require(len(actual)==len(set(actual)) and set(actual)==set(names),'Archive inventory mismatch')
            for e in entries:
                require(not e.is_dir() and stat.S_IFMT(e.external_attr>>16)==stat.S_IFREG,'Unsafe archive member')
                (out/e.filename).write_bytes(z.read(e))
        for r in m['files']:
            b=(out/r['path']).read_bytes(); require(len(b)==r['bytes'] and h(b)==r['sha256'],'Audit file mismatch')
        replay=[]
        for opt in (False,True):
            for script,args in [('verify_acceptance.py',[]),('check_hu_parity.py',['--check',str(out/'HU_PARITY_RESULTS.json')])]:
                cp=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(out/script)]+args,capture_output=True,text=True,timeout=60)
                require(cp.returncode==0,'Bound audit replay failed: '+script)
                replay.append({'script':script,'optimized':opt,'passed':True})
    print(json.dumps({'result':'pass','audit_files':22,'zip_sha256':ARCHIVE_SHA,'canonical_status':'unsolved','turns':'1/5','replay':replay,'theorem_certification':False},sort_keys=True))
if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(json.dumps({'result':'fail','error':str(exc)},sort_keys=True),file=sys.stderr); sys.exit(1)
