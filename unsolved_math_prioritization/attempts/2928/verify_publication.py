#!/usr/bin/env python3
"""Authenticate and replay an exact partial-result packet. No theorem certification."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

MANIFEST_SHA256 = '20be2e2092c30e50346ca1ddf2b644b9d5b6fbf5b79cf521812fe76ede87a8a7'
MANIFEST_NAME = 'PUBLICATION_MANIFEST.json'
ENTRYPOINT = 'verify_publication.py'

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

def read_json(data):
    return json.loads(data, object_pairs_hook=unique)

def regular_bytes(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'non-regular file: ' + path.name)
    return path.read_bytes()

def authenticate(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'root is not an ordinary directory')
    data = regular_bytes(root / MANIFEST_NAME)
    require(sha(data) == MANIFEST_SHA256, 'publication manifest pin mismatch')
    manifest = read_json(data)
    require(manifest['problem_id'] == 2928 and manifest['disposition'] == 'unsolved', 'manifest identity')
    records = manifest['files']
    expected = set(records) | {MANIFEST_NAME, ENTRYPOINT}
    dirs = set()
    for name in expected:
        pp = PurePosixPath(name)
        require(not pp.is_absolute() and '..' not in pp.parts and '\\' not in name, 'unsafe member name')
        dirs.update(str(p) for p in pp.parents if str(p) != '.')
    found = set()
    for base, subdirs, names in os.walk(root, followlinks=False):
        for d in subdirs:
            p = Path(base) / d
            require(stat.S_ISDIR(p.lstat().st_mode), 'non-ordinary directory')
            require(p.relative_to(root).as_posix() in dirs, 'unexpected directory')
        for name in names:
            p = Path(base) / name
            require(stat.S_ISREG(p.lstat().st_mode), 'non-regular file')
            found.add(p.relative_to(root).as_posix())
    require(found == expected, 'publication file allowlist mismatch')
    buffers = {MANIFEST_NAME: data, ENTRYPOINT: regular_bytes(root / ENTRYPOINT)}
    require(buffers[ENTRYPOINT] == Path(__file__).read_bytes(), 'entrypoint copy mismatch')
    for name, pin in records.items():
        require(type(pin['bytes']) is int and pin['bytes'] >= 0, 'invalid byte count')
        b = regular_bytes(root / name)
        require(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'file pin mismatch: ' + name)
        buffers[name] = b
    return manifest, buffers

def verify_archives(root, manifest):
    summary = []
    for item in manifest['archives']:
        archive = root / 'releases' / item['archive']
        m = read_json((root / 'releases' / item['manifest']).read_bytes())
        require(archive.stat().st_size == m['archive_bytes'] and sha(archive.read_bytes()) == m['archive_sha256'], 'archive metadata mismatch')
        entries = m['files']
        names = [f['path'] for f in entries]
        require(len(names) == len(set(names)), 'duplicate manifest member')
        with zipfile.ZipFile(archive) as z:
            require(len(z.namelist()) == len(set(z.namelist())), 'duplicate ZIP member')
            require(set(z.namelist()) == set(names), 'archive member-set mismatch')
            for f in entries:
                pp = PurePosixPath(f['path'])
                require(not pp.is_absolute() and '..' not in pp.parts and '\\' not in f['path'], 'unsafe ZIP path')
                require(stat.S_ISREG(z.getinfo(f['path']).external_attr >> 16), 'non-regular ZIP member')
                b = z.read(f['path'])
                require(len(b) == f['bytes'] and sha(b) == f['sha256'], 'ZIP member hash mismatch')
                require(b == (root / item['directory'] / f['path']).read_bytes(), 'expanded member mismatch')
        summary.append({'label': item['directory'], 'archive_sha256': m['archive_sha256'], 'members': len(names)})
    return summary

def run(command, cwd):
    p = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=240)
    require(p.returncode == 0, 'replay command failed: ' + p.stdout + p.stderr)
    return p.stdout

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).absolute().parent)
    ap.add_argument('--integrity-only', action='store_true', help='Authenticate bytes only; do not execute replay drivers.')
    for name in ['catalog', 'problems', 'reports', 'pdf-directory', 'kt-pdf']:
        ap.add_argument('--' + name, type=Path)
    args = ap.parse_args()
    names = ['catalog', 'problems', 'reports', 'pdf_directory', 'kt_pdf']
    values = [getattr(args, x) for x in names]
    require(not any(values) or all(values), 'supply all five source-input arguments')
    if all(values):
        values = [p.absolute() for p in values]
    require(not (args.integrity_only and any(values)), 'source replay requires full mode')
    root = args.root.absolute()
    manifest, buffers = authenticate(root)
    result = {'result': 'PASS', 'problem_id': 2928, 'rank': 919, 'problem_number': 'KP-4.52',
              'disposition': 'unsolved', 'turns_used': 3, 'turn_limit': 5,
              'scope': 'finite byte integrity and selected metadata only; no theorem, novelty, or peer-review certification',
              'publication_manifest_sha256': MANIFEST_SHA256,
              'files_authenticated': len(buffers), 'source_input_replay': 'not_run_inputs_not_supplied'}
    with tempfile.TemporaryDirectory(prefix='stable normal publication α ') as tmp:
        work = Path(tmp)
        packet = work / 'authenticated packet'
        for name, b in buffers.items():
            p = packet / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b)
        result['archives'] = verify_archives(packet, manifest)
        if args.integrity_only:
            result['mode'] = 'integrity_only_no_replay'
        else:
            result['mode'] = 'full_replay'
            replay = work / 'patch replay'
            shutil.copytree(packet / 'original', replay)
            run(['patch', '-p1', '--batch', '--forward', '--fuzz=0', '-i', str(packet / 'audit/orientation_clarification.patch')], replay)
            files = sorted(p.name for p in (packet / 'corrected').iterdir())
            require(sorted(p.name for p in replay.iterdir()) == files, 'patch replay file set mismatch')
            require(all((replay / f).read_bytes() == (packet / 'corrected' / f).read_bytes() for f in files), 'patch replay byte mismatch')
            result['patch_replay_members'] = len(files)
            result['packet_checks'] = []
            result['exact_acceptance'] = []
            result['audit_replay'] = []
            outputs = []
            for flags in (['-B'], ['-O', '-B']):
                for label in ('original', 'corrected'):
                    command = [sys.executable, *flags, str(packet / label / 'verify_packet.py'), '--root', str(packet / label)]
                    result['packet_checks'].append({'flags': flags, 'label': label, 'result': read_json(run(command, work))})
                command = [sys.executable, *flags, str(packet / 'acceptance/verify_acceptance.py'), '--release-directory', str(packet / 'releases')]
                result['exact_acceptance'].append({'flags': flags, 'result': read_json(run(command, work))})
                output = work / ('replay-optimized.json' if '-O' in flags else 'replay-normal.json')
                command = [sys.executable, *flags, str(packet / 'audit/replay_audit.py'), '--release-directory', str(packet / 'releases'), '--output', str(output)]
                r = read_json(run(command, work))
                require(r == {'result': 'PASS', 'packets': 2, 'positive_runs': 4, 'tamper_rejections': 96, 'trust_probes': 8}, 'unexpected replay counts')
                result['audit_replay'].append({'flags': flags, 'result': r})
                outputs.append(output.read_bytes())
            require(outputs[0] == outputs[1], 'normal and optimized replay differ')
            require(outputs[0] == (packet / 'audit/replay_results.json').read_bytes(), 'replay differs from frozen evidence')
            require(outputs[1] == (packet / 'audit/replay_results_optimized.json').read_bytes(), 'optimized replay differs from frozen evidence')
            result['replay_outputs_match_frozen'] = True
            if all(values):
                result['source_input_replay'] = []
                for flags in (['-B'], ['-O', '-B']):
                    command = [sys.executable, *flags, str(packet / 'verify_source_inputs.py')]
                    for name, value in zip(names, values):
                        command.extend(['--' + name.replace('_', '-'), str(value)])
                    result['source_input_replay'].append({'flags': flags, 'result': read_json(run(command, work))})
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
