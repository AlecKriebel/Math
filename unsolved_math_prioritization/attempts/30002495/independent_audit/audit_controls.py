#!/usr/bin/env python3
"""Pinned, read-only audit of the input and optimization/mutation correction.

This is a finite software/control audit, never a proof of an asymptotic or RH.
All output is deterministic except Python's runtime version, which is metadata.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PIN = '6c41bb59af46e93ffdc169484847271bbec0a6fc178673d491cf8ec9e41244ea'


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(source, optimize=0):
    scope = {'__name__': 'audit_loaded_module'}
    exec(compile(source, '<audit-loaded>', 'exec', optimize=optimize), scope)
    return scope


def anchored_inventory(packet):
    packet = Path(packet)
    require(not (packet/'MANIFEST.json').is_symlink(), 'Symlinked manifest')
    raw = (packet/'MANIFEST.json').read_bytes()
    require(digest(raw) == PIN, 'Input manifest does not match the externally pinned digest')
    manifest = json.loads(raw)
    expected = {'MANIFEST.json'}
    for entry in manifest['files']:
        p = packet/entry['path']
        require(p.is_file() and not p.is_symlink(), 'Nonregular inventory member')
        data = p.read_bytes()
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'Input byte mismatch')
        expected.add(entry['path'])
    require({p.name for p in packet.iterdir()} == expected, 'Unexpected input inventory')
    return manifest


def run_file(file, flags=(), environment_optimize=None, args=()):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    if environment_optimize is not None:
        env['PYTHONOPTIMIZE'] = str(environment_optimize)
    return subprocess.run([sys.executable, *flags, str(file), *args], capture_output=True, env=env)


def reduced(source):
    # Mutation coverage uses reduced positive domains only for speed. Full,
    # unchanged-domain positive replays are separately required below.
    for old, new in [('maxn = 3000', 'maxn = 700'),
                     ('range(1, 301)', 'range(1, 3)'),
                     ('range(1, 25)', 'range(1, 3)'),
                     ('range(1, 701)', 'range(1, 8)'),
                     ('range(1, 101)', 'range(1, 3)')]:
        source = source.replace(old, new)
    return source


def semantic_mutations(source, hardened):
    tree = ast.parse(reduced(source))
    if hardened:
        nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == 'require']
    else:
        nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    sites = sorted(n.lineno for n in nodes)
    require(len(sites) == 16, 'Expected exactly 16 control-check sites')
    result = {}
    for optimization in (0, 1, 2):
        rejected = 0
        accepted = 0
        for site in sites:
            mutated = ast.parse(reduced(source))
            for n in ast.walk(mutated):
                if getattr(n, 'lineno', None) == site:
                    if hardened and isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'require':
                        n.args[0] = ast.Constant(False)
                    elif not hardened and isinstance(n, ast.Assert):
                        n.test = ast.Constant(False)
            ast.fix_missing_locations(mutated)
            scope = {'__name__': 'semantic_mutation'}
            exec(compile(mutated, '<semantic-mutation>', 'exec', optimize=optimization), scope)
            try:
                output = scope['main']()
            except AssertionError:
                rejected += 1
            else:
                require(output['status'] == 'PASS', 'Unexpected accepted mutation status')
                accepted += 1
        if hardened or optimization == 0:
            require(rejected == 16 and accepted == 0, 'A false mathematical check escaped')
        else:
            require(accepted == 16 and rejected == 0, 'Original optimization issue did not reproduce')
        result[str(optimization)] = {'false_sites_rejected': rejected, 'false_sites_accepted': accepted}
    return result


def integrity_mutations(packet, verifier_source):
    names = ['altered_bytes', 'missing_file', 'extra_file', 'wrong_byte_count',
             'wrong_hash', 'traversal_path', 'absolute_path', 'duplicate_entry',
             'symlinked_file', 'symlinked_manifest', 'nested_directory', 'fifo',
             'negative_bytes', 'boolean_bytes', 'bad_digest', 'wrong_schema',
             'manifest_self_entry', 'extra_entry_field', 'missing_manifest', 'malformed_json']
    results = {}
    with tempfile.TemporaryDirectory(prefix='nyman_audit_integrity_') as tmp:
        for optimization in (0, 1, 2):
            verify = load(verifier_source, optimization)['verify']
            passed = []
            for name in names:
                p = Path(tmp)/f'{optimization}_{name}'
                shutil.copytree(packet, p)
                mp = p/'MANIFEST.json'
                m = json.loads(mp.read_bytes())
                if name == 'altered_bytes':
                    with (p/'PROOFS.md').open('ab') as out:
                        out.write(b'\nAUDIT NEGATIVE CONTROL\n')
                elif name == 'missing_file': (p/'RESULT.json').unlink()
                elif name == 'extra_file': (p/'EXTRA.txt').write_text('test')
                elif name == 'wrong_byte_count': m['files'][0]['bytes'] += 1
                elif name == 'wrong_hash': m['files'][0]['sha256'] = '0'*64
                elif name == 'traversal_path': m['files'][0]['path'] = '../escape'
                elif name == 'absolute_path': m['files'][0]['path'] = '/escape'
                elif name == 'duplicate_entry': m['files'].append(dict(m['files'][0]))
                elif name == 'symlinked_file':
                    (p/'RESULT.json').unlink()
                    (p/'RESULT.json').symlink_to((packet/'RESULT.json').resolve())
                elif name == 'nested_directory': (p/'nested').mkdir()
                elif name == 'fifo': os.mkfifo(p/'pipe')
                elif name == 'negative_bytes': m['files'][0]['bytes'] = -1
                elif name == 'boolean_bytes': m['files'][0]['bytes'] = True
                elif name == 'bad_digest': m['files'][0]['sha256'] = 'not-a-digest'
                elif name == 'wrong_schema': m['schema'] = 'wrong'
                elif name == 'manifest_self_entry': m['files'][0]['path'] = 'MANIFEST.json'
                elif name == 'extra_entry_field': m['files'][0]['extra'] = 'test'
                mp.write_text(json.dumps(m, indent=2)+'\n')
                if name == 'symlinked_manifest':
                    mp.unlink()
                    mp.symlink_to((packet/'MANIFEST.json').resolve())
                elif name == 'missing_manifest': mp.unlink()
                elif name == 'malformed_json': mp.write_text('{')
                try:
                    verify(p)
                except (ValueError, OSError, TypeError, KeyError):
                    passed.append(name)
                else:
                    raise RuntimeError('Integrity mutation accepted: '+name)
            require(len(passed) == len(names), 'Incomplete integrity mutation coverage')
            results[str(optimization)] = passed
    return results


def pin_controls(packet, verifier_source):
    # Coordinated rehashing is outside an unanchored manifest's trust boundary.
    with tempfile.TemporaryDirectory(prefix='nyman_audit_pin_') as tmp:
        p = Path(tmp)/'packet'
        shutil.copytree(packet, p)
        data = (p/'PROOFS.md').read_bytes()+b'\nAUDIT COORDINATED MUTATION\n'
        (p/'PROOFS.md').write_bytes(data)
        mp = p/'MANIFEST.json'
        m = json.loads(mp.read_bytes())
        for e in m['files']:
            if e['path'] == 'PROOFS.md':
                e['bytes'], e['sha256'] = len(data), digest(data)
        mp.write_text(json.dumps(m, indent=2)+'\n')
        require(load(verifier_source)['verify'](p) == 10, 'Unexpected original trust behavior')
        try:
            anchored_inventory(p)
        except RuntimeError:
            return {'unanchored_coordinated_rehash': 'ACCEPTED_AS_EXPECTED',
                    'externally_pinned_coordinated_rehash': 'REJECTED'}
        raise RuntimeError('External pin failed')


def corrected_integration(packet, hardened):
    with tempfile.TemporaryDirectory(prefix='nyman_corrected_integration_') as tmp:
        p = Path(tmp)/'packet'
        shutil.copytree(packet, p)
        def install(source):
            (p/'check_controls.py').write_text(source)
            mp = p/'MANIFEST.json'
            m = json.loads(mp.read_bytes())
            for e in m['files']:
                if e['path'] == 'check_controls.py':
                    data = (p/e['path']).read_bytes()
                    e['bytes'], e['sha256'] = len(data), digest(data)
            mp.write_text(json.dumps(m, indent=2)+'\n')
        install(hardened)
        positive = run_file(p/'verify_packet.py', environment_optimize=2,
                            args=('--replay', '--selftest'))
        require(positive.returncode == 0, 'Corrected optimized verifier integration failed')
        report = json.loads(positive.stdout)
        require(report['control_replay'] == 'BYTE_IDENTICAL' and report['assertion_groups'] == 23767,
                'Corrected integration replay mismatch')
        require(len(report['rejected_integrity_mutations']) == 8, 'Original selftest not preserved')
        bad = hardened.replace('require(Q(1, 2)-Q(3, 2)*Q(1, 3) == 0,',
                               'require(Q(1, 2)-Q(3, 2)*Q(1, 3) == 1,')
        require(bad != hardened, 'Corrected negative-control site missing')
        install(bad)
        negative = run_file(p/'verify_packet.py', environment_optimize=2, args=('--replay',))
        require(negative.returncode != 0, 'Corrected optimized verifier accepted false arithmetic')
        return {'optimization': 'PYTHONOPTIMIZE=2',
                'positive_full_replay': 'BYTE_IDENTICAL_23767_GROUPS',
                'original_selftest_mutations_rejected': 8,
                'rehashed_false_arithmetic': 'REJECTED'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    args = parser.parse_args()
    packet = args.packet.resolve()
    original_manifest = anchored_inventory(packet)
    before = {p.name: digest(p.read_bytes()) for p in packet.iterdir()}
    original = (packet/'check_controls.py').read_text()
    verifier = (packet/'verify_packet.py').read_text()
    hardened_path = Path(__file__).resolve().parent/'check_controls_hardened.py'
    hardened = hardened_path.read_text()
    expected = (packet/'CONTROL_RESULTS.json').read_bytes()
    # Ensure the correction changes only assertion evaluation, not mathematics.
    transformed = []
    for line_number, line in enumerate(original.splitlines(), 1):
        stripped = line.lstrip()
        indent = line[:len(line)-len(stripped)]
        if stripped.startswith('assert '):
            transformed.append(indent+f'require({stripped[7:]}, "original check_controls.py:{line_number}")')
        else:
            transformed.append(line)
    expected_patch = '\n'.join(transformed)+'\n'
    expected_patch = expected_patch.replace('\n\ndef factor(n):',
        '\n\ndef require(condition, label):\n    """Keep mathematical checks active under -O, -OO and PYTHONOPTIMIZE."""\n    if not condition:\n        raise AssertionError(label)\n\n\ndef factor(n):')
    require(hardened == expected_patch, 'Correction exceeds the declared minimal changes')
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(hardened))),
            'Hardened checker still contains removable asserts')
    original_replay = run_file(packet/'check_controls.py')
    require(original_replay.returncode == 0 and original_replay.stdout == expected,
            'Original unoptimized full replay failed')
    modes = [('normal', (), None), ('-O', ('-O',), None), ('-OO', ('-OO',), None),
             ('PYTHONOPTIMIZE=1', (), 1), ('PYTHONOPTIMIZE=2', (), 2)]
    positive = {}
    for name, flags, envopt in modes:
        r = run_file(hardened_path, flags, envopt)
        require(r.returncode == 0 and r.stdout == expected, 'Hardened full replay mismatch: '+name)
        positive[name] = 'BYTE_IDENTICAL_23767_GROUPS'
    original_semantic = semantic_mutations(original, False)
    corrected_semantic = semantic_mutations(hardened, True)
    integrity = integrity_mutations(packet, verifier)
    trust = pin_controls(packet, verifier)
    integration = corrected_integration(packet, hardened)
    # Demonstrate the original replay weakness through its actual CLI, including
    # a coherently rehashed but false arithmetic control. Normal execution fails.
    with tempfile.TemporaryDirectory(prefix='nyman_audit_replay_') as tmp:
        p = Path(tmp)/'packet'
        shutil.copytree(packet, p)
        old = 'assert Q(1, 2)-Q(3, 2)*Q(1, 3) == 0'
        bad = original.replace(old, 'assert Q(1, 2)-Q(3, 2)*Q(1, 3) == 1')
        require(bad != original, 'Mutation site missing')
        (p/'check_controls.py').write_text(bad)
        manifest = json.loads((p/'MANIFEST.json').read_bytes())
        for e in manifest['files']:
            if e['path'] == 'check_controls.py':
                data = (p/e['path']).read_bytes()
                e['bytes'], e['sha256'] = len(data), digest(data)
        (p/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
        cli = {}
        for name, flags, envopt in modes:
            r = run_file(p/'verify_packet.py', flags, envopt, ('--replay',))
            expected_acceptance = envopt in (1, 2)
            require((r.returncode == 0) == expected_acceptance, 'Unexpected verifier optimization behavior')
            cli[name] = 'FALSE_CONTROL_ACCEPTED' if expected_acceptance else 'FALSE_CONTROL_REJECTED'
    after = {p.name: digest(p.read_bytes()) for p in packet.iterdir()}
    require(before == after, 'Original input changed during audit')
    result = {'schema': 'nyman-independent-audit-controls-v1', 'status': 'PASS',
              'python': sys.version.split()[0], 'input_manifest_sha256': PIN,
              'input_files': len(original_manifest['files']), 'originals_unchanged': True,
              'minimal_patch_verified': True, 'hardened_full_replays': positive,
              'original_semantic_mutations': original_semantic,
              'hardened_semantic_mutations': corrected_semantic,
              'semantic_mutation_domain': 'Reduced positive loop ranges; each of all 16 check sites is separately forced false. Full unchanged-domain positive replays are separate.',
              'integrity_mutations': integrity, 'manifest_trust_boundary': trust,
              'corrected_verifier_integration': integration,
              'rehashed_false_control_original_verifier_cli': cli,
              'limits': ['AI-assisted independent audit, not formal proof verification.',
                         'Finite controls do not settle infinite limits, RH, or the methodological equivalence.',
                         'Coordinated rehash tests deliberately leave the original external pin; pinned input checking rejects them.']}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
