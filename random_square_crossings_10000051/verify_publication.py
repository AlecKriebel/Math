"""Read-only, fail-closed publication replay. Supply an externally trusted pin.
python3 verify_publication.py --manifest-sha256 HASH
The pin must come from the PR acceptance record, not this directory's manifest.
Validation uses explicit exceptions and remains active under -O and -OO.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

ORIGINAL_PIN = 'd7e9b428572aa3864071d8e9bba50732afa6606586a4f1aa5250ada59ea24736'
AUDIT_PIN = '4c4bb2148bd8dabaabccc741351b24c08cd48f372bc8dc14ced7c7b3d8f7cff8'
CORRECTED_PIN = '57cda6d9529eb69521cab8e4e71aae5cfb5908d4ceb7dfd3c02f793b500c9cd8'
CANDIDATE_PIN = '01b2e76ed4e7b3b2e41b4d1467d2a56207839904ab541c356271e891da140254'


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, 'duplicate JSON key: '+key)
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique)


def inventory(root):
    need(root.is_dir() and not root.is_symlink(), 'invalid packet directory')
    files = set()
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'symlink prohibited: '+str(p.relative_to(root)))
        need(p.is_file() or p.is_dir(), 'non-regular entry')
        if p.is_file():
            files.add(p.relative_to(root).as_posix())
    return files


def verify_manifest(root, name, pin):
    need(re.fullmatch('[0-9a-f]{64}', pin) is not None, 'invalid external hash')
    actual = inventory(root)
    data = (root/name).read_bytes()
    need(sha(data) == pin, 'manifest pin mismatch: '+name)
    manifest = parse_json(data)
    need(manifest['problem_id'] == 10000051, 'wrong problem')
    entries = manifest['files']
    need(isinstance(entries, list) and len(entries) > 0, 'empty inventory')
    paths = set()
    for entry in entries:
        path = entry['path']
        pp = PurePosixPath(path)
        need(isinstance(path, str) and not pp.is_absolute() and '..' not in pp.parts
             and pp.as_posix() == path and path not in ('', '.') and '\\' not in path,
             'unsafe path')
        need(path != name and path not in paths, 'duplicate/self manifest entry')
        paths.add(path)
        need(type(entry['bytes']) is int and entry['bytes'] >= 0, 'bad size')
        need(re.fullmatch('[0-9a-f]{64}', entry['sha256']) is not None, 'bad hash')
        b = (root/path).read_bytes()
        need(len(b) == entry['bytes'] and sha(b) == entry['sha256'], 'file mismatch: '+path)
    need(actual == paths | {name}, 'extra or missing files')
    expected_dirs = {parent.as_posix() for path in paths | {name}
                     for parent in PurePosixPath(path).parents if parent.as_posix() != '.'}
    actual_dirs = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
    need(actual_dirs == expected_dirs, 'extra or missing directories')
    return manifest


def run(script, args=(), flags=(), cwd=None):
    # -I ignores PYTHONOPTIMIZE and all other PYTHON* environment variables.
    # No wrapper optimization flag is inherited. Assert-based scripts run normally.
    return subprocess.run([sys.executable, '-I', '-B', *flags, str(script), *map(str, args)],
                          cwd=cwd, capture_output=True, text=True, timeout=180)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.packet.absolute()
    need(root.is_dir() and not root.is_symlink(), 'invalid packet root')
    manifest = verify_manifest(root, 'PUBLIC_MANIFEST.json', args.manifest_sha256)
    need(manifest['status'] == 'PARTIAL_NOT_SOLVED' and manifest['mathematical_turns'] == 5,
         'publication scope mismatch')
    verify_manifest(root/'original', 'FROZEN_MANIFEST.json', ORIGINAL_PIN)
    verify_manifest(root/'audit', 'AUDIT_MANIFEST.json', AUDIT_PIN)
    corrected = verify_manifest(root/'corrected', 'CORRECTED_MANIFEST.json', CORRECTED_PIN)
    need(sha((root/'corrected/CANDIDATE.md').read_bytes()) == CANDIDATE_PIN,
         'corrected candidate pin mismatch')
    need((root/'corrected/CANDIDATE.md').read_bytes() ==
         (root/'audit/CANDIDATE_CORRECTED.md').read_bytes(), 'audit candidate mismatch')
    status = parse_json((root/'STATUS.json').read_bytes())
    need(status['status'] == 'unsolved' and status['turns'] == '5/5'
         and status['fair_color_lower_bound_proved'] is False
         and status['fair_color_small_mesh_limit_proved'] is False, 'incorrect status')
    before = {p: sha((root/p).read_bytes()) for p in inventory(root)}
    audit_results = []
    for flags in [(), ('-O',), ('-OO',)]:
        r = run(root/'audit/checks/independent_audit.py', [root/'original'], flags)
        need(r.returncode == 0, 'independent audit failed: '+r.stderr)
        need(r.stdout.encode() == (root/'audit/checks/independent_results.json').read_bytes(),
             'independent audit output changed')
        audit_results.append(json.loads(r.stdout)['status'])
    with tempfile.TemporaryDirectory(prefix='square-crossing-replay-') as td:
        temp = Path(td)
        patch_root = temp/'patched'
        shutil.copytree(root/'original', patch_root)
        r = subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i',
                            str(root/'audit/CORRECTION.patch')], cwd=patch_root,
                           capture_output=True, text=True, timeout=30)
        need(r.returncode == 0, 'correction patch failed: '+r.stdout+r.stderr)
        for entry in corrected['files']:
            need((patch_root/entry['path']).read_bytes() ==
                 (root/'corrected'/entry['path']).read_bytes(), 'patch replay differs')
        expected_changed = {'CANDIDATE.md', 'checks/exact_crossings.py', 'checks/verify_rational.py'}
        actual_changed = {p for p in inventory(root/'original')
                          if (root/'original'/p).read_bytes() != (patch_root/p).read_bytes()}
        need(actual_changed == expected_changed, 'patch changed unexpected files')
        script_results = []
        for name in ['original', 'corrected']:
            work = temp/name
            shutil.copytree(root/name, work)
            frozen = {p: (work/p).read_bytes() for p in inventory(work)}
            for script in ['exact_crossings.py', 'verify_rational.py']:
                r = run(work/'checks'/script)
                need(r.returncode == 0, name+' ordinary replay failed: '+r.stderr)
                result = script.replace('.py', '_results.json')
                if script == 'verify_rational.py':
                    result = 'rational_results.json'
                need(r.stdout.encode() == frozen['checks/'+result], 'script output differs')
                script_results.append(name+'/'+script)
            need(all((work/p).read_bytes() == b for p, b in frozen.items()),
                 'script replay altered frozen bytes')
        guards = []
        for script in ['exact_crossings.py', 'verify_rational.py']:
            for flags in [('-O',), ('-OO',)]:
                r = run(temp/'corrected/checks'/script, flags=flags)
                need(r.returncode != 0 and 'Verification requires assertions' in r.stderr,
                     'corrected optimization guard failed')
                guards.append(script+':'+flags[0])
    need(before == {p: sha((root/p).read_bytes()) for p in inventory(root)},
         'verification mutated packet')
    print(json.dumps({'status': 'PASS', 'claim_status': 'PARTIAL_NOT_SOLVED',
                      'original_audit_corrected_pins_verified': True,
                      'external_public_manifest_pin_verified': True,
                      'patch_reconstructed_exactly': True,
                      'independent_modes': audit_results,
                      'ordinary_script_replays': script_results,
                      'optimized_direct_runs_rejected': guards,
                      'source_packet_unchanged': True}, indent=2))


if __name__ == '__main__':
    main()
