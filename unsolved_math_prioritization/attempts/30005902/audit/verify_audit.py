#!/usr/bin/env python3
"""Authenticate the audit inventory and replay its separate exact certificate."""
import argparse,hashlib,json,shutil,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path
FILES={'AUDIT_REPORT.md','AUDIT_RESULT.json','AUTHOR_REPLAY.json','IDENTITY_RESULTS.json','INDEPENDENT_RESULTS.json','README.md','REPOSITORY_RECHECK.json','SOURCE_RECHECK.json','check_identity.py','independent_check.py','verify_audit.py'}
AUTHOR_SHA='ff9116239038710665c590fa392318df98aa368171545db229cebb912a7cd2f8'
AUTHOR_MANIFEST='0fcd8510f2eede331a5a2bb9c2c55d21d2448e21515cdc494a2771d8c33ee281'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,msg):
    if not v:raise ValueError(msg)
def check(root,pin=None,replay=True):
    root=Path(root);need(root.is_dir() and not root.is_symlink(),'Root')
    paths=list(root.rglob('*'));need(all(p.is_file() and not p.is_symlink() for p in paths),'Non-file or symlink')
    need({p.relative_to(root).as_posix() for p in paths}==FILES|{'MANIFEST.json'},'Inventory')
    raw=(root/'MANIFEST.json').read_bytes();digest=sha(raw)
    if pin is not None:need(digest==pin,'External pin')
    m=json.loads(raw);need(set(m)=={'format','problem_id','files'} and m['format']==1 and m['problem_id']=='30005902','Manifest schema')
    need(set(m['files'])==FILES,'Manifest inventory')
    for n in sorted(FILES):
        b=(root/n).read_bytes();need(m['files'][n]=={'bytes':len(b),'sha256':sha(b)},'File identity: '+n)
    r=json.loads((root/'AUDIT_RESULT.json').read_bytes())
    need(r['verdict']=='ACCEPT_WITH_EXPLICIT_SCOPE' and r['required_mathematical_corrections']==[],'Disposition')
    need(r['original_author_zip']['sha256']==AUTHOR_SHA and r['original_author_zip']['manifest_sha256']==AUTHOR_MANIFEST,'Author linkage')
    need(r['novelty_claim'] is False and r['remote_writes'] is False,'Scope')
    if replay:
        p=subprocess.run([sys.executable,'-B',str(root/'independent_check.py')],capture_output=True,check=True)
        need(p.stdout==(root/'INDEPENDENT_RESULTS.json').read_bytes(),'Independent replay bytes')
    return {'status':'PASS','manifest_sha256':digest,'external_pin_checked':pin is not None,'file_count':len(FILES)+1,'independent_math_replayed':replay}
def author_check(path,root):
    raw=Path(path).read_bytes();need(sha(raw)==AUTHOR_SHA and len(raw)==21055,'Author ZIP identity')
    with tempfile.TemporaryDirectory(prefix='hopf-author-audit-') as d:
        with zipfile.ZipFile(path) as z:
            ns=z.namelist();need(len(ns)==len(set(ns))==13,'Author ZIP count')
            for item in z.infolist():
                need('/' not in item.filename and '\\' not in item.filename and item.filename not in {'.','..'},'Author ZIP paths')
                need(stat.S_ISREG(item.external_attr>>16),'Author ZIP regular members')
            z.extractall(d)
        p=subprocess.run([sys.executable,'-B',str(Path(d)/'verify_packet.py'),'--manifest-sha256',AUTHOR_MANIFEST,'--negative-controls'],capture_output=True,check=True)
        need(p.stdout==(root/'AUTHOR_REPLAY.json').read_bytes(),'Author replay bytes')
    return {'status':'PASS','sha256':AUTHOR_SHA,'manifest_sha256':AUTHOR_MANIFEST,'original_assertions':26584,'original_mathematical_negative_controls':4,'original_integrity_negative_controls':8}
def negatives(root,pin):
    names=[]
    def trial(name,fn):
        with tempfile.TemporaryDirectory(prefix='hopf-audit-mutation-') as d:
            p=Path(d)/'packet';shutil.copytree(root,p);fn(p)
            try:check(p,pin,False)
            except (ValueError,FileNotFoundError,json.JSONDecodeError):names.append(name)
            else:raise AssertionError('False packet accepted: '+name)
    trial('changed_report',lambda p:(p/'AUDIT_REPORT.md').write_text('changed'))
    trial('changed_result',lambda p:(p/'INDEPENDENT_RESULTS.json').write_text('{}'))
    trial('changed_code',lambda p:(p/'independent_check.py').write_text('pass'))
    trial('missing_file',lambda p:(p/'SOURCE_RECHECK.json').unlink())
    trial('extra_file',lambda p:(p/'extra.txt').write_text('extra'))
    trial('extra_directory',lambda p:(p/'extra').mkdir())
    def symlink(p):
        (p/'SOURCE_RECHECK.json').unlink();(p/'SOURCE_RECHECK.json').symlink_to('README.md')
    trial('symlink',symlink)
    def rebind(p):
        f=p/'AUDIT_REPORT.md';f.write_bytes(f.read_bytes()+b'changed');m=json.loads((p/'MANIFEST.json').read_bytes());m['files'][f.name]={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())};(p/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    trial('rebound_manifest_external_pin',rebind)
    return names
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256');ap.add_argument('--negative-controls',action='store_true');ap.add_argument('--author-zip');a=ap.parse_args()
    root=Path(__file__).resolve().parent;out=check(root,a.manifest_sha256)
    if a.negative_controls:out['rejected_negative_controls']=negatives(root,a.manifest_sha256 or out['manifest_sha256'])
    if a.author_zip:out['original_author_replay']=author_check(a.author_zip,root)
    if a.manifest_sha256 is None:out['qualification']='Internal consistency only; compare against the separately supplied manifest digest.'
    print(json.dumps(out,indent=2,sort_keys=True))
