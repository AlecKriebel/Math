"""Offline adversarial cases; all writes remain in this folder's ignored tmp."""
import argparse
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

import accepted_state_sync as sync

STAMP = '2026-10-01T20:00:00+00:00'
LEGACY = sync.HERE.parents[2] / 'unsolved_math_prioritization/queue.py'


class AcceptanceMirrorTests(unittest.TestCase):
    def setUp(self):
        (sync.HERE / 'tmp').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=sync.HERE / 'tmp')
        self.repo = Path(self.temp.name)
        self.q = self.repo / 'unsolved_math_prioritization'
        self.q.mkdir()
        self.write('unsolved_math_prioritization/state.json', {'999': {'status': 'partial', 'turns_used': 2}})
        (self.q / 'history.jsonl').write_text('')
        problem = {'id': 1, 'statement': 'An original mathematical target that remains unresolved.'}
        cache = self.q / 'cache'
        cache.mkdir()
        with sqlite3.connect(cache / 'catalog.sqlite') as db:
            db.execute('CREATE TABLE records (key TEXT PRIMARY KEY,payload TEXT,report TEXT)')
            db.execute('INSERT INTO records VALUES (?,?,?)', ('1', json.dumps(problem), '{}'))
        db.close()
        hashes = sync.source_hashes(self.repo, '1')
        self.write('unsolved_math_prioritization/catalog.json', [
            {'id': '1', 'present': True, 'eligible': True, **hashes},
            {'id': '2', 'present': True, 'eligible': False}])
        self.write('unsolved_math_prioritization/policy.json', {'turn_limit': 5})
        self.queue = '| Rank | ID / code | Problem | Status | Turns | DOI |\n|---|---|---|---|---|---|\n| 1 | 1 / TARGET | Original target | unsolved | 1/5 |  |\n'
        (self.q / 'QUEUE.md').write_text(self.queue)
        self.inventory_path = 'program/inventory.json'
        self.write(self.inventory_path, {'excluded_prs': [8], 'items': [
            {'number': 1, 'headRefName': 'dot/math-1', 'headRefOid': 'a' * 40,
             'stage': 'complete', 'outcome': 'unsolved_partial_accepted_merged', 'merge_commit': 'b' * 40}]})
        self.acceptance_path = 'unsolved_math_prioritization/attempts/1/acceptance.json'
        self.proof_path = 'unsolved_math_prioritization/attempts/1/PARTIAL.md'
        self.write_text(self.proof_path, 'Original target remains unresolved; validated partial findings.\n')
        self.write(self.acceptance_path, {'pr': 1, 'problem_id': 1, 'queue_status': 'unsolved',
                   'original_head': 'a' * 40, 'merge_commit': 'b' * 40, 'merged_at': '2026-10-01T19:00:00Z',
                   'original_attempts_used': 1, 'turn_limit': 5,
                   'canonical_proof_sha256': sync.sha((self.repo / self.proof_path).read_bytes())})
        self.remote_path = 'program/pr1_1/remote.json'
        self.write(self.remote_path, {'number': 1, 'state': 'MERGED', 'headRefOid': 'a' * 40,
                   'mergeCommit': {'oid': 'b' * 40}, 'mergedAt': '2026-10-01T19:00:00Z',
                   'url': 'https://github.com/AlecKriebel/Math/pull/1'})
        self.source_path = 'unsolved_math_prioritization/attempts/1/source_record.json'
        self.write(self.source_path, problem)
        self.ledger_path = 'unsolved_math_prioritization/attempts/1/turns.json'
        self.write(self.ledger_path, {'used': 1, 'limit': 5, 'turns': [{'turn': 1}]})
        self.spec = {'authorization': 'human_authorized_current_acceptance_mirror',
                     'inventory': self.binding(self.inventory_path),
                     'queue': self.binding('unsolved_math_prioritization/QUEUE.md'),
                     'catalog': self.binding('unsolved_math_prioritization/catalog.json'),
                     'policy': self.binding('unsolved_math_prioritization/policy.json'),
                     'entries': [{'id': '1', 'pr': 1, 'status': 'unsolved',
                                  'acceptance': self.binding(self.acceptance_path),
                                  'remote': self.binding(self.remote_path),
                                  'accepted_source': self.binding(self.source_path),
                                  'artifact': self.binding(self.proof_path, acceptance_hash_field='canonical_proof_sha256'),
                                  'budget': {'used': 1, 'limit': 5, 'kind': 'json_turns', 'ledger': self.binding(self.ledger_path)},
                                  'duplicates': []}]}

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, value):
        self.write_text(name, json.dumps(value) + '\n')

    def write_text(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def binding(self, name, **extra):
        return {'path': name, 'sha256': sync.sha((self.repo / name).read_bytes()), **extra}

    def refresh(self, binding):
        binding['sha256'] = sync.sha((self.repo / binding['path']).read_bytes())

    def mutate(self, binding, callback):
        obj = sync.load(self.repo / binding['path'])
        callback(obj)
        self.write(binding['path'], obj)
        self.refresh(binding)

    def plan(self):
        return sync.build_plan(self.repo, self.spec, STAMP)

    def reject(self, message):
        with self.assertRaisesRegex(sync.Rejected, message):
            self.plan()

    def published(self):
        e = self.spec['entries'][0]
        e['status'] = 'preprint_published'
        doi = '10.5281/zenodo.123456'
        self.mutate(e['acceptance'], lambda x: x.update(queue_status=e['status'], doi=doi))
        self.mutate(self.spec['inventory'], lambda x: x['items'][0].update(doi=doi))
        self.write_text('unsolved_math_prioritization/QUEUE.md', self.queue.replace('unsolved | 1/5 |  |', f'preprint_published | 1/5 | {doi} |'))
        self.refresh(self.spec['queue'])
        self.write('program/publication.json', {'doi': doi, 'published_state_verified_by_repository_tool': True})
        e['publication'] = self.binding('program/publication.json')
        return e

    def test_dry_run_preserves_original_files_and_unrelated_state(self):
        before = {x: (self.q / x).read_bytes() for x in ['state.json', 'history.jsonl', 'QUEUE.md', 'catalog.json']}
        plan = self.plan()
        self.assertEqual(plan['state_after']['999'], {'status': 'partial', 'turns_used': 2})
        imported = plan['state_after']['1']
        self.assertEqual((imported['status'], imported['turns_used'], imported['turn_limit']), ('unsolved', 1, 5))
        self.assertEqual(imported['at'], STAMP)
        self.assertNotIn('candidate_turn', imported)
        self.assertNotIn('readiness_review_hash', imported)
        self.assertFalse(imported['evidence']['historical_transitions_asserted'])
        self.assertEqual(before, {x: (self.q / x).read_bytes() for x in before})

    def test_pending_inventory_is_rejected(self):
        self.mutate(self.spec['inventory'], lambda x: x['items'][0].update(stage='fresh_gate_running'))
        self.reject('pending')

    def test_unmerged_remote_is_rejected(self):
        self.mutate(self.spec['entries'][0]['remote'], lambda x: x.update(state='OPEN'))
        self.reject('MERGED')

    def test_remote_original_head_mismatch_is_rejected(self):
        self.mutate(self.spec['entries'][0]['remote'], lambda x: x.update(headRefOid='c' * 40))
        self.reject('exact-head')

    def test_acceptance_merge_mismatch_is_rejected(self):
        self.mutate(self.spec['entries'][0]['acceptance'], lambda x: x.update(merge_commit='c' * 40))
        self.reject('merge mismatch')

    def test_stale_acceptance_bytes_are_rejected(self):
        self.write(self.acceptance_path, {'pr': 99})
        self.reject('Stale/mismatched')

    def test_wrong_acceptance_id_is_rejected_even_when_hash_refreshed(self):
        self.mutate(self.spec['entries'][0]['acceptance'], lambda x: x.update(problem_id=2))
        self.reject('ID mismatch')

    def test_changed_source_is_rejected_even_when_binding_refreshed(self):
        self.mutate(self.spec['entries'][0]['accepted_source'], lambda x: x.update(statement='Different open target'))
        self.reject('source record mismatch')

    def test_current_catalog_hash_cannot_silently_rebind_source(self):
        self.mutate(self.spec['catalog'], lambda x: x[0].update(review_hash='c' * 64))
        self.reject('source/catalog hash')

    def test_wrong_accepted_artifact_is_rejected(self):
        e = self.spec['entries'][0]
        self.write_text(self.proof_path, 'Replacement result never accepted.\n')
        self.refresh(e['artifact'])
        self.reject('artifact hash')

    def test_duplicate_selected_queue_row_is_rejected(self):
        self.write_text('unsolved_math_prioritization/QUEUE.md', self.queue + self.queue.splitlines()[-1] + '\n')
        self.refresh(self.spec['queue'])
        self.reject('Ambiguous')

    def test_budget_usage_mismatch_is_rejected(self):
        self.spec['entries'][0]['budget']['used'] = 2
        self.reject('budget mismatch')

    def test_original_ledger_mismatch_is_rejected(self):
        self.mutate(self.spec['entries'][0]['budget']['ledger'], lambda x: x.update(used=2))
        self.reject('Original budget')

    def test_missing_or_displaced_budget_is_rejected(self):
        self.write_text('unsolved_math_prioritization/QUEUE.md', self.queue.replace('1/5', '?/5'))
        self.refresh(self.spec['queue'])
        self.reject('budget mismatch')

    def test_no_budget_counter_reset(self):
        self.write('unsolved_math_prioritization/state.json', {'1': {'turns_used': 4, 'status': 'partial'}})
        self.reject('decrease')

    def test_selected_duplicate_must_already_be_ineligible(self):
        e = self.spec['entries'][0]
        e['duplicates'] = ['2']
        self.write('program/duplicates.json', {'selected': '1', 'duplicate': '2'})
        e['duplicate_evidence'] = self.binding('program/duplicates.json')
        self.mutate(self.spec['catalog'], lambda x: x[1].update(eligible=True))
        self.reject('research-eligible')

    def test_preserve_duplicate_selection_without_new_budget(self):
        e = self.spec['entries'][0]
        e['duplicates'] = ['2']
        self.write('program/duplicates.json', {'selected': '1', 'duplicate': '2'})
        e['duplicate_evidence'] = self.binding('program/duplicates.json')
        plan = self.plan()
        self.assertNotIn('2', plan['state_after'])
        self.assertEqual(plan['state_after']['1']['evidence']['duplicate_ids'], ['2'])

    def test_publication_pending_is_rejected(self):
        e = self.published()
        self.mutate(e['publication'], lambda x: x.update(published_state_verified_by_repository_tool=False, state='draft'))
        self.reject('not verified public')

    def test_duplicate_doi_is_rejected(self):
        self.published()
        path = self.q / 'QUEUE.md'
        path.write_text(path.read_text() + '| 2 | 2 / OTHER | Different target | preprint_published | 1/5 | 10.5281/zenodo.123456 |\n')
        self.refresh(self.spec['queue'])
        self.reject('Duplicate/wrong-row DOI')

    def test_known_partial_cannot_acquire_new_doi(self):
        self.mutate(self.spec['entries'][0]['acceptance'], lambda x: x.update(doi='10.5281/zenodo.123456'))
        self.reject('Unpublished result')

    def test_publication_doi_mismatch_is_rejected(self):
        e = self.published()
        self.mutate(e['publication'], lambda x: x.update(doi='10.5281/zenodo.999999'))
        self.reject('Publication DOI')

    def test_idempotent_accepted_replay_and_new_plan(self):
        plan = self.plan()
        sync.replay_sandbox(plan, self.q)
        before = ((self.q / 'state.json').read_bytes(), (self.q / 'history.jsonl').read_bytes())
        sync.replay_sandbox(plan, self.q)
        self.assertEqual(before, ((self.q / 'state.json').read_bytes(), (self.q / 'history.jsonl').read_bytes()))
        next_plan = sync.build_plan(self.repo, self.spec, '2026-10-02T20:00:00+00:00')
        self.assertEqual(next_plan['history_append'], [])
        self.assertEqual(next_plan['state_after_bytes'].encode(), before[0])
        self.assertEqual(next_plan['state_after']['1']['at'], STAMP)

    def test_interruption_after_history_recovers_once(self):
        plan = self.plan()
        with self.assertRaisesRegex(RuntimeError, 'Injected'):
            sync.replay_sandbox(plan, self.q, fail_after_history=True)
        self.assertNotIn('1', sync.load(self.q / 'state.json'))
        sync.replay_sandbox(plan, self.q)
        events = [json.loads(x) for x in (self.q / 'history.jsonl').read_text().splitlines()]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['event_id'], sync.load(self.q / 'state.json')['1']['event_id'])

    def test_unknown_outcome_is_not_overwritten(self):
        plan = self.plan()
        with self.assertRaises(RuntimeError):
            sync.replay_sandbox(plan, self.q, fail_after_history=True)
        self.write('unsolved_math_prioritization/state.json', {'unexpected': 'manual concurrent edit'})
        with self.assertRaisesRegex(sync.Rejected, 'Unknown write outcome'):
            sync.replay_sandbox(plan, self.q)
        self.assertEqual(sync.load(self.q / 'state.json'), {'unexpected': 'manual concurrent edit'})

    def test_replay_live_path_is_prohibited(self):
        with self.assertRaisesRegex(sync.Rejected, 'live writes prohibited'):
            sync.replay_sandbox(self.plan(), sync.HERE.parents[2] / 'unsolved_math_prioritization')

    def test_partial_history_tail_is_rejected(self):
        (self.q / 'history.jsonl').write_text('{"event":')
        self.reject('History tail incomplete')

    def test_readonly_reviewed_plan_preflight_and_changed_input_rejection(self):
        plan = self.plan()
        self.assertEqual(sync.validate_plan(self.repo, plan)['preflight'], 'PASS')
        self.write_text(self.proof_path, 'Later unaccepted artifact change.\n')
        with self.assertRaisesRegex(sync.Rejected, 'Stale/mismatched'):
            sync.validate_plan(self.repo, plan)

    def test_reviewed_plan_rejects_concurrent_state_change(self):
        plan = self.plan()
        self.write('unsolved_math_prioritization/state.json', {'other': 'changed after review'})
        with self.assertRaisesRegex(sync.Rejected, 'precondition changed'):
            sync.validate_plan(self.repo, plan)

    def test_plan_cannot_silently_add_unrelated_state(self):
        plan = self.plan()
        plan['state_after']['unauthorized'] = {'status': 'queued', 'turns_used': 0}
        plan['state_after_bytes'] = sync.encode(plan['state_after']).decode()
        plan['state_after_sha256'] = sync.sha(plan['state_after_bytes'].encode())
        with self.assertRaisesRegex(sync.Rejected, 'unrelated state'):
            sync.validate_plan(self.repo, plan)

    def test_actual_legacy_eligibility_expression_honors_all_terminal_strings(self):
        tree = ast.parse(LEGACY.read_text())
        rank = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'rank')
        assignment = next(x for x in ast.walk(rank) if isinstance(x, ast.Assign) and any(isinstance(y, ast.Name) and y.id == 'eligible' for y in x.targets))
        code = compile(ast.Expression(assignment.value), str(LEGACY), 'eval')
        for status in sync.TERMINAL:
            self.assertFalse(eval(code, {'a': {'holds': []}, 'local_status': status, 'turns': 1, 'cfg': {'turn_limit': 5}}))
        self.assertTrue(eval(code, {'a': {'holds': []}, 'local_status': 'queued', 'turns': 1, 'cfg': {'turn_limit': 5}}))

    def test_actual_legacy_turn_command_rejects_mirror_without_mutation(self):
        plan = self.plan()
        self.write('unsolved_math_prioritization/state.json', plan['state_after'])
        spec = importlib.util.spec_from_file_location('legacy_queue_offline_audit', LEGACY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.ROOT = self.q
        module.require_cache = lambda: None
        before = (self.q / 'state.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'Start a reviewed attempt'):
            module.record_turn(argparse.Namespace(id='1', note='Unauthorized extra research', outcome='continue'))
        self.assertEqual(before, (self.q / 'state.json').read_bytes())
        self.assertNotIn('unsolved', module.STATES)
        self.assertNotIn('preprint_published', module.STATES)


if __name__ == '__main__':
    unittest.main(verbosity=2)
