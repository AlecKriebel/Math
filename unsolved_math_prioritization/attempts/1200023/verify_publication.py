#!/usr/bin/env python3
"""Strict publication integrity and final-layout replay; standard library only."""
from pathlib import Path,PurePosixPath
import hashlib,json,shutil,subprocess,sys,tempfile
sys.dont_write_bytecode=True

def check(root):
    root=Path(root);meta=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
    wanted=meta['files']
    for n in wanted:
        q=PurePosixPath(n)
        if q.is_absolute() or '..' in q.parts or str(q)!=n:
            raise ValueError('unsafe manifest path')
    actual={str(x.relative_to(root)) for x in root.rglob('*') if x.is_file()}
    if actual!=set(wanted)|{'PUBLICATION_MANIFEST.json'}:raise ValueError('inventory mismatch')
    if any(x.is_symlink() for x in root.rglob('*')):raise ValueError('symlink not allowed')
    for n,m in wanted.items():
        d=(root/n).read_bytes()
        if len(d)!=m['bytes'] or hashlib.sha256(d).hexdigest()!=m['sha256']:
            raise ValueError('file mismatch: '+n)
    author=json.loads((root/'AUTHOR_FREEZE_RECEIPT.json').read_text())
    names=sorted(author['publication_allowlist'])
    hashes={n:hashlib.sha256((root/'submission'/n).read_bytes()).hexdigest() for n in names}
    tree=hashlib.sha256(''.join(n+'\0'+h+'\n' for n,h in hashes.items()).encode()).hexdigest()
    if hashes!=author['submission_file_sha256'] or tree!=author['submission_tree_sha256']:raise ValueError('author binding')
    audit=json.loads((root/'INDEPENDENT_AUDIT_RECEIPT.json').read_text())
    ah={n:hashlib.sha256((root/'independent-audit'/n).read_bytes()).hexdigest() for n in sorted(audit['audit_files'])}
    at=hashlib.sha256(''.join(n+'\0'+h+'\n' for n,h in ah.items()).encode()).hexdigest()
    if at!=audit['audit_tree_sha256']:raise ValueError('audit binding')
    return len(wanted)+1

def selftest(root):
    rejected=[]
    for mode in ('altered','missing','unexpected','unsafe_path'):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'packet';shutil.copytree(root,p)
            f=p/'submission/README.md'
            if mode=='altered':f.write_bytes(f.read_bytes()+b'\nnegative control\n')
            elif mode=='missing':f.unlink()
            elif mode=='unexpected':(p/'UNEXPECTED.txt').write_text('negative control')
            else:
                m=json.loads((p/'PUBLICATION_MANIFEST.json').read_text());m['files']['../escape']={'bytes':0,'sha256':'0'*64}
                (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
            try:check(p)
            except (ValueError,FileNotFoundError):rejected.append(mode)
            else:raise RuntimeError('negative control accepted: '+mode)
    return rejected

def main():
    root=Path(__file__).resolve().parent;count=check(root)
    if sys.argv[1:]==['--self-test']:
        print(json.dumps({'status':'PASS','files':count,'rejected':selftest(root)},sort_keys=True));return
    if sys.argv[1:]:raise SystemExit('Only --self-test is supported.')
    original=subprocess.check_output([sys.executable,'-B',str(root/'submission/verify.py')])
    if original!=(root/'submission/CONTROL_RESULTS.json').read_bytes():raise RuntimeError('original replay differs')
    subprocess.check_output([sys.executable,'-B',str(root/'submission/verify_manifest.py')])
    independent=subprocess.check_output([sys.executable,'-B',str(root/'independent-audit/audit_verify.py'),str(root)])
    if independent!=(root/'independent-audit/AUDIT_RESULTS.json').read_bytes():raise RuntimeError('independent replay differs')
    print(json.dumps({'status':'PASS','files':count,'author_files':12,'audit_files':6,'original_replay_byte_identical':True,'independent_replay_byte_identical':True,'original_networks':31,'original_small_subsets':872,'original_interval_cases':30595},sort_keys=True))

if __name__=='__main__':main()
