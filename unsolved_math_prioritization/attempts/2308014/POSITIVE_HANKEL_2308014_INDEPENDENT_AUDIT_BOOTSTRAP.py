#!/usr/bin/env python3
"""Pin the independent audit envelope before executing any packaged code.
Usage: python3 -I -B BOOTSTRAP.py AUDIT.zip AUDIT_EXTERNAL_MANIFEST.json
"""
import hashlib,json,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
ARCHIVE_SHA='dbf3e1018e29b3a2663368357823ec29a87c49e5eea35ce110bb643b6c2ae63e'
ARCHIVE_SIZE=45298
MANIFEST_SHA='526e03b422ea5f3dd433381647b5edeedb6ee8216f0b5608ab193f72b175e4c9'
MANIFEST_SIZE=4758

def need(condition,message):
    if not condition: raise SystemExit(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    need(len(sys.argv)==3,'Usage: BOOTSTRAP.py AUDIT.zip AUDIT_EXTERNAL_MANIFEST.json')
    archive,manifest=map(Path,sys.argv[1:]);a=archive.read_bytes();b=manifest.read_bytes()
    need(len(a)==ARCHIVE_SIZE and sha(a)==ARCHIVE_SHA,'Audit archive pin mismatch; no payload execution')
    need(len(b)==MANIFEST_SIZE and sha(b)==MANIFEST_SHA,'Audit external manifest pin mismatch; no payload execution')
    m=json.loads(b);expected={i['path']:i for i in m['members']}
    need(len(expected)==len(m['members'])==19,'Manifest duplicate or count mismatch')
    with tempfile.TemporaryDirectory(prefix='positive_hankel_sealed_replay_') as td:
        root=Path(td)
        with zipfile.ZipFile(archive) as z:
            infos=z.infolist()
            need(len(infos)==len(expected) and {i.filename for i in infos}==set(expected),'ZIP inventory mismatch')
            for i in infos:
                n=PurePosixPath(i.filename);mode=i.external_attr>>16
                need(not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and stat.S_ISREG(mode),'Unsafe ZIP member')
                payload=z.read(i);e=expected[i.filename]
                need(len(payload)==e['bytes'] and sha(payload)==e['sha256'],'Member pin mismatch: '+i.filename)
                p=root/i.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(payload)
        command=[sys.executable,'-I','-B',str(root/'audit/verify_author_freeze.py'),str(root/'provenance/POSITIVE_HANKEL_2308014_AUTHOR_SAFE_FREEZE.zip'),str(root/'provenance/POSITIVE_HANKEL_2308014_AUTHOR_EXTERNAL_MANIFEST.json')]
        r=subprocess.run(command,cwd=root,text=True,capture_output=True,timeout=60)
        need(r.returncode==0,'Pinned author replay failed: '+r.stderr)
        report=json.loads(r.stdout)
        need(report['result']=='PASS_PINNED_AUTHOR_REPLAY_AND_EXPECTED_NEGATIVE_CONTROLS','Unexpected replay result')
        need(report['exact_sanity_check_counts']['total_exact_checks']==1948 and len(report['checks'])==17,'Unexpected replay count')
        for n,e in expected.items():
            p=root/n;payload=p.read_bytes()
            need(stat.S_ISREG(p.lstat().st_mode) and len(payload)==e['bytes'] and sha(payload)==e['sha256'],'Post-execution member change: '+n)
        need(not list(root.rglob('__pycache__')),'Unexpected bytecode cache')
    print(json.dumps({'result':'PASS_SEALED_INDEPENDENT_AUDIT_REPLAY','archive_sha256':ARCHIVE_SHA,'manifest_sha256':MANIFEST_SHA,'members_verified':19,'exact_finite_sanity_checks':1948,'replay_and_adversarial_controls':17,'optimized_author_execution':'EXPECTED_REJECTION; not an optimized mathematical pass','mathematical_acceptance':'Authored analytic audit accepts the full prior-result reduction; no proof patch','limitations':'Hashes and finite checks do not prove the mathematical theorem'},indent=2))
if __name__=='__main__':main()
