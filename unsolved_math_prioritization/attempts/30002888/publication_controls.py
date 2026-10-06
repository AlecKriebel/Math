"""Independent publication-boundary tests; first authenticate the package."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise SystemExit('Python -I -S -B required')
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

def need(ok, message):
    if not ok: raise ValueError(message)

def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    need(len(sys.argv) == 3, 'root and external manifest hash required')
    original = Path(sys.argv[1]).absolute()
    manifest_pin = sys.argv[2]
    wrapper = original / 'publication_bootstrap.py'
    wrapper_bytes = wrapper.read_bytes()
    records = []
    with tempfile.TemporaryDirectory(prefix='mixed-perverse-boundary-') as td:
        work = Path(td)
        sentinel = work / 'POISON_EXECUTED'
        poison = ('open(' + repr(str(sentinel)) + ', "w").write("bad")\n').encode()
        hostile = work / 'hostile working root'; hostile.mkdir()
        for mod in ('json', 'hashlib', 'pathlib', 'subprocess', 'stat', 'zipfile', 'sitecustomize', 'usercustomize'):
            (hostile / (mod + '.py')).write_bytes(poison)
            (hostile / (mod + '.pyc')).write_bytes(poison)
        env = dict(os.environ, PYTHONPATH=str(hostile), PYTHONPYCACHEPREFIX=str(hostile / 'cache'))

        def run(label, root, pin, accept=False, entry=None, flags=None):
            target = Path(entry) if entry else root / 'publication_bootstrap.py'
            # Test copies of the trusted wrapper only, including the intentional symlink case.
            need(target.read_bytes() == wrapper_bytes, 'wrapper unexpectedly changed')
            command = [sys.executable] + (['-I', '-S', '-B'] if flags is None else flags)
            if sys.flags.optimize: command.append('-O')
            proc = subprocess.run(command + [str(target), str(root), pin], cwd=hostile, env=env, capture_output=True, text=True, timeout=40)
            need(not sentinel.exists(), 'poison executed')
            need((proc.returncode == 0) == accept, 'unexpected outcome: ' + label + ': ' + proc.stderr)
            if accept: need(json.loads(proc.stdout)['verified'] is True, 'positive result')
            records.append({'case': label, 'outcome': 'accepted' if accept else 'rejected', 'poison_sentinel_absent': True})

        run('original hostile CWD and PYTHONPATH', original, manifest_pin, True)
        relocated = work / 'relocated complete package with spaces'; shutil.copytree(original, relocated)
        run('relocated full package', relocated, manifest_pin, True)
        run('incorrect external pin', original, '0' * 64)
        for label, flags in [('missing isolation', ['-S', '-B']), ('missing no-site', ['-I', '-B']), ('missing no-bytecode', ['-I', '-S'])]:
            run(label, original, manifest_pin, flags=flags)
        link = work / 'root link'; link.symlink_to(original, target_is_directory=True)
        run('root symlink', link, manifest_pin)
        parent = work / 'parent'; parent.mkdir()
        child = parent / 'packet'; shutil.copytree(original, child)
        plink = work / 'parent link'; plink.symlink_to(parent, target_is_directory=True)
        run('ancestor symlink', plink / 'packet', manifest_pin)
        entry = work / 'entry link.py'; entry.symlink_to(wrapper)
        run('operative entrypoint symlink', original, manifest_pin, entry=entry)
        wrong = work / 'wrong_entry.py'; wrong.write_bytes(wrapper_bytes)
        run('wrong operative entrypoint', original, manifest_pin, entry=wrong)

        def fixture(name):
            root = work / name; shutil.copytree(original, root); return root
        for name in ['__main__.py', 'json.py', '__pycache__/checks.pyc', 'empty_directory/']:
            root = fixture('extra-' + str(len(records)))
            p = root / name
            if name.endswith('/'): p.mkdir()
            else: p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(poison)
            run('unexpected ' + name, root, manifest_pin)
        for name in ['MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_BOOTSTRAP.py', 'audit/verify_author_freeze.py', 'author/proof.md', 'audit/acceptance.json', 'PUBLICATION_MANIFEST.json']:
            root = fixture('symlink-' + str(len(records)))
            p = root / name; p.unlink(); p.symlink_to(original / name)
            run('symlink member ' + name, root, manifest_pin)
        for name in ['MIXED_PERVERSE_30002888_AUTHOR_SAFE_FREEZE.zip', 'MIXED_PERVERSE_30002888_INDEPENDENT_AUDIT_SAFE.zip', 'author/proof.md', 'audit/audit.md']:
            root = fixture('change-' + str(len(records)))
            with (root / name).open('ab') as f: f.write(b'changed')
            run('changed ' + name, root, manifest_pin)
        root = fixture('missing-member'); (root / 'author/status.md').unlink()
        run('missing member', root, manifest_pin)
        for label, mutate in [
            ('duplicate JSON key', lambda b: b'{"schema":1,"schema":1}'),
            ('wrong schema', lambda b: json.dumps(dict(json.loads(b), schema=True)).encode()),
            ('wrong manifest inventory', lambda b: json.dumps(dict(json.loads(b), files={})).encode()),
            ('unsafe manifest path', lambda b: b.replace(b'"author/status.md"', b'"../README.md"')),
            ('boolean byte count', lambda b: json.dumps(dict(json.loads(b), files={k:dict(v,bytes=True) for k,v in json.loads(b)['files'].items()})).encode()),
        ]:
            root = fixture('malformed-' + str(len(records)))
            mp = root / 'PUBLICATION_MANIFEST.json'; before = mp.read_bytes(); after = mutate(before)
            need(after != before, 'mutation ineffective')
            mp.write_bytes(after)
            run(label + ' with test-only replacement external pin', root, sha(after))
        root = fixture('source-rehashed')
        p = root / 'author/source_metadata.json'; s = json.loads(p.read_bytes()); s['sources'][0]['pdf_sha256'] = '0' * 64
        p.write_text(json.dumps(s, sort_keys=True, indent=2) + '\n')
        mpath = root / 'PUBLICATION_MANIFEST.json'; m = json.loads(mpath.read_bytes()); b = p.read_bytes()
        m['files']['author/source_metadata.json'] = {'bytes': len(b), 'sha256': sha(b)}
        mb = (json.dumps(m, sort_keys=True, indent=2) + '\n').encode(); mpath.write_bytes(mb)
        run('rehashed source metadata retains immutable archive pin', root, sha(mb))
    need(wrapper.read_bytes() == wrapper_bytes, 'original wrapper changed')
    return {'problem_id': 30002888, 'reviewer_optimized': bool(sys.flags.optimize), 'positive_runs': sum(r['outcome'] == 'accepted' for r in records), 'negative_runs': sum(r['outcome'] == 'rejected' for r in records), 'records': records, 'scope': 'Publication integrity tests only. Replacement manifest anchors are test-local and never deployment anchors.'}

if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
