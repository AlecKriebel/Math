#!/usr/bin/env python3
"""Non-mutating runtime audit of a separately frozen KP-1.30 packet.

Usage: python audit_runtime.py ORIGINAL_DIRECTORY AUDIT_WORK_DIRECTORY
The original directory must contain public/ and the candidate zip.  Only a
fresh work directory is written.  Actual UID 1000 and failed write probes
are required; no root-only simulation of a read-only working directory.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import zipfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(directory):
    return {str(p.relative_to(directory)): {'bytes': p.stat().st_size,
             'sha256': digest(p.read_bytes())}
            for p in sorted(directory.rglob('*')) if p.is_file()}


def main():
    original, work = [Path(x).resolve() for x in sys.argv[1:3]]
    require(os.getuid() == os.geteuid() == 1000, 'Audit must actually run as UID 1000')
    before = snapshot(original/'public')
    receipt = json.loads((original/'FROZEN_RECEIPT.json').read_text())
    manifest = json.loads((original/'public/MANIFEST.json').read_text())
    for f in manifest['files']:
        require(before[f['file']] == {'bytes': f['bytes'], 'sha256': f['sha256']},
                'Frozen manifest mismatch: '+f['file'])
    require(before['MANIFEST.json']['sha256'] == receipt['manifest_sha256'], 'Manifest anchor mismatch')
    require(before['REPORT.md']['sha256'] == receipt['report_sha256'], 'Report anchor mismatch')
    zip_path = original/receipt['archive']
    zip_before = digest(zip_path.read_bytes())
    require(zip_before == receipt['archive_sha256'], 'Archive anchor mismatch')
    require(zip_path.stat().st_size == receipt['archive_bytes'], 'Archive size mismatch')
    with zipfile.ZipFile(zip_path) as archive:
        require(sorted(archive.namelist()) == sorted(before), 'Unexpected archive members')
        require(archive.testzip() is None, 'Archive CRC check failed')
        for name in archive.namelist():
            require(archive.read(name) == (original/'public'/name).read_bytes(), 'Archive file mismatch')
    work.mkdir(parents=True, exist_ok=True)
    readonly = work/'readonly'
    require(not readonly.exists(), 'Use a fresh work directory')
    shutil.copytree(original/'public', readonly)
    for file in readonly.iterdir():
        file.chmod(0o444)
    readonly.chmod(0o555)
    probe = '''import json, os
out={"uid":os.getuid(),"euid":os.geteuid(),"gid":os.getgid()}
for key,path,mode in [("create_denied","write_probe","x"),("truncate_denied","REPORT.md","w")]:
    try:
        with open(path,mode): pass
    except PermissionError:
        out[key]=True
    else:
        raise RuntimeError(key+" did not fail")
print(json.dumps(out,sort_keys=True))
'''
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    probe_run = subprocess.run([sys.executable, '-c', probe], cwd=readonly, env=env,
                               capture_output=True, text=True)
    require(probe_run.returncode == 0, 'Read-only probes failed')
    expected = (readonly/'EXACT_CHECKS.json').read_bytes()
    runs = []
    for flags in ([], ['-O'], ['-OO']):
        run = subprocess.run([sys.executable, *flags, 'verify_exact.py'], cwd=readonly,
                             env=env, capture_output=True)
        require(run.returncode == 0 and run.stdout == expected, 'Candidate result mismatch')
        runs.append({'flags': flags, 'exit_code': run.returncode,
                     'output_bytes': len(run.stdout), 'output_sha256': digest(run.stdout),
                     'stderr_bytes': len(run.stderr), 'matches_frozen_output': True})
    require(snapshot(readonly) == before, 'Read-only copy changed')

    source = (original/'public/verify_exact.py').read_text()
    mutations = [
        ('trefoil_rank', '(3, (4, 6, 3, 3))', '(3, (4, 5, 3, 3))', 'main'),
        ('cube_sign', 'sign = (-1) ** sum(s[:k])', 'sign = 1', 'main'),
        ('comultiplication', '[(0, 1), (1, 0)]', '[(0, 1)]', 'main'),
        ('bockstein_parity', 'int(e == 1)', 'int(e == 2)', 'algebra_checks'),
        ('odd_cycle_smith', '[2 if n % 2 else 0]', '[0 if n % 2 else 2]', 'algebra_checks'),
        ('module_composition', 'sp.Matrix([[0], [1], [0]])', 'sp.Matrix([[0], [0], [0]])', 'algebra_checks'),
        ('turner_zigzag', 'sp.eye(2)', 'sp.zeros(2)', 'algebra_checks'),
        ('tensor_connecting_rank', 'require(delta_sum.rank() == 4)', 'require(delta_sum.rank() == 3)', 'algebra_checks'),
    ]
    controls = []
    for name, old, new, entry in mutations:
        require(source.count(old) == 1, 'Mutation is not unique: '+name)
        mutated = source.replace(old, new)
        # Compile the isolated authored mutation directly; do not create a second
        # candidate file or modify any frozen bytes.
        program = "ns={'__name__':'audit_mutant'}\nexec(compile("+repr(mutated)+",'<audit-mutant>','exec'),ns)\nns["+repr(entry)+"]()\n"
        for flags in ([], ['-O'], ['-OO']):
            run = subprocess.run([sys.executable, *flags, '-c', program], cwd=readonly,
                                 env=env, capture_output=True)
            require(run.returncode != 0, 'Surviving semantic mutation: '+name)
            require(b'RuntimeError: Exact verification condition failed' in run.stderr,
                    'Mutation failed for an unrelated reason: '+name)
            controls.append({'mutation': name, 'flags': flags, 'exit_code': run.returncode,
                             'reason': 'Explicit verification RuntimeError',
                             'candidate_sha256': digest(mutated.encode()),
                             'stdout_bytes': len(run.stdout),
                             'stderr_sha256': digest(run.stderr)})
    require(snapshot(original/'public') == before, 'Original packet was altered')
    require(digest(zip_path.read_bytes()) == zip_before, 'Original archive was altered')
    require(snapshot(readonly) == before, 'Read-only copy changed during mutation checks')
    result = {
        'status': 'PASS',
        'frozen_manifest_sha256': receipt['manifest_sha256'],
        'frozen_report_sha256': receipt['report_sha256'],
        'frozen_archive_sha256': zip_before,
        'frozen_archive_bytes': zip_path.stat().st_size,
        'archive_members': sorted(before),
        'manifest_file_records_verified': len(manifest['files']),
        'original_packet_unchanged': True, 'readonly_copy_unchanged': True,
        'uid_and_readonly_probes': json.loads(probe_run.stdout),
        'readonly_directory_mode': oct(stat.S_IMODE(readonly.stat().st_mode)),
        'readonly_file_modes': sorted({oct(stat.S_IMODE(p.stat().st_mode)) for p in readonly.iterdir()}),
        'python_version': sys.version.split()[0],
        'assert_statements_in_candidate': sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(source))),
        'normal_and_optimized_runs': runs,
        'semantic_mutation_count': len(mutations),
        'failed_mutation_runs': controls,
        'mutation_scope': '8 semantic mutations, each required to fail through an explicit check in normal, -O, and -OO modes',
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
