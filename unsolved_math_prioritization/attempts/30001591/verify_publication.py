#!/usr/bin/env python3
"""Anchored source-free inventory, patch application, and real child-mode replay.

Use a PUBLIC_MANIFEST.json SHA-256 obtained outside this package. An optional
package root permits a trusted verifier to examine relocated or damaged copies.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

AUTHOR = 'ce4ff19beb1fa50a1ba6f504bd1373943b355171e932f39ba1a4770ccbf7ad30'
AUDIT = '22f4ae3c2a188b61782568382a141d4af6402dcf5a36f16bc1dadc31a2681c0a'
PROOF = '30d352188a97a117b29079ff714acdae753ef4f5bbdb5d350d80662f0cb08115'
CORRECTED = 'dd941795fa975569204823d8cb7d8b6d91b4396db191b839c5ab8b36c5a0249a'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root, pin):
    require(not root.is_symlink() and root.is_dir(), 'Nonregular package root')
    manifest = root/'PUBLIC_MANIFEST.json'
    require(not manifest.is_symlink() and manifest.is_file(), 'Nonregular public manifest')
    raw = manifest.read_bytes()
    require(re.fullmatch('[0-9a-f]{64}', pin) is not None, 'Invalid trusted digest')
    require(sha(raw) == pin, 'Public manifest differs from external trust anchor')
    man = json.loads(raw)
    require(man['schema'] == 'borderline-soliton-source-free-publication-v1', 'Wrong schema')
    require(man['problem_id'] == 30001591, 'Wrong problem')
    files = man['files']
    allowed_dirs = set()
    for name, meta in files.items():
        pp = PurePosixPath(name)
        require(not pp.is_absolute() and '..' not in pp.parts and str(pp) == name, 'Unsafe inventory path')
        require(name != 'PUBLIC_MANIFEST.json', 'Self-inventory forbidden')
        allowed_dirs.update(str(p) for p in pp.parents if str(p) != '.')
        f = root/name
        require(not f.is_symlink() and f.is_file(), 'Nonregular or missing payload: '+name)
        data = f.read_bytes()
        require(len(data) == meta['bytes'] and sha(data) == meta['sha256'], 'Payload mismatch: '+name)
    found = set()
    dirs = set()
    for f in root.rglob('*'):
        require(not f.is_symlink(), 'Symlink in package')
        name = f.relative_to(root).as_posix()
        if f.is_dir():
            dirs.add(name)
        else:
            require(f.is_file(), 'Special file in package')
            found.add(name)
    require(found == set(files)|{'PUBLIC_MANIFEST.json'}, 'Exact file inventory mismatch')
    require(dirs == allowed_dirs, 'Exact directory inventory mismatch')
    for name, pin2 in [('release/AUTHOR_MANIFEST.json', AUTHOR), ('release/PARTIAL_RESULTS.md', PROOF),
                       ('audit_release/AUDIT_MANIFEST.json', AUDIT),
                       ('audit_release/PARTIAL_RESULTS.corrected.md', CORRECTED)]:
        require(sha((root/name).read_bytes()) == pin2, 'Frozen anchor mismatch: '+name)
    for directory, manifest_name in [('release', 'AUTHOR_MANIFEST.json'), ('audit_release', 'AUDIT_MANIFEST.json')]:
        inner = json.loads((root/directory/manifest_name).read_bytes())
        require({p.name for p in (root/directory).iterdir()} == set(inner['files'])|{manifest_name}, 'Frozen inventory mismatch')
        for name, meta in inner['files'].items():
            data = (root/directory/name).read_bytes()
            require(len(data) == meta['bytes'] and sha(data) == meta['sha256'], 'Frozen payload mismatch: '+directory+'/'+name)
    return man

def apply_patch(original, patch):
    old = original.decode('utf-8').splitlines(True)
    lines = patch.decode('utf-8').splitlines(True)
    require(lines[:2] == ['--- a/PARTIAL_RESULTS.md\n', '+++ b/PARTIAL_RESULTS.md\n'], 'Patch file headers changed')
    out = []
    cursor = 0
    i = 2
    hunks = 0
    while i < len(lines):
        match = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@\n', lines[i])
        require(match is not None, 'Invalid hunk header')
        a, an, b, bn = [int(x) if x is not None else 1 for x in match.groups()]
        start = a-1
        require(start >= cursor and start <= len(old), 'Overlapping or out-of-range hunk')
        out.extend(old[cursor:start]); cursor = start
        require(len(out) == b-1, 'New hunk coordinate mismatch')
        i += 1; removed = added = 0
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]; op = line[:1]; body = line[1:]
            require(op in (' ', '+', '-'), 'Invalid patch operation')
            if op in (' ', '-'):
                require(cursor < len(old) and old[cursor] == body, 'Patch source/context mismatch')
                cursor += 1; removed += 1
            if op in (' ', '+'):
                out.append(body); added += 1
            i += 1
        require((removed, added) == (an, bn), 'Hunk length mismatch')
        hunks += 1
    out.extend(old[cursor:])
    require(hunks > 0, 'Empty correction')
    return ''.join(out).encode('utf-8'), hunks

def child(script, mode, args=()):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    probe = 'import sys,runpy; print("CHILD_OPTIMIZE="+str(sys.flags.optimize),file=sys.stderr);sys.argv=sys.argv[1:];runpy.run_path(sys.argv[0],run_name="__main__")'
    command = [sys.executable, '-B'] + ([] if mode == 0 else ['-O' if mode == 1 else '-OO'])
    command += ['-c', probe, str(script), *map(str, args)]
    run = subprocess.run(command, cwd=script.parent, env=env, capture_output=True, timeout=180)
    require(run.returncode == 0, 'Child failed: '+str(script.name)+' '+run.stderr.decode())
    require(run.stderr == ('CHILD_OPTIMIZE='+str(mode)+'\n').encode(), 'Child mode probe mismatch')
    return run.stdout

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trusted_manifest_sha256')
    parser.add_argument('package_root', nargs='?', default=str(Path(__file__).resolve().parent))
    parser.add_argument('--inventory-only', action='store_true')
    args = parser.parse_args()
    root = Path(args.package_root).absolute()
    man = inventory(root, args.trusted_manifest_sha256)
    corrected, hunks = apply_patch((root/'release/PARTIAL_RESULTS.md').read_bytes(),
                                    (root/'audit_release/CORRECTION.patch').read_bytes())
    require(corrected == (root/'audit_release/PARTIAL_RESULTS.corrected.md').read_bytes(), 'Actual patch application differs')
    accept = json.loads((root/'audit_release/ACCEPTANCE.json').read_bytes())
    require(accept['disposition'] == 'unsolved' and accept['turns_completed'] == 5, 'Acceptance scope mismatch')
    runs = []
    if not args.inventory_only:
        for mode in (0, 1, 2):
            for directory, script, result in [('release','check_algebra.py','CHECK_RESULTS.json'),
                                               ('audit_release','independent_controls.py','INDEPENDENT_RESULTS.json')]:
                output = child(root/directory/script, mode)
                require(output == (root/directory/result).read_bytes(), 'Direct replay result differs')
                runs.append({'script':directory+'/'+script, 'actual_child_optimization':mode,
                             'stdout_sha256':sha(output)})
            author = json.loads(child(root/'release/verify_packet.py', mode))
            audit = json.loads(child(root/'audit_release/verify_audit.py', mode, [root/'release', AUDIT]))
            require(author['status'] == audit['status'] == 'PASS', 'Frozen verifier rejected')
            require(author['exact_algebra_checks'] == 43 and author['mathematical_mutations_rejected'] == 3, 'Author counts changed')
            require(audit['audit_digest_authenticated'] is True and audit['corrected_proof_sha256'] == CORRECTED, 'Audit anchor not authenticated')
            runs.extend([{'script':'release/verify_packet.py','actual_child_optimization':mode},
                         {'script':'audit_release/verify_audit.py','actual_child_optimization':mode}])
    print(json.dumps({'status':'PASS','problem_id':30001591,'disposition':'unsolved','turns':'5/5',
                      'public_manifest_sha256':args.trusted_manifest_sha256,
                      'payload_files':len(man['files']),'patch_hunks_applied':hunks,
                      'inventory_only':args.inventory_only,'replays':runs,
                      'scope':'Authenticated package consistency and finite algebra replay; no proof of critical PDE equality.'},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
