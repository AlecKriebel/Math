#!/usr/bin/env python3
"""Explicit-guard verification. All verification guards survive -O and -OO."""
from __future__ import annotations
import argparse
import ast
import copy
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from finite_solver import (
    VerificationError, require, smooth_prefix, heights, solve, solve_defect_cap,
    validate_hitting, color_candidate, brute_force, branch_exact, all_optima, triples,
)
ROOT = Path(__file__).resolve().parent
DATA = ROOT.parents[1] / 'fixtures' / 'exact'
SCHEMA = 'ep168-synthetic-recovery-prefix-v1'
PROVENANCE = 'New reconstruction on 2026-10-15; not restored original unpublished bytes.'
ROW_KEYS = {'index','X','tau','selected','defect','optimal_count','heights','colors',
            'isolated','q0_candidate','q1_candidate','adjusted_colors','patch_m',
            'avoidance','delta_tau','delta_avoidance','q0','q1','q0_selected','q1_selected'}
MUTATIONS = ('wrong_tau', 'omit_vertex', 'wrong_X', 'wrong_count', 'wrong_delta',
             'wrong_q0', 'wrong_q1', 'wrong_q0_witness', 'wrong_color',
             'wrong_patch', 'truncate_prefix', 'historic_bytes_claim')

def read(name):
    return json.loads((DATA / name).read_text())

def validate_packet(packet, recompute=True):
    require(type(packet) is dict and set(packet) == {'schema','provenance','rows'}, 'packet keys mismatch')
    require(packet['schema'] == SCHEMA, 'schema mismatch')
    require(packet['provenance'] == PROVENANCE, 'reconstruction provenance mismatch')
    rows = packet['rows']
    require(type(rows) is list and len(rows) == 200, 'exactly 200 prefix rows required')
    ds = smooth_prefix(200)
    previous_tau = 0
    for index, (X, row) in enumerate(zip(ds, rows), 1):
        require(type(row) is dict and set(row) == ROW_KEYS, 'row keys mismatch')
        require(row['index'] == index and row['X'] == X, 'smooth prefix order or cutoff mismatch')
        for k in ('tau','defect','optimal_count','avoidance','delta_tau','delta_avoidance','q0','q1','q0_candidate','q1_candidate'):
            require(type(row[k]) is int, 'integer field required: '+k)
        require(0 <= row['tau'] <= index, 'invalid tau range')
        require(row['optimal_count'] >= 1, 'invalid optimum count')
        require(row['heights'] == heights(X), 'column heights mismatch')
        defect = validate_hitting(X,row['selected'],row['tau'])
        require(defect == row['defect'], 'witness defect mismatch')
        require(row['avoidance'] == index-row['tau'], 'avoidance cardinality mismatch')
        require(row['delta_tau'] == row['tau']-previous_tau and row['delta_tau'] in (0,1), 'delta tau mismatch')
        require(row['delta_avoidance'] == 1-row['delta_tau'], 'delta avoidance mismatch')
        require(validate_hitting(X,row['q0_selected'],row['q0']) == 0, 'q0 witness is not exact-one')
        require(validate_hitting(X,row['q1_selected'],row['q1']) <= 1, 'q1 witness excess exceeds one')
        candidate = color_candidate(X)
        for k,v in candidate.items():
            require(row[k] == v, 'candidate field mismatch: '+k)
        require(row['tau'] <= row['q1'] <= row['q0'], 'constraint relaxation order mismatch')
        if recompute:
            actual = solve(X, count_optima=True)
            require(row['tau'] == actual['tau'], 'transfer minimum mismatch')
            require(row['optimal_count'] == actual['optimal_count'], 'transfer optimal-count mismatch')
            require(row['q0'] == solve_defect_cap(X,0)['minimum'], 'defect-zero recurrence mismatch')
            require(row['q1'] == solve_defect_cap(X,1)['minimum'], 'defect-one recurrence mismatch')
        previous_tau = row['tau']
    require(rows[23]['tau'] == 7 and rows[23]['X'] == 162, 'index24 anchor mismatch')
    require(rows[44]['tau'] == 14 and rows[44]['X'] == 1536 and rows[44]['q0'] == 15, 'index45 anchor mismatch')
    require(rows[76]['X'] == 3**9 and rows[76]['delta_avoidance'] == 1, 'index77 avoidance anchor mismatch')
    return rows

