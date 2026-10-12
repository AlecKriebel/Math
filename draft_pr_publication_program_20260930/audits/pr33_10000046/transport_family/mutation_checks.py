#!/usr/bin/env python3
"""Tamper with private in-memory certificate copies; preserve each rejection.
No solver imports; the independent verifier is the checker under attack.
"""
from copy import deepcopy
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('transport_certificate_checker', HERE/'check_certificates.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
data = json.loads((HERE/'certificates.json').read_text())
outputs = []


def try_bad(name, record, validate):
    try:
        validate(record)
    except AssertionError as error:
        outputs.append({'name': name, 'rejected': True, 'reason': str(error)})
    else:
        outputs.append({'name': name, 'rejected': False, 'reason': 'validator accepted corruption'})
        raise AssertionError(name)


record = deepcopy(data['finite'][2])
record['permutation'][1] = record['permutation'][0]
try_bad('duplicate_right_label_breaks_full_marginal', record, checker.finite)

record = deepcopy(data['finite'][2])
record['Hall_A'] = []
try_bad('erase_nonzero_Hall_deficiency', record, checker.finite)

record = deepcopy(data['finite'][2])
record['safe_count'] += 1
try_bad('inflate_finite_optimum', record, checker.finite)

record = deepcopy(data['finite'][2])
record['event'] = 'synchronous'
try_bad('substitute_synchronous_relation_for_full', record, checker.finite)

record = deepcopy(data['finite'][19])
record['event'] = 'drop_zero'
try_bad('omit_initial_vertex_of_shared_start', record, checker.finite)

record = deepcopy(data['weighted'][0])
record['optimum'] = '1'
try_bad('use_unweighted_perfect_matching_probability', record, checker.weighted)

record = deepcopy(data['weighted'][0])
record['full_coupling'][0][0] = '1/2'
try_bad('change_weighted_row_mass', record, checker.weighted)

record = deepcopy(data['vanishing'][-1])
record['optimum'] = '1/2'
try_bad('pretend_vanishing_prefix_mass_is_uniform', record, checker.weighted)

result = {'pass': True, 'tested': len(outputs), 'all_corruptions_rejected': True,
          'failures_preserved': outputs,
          'scope': 'Corrupted local certificate controls only; original frozen files untouched'}
(HERE/'MUTATION_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
