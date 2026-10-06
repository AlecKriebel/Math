#!/usr/bin/env python3
"""Replay finite packet checks. These checks do not certify mathematical prose."""
import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    def unique(pairs):
        d = {}
        for k, v in pairs:
            require(k not in d, 'duplicate JSON key')
            d[k] = v
        return d
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def seal(root):
    manifest = {p.name: {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
                for p in sorted(root.iterdir()) if p.name != 'FILES_SHA256.json'}
    (root / 'FILES_SHA256.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')


def verify_archive(archive, manifest, pin):
    data = archive.read_bytes()
    require(len(data) == pin['bytes'] and digest(data) == pin['sha256'], 'archive pin mismatch')
    require(digest(manifest.read_bytes()) == pin['manifest_sha256'], 'manifest pin mismatch')
    m = load(manifest)
    require(m['archive_bytes'] == len(data) and m['archive_sha256'] == digest(data), 'archive manifest mismatch')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'duplicate ZIP member')
        require(set(names) == {x['path'] for x in m['files']}, 'ZIP member set mismatch')
        for x in m['files']:
            p = Path(x['path'])
            require(not p.is_absolute() and '..' not in p.parts, 'unsafe archive path')
            require(stat.S_ISREG(z.getinfo(x['path']).external_attr >> 16), 'non-regular ZIP member')
            b = z.read(x['path'])
            require(len(b) == x['bytes'] and digest(b) == x['sha256'], 'member pin mismatch')
    return m


def run_checker(checker, root, flags, cwd):
    p = subprocess.run([sys.executable, *flags, str(checker), '--root', str(root)],
                       cwd=cwd, capture_output=True, text=True, timeout=30)
    return p


