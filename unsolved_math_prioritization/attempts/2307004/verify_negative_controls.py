#!/usr/bin/env python3
"""Relocation, optimization, integrity, and scope negative controls."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rebind(packet, changed):
    manifest = packet / 'PUBLICATION_MANIFEST.json'
    value = json.loads(manifest.read_text())
    for row in value['files']:
        if row['path'] == changed:
            data = (packet / changed).read_bytes()
            row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    manifest.write_text(json.dumps(value, indent=2) + '\n')


def main():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    scope_cases = {
        'false-solution': ('full_problem_solved', True),
        'false-optimality': ('finite_certificate_is_optimal', True),
        'false-uniform-gap': ('strict_half_proof_supplies_uniform_positive_gap', True),
        'false-limsup-identification': ('inf_all_n_identified_with_limsup', True),
        'false-proposal-theorem': ('recent_2026_proposal_adopted_as_theorem', True),
        'false-source-verification': ('source_corpora_freshly_verified', True),
        'wrong-queue-status': ('queue_status', 'exhausted'),
        'wrong-turns': ('turns', '0/5'),
    }
    cases = ['content', 'missing', 'extra', 'extra-directory', 'symlink', 'duplicate-path',
             'unsafe-path', 'duplicate-json-key', 'author-freeze-identity',
             'audit-freeze-identity', *scope_cases]
    mutants = []
    with tempfile.TemporaryDirectory(prefix='power-sum-negative-') as temp:
        base = Path(temp)
        pristine = base / 'relocated packet with spaces'
        shutil.copytree(ROOT, pristine)
        positive = []
        for flags, optimize in (([], None), (['-O'], None), ([], '1')):
            use_env = env.copy()
            if optimize:
                use_env['PYTHONOPTIMIZE'] = optimize
            run = subprocess.run([sys.executable, '-B', *flags, str(pristine / 'verify_publication.py')],
                                 cwd=base, env=use_env, capture_output=True, check=True)
            positive.append(run.stdout)
        need(positive[0] == positive[1] == positive[2], 'relocated optimization disagreement')
        for optimized in (False, True):
            for kind in cases:
                packet = base / ('mutant-' + str(optimized) + '-' + kind)
                shutil.copytree(pristine, packet)
                manifest = packet / 'PUBLICATION_MANIFEST.json'
                value = json.loads(manifest.read_text())
                if kind == 'content':
                    (packet / 'README.md').write_bytes(b'altered\n')
                elif kind == 'missing':
                    (packet / 'README.md').unlink()
                elif kind == 'extra':
                    (packet / 'unexpected.txt').write_text('extra\n')
                elif kind == 'extra-directory':
                    (packet / 'unexpected-empty-directory').mkdir()
                elif kind == 'symlink':
                    (packet / 'README.md').unlink()
                    (packet / 'README.md').symlink_to(pristine / 'README.md')
                elif kind == 'duplicate-path':
                    value['files'].append(value['files'][0])
                    manifest.write_text(json.dumps(value))
                elif kind == 'unsafe-path':
                    value['files'][0]['path'] = '../outside.txt'
                    manifest.write_text(json.dumps(value))
                elif kind == 'duplicate-json-key':
                    manifest.write_text('{"problem_id":"bad",' + manifest.read_text()[1:])
                elif kind in ('author-freeze-identity', 'audit-freeze-identity'):
                    changed = ('safe_output/FREEZE_MANIFEST.json' if kind.startswith('author')
                               else 'independent_audit/AUDIT_BINDING.json')
                    p = packet / changed
                    p.write_bytes(p.read_bytes() + b' ')
                    rebind(packet, changed)
                else:
                    changed = 'PUBLICATION_SCOPE.json'
                    p = packet / changed
                    scope = json.loads(p.read_text())
                    key, item = scope_cases[kind]
                    scope[key] = item
                    p.write_text(json.dumps(scope))
                    rebind(packet, changed)
                run = subprocess.run([sys.executable, '-B', *(['-O'] if optimized else []),
                                      str(packet / 'verify_publication.py')], cwd=base,
                                     env=env, capture_output=True, text=True)
                need(run.returncode != 0 and 'ValueError:' in run.stderr,
                     'mutant not rejected: ' + kind)
                mutants.append({'kind': kind, 'optimized': optimized, 'rejected': True,
                                'diagnostic': run.stderr.strip().splitlines()[-1]})
    print(json.dumps({'result': 'PASS', 'relocated_normal_optimized_and_environment':
                      json.loads(positive[0]), 'rejected_mutants': len(mutants), 'mutants': mutants},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
