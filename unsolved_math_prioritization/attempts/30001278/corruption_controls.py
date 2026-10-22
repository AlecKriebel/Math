#!/usr/bin/env python3
"""Execute benign mutations in disposable copies; require actual CLI failures."""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, os, pathlib, shutil, subprocess, tempfile

def need(ok, message):
    if not ok: raise RuntimeError(message)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest-sha256',required=True)
    args = ap.parse_args(); root = pathlib.Path(__file__).absolute().parent
    need(hashlib.sha256((root/'PUBLIC_MANIFEST.json').read_bytes()).hexdigest() == args.manifest_sha256,'external anchor')
    m = json.loads((root/'PUBLIC_MANIFEST.json').read_bytes())
    tests = [("changed_"+x['path'],lambda d,n=x['path']:(d/n).write_bytes((d/n).read_bytes()+b'\n# authored harmless mutation\n')) for x in m['files']]
    def coordinated(d):
        f = d/'accepted/01_UPPER_BREAK.md'; f.write_bytes(f.read_bytes()+b'\nAuthored dummy change.\n')
        p = d/'PUBLIC_MANIFEST.json'; obj = json.loads(p.read_bytes())
        x = next(x for x in obj['files'] if x['path']=='accepted/01_UPPER_BREAK.md')
        x.update(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
        p.write_text(json.dumps(obj))
    tests += [
        ('missing_file',lambda d:(d/'accepted/NORMALIZATIONS.md').unlink()),
        ('extra_dummy_pdf',lambda d:(d/'dummy.pdf').write_bytes(b'authored dummy')),
        ('extra_hidden_file',lambda d:(d/'.dummy').write_text('authored dummy')),
        ('empty_directory',lambda d:(d/'unlisted').mkdir()),
        ('payload_symlink',lambda d:((d/'accepted/README.md').unlink(),(d/'accepted/README.md').symlink_to(d/'original/README.md'))),
        ('manifest_symlink',lambda d:((d/'PUBLIC_MANIFEST.json').rename(d.parent/'saved-manifest'),(d/'PUBLIC_MANIFEST.json').symlink_to(d.parent/'saved-manifest'))),
        ('duplicate_manifest_key',lambda d:(d/'PUBLIC_MANIFEST.json').write_text((d/'PUBLIC_MANIFEST.json').read_text().replace('{','{"schema":"duplicate",',1))),
        ('coordinated_prose_and_manifest',coordinated),
    ]
    outcomes = []
    for mode in ('normal','dash_O','environment_2'):
        env = dict(os.environ); env.pop('PYTHONOPTIMIZE',None); env['PYTHONDONTWRITEBYTECODE']='1'
        if mode == 'environment_2': env['PYTHONOPTIMIZE']='2'
        flags = ['-O'] if mode == 'dash_O' else []
        for name, change in tests:
            with tempfile.TemporaryDirectory(prefix='ramification-corruption-') as temp:
                copy = pathlib.Path(temp)/'packet'; shutil.copytree(root,copy); change(copy)
                r = subprocess.run([sys.executable,'-B',*flags,str(copy/'verify_publication.py'),'--manifest-sha256',args.manifest_sha256,'--integrity-only'],capture_output=True,cwd=temp,env=env,timeout=30)
                need(r.returncode != 0 and r.stderr,'mutation accepted: '+mode+' '+name)
                outcomes.append({'test':name,'mode':mode,'returncode':r.returncode})
        with tempfile.TemporaryDirectory(prefix='ramification-root-') as temp:
            link = pathlib.Path(temp)/'root-alias'; link.symlink_to(root,target_is_directory=True)
            r = subprocess.run([sys.executable,'-B',*flags,str(link/'verify_publication.py'),'--manifest-sha256',args.manifest_sha256,'--integrity-only'],capture_output=True,cwd=temp,env=env,timeout=30)
            need(r.returncode != 0 and b'root is a symlink' in r.stderr,'root alias accepted')
            outcomes.append({'test':'direct_root_symlink','mode':mode,'returncode':r.returncode})
    print(json.dumps({'status':'PASS','negative_runs':len(outcomes),'rejections':outcomes,
                      'scope':'Benign actual CLI corruption controls, not a malicious-code sandbox or mathematical proof.'},indent=2,sort_keys=True))

if __name__ == '__main__': main()
