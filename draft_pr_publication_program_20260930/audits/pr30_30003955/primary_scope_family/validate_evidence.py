#!/usr/bin/env python3
"""Reproduce original-stage identity, legacy replay and adversarial scope controls.

Reads original Git/snapshot bytes; all checker writes are confined to ignored
family tmp copies. This is validation, never proof search or a queue mutation.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

FAMILY = Path(__file__).resolve().parent
AUDIT = FAMILY.parent
SOURCE = AUDIT / 'source_snapshot'
MANIFEST = json.loads((AUDIT / 'snapshot_manifest.json').read_text())
REPO = FAMILY.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def checker(copy, script, output):
    result = subprocess.run(['python3', str(copy / script)], capture_output=True,
                            text=True, timeout=60, check=True)
    data = json.loads((copy / output).read_text())
    assert result.stderr == ''
    return data, (copy / output).read_bytes()


identities = []
for item in MANIFEST['files']:
    original = (SOURCE / item['path']).read_bytes()
    target = 'unsolved_math_prioritization/attempts/30003955/' + item['path']
    blob = subprocess.check_output(['git', 'show', MANIFEST['head'] + ':' + target], cwd=REPO)
    oid = subprocess.check_output(['git', 'rev-parse', MANIFEST['head'] + ':' + target], cwd=REPO).decode().strip()
    assert original == blob
    assert sha(original) == item['sha256'] and len(original) == item['bytes']
    assert oid == item['git_blob_sha1']
    identities.append(item['path'])
assert len(identities) == 15
assert (SOURCE / 'PARTIAL.md').read_bytes() == (SOURCE / 'review/reviewed_partial.md').read_bytes()
changed = subprocess.check_output(['git', 'diff', '--name-only', MANIFEST['base'], MANIFEST['head']], cwd=REPO).decode().splitlines()
assert changed == MANIFEST['changed_paths'] and len(changed) == 16
assert 'unsolved_math_prioritization/QUEUE.md' in changed

scripts = [('check_monodromy.py', 'check_results.json', 31),
           ('review/independent_checks.py', 'review/independent_results.json', 53830)]
replay = FAMILY / 'tmp' / 'repro_originals'
shutil.copytree(SOURCE, replay, dirs_exist_ok=True)
for script, output, count in scripts:
    result, raw = checker(replay, script, output)
    assert result['assertions'] == count
    assert raw == (SOURCE / output).read_bytes()

mutation_results = []
for name, text in [('deleted_proof', 'No proof supplied.\n'),
                   ('invented_solution', 'Theorem: all covers admit such H. Proof: Assume such H exists. Thus done.\n')]:
    copy = FAMILY / 'tmp' / ('repro_' + name)
    shutil.copytree(SOURCE, copy, dirs_exist_ok=True)
    (copy / 'PARTIAL.md').write_text(text)
    (copy / 'review/reviewed_partial.md').write_text(text)
    for script, output, count in scripts:
        result, _ = checker(copy, script, output)
        assert result['assertions'] == count
        assert result.get('all_assertions_passed', result.get('all_passed')) is True
        assert result.get('partial_note_sha256', result.get('reviewed_sha256')) == sha(text.encode())
        mutation_results.append({'mutation': name, 'checker': script, 'assertions': count})

# Essential simple classes of pants are peripheral. This obstruction distinguishes
# the killed inverse word from the simple third boundary with coherent orientations.
peripheral = {(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)}
assert (1, -1) not in peripheral
assert (1 - 1) % 3 == 0 and (1 + 1) % 3 == 2

# Independent component control from explicit cosets rather than legacy orbit BFS.
from itertools import permutations
G = set(permutations(range(3)))
r = (1, 2, 0)
t = (1, 0, 2)
identity = (0, 1, 2)


def compose(a, b):
    return tuple(a[b[i]] for i in range(3))


def inverse(a):
    return tuple(a.index(i) for i in range(3))


def comm(a, b):
    return compose(compose(compose(a, b), inverse(a)), inverse(b))


assert compose(comm(r, t), comm(inverse(r), t)) == identity
A3 = {identity, r, compose(r, r)}
assert compose(compose(t, inverse(r)), inverse(t)) in A3
regular_cosets = {frozenset(compose(a, g) for a in A3) for g in G}
assert len(regular_cosets) == 2 and {len(c) for c in regular_cosets} == {3}
assert {a[0] for a in A3} == {0, 1, 2}
assert 1 + 6 * (2 - 1) == 7 and 1 + 3 * (2 - 1) == 4

out = {'frozen15_verified': True, 'exact_diff_paths': len(changed),
       'legacy_results_byte_identical': True, 'deleted_and_invented_proofs_still_pass': mutation_results,
       'coherent_pants_inverse_word_control': True, 'independent_s3_coset_control': True,
       'all_original_bytes_preserved': True,
       'meaning': 'Checks identities and specified controls; cannot certify deleted/circular proof or the full universal target.'}
(FAMILY / 'validation_results.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
