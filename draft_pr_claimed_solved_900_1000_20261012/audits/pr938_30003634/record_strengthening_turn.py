#!/usr/bin/env python3
"""Record the two known proof responses using the unmodified queue.py CLI.

Uses a private one-target native slice. It never regenerates the shared queue,
changes another target, resets a counter, or changes the immutable PR snapshot.
The first CLI turn reconciles the preserved historical candidate; the second
records the new strengthening. The resulting selected ledger is public evidence.
"""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

AUDIT = Path(__file__).absolute().parent
REPO = AUDIT.parents[2]
NATIVE = REPO / 'unsolved_math_prioritization'
TARGET = '30003634'
HEAD = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
REVIEW = 'eebfb186fc2eefe2cb9756aec0572e127127fc1be6e248d6abad78a4fe298bd9'
STATEMENT = '2302f06ebd156e0ce9f1728964208380752184dcd932a117b8b397e409c15d6b'
ATTEMPT = AUDIT / 'strengthening/unsolved_math_prioritization/attempts' / TARGET


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    receipt_path = ATTEMPT / 'NATIVE_TURN_RECEIPT.json'
    need(not receipt_path.exists(), 'Already recorded; inspect the existing receipt rather than repeat turns')
    private = AUDIT / 'private/strengthening_turn_native/unsolved_math_prioritization'
    need(not private.exists(), 'Partial/private ledger exists; inspect and resume explicitly, never reset counters')
    before_shared = {name: sha((NATIVE / name).read_bytes()) for name in ['state.json', 'history.jsonl', 'QUEUE.md']}
    original_ledger = AUDIT / 'original/unsolved_math_prioritization/attempts/30003634/original/ATTEMPT_LEDGER.json'
    need(sha(original_ledger.read_bytes()) == '9f9e6e1e907f6616ec2d2ce345019649e69b41f5ea27d6fd305707663f62361d', 'wrong original attempt ledger')
    historical = json.loads(original_ledger.read_bytes())
    need(historical['turns_used'] == 1 and historical['turn_limit'] == 5, 'original accounting changed')
    current_state = json.loads((NATIVE / 'state.json').read_bytes()).get(TARGET)
    need(current_state is None or current_state.get('turns_used', 0) == 0, 'newer selected native attempts require reconciliation')
    previous_state = json.loads(subprocess.check_output(['git', 'show', HEAD + ':unsolved_math_prioritization/state.json'], cwd=REPO)).get(TARGET)
    need(previous_state is None, 'original native state now differs from recorded absence')
    db = sqlite3.connect('file:' + str(NATIVE / 'cache/catalog.sqlite') + '?mode=ro', uri=True)
    selected = db.execute('SELECT payload,report FROM records WHERE key=?', (TARGET,)).fetchone()
    db.close()
    need(selected is not None, 'selected source missing')
    problem, prior_report = map(json.loads, selected)
    need(sha(problem['statement'].encode()) == STATEMENT, 'selected statement changed')
    need(sha(json.dumps([problem, prior_report], sort_keys=True).encode()) == REVIEW, 'selected complete source/prior report changed')
    catalog = next(row for row in json.loads((NATIVE / 'catalog.json').read_bytes()) if row['id'] == TARGET)
    need(catalog['present'] is True and not catalog['holds'] and catalog['review_hash'] == REVIEW, 'selected readiness hold or identity change')
    policy = json.loads((NATIVE / 'policy.json').read_bytes())
    need(policy['turn_limit'] == 5, 'unexpected proof budget')
    review = json.loads((NATIVE / 'assessments.json').read_bytes())[TARGET]
    need(review['review_hash'] == REVIEW, 'stale selected assessment')
    proof = ATTEMPT / 'PROOF.md'
    need(proof.is_file() and proof.stat().st_size > 5000, 'complete new candidate artifact not yet saved')
    private.mkdir(parents=True)
    (private / 'cache').mkdir()
    shutil.copyfile(NATIVE / 'queue.py', private / 'queue.py')
    queue_hash = sha((private / 'queue.py').read_bytes())
    parent_manifest = json.loads((NATIVE / 'manifest.json').read_bytes())
    save(private / 'policy.json', policy)
    save(private / 'assessments.json', {TARGET: review})
    save(private / 'catalog.json', [catalog])
    save(private / 'state.json', {})
    save(private / 'manifest.json', {'revision': parent_manifest['revision'], 'records': 1, 'scope': 'Private isolated selected-record subset, not a full dataset import', 'parent_manifest_sha256': sha((NATIVE / 'manifest.json').read_bytes()), 'selected_review_hash': REVIEW})
    db = sqlite3.connect(private / 'cache/catalog.sqlite')
    db.execute('CREATE TABLE records(key TEXT PRIMARY KEY,payload TEXT,report TEXT)')
    db.execute('INSERT INTO records VALUES(?,?,?)', (TARGET, *selected))
    db.execute('CREATE TABLE metadata(revision TEXT)')
    db.execute('INSERT INTO metadata VALUES(?)', (parent_manifest['revision'],))
    db.commit()
    db.close()
    readiness = {'review_hash': REVIEW, 'exact_claim': 'Original explicit n1/m3 negative answer; current stronger candidate: for every finite k>=1,m>=3, P_m^(k) is not contained in F_1^m, hence the source containment fails for every n>=1.', 'primary_sources': ['https://www.numdam.org/item/10.24033/bsmf.2496.pdf', 'https://math.uchicago.edu/~dannyc/books/scl/scl.pdf', 'https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf', 'https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf'], 'literature_checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'success_test': 'Complete saved deduction and fresh adversarial proof check; no numerical limit extrapolation, no present-open/firstness assumption. Priority and full-package acceptance remain pending.', 'budget': 'Five maximum substantive proof responses. Reconcile the preserved original candidate as turn1, then record the newly proposed strengthening as turn2. No reset; verification is separately0 positive turns.', 'prior_attempt_gap': 'The preserved complete original n1 counterexample already negates the universal question but makes no all-higher-n claim. The quasimorphism/amenable quotient argument is a materially new strengthening and is counted separately.', 'duplicate_check': 'Exact numeric target/source hashes match; selected catalog present and no holds. Initial related-target membership was empty. No other target is researched or mutated.', 'proof_artifact': str(proof), 'prior_candidate_artifact': str(original_ledger.parent / 'PROOF.md'), 'prior_candidate_ledger_sha256': sha(original_ledger.read_bytes()), 'accounting_limit': 'Original state.json has no selected entry;1/5 is the preserved artifact ledger and PR-head queue observation, not an invented historical CLI event.'}
    save(ATTEMPT / 'READINESS.json', readiness)
    commands = [
        ['status', TARGET, 'in_progress', '--note', 'Reconcile preserved PR938 original one-turn candidate into an isolated selected ledger; no new proof response.', '--evidence', str(ATTEMPT / 'READINESS.json')],
        ['turn', TARGET, '--outcome', 'candidate', '--note', 'Historical reconciliation only: original immutable PR938104-letter candidate, original artifact ledger1/5, already independently mathematically audited. This event is recorded now, not backdated.'],
        ['status', TARGET, 'in_progress', '--note', 'New substantive strengthening route within the existing five-turn budget; preserve original turn1.', '--evidence', str(ATTEMPT / 'READINESS.json')],
        ['turn', TARGET, '--outcome', 'candidate', '--note', 'New positive turn2: complete saved quasimorphism/amenable-derived-quotient proof of P_m^(k)notcontainedF1 for every finite k>=1,m>=3. Fresh final adversarial and priority/full-package verification pending.'],
    ]
    calls = []
    for command in commands:
        cp = subprocess.run([sys.executable, '-B', str(private / 'queue.py'), *command], cwd=private.parent, capture_output=True, timeout=90)
        calls.append({'arguments': command, 'returncode': cp.returncode, 'stdout': cp.stdout.decode(), 'stderr': cp.stderr.decode(), 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
        save(private / 'CLI_CALLS.json', calls)
        need(cp.returncode == 0 and not cp.stderr, 'native CLI failed; inspect private calls and state before resuming')
    result = json.loads((private / 'state.json').read_bytes())[TARGET]
    need(result['turns_used'] == result['candidate_turn'] == 2 and result['status'] == 'candidate_result', 'unexpected final attempt accounting')
    events = [json.loads(line) for line in (private / 'history.jsonl').read_text().splitlines()]
    need(len(events) == 4 and [e['turns_used'] for e in events] == [0, 1, 1, 2], 'unexpected actual CLI history')
    after_shared = {name: sha((NATIVE / name).read_bytes()) for name in before_shared}
    need(before_shared == after_shared, 'shared native files changed during accounting; inspect concurrent modification')
    save(ATTEMPT / 'ATTEMPT_LEDGER.json', result)
    (ATTEMPT / 'NATIVE_HISTORY.jsonl').write_bytes((private / 'history.jsonl').read_bytes())
    receipt = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS_NATIVE_QUEUE_CLI_ACCOUNTING', 'target': TARGET, 'unmodified_queue_py_sha256': queue_hash, 'source_statement_hash': STATEMENT, 'source_review_hash': REVIEW, 'private_slice_record_count': 1, 'commands': calls, 'original_native_state': None, 'original_ledger_turns': 1, 'new_positive_research_turns': 1, 'combined_known_turns': 2, 'limit': 5, 'candidate_proof_sha256': sha(proof.read_bytes()), 'shared_native_before_after_sha256': before_shared, 'shared_queue_state_history_unchanged': True, 'no_other_target_processed': True, 'publication_acceptance': False, 'scope': 'Genuine native CLI events in an isolated one-target subset. Turn1reconciles preserved original, turn2new. Does not claim a historical CLI execution or mutate shared main ledger; selected integration remains a later reviewed action.'}
    save(receipt_path, receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
