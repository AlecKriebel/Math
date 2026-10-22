#!/usr/bin/env python3
"""Source-free independent replay and hostile frozen-packet controls."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'public'

def snapshot(path):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in path.iterdir()}

def rebind(path):
    manifest = json.loads((path/'MANIFEST.json').read_text())
    for item in manifest['files']:
        data = (path/item['name']).read_bytes()
        item['bytes'] = len(data)
        item['sha256'] = hashlib.sha256(data).hexdigest()
    (path/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')

def claim(path, key, value):
    c = json.loads((path/'CLAIMS.json').read_text())
    c[key] = value
    (path/'CLAIMS.json').write_text(json.dumps(c, indent=2)+'\n')
    rebind(path)

def manifest_edit(path, fn):
    m = json.loads((path/'MANIFEST.json').read_text())
    fn(m)
    (path/'MANIFEST.json').write_text(json.dumps(m)+'\n')

def replace(path, name, data, rebinding=False):
    (path/name).write_bytes(data)
    if rebinding:
        rebind(path)

def symlink(path):
    (path/'PROOF.md').unlink()
    (path/'PROOF.md').symlink_to(BASE/'PROOF.md')

def directory_member(path):
    (path/'PROOF.md').unlink()
    (path/'PROOF.md').mkdir()

def rebound_proof(path):
    proof = (path/'PROOF.md').read_text()
    proof = proof.replace('For every g>=2', 'For every g>=3', 1)
    (path/'PROOF.md').write_text(proof)
    rebind(path)

MUTATIONS = [
 ('target-genus-expansion', lambda p: claim(p, 'target_solved_genera', [2, 3])),
 ('general-solution-claim', lambda p: claim(p, 'general_target_solved', True)),
 ('wrong-target-degree', lambda p: claim(p, 'target_degree', [4, -5])),
 ('wrong-proved-degree', lambda p: claim(p, 'proved_degree', [2, -1])),
 ('wrong-coefficient', lambda p: claim(p, 'coefficient', 'H^(2g-2)(C_g;Z)')),
 ('wrong-subgroup-quantifier', lambda p: claim(p, 'subgroup', 'some congruence subgroup')),
 ('genus-one-expansion', lambda p: claim(p, 'genus_min', 1)),
 ('boolean-integer-confusion', lambda p: claim(p, 'genus_min', True)),
 ('wrong-status', lambda p: claim(p, 'status', 'solved')),
 ('wrong-approach-count', lambda p: claim(p, 'approaches', 4)),
 ('false-human-acceptance', lambda p: claim(p, 'independent_review', 'human accepted')),
 ('formal-proof-overclaim', lambda p: claim(p, 'formal_verification', True)),
 ('novelty-overclaim', lambda p: claim(p, 'novelty_claim', True)),
 ('dependency-change', lambda p: claim(p, 'avramidi_dependency_in_main_theorem', True)),
 ('extra-claim', lambda p: claim(p, 'extra', True)),
 ('invalid-json-rebound', lambda p: replace(p, 'CLAIMS.json', b'{', True)),
 ('duplicate-json-rebound', lambda p: replace(p, 'CLAIMS.json', b'{"a":1,"a":2}', True)),
 ('null-json-rebound', lambda p: replace(p, 'CLAIMS.json', b'null', True)),
 ('nonfinite-json-rebound', lambda p: replace(p, 'CLAIMS.json', b'{"x":NaN}', True)),
 ('invalid-utf8-rebound', lambda p: replace(p, 'CLAIMS.json', b'\xff', True)),
 ('missing-proof', lambda p: (p/'PROOF.md').unlink()),
 ('missing-manifest', lambda p: (p/'MANIFEST.json').unlink()),
 ('extra-document', lambda p: (p/'source.pdf').write_bytes(b'%PDF fake')),
 ('extra-directory', lambda p: (p/'nested').mkdir()),
 ('symlink-member', symlink),
 ('directory-member', directory_member),
 ('manifest-path-traversal', lambda p: manifest_edit(p, lambda m: m['files'][0].update(name='../PROOF.md'))),
 ('manifest-absolute-path', lambda p: manifest_edit(p, lambda m: m['files'][0].update(name='/tmp/PROOF.md'))),
 ('manifest-duplicate-path', lambda p: manifest_edit(p, lambda m: m['files'][0].update(name=m['files'][1]['name']))),
 ('manifest-bool-version', lambda p: manifest_edit(p, lambda m: m.update(schema=True))),
 ('manifest-byte-bool', lambda p: manifest_edit(p, lambda m: m['files'][0].update(bytes=True))),
 ('manifest-negative-bytes', lambda p: manifest_edit(p, lambda m: m['files'][0].update(bytes=-1))),
 ('manifest-bad-digest', lambda p: manifest_edit(p, lambda m: m['files'][0].update(sha256='0'*64))),
 ('manifest-nonfinite', lambda p: replace(p, 'MANIFEST.json', b'{"schema":NaN,"files":[]}')),
 ('manifest-invalid-json', lambda p: replace(p, 'MANIFEST.json', b'{')),
 ('manifest-null', lambda p: replace(p, 'MANIFEST.json', b'null')),
 ('proof-rebound-to-self-manifest', rebound_proof),
 ('provenance-rebound', lambda p: replace(p, 'PROVENANCE.json', b'{}', True)),
 ('author-verifier-rebound', lambda p: replace(p, 'verify.py', b'print("PASS")\n', True)),
 ('readme-rebound', lambda p: replace(p, 'README.md', b'Everything is solved.\n', True)),
]

def run(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True)

def main():
    before_original = snapshot(BASE)
    reports = []
    outputs = []
    author_outputs = []
    for mode in [[], ['-O'], ['-OO']]:
        with tempfile.TemporaryDirectory(prefix='independent-mapping-audit-') as temp:
            temp = Path(temp)
            verifier = temp/'independent_verify.py'
            shutil.copyfile(HERE/'independent_verify.py', verifier)
            verifier.chmod(0o444)
            packet = temp/'read-only-author'
            shutil.copytree(BASE, packet)
            before = snapshot(packet)
            for file in packet.iterdir():
                file.chmod(0o444)
            packet.chmod(0o555)
            probe = run([sys.executable, '-B', '-c',
                         'from pathlib import Path; Path('+repr(str(packet/'probe'))+').write_text("bad")'], temp)
            if probe.returncode == 0:
                raise RuntimeError('read-only permission probe unexpectedly succeeded')
            command = [sys.executable, *mode, '-B', str(verifier), str(packet)]
            good = run(command, temp)
            if good.returncode:
                raise RuntimeError(good.stderr)
            original = run([sys.executable, *mode, '-B', str(packet/'verify.py')], temp)
            if original.returncode:
                raise RuntimeError(original.stderr)
            if snapshot(packet) != before:
                raise RuntimeError('read-only packet changed')
            outputs.append(good.stdout)
            author_outputs.append(original.stdout)
            packet.chmod(0o755)
            for file in packet.iterdir():
                file.chmod(0o644)
            negatives = []
            for label, mutation in MUTATIONS:
                target = temp/label
                shutil.copytree(BASE, target)
                mutation(target)
                bad = run([sys.executable, *mode, '-B', str(verifier), str(target)], temp)
                if bad.returncode == 0:
                    raise RuntimeError('hostile mutation accepted: '+label)
                negatives.append({'case': label, 'returncode': bad.returncode,
                                  'reason': bad.stderr.strip()})
            reports.append({'mode': ' '.join(mode) or 'normal',
                            'independent_output': json.loads(good.stdout),
                            'author_output': json.loads(original.stdout),
                            'read_only_write_probe_rejected': True,
                            'unchanged_snapshot': True,
                            'rejected_controls': negatives})
    if len(set(outputs)) != 1 or len(set(author_outputs)) != 1:
        raise RuntimeError('optimized outputs differ')
    # Replay the author's own complete mutation harness as an additional check,
    # separate from the 120 independently designed hostile executions above.
    own_tests = run([sys.executable, '-B', str(BASE/'test_verifier.py')], HERE)
    if own_tests.returncode:
        raise RuntimeError(own_tests.stderr)
    if before_original != snapshot(BASE):
        raise RuntimeError('original freeze changed')
    print(json.dumps({'status': 'PASS', 'independent_negative_controls_per_mode': len(MUTATIONS),
                      'mode_count': 3, 'identical_optimized_outputs': True,
                      'original_freeze_unchanged': True,
                      'author_harness': json.loads(own_tests.stdout),
                      'modes': reports}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
