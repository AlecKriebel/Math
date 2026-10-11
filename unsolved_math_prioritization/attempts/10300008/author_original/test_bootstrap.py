#!/usr/bin/env python3
"""Replay and mutate isolated source-free copies; never writes the originals."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile

class TestError(Exception):pass
def require(ok,message):
    if not ok:raise TestError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(root):
    return {str(p.relative_to(root)):sha(p.read_bytes())
            for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}
def copy_package(base,dest):
    dest.mkdir()
    for name in ('AUTHOR_MANIFEST.json','bootstrap.py'):shutil.copy2(base/name,dest/name)
    shutil.copytree(base/'packet',dest/'packet')
def command(root,mode):
    flags=[] if mode=='normal' else [mode]
    return subprocess.run([sys.executable,'-I','-S','-B']+flags+[str(root/'bootstrap.py')],
                          cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
def main():
    require(len(sys.argv)==1,'no arguments supported')
    base=Path(__file__).resolve().parent
    names=sorted(p.name for p in (base/'packet').iterdir())
    before=snapshot(base)
    positive=[];negative=[]
    with tempfile.TemporaryDirectory(prefix='minimal-surfaces-check-') as tmp:
        temp=Path(tmp)
        expected=None
        for mode in ('normal','-O','-OO'):
            cp=command(base,mode)
            require(cp.returncode==0,'original replay failed '+mode+': '+cp.stderr.decode())
            if expected is None:expected=cp.stdout
            require(cp.stdout==expected,'mode-dependent output')
            positive.append({'layout':'original','mode':mode,'stdout_sha256':sha(cp.stdout)})
        relocated=temp/'unrelated-layout';copy_package(base,relocated)
        for p in relocated.rglob('*'):
            p.chmod(0o555 if p.is_dir() else 0o444)
        relocated.chmod(0o555)
        denied=False
        try:(relocated/'packet'/'forbidden-write').write_text('unexpected')
        except PermissionError:denied=True
        require(denied,'read-only permissions were not enforced')
        relocated_before=snapshot(relocated)
        for mode in ('normal','-O','-OO'):
            cp=command(relocated,mode)
            require(cp.returncode==0,'read-only replay failed '+mode+': '+cp.stderr.decode())
            require(cp.stdout==expected,'relocated output mismatch')
            require(snapshot(relocated)==relocated_before,'relocated files changed')
            positive.append({'layout':'relocated-read-only','mode':mode,'stdout_sha256':sha(cp.stdout)})
        # Restore permissions only to remove the isolated test copy afterward.
        relocated.chmod(0o755)
        for p in relocated.rglob('*'):p.chmod(0o755 if p.is_dir() else 0o644)
        cases=[]
        for name in names:
            cases.append(('payload-byte-'+name,lambda d,name=name:(d/'packet'/name).write_bytes((d/'packet'/name).read_bytes()+b'!')))
            cases.append(('payload-missing-'+name,lambda d,name=name:(d/'packet'/name).unlink()))
        cases.append(('extra-payload',lambda d:(d/'packet'/'unexpected.txt').write_text('extra')))
        cases.append(('extra-directory',lambda d:(d/'packet'/'unexpected').mkdir()))
        cases.append(('malformed-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').write_text('{bad')))
        cases.append(('missing-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').unlink()))
        def wrong_claim(d):
            p=d/'packet'/'CLAIMS.json';c=json.loads(p.read_text());c['status']='claimed_solved';p.write_text(json.dumps(c))
        cases.append(('wrong-solved-claim',wrong_claim))
        def replaced_manifest(d):
            wrong_claim(d)
            p=d/'AUTHOR_MANIFEST.json';m=json.loads(p.read_text())
            for e in m['files']:
                if e['path']=='CLAIMS.json':
                    b=(d/'packet'/'CLAIMS.json').read_bytes();e.update(bytes=len(b),sha256=sha(b))
            p.write_text(json.dumps(m))
        cases.append(('self-consistent-wrong-claim-manifest',replaced_manifest))
        def symlink_payload(d):
            p=d/'packet'/'CLAIMS.json';content=p.read_bytes();p.unlink()
            target=d/'outside-claims.json';target.write_bytes(content);p.symlink_to(target)
        cases.append(('symlink-payload',symlink_payload))
        def untrusted_code(d):
            (d/'packet'/'verify.py').write_text("from pathlib import Path\nPath('../EXECUTED').write_text('bad')\n")
        cases.append(('untrusted-code-before-authentication',untrusted_code))
        for index,(name,mutate) in enumerate(cases):
            d=temp/('mutation-'+str(index));copy_package(base,d);mutate(d)
            for mode in ('normal','-O','-OO'):
                cp=command(d,mode)
                require(cp.returncode==1,'mutation accepted: '+name+' '+mode)
                require(cp.stderr.startswith(b'REJECT:'),'non-explicit rejection: '+name)
                require(not (d/'EXECUTED').exists(),'unauthenticated code executed')
                negative.append({'case':name,'mode':mode,'rejected':True})
        require(snapshot(base)==before,'original files changed')
    return {'schema':'minimal-surfaces-10300008-replay-v1','status':'pass',
            'positive_runs':positive,'negative_runs':negative,
            'positive_count':len(positive),'negative_count':len(negative),
            'mutation_case_count':len(cases),'read_only_write_denied':denied,
            'original_and_relocated_bytes_unchanged':True,
            'source_free':True,'checks_use_explicit_exceptions':True,
            'scope':'Integrity/replay and finite controls only; no mathematical peer review or CI claim.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (TestError,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
