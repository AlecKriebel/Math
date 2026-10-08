#!/usr/bin/env python3
"""Authenticate a source-free prior-proof audit and replay bounded controls."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile

ACCEPTED = {'ROBUST_INTERPOLATION_2508_AUDIT.tar.gz': {'bytes': 17247, 'sha256': '74b4b17367e5926f3fcf35307e8dff9c0d8cd37923b20066d31fe8bdfb1c9203'}, 'ROBUST_INTERPOLATION_2508_INDEPENDENT_AUDIT.tar.gz': {'bytes': 14569, 'sha256': '2fd59af57e01c38fc3a25b4a98f69c925eef917fb0840f2a784dd9a60c761783'}, 'author/EXTERNAL_PINS.json': {'bytes': 197, 'sha256': '7f750c61445454d46c24567ca9d270adfe6db5250b92b8631a0dcfbb72cee18b'}, 'author/FINAL_RECEIPT.json': {'bytes': 509, 'sha256': 'b7734fabab1014dc7f0284ea2e6c7bfa370ff2de0eb41368d9ef4f0dcb9f665e'}, 'author/FROZEN_METADATA.json': {'bytes': 2976, 'sha256': 'baf6e1ac604e413d3b5872f6874769846e03e0c73fcca631377a4fdd5d4b2176'}, 'author/evidence/controls.json': {'bytes': 915, 'sha256': '45d15960b792e6cf28550cbe5325e9bca8685392663057ec46bfe4309dfb7cbf'}, 'author/evidence/readonly_full_source_replay.json': {'bytes': 459, 'sha256': 'af5ba52c8ed293d7e48ab47584e58d9259b3e86804be3d829176a8bb48917bdc'}, 'author/evidence/source_negative_controls.json': {'bytes': 504, 'sha256': '03fe44226a0b7e394bd78305044a9e8565ddf901950c4e55b2d92143b249a29c'}, 'author/evidence/source_replay_O.json': {'bytes': 316, 'sha256': 'a2cc62785132f7a073ba53ae2b6dfe2bb75efd637549158d92da4f2b28c48914'}, 'author/evidence/source_replay_OO.json': {'bytes': 316, 'sha256': 'a2cc62785132f7a073ba53ae2b6dfe2bb75efd637549158d92da4f2b28c48914'}, 'author/evidence/source_replay_normal.json': {'bytes': 316, 'sha256': 'a2cc62785132f7a073ba53ae2b6dfe2bb75efd637549158d92da4f2b28c48914'}, 'author/public/CLAIMS.json': {'bytes': 537, 'sha256': '23bd1984cf07c19226a17ef2a75168867d56e67392592c1faff1f769dd07a6c6'}, 'author/public/FIXTURES.json': {'bytes': 11203, 'sha256': '743372fe50b260157aef7f399fb8a0807bc922902e0055d7e3f8249625c84054'}, 'author/public/MANIFEST.json': {'bytes': 1077, 'sha256': '97185d9d301079510b35dcc78944f1f536c10e34f4de5222aadf474093b1b15d'}, 'author/public/README.md': {'bytes': 1830, 'sha256': '256bfb51d5eb961cc887a725c66cd305041ed96c4ad308a81b359c27f14f14d9'}, 'author/public/REPORT.md': {'bytes': 15599, 'sha256': '0ef88e9b4a73ab4028e16dc98f641a55a0c157958b1da3ce615d9092a62ad053'}, 'author/public/SOURCES.json': {'bytes': 3531, 'sha256': 'b91f0393d94a7c3b9bfaa725ff805c0145230e65ca0f253f0a077fcc47615b05'}, 'author/public/controls.py': {'bytes': 8455, 'sha256': 'ecba357f295745f612a98a591bcbdc3853a2c42f092d5bc2f018e7cfb5cc45eb'}, 'author/public/verify.py': {'bytes': 9994, 'sha256': '14733b9582625d2cdecc12312832a3af5b1f4737646088a54b7f4b9c8586af8d'}, 'independent_audit/FINAL_RECEIPT.json': {'bytes': 985, 'sha256': 'b337625f6509b8a6ce45faa6e01c3ae1d6cd8dd5a85dc6506ad5920c2e3347f6'}, 'independent_audit/INDEPENDENT_AUDIT.md': {'bytes': 20780, 'sha256': 'c5e810827380a1d9e4b7faf75fe6832bae5e1d03864ec5d3b9eaff836b68a779'}, 'independent_audit/MANIFEST.json': {'bytes': 1202, 'sha256': 'aab77e1317076d4369cb0ba8b585773b95675e174f4dd22929c8f175ec9df9ce'}, 'independent_audit/SCOPE.json': {'bytes': 1182, 'sha256': '8853b3746b3194d3d72f9fe8014644f6032df7fd7e10b7c1afc35ba73f7bae62'}, 'independent_audit/evidence/archive_review.json': {'bytes': 1071, 'sha256': '7f9bd3fdcb0482a0e2b7395ef388e34eaaa7ac292c34a105a9fb1b9ba26fe3e9'}, 'independent_audit/evidence/independent_controls.json': {'bytes': 915, 'sha256': '45d15960b792e6cf28550cbe5325e9bca8685392663057ec46bfe4309dfb7cbf'}, 'independent_audit/evidence/independent_full_checks.json': {'bytes': 9337, 'sha256': '1304044a413be0fda04a5d9ac5a9a24ca3149629b3a9f9512998d4d52092cea6'}, 'independent_audit/evidence/source_normal.json': {'bytes': 316, 'sha256': 'a2cc62785132f7a073ba53ae2b6dfe2bb75efd637549158d92da4f2b28c48914'}, 'independent_audit/independent_checks.py': {'bytes': 11403, 'sha256': 'cc32cb3a1fac6c483d480e3d0698020083b9f178bac594c363947edbbdbf4a2e'}}
AUTHOR = ['EXTERNAL_PINS.json', 'FROZEN_METADATA.json', 'evidence/controls.json', 'evidence/readonly_full_source_replay.json', 'evidence/source_negative_controls.json', 'evidence/source_replay_O.json', 'evidence/source_replay_OO.json', 'evidence/source_replay_normal.json', 'public/CLAIMS.json', 'public/FIXTURES.json', 'public/MANIFEST.json', 'public/README.md', 'public/REPORT.md', 'public/SOURCES.json', 'public/controls.py', 'public/verify.py']
AUDIT = ['INDEPENDENT_AUDIT.md', 'MANIFEST.json', 'SCOPE.json', 'evidence/archive_review.json', 'evidence/independent_controls.json', 'evidence/independent_full_checks.json', 'evidence/source_normal.json', 'independent_checks.py']
DIRS = {'independent_audit', 'author/public', 'independent_audit/evidence', 'author/evidence', 'author'}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
AUTHOR_PIN = '97185d9d301079510b35dcc78944f1f536c10e34f4de5222aadf474093b1b15d'
AUTHOR_VERIFIER = '14733b9582625d2cdecc12312832a3af5b1f4737646088a54b7f4b9c8586af8d'
MODES = [('normal', []), ('-O', ['-O']), ('-OO', ['-OO'])]

def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return set(a) == set(b) and all(same(a[k], v) for k, v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('nonfinite JSON number')


def finite(value):
    result = float(value)
    need(math.isfinite(result), 'overflowed JSON number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite, parse_float=finite)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object schema')


def exact_int(value, expected=None):
    need(type(value) is int and value >= 0 and (expected is None or value == expected), 'exact nonnegative integer')


def digest(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'lowercase SHA-256')


def inventory(root):
    for path in (root, *root.parents):
        need(stat.S_ISDIR(path.lstat().st_mode), 'linked/non-directory root or ancestor')
    files, dirs = set(), set()
    def visit(directory):
        for entry in os.scandir(directory):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'extra directory')
                dirs.add(name)
                visit(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special member')
                files.add(name)
    visit(root)
    need(files == FILES and dirs == DIRS, 'exact recursive inventory')


def ordinary(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000, 'regular bounded member')
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'member replaced at open')
        raw = stream.read(1000001)
    need(len(raw) == before.st_size, 'member size changed')
    return raw


def manifest(value, snapshot, payload, role=None):
    keys(value, ['schema', 'problem_id', 'files'] + (['role'] if role is not None else []))
    if role is not None:
        need(same(value['role'], role), 'manifest role')
    exact_int(value['schema'], 1)
    exact_int(value['problem_id'], 2508)
    rows = value['files']
    need(type(rows) is list and len(rows) == len(payload), 'manifest list length/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        name = row['path']
        need(type(name) is str and name in payload and name not in seen, 'unknown/duplicate manifest path')
        seen.add(name)
        exact_int(row['bytes']); digest(row['sha256'])
        need(same(row, dict(path=name, bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'manifest byte binding')
    need(seen == payload, 'manifest inventory')



def archive(raw, snapshot, prefix, names):
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as package:
        entries = package.getmembers()
        need(len(entries) == len(names), 'archive member count')
        need(len({e.name for e in entries}) == len(entries), 'duplicate archive path')
        need({e.name for e in entries} == set(names), 'archive exact inventory')
        need(not package.pax_headers, 'archive global extensions')
        for entry in entries:
            need(entry.isreg() and not entry.pax_headers and not entry.linkname, 'archive regular member')
            need(entry.size == len(snapshot[prefix+entry.name]), 'archive member size')
            stream = package.extractfile(entry)
            need(stream is not None and stream.read(1000001) == snapshot[prefix+entry.name], 'archive byte comparison')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap pin')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot, PAYLOAD)
    for name, row in ACCEPTED.items():
        need(same(row, dict(bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'accepted bytes changed')
    # Every historical JSON object is exact-byte authenticated above and strictly
    # parsed for duplicate keys/nonfinite numbers. This is not generic semantic
    # certification of arbitrary newly repinned historical descriptive metadata.
    archive(snapshot['ROBUST_INTERPOLATION_2508_AUDIT.tar.gz'], snapshot, 'author/', AUTHOR)
    archive(snapshot['ROBUST_INTERPOLATION_2508_INDEPENDENT_AUDIT.tar.gz'], snapshot, 'independent_audit/', AUDIT)
    claims = parsed['author/public/CLAIMS.json']
    need(type(claims['new_approaches']) is int and claims['new_approaches'] == 0, 'approach scope')
    need(claims['classification'] == 'PRIOR_SOLUTION_VERIFIED_RELATIVE_TO_IMPORTED_THEOREMS', 'classification')
    for name in ['new_discovery_claimed','community_acceptance_verified','proof_assistant_verified','effective_constants_in_C_claimed','finite_checks_prove_theorem']:
        need(claims[name] is False, 'claim scope')
    inventory(root)
    return snapshot, parsed


def thaw(root):
    # Only ever applied to disposable copies, never the accepted packet.
    root.chmod(0o755)
    for path in root.rglob('*'):
        if not path.is_symlink():
            path.chmod(0o755 if path.is_dir() else 0o644)


def run(verifier, root, pin, mode, cwd, env):
    result = subprocess.run([sys.executable, '-I', '-S', '-B', *mode, str(verifier),
                             '--root', str(root), '--manifest-sha256', pin],
                            cwd=cwd, env=env, capture_output=True, timeout=120)
    return result


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() != 0, 'actual nonroot required')
    with tempfile.TemporaryDirectory(prefix='ep1133-publication-') as temporary:
        work = Path(temporary)
        public = work/'public'; public.mkdir()
        cwd = work/'cwd'; cwd.mkdir()
        for name in AUTHOR:
            if name.startswith('public/'):
                (public/name.split('/',1)[1]).write_bytes(snapshot['author/'+name])
        env = dict(PATH=os.defpath, HOME=str(work), TMPDIR=str(work), LC_ALL='C',
                   PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', PYTHONSAFEPATH='1')
        # Run the exact accepted author harness on a disposable writable copy.
        # Its own read-only relocation and 28 mutation categories are unchanged.
        controls = subprocess.run([sys.executable, '-I', '-S', '-B', str(public/'controls.py'),
            '--root', str(public), '--manifest-sha256', AUTHOR_PIN,
            '--verifier-sha256', AUTHOR_VERIFIER], cwd=cwd, env=env,
            capture_output=True, timeout=240)
        need(controls.returncode == 0 and controls.stderr == b'', 'author controls failed')
        author = parse(controls.stdout)
        expected = dict(parsed['author/evidence/controls.json'])
        expected['nonroot_euid'] = os.geteuid()
        need(same(author, expected), 'author control output differs')
        baseline = [run(public/'verify.py', public, AUTHOR_PIN, flags, cwd, env) for _, flags in MODES]
        need(all(x.returncode == 0 and x.stderr == b'' for x in baseline), 'source-free baseline')
        need(len({x.stdout for x in baseline}) == 1, 'optimization mismatch')
        result = parse(baseline[0].stdout)
        need(same(result['finite_evidence'], dict(parameter_cases=80, large_n_arithmetic_cases=400,
                 finite_block_patterns=15192)), 'finite coverage')
        need(same(result['source_replay'], dict(performed=False, reason='external source files not supplied')), 'default source replay overclaim')
        # Portable subset of the accepted independent audit's hostile cases.
        # Its two source-bound metadata and six source-input categories are omitted.
        tests = [
            ('boolean_claim_integer','CLAIMS.json',lambda c:c.update(new_approaches=False)),
            ('integer_claim_boolean','CLAIMS.json',lambda c:c.update(new_discovery_claimed=0)),
            ('float_claim_integer','CLAIMS.json',lambda c:c.update(rank=1037.0)),
            ('extra_claim','CLAIMS.json',lambda c:c.update(extra=True)),
            ('integer_fixture_boolean','FIXTURES.json',lambda c:c.update(finite_evidence_only=1)),
            ('boolean_fraction_denominator','FIXTURES.json',lambda c:c['parameters'][0].update(eta=[1,True])),
            ('negative_fraction_numerator','FIXTURES.json',lambda c:c['parameters'][0].update(eta=[-1,100])),
            ('float_fraction_numerator','FIXTURES.json',lambda c:c['parameters'][0].update(eta=[1.0,100])),
            ('boolean_threshold','FIXTURES.json',lambda c:c['parameters'][0].update(n0=True)),
            ('negative_infinity_threshold','FIXTURES.json',lambda c:c['parameters'][0].update(n0=float('-inf'))),
            ('boolean_dataset_bytes','SOURCES.json',lambda c:c['dataset_pins'][0].update(bytes=True)),
            ('float_dataset_bytes','SOURCES.json',lambda c:c['dataset_pins'][0].update(bytes=68931837.0)),
            ('nan_source_metadata','SOURCES.json',lambda c:c.update(checked_utc=float('nan'))),
            ('uppercase_source_digest','SOURCES.json',lambda c:c['scholarly_sources'][0].update(sha256='A'*64)),
            ('integer_source_boolean','SOURCES.json',lambda c:c.update(research_entry_present=0))]
        rejections = []
        for label, filename, mutate in tests + [('duplicate_claim_key', 'CLAIMS.json', None), ('wrong_external_manifest_pin', None, None)]:
            copy = work/label; shutil.copytree(public, copy); thaw(copy)
            pin = AUTHOR_PIN
            if filename:
                p=copy/filename
                if mutate:
                    obj=json.loads(p.read_bytes()); mutate(obj)
                    p.write_text(json.dumps(obj,indent=2,allow_nan=True)+'\n')
                else:
                    p.write_bytes(p.read_bytes().replace(b'"new_approaches": 0',b'"new_approaches": 0, "new_approaches": 0'))
                m=json.loads((copy/'MANIFEST.json').read_bytes())
                for row in m['files']:
                    raw=(copy/row['path']).read_bytes();row.update(bytes=len(raw),sha256=sha(raw))
                (copy/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
                pin=sha((copy/'MANIFEST.json').read_bytes())
            else:
                pin='0'*64
            for mode,flags in MODES:
                x=run(public/'verify.py',copy,pin,flags,cwd,env)
                need(x.returncode != 0 and x.stderr.startswith(b'REJECT:'), 'independent portable mutation accepted')
                rejections.append(dict(label=label,mode=mode,rejected=True))
        # Genuine read-only portable baseline, verified with denied write probes.
        ro=work/'readonly';shutil.copytree(public,ro)
        before={p.name:sha(p.read_bytes()) for p in ro.iterdir()}
        for p in ro.iterdir():p.chmod(0o444)
        ro.chmod(0o555);cwd.chmod(0o555)
        denied=0
        try:
            for p in [ro/'NEW_FILE',ro/'REPORT.md',cwd/'NEW_FILE']:
                try:
                    with p.open('ab') as stream:stream.write(b'forbidden')
                except PermissionError:denied+=1
                else:raise ValueError('read-only write succeeded')
            for mode,flags in MODES:
                x=run(ro/'verify.py',ro,AUTHOR_PIN,flags,cwd,env)
                need(x.returncode==0 and x.stderr==b'' and x.stdout==baseline[0].stdout,'read-only replay differs')
            need(before=={p.name:sha(p.read_bytes()) for p in ro.iterdir()},'read-only bytes changed')
        finally:
            thaw(ro);cwd.chmod(0o755)
        return dict(finite_evidence=result['finite_evidence'], modes=[x[0] for x in MODES],
            author_fresh_bundle_rejections=84, author_historical_optional_source_rejections=6,
            author_historical_total_rejections=90, author_optional_source_replay='NOT_RUN',
            independent_fresh_portable_rejections=len(rejections), independent_omitted_source_rejections=24,
            independent_historical_full_rejections=75, independent_full_source_harness='NOT_RUN',
            independent_portable_categories=[x['label'] for x in rejections[::3]],
            actual_nonroot_readonly=True,readonly_write_probes_denied=denied,
            fresh_sources='NOT_RUN',fresh_corpora='NOT_RUN',
            compactness_proved_by_computation=False,formal_proof_verification=False)


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:]
    root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin)
    result=replay(snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'packet changed during replay')
    result.update(schema=1,status='PASS',problem_id=2508,publication_files=len(FILES),
                  queue_status='already_solved',substantive_turns='0/5',
                  manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True,allow_nan=False))


if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,TypeError,KeyError,tarfile.TarError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr)
        sys.exit(1)
