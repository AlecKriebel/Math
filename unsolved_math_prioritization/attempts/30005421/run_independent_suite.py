#!/usr/bin/env python3
"""Replay the independent checker and twelve mathematical fault mutations.

Run from any directory. Writes only to stdout; no third-party dependencies.
All clean/mutant executions use the same pinned checker in three Python modes.
"""
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

EXPECTED = {
    'reverse_skew':'Euler_skew_identity',
    'negative_sign_reversed':'uniform_numerical_estimate',
    'minimum_instead_of_maximum':'unweighted_box',
    'zero_epsilon':'strict_epsilon_positive',
    'gap_ignores_cutoff':'strict_expansion_gap',
    'transpose_incidence':'incidence_dimension',
    'reverse_avoidance':'negative_euler_locus_excluded',
    'missing_n_normalization':'weighted_orthogonality',
    'missing_f_normalization':'Euler_homogeneity',
    'wrong_coordinate_sign':'coordinate_square',
    'all_Rayleigh_quotients_equal':'Rayleigh_quotient_variation',
    'zero_offcomponent_kappa':'disconnected_full_cone_positivity',
}


def demand(value, label):
    if not value:
        raise RuntimeError(label)


def main():
    checker=Path(__file__).with_name('independent_check.py')
    raw=checker.read_bytes()
    parsed=ast.parse(raw)
    demand(not any(isinstance(n,ast.Assert) for n in ast.walk(parsed)),
           'Independent verifier unexpectedly contains assert statements')
    rows=[]
    baseline_bytes=None
    for mode,flags in [('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]:
        for mutant in ['none']+list(EXPECTED):
            args=[sys.executable,'-B']+flags+[str(checker),'--mutant',mutant]
            p=subprocess.run(args,capture_output=True)
            demand(not p.stderr,'Unexpected stderr: '+p.stderr.decode(errors='replace'))
            result=json.loads(p.stdout)
            if mutant == 'none':
                demand(p.returncode==0 and result['status']=='PASS','Clean execution failed')
                if baseline_bytes is None:
                    baseline_bytes=p.stdout
                demand(p.stdout==baseline_bytes,'Clean output changed across optimization modes')
                evidence={'checks':result['total_checks'],
                          'enumerated':sum(c['enumerated'] for c in result['cases']),
                          'eligible':sum(c['eligible'] for c in result['cases']),
                          'strict_cutoffs':sum(c['strict_cutoffs'] for c in result['cases']),
                          'negative_Rayleigh_vectors':sum(c['negative_Rayleigh_vectors'] for c in result['cases'])}
            else:
                demand(p.returncode==1 and result['status']=='REJECT','Mutant was not rejected: '+mutant)
                demand(result['failure']['failed_check']==EXPECTED[mutant],
                       'Mutation rejected for an unexpected reason: '+mutant)
                evidence=result
            rows.append({'mode':mode,'mutant':mutant,'exit_code':p.returncode,
                         'stdout_bytes':len(p.stdout),'stdout_sha256':sha256(p.stdout).hexdigest(),
                         'evidence':evidence})
    print(json.dumps({'status':'PASS','checker_sha256':sha256(raw).hexdigest(),
        'checker_bytes':len(raw),'assert_nodes':0,'clean_runs':3,'rejected_mutant_runs':36,
        'same_clean_output_all_modes':True,'baseline':json.loads(baseline_bytes),
        'runs':rows},indent=2,sort_keys=True))
    return 0


if __name__=='__main__':
    sys.exit(main())
