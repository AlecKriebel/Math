"""Replay reviewed v2 bytes in isolated disposable directories; no mathematical checking."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use -I -S -B')
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import zipfile

PINNED = {
    'LEAF_SPACE_10300026_AUTHOR_V2_SAFE_FREEZE.zip': (19002, '7f36eececb5ddcbdfd17e34a7dd015d081641b2d5aa555f093576ae9713df454'),
    'LEAF_SPACE_10300026_AUTHOR_V2_EXTERNAL_MANIFEST.json': (1232, 'a826f34dcfe07ba474ddb7022907bc090faa120569d49a3b262a575e257fb88c'),
    'LEAF_SPACE_10300026_AUTHOR_V2_BOOTSTRAP.py': (2994, 'a1dfd605ea34bdc4df5e350cbf0704ab2025363f8e3e5fb59790c54ab322770a'),
    'LEAF_SPACE_10300026_AUTHOR_V2_VALIDATION_RECEIPT.json': (4596, '3f11cf550f9eec5089c06c7334b7d17bf8afc3b7ae9ec64020c28b94279c2845'),
}
MEMBERS = {'REPORT.md', 'STATUS.json', 'VERIFICATION_METADATA.json', 'validate.py'}
if len(sys.argv) != 2:
    raise SystemExit('usage: replay_author.py absolute_directory_containing_v2_inputs')
source = Path(sys.argv[1])
if not source.is_absolute() or str(source.resolve()) != str(source):
    raise SystemExit('REJECT: input directory must be canonical and absolute')
blobs = {}
for name, (size, digest) in PINNED.items():
    p = source / name
    if p.is_symlink() or not stat.S_ISREG(p.lstat().st_mode):
        raise SystemExit('REJECT: input is not regular')
    b = p.read_bytes()
    if len(b) != size or hashlib.sha256(b).hexdigest() != digest:
        raise SystemExit('REJECT: v2 external input integrity')
    blobs[name] = b
manifest = json.loads(blobs['LEAF_SPACE_10300026_AUTHOR_V2_EXTERNAL_MANIFEST.json'])
if set(manifest['files']) != MEMBERS or manifest['entrypoint'] != 'validate.py':
    raise SystemExit('REJECT: manifest shape')
with tempfile.TemporaryDirectory(prefix='leafspace_independent_') as tmp:
    base = Path(tmp)
    inputs = base / 'trusted_inputs'
    inputs.mkdir()
    for name, blob in blobs.items():
        (inputs / name).write_bytes(blob)
    archive = inputs / 'LEAF_SPACE_10300026_AUTHOR_V2_SAFE_FREEZE.zip'
    bootstrap = inputs / 'LEAF_SPACE_10300026_AUTHOR_V2_BOOTSTRAP.py'
    mf = inputs / 'LEAF_SPACE_10300026_AUTHOR_V2_EXTERNAL_MANIFEST.json'
    pristine = base / 'pristine'
    pristine.mkdir()
    with zipfile.ZipFile(archive) as z:
        if len(z.infolist()) != len(MEMBERS) or set(z.namelist()) != MEMBERS:
            raise SystemExit('REJECT: zip inventory')
        for name in MEMBERS:
            info = z.getinfo(name)
            kind = stat.S_IFMT(info.external_attr >> 16)
            if info.is_dir() or info.flag_bits & 1 or kind not in (0, stat.S_IFREG):
                raise SystemExit('REJECT: zip entry type')
            b = z.read(name)
            rec = manifest['files'][name]
            if len(b) != rec['bytes'] or hashlib.sha256(b).hexdigest() != rec['sha256']:
                raise SystemExit('REJECT: zip member integrity')
            (pristine / name).write_bytes(b)
    empty = base / 'empty_cwd'
    empty.mkdir()
    hostile = base / 'hostile_cwd'
    hostile.mkdir()
    marker = base / 'SHADOW_EXECUTED'
    poison = "from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('executed')\nraise SystemExit('SHADOW EXECUTED')\n"
    for name in ['json.py', 'pathlib.py', 'hashlib.py', 'zipfile.py', 'sitecustomize.py', 'usercustomize.py']:
        (hostile / name).write_text(poison)
    results = []
    def run(label, expect, root=pristine, arc=archive, man=mf, cwd=empty, flags=None, env=None):
        actual_flags = ['-I', '-S', '-B'] if flags is None else flags
        p = subprocess.run([sys.executable, *actual_flags, str(bootstrap), str(arc), str(root), str(man)], cwd=cwd, env=env, capture_output=True, text=True, timeout=20)
        output = (p.stdout + p.stderr).strip()
        accept = p.returncode == 0 and output == '{"full_solution": false, "mathematical_proof_checked": false, "metadata_validation": "PASS", "problem_id": 10300026}'
        rejection = p.returncode != 0 and output.startswith('REJECT:')
        ok = (accept if expect == 'ACCEPT' else rejection) and not marker.exists()
        results.append({'case': label, 'expected': expect, 'returncode': p.returncode, 'output': output, 'shadow_marker_absent': not marker.exists(), 'pass': ok})
    for opt in [False, True]:
        flags = ['-I', '-S', '-B'] + (['-O'] if opt else [])
        suffix = '_optimized' if opt else '_normal'
        run('clean' + suffix, 'ACCEPT', flags=flags)
        relocated = base / ('relocated space' + suffix)
        shutil.copytree(pristine, relocated)
        run('relocation' + suffix, 'ACCEPT', root=relocated, flags=flags)
        env = os.environ.copy()
        env.update({'PYTHONPATH': str(hostile), 'PYTHONHOME': str(hostile), 'PYTHONSTARTUP': str(hostile / 'sitecustomize.py')})
        run('hostile_cwd_and_environment' + suffix, 'ACCEPT', cwd=hostile, env=env, flags=flags)
        for mutation in ['extra', 'missing', 'entrypoint', 'report', 'status', 'metadata', 'cache', 'shadow', 'member_symlink', 'member_directory', 'root_symlink', 'relative_root', 'wrong_root', 'manifest_entrypoint', 'manifest_extra', 'archive_tamper', 'archive_symlink', 'manifest_symlink']:
            trial = base / (mutation + suffix)
            shutil.copytree(pristine, trial)
            arc, man, root = archive, mf, trial
            if mutation == 'extra': (trial / 'unexpected.txt').write_text('extra')
            elif mutation == 'missing': (trial / 'REPORT.md').unlink()
            elif mutation in ['entrypoint', 'report', 'status', 'metadata']:
                name = {'entrypoint': 'validate.py', 'report': 'REPORT.md', 'status': 'STATUS.json', 'metadata': 'VERIFICATION_METADATA.json'}[mutation]
                (trial / name).write_bytes((trial / name).read_bytes() + b'\n# changed\n')
            elif mutation == 'cache': (trial / '__pycache__').mkdir()
            elif mutation == 'shadow': (trial / 'json.py').write_text(poison)
            elif mutation == 'member_symlink':
                (trial / 'REPORT.md').unlink()
                (trial / 'REPORT.md').symlink_to(pristine / 'REPORT.md')
            elif mutation == 'member_directory':
                (trial / 'validate.py').unlink()
                (trial / 'validate.py').mkdir()
            elif mutation == 'root_symlink':
                root = base / ('linked_root' + suffix)
                root.symlink_to(trial, target_is_directory=True)
            elif mutation == 'relative_root': root = Path('../pristine')
            elif mutation == 'wrong_root': root = inputs
            elif mutation.startswith('manifest_') and mutation != 'manifest_symlink':
                m = json.loads(mf.read_bytes())
                if mutation == 'manifest_entrypoint': m['entrypoint'] = 'REPORT.md'
                else: m['files']['extra.py'] = {'bytes': 0, 'sha256': hashlib.sha256(b'').hexdigest()}
                man = base / (mutation + suffix + '.json')
                man.write_text(json.dumps(m))
            elif mutation == 'archive_tamper':
                arc = base / ('changed' + suffix + '.zip')
                arc.write_bytes(archive.read_bytes() + b'changed')
            elif mutation == 'archive_symlink':
                arc = base / ('linked_archive' + suffix + '.zip')
                arc.symlink_to(archive)
            elif mutation == 'manifest_symlink':
                man = base / ('linked_manifest' + suffix + '.json')
                man.symlink_to(mf)
            run(mutation + suffix, 'REJECT', root=root, arc=arc, man=man, flags=flags)
    run('without_isolation', 'REJECT', flags=['-S', '-B'])
    run('without_no_site', 'REJECT', flags=['-I', '-B'])
    run('without_no_bytecode', 'REJECT', flags=['-I', '-S'])
    result = {'problem_id': 10300026, 'all_tests_pass': all(x['pass'] for x in results), 'test_count': len(results), 'pre_execution_pins_pass': True, 'mathematical_proof_checked_by_program': False, 'tests': results}
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result['all_tests_pass']:
        raise SystemExit(1)
