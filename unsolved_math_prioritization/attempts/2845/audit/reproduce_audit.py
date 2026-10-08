#!/usr/bin/env python3
"""Recheck pinned packets and execute exact controls under a read-only UID-1000 mount.

Usage: python3 reproduce_audit.py ORIGINAL_PUBLIC CORRECTED_PUBLIC
This driver emits JSON; it does not write files. Linux bubblewrap is required.
"""
import ast
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


HERE = Path(__file__).resolve().parent
FROZEN_SHA256 = 'e807c15d1bcd72e46389a6f9955a9a8c6ce73e764b036ae2a08aa356d9b9c4a1'
MODES = [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pins_match(directory, rows):
    require(sorted(p.name for p in directory.iterdir()) == sorted(r['file'] for r in rows), 'exact file inventory')
    for row in rows:
        path = directory/row['file']
        require(path.is_file() and not path.is_symlink(), 'regular non-symlink file')
        data = path.read_bytes()
        require(len(data) == row['bytes'] and digest(data) == row['sha256'], 'pin mismatch: '+row['file'])


def main():
    require(len(sys.argv) == 3, 'supply original and corrected public packet paths')
    original, candidate = map(lambda x: Path(x).resolve(), sys.argv[1:])
    require(os.getuid() == 1000 and os.geteuid() == 1000, 'driver must actually run as UID 1000')
    bwrap = shutil.which('bwrap')
    require(bwrap is not None, 'bubblewrap required; do not silently fall back to chmod')
    original_pins = json.loads((HERE/'FROZEN_INPUTS.json').read_text())
    corrected_pins = json.loads((HERE/'CORRECTED_PACKET_PINS.json').read_text())
    require(digest((original/'MANIFEST.json').read_bytes()) == FROZEN_SHA256, 'frozen manifest authority')
    pins_match(original, original_pins['files'])
    pins_match(candidate, corrected_pins['files'])
    for directory in (original, candidate):
        for row in json.loads((directory/'MANIFEST.json').read_text())['files']:
            data = (directory/row['file']).read_bytes()
            require(len(data) == row['bytes'] and digest(data) == row['sha256'], 'internal manifest')

    def execute(flags, source=None, file=None):
        # No writable rebind or tmpfs is supplied: the complete visible host
        # filesystem is read-only. stdout is collected by the outer driver.
        command = [bwrap, '--ro-bind', '/', '/', '--die-with-parent',
                   sys.executable, '-B', *flags]
        command += [str(file)] if file is not None else ['-']
        return subprocess.run(command, input=source, text=True,
                              capture_output=True, timeout=180, check=False)

    probe = '''import errno,json,os
targets = TARGETS
if os.getuid()!=1000 or os.geteuid()!=1000: raise RuntimeError('wrong UID')
results=[]
for path in targets:
    try:
        fd=os.open(path,os.O_WRONLY)
    except OSError as exc:
        if exc.errno!=errno.EROFS: raise
        results.append({'target':os.path.basename(path),'errno':exc.errno,'name':'EROFS'})
    else:
        os.close(fd)
        raise RuntimeError('filesystem was writable')
print(json.dumps({'uid':os.getuid(),'euid':os.geteuid(),'write_open_denials':results},sort_keys=True))
'''.replace('TARGETS', repr([str(original/'verify_exact.py'), str(candidate/'verify_exact.py'), str(HERE/'independent_checks.py')]))

    mode_results = []
    independent_output = None
    baseline = (original/'EXACT_CHECKS.json').read_text()
    for label, flags in MODES:
        identity = execute(flags, source=probe)
        require(identity.returncode == 0 and not identity.stderr, 'UID/read-only probe: '+label)
        probes = json.loads(identity.stdout)
        executions = []
        for name, directory in [('frozen', original), ('corrected', candidate)]:
            result = execute(flags, file=directory/'verify_exact.py')
            require(result.returncode == 0 and not result.stderr, name+' exact verifier: '+label)
            require(result.stdout == baseline, name+' output not byte-identical to recorded checks')
            executions.append({'packet':name, 'exit_code':result.returncode,
                               'stdout_sha256':digest(result.stdout.encode()), 'stdout_bytes':len(result.stdout.encode())})
        independent = execute(flags, file=HERE/'independent_checks.py')
        require(independent.returncode == 0 and not independent.stderr, 'independent checks: '+label)
        if independent_output is None:
            independent_output = independent.stdout
        require(independent.stdout == independent_output, 'independent outputs differ across optimization modes')
        mode_results.append({'mode':label,'read_only_probe':probes,'original_and_corrected':executions,
                             'independent_stdout_sha256':digest(independent.stdout.encode()),
                             'independent_stdout_bytes':len(independent.stdout.encode())})

    script = (original/'verify_exact.py').read_text()
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(script))), 'original contains assert')
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse((HERE/'independent_checks.py').read_text()))), 'independent contains assert')
    mutation_specs = [
        ('reverse_matrix_product', 'q(F(1)), q(F(2))', 'q(F(2)), q(F(1))', 'quarter-turn product'),
        ('wrong_index_parity', 'sign == (1 if m % 2 else -1)', 'sign == (-1 if m % 2 else 1)', 'negative hyperbolic index alternation'),
        ('drop_cycle_weight', 'sum(d*(-positive.get', 'sum((-positive.get', 'all-iterate formal Lefschetz model'),
        ('finite_period_doubling_cutoff', 'b = {d: 1 for d in range(1, 513)', 'b = {d: 1 for d in range(1, 257)', 'all-iterate formal Lefschetz model'),
        ('reverse_index_gap', '3*k < 4*k-1', '3*k > 4*k-1', 'index-three iterate misses stronger threshold'),
        ('wrong_positive_parabolic_trace', "('positive_parabolic', [[F(1),F(1)],[F(0),F(1)]], 2)", "('positive_parabolic', [[F(1),F(1)],[F(0),F(1)]], 0)", 'positive_parabolic')
    ]
    negative_controls=[]
    for name, before, after, error in mutation_specs:
        require(script.count(before) == 1, 'mutation target must be unique: '+name)
        mutated = script.replace(before, after)
        ast.parse(mutated)
        outcomes=[]
        for label, flags in MODES:
            result=execute(flags,source=mutated)
            require(result.returncode != 0 and ('RuntimeError: '+error) in result.stderr,
                    'negative control was not rejected for the intended reason: '+name+'/'+label)
            require(not result.stdout, 'negative control emitted success output')
            outcomes.append({'mode':label,'exit_code':result.returncode,'rejection':error})
        negative_controls.append({'mutation':name,'mutated_source_sha256':digest(mutated.encode()),'outcomes':outcomes})

    # An independent integrity negative control changes a byte in memory only.
    target=(original/'REPORT.md').read_bytes()
    changed=bytes([target[0]^1])+target[1:]
    require(len(changed)==len(target) and digest(changed)!=digest(target), 'same-size content corruption escaped hash')
    pins_match(original,original_pins['files'])
    pins_match(candidate,corrected_pins['files'])
    return {'status':'pass','frozen_manifest_sha256':FROZEN_SHA256,
            'corrected_manifest_sha256':corrected_pins['corrected_manifest_sha256'],
            'genuine_uid':os.getuid(),'readonly_mechanism':'bubblewrap --ro-bind / /, no writable mounts',
            'network_isolation_claimed':False,
            'mode_results':mode_results,'independent_math_results':json.loads(independent_output),
            'negative_control_mutations':negative_controls,'negative_control_executions':len(negative_controls)*len(MODES),
            'integrity_negative_control':'same-byte-count one-byte REPORT corruption changes SHA-256',
            'inputs_unchanged_after_execution':True,
            'limitations':['Finite tests do not establish universal theorems.','Read-only mounting is verified by EROFS at the actual inputs, not inferred from file permission bits.','No claim of network-namespace isolation is made.']}


if __name__ == '__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
