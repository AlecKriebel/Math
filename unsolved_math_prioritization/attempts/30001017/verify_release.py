#!/usr/bin/env python3
"""Offline, strict release integrity and exact-arithmetic replay; standard library only."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, stat, subprocess, sys, zipfile
ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def measure(data):
    return {'bytes': len(data), 'sha256': digest(data)}

def safe_path(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and not p.is_absolute() and '..' not in p.parts
            and str(p) == name and name not in ('', '.'), 'Unsafe path')

def replay(relative, *args):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run([sys.executable, '-B', str(ROOT / relative), *map(str, args)],
                            cwd=ROOT, env=env, capture_output=True)
    require(result.returncode == 0, 'Replay failed: ' + relative + '\n' + result.stderr.decode())
    return result.stdout

def main():
    manifest_path = ROOT / 'RELEASE_MANIFEST.json'
    require(manifest_path.is_file() and not manifest_path.is_symlink(), 'Invalid manifest')
    manifest = json.loads(manifest_path.read_bytes())
    require(manifest['format'] == 'voronoi-release-sha256-v1', 'Manifest format')
    expected = manifest['files']
    require(isinstance(expected, dict) and 'RELEASE_MANIFEST.json' not in expected, 'Manifest shape')
    actual = set()
    directories = set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink forbidden')
        name = p.relative_to(ROOT).as_posix()
        if p.is_dir():
            directories.add(name)
        else:
            require(stat.S_ISREG(p.stat().st_mode), 'Non-regular file')
            actual.add(name)
    require(directories == {'author', 'audit'}, 'Unexpected or missing directories')
    require(actual == set(expected) | {'RELEASE_MANIFEST.json'}, 'Release allowlist mismatch')
    for name, record in expected.items():
        safe_path(name)
        require(measure((ROOT / name).read_bytes()) == record, 'Hash/size mismatch: ' + name)
    binding = json.loads((ROOT / 'RELEASE_BINDING.json').read_bytes())
    require(binding['problem_id'] == 30001017 and binding['rank'] == 662, 'Wrong target')
    require(binding['status'] == 'unsolved' and binding['turns'] == '5/5', 'Wrong disposition')
    for flag in ['all_genus_target_resolved', 'genus5_L2_D13_evaluated', 'novelty_claim', 'journal_text_inspected']:
        require(binding[flag] is False, 'Unsupported claim: ' + flag)
    archive_records = {
        'author-packet.zip': {'bytes': 25801, 'sha256': 'b4843f6a1906674e6a0ad15e5f05e4b23e08692f039cd6847780559663e07797'},
        'audit-packet.zip': {'bytes': 15244, 'sha256': 'cc8696d6d8de5deab5565c51013adfc86693efa60a7c23212937d8fd3e299036'},
    }
    member_counts = {}
    for name, record in archive_records.items():
        require(measure((ROOT / name).read_bytes()) == record, 'Frozen archive changed')
        key = 'author_archive' if name.startswith('author') else 'audit_archive'
        require(binding[key] == record, 'Archive binding mismatch')
        layout = binding['archive_layout'][name]
        folder = 'author' if name.startswith('author') else 'audit'
        prefix = 'safe/' if folder == 'author' else 'audit-safe/'
        require(layout == {'directory': folder, 'prefix': prefix}, 'Archive layout mismatch')
        with zipfile.ZipFile(ROOT / name) as archive:
            members = archive.infolist()
            names = [m.filename for m in members]
            require(len(names) == len(set(names)), 'Duplicate archive members')
            local = {p.name for p in (ROOT / folder).iterdir()}
            require(set(names) == {prefix + n for n in local}, 'Archive member allowlist mismatch')
            for member in members:
                safe_path(member.filename)
                require(not member.is_dir() and not stat.S_ISLNK(member.external_attr >> 16), 'Invalid archive member')
                require(archive.read(member) == (ROOT / folder / member.filename[len(prefix):]).read_bytes(), 'Archive member bytes differ')
        member_counts[folder] = len(names)
    require(member_counts == {'author': 14, 'audit': 8}, 'Frozen file count mismatch')
    correction = (ROOT / 'audit/CORRECTIONS.md').read_bytes()
    require(binding['corrections']['path'] == 'audit/CORRECTIONS.md', 'Correction path')
    require(binding['corrections']['sha256'] == digest(correction)
            and binding['corrections']['bytes'] == len(correction)
            and binding['corrections']['controls_frozen_author_text'] is True, 'Correction binding')
    require(binding['corrections']['applies_to'] == ['author/PROOF.md: Lemma 6.1 proof', 'author/SOURCE_ISSUES.md: OWR rank-one normalization'], 'Correction scope')
    guide = (ROOT / 'README.md').read_bytes()
    require(binding['corrections']['reproduced_verbatim_in'] == 'README.md'
            and guide.endswith(correction) and guide.count(correction) == 1, 'Correction guide reproduction')
    author = replay('author/verify.py')
    require(author == (ROOT / 'author/CONTROL_RESULTS.json').read_bytes(), 'Author arithmetic bytes differ')
    independent = replay('audit/independent_verify.py')
    require(independent == (ROOT / 'audit/INDEPENDENT_RESULTS.json').read_bytes(), 'Independent arithmetic bytes differ')
    require(json.loads(replay('author/verify_manifest.py'))['status'] == 'PASS', 'Author manifest failed')
    audit = json.loads(replay('audit/verify_audit.py', ROOT / 'author-packet.zip'))
    require(audit['status'] == 'PASS' and audit['author_archive_checked'] is True, 'Audit binding/replay failed')
    print(json.dumps({'status': 'PASS', 'problem_id': 30001017, 'disposition': 'unsolved',
                      'turns': '5/5', 'release_files': len(actual), 'frozen_members': member_counts,
                      'author_arithmetic_byte_match': True, 'independent_arithmetic_byte_match': True,
                      'archives_exact': True, 'corrections_bound_and_reproduced': True}, sort_keys=True))

if __name__ == '__main__':
    main()
