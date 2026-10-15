#!/usr/bin/env python3
"""Positive authored payload seal for the complete current-candidate review."""
from pathlib import Path
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
PAYLOAD = [
    'REPORT.md', 'RESULT.json', 'RESEARCH_LOG.md', 'INITIAL_RECONSTRUCTION.md',
    'INITIAL_BINDINGS.json', 'SOURCE_ACQUISITION.json', 'ADDITIONAL_SOURCE_ACQUISITION.json',
    'controls.py', 'run_controls.py', 'review_peer_proposal.py', 'verify_exposed_inputs.py', 'seal_review.py',
    'CONTROL_RESULTS.json', 'CONTROL_RESULTS_OPTIMIZED.json', 'CONTROL_RUN_SUMMARY.json', 'INPUT_BINDINGS.json',
    'records/fresh_bad_marker_normal.json', 'records/fresh_bad_marker_optimized.json',
    'records/fresh_controls_optimized.json', 'records/original_bad_flow_normal.json',
    'records/original_bad_flow_optimized.json', 'records/original_bad_marker_normal.json',
    'records/original_bad_marker_optimized.json', 'records/original_bad_pair_normal.json',
    'records/original_bad_pair_optimized.json', 'records/original_baseline.json',
    'records/original_baseline_optimized.json', 'records/peer_proposal_replay.json',
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


result = json.loads((HERE/'RESULT.json').read_text())
require(result['pr'] == 445 and result['problem_id'] == 30002737 and
        result['frozen_head'] == '3242c84e06db7e99012c7fe581adde5c3f89fc89' and
        result['reviewer'] == '/root/pr445_whole_math_adversary', 'Result identity mismatch')
for field in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']:
    require(type(result[field]) is int, 'Noninteger result count')
require([result[k] for k in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']] == [1, 1, 0],
        'Original current-candidate history not preserved')
rows = []
for name in PAYLOAD:
    f = HERE/name
    require(f.is_file() and not f.is_symlink(), 'Missing or indirect authored payload '+name)
    data = f.read_bytes()
    if f.suffix == '.py':
        require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(data))), 'Essential assert present '+name)
    rows.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                 'classification': 'positive_authored_payload'})
require(hashlib.sha256((HERE/'INITIAL_RECONSTRUCTION.md').read_bytes()).hexdigest() ==
        '630b044983db4deb7a695037ce1ed49d2a193498cded21cf345b9054c95e3fa4', 'Independent checkpoint changed')
manifest = {'schema_version': 1, 'pr': 445, 'problem_id': 30002737,
            'frozen_head': result['frozen_head'], 'reviewer': result['reviewer'],
            'policy': 'Positive complete authored allowlist; all controlling code and raw records included; no self-hash. No foreign source bytes/extracts/renders, copied candidate code, mutants, private fixtures, cache or environments are public.',
            'files': rows, 'excluded_directory_prefixes': ['private/', '__pycache__/', '.venv/', 'cache/']}
(HERE/'PUBLIC_FILES.json').write_text(json.dumps(manifest, indent=2)+'\n')
for row in json.loads((HERE/'PUBLIC_FILES.json').read_text())['files']:
    data = (HERE/row['path']).read_bytes()
    require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], 'Seal readback mismatch')
print(json.dumps({'status': 'SEALED', 'payloads': len(rows), 'counts': [1, 1, 0],
                  'central_mathematical_scope_counts': [0, 0, 0], 'foreign_payloads': 0}, indent=2))
