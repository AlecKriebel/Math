"""Independent execution-boundary controls for the pinned author packet.

Run with python -I -S -B [ -O ] replay_controls.py BOOTSTRAP ZIP MANIFEST.
This verifies infrastructure, not a mathematical proof. No network access.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    raise SystemExit('Run this reviewer under -I -S')
import copy
import hashlib
import io
import json
import marshal
import os
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import tempfile
import warnings
import zipfile
import importlib.util

PINS = {
    'bootstrap': '303c8a3f91db4cafd7a73504357ac1c90170bdee17635f8222498462fb3f2d7c',
    'zip': '3e77fa2a11514444ea34bbee9ebd9096cbf313749d22dd4c7afc21060ef4218b',
    'manifest': '7ed84eb3615eba0c2a413e3a7653e7a826312171aff1f61666c67d614b06503f',
}
NAMES = {'README.md', 'RESULT.md', 'APPROACHES.md', 'STATUS.json',
         'INPUT_BINDING.json', 'SOURCES.json', 'checks.py', 'EXPECTED.json'}

def need(ok, label):
    if not ok:
        raise RuntimeError(label)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    need(len(sys.argv) == 4, 'expected bootstrap, ZIP, manifest paths')
    bp, zp, mp = [Path(x).resolve() for x in sys.argv[1:]]
    bb, zb, mb = [p.read_bytes() for p in (bp, zp, mp)]
    for key, b in zip(('bootstrap', 'zip', 'manifest'), (bb, zb, mb)):
        need(sha(b) == PINS[key], key + ' external anchor mismatch')
    manifest = json.loads(mb)
    with zipfile.ZipFile(io.BytesIO(zb)) as z:
        infos = z.infolist()
        need(len(infos) == len(NAMES), 'independent inventory count')
        need({i.filename for i in infos} == NAMES, 'independent inventory names')
        members = [(copy.copy(i), z.read(i)) for i in infos]
    for i, b in members:
        need(stat.S_ISREG(i.external_attr >> 16), 'independent member regularity')
        need(manifest['files'][i.filename] == {'bytes': len(b), 'sha256': sha(b)},
             'independent exact member binding')
    records = []
    with tempfile.TemporaryDirectory(prefix='stringy-independent-') as td:
        root = Path(td)
        sentinel = root / 'UNTRUSTED_CODE_EXECUTED'
        poison = 'open(' + repr(str(sentinel)) + ', "w").write("executed")\nraise RuntimeError("poison")\n'
        env = dict(os.environ)
        hostile = root / 'hostile external root'; hostile.mkdir()
        for name in ('json', 'hashlib', 'pathlib', 'zipfile', 'subprocess', 'tempfile',
                     'stat', 're', 'io', 'sitecustomize', 'usercustomize', 'checks'):
            (hostile / (name + '.py')).write_text(poison)
            code = compile(poison, name + '.py', 'exec')
            pyc = importlib.util.MAGIC_NUMBER + struct.pack('<III', 0, 0, 0) + marshal.dumps(code)
            (hostile / (name + '.pyc')).write_bytes(pyc)
            cache = hostile / '__pycache__'; cache.mkdir(exist_ok=True)
            for suffix in ('', '.opt-1'):
                (cache / (name + '.' + sys.implementation.cache_tag + suffix + '.pyc')).write_bytes(pyc)
        env['PYTHONPATH'] = str(hostile)
        env['PYTHONPYCACHEPREFIX'] = str(hostile / '__pycache__')

        def run(label, bootstrap, archive, metadata, cwd, opt, accept, flags=None):
            need(sha(bootstrap.read_bytes()) == PINS['bootstrap'], 'bootstrap changed before execution')
            cmd = [sys.executable] + (['-I', '-S', '-B'] if flags is None else flags)
            if opt: cmd.append('-O')
            cmd += [str(bootstrap), str(archive), str(metadata)]
            p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=45)
            need(not sentinel.exists(), 'untrusted import/cache/source executed: ' + label)
            if accept:
                need(p.returncode == 0 and p.stderr == '', 'positive failed: ' + label + ': ' + p.stderr)
                got = json.loads(p.stdout)
                need(got['verified'] is True and got['checks_passed'] == 230, 'positive result wrong')
                need(got['optimized'] is opt, 'optimization propagation')
            else:
                need(p.returncode != 0, 'negative accepted: ' + label)
            records.append({'case': label, 'optimized': opt,
                            'outcome': 'accepted' if accept else 'rejected',
                            'sentinel_absent': True,
                            'reason': p.stderr.strip() if not accept else '230 exact author checks'})

        relocated = root / 'relocated packet with spaces'; relocated.mkdir()
        rb, rz, rm = [relocated / x for x in ('BOOTSTRAP.py', 'packet.zip', 'manifest.json')]
        for p, b in ((rb, bb), (rz, zb), (rm, mb)): p.write_bytes(b)
        # A stale extracted source and a malicious sibling entrypoint must be irrelevant:
        # the bootstrap executes only the checks.py bytes authenticated inside the ZIP.
        (relocated / 'checks.py').write_text(poison)
        (relocated / '__main__.py').write_text(poison)
        for opt in (False, True):
            run('original from unrelated root', bp, zp, mp, root, opt, True)
            run('relocation plus hostile sibling source/entrypoint', rb, rz, rm, relocated, opt, True)
            run('hostile CWD, PYTHONPATH, source and bytecode cache', rb, rz, rm, hostile, opt, True)
            # -I blocks startup poison; without -S the bootstrap must refuse before imports.
            run('missing no-site flag', rb, rz, rm, root, opt, False, ['-I', '-B'])
            # -S prevents startup hooks. Put the bootstrap in a clean script directory.
            clean = root / 'clean bootstrap'; clean.mkdir(exist_ok=True)
            cb = clean / 'BOOTSTRAP.py'; cb.write_bytes(bb)
            run('missing isolation flag', cb, rz, rm, root, opt, False, ['-S', '-B'])

        variants = {}
        def archive(name, mutate, metadata=None):
            items = mutate([(copy.copy(i), b) for i, b in members])
            dest = root / name; dest.mkdir()
            zpath, mpath = dest / 'packet.zip', dest / 'manifest.json'
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                with zipfile.ZipFile(zpath, 'w') as z:
                    for i, b in items: z.writestr(i, b)
            mpath.write_bytes(mb if metadata is None else metadata)
            variants[name] = (zpath, mpath)
        def extra(name, mode=stat.S_IFREG | 0o444):
            i = zipfile.ZipInfo(name); i.create_system = 3; i.external_attr = mode << 16
            return (i, poison.encode())
        archive('changed_prose', lambda xs: [(i, b + b'\nchanged') if i.filename == 'RESULT.md' else (i, b) for i,b in xs])
        archive('changed_checked_source', lambda xs: [(i, poison.encode()) if i.filename == 'checks.py' else (i, b) for i,b in xs])
        archive('extra_root_module', lambda xs: xs + [extra('json.py')])
        archive('extra_entrypoint', lambda xs: xs + [extra('__main__.py')])
        archive('extra_cache_member', lambda xs: xs + [extra('__pycache__/checks.pyc')])
        archive('missing_member', lambda xs: [(i,b) for i,b in xs if i.filename != 'README.md'])
        archive('duplicate_member', lambda xs: xs + [xs[0]])
        archive('traversal_member', lambda xs: xs + [extra('../outside.py')])
        archive('absolute_member', lambda xs: xs + [extra('/outside.py')])
        archive('directory_member', lambda xs: xs + [extra('extra/', stat.S_IFDIR | 0o755)])
        def symlink(xs):
            for i,b in xs:
                if i.filename == 'README.md': i.external_attr = (stat.S_IFLNK | 0o777) << 16
            return xs
        archive('symlink_member', symlink)
        archive('manifest_duplicate_key', lambda xs: xs, b'{"schema":1,"schema":1}')
        wrong = copy.deepcopy(manifest); wrong['files']['README.md']['bytes'] = True
        archive('manifest_boolean_size', lambda xs: xs, json.dumps(wrong).encode())
        wrong = copy.deepcopy(manifest); wrong['files']['RESULT.md']['sha256'] = '0' * 64
        archive('manifest_changed_hash', lambda xs: xs, json.dumps(wrong).encode())
        for name, (zpath, mpath) in variants.items():
            for opt in (False, True): run(name, rb, zpath, mpath, root, opt, False)
        for label, zpath, mpath in (
            ('symlink archive input', root / 'archive_link.zip', rm),
            ('symlink manifest input', rz, root / 'manifest_link.json')):
            (zpath if 'archive' in label else mpath).symlink_to(rz if 'archive' in label else rm)
            for opt in (False, True): run(label, rb, zpath, mpath, root, opt, False)

        # Defense-in-depth coverage only. Test-local changed pins allow malformed packets
        # past the *first* check to verify that the untouched structural/member code rejects.
        # These altered namespace pins are never persisted or used for acceptance.
        structural = []
        for name, (zpath, mpath) in variants.items():
            ns = {'__name__': 'independent_structure_probe'}
            exec(compile(bb, '<pinned author bootstrap>', 'exec'), ns)
            ns['ZIP_SHA256'] = sha(zpath.read_bytes())
            ns['MANIFEST_SHA256'] = sha(mpath.read_bytes())
            try:
                ns['verify'](zpath, mpath)
            except (ValueError, OSError, TypeError, KeyError) as e:
                reason = str(e)
            else: raise RuntimeError('structural control accepted: ' + name)
            need(not sentinel.exists(), 'structural probe executed untrusted code')
            structural.append({'case': name, 'outcome': 'rejected', 'reason': reason,
                               'sentinel_absent': True, 'test_only_anchor_replacement': True})
    need((bp.read_bytes(), zp.read_bytes(), mp.read_bytes()) == (bb, zb, mb), 'originals changed')
    return {'schema': 1, 'problem_id': 30002042, 'external_pins': PINS,
            'reviewer_optimized': bool(sys.flags.optimize), 'records': records,
            'positive_runs': sum(r['outcome'] == 'accepted' for r in records),
            'negative_runs': sum(r['outcome'] == 'rejected' for r in records),
            'structure_layer_controls': structural, 'originals_unchanged': True,
            'scope': 'Infrastructure audit only; not a formal proof certificate.'}

if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
