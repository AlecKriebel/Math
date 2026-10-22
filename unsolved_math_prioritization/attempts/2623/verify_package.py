#!/usr/bin/env python3
"""Read-only, relocatable verification of the accepted KOU-21.114 safe package."""
import os
import sys
# Preserve the frozen checkers while preventing Python optimization from disabling checks.
if not __debug__:
    os.environ.pop('PYTHONOPTIMIZE', None)
    os.execv(sys.executable, [sys.executable, '-B', __file__, *sys.argv[1:]])
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile
ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def assertions_sentinel():
    triggered = False
    try:
        exec(compile('assert False, "assertions-enabled sentinel"', '<sentinel>', 'exec', optimize=0))
    except AssertionError:
        triggered = True
    require(triggered and __debug__, 'Assertions are not enabled')

def run(relative, *args):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    launcher = 'import runpy,sys; assert __debug__, "Child assertions disabled"; p=sys.argv[1]; sys.argv=sys.argv[1:]; runpy.run_path(p,run_name="__main__")'
    command = [sys.executable, '-B', '-c', launcher, str(ROOT/relative), *map(str,args)]
    proc = subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True)
    require(proc.returncode == 0, f'{relative} failed\n{proc.stdout}\n{proc.stderr}')
    return proc.stdout

def main():
    assertions_sentinel()
    manifest = json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_text())
    expected = {entry['path'] for entry in manifest['files']}
    paths = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in paths), 'Symlinks are not allowed')
    actual = {p.relative_to(ROOT).as_posix() for p in paths if p.is_file()}
    require(actual == expected|{'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing publication file')
    require(len(expected)==len(manifest['files']), 'Duplicate manifest member')
    for item in manifest['files']:
        data=(ROOT/item['path']).read_bytes()
        require(len(data)==item['bytes'] and digest(data)==item['sha256'], 'Publication hash: '+item['path'])
    archives = {
        'KOUROVKA_2623_AUTHOR_SAFE_FREEZE.zip':'author_v1',
        'KOUROVKA_2623_AUTHOR_V2_SAFE_FREEZE.zip':'author',
        'KOUROVKA_2623_AUDIT_SAFE_FREEZE.zip':'audit',
        'KOUROVKA_2623_V2_DELTA_ACCEPTANCE_SAFE_FREEZE.zip':'acceptance'}
    for filename, directory in archives.items():
        with zipfile.ZipFile(ROOT/'archives'/filename) as z:
            names=z.namelist()
            require(len(names)==len(set(names)) and all(Path(n).name==n for n in names), 'Unsafe ZIP inventory')
            require(z.testzip() is None, 'ZIP CRC failure')
            extracted={p.name for p in (ROOT/directory).iterdir() if p.is_file()}
            require(set(names)==extracted, 'ZIP/extracted inventory mismatch')
            for name in names:
                require(z.read(name)==(ROOT/directory/name).read_bytes(), 'ZIP member mismatch: '+name)
    checks={}
    for name in ['author_v1/verify_manifest.py','author/verify_manifest.py','acceptance/verify_acceptance_manifest.py']:
        checks[name]=json.loads(run(name))
    checks['audit_manifest']=json.loads(run('audit/verify_audit_manifest.py','--author-freeze',ROOT/'archives/KOUROVKA_2623_AUTHOR_SAFE_FREEZE.zip'))
    delta=json.loads(run('acceptance/verify_exact_delta.py','--inputs',ROOT/'archives','--audit-dir',ROOT/'audit'))
    require(delta==json.loads((ROOT/'acceptance/EXACT_DELTA_CHECK.json').read_text()), 'Exact delta differs from accepted record')
    checks['exact_delta']=delta['exact_delta']
    checks['author_math']=json.loads(run('author/verify_math.py'))
    with tempfile.TemporaryDirectory(prefix='kourovka-2623-replay-') as tmp:
        out=Path(tmp)/'independent.json'
        run('audit/independent_verifier.py','--check',ROOT/'audit/INDEPENDENT_RESULTS.json','--compare-author',ROOT/'author/CHECK_RESULTS.json','--output',out)
        independent=json.loads(out.read_text())
        checks['independent_author_comparison']=independent['author_comparison']
    print(json.dumps({'ok':True,'problem_id':2623,'status':'unsolved','turns':'5/5','assertions_enabled':True,'publication_files':len(actual),'archive_count':len(archives),'checks':checks},indent=2))

if __name__=='__main__':
    main()
