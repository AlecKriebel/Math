#!/usr/bin/env python3
"""Finite adversarial controls of source predicates, without importing them.

The small independent models below explicitly identify the source predicates
they model. Passing vectors are local counterexamples, not full forged gate
executions. The sole file-write demonstration uses only this family's private
first-party fixture directory; it never addresses native or reviewed paths.
"""
import ast
import copy
import datetime
import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
PREP = AUDIT / 'acceptance_preparation_family'


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def same(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) is list: return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def digest(raw): return hashlib.sha256(raw).hexdigest()
def load(p): return json.loads(p.read_bytes())


def main():
    source = (PREP / 'pr40_guards.py').read_text()
    integrate = (PREP / 'integrate_reviewed_partial.py').read_text()
    mirror = (PREP / 'state_mirror_reconciliation.py').read_text()
    ast.parse(source)
    results = []

    scope = load(PREP / 'SCIENTIFIC_SCOPE.json')
    original = (AUDIT / 'source_snapshot/SOURCE_STATUS.md').read_text()
    primary = (AUDIT / 'whole_current_source_first_family/ROOTforeign_primary/kuhlmann_2006_correct.pdf.txt').read_text()
    require(any('cusped orientable and nonorientable' in x and 'published Kuhlmann' in x for x in scope['credited_existing_coverage']), 'Scope attribution vector')
    require('Theorem 1.1 Every cusped orientable hyperbolic 3' in primary, 'Published orientable hypothesis')
    require('Cusped and nonorientable: Xia, Theorem 1.2 / 4.1' in original, 'Correct unchanged original attribution')
    require('Xia' not in json.dumps(scope['credited_existing_coverage']), 'Xia omitted from scope list')
    require("equal(o['scientific_scope'],load(HERE/'SCIENTIFIC_SCOPE.json'))" in source, 'Whole plan exact-binds wrong attribution')
    require("'scientific_scope':g.load(g.HERE/'SCIENTIFIC_SCOPE.json')" in integrate, 'Accepted receipt copies wrong attribution')
    require("'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json')" in source, 'Accepted guard mandates wrong attribution')
    results.append({'control': 'S1_existing_theorem_attribution', 'finding_reproduced': True,
                    'classification': 'Mandatory scientific attribution correction; no target counterexample',
                    'source_mapping': ['SCIENTIFIC_SCOPE.json credited_existing_coverage[2]', 'DRAFT_FINAL_PLAN.json scientific_scope', 'pr40_guards.py:230,232,300', 'integrate_reviewed_partial.py:102'],
                    'whole_scope_equal_draft': same(scope, load(PREP / 'DRAFT_FINAL_PLAN.json')['scientific_scope']),
                    'published_Kuhlmann_hypothesis': 'orientable', 'nonorientable_cusped_attribution': 'Xia Theorems1.2/4.1'})

    # Exactly the nonempty-string clock predicate in guards:262, independently
    # transcribed, without any reviewed module or AST execution.
    def clock_predicate(start, finish):
        return type(start) is str and bool(start) and type(finish) is str and bool(finish)
    vectors = [('not-a-clock', 'also-not-a-clock'), ('2026-10-02T13:00:00+00:00', '2026-10-01T13:00:00+00:00')]
    require(all(clock_predicate(*v) for v in vectors), 'Original local clock predicate admits vectors')
    try: datetime.datetime.fromisoformat(vectors[0][0])
    except ValueError: invalid_rejected = True
    else: invalid_rejected = False
    require(invalid_rejected and datetime.datetime.fromisoformat(vectors[1][1]) < datetime.datetime.fromisoformat(vectors[1][0]), 'Independent semantic clock checks')
    require("type(cap['started_utc']) is str and cap['started_utc'] and type(cap['finished_utc']) is str and cap['finished_utc']" in source, 'Clock predicate source mapping')
    results.append({'control': 'S2_actual_capture_clocks', 'finding_reproduced': True, 'source_mapping': ['pr40_guards.py:262'],
                    'admitted_local_vectors': [{'started_utc': s, 'finished_utc': f} for s, f in vectors],
                    'scope_limit': 'Local gate predicate; no reviewed helper or full acceptance gate executed'})

    # rows() correctly rejects stdout==stderr, but does not see the prelaunch
    # source in its two input rows. A stderr/source alias has no duplicate row.
    sealed_source = (PREP / 'seal_final_evidence.py').read_bytes()
    stdout = b'{"status":"PASS","final_receipt_sha256":"' + b'1' * 64 + b'","final_manifest_sha256":"' + b'2' * 64 + b'"}\n'
    objects = {'CAPTURE.json': b'fixture capture retained separately', 'prelaunch_source.py': sealed_source, 'stdout.bin': stdout}
    streams = [{'path': 'stdout.bin', 'bytes': len(stdout), 'sha256': digest(stdout)},
               {'path': 'prelaunch_source.py', 'bytes': len(sealed_source), 'sha256': digest(sealed_source)}]
    require(len({r['path'] for r in streams}) == len(streams), 'Original two-row duplicate guard passes')
    require(all(len(objects[r['path']]) == r['bytes'] and digest(objects[r['path']]) == r['sha256'] for r in streams), 'Original two-row full byte guard passes')
    demand_names = {'CAPTURE.json', 'prelaunch_source.py', streams[0]['path'], streams[1]['path']}
    require(set(objects) == demand_names and len(demand_names) == 3, 'Original exact set collapses three distinct files')
    require(load(PREP / 'SCIENTIFIC_SCOPE.json')['full_problem_solved'] is False, 'No final theorem claim in vector')
    require("check(cb,[cap['stdout'],cap['stderr']])" in source and "exact(cb,{ps['reconciliation_capture'].name,'prelaunch_source.py',cap['stdout']['path'],cap['stderr']['path']})" in source, 'Stream guard source mapping')
    results.append({'control': 'S3_capture_stderr_aliases_prelaunch_source', 'finding_reproduced': True,
                    'source_mapping': ['pr40_guards.py:99,266-268'], 'stdout_equal_stderr_is_rejected': True,
                    'stderr_path': 'prelaunch_source.py', 'source_and_two_stream_guards_pass': True,
                    'set_collapsed_exact_file_count': 3, 'required_distinct_file_count': 4,
                    'scope_limit': 'Local full byte/set predicate vector; not a claim that genuine root captures have collided'})

    # Readable real interleaving of the same check/temp/replace mechanism, only
    # within this NEW family. Each before/after byte object remains retained.
    fixture = HERE / 'private_fixtures'
    require(not fixture.exists(), 'Own fixture starts absent')
    fixture.mkdir()
    target = fixture / 'exclusive_target.json'
    temporary = fixture / 'exclusive_target.json.pr40-tmp'
    require(not target.exists(), 'exclusive exists check at t1')
    intended = b'{"writer":"first","phase":"intended"}\n'
    intervening = b'{"writer":"second","phase":"created_after_absence_check"}\n'
    with temporary.open('xb') as stream: stream.write(intended)
    with target.open('xb') as stream: stream.write(intervening)
    (fixture / 'intervening_complete_preimage.json').write_bytes(target.read_bytes())
    os.replace(temporary, target)
    (fixture / 'intended_complete_bytes.json').write_bytes(intended)
    require(target.read_bytes() == intended and (fixture / 'intervening_complete_preimage.json').read_bytes() == intervening, 'Intervening target overwritten')
    require("if exclusive: require(not p.exists(),'Existing output: inspect before retry')" in source and 'os.replace(tmp,p)' in source, 'Exclusive race source mapping')
    results.append({'control': 'S4_exclusive_write_absence_race', 'finding_reproduced': True,
                    'source_mapping': ['pr40_guards.py:156-163'], 'actual_own_private_interleaving': True,
                    'steps': ['t1 exclusive absent check', 't2 temporary xb created', 't3 second writer creates target', 't4 os.replace overwrites target'],
                    'intervening_original_bytes_retained': 'private_fixtures/intervening_complete_preimage.json',
                    'actual_overwritten_target_retained': 'private_fixtures/exclusive_target.json',
                    'scope_limit': 'Only own disposable first-party fixture; reviewed helper and native/canonical/shared paths untouched'})

    # Contract's dated-reason requirement is stronger than this literal guard.
    local_reason = {'reason': 'yes', 'current_head': 'a' * 40}
    reason_ok = type(local_reason['reason']) is str and bool(local_reason['reason']) and type(local_reason['current_head']) is str and bool(re.fullmatch('[0-9a-f]{40}', local_reason['current_head']))
    require(reason_ok and 'nonempty dated reason' in (PREP / 'CONTRACT.md').read_text(), 'Undated local reason admits')
    results.append({'control': 'S5_undated_rebase_reason', 'finding_reproduced': True,
                    'source_mapping': ['CONTRACT.md:21', 'pr40_guards.py:273'], 'admitted_local_vector': local_reason,
                    'scope_limit': 'Small contract gap; full13 source pins/main actual HEAD/fresh state remain required, no stale rebase bypass claimed'})

    # These tests check independent expectations, then bind the visible source
    # assertions. They do not fabricate actual future PR39 or native records.
    original_ledger = load(AUDIT / 'source_snapshot/turns.json')
    negatives = []
    for label, changed in [('bool_count', False), ('count_one', 1), ('wrong_id', 20001896), ('phantom_attempt', [{'number': 1}]), ('extra_field', None)]:
        mutant = copy.deepcopy(original_ledger)
        if label in ['bool_count', 'count_one']: mutant['count'] = changed
        elif label == 'wrong_id': mutant['id'] = changed
        elif label == 'phantom_attempt': mutant['substantive_attempts'] = changed
        else: mutant['extra'] = changed
        require(not same(mutant, original_ledger), 'Typed whole ledger mutant rejection expectation')
        negatives.append(label)
    require('len(prior)==30' in mirror and "sum(z['turns_used'] for z in prior.values())==37" in mirror, 'Fresh30/37 source guard')
    require("len(plan['history_append'])==1" in mirror and "'duplicate_ids':[]" in mirror and "'new_proof_turns':0" in mirror, 'Exact one event zero turns source guard')
    require("all(g.equal(plan['state_after'][k],v) for k,v in prior.items())" in mirror and "'20001896' not in plan['state_after']" in mirror, 'Prior states unchanged and no duplicate source guard')
    require("ps['previous_mirror']==B/'audits/pr39_9500008/state_mirror_bindings.json'" in source, 'Exact future prior39 path')
    require("len(previous['entries'])==29 and 39 in previous['required_completed_prs'] and 40 not in previous['required_completed_prs']" in source, 'Exact future prior39 scope')
    require(not same(False, 0) and not same(None, {}) and not same({'a': 0}, {'a': 0, 'b': None}), 'Typed complete equality boundaries')
    results.append({'control': 'C1_preservation_and_zero_budget_source_contract', 'status': 'PASS_STATIC_BOUNDARY_CHECKS',
                    'whole_typed_zero_ledger_negatives': negatives, 'bool_integer_null_object_extra_key_boundaries_distinct': True,
                    'fresh_future_prior39_cli_source_binding': True, 'one_primary_present_event_zero_turns_no_duplicate_state_source_guards': True,
                    'scope_limit': 'Actual prior39 acceptance, fresh13 native files, SQL-driver plan/no-op and remote gate still require genuine root execution'})
    print(json.dumps({'schema': 'pr40-independent-acceptance-static-controls/v1', 'status': 'FINDINGS_REPRODUCED_STATIC_ONLY',
                      'controls': results, 'reviewed_helper_import_or_execution': False,
                      'Git_SQL_native_shared_remote_access': False,
                      'own_private_fixture_writes_only': True,
                      'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0}, sort_keys=True, indent=2))


if __name__ == '__main__': main()
