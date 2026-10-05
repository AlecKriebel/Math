#!/usr/bin/env python3
"""Post-seal replays; all writes remain inside this review subtree."""
import gzip, json, pathlib, shutil, sys
from capture_readonly import capture

ROOT = pathlib.Path(__file__).resolve().parent
A = ROOT.parent
W = pathlib.Path('/Users/alec/Documents/Math')
S = A / 'snapshot' / 'unsolved_math_prioritization' / 'attempts' / '2303002'
PYTHON = sys.executable
HEAD = '4245f1af53840a07f43c05c928c4783bc6c3a467'
BASE = 'efd29c05204703acca9a0860812f54b94fae54b1'
PREFIX = 'unsolved_math_prioritization/attempts/2303002'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
sources = ROOT / 'private_inputs'
sources.mkdir(exist_ok=True)
for name in ['hayman_lingham_2018.pdf', 'carleson_1976.pdf']:
    (sources / name).write_bytes(gzip.decompress((ROOT / 'private_sources' / (name + '.gz')).read_bytes()))

commands = [
    ('author_replay', [PYTHON, str(S / 'verify_source_alignment.py')]),
    ('historical_verbatim', [PYTHON, str(S / 'final_review' / 'check_independent.py')]),
    ('portable_math_only', [PYTHON, str(S / 'final_review' / 'run_portable.py'), '--math-only']),
    ('portable_full_sources', [PYTHON, str(S / 'final_review' / 'run_portable.py'), '--sources', str(sources)]),
    ('git_branch', ['git', '-C', str(W), 'symbolic-ref', '--quiet', '--short', 'HEAD']),
    ('git_scoped_tree', ['git', '-C', str(W), 'ls-tree', '-rz', HEAD, '--', PREFIX, QUEUE]),
    ('git_scoped_diff', ['git', '-C', str(W), 'diff', '--no-ext-diff', '--no-textconv', BASE, HEAD, '--', PREFIX, QUEUE]),
    ('git_target_history', ['git', '-C', str(W), 'log', '--format=fuller', '--name-status', HEAD, '--', PREFIX]),
    ('git_target_all_local_history', ['git', '-C', str(W), 'log', '--all', '--format=fuller', '--name-status', '--', PREFIX]),
    ('git_base_queue', ['git', '-C', str(W), 'show', BASE + ':' + QUEUE]),
]
results = []
for label, argv in commands:
    r = capture(label, argv)
    results.append({'label': label, 'exit_code': r['exit_code'], 'stdout': r['stdout'], 'stderr': r['stderr']})
    print(label + ': exit=' + str(r['exit_code']))

private = ROOT / 'private_mutations'
private.mkdir(exist_ok=True)
author = (S / 'verify_source_alignment.py').read_text()
for label, old, new in [
    ('mutation_radial_sign', 'a=2-n;check(a*(a+n-2)==0)', 'a=2+n;check(a*(a+n-2)==0)'),
    ('mutation_compact_cutoff', 'cutoff=max(1,compact_upper_bound+1)', 'cutoff=max(1,compact_upper_bound-1)'),
]:
    assert author.count(old) == 1
    target = private / (label + '.py')
    target.write_text(author.replace(old, new))
    print(label + ': exit=' + str(capture(label, [PYTHON, str(target)])['exit_code']))

copy = private / 'tampered_packet'
shutil.copytree(S, copy, dirs_exist_ok=True)
(copy / 'SOURCE_PROOF.md').write_bytes((copy / 'SOURCE_PROOF.md').read_bytes() + b'\nChanged proof bytes for negative control.\n')
print('mutation_proof_binding: exit=' + str(capture('mutation_proof_binding', [PYTHON, str(copy / 'final_review' / 'run_portable.py'), '--math-only'])['exit_code']))
bad_sources = private / 'tampered_sources'
bad_sources.mkdir(exist_ok=True)
# Avoid copying both full PDFs. The first source's hash must fail before the second is read.
(bad_sources / 'hayman_lingham_2018.pdf').write_bytes(b'Intentionally invalid PDF source bytes.\n')
print('mutation_source_binding: exit=' + str(capture('mutation_source_binding', [PYTHON, str(S / 'final_review' / 'run_portable.py'), '--sources', str(bad_sources)])['exit_code']))
