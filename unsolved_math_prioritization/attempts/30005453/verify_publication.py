#!/usr/bin/env python3
"""Verify the exact safe publication; replay diagnostics in temporary directories."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, importlib.util, json, os, stat, subprocess, sys, tempfile, zipfile
sys.dont_write_bytecode = True
ANCHORS = {
    'AUTHOR_SAFE_FREEZE': (19790, '4e2b7cbf89688b04a80bfae946457582f8970cb90d6af260302aa1dad3a33856', 'author_v1', 11),
    'AUTHOR_V2_PROPOSED_SAFE': (20008, '689cd325db19a449e373441c0c7cb0ede0e103456ec857215a207b7af83d3d8d', 'author_v2', 11),
    'INDEPENDENT_AUDIT_SAFE': (29473, 'e459a35c00246f2cd5db956283e1dced8b0665524919a461dd42e964d20f22cd', 'first_audit', 16),
    'V2_ACCEPTANCE_SAFE': (51136, '3d41e5d4a1b68778252a3e313ef36b8aad3220fb945154daccdd31f3f675226f', 'v2_acceptance', 14),
}


def require(test, message):
    if not test:
        raise ValueError(message)


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def object_without_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def decode(data):
    return json.loads(data, object_pairs_hook=object_without_duplicates)


def safe_relative(name):
    p = PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts
            and str(p) == name and '\\' not in name, 'Unsafe path: ' + name)
    return p


def inventory(root):
    files, directories = set(), set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink in publication')
        name = path.relative_to(root).as_posix()
        if path.is_dir():
            directories.add(name)
        else:
            require(stat.S_ISREG(path.stat().st_mode), 'Nonregular file')
            files.add(name)
    return files, directories


def verify(root):
    root = Path(root)
    m = decode((root / 'PUBLICATION_MANIFEST.json').read_bytes())
    entries = m['files']
    names = [e['path'] for e in entries]
    require(len(names) == len(set(names)), 'Duplicate publication manifest entry')
    actual, directories = inventory(root)
    require(actual == set(names) | {'PUBLICATION_MANIFEST.json'}, 'Publication inventory mismatch')
    require(directories == set(m['directories']), 'Publication directory inventory mismatch')
    for entry in entries:
        name = str(safe_relative(entry['path']))
        require(identity((root / name).read_bytes()) == {k: entry[k] for k in ('bytes', 'sha256')},
                'Publication byte identity: ' + name)
    p = decode((root / 'PUBLICATION_PROVENANCE.json').read_bytes())
    require(len(p['archives']) == len(ANCHORS), 'Archive provenance count')
    listed = {x['path']: x for x in p['archives']}
    require(len(listed) == len(ANCHORS), 'Duplicate archive provenance')
    all_payloads = {}
    for suffix, (size, digest, directory, count) in ANCHORS.items():
        archive_name = 'SUBCRITICAL_REINFORCEMENT_30005453_' + suffix + '.zip'
        relative = 'frozen_archives/' + archive_name
        raw = (root / relative).read_bytes()
        require(identity(raw) == {'bytes': size, 'sha256': digest}, 'Frozen ZIP anchor: ' + suffix)
        record = listed[relative]
        require(record['extracted_directory'] == directory and record['member_count'] == count,
                'Archive provenance structure')
        require({k: record[k] for k in ('bytes', 'sha256')} == identity(raw), 'Archive provenance identity')
        target = root / directory
        disk_files, disk_dirs = inventory(target)
        with zipfile.ZipFile(root / relative) as z:
            infos = z.infolist()
            names = [i.filename for i in infos]
            require(len(names) == len(set(names)) == count, 'ZIP member count/duplicates')
            require(set(names) == disk_files, 'ZIP versus extracted inventory')
            require(z.testzip() is None, 'ZIP CRC')
            contents = {}
            for info in infos:
                name = str(safe_relative(info.filename))
                mode = info.external_attr >> 16
                require(not info.is_dir() and not stat.S_ISLNK(mode) and not info.flag_bits & 1,
                        'ZIP unsupported member')
                require(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'ZIP nonregular member')
                contents[name] = z.read(info)
                require(contents[name] == (target / name).read_bytes(), 'ZIP/extracted byte mismatch')
        all_payloads[directory] = contents
        fm = decode(contents['MANIFEST.json'])
        items = fm['files']
        fnames = [x['path'] for x in items]
        require(len(fnames) == len(set(fnames)) == count - 1, 'Frozen manifest count/duplicates')
        require(set(fnames) == disk_files - {'MANIFEST.json'}, 'Frozen manifest coverage')
        require(identity(contents['MANIFEST.json'])['sha256'] == record['manifest_sha256'], 'Manifest anchor')
        for item in items:
            safe_relative(item['path'])
            require(identity(contents[item['path']]) == {k: item[k] for k in ('bytes', 'sha256')},
                    'Frozen manifest byte identity')
    path = root / 'v2_acceptance/code/verify_delta.py'
    spec = importlib.util.spec_from_file_location('accepted_delta', path)
    delta = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(delta)
    checked = delta.verify_delta(all_payloads['author_v1'], all_payloads['author_v2'])
    require(checked['analytic_sections_2_through_8_bytes'] == 12593, 'Analytic core size')
    require(checked['analytic_sections_2_through_8_sha256'] ==
            'd9da7dc05a3debfd2537a00f0a193b72f6e8714bbe3e8389f5dc6b9a916a9e54', 'Analytic core hash')
    return {'status': 'PASS', 'payload_files': len(actual), 'archive_members': 52,
            'archives': 4, 'all_frozen_manifests': 'PASS', 'approved_v2_delta': 'PASS',
            'analytic_sections_2_through_8_bytes': 12593, 'exact_recursive_inventory': True}


def verify_queue(root, base_path, updated_path):
    record = decode((Path(root) / 'QUEUE_DELTA.json').read_bytes())
    base, updated = Path(base_path).read_bytes(), Path(updated_path).read_bytes()
    require(identity(base) == record['base'] and identity(updated) == record['updated'], 'Queue hashes')
    old, new = base.splitlines(keepends=True), updated.splitlines(keepends=True)
    require(len(old) == len(new), 'Queue line count')
    indices = [i for i, line in enumerate(old) if b'| 30005453 / OWR-12697708-006 |' in line]
    require(len(indices) == 1, 'Queue target uniqueness')
    i = indices[0]
    require(i + 1 == record['row_line_1_based'], 'Queue row position')
    require(old[:i] == new[:i] and old[i+1:] == new[i+1:], 'Unrelated queue bytes changed')
    a, b = old[i].split(b'|'), new[i].split(b'|')
    require(len(a) == len(b), 'Queue cell count')
    require([j for j in range(len(a)) if a[j] != b[j]] == [8, 9, 11], 'Queue changed cell set')
    require(len(record['changes']) == 3, 'Queue change-record count')
    for j, name, change in zip((8, 9, 11), ('Status', 'Turns', 'Findings'), record['changes']):
        require(change['column'] == name and a[j].decode().strip() == change['old']
                and b[j].decode().strip() == change['new'], 'Queue change-record value')
    require(b[8].strip() == b'claimed_solved' and b[9].strip() == b'4/5', 'Queue disposition')
    return {'status': 'PASS', 'changed_cells': ['Status', 'Turns', 'Findings'],
            'all_other_bytes_preserved': True, 'stale_header_preserved': True}


def replay(root):
    root = Path(root).resolve()
    before = {p.relative_to(root).as_posix(): identity(p.read_bytes())
              for p in root.rglob('*') if p.is_file()}
    code = root / 'v2_acceptance/code'
    records = []
    with tempfile.TemporaryDirectory(prefix='reinforcement-publication-replay-') as temp:
        for optimize in (False, True):
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='1' if optimize else '0')
            flags = ['-B'] + (['-O'] if optimize else [])
            for script, expected, use_inputs in (
                    ('verify_delta.py', 'delta_checks.json', True),
                    ('targeted_checks.py', 'targeted_checks.json', False),
                    ('replay_inputs.py', 'input_replays.json', True)):
                output = Path(temp) / ('optimized_' if optimize else 'normal_') / expected
                output.parent.mkdir(exist_ok=True)
                command = [sys.executable, *flags, str(code / script)]
                if use_inputs:
                    command += ['--input-dir', str(root / 'frozen_archives')]
                command += ['--output', str(output)]
                result = subprocess.run(command, env=env, cwd=temp, capture_output=True, text=True, timeout=180)
                require(result.returncode == 0, script + ': ' + result.stderr)
                raw = output.read_bytes()
                require(raw == (root / 'v2_acceptance/results' / expected).read_bytes(),
                        'Replay result bytes differ: ' + expected)
                require(decode(raw)['status'] == 'PASS', 'Replay status')
                records.append({'script': script, 'mode': 'optimized' if optimize else 'normal',
                                'exact_result_bytes': True, **identity(raw)})
            result = subprocess.run([sys.executable, *flags, str(code / 'verify_package.py')],
                                    env=env, cwd=temp, capture_output=True, text=True, timeout=30)
            require(result.returncode == 0 and decode(result.stdout)['status'] == 'PASS',
                    'Acceptance verifier failed')
    after = {p.relative_to(root).as_posix(): identity(p.read_bytes())
             for p in root.rglob('*') if p.is_file()}
    require(before == after, 'Replay modified publication')
    return {'status': 'PASS', 'records': records, 'acceptance_manifest_both_modes': 'PASS',
            'all_publication_bytes_unchanged': True,
            'scope': 'Integrity and finite diagnostics; analytic review remains in the proof and reports.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replay', action='store_true')
    ap.add_argument('--queue-base', type=Path)
    ap.add_argument('--queue-updated', type=Path)
    args = ap.parse_args()
    require(bool(args.queue_base) == bool(args.queue_updated), 'Supply both queue paths')
    root = Path(__file__).resolve().parent
    out = verify(root)
    if args.queue_base:
        out['queue'] = verify_queue(root, args.queue_base, args.queue_updated)
    if args.replay:
        out['replay'] = replay(root)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
