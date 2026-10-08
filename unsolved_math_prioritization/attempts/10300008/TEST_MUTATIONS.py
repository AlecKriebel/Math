#!/usr/bin/env python3
"""Exercise the frozen publication boundary using a separate trusted launcher."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
class Failure(Exception):pass
def need(c,m):
    if not c:raise Failure(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(r):return {str(p.relative_to(r)):sha(p.read_bytes()) for p in r.rglob('*') if p.is_file() and not p.is_symlink()}
def thaw(r):
    r.chmod(0o755)
    for p in r.rglob('*'):
        if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
def copy(src,dst):shutil.copytree(src,dst);thaw(dst)
def main():
    need(len(sys.argv)==1,'no arguments supported')
    root=Path(__file__).resolve().parent;before=snapshot(root);flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    def run(r,integrity=False):
        args=[sys.executable,'-I','-S','-B']+flags+[str(root/'BOOTSTRAP.py'),str(r)]+(['--integrity-only'] if integrity else [])
        return subprocess.run(args,cwd=r.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
    positives=[];negative=[]
    with tempfile.TemporaryDirectory(prefix='minimal-wrapper-controls-') as tmp:
        top=Path(tmp)
        for label,readonly in [('relocated',False),('relocated-read-only',True)]:
            d=top/label;copy(root,d)
            if readonly:
                for p in d.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
                d.chmod(0o555);denied=False
                try:(d/'UNEXPECTED_WRITE').write_bytes(b'x')
                except PermissionError:denied=True
                need(denied,'read-only permissions not enforced')
            cp=run(d,True);need(cp.returncode==0 and cp.stderr==b'','positive control rejected')
            need(snapshot(d)==before,'positive copy changed');positives.append(label);thaw(d)
        cases=[]
        for n in sorted(before):
            cases.append(('byte:'+n,lambda d,n=n:(d/n).write_bytes((d/n).read_bytes()+b'!')))
            cases.append(('missing:'+n,lambda d,n=n:(d/n).unlink()))
        cases.extend([
            ('extra-file',lambda d:(d/'EXTRA.txt').write_text('unexpected')),
            ('extra-empty-directory',lambda d:(d/'EXTRA').mkdir()),
            ('malformed-manifest',lambda d:(d/'PUBLICATION_MANIFEST.json').write_bytes(b'{')),
            ('duplicate-key-manifest',lambda d:(d/'PUBLICATION_MANIFEST.json').write_bytes(b'{"files":[],"files":[]}')),
        ])
        def symlink_file(d):
            p=d/'author_original/packet/PROOF.md';p.unlink();p.symlink_to(root/'author_original/packet/PROOF.md')
        def symlink_dir(d):
            p=d/'author_original/packet';shutil.rmtree(p);p.symlink_to(root/'author_original/packet',target_is_directory=True)
        cases.extend([('symlink-proof',symlink_file),('symlink-directory',symlink_dir)])
        def forge(d):
            p=d/'audit/ACCEPTANCE.json';j=json.loads(p.read_text());j['general_resolution']=True;p.write_text(json.dumps(j))
            m=d/'PUBLICATION_MANIFEST.json';j=json.loads(m.read_text())
            for e in j['files']:
                if e['path']=='audit/ACCEPTANCE.json':b=p.read_bytes();e.update(bytes=len(b),sha256=sha(b))
            m.write_text(json.dumps(j))
        cases.append(('self-consistent-solved-forgery',forge))
        def corrupt_patch(d):
            p=d/'audit/HARNESS_CORRECTION.patch';p.write_bytes(p.read_bytes().replace(b'0o644',b'0o666'))
        cases.append(('patch-substitution',corrupt_patch))
        for n in ['VERIFY_PUBLICATION.py','BOOTSTRAP.py','author_original/bootstrap.py','author_corrected/bootstrap.py','author_corrected/test_bootstrap.py','audit/independent_verify.py']:
            def code(d,n=n):
                (d/n).write_text('from pathlib import Path\nPath('+repr(str(d/'HOSTILE_EXECUTED'))+').write_text("bad")\n')
            cases.append(('hostile-code:'+n,code))
        for index,(name,mutate) in enumerate(cases):
            d=top/('case-'+str(index));copy(root,d);mutate(d);cp=run(d)
            need(cp.returncode==1 and cp.stderr.startswith(b'REJECT:'),'mutation did not fail closed: '+name)
            need(not (d/'HOSTILE_EXECUTED').exists(),'unauthenticated code executed: '+name)
            negative.append(name)
        link=top/'symlink-root';link.symlink_to(root,target_is_directory=True);cp=run(link)
        need(cp.returncode==1 and cp.stderr.startswith(b'REJECT:'),'symlink root accepted');negative.append('symlink-root')
    need(snapshot(root)==before,'original publication changed')
    return {'schema':'minimal-surfaces-publication-controls-v1','status':'pass','positive_count':len(positives),'positive_cases':positives,'negative_count':len(negative),'rejected_cases':negative,'read_only_write_denied':True,'source_bytes_unchanged':True,'trust_boundary':'Separate trusted original BOOTSTRAP.py authenticates each candidate tree; the bootstrap and manifest hashes must themselves be checked against external pins.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Failure,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
