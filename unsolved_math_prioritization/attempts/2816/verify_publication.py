#!/usr/bin/env python3
"""Fail-closed, isolated finite replay of the exact accepted publication bytes.

Authenticate this script and PUBLICATION_MANIFEST.json against independently
delivered GitHub commit/byte hashes. An editable local manifest is not an
independent trust anchor. These checks do not prove the geometric assertions.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    'MINIMAL_FOLIATIONS_2816_AUTHOR_SAFE_FREEZE.zip': (14759, '0f9410f5d63e3d6985d9c34096c16a3eecf7f306e6281bcea49b3e806481c9d6'),
    'MINIMAL_FOLIATIONS_2816_AUTHOR_EXTERNAL_MANIFEST.json': (1942, 'b1e084a80ccd3f8192684c0155b3cd5176943b000dbc56e5e46d95e6a034d484'),
    'MINIMAL_FOLIATIONS_2816_AUTHOR_VALIDATION_RECEIPT.json': (5223, 'd22e09f027f94256657575d48b52198f612e8fcb776e9f962f81c49ca527b4e7'),
    'MINIMAL_FOLIATIONS_2816_INDEPENDENT_AUDIT_SAFE.zip': (27193, '789717f4dd9b0974555823f7fa853db7979ff7c13609636a21ed7ab0d321231e'),
    'MINIMAL_FOLIATIONS_2816_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (2819, 'ba955362412777c149178248627d75653380b29f01a29f461a8d509502cfb3a8'),
}
TOP = {'README.md', 'STATUS.json', 'RESEARCH_LOG.md', 'INPUT_VERIFICATION.json',
       'VALIDATION_RESULTS.json', 'PUBLICATION_MANIFEST.json', 'verify_publication.py'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def parsed(data):
    return json.loads(data, object_pairs_hook=unique)


def metadata(data, expected, name):
    require(type(expected) is dict and set(expected) == {'bytes', 'sha256'}, 'metadata schema: ' + name)
    require(type(expected['bytes']) is int and expected['bytes'] >= 0, 'invalid byte count: ' + name)
    require(type(expected['sha256']) is str and re.fullmatch('[0-9a-f]{64}', expected['sha256']), 'invalid digest: ' + name)
    require(len(data) == expected['bytes'] and digest(data) == expected['sha256'], 'byte pin mismatch: ' + name)


def run(script, mode, cwd, args=()):
    return subprocess.run([sys.executable, *mode, str(script), *args], cwd=cwd,
                          capture_output=True, timeout=180,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))


def audit_selftests(source, root, elsewhere):
    cases = []
    kinds = ['pristine', 'same-size-change', 'missing-file', 'extra-file', 'extra-directory',
             'symlink', 'bad-json', 'duplicate-key', 'boolean-version', 'float-size',
             'boolean-size', 'bad-digest', 'extra-schema-key', 'unexpected-argument']
    for mode in ([], ['-O'], ['-OO']):
        for kind in kinds:
            d = root / 'audit test'; shutil.copytree(source, d)
            p = d / 'MANIFEST.json'; m = parsed(p.read_bytes()); args = []
            if kind == 'same-size-change':
                f = d / 'ACCEPTANCE.md'; b = f.read_bytes(); f.write_bytes(bytes([b[0] ^ 1]) + b[1:])
            elif kind == 'missing-file': (d / 'ACCEPTANCE.md').unlink()
            elif kind == 'extra-file': (d / 'EXTRA').write_text('unexpected')
            elif kind == 'extra-directory': (d / 'EXTRA').mkdir()
            elif kind == 'symlink':
                (d / 'ACCEPTANCE.md').unlink(); (d / 'ACCEPTANCE.md').symlink_to(source / 'ACCEPTANCE.md')
            elif kind == 'bad-json': p.write_text('{')
            elif kind == 'duplicate-key': p.write_text('{"format_version":1,"format_version":1,"files":{}}')
            elif kind == 'boolean-version': m['format_version'] = True
            elif kind == 'float-size': m['files']['ACCEPTANCE.md']['bytes'] = float(m['files']['ACCEPTANCE.md']['bytes'])
            elif kind == 'boolean-size': m['files']['ACCEPTANCE.md']['bytes'] = True
            elif kind == 'bad-digest': m['files']['ACCEPTANCE.md']['sha256'] = 'broken'
            elif kind == 'extra-schema-key': m['extra'] = 1
            elif kind == 'unexpected-argument': args = ['unexpected']
            if kind in ['boolean-version', 'float-size', 'boolean-size', 'bad-digest', 'extra-schema-key']:
                p.write_text(json.dumps(m))
            r = run(d / 'verify_audit.py', mode, elsewhere, args)
            require((r.returncode == 0) == (kind == 'pristine'), 'audit selftest: ' + kind)
            require(kind == 'pristine' or b'FAIL:' in r.stderr, 'missing audit failure diagnostic')
            cases.append({'test':kind, 'mode':' '.join(mode) or 'default', 'exit_code':r.returncode,
                          'result':'PASS' if kind == 'pristine' else 'REJECTED_AS_EXPECTED',
                          'stderr':r.stderr.decode().strip()})
            shutil.rmtree(d)
    require(cases == parsed((source / 'AUDITOR_SELF_TESTS.json').read_bytes())['cases'], 'audit selftest receipt differs')
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    root = args.root.absolute()
    require(root.is_dir() and not root.is_symlink(), 'root must be an ordinary directory')
    files = {}; directories = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink rejected')
        rel = p.relative_to(root).as_posix()
        if p.is_dir(): directories.add(rel)
        else:
            require(p.is_file(), 'nonregular file rejected'); files[rel] = p.read_bytes()
    require(directories == {'author', 'independent_audit', 'frozen'}, 'directory allowlist')
    for name, (size, sha) in PINS.items():
        key = 'frozen/' + name
        require(key in files and len(files[key]) == size and digest(files[key]) == sha, 'untrusted frozen input: ' + name)
    expected = set(TOP) | {'frozen/' + name for name in PINS}
    for prefix, folder in [('AUTHOR', 'author'), ('INDEPENDENT_AUDIT', 'independent_audit')]:
        manifest = parsed(files['frozen/MINIMAL_FOLIATIONS_2816_' + prefix + '_EXTERNAL_MANIFEST.json'])
        members = manifest['files']; archive = files['frozen/' + manifest['archive']['filename']]
        require(len(members) == (10 if folder == 'author' else 17), 'frozen member count')
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            require(len(z.namelist()) == len(set(z.namelist())) and set(z.namelist()) == set(members), 'ZIP member allowlist')
            for info in z.infolist():
                name = info.filename; path = PurePosixPath(name)
                require(len(path.parts) == 1 and path.name == name and not info.is_dir() and
                        stat.S_ISREG(info.external_attr >> 16), 'unsafe ZIP member')
                b = z.read(info); metadata(b, members[name], name)
                key = folder + '/' + name; expected.add(key)
                require(files.get(key) == b, 'unpacked member differs: ' + key)
    require(set(files) == expected, 'publication file allowlist')
    manifest = parsed(files['PUBLICATION_MANIFEST.json'])
    require(type(manifest) is dict and set(manifest) == {'format_version', 'files'}, 'publication manifest schema')
    require(type(manifest['format_version']) is int and manifest['format_version'] == 1, 'publication manifest version')
    require(type(manifest['files']) is dict and set(manifest['files']) == expected - {'PUBLICATION_MANIFEST.json'}, 'manifest allowlist')
    for name, item in manifest['files'].items(): metadata(files[name], item, name)
    status = parsed(files['STATUS.json']); acceptance = parsed(files['independent_audit/ACCEPTANCE.json'])
    for record in [status, acceptance]:
        require(record['problem_id'] == 2816 and record['problem_number'] == 'KP-3.18' and
                record['catalog_rank'] == 911 and record['status'] == 'unsolved' and
                type(record['turns_used']) is int and record['turns_used'] == 3 and
                type(record['turn_limit']) is int and record['turn_limit'] == 5 and
                record['full_solution'] is False and record['novelty_claim'] is False and
                record['human_peer_review'] is False and record['verdict'] == 'ACCEPT_EXACT_ORIGINAL_SCOPED_PARTIALS', 'canonical scope changed')
    require(acceptance['mandatory_corrections'] == [] and acceptance['corrected_derivative_needed'] is False, 'acceptance changed')
    output = {'result':'PASS_PUBLICATION_INTEGRITY', 'files':len(files), 'frozen_inputs':5,
              'author_members':10, 'audit_members':17, 'status':'unsolved', 'turns_used':3,
              'source_contents_included':False, 'mathematical_proof_certified_by_computation':False}
    if not args.integrity_only:
        with tempfile.TemporaryDirectory(prefix='minimal foliation publication ') as tmp:
            staging = Path(tmp) / 'relocated inputs'; staging.mkdir()
            elsewhere = Path(tmp) / 'unrelated working directory'; elsewhere.mkdir()
            for name, data in files.items():
                p = staging / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
            replay_args = ['--archive', str(staging / 'frozen/MINIMAL_FOLIATIONS_2816_AUTHOR_SAFE_FREEZE.zip'),
                           '--manifest', str(staging / 'frozen/MINIMAL_FOLIATIONS_2816_AUTHOR_EXTERNAL_MANIFEST.json'),
                           '--receipt', str(staging / 'frozen/MINIMAL_FOLIATIONS_2816_AUTHOR_VALIDATION_RECEIPT.json')]
            for mode in ([], ['-O'], ['-OO']):
                r = run(staging / 'independent_audit/replay_independent.py', mode, elsewhere, replay_args)
                require(r.returncode == 0 and r.stdout == files['independent_audit/REPLAY_RESULTS.json'], 'isolated replay failed or changed')
            count = audit_selftests(staging / 'independent_audit', Path(tmp), elsewhere)
            output.update(result='PASS_PUBLICATION_REPLAY', replay_harness_modes=['default','-O','-OO'],
                          replay_cases_per_harness=63, author_checks_per_mode=139, independent_checks_per_mode=512,
                          author_integrity_mutations_per_mode=16, trusted_input_controls_per_harness=3,
                          audit_selftests=count, isolated=True, unrelated_working_directory=True)
    for name, data in files.items():
        require((root / name).read_bytes() == data, 'input changed during verification')
    output['inputs_unchanged'] = True
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