def packet_tests(archive, name):
    results = {'label': name, 'positive': [], 'tamper': [], 'trust_boundary': []}
    with tempfile.TemporaryDirectory(prefix='normal invariants audit ') as t:
        base = Path(t)
        root = base / 'relocated packet α'
        root.mkdir()
        with zipfile.ZipFile(archive) as z:
            z.extractall(root)
        checker = root / 'verify_packet.py'
        for flags in (['-B'], ['-O', '-B']):
            p = run_checker(checker, root, flags, base)
            require(p.returncode == 0, 'positive checker failed: ' + p.stderr)
            results['positive'].append({'flags': flags, 'returncode': 0, 'result': json.loads(p.stdout), 'relocated': True})
        controls = ['wrong_problem', 'solved_claim', 'missing_scope', 'wrong_turns',
                    'missing_file', 'extra_file', 'duplicate_key', 'hash_mismatch',
                    'wrong_code', 'new_solution', 'counterexample', 'wrong_limit',
                    'boolean_turn', 'wrong_statement', 'wrong_pair', 'source_contents',
                    'dataset_contents', 'duplicate_source_id', 'non_https_source',
                    'bad_byte_count', 'boolean_byte_count', 'duplicate_manifest_key',
                    'symlink_member', 'directory_member']
        for control in controls:
            d = base / ('tamper_' + control)
            shutil.copytree(root, d)
            sp = d / 'status.json'
            s = load(sp)
            status_changes = {'wrong_problem': ('problem_id', 30002928), 'solved_claim': ('full_problem_solved', True),
                              'wrong_turns': ('turns_used', 6), 'wrong_code': ('problem_number', 'KP-4.51'),
                              'new_solution': ('new_solution_claimed', True), 'counterexample': ('counterexample_claimed', True),
                              'wrong_limit': ('turn_limit', 6), 'boolean_turn': ('turns_used', True)}
            if control in status_changes:
                k, v = status_changes[control]
                s[k] = v
                sp.write_text(json.dumps(s))
                seal(d)
            elif control == 'missing_scope':
                del s['conditional_results_only']
                sp.write_text(json.dumps(s))
                seal(d)
            elif control == 'missing_file':
                (d / 'PROOF.md').unlink()
            elif control == 'extra_file':
                (d / 'unapproved.txt').write_text('test')
            elif control == 'duplicate_key':
                sp.write_text(sp.read_text().replace('{', '{"problem_id":2928,', 1))
                seal(d)
            elif control == 'hash_mismatch':
                (d / 'PROOF.md').write_text((d / 'PROOF.md').read_text() + '\nchanged\n')
            elif control in ['wrong_statement', 'wrong_pair', 'source_contents', 'dataset_contents']:
                p = d / 'verification_metadata.json'
                m = load(p)
                keys = {'wrong_statement': ('statement_sha256', '0' * 64), 'wrong_pair': ('paired_record_sha256', '0' * 64),
                        'source_contents': ('source_contents_included', True), 'dataset_contents': ('dataset_contents_included', True)}
                k, v = keys[control]
                m[k] = v
                p.write_text(json.dumps(m))
                seal(d)
            elif control in ['duplicate_source_id', 'non_https_source']:
                p = d / 'sources.json'
                m = load(p)
                if control == 'duplicate_source_id':
                    m[0]['id'] = m[1]['id']
                else:
                    m[0]['url'] = 'file:///invalid'
                p.write_text(json.dumps(m))
                seal(d)
            elif control in ['bad_byte_count', 'boolean_byte_count']:
                p = d / 'FILES_SHA256.json'
                m = load(p)
                m['PROOF.md']['bytes'] = True if control == 'boolean_byte_count' else 0
                p.write_text(json.dumps(m))
            elif control == 'duplicate_manifest_key':
                p = d / 'FILES_SHA256.json'
                p.write_text(p.read_text().replace('{', '{"PROOF.md":{},', 1))
            elif control == 'symlink_member':
                p = d / 'PROOF.md'
                p.unlink()
                p.symlink_to(root / 'PROOF.md')
            elif control == 'directory_member':
                p = d / 'PROOF.md'
                p.unlink()
                p.mkdir()
            for flags in (['-B'], ['-O', '-B']):
                p = run_checker(checker, d, flags, base)
                require(p.returncode != 0, 'tamper accepted: ' + control)
                results['tamper'].append({'control': control, 'flags': flags, 'rejected': True})
        # The local manifest is not an independent trust root. External pins catch resealing.
        for control in ['rehashed_unchecked_rank', 'rehashed_prose']:
            d = base / control
            shutil.copytree(root, d)
            if control == 'rehashed_unchecked_rank':
                p = d / 'status.json'
                s = load(p)
                s['rank'] = 1
                p.write_text(json.dumps(s))
            else:
                p = d / 'PROOF.md'
                p.write_text(p.read_text() + '\nTest-only altered prose.\n')
            seal(d)
            for flags in (['-B'], ['-O', '-B']):
                p = run_checker(checker, d, flags, base)
                require(p.returncode == 0, 'trust probe changed unexpectedly')
                external_rejects = any((d / p.name).read_bytes() != p.read_bytes() for p in root.iterdir())
                require(external_rejects, 'external pin should detect altered bytes')
                results['trust_boundary'].append({'control': control, 'flags': flags,
                                                  'packet_checker_accepts': True, 'external_member_pins_reject': True})
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--release-directory', type=Path, required=True)
    ap.add_argument('--pins', type=Path, default=Path(__file__).with_name('release_pins.json'))
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    pins = load(args.pins)
    out = {'problem_id': 2928, 'scope': 'finite integrity, conservative fields, relocation, and trust-boundary tests only', 'packets': []}
    for label, pin in pins.items():
        archive = (args.release_directory / pin['archive']).resolve()
        manifest = (args.release_directory / pin['manifest']).resolve()
        verify_archive(archive, manifest, pin)
        out['packets'].append(packet_tests(archive, label))
    raw = json.dumps(out, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(raw)
    print(json.dumps({'result': 'PASS', 'packets': len(out['packets']),
                      'positive_runs': sum(len(x['positive']) for x in out['packets']),
                      'tamper_rejections': sum(len(x['tamper']) for x in out['packets']),
                      'trust_probes': sum(len(x['trust_boundary']) for x in out['packets'])}, sort_keys=True))


if __name__ == '__main__':
    main()
