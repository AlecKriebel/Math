#!/usr/bin/env python3
"""Unprivileged checks against the final frozen distribution; only temp copies mutate."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
class TestError(Exception):pass
def require(ok,message):
    if not ok:raise TestError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(root):return {str(p.relative_to(root)):sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}
def writable(root):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
def copy_package(base,dest):
    dest.mkdir()
    for name in ('AUTHOR_MANIFEST.json','bootstrap.py'):shutil.copy2(base/name,dest/name)
    shutil.copytree(base/'packet',dest/'packet')
    # copy2/copytree preserve immutable distribution modes; mutations need writable TEMP copies.
    writable(dest)
def command(root,mode,args=(),direct=False,cwd=None):
    flags=[] if mode=='normal' else [mode]
    script=root/'packet/verify.py' if direct else root/'bootstrap.py'
    return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=cwd or root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
def main():
    require(len(sys.argv)==1,'no arguments')
    require(os.getuid()!=0,'must run unprivileged')
    base=Path(__file__).resolve().parent;names=sorted(p.name for p in (base/'packet').iterdir())
    original=snapshot(base);positives=[];negatives=[];semantics=[];modes=('normal','-O','-OO')
    with tempfile.TemporaryDirectory(prefix='fixed-span-controls-') as td:
        temp=Path(td);expected=None
        for mode in modes:
            r=command(base,mode,cwd=temp);require(r.returncode==0,'original replay '+mode+':'+r.stderr.decode())
            expected=expected or r.stdout;require(r.stdout==expected,'mode-dependent output')
            positives.append({'layout':'final-freeze','mode':mode})
        relocated=temp/'relocated';copy_package(base,relocated)
        for p in relocated.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
        relocated.chmod(0o555);before=snapshot(relocated);denied=False
        try:(relocated/'packet'/'forbidden').write_text('bad')
        except PermissionError:denied=True
        require(denied,'read-only not enforced')
        for mode in modes:
            r=command(relocated,mode,cwd=temp)
            require(r.returncode==0 and r.stdout==expected,'read-only relocated replay '+mode)
            positives.append({'layout':'relocated-read-only','mode':mode})
        require(snapshot(relocated)==before,'read-only bytes changed');writable(relocated)
        cases=[]
        for name in names:
            cases.append(('byte-drift-'+name,lambda d,name=name:(d/'packet'/name).write_bytes((d/'packet'/name).read_bytes()+b'!')))
            cases.append(('missing-'+name,lambda d,name=name:(d/'packet'/name).unlink()))
        cases += [('extra-file',lambda d:(d/'packet/unexpected').write_text('extra')),
                  ('extra-directory',lambda d:(d/'packet/unexpected').mkdir()),
                  ('malformed-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').write_text('{bad')),
                  ('missing-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').unlink())]
        def wrong(d):
            p=d/'packet/CLAIMS.json';c=json.loads(p.read_text());c['full_resolution']=True;p.write_text(json.dumps(c))
        cases.append(('false-solution',wrong))
        def selfconsistent(d):
            wrong(d);p=d/'AUTHOR_MANIFEST.json';m=json.loads(p.read_text())
            for e in m['files']:
                if e['path']=='CLAIMS.json':b=(d/'packet/CLAIMS.json').read_bytes();e.update(bytes=len(b),sha256=sha(b))
            p.write_text(json.dumps(m))
        cases.append(('self-consistent-forged-manifest',selfconsistent))
        def symlink(d):
            p=d/'packet/CLAIMS.json';b=p.read_bytes();p.unlink();target=d/'outside';target.write_bytes(b);p.symlink_to(target)
        cases.append(('symlink-payload',symlink))
        def untrusted(d):(d/'packet/verify.py').write_text("from pathlib import Path\nPath('../EXECUTED').write_text('unsafe')\n")
        cases.append(('untrusted-code-before-authentication',untrusted))
        for i,(label,mutate) in enumerate(cases):
            d=temp/('mutation-'+str(i));copy_package(base,d);mutate(d)
            for mode in modes:
                r=command(d,mode,cwd=temp)
                require(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'mutation accepted or unclear: '+label+' '+mode)
                require(not (d/'EXECUTED').exists(),'untrusted code executed')
                negatives.append({'case':label,'mode':mode})
        # Authenticated unchanged verifier is also tested against semantic and malformed inputs.
        c=json.loads((base/'packet/CLAIMS.json').read_text());bad=[]
        for key in ('full_resolution','knot_counterexample','formal_specializations_are_realized','novelty_claimed','finite_checks_are_proof'):
            z=dict(c);z[key]=True;bad.append((key,json.dumps(z)))
        for key in ('fixed_braid_index_required','fixed_adequate_diagram_genus_required','fixed_twist_exterior_required'):
            z=dict(c);z[key]=False;bad.append((key,json.dumps(z)))
        z=dict(c);z['traczyk_components']=1;bad.append(('links-promoted-to-knots',json.dumps(z)))
        z=dict(c);z['approaches']=True;bad.append(('boolean-as-integer',json.dumps(z)))
        z=dict(c);z['unexpected']=0;bad.append(('extra-key',json.dumps(z)))
        z=dict(c);del z['status'];bad.append(('missing-key',json.dumps(z)))
        bad.extend([('malformed-json','{bad'),('duplicate-json-key','{"schema":1,"schema":2}'),('nonfinite-json','{"schema":NaN}')])
        for label,body in bad:
            p=temp/(label+'.json');p.write_text(body)
            for mode in modes:
                r=command(base,mode,('--claims',p),direct=True,cwd=temp)
                require(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'semantic input accepted: '+label)
                semantics.append({'case':label,'mode':mode})
        require(snapshot(base)==original,'original freeze bytes changed')
    return {'schema':'fixed-span-replay-controls-v1','status':'PASS','positive_count':len(positives),'negative_count':len(negatives),'semantic_negative_count':len(semantics),'mutation_cases':len(cases),'semantic_cases':len(bad),'unprivileged_uid':os.getuid(),'read_only_write_denied':denied,'original_and_relocated_bytes_unchanged':True,'positives':positives,'negatives':negatives,'semantic_negatives':semantics,'scope':'Integrity and finite algebra diagnostics; no independent mathematical review or hosted CI claim.'}
if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except (TestError,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
