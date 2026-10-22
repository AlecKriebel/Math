"""Fail closed before reading package bytes. Run: python [-O] validate.py."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

EXPECTED = {'RESULT.md','INDEPENDENT_AUDIT.md','ORIGINAL_MANIFEST.json','backward.py','backward_output.txt','extend.py','extend_output.txt','frozen32.py','frozen32_output.txt','linear.py','linear_output.txt','SOURCE_GATE.md','SOURCE_METADATA.json','DATASET_METADATA.json','semantic_checks.py','validate.py','README.md','PROVENANCE.json','MANIFEST.json','REPLAY_RESULTS.json'}
SCRIPTS = ('backward.py','extend.py','frozen32.py','linear.py')

def require(ok, message):
    if not ok: raise ValueError(message)

def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'package root is not a real directory')
    entries = list(os.scandir(root))
    for e in entries:
        require(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode), 'nonregular entry: '+e.name)
    require({e.name for e in entries} == EXPECTED, 'exact inventory mismatch')

def validate(root):
    inventory(root)  # No package content read can precede this check.
    manifest = json.loads((root/'MANIFEST.json').read_text())
    require(set(manifest['files']) == EXPECTED-{'MANIFEST.json'}, 'manifest inventory mismatch')
    for name, item in manifest['files'].items():
        data = (root/name).read_bytes()
        require(len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'], 'hash mismatch: '+name)
    provenance = json.loads((root/'PROVENANCE.json').read_text())
    original = json.loads((root/'ORIGINAL_MANIFEST.json').read_text())
    for item in original['files']:
        name = item['path'].rsplit('/',1)[-1]
        data = (root/name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == item['sha256'] and len(data)==item['bytes'], 'original binding: '+name)
    ns = {}
    exec(compile((root/'semantic_checks.py').read_text(), 'semantic_checks.py','exec'),ns)
    for name in SCRIPTS:
        src = (root/name).read_text()
        tree = ast.dump(ast.parse(src),include_attributes=False)
        require(hashlib.sha256(tree.encode()).hexdigest()==provenance['scripts'][name]['whole_module_ast_sha256'], 'whole AST provenance: '+name)
        ns['check'](name,src)
    results = []
    for mode in ([],['-O']):
        for name in SCRIPTS:
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
            p = subprocess.run([sys.executable,*mode,str(root/name)],cwd=root,env=env,capture_output=True,timeout=240)
            expected = (root/name.replace('.py','_output.txt')).read_bytes()
            require(p.returncode==0 and not p.stderr and p.stdout==expected,'full replay: '+name+' '+repr(mode))
            results.append({'script':name,'mode':'optimized' if mode else 'normal','stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stdout_bytes':len(p.stdout),'returncode':p.returncode})
    require(results==json.loads((root/'REPLAY_RESULTS.json').read_text()),'replay receipt mismatch')
    print('PASS: exact inventory, byte and whole-module AST provenance, semantic controls, eight complete replays; scoped candidate counterexample only.')

if __name__=='__main__':
    validate(Path(__file__).absolute().parent)