def validate_other_artifacts(rows):
    expected_small = []
    for index,row in enumerate(rows[:25],1):
        b = branch_exact(row['X'])
        require(b['tau'] == row['tau'], 'independent edge-branch mismatch')
        item = {'index':index,'X':row['X'],'branch':b}
        if index <= 20:
            e = brute_force(row['X'])
            require(e['tau'] == row['tau'], 'independent all-subset minimum mismatch')
            require(e['optimal_count'] == row['optimal_count'], 'independent all-subset count mismatch')
            item['exhaustive'] = e
        expected_small.append(item)
    require(read('independent_small_checks.json') == {'rows':expected_small}, 'independent check record mismatch')
    numeric = [{'index':r['index'],'X':r['X'],'tau':r['tau']} for r in rows if r['X'] <= 192]
    require(read('tau_through_X192.json') == numeric, 'numeric X192 table mismatch')
    opts = all_optima(rows[44]['X'])
    opts['X'], opts['index'] = rows[44]['X'],45
    opts['excess_profiles'] = [[[edge[0],sum(n in H for n in edge)-1] for edge in triples(opts['X'])
                                if sum(n in H for n in edge)>1] for H in opts['solutions']]
    require(opts['optimal_count'] == 1, 'index45 uniqueness mismatch')
    require(opts['excess_profiles'] == [[[192,1]]], 'index45 extra-hit location mismatch')
    require(read('all_optima_index45.json') == opts, 'all-optima artifact mismatch')
    require(read('candidate_comparison.json') == {
        'checked_smooth_prefixes':200,'maximum_X':rows[-1]['X'],
        'q0_formula_mismatches':[r['index'] for r in rows if r['q0'] != r['q0_candidate']],
        'q1_formula_mismatches':[r['index'] for r in rows if r['q1'] != r['q1_candidate']],
        'q1_not_tau_indices':[r['index'] for r in rows if r['q1'] != r['tau']],
        'scope':'Finite checks only. Neither q0 nor q1 formula is proved for all cutoffs.'}, 'candidate comparison mismatch')
    for name in ('finite_solver.py','verify_exact.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((ROOT/name).read_text()))),
                'optimization-sensitive assert statement in '+name)

def mutate(packet,name):
    p = copy.deepcopy(packet)
    row = p['rows'][44]
    if name == 'wrong_tau': row['tau'] += 1
    elif name == 'omit_vertex': row['selected'].remove(3)
    elif name == 'wrong_X': row['X'] += 1
    elif name == 'wrong_count': row['optimal_count'] = 2
    elif name == 'wrong_delta': row['delta_avoidance'] = 0
    elif name == 'wrong_q0': row['q0'] -= 1
    elif name == 'wrong_q1': row['q1'] += 1
    elif name == 'wrong_q0_witness': row['q0_selected'] = row['q1_selected'][:]
    elif name == 'wrong_color': row['colors'][0] += 1
    elif name == 'wrong_patch': row['patch_m'] = None
    elif name == 'truncate_prefix': p['rows'].pop()
    elif name == 'historic_bytes_claim': p['provenance'] = 'Restored original unpublished certificate bytes.'
    else: raise VerificationError('unknown negative control')
    return p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inject',choices=MUTATIONS)
    args = ap.parse_args()
    packet = read('prefix_200.json')
    if args.inject:
        packet = mutate(packet,args.inject)
        # The count mutation needs exact minimizer counting; check it first with
        # the direct backtracking recurrence, so rejection is independent.
        if args.inject == 'wrong_count':
            require(packet['rows'][44]['optimal_count'] == all_optima(packet['rows'][44]['X'])['optimal_count'],
                    'direct all-optima count mismatch')
        validate_packet(packet,recompute=False)
        raise VerificationError('negative control was not rejected')
    rows = validate_packet(packet,recompute=True)
    validate_other_artifacts(rows)
    print(json.dumps({'verified':True,'prefixes':200,'maximum_X':rows[-1]['X'],
                      'independent_exhaustive_prefixes':20,'independent_branch_prefixes':25,
                      'all_optima_index45':1,'q0_formula_finite_mismatches':sum(r['q0'] != r['q0_candidate'] for r in rows),
                      'q1_formula_finite_mismatches':sum(r['q1'] != r['q1_candidate'] for r in rows),
                      'tau_q1_finite_mismatches':sum(r['tau'] != r['q1'] for r in rows)},sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (VerificationError,ValueError,TypeError,KeyError) as error:
        print('VERIFICATION FAILED: '+str(error), file=sys.stderr)
        sys.exit(2)
