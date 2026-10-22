#!/usr/bin/env python3
"""Check this review's public map and the exact frozen candidate; optional replay.

Supply an external --expected-manifest pin to authenticate MANIFEST.json itself.
The source bodies/renders are deliberately absent. Replays never recertify them.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,stat,subprocess,sys,tempfile,zipfile

HERE=Path(__file__).absolute().parent
ROOT=HERE.parent.parent
FREEZE_PIN='c58e74cd19d42ac1b867dc9add2f6c3ab9075248dcac0e19432f851ccba7509f'
PACKAGE_PIN='0189e0ecd7bb39a1ed3899ee785cfc9f48bae7fdf386cd3002fd0a4849b70313'
def require(ok,label):
    if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(data):
    def pairs(xs):
        out={}
        for k,v in xs:require(k not in out,'duplicate key');out[k]=v
        return out
    def invalid(v):raise RuntimeError('nonfinite JSON: '+v)
    return json.loads(data,object_pairs_hook=pairs,parse_constant=invalid)
def fp(p):
    require(stat.S_ISREG(p.lstat().st_mode),'not a regular file: '+str(p))
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected-manifest')
    ap.add_argument('--extract',action='store_true')
    ap.add_argument('--replay',action='store_true')
    args=ap.parse_args()
    raw=(HERE/'MANIFEST.json').read_bytes();pin=sha(raw)
    if args.expected_manifest:require(pin==args.expected_manifest,'external review manifest mismatch')
    m=strict(raw);files=m['files'];require(set(files)==set(m['explicit_public_allowlist']),'review allowlist')
    require('MANIFEST.json' not in files,'manifest must exclude itself')
    actual={p.name for p in HERE.iterdir() if p.name!='tmp'}
    require(actual==set(files)|{'MANIFEST.json'},'unexpected public entry')
    for n,v in files.items():require(fp(HERE/n)==v,'review fingerprint: '+n)
    freeze=ROOT/'publication/PREPUBLICATION_FREEZE.json';require(sha(freeze.read_bytes())==FREEZE_PIN,'candidate freeze pin')
    f=strict(freeze.read_bytes());require(len(f['files'])==14,'14 frozen files')
    for n,v in f['files'].items():require(fp(ROOT/'publication'/n)==v,'frozen payload: '+n)
    snap=strict((ROOT/'ORIGINAL_SNAPSHOT.json').read_bytes());require(snap['head']=='d186dea31791cd3e8acf6829e0b65d01849623b8' and len(snap['files'])==28,'original target')
    for n,v in snap['files'].items():require(fp(ROOT/'original'/n)['sha256']==v,'original: '+n)
    archive=ROOT/'publication/rough-m-arrangements-source-verification-v1.0.zip'
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();require(len(names)==len(set(names))==106,'zip inventory')
        package_raw=z.read('PACKAGE_MANIFEST.json');require(sha(package_raw)==PACKAGE_PIN,'external package manifest')
        require((ROOT/'ORIGINAL_SNAPSHOT.json').read_bytes()==z.read('ORIGINAL_SNAPSHOT.json'),'original snapshot external package binding')
        p=strict(package_raw);require(set(names)==set(p['files'])|{'PACKAGE_MANIFEST.json'},'closed zip files')
        for i in z.infolist():
            q=PurePosixPath(i.filename);require(not q.is_absolute() and q.as_posix()==i.filename and '..' not in q.parts,'unsafe zip name')
            require(stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG,'zip nonregular')
        for n,v in p['files'].items():
            b=z.read(n);require({'bytes':len(b),'sha256':sha(b)}==v,'zip payload: '+n)
        if args.extract or args.replay:
            destination=HERE/'tmp/extracted'
            if not destination.exists():destination.mkdir(parents=True);z.extractall(destination)
            actual={x.relative_to(destination).as_posix() for x in destination.rglob('*') if x.is_file()}
            require(actual==set(names),'extracted file inventory')
            for n in names:require((destination/n).read_bytes()==z.read(n),'actual extraction byte mismatch')
    replay=False
    if args.replay:
        require(sys.flags.optimize==0 and sys.flags.isolated==1,'run replay verifier with -I -B and normal optimization')
        exact=subprocess.run([sys.executable,'-I','-B',str(HERE/'independent_checks.py')],capture_output=True,text=True,check=True)
        require(strict(exact.stdout)==strict((HERE/'INDEPENDENT_CHECKS.json').read_bytes()),'independent exact result')
        with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='review_replay_receipt_') as td:
            out=Path(td)/'result.json'
            subprocess.run([sys.executable,'-I','-B',str(HERE/'replay_and_guards.py'),'--output',str(out)],check=True)
            result=strict(out.read_bytes());require(result['status']=='PASS' and len(result['full_replays'])==4 and result['negative_control_count']==22,'fresh replay result')
        replay=True
    print(json.dumps({'status':'PASS','review_manifest_sha256':pin,'review_external_anchor_checked':args.expected_manifest is not None,'public_files':len(files),'frozen_files':14,'original_files':28,'package_payload_files':105,'fresh_replay_performed':replay,'source_bodies_retrieved_or_recertified':False},indent=2))
if __name__=='__main__':main()
