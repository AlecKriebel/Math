#!/usr/bin/env python3
"""Verify the exact safe packet, replay finite controls, reject altered copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True

PAYLOAD = {
    'README.md', 'STATUS.json', 'verify_packet.py',
    'author/PROOF.md', 'author/README.md', 'author/RESEARCH_LOG.md',
    'author/RESULT.json', 'author/SOURCES.md', 'author/SHA256SUMS',
    'author/verify_bridge.py', 'author/control_results.json',
    'audit-independent/AUDIT.md', 'audit-independent/AUDIT_MANIFEST.json',
    'audit-independent/SHA256SUMS', 'audit-independent/independent_checks.py',
    'audit-independent/independent_results.json',
    'audit-independent/replay_frozen.py', 'audit-independent/replay_results.json',
}
EXPECTED = PAYLOAD | {'MANIFEST.json', 'SHA256SUMS'}
ANCHORS = {
    'author/SHA256SUMS': 'ff5e02d9d7dc9d20ee690b6b523de26e2bbb54cd852680d9c310bac7963b635b',
    'audit-independent/SHA256SUMS': '19ab628ca66cbe3e46f89b539e066e1c34ddad4ac972b3fc0b780ec2303bfc23',
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def listed(path):
    records = {}
    for line in path.read_text().splitlines():
        value, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        assert name not in records, ('duplicate manifest name', name)
        assert len(value) == 64 and all(c in '0123456789abcdef' for c in value)
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        records[name] = value
    return records


def integrity(root):
    found = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert found == EXPECTED, ('inventory mismatch', sorted(found ^ EXPECTED))
    assert not any(p.is_symlink() for p in root.rglob('*')), 'symlinks forbidden'
    sums = listed(root/'SHA256SUMS')
    assert set(sums) == EXPECTED - {'SHA256SUMS'}
    for name, value in sums.items():
        assert digest(root/name) == value, ('hash mismatch', name)
    manifest = json.loads((root/'MANIFEST.json').read_text())
    assert set(manifest['files']) == PAYLOAD
    for name, record in manifest['files'].items():
        assert digest(root/name) == record['sha256'] == sums[name]
        assert (root/name).stat().st_size == record['bytes']
    for name, expected in ANCHORS.items():
        assert digest(root/name) == expected, ('frozen manifest altered', name)
        for child, value in listed(root/name).items():
            assert digest((root/name).parent/child) == value
    return len(found)


def run_command(root, script):
    output = subprocess.check_output([sys.executable, '-B', str(root/script)], cwd=root, text=True)
    return json.loads(output)


def verify(root):
    count = integrity(root)
    original = run_command(root, 'author/verify_bridge.py')
    assert original == json.loads((root/'author/control_results.json').read_text())
    assert original['function_coalition_pairs'] == 1050698
    independent = run_command(root, 'audit-independent/independent_checks.py')
    assert independent == json.loads((root/'audit-independent/independent_results.json').read_text())
    assert independent['all_boolean_function_coalition_pairs'] == 1050698
    assert independent['all_support_inclusion_coalition_pairs_dimensions_0_through_3'] == 52833
    assert independent['exact_random_clause_joint_probability_cases'] == 112
    replay = run_command(root, 'audit-independent/replay_frozen.py')
    assert replay['status'] == 'passed' and replay['exact_json_match']
    assert integrity(root) == count
    rejected = []
    for mutant in ['changed_proof', 'changed_audit', 'missing_output', 'unexpected_file']:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp)/'packet'
            shutil.copytree(root, copy)
            if mutant == 'changed_proof':
                with (copy/'author/PROOF.md').open('a') as f: f.write('\ncorruption\n')
            elif mutant == 'changed_audit':
                with (copy/'audit-independent/AUDIT.md').open('a') as f: f.write('\ncorruption\n')
            elif mutant == 'missing_output':
                (copy/'author/control_results.json').unlink()
            else:
                (copy/'unexpected.txt').write_text('not in the safe inventory\n')
            try:
                integrity(copy)
            except AssertionError:
                rejected.append(mutant)
            else:
                raise AssertionError(('corruption not rejected', mutant))
    assert integrity(root) == count
    return {
        'result': 'PASS', 'packet_files': count,
        'original_function_coalition_pairs': 1050698,
        'independent_function_coalition_pairs': 1050698,
        'support_inclusion_pairs': 52833, 'clause_probability_cases': 112,
        'frozen_author_and_audit_preserved': True,
        'control_outputs_byte_identical': True,
        'mutants_rejected': rejected,
        'limitations': 'Integrity and finite arithmetic checks do not replace the written asymptotic proof or human mathematical review.',
    }

if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent), indent=2, sort_keys=True))
