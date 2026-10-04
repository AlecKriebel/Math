#!/usr/bin/env python3
"""Portable, fail-closed integrity and exact-control replay (standard library)."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, subprocess, sys, tempfile, zipfile
ROOT = Path(__file__).resolve().parent
ARCHIVES = {
    'author-packet.zip': (15098, '5caa2ded8af38610317260f2f002b0a3bb813b06c58962e628462394f7f2e512', 'safe'),
    'audit-packet.zip': (12772, 'a5e48996c5cebadbf650a7a37e5449c3eb8b858fc87174892006fdf879bf49dc', 'audit'),
}
def require(condition, message):
    if not condition:
        raise ValueError(message)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def inventory(root):
    result = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink: ' + str(p))
        require(p.is_file() or p.is_dir(), 'special file: ' + str(p))
        if p.is_file():
            result.add(p.relative_to(root).as_posix())
    return result
def run(script, *args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    result = subprocess.run([sys.executable, '-B', str(script), *map(str, args)], cwd=script.parent, env=env, capture_output=True, check=True)
    return result.stdout

def main():
    require(sys.flags.optimize == 0, 'Optimized Python disables frozen assertions; run without -O/-OO/PYTHONOPTIMIZE.')
    manifest = json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
    rows = manifest['files']
    paths = [e['path'] for e in rows]
    require(len(paths) == len(set(paths)), 'duplicate manifest paths')
    for path in paths:
        pp = PurePosixPath(path)
        require(not pp.is_absolute() and '..' not in pp.parts and str(pp) == path, 'unsafe path')
    require(inventory(ROOT) == set(paths) | {'RELEASE_MANIFEST.json'}, 'release file set differs')
    for e in rows:
        data = (ROOT/e['path']).read_bytes()
        require(len(data) == e['bytes'] and digest(data) == e['sha256'], 'release hash/size: ' + e['path'])
    archive_counts = {}
    for name, (size, expected, prefix) in ARCHIVES.items():
        data = (ROOT/name).read_bytes()
        require(len(data) == size and digest(data) == expected, 'frozen archive changed: ' + name)
        with zipfile.ZipFile(ROOT/name) as archive:
            names = archive.namelist()
            require(len(names) == len(set(names)), 'duplicate ZIP members')
            require(set(names) == {p for p in paths if p.startswith(prefix + '/')}, 'ZIP/extracted file set differs')
            for info in archive.infolist():
                pp = PurePosixPath(info.filename)
                require(not pp.is_absolute() and '..' not in pp.parts and str(pp) == info.filename, 'unsafe ZIP member')
                require((info.external_attr >> 16) & 0o170000 != 0o120000, 'ZIP symlink')
                require(archive.read(info) == (ROOT/info.filename).read_bytes(), 'ZIP/extracted bytes differ: ' + info.filename)
            archive_counts[name] = len(names)
    require(json.loads((ROOT/'safe/STATUS.json').read_text())['substantive_attempt_responses'] == 1, 'wrong author approach count')
    require(len((ROOT/'safe/turns.jsonl').read_text().splitlines()) == 1, 'wrong turn count')
    require(json.loads((ROOT/'audit/CORRECTIONS.json').read_text())['required_mathematical_corrections'] == [], 'unexpected required correction')
    author_manifest = json.loads(run(ROOT/'safe/verify_manifest.py'))
    audit_manifest = json.loads(run(ROOT/'audit/verify_audit.py', '--author-packet', ROOT/'author-packet.zip'))
    author = run(ROOT/'safe/verify.py')
    require(author == (ROOT/'safe/CONTROL_RESULTS.json').read_bytes(), 'author control output differs')
    require(author == (ROOT/'audit/AUTHOR_CONTROL_RERUN.json').read_bytes(), 'audit author rerun differs')
    independent = run(ROOT/'audit/independent_verify.py')
    require(independent == (ROOT/'audit/INDEPENDENT_CONTROLS.json').read_bytes(), 'independent control output differs')
    # Also replay from fresh archive-only extraction, without referring to extracted payloads.
    with tempfile.TemporaryDirectory(prefix='im-sharing-replay-') as tmp:
        out = Path(tmp)
        for name in ARCHIVES:
            with zipfile.ZipFile(ROOT/name) as archive:
                archive.extractall(out)
        require(run(out/'safe/verify.py') == author, 'fresh ZIP author replay differs')
        require(run(out/'audit/independent_verify.py') == independent, 'fresh ZIP audit replay differs')
        run(out/'safe/verify_manifest.py')
        run(out/'audit/verify_audit.py', '--author-packet', ROOT/'author-packet.zip')
    print(json.dumps({'status':'PASS', 'problem_id':30000700, 'queue_status':'claimed_solved', 'turns':'1/5', 'scope':'negative answer to the literal printed universal IM statement through its permitted zero-value case', 'files_verified':len(rows), 'archive_members':archive_counts, 'author_manifest':author_manifest, 'audit_manifest':audit_manifest, 'author_controls':'byte-identical', 'independent_controls':'byte-identical', 'clean_archive_replay':'PASS', 'assertions_enabled':True}, sort_keys=True, indent=2))
if __name__ == '__main__':
    main()
