"""Authenticate this test script via verify_packet.py before running it.

Tests use disposable copies; source packets and pins are never rewritten.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(p, message):
    if not p:
        raise RuntimeError(message)


need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode, 'use -I -S -B')
need(len(sys.argv) == 4, 'ROOT MANIFEST_SHA256 CHECKER_SHA256 required')
source = Path(sys.argv[1]).absolute()
mpin, cpin = sys.argv[2:]
results = []
with tempfile.TemporaryDirectory(prefix='Frobenius controls ') as temp:
    scratch = Path(temp).resolve()
    hostile = scratch/'hostile cwd'
    hostile.mkdir()
    marker = scratch/'SHOULD_NOT_EXIST'
    injection = "open("+repr(str(marker))+",'w').write('executed')\nraise RuntimeError('hostile import')\n"
    for name in ['fractions.py', 'json.py', 'sitecustomize.py', 'usercustomize.py']:
        (hostile/name).write_text(injection)
    environment = dict(os.environ, PYTHONPATH=str(hostile), PYTHONSTARTUP=str(hostile/'sitecustomize.py'))

    def run(root, name, expected, optimized=False, pin=mpin, code_pin=cpin, flags=None):
        fs = flags if flags is not None else ['-I', '-S', '-B']+(['-O'] if optimized else [])
        # Missing-isolation rejection is tested without hostile imports, since
        # Python can import environment-controlled modules before our code runs.
        env = environment if '-I' in fs else {k:v for k,v in os.environ.items()
                                               if k not in {'PYTHONPATH','PYTHONSTARTUP'}}
        cwd = hostile if '-I' in fs else scratch
        p = subprocess.run([sys.executable]+fs+[str(root/'verify_packet.py'), str(root), pin, code_pin],
                           cwd=cwd, env=env, capture_output=True, text=True)
        actual = p.returncode == 0
        need(actual == expected, name+': '+p.stderr)
        need(not marker.exists(), 'hostile marker executed')
        results.append({'name': name, 'expected_pass': expected, 'actual_pass': actual})

    run(source, 'normal authenticated original', True)
    run(source, 'optimized authenticated original', True, optimized=True)

    def copy(name):
        d = scratch/name
        shutil.copytree(source, d)
        return d

    run(copy('relocated packet with spaces'), 'relocation and hostile cwd', True)
    d = copy('proof tamper'); (d/'REPORT.md').write_text('changed')
    run(d, 'changed report rejected', False)
    d = copy('checker payload tamper'); (d/'exact_checker.py').write_text(injection)
    run(d, 'changed executable rejected before execution', False)
    d = copy('extra file'); (d/'extra.txt').write_text('extra')
    run(d, 'extra file rejected', False)
    d = copy('missing file'); (d/'EXPECTED.json').unlink()
    run(d, 'missing expected rejected', False)
    d = copy('cache directory'); (d/'__pycache__').mkdir()
    run(d, 'cache directory rejected', False)
    d = copy('symlink member'); (d/'REPORT.md').unlink(); (d/'REPORT.md').symlink_to(source/'REPORT.md')
    run(d, 'symlink member rejected', False)
    d = scratch/'symlink root'; d.symlink_to(source, target_is_directory=True)
    run(d, 'symlink root rejected', False)
    d = copy('symlink manifest'); (d/'MANIFEST.json').unlink(); (d/'MANIFEST.json').symlink_to(source/'MANIFEST.json')
    run(d, 'symlink manifest rejected', False)
    d = copy('changed manifest'); (d/'MANIFEST.json').write_text('{}')
    run(d, 'changed manifest rejected', False)
    run(source, 'wrong manifest pin rejected', False, pin='0'*64)
    run(source, 'wrong checker pin rejected', False, code_pin='0'*64)
    run(source, 'nonisolated invocation rejected', False, flags=['-S','-B'])

    # Deliberately authenticate a modified math input to distinguish mathematical
    # checks from mere hash rejection. These are bounded source transformations.
    for label, filename, old, new in [
        ('wrong Tate wedge detected', 'exact_checker.py', 'quartic = (1, 3, 13, 15)', 'quartic = (1, 3, 13, 14)'),
        ('wrong expected arithmetic detected', 'EXPECTED.json', '"hodge_determinant": 256', '"hodge_determinant": 255')]:
        d = copy(label)
        p = d/filename
        text = p.read_text()
        need(old in text, 'bounded mutation target')
        p.write_text(text.replace(old,new,1))
        m = json.loads((d/'MANIFEST.json').read_text())
        b = p.read_bytes()
        m['files'][filename] = {'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
        (d/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
        pin = hashlib.sha256((d/'MANIFEST.json').read_bytes()).hexdigest()
        run(d,label,False, pin=pin)

print(json.dumps({'control_count':len(results),'all_expected':True,
                  'untrusted_marker_executed':False,'controls':results}, indent=2))
