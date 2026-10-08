#!/usr/bin/env python3
"""Semantic mutation harness. Mutates temporary copies, never the input packet."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def need(ok, text):
    if not ok:
        raise RuntimeError(text)


def main():
    need(len(sys.argv) == 2, 'provide frozen verifier path')
    original = Path(sys.argv[1]).resolve()
    payload = original.read_bytes()
    source = payload.decode()
    independent = Path(__file__).with_name('independent_checks.py').resolve()
    mutations = [
        ('taxicab_metric', 'return F(rn, rd)',
         'return sum(abs(a-b) for a,b in zip(p,q))', False),
        ('skip_intermediate_vertices', 'for i, j in zip(indices, indices[1:]):',
         'for i, j in itertools.combinations(indices, 2):', False),
        ('hop_weights_for_euclidean', 'candidate = d + (1 if hop else w)',
         'candidate = d + 1', False),
        ('directed_edges', 'self.adj[i][j] = self.adj[j][i] = w',
         'self.adj[i][j] = w', False),
        ('obsolete_hop_witness', 'hop_corner = a.index(F(79, 7), F(209, 21))',
         'hop_corner = a.index(F(5, 7), F(-20, 21))', False),
        ('overstrong_edge_bound', 'require(len(path) - 1 <= bound,',
         'require(len(path) - 1 <= bound - 1,', False),
        ('disable_edge_bound', 'require(len(path) - 1 <= bound,',
         'require(True,', True),
        ('disable_connected_intersection',
         'require(not hits or hits == list(range(hits[0], hits[-1] + 1)),',
         'require(True,', True),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix='line-arrangement-mutations-') as name:
        temporary = Path(name)
        for label, old, new, original_survives in mutations:
            need(source.count(old) == 1, 'mutation anchor not unique: ' + label)
            mutant = temporary / (label + '.py')
            mutated = source.replace(old, new)
            mutant.write_text(mutated)
            modes = []
            for mode in ([], ['-O'], ['-OO']):
                def run(arguments):
                    completed = subprocess.run([sys.executable, '-I', '-B'] + mode + arguments,
                                               capture_output=True, text=True, timeout=20)
                    return {'exit_code': completed.returncode,
                            'last_error_line': completed.stderr.strip().splitlines()[-1]
                            if completed.stderr.strip() else None}
                original_result = run([str(mutant)])
                need((original_result['exit_code'] == 0) == original_survives,
                     'unexpected original-suite mutant outcome: ' + label)
                supplemental = None
                if original_survives:
                    supplemental = run([str(independent), str(mutant)])
                    need(supplemental['exit_code'] != 0, 'audit failed to kill weakened guard: ' + label)
                modes.append({'mode': mode[0] if mode else 'normal',
                              'original_suite': original_result, 'audit_adversarial_suite': supplemental})
            results.append({'mutation': label, 'mutant_sha256': hashlib.sha256(mutated.encode()).hexdigest(),
                            'expected_original_suite_survival': original_survives, 'runs': modes})
    need(original.read_bytes() == payload, 'frozen input changed')
    print(json.dumps({'status': 'passed', 'original_unchanged': True,
                      'input_sha256': hashlib.sha256(payload).hexdigest(), 'mutations': results,
                      'scope': 'Eight deliberately chosen semantic mutants; not exhaustive mutation coverage.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
