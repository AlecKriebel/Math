#!/usr/bin/env python3
"""Fail-closed byte and acceptance replay; no mathematical proof certification."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

MANIFEST_SHA256 = 'd49bbc369c5b73e308153ca97af80f6043ed8f5cd438958e1143350c454185e0'
MANIFEST_NAME = 'PUBLICATION_MANIFEST.json'
ENTRYPOINT = 'verify_publication.py'
AZ = 'STABLE_PSEUDOISOTOPY_2950_AUTHOR_SAFE_FREEZE.zip'
AM = 'STABLE_PSEUDOISOTOPY_2950_AUTHOR_EXTERNAL_MANIFEST.json'
IZ = 'STABLE_PSEUDOISOTOPY_2950_INDEPENDENT_AUDIT_SAFE.zip'
IM = 'STABLE_PSEUDOISOTOPY_2950_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'
PINS = {
    AZ: (11204, 'c49cd7cd07b7691f1504c99cb6e8bfa03f27c00fe94171b0730e1051a718d556'),
    AM: (1632, '8159de4db930160353ee17c2e01ecf82d51f75a7389e3b06d771a5d98f219198'),
    IZ: (32127, '191e3d0a7c83b2123acb4940fbe67d0acd69aa15843be24fd6f08c91ce572af6'),
    IM: (2534, 'ab5a0ac2dd84c66856cf3698fdb4fbd7441dcd5416790f6caaacc9aed702d2cf'),
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'duplicate JSON key')
        out[k] = v
    return out

def parse(data):
    return json.loads(data, object_pairs_hook=unique)

def regular_bytes(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'nonregular file: ' + path.name)
    return path.read_bytes()

def authenticate(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'nonordinary root directory')
    raw = regular_bytes(root / MANIFEST_NAME)
    require(sha(raw) == MANIFEST_SHA256, 'publication manifest pin mismatch')
    m = parse(raw)
    require(m['problem_id'] == 2950 and m['status'] == 'unsolved' and m['approaches_used'] == 4, 'manifest identity/scope')
    expected = set(m['files']) | {MANIFEST_NAME, ENTRYPOINT}
    dirs = set()
    for name in expected:
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in name, 'unsafe path')
        dirs.update(str(x) for x in p.parents if str(x) != '.')
    found = set()
    for base, subdirs, names in os.walk(root, followlinks=False):
        for name in subdirs:
            p = Path(base) / name
            require(stat.S_ISDIR(p.lstat().st_mode), 'nonordinary subdirectory')
            require(p.relative_to(root).as_posix() in dirs, 'unexpected directory')
        for name in names:
            p = Path(base) / name
            require(stat.S_ISREG(p.lstat().st_mode), 'nonregular file')
            found.add(p.relative_to(root).as_posix())
    require(found == expected, 'file allowlist mismatch')
    buffers = {MANIFEST_NAME: raw, ENTRYPOINT: regular_bytes(root / ENTRYPOINT)}
    require(buffers[ENTRYPOINT] == regular_bytes(Path(__file__)), 'entrypoint copy mismatch')
    for name, pin in m['files'].items():
        raw = regular_bytes(root / name)
        require(type(pin['bytes']) is int and (len(raw), sha(raw)) == (pin['bytes'], pin['sha256']), 'file pin mismatch: ' + name)
        buffers[name] = raw
    for name, pin in PINS.items():
        require((len(buffers['releases/' + name]), sha(buffers['releases/' + name])) == pin, 'frozen release pin mismatch')
    return m, buffers

def archive_checks(root):
    results = []
    for label, zname, mname, count in [('original', AZ, AM, 8), ('audit', IZ, IM, 13)]:
        raw = (root / 'releases' / zname).read_bytes()
        m = parse((root / 'releases' / mname).read_bytes())
        require(m['archive'] == {'name': zname, 'bytes': len(raw), 'sha256': sha(raw)}, 'archive manifest mismatch')
        rows = m['files']
        names = [row['name'] for row in rows]
        require(len(names) == len(set(names)) == count, 'manifest inventory')
        with zipfile.ZipFile(root / 'releases' / zname) as z:
            require(len(z.namelist()) == count and set(z.namelist()) == set(names), 'ZIP inventory')
            for row in rows:
                name = row['name']
                require('/' not in name and '\\' not in name and name not in ('.', '..'), 'unsafe ZIP name')
                info = z.getinfo(name)
                require(not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG) and not info.flag_bits & 1, 'unsafe ZIP mode')
                b = z.read(info)
                require((len(b), sha(b)) == (row['bytes'], row['sha256']), 'ZIP member pin')
                require(b == (root / label / name).read_bytes(), 'expanded member mismatch')
        results.append({'directory': label, 'members': count, 'exact_match': True})
    for name in (AZ, AM):
        require((root / 'audit' / name).read_bytes() == (root / 'releases' / name).read_bytes(), 'nested original changed')
    acceptance = parse((root / 'audit/ACCEPTANCE.json').read_bytes())
    require(acceptance['decision'] == 'ACCEPT_ORIGINAL_SCOPED_PARTIAL' and acceptance['problem_id'] == 2950 and acceptance['problem_number'] == 'KP-4.74' and acceptance['rank'] == 921, 'acceptance identity')
    require(acceptance['status'] == 'unsolved' and acceptance['approaches_used'] == 4 and acceptance['approach_limit'] == 5, 'acceptance disposition')
    require(acceptance['original_members_unchanged'] is True and acceptance['repair_required'] is False, 'acceptance unchanged scope')
    for field in ['full_solution_claim', 'novelty_claim', 'formal_proof_check', 'geometric_counterexample_constructed', 'human_peer_review_claim', 'source_contents_included']:
        require(acceptance[field] is False, 'acceptance false claim: ' + field)
    require(acceptance['author_member_count'] == 8 and acceptance['full_corpus_pin_count'] == 3 and acceptance['independently_redownloaded_matching_pdf_count'] == 3, 'acceptance counts')
    for name in (AZ, AM):
        require(acceptance['accepted_inputs'][name] == {'bytes': PINS[name][0], 'sha256': PINS[name][1]}, 'acceptance exact input pin')
    return results

def run(script, args, flags, cwd):
    p = subprocess.run([sys.executable, *flags, str(script), *map(str, args)], cwd=cwd, capture_output=True, text=True, timeout=240)
    require(p.returncode == 0, 'replay failed: ' + p.stdout + p.stderr)
    return parse(p.stdout)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).absolute().parent)
    ap.add_argument('--integrity-only', action='store_true')
    for name in ['catalog', 'problems', 'reports', 'pdf-directory']:
        ap.add_argument('--' + name, type=Path)
    args = ap.parse_args()
    source = [args.catalog, args.problems, args.reports, args.pdf_directory]
    require(not any(source) or all(source), 'supply all four source-input arguments')
    require(not (args.integrity_only and any(source)), 'source replay requires full mode')
    if all(source):
        source = [p.absolute() for p in source]
    m, buffers = authenticate(args.root.absolute())
    result = {'result': 'PASS', 'problem_id': 2950, 'rank': 921, 'problem_number': 'KP-4.74', 'status': 'unsolved', 'approaches_used': 4, 'approach_limit': 5, 'files_authenticated': len(buffers), 'publication_manifest_sha256': MANIFEST_SHA256, 'mathematical_checker': False, 'formal_proof_claim': False, 'source_input_replay': 'not_run_inputs_not_supplied', 'mode': 'integrity_only' if args.integrity_only else 'full_replay'}
    with tempfile.TemporaryDirectory(prefix='stable pseudo-isotopy publication α ') as tmp:
        work = Path(tmp)
        packet = work / 'authenticated packet'
        for name, raw in buffers.items():
            p = packet / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        result['archives'] = archive_checks(packet)
        if not args.integrity_only:
            result['replays'] = []
            rel = packet / 'releases'
            for flags in (['-B'], ['-O', '-B']):
                author = run(packet / 'original/verify_packet.py', [rel / AZ, rel / AM], flags, work)
                require(author == {'result': 'PASS', 'files': 8, 'scope': 'archive_integrity_only'}, 'author replay output')
                audit = run(packet / 'audit/replay.py', [rel / IZ, rel / IM], flags, work)
                require(audit['result'] == 'PASS' and audit['audit_members'] == 13 and audit['author_members'] == 8 and audit['accepted_original_exact'] is True and audit['mathematical_proof_check'] is False, 'audit replay output')
                controls = run(packet / 'audit/test_integrity.py', [rel / AZ, rel / AM, rel / IZ, rel / IM], flags, work)
                require(controls == parse((packet / 'audit/INTEGRITY_TEST_RESULTS.json').read_bytes()) and controls['negative_control_count'] == 32, 'frozen integrity controls differ')
                result['replays'].append({'flags': flags, 'original': author, 'audit': audit, 'packet_corruption_rejections': 32})
            if all(source):
                result['source_input_replay'] = []
                expected = parse((packet / 'audit/SOURCE_PIN_RESULTS.json').read_bytes())
                for flags in (['-B'], ['-O', '-B']):
                    observed = run(packet / 'audit/verify_sources.py', source, flags, work)
                    require(observed == expected, 'source results differ from audit pins')
                    result['source_input_replay'].append({'flags': flags, 'result': observed})
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
