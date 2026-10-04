#!/usr/bin/env python3
"""Bind the root's complete mathematical read to independent frozen evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

A = Path(__file__).resolve().parent
T = A / 'snapshot/unsolved_math_prioritization/attempts/9900002'

def need(value, message):
    if not value:
        raise RuntimeError(message)

def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'mode': oct(stat.S_IMODE(p.stat().st_mode))}

def load(p):
    return json.loads(p.read_text())

snapshot = load(A / 'snapshot_manifest.json')
need(snapshot['head'] == 'c96a3b2019ed3d6aabe0612b31491161dcb275e8', 'submitted head')
target = [x for x in snapshot['files'] if x['path'].startswith(snapshot['target_prefix'] + '/')]
need(len(target) == 18, 'exact eighteen historical target files')
for x in target:
    q = pin(A / 'snapshot' / x['path'])
    need(q['sha256'] == x['sha256'] and q['bytes'] == x['bytes'], x['path'])

family_pins = {}
for family, names in {
    'renewal_probability': [('PROBABILITY_AUDIT.md', 'f8aa56951e196dc03b8f8506e48be60f612c063b9631ada8d5a619514009fd1e'),
                            ('CLOSURE_MANIFEST.json', '19dd7633c2eeebc5c88abad9e130f7b701205e0a51b6b0c6c24d610f63dec9c4')],
    'normalization_limits': [('FINAL_NORMALIZATION_REPORT.md', 'bf5322e15f09f366bbda919a20ffb58d16b7d7819d4b7c0f95cac5441fa1e2a6'),
                             ('NORMALIZATION_EXECUTION_EVIDENCE.json', 'aa9df9fcab81d792ab2a9522905abe0500e416d245f0af958669f877887a37b1')]
}.items():
    p = A / family
    for name, sha in names:
        need(pin(p / name)['sha256'] == sha, name)
    files = [f for f in p.iterdir() if f.is_file()]
    need(len(files) == (14 if family == 'renewal_probability' else 8), 'complete held family inventory')
    family_pins[family] = {f.name: pin(f) for f in sorted(files)}
    need(all(x['mode'] == '0o444' for x in family_pins[family].values()), 'final family read-only modes')
    for stage in ['SOURCE', 'CANDIDATE']:
        gate = load(A / f'ROOT_{"RENEWAL" if family == "renewal_probability" else "NORMALIZATION"}_{stage}_GATE.json')
        for name, old in gate['held_files'].items():
            now = family_pins[family][name]
            need(now['bytes'] == old['bytes'] and now['sha256'] == old['sha256'], 'early checkpoint byte preservation')
            need(old['mode'] == ('0o644' if family == 'renewal_probability' else '0o444'), 'historical mode')

prob = A / 'renewal_probability'
closure = load(prob / 'CLOSURE_MANIFEST.json')
need(len(closure['files']) == 13, 'probability closure inventory')
for f in closure['files']:
    need(pin(Path(f['path'])) == {k: f[k] for k in ['bytes', 'sha256', 'mode']}, 'probability held closure pin')
for f in load(prob / 'READ_INPUT_MANIFEST.json')['files']:
    need(pin(Path(f['path']))['sha256'] == f['sha256'], 'probability original read input')

pruns = load(prob / 'CONTROL_EXECUTION_RECEIPT.json')['runs']
nruns = load(A / 'normalization_limits/NORMALIZATION_EXECUTION_EVIDENCE.json')['runs']
need(len(pruns) == 3 and len(nruns) == 3, 'all six actual family executions')
for r in pruns:
    program = Path(r['argv'][-1])
    need(program.read_text() == r['program_body'], 'entire embedded program body')
    need(pin(program)['sha256'] == r['program_sha256'], 'probability actual program pin')
    need(r['exit_code'] == 0 and r['stderr'] == '', 'probability successful actual streams')
    if 'expected_output_path' in r:
        need(r['stdout'].encode() == Path(r['expected_output_path']).read_bytes(), 'probability entire inherited output')
for r in nruns:
    program = Path(r['argv'][-1])
    need({k: pin(program)[k] for k in ['bytes', 'sha256']} == r['script'], 'normalization actual program pin')
    need(r['returncode'] == 0 and r['stderr'] == '', 'normalization successful actual streams')
    if program.name == 'verify_turn1.py':
        need(r['stdout'].encode() == (T / 'TURN_1_CHECKS.json').read_bytes(), 'normalization entire author output')
    elif program.name == 'independent_checks.py':
        need(r['stdout'].encode() == (T / 'review/independent_output.json').read_bytes(), 'normalization entire inherited output')

root_runs = {}
for name, expected in [('pr316_fresh_probability_root001', pruns[0]['stdout'].encode()),
                       ('pr316_fresh_normalization_root001', nruns[2]['stdout'].encode())]:
    p = A / 'root_runs_private' / name
    e = load(p / 'execution.json')
    need(e['exit_code'] == 0 and (p / 'stderr.bin').read_bytes() == b'', 'root replay exit')
    need((p / 'stdout.bin').read_bytes() == expected, 'root replay complete byte-identical stream')
    need(pin(Path(e['argv'][-1]))['sha256'] == e['programs'][0]['sha256'], 'root replay program pin')
    root_runs[name] = e

receipt = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'status': 'PASS_PR316_SOURCE_CORRESPONDENCE_PROOF_AND_TWO_FRESH_INDEPENDENT_MATHEMATICAL_FAMILIES',
    'pr': 316, 'submitted_head': snapshot['head'], 'author_turns': '1/5',
    'mathematical_acceptance': True, 'mathematical_completion_percent': 100,
    'workflow_completion_percent': 30, 'priority_acceptance': False,
    'preprint_ready': False, 'publication_authorized_by_this_receipt': False,
    'root_complete_semantic_reads': ['exact relevant indexed primary hypotheses and Problem 1.2',
        'all eighteen original target files', 'both entire frozen early independent assessments per family',
        'both entire final independent reports and their fresh control programs',
        'complete actual six family execution streams and both new root replay streams'],
    'strongest_verified_result': 'One strictly positive finite non-lattice infinite-mean renewal law with zero delay admits no eventually finite positive deterministic scaling of the straddling increment to a proper nondegenerate full weak limit. The truncated-mean scale is not tight along the displayed inspection sequence.',
    'mechanisms': ['submitted first-success Tonelli/Markov proof',
        'independent geometric count-of-failures concentration bound',
        'tightness plus bounded continuous test functions for all scales',
        'independent bounded-transform variance exclusion of nondegenerate limits'],
    'scope_of_computations': 'Finite exact controls and adversarial false-variant checks; the infinite-law and every-normalizer conclusions are proved analytically.',
    'family_pins': family_pins, 'root_replays': root_runs,
    'original_files_byte_preserved': 18,
    'historical_mode_transition': 'Probability early files were 0644 at source/proof gates, then deliberately frozen 0444 at final closure. Their bytes are unchanged. Normalization early and final files remain 0444.',
    'remaining_gates': ['in-depth current priority audit', 'preprint and portable verification package',
                        'successive fresh whole-package adversarial reviews until clean',
                        'exact reviewed merge, production Zenodo publication and tracker readback'],
    'source_limit': 'Original primary PDF full binary/visual access unavailable after recorded timeouts; exact relevant text was checked in the indexed institutional primary source, and formal article metadata in the publisher preview. No full preprint/published-text comparison claimed.',
    'bibliographic_correction_required_in_current_materials': 'Angus–Ding article number 108745, not historical SOURCE_GATE 108747.',
    'external_individual_contact': False
}
(A / 'ROOT_MATHEMATICAL_ACCEPTANCE.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: receipt[k] for k in ['utc', 'status', 'mathematical_completion_percent', 'workflow_completion_percent', 'priority_acceptance', 'source_limit']}, indent=2))
