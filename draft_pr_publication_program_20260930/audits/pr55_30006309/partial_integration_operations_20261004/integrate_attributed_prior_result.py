"""Prospective PR55-only exact merge and current attributed-result mirror.

UNEXECUTED AT SOURCE HANDOFF. ROOT must read all source and author an explicit
scope/adjudication gate after reading the new prior-implication adversary.
Both phases require a real acknowledged exclusive shared-checkout writer
window. This helper does not create a paper, Zenodo record, DOI or tracker row.
Failures retain partial state; no reset, stash, abort, branch switch or force
push is used. An existing attempt directory prevents blind re-execution.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys

HEAD = '85c78d0cf3959d9d492a637cb90835ebc6a0e828'
ID = '30006309'
CODE = 'OWR-14299288-015'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
PREFIX = 'unsolved_math_prioritization/attempts/' + ID
STATE = 'unsolved_math_prioritization/state.json'
HISTORY = 'unsolved_math_prioritization/history.jsonl'
GOAL = Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
GOAL_SHA = '1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04'
PAIR_SHA = '1977a9fb3d6f860866cacdc4293e50016f17c4a3d169701470eb41be8eda7bfd'
HUMAN_PARTIAL_RULE = ('If the result was already_solved or unsolved, audit the findings, and if valid and everything checks out, '
                      'merge the PR as a partial result. Do not make a paper for these.')
CLAIM = ('Verified scoped combinatorial comparison pi D(Q x Delta_(n-1)) = H(Q) for n>=1, '
         'Q Delzant, A=Q intersection Z^n, the smooth complete very ample toric embedding of degree>=2, '
         'with full induced face lattices and imported established GKZ foundations; '
         'accepted as attributed partial progress and a prior-theorem corollary of Esterov2010.')
QUEUE_NOTE = ('Verified scoped comparison in smooth complete very ample Delzant all-lattice-point n>=1 degree>=2 regime; '
              'credited prior-theorem corollary of Esterov2010; exact prior Hurwitz derivation and candidate algorithm priority '
              'unestablished; arbitrary singular/sparse/incomplete and foundation-free cases not certified; accepted partial '
              'attributed progress; full-source/bijection unresolved; AI-assisted, unrefereed; original1/5; no new paper/DOI/tracker')

def sha(b): return hashlib.sha256(b).hexdigest()
def must(ok, msg):
    if not ok: raise RuntimeError(msg)
def jbytes(v): return (json.dumps(v, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['merge', 'mirror'])
    parser.add_argument('--gate', type=Path, required=True)
    parser.add_argument('--exclusive-window-confirmed', action='store_true', required=True)
    parser.add_argument('--root-after-source-reading', action='store_true', required=True)
    args = parser.parse_args()
    must(not sys.flags.optimize and args.exclusive_window_confirmed and args.root_after_source_reading,
         'Nonoptimized ROOT source-reading and confirmed-window invocation required')
    own = Path(__file__).resolve().parent
    audit = own.parent
    repo = own.parents[3]
    phase_dir = own / 'private' / ('integration-' + args.phase)
    must(not phase_dir.exists(), 'Prior attempt exists: inspect its actual state; do not blindly retry')
    phase_dir.mkdir(parents=True)
    (phase_dir / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    commands = []
    def run(argv, allowed=(0,)):
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        child = subprocess.Popen(argv, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = child.communicate()
        number = str(len(commands) + 1)
        (phase_dir / (number + '.stdout')).write_bytes(out)
        (phase_dir / (number + '.stderr')).write_bytes(err)
        commands.append({'argv': argv, 'actual_pid': child.pid, 'started_UTC': start,
                         'finished_UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code': child.returncode,
                         'stdout_sha256': sha(out), 'stderr_sha256': sha(err)})
        (phase_dir / 'COMMANDS.json').write_bytes(jbytes(commands))
        must(child.returncode in allowed, 'Command failed: exact actual streams retained privately')
        return out, child.returncode
    def git(*parts): return run(['git', '--no-optional-locks', *parts])[0]
    def binding(path):
        p = path.resolve()
        p.relative_to(repo)
        return {'path': p.relative_to(repo).as_posix(), 'sha256': sha(p.read_bytes())}
    def checked(b):
        must(set(b) == {'path', 'sha256'}, 'Evidence binding shape differs')
        path = repo / b['path']
        must(not path.is_symlink(), 'Evidence symlink is forbidden')
        p = path.resolve()
        p.relative_to(repo)
        must(p.is_file() and sha(p.read_bytes()) == b['sha256'], 'Bound evidence bytes drifted')
        return p
    gate_path = args.gate.resolve()
    gate_path.relative_to(audit)
    adjudication = json.loads(gate_path.read_bytes())
    gate_pin = binding(gate_path)
    # SOURCE_BINDINGS is an operational input manifest with no decision
    # authority. The separately authored actual ROOT record supplies authority.
    gate = json.loads((own / 'SOURCE_BINDINGS.json').read_bytes())
    inputs_pin = binding(own / 'SOURCE_BINDINGS.json')
    must(gate['schema'] == 'pr55-prospective-partial-operation-source-bindings/v1'
         and gate['ROOT_disposition_authority'] is False and gate['scope_decision'] == gate_pin,
         'Prospective source bindings or actual ROOT gate changed')
    must(gate_path == audit / 'root_goal_resumption_20261004/ROOT_REVIEW_AND_SCOPE_BINDING.json', 'Wrong ROOT decision path')
    must(adjudication['schema'] == 'pr55-root-scientific-and-scope-adjudication/v1'
         and adjudication['PR'] == 55 and adjudication['expected_original_head'] == HEAD, 'Wrong ROOT final gate')
    must(adjudication['root_authorizes_guarded_partial_disposition_under_combined_scope'] is True
         and adjudication['root_personally_read_fresh_report_and_verdict_in_full'] is True
         and adjudication['root_personally_rechecked_original_candidate_and_two_universal_proof_families'] is True
         and adjudication['root_personally_read_both_prior_derivations'] is True, 'ROOT current reading/adjudication missing')
    must(adjudication['scoped_mathematics_verified'] is True
         and adjudication['root_scientific_verdict'] == 'sound_scoped_comparison_already_implied_by_prior_machinery'
         and adjudication['audited_outcome'] == 'already_solved', 'Scoped mathematics/prior implication differs')
    must(adjudication['scope'] == 'n>=1; smooth polarized toric variety; complete very ample embedding by all lattice points of a Delzant polytope; degree>=2; full induced face lattices and massive boundary convention'
         and adjudication['full_source_solved'] is False, 'Narrow scope/full-source limitation differs')
    must(adjudication['eligible_intake_literal_status'] == 'claimed_solved'
         and adjudication['goal_objective_sha256'] == GOAL_SHA
         and sha(GOAL.read_bytes()) == GOAL_SHA, 'Current intake/goal binding differs')
    must(adjudication['original_human_outcome_instruction'] == HUMAN_PARTIAL_RULE
         and 'the goal file itself does not contain that partial-outcome clause' in adjudication['root_scope_interpretation']
         and adjudication['never_process_initially_nonclaimed_PRs'] is True,
         'Combined interpretation must distinguish narrower intake from original human outcome rule')
    for key in ('PR50_exception_extended', 'prepare_paper', 'Zenodo_upload', 'tracker_append',
                'exact_earlier_printed_hurwitz_proof_located', 'new_solution_priority_clearance', 'formal_or_human_refereed_certification'):
        must(adjudication[key] is False, 'Excluded publication/priority/certification flag differs: ' + key)
    must(adjudication['new_DOI'] is None and adjudication['candidate_method_originality'] == 'unestablished'
         and adjudication['new_central_proof_attempts'] == 0 and adjudication['preserve_original_ledger_turns_used'] == 1,
         'Publication/method priority/budget differs')
    for key in ('preserve_original_scientific_bodies_as_dated_inputs', 'fresh_current_acceptance_required',
                'raw_report_absent_SQL_report_nonNULL_empty_object_wrapper_null_distinguished',
                'fresh_exact_head_eligibility_required_before_merge', 'actual_exclusive_writer_ack_required_before_Git_mutation'):
        must(adjudication[key] is True, 'Current source/eligibility/preservation guard missing: ' + key)
    must(adjudication['native_Git_PR_mutation_performed_by_this_record'] is False,
         'ROOT decision must not be confused with a native execution receipt')
    auth_path = checked(gate['original_authentication'])
    must(auth_path == audit / 'original_preparation_family/ORIGINAL_AUTHENTICATION.json', 'Wrong original authentication')
    auth = json.loads(auth_path.read_bytes())
    originals = auth['original_science_files']
    must(auth['original_head'] == HEAD and len(originals) == 16 and auth['complete_diff_file_count'] == 17, 'Original domain differs')
    custody = checked(gate['original_custody'])
    current_custody = checked(gate['current_SOURCE_custody'])
    must(custody == audit / 'original_preparation_family/SELF_MANIFEST.json'
         and current_custody == audit / 'current_preparation_family/MANIFEST.json', 'Wrong source custody families')
    prior_path = checked(gate['prior_specialization'])
    must(prior_path == audit / 'current_preparation_family/science/PRIOR_ART_SPECIALIZATION.md', 'Wrong attributed specialization')
    fresh_verdict = checked(gate['fresh_prior_implication_verdict'])
    fresh_report = checked(gate['fresh_prior_implication_report'])
    fresh_custody = checked(gate['fresh_prior_implication_custody'])
    must(fresh_verdict.parent == fresh_report.parent == audit / 'prior_implication_fresh_adversary_20261004',
         'New independent prior-implication family differs')
    fresh = json.loads(fresh_verdict.read_bytes())
    must(fresh['schema'] == 'pr55-fresh-independent-prior-implication-adversary/v1'
         and fresh['head_parent_bound'] == HEAD and fresh['verdict'] == 'PRIOR_IMPLICATION_VERIFIED_IN_EXACT_RESTORED_SMOOTH_MODEL_REGIME'
         and fresh['substantive_mathematical_defect_within_scope'] is False and fresh['target_sized_unsupported_step'] is False,
         'Actual fresh prior-implication verdict differs')
    reviews = gate['mathematical_reviews']
    must(len(reviews) >= 2 and len({checked(p).parent for p in reviews}) == len(reviews),
         'At least two distinct reviewed mathematical families required')
    evidence = ([gate[k] for k in ('scope_decision', 'original_authentication', 'original_custody', 'current_SOURCE_custody',
                                 'prior_specialization', 'fresh_prior_implication_verdict', 'fresh_prior_implication_report',
                                 'fresh_prior_implication_custody')]
                + reviews)
    # Hashing complete custody members verifies immutability, not mathematical
    # truth or personal reading. ROOT's separate adjudication is required above.
    for item in json.loads(custody.read_bytes())['files']:
        p = Path(item['path'])
        p.resolve().relative_to(audit / 'original_preparation_family')
        must(not p.is_symlink() and p.is_file() and len(p.read_bytes()) == item['bytes']
             and sha(p.read_bytes()) == item['sha256'] and stat.S_IMODE(p.stat().st_mode) == item['mode'], 'Original custody member drifted')
    for item in json.loads(current_custody.read_bytes())['files']:
        if item['path'] == 'MANIFEST.json':
            must(item['sha256'] == 'LITERAL_SELF_REFERENCE_NOT_A_DIGEST', 'Current custody self-reference differs')
            continue
        p = current_custody.parent / item['path']
        p.resolve().relative_to(current_custody.parent)
        must(not p.is_symlink() and p.is_file() and len(p.read_bytes()) == item['bytes']
             and sha(p.read_bytes()) == item['sha256'] and format(stat.S_IMODE(p.stat().st_mode), '04o') == item['mode'],
             'Current SOURCE custody member drifted')
    must(fresh_custody == fresh_report.parent / 'SELF_MANIFEST.json', 'Wrong fresh review custody')
    for item in json.loads(fresh_custody.read_bytes())['files']:
        p = Path(item['path'])
        p.resolve().relative_to(fresh_custody.parent)
        must(not p.is_symlink() and p.is_file() and len(p.read_bytes()) == item['bytes']
             and sha(p.read_bytes()) == item['sha256'], 'Fresh review custody member drifted')
    source = json.loads((audit / 'original_preparation_family/original/source_record.json').read_bytes())
    must(source['problem']['id'] == int(ID) and source['problem']['problem_number'] == CODE
         and 'upstream_report' in source and source['upstream_report'] is None, 'Original source wrapper differs')
    original_paths = {p['repository_path'] for p in originals}
    mirror_paths = {PREFIX + '/acceptance.json', PREFIX + '/CURRENT_RESULT.md', PREFIX + '/CURRENT_PRIORITY_SPECIALIZATION.md', STATE, HISTORY}
    owned_paths = original_paths | {QUEUE} if args.phase == 'merge' else mirror_paths
    owned_bytes = {p.encode() for p in owned_paths}
    def committed_originals(commit):
        for item in originals:
            path = item['repository_path']
            must(sha(git('show', commit + ':' + path)) == item['sha256'], 'Committed original body differs')
            tree = git('ls-tree', commit, '--', path).decode().split()
            must(tree[0] == item['git_mode'] and tree[2] == item['git_blob_sha1'], 'Committed original mode/blob differs')
    def foreign_index():
        return b'\0'.join(e for e in git('ls-files', '--stage', '-z').split(b'\0')
                          if e and e.split(b'\t', 1)[1] not in owned_bytes)
    def foreign_dirty_paths():
        return {p.decode() for p in git('diff', '--name-only', '-z').split(b'\0') if p and p not in owned_bytes}
    def body_state(path):
        p = repo / path
        if not p.exists() and not p.is_symlink(): return {'exists': False}
        mode = p.lstat().st_mode
        must(stat.S_ISREG(mode), 'Foreign dirty nonregular path: inspect without changing it')
        return {'exists': True, 'mode': mode, 'sha256': sha(p.read_bytes())}
    must(git('branch', '--show-current').strip() == b'main', 'Stay on main')
    must(not git('diff', '--cached', '--name-only', '-z'), 'Entire real index must be empty; preserve foreign staging')
    merge_head = Path(git('rev-parse', '--git-path', 'MERGE_HEAD').decode().strip())
    if not merge_head.is_absolute(): merge_head = repo / merge_head
    must(not merge_head.exists(), 'Another merge exists; preserve its state')
    base = git('rev-parse', 'HEAD').decode().strip()
    must(git('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == base, 'Main/remote baseline differs')
    valid_pause_bases = {base}
    if args.phase == 'mirror':
        prior_merge = json.loads((own / 'NATIVE_MERGE_RESULT.json').read_bytes())
        must(prior_merge['schema'] == 'pr55-attributed-prior-result-native-merge/v1' and prior_merge['submitted_head'] == HEAD
             and prior_merge['merge_commit'] == base and prior_merge['gate'] == gate_pin, 'Actual previous merge identity differs')
        must(git('show', '-s', '--format=%P', base).decode().strip().split() == [prior_merge['base'], HEAD],
             'Continuous writer window lacks the exact two-parent transition')
        valid_pause_bases.add(prior_merge['base'])
    window_path = repo / 'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
    def check_window():
        window = json.loads(window_path.read_bytes())
        must(window['shared_git_writes_paused'] is True and 'PR55' in window['paused_for'], 'No real acknowledged PR55 writer window')
        must(window['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True
             and window['all_staged_path_count'] == 0 and not window['owned_staged_paths'],
             'Acknowledged foreign-body freeze and empty shared index are required')
        must(window['local_main_at_pause'] == window['remote_main_at_pause']
             and window['local_main_at_pause'] in valid_pause_bases, 'Writer-window baseline differs from actual phase or exact merge parent')
        return window
    window = check_window()
    window_pin = binding(window_path)
    (phase_dir / 'ACKNOWLEDGED_WINDOW.json').write_bytes(jbytes(window))
    foreign_stage = foreign_index()
    foreign_dirty = foreign_dirty_paths()
    foreign_bodies = {p: body_state(p) for p in foreign_dirty}
    def preserve():
        check_window()
        must(foreign_index() == foreign_stage, 'Foreign index changed')
        must(foreign_dirty_paths() == foreign_dirty and all(body_state(p) == b for p, b in foreign_bodies.items()),
             'Foreign dirty path set/body/mode changed')
        for b in evidence: checked(b)
        checked(inputs_pin)
        must(binding(gate_path) == gate_pin and sha(GOAL.read_bytes()) == GOAL_SHA, 'ROOT gate/goal changed')
    def source_identity():
        manifest = json.loads((repo / 'unsolved_math_prioritization/manifest.json').read_bytes())
        must(manifest['revision'] == source['dataset_revision'], 'Current source revision differs from original wrapper')
        for name in ('problems.json', 'research_results.json'):
            p = repo / 'unsolved_math_prioritization/cache' / name
            b = p.read_bytes()
            must({'bytes': len(b), 'sha256': sha(b)} == manifest['files'][name], 'Raw corpus no longer matches its manifest')
        raw = json.loads((repo / 'unsolved_math_prioritization/cache/problems.json').read_bytes())
        matches = [p for p in raw if str(p['id']) == ID]
        must(len(matches) == 1 and matches[0] == source['problem'], 'Selected raw typed problem differs')
        reports = json.loads((repo / 'unsolved_math_prioritization/cache/research_results.json').read_bytes())
        must(CODE not in reports, 'Raw selected report key is no longer ABSENT')
        with sqlite3.connect('file:' + str(repo / 'unsolved_math_prioritization/cache/catalog.sqlite') + '?mode=ro', uri=True) as db:
            row = db.execute('SELECT payload,report FROM records WHERE key=?', (ID,)).fetchone()
            revision = db.execute('SELECT revision FROM metadata').fetchall()
        must(row is not None and json.loads(row[0]) == source['problem'], 'SQL selected typed problem differs')
        must(row[1] is not None and row[1] == '{}' and json.loads(row[1]) == {}, 'SQL fallback is no longer non-NULL TEXT {}')
        must(revision == [(manifest['revision'],)], 'SQL revision differs')
        pair = sha(json.dumps([source['problem'], {}], sort_keys=True).encode())
        must(pair == PAIR_SHA, 'Current selected SQL typed-pair hash differs')
        selected = [p for p in json.loads((repo / 'unsolved_math_prioritization/catalog.json').read_bytes()) if p['id'] == ID]
        must(len(selected) == 1 and selected[0]['review_hash'] == pair, 'Selected catalog source fingerprint differs')
        return {'raw_problem_equals_original_and_SQL': True, 'raw_report_key_present': False, 'raw_report': 'ABSENT; no raw value',
                'SQL_report_is_NULL': False, 'SQL_report_literal': '{}', 'original_wrapper_upstream_report': None,
                'review_hash': pair, 'review_hash_uses': 'Current SQL typed pair [problem, {}]; wrapper null is not the SQL report.',
                'wrapper_pair_hash': sha(json.dumps([source['problem'], None], sort_keys=True).encode()),
                'original_readiness_review_hash_present': 'review_hash' in json.loads((audit / 'original_preparation_family/original/readiness.json').read_bytes()),
                'dataset_revision': manifest['revision'], 'raw_corpus_manifest': binding(repo / 'unsolved_math_prioritization/manifest.json')}
    identity = source_identity()
    preserve()
    pr = json.loads(run(['gh', 'pr', 'view', '55', '--repo', 'AlecKriebel/Math', '--json',
                         'number,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,url'])[0])
    must(pr['number'] == 55 and pr['headRefOid'] == HEAD and pr['headRefName'] == 'dot/math-' + ID
         and pr['baseRefName'] == 'main', 'Current PR identity differs')
    api_queue = json.loads(run(['gh', 'api', 'repos/AlecKriebel/Math/contents/' + QUEUE + '?ref=' + HEAD])[0])
    submitted_queue = base64.b64decode(api_queue['content'])
    blob = hashlib.sha1(b'blob ' + str(len(submitted_queue)).encode() + b'\0' + submitted_queue).hexdigest()
    must(blob == api_queue['sha'] == auth['original_queue_destination_blob_sha1'], 'Fresh submitted queue blob differs')
    rows = [line for line in submitted_queue.decode().splitlines() if '| ' + ID + ' /' in line]
    must(len(rows) == 1 and rows[0].split('|')[8].strip() == 'claimed_solved'
         and rows[0].split('|')[9].strip() == '1/5', 'Fresh literal intake eligibility changed')
    _, availability = run(['git', '--no-optional-locks', 'cat-file', '-e', HEAD + '^{commit}'], allowed=(0,128))
    if availability != 0:
        must(args.phase == 'merge', 'Previous merge object disappeared: inspect')
        preserve()
        # Object-only import inside the genuine writer window. No branch/ref
        # destination and no FETCH_HEAD write; current PR head is rechecked.
        git('fetch', '--no-tags', '--no-write-fetch-head', 'origin', 'refs/pull/55/head')
        git('cat-file', '-e', HEAD + '^{commit}')
        reread = json.loads(run(['gh', 'pr', 'view', '55', '--repo', 'AlecKriebel/Math', '--json', 'headRefOid,state,isDraft'])[0])
        must(reread['headRefOid'] == HEAD and reread['state'] == 'OPEN' and reread['isDraft'] is True, 'PR drifted during object import')
    committed_originals(HEAD)
    status = json.loads(git('show', HEAD + ':' + PREFIX + '/status.json'))
    ledger = git('show', HEAD + ':' + PREFIX + '/turns.jsonl')
    must(status['turns_used'] == 1 and status['turn_limit'] == 5 and len(ledger.splitlines()) == 1
         and json.loads(ledger)['turn'] == 1, 'Original sole 1/5 attempt changed')
    queue_before = (repo / QUEUE).read_bytes()
    must(queue_before == git('show', base + ':' + QUEUE), 'Native queue has uncommitted foreign changes')
    if args.phase == 'merge':
        must(pr['state'] == 'OPEN' and pr['isDraft'] is True, 'Original open draft required')
        incoming = json.loads(run(['gh', 'api', 'repos/AlecKriebel/Math/pulls/55/files?per_page=100'])[0])
        must(len(incoming) == 17 and {p['filename'] for p in incoming} == owned_paths, 'Current incoming GitHub domain differs')
        common = git('merge-base', base, HEAD).decode().strip()
        must({p.decode() for p in git('diff', '--name-only', '-z', common, HEAD).split(b'\0') if p} == owned_paths,
             'Local exact-head incoming scope differs')
        for p in original_paths:
            must(not (repo / p).exists() and not (repo / p).is_symlink(), 'An original native path already exists')
        lines = queue_before.decode().splitlines(keepends=True)
        indexes = [i for i, line in enumerate(lines) if '| ' + ID + ' /' in line]
        must(len(indexes) == 1, 'Native target row not unique')
        i = indexes[0]
        cells = lines[i].split('|')
        must(len(cells) == 14 and cells[8].strip() == 'queued' and cells[9].strip() == '0/5' and not cells[12].strip(),
             'Native target queue baseline differs')
        cells[8] = ' already_solved '
        cells[9] = ' 1/5 '
        cells[11] = ' ' + QUEUE_NOTE + ' '
        lines[i] = '|'.join(cells)
        accepted_queue = ''.join(lines).encode()
        must(git('rev-parse', 'HEAD').decode().strip() == base, 'Main moved before merge')
        preserve()
        _, merge_exit = run(['git', '--no-optional-locks', 'merge', '--no-ff', '--no-commit', HEAD], allowed=(0,1))
        conflicts = {p.decode() for p in git('diff', '--name-only', '--diff-filter=U', '-z').split(b'\0') if p}
        must(conflicts <= {QUEUE} and merge_head.read_text().strip() == HEAD, 'Unexpected conflict/parent: inspect retained partial merge')
        preserve()
        (repo / QUEUE).write_bytes(accepted_queue)
        for item in originals:
            p = repo / item['repository_path']
            must(sha(p.read_bytes()) == item['sha256'] and stat.S_IMODE(p.stat().st_mode) == 0o644,
                 'Imported original body or working mode differs')
        git('add', '--', QUEUE)
        must(not git('diff', '--name-only', '--diff-filter=U', '-z'), 'Unresolved conflicts remain')
        must({p.decode() for p in git('diff', '--cached', '--name-only', '-z').split(b'\0') if p} == owned_paths, 'Merge staged domain differs')
        preserve()
        git('commit', '-m', 'Accept PR55 scoped comparison as attributed prior-theorem corollary')
        commit = git('rev-parse', 'HEAD').decode().strip()
        must(git('show', '-s', '--format=%P', commit).decode().strip().split() == [base, HEAD], 'Exact two-parent merge differs')
        must((repo / QUEUE).read_bytes() == accepted_queue, 'Accepted queue bytes differ')
        must({p.decode() for p in git('diff', '--name-only', '-z', base, commit).split(b'\0') if p} == owned_paths, 'Committed merge domain differs')
        committed_originals(commit)
        must(not git('diff', '--cached', '--name-only', '-z'), 'Index is not empty after merge commit')
        preserve()
        git('push', 'origin', 'main')
        must(git('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == commit, 'Actual merge push readback differs')
        preserve()
        receipt = {'schema': 'pr55-attributed-prior-result-native-merge/v1', 'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
                   'actual_pid': os.getpid(), 'base': base, 'submitted_head': HEAD, 'merge_commit': commit, 'remote_main': commit,
                   'gate': gate_pin, 'operative_source_bindings': inputs_pin,
                   'acknowledged_shared_writer_window': window_pin, 'merge_exit_code': merge_exit,
                   'conflicts': sorted(conflicts), 'all_16_original_bodies_modes_blobs_unchanged': True,
                   'queue_only_target_status_turns_note_changed': True, 'queue_publication_DOI_cell_empty': True,
                   'foreign_dirty_path_set_bodies_modes_and_index_unchanged': True, 'native_mirror_pending': True,
                   'current_source_identity': identity, 'original_budget': '1/5', 'new_central_proof_attempts': 0,
                   'new_paper': False, 'Zenodo_upload': False, 'new_publication_DOI': False, 'tracker_row': False,
                   'GitHub_merged_readback_not_yet_asserted': True}
        out = own / 'NATIVE_MERGE_RESULT.json'
    else:
        must(pr['state'] == 'MERGED' and pr['mergeCommit']['oid'] == base, 'GitHub has not confirmed exact merge: do not infer from push')
        committed_originals(base)
        state_before = (repo / STATE).read_bytes()
        history_before = (repo / HISTORY).read_bytes()
        must(state_before == git('show', base + ':' + STATE) and history_before == git('show', base + ':' + HISTORY),
             'Native state/history contain uncommitted foreign changes')
        state = json.loads(state_before)
        must(ID not in state and all(str(json.loads(s).get('id')) != ID for s in history_before.splitlines()),
             'Prior target mirror exists: do not duplicate')
        must(history_before.endswith(b'\n'), 'History has an incomplete last line')
        for p in mirror_paths - {STATE, HISTORY}:
            must(not (repo / p).exists() and not (repo / p).is_symlink(), 'Current native acceptance destination already exists')
        target = [line for line in queue_before.decode().splitlines() if '| ' + ID + ' /' in line]
        must(len(target) == 1 and target[0].split('|')[8].strip() == 'already_solved'
             and target[0].split('|')[9].strip() == '1/5' and target[0].split('|')[11].strip() == QUEUE_NOTE
             and not target[0].split('|')[12].strip(), 'Exact accepted native target queue row differs')
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        specialization = ('# Current credited prior-theorem deduction — PR55\n\n'
                          'This is the current accepted supporting deduction for the scoped prior-theorem corollary. '
                          'ROOT adjudicated it after the fresh independent prior-implication review. '
                          'Its source is the exact frozen preparation specialization bound in acceptance.json; the dated SOURCE packet '
                          'remains unchanged and confers no native authority on its own. The accepted scope is the smooth complete '
                          'very ample Delzant all-lattice-point n>=1 degree>=2 regime. The introductory arbitrary-A notation in OWR '
                          'does not certify singular, sparse, incomplete or foundation-free extensions. The stronger combinatorial '
                          'one-to-one correspondence request is also not certified. Esterov2010 is credited as '
                          'the earlier sufficient theorem; no exact printed prior Hurwitz derivation or identical algorithm priority '
                          'is claimed. Its DOI below is a literature citation, not a new publication DOI for this project.\n\n'
                          '---\n\n').encode() + prior_path.read_bytes()
        (repo / (PREFIX + '/CURRENT_PRIORITY_SPECIALIZATION.md')).write_bytes(specialization)
        acceptance = {'schema': 'pr55-current-attributed-prior-result-acceptance/v1', 'at': now, 'actual_author_pid': os.getpid(),
                      'problem_id': ID, 'problem_code': CODE, 'pr': 55, 'reviewed_head': HEAD, 'merge_commit': base,
                      'merged_at': pr['mergedAt'], 'outcome': 'already_solved_scoped_prior_theorem_corollary_accepted_partial',
                      'status': 'already_solved', 'accepted_as': 'partial_attributed_prior_theorem_corollary', 'exact_scope': CLAIM,
                      'full_source_solved': False, 'broader_combinatorial_bijection_certified': False,
                      'final_gate': gate_pin, 'scope_decision': gate['scope_decision'], 'original_authentication': gate['original_authentication'],
                      'operative_source_bindings': inputs_pin,
                      'original_custody': gate['original_custody'], 'current_SOURCE_custody': gate['current_SOURCE_custody'],
                      'mathematical_reviews': reviews, 'fresh_prior_implication_verdict': gate['fresh_prior_implication_verdict'],
                      'fresh_prior_implication_report': gate['fresh_prior_implication_report'], 'frozen_prior_specialization': gate['prior_specialization'],
                      'current_priority_specialization': binding(repo / (PREFIX + '/CURRENT_PRIORITY_SPECIALIZATION.md')),
                      'current_source_identity': identity, 'original_scientific_files_are_dated_inputs': True,
                      'original_budget': '1/5', 'original_turn_ledger': binding(repo / (PREFIX + '/turns.jsonl')),
                      'new_central_proof_attempts': 0, 'new_paper': False, 'Zenodo_upload': False, 'new_publication_DOI': False,
                      'tracker_row': False, 'prior_theorem': {'author': 'Alexander Esterov', 'year': 2010,
                      'arXiv': '0810.4996v3', 'journal_DOI_citation_only': '10.1007/s00454-010-9242-7'},
                      'earlier_exact_Hurwitz_derivation_located': False, 'identical_candidate_algorithm_priority_certified': False,
                      'arbitrary_singular_sparse_incomplete_scope_certified': False, 'global_novelty_certified': False,
                      'AI_tools_used_extensively': True, 'human_peer_review': False, 'formal_proof_certification': False,
                      'native_status_is_present_day_mirror': True, 'historical_lifecycle_transitions_reconstructed': False}
        (repo / (PREFIX + '/acceptance.json')).write_bytes(jbytes(acceptance))
        current = ('# Accepted current result — PR55 / ' + CODE + '\n\n'
                   'Accepted as **verified scoped comparison; prior-theorem corollary**, categorized `already_solved` and retained '
                   'as attributed partial progress.\n\n' + CLAIM + '\n\n'
                   'The exact source asks for a combinatorial reproof of a known equality. The accepted proof retains the '
                   'cited Sano smooth complete very ample Delzant, full lattice-point, degree-at-least-two setting. OWR’s terse '
                   'introductory arbitrary-configuration notation is not certified here as a singular, sparse, incomplete, '
                   'lattice-index-defective, degree-one or foundation-free theorem. The stronger one-to-one correspondence '
                   'request in Ogusu–Sano Conjecture4.5 is not certified; only the hull equality is accepted. '
                   'Accordingly full_source_solved=false.\n\n'
                   'Esterov’s 2010 general Newton formula implies this scoped comparison by the explicitly checked specialization '
                   'in CURRENT_PRIORITY_SPECIALIZATION.md. The earlier theorem and the newly written target-specific deduction '
                   'are distinguished. No literal earlier Hurwitz derivation, identical candidate algorithm, earliest recognition, '
                   'global novelty or comprehensive absence finding is claimed. The old candidate’s direct presentation remains '
                   'useful verified exposition; it is not accepted as a novel resolution of a genuinely open problem.\n\n'
                   'The sixteen original scientific files from head `' + HEAD + '` retain their exact bodies, modes and blobs '
                   'as dated inputs. Their claimed_solved/full_source_solved assertions and dated open triage do not govern present '
                   'acceptance. The frozen corrected SOURCE packet’s approval-false/prospective handoff statements remain truthful '
                   'historical statements in that packet and have not been copied as present native authority. acceptance.json '
                   'binds the actual ROOT decision, current reviews, prior deduction, original source custody and GitHub exact-head '
                   'merge.\n\n'
                   'The raw upstream report key is absent; the selected SQL fallback is non-NULL text `{}`; the original wrapper '
                   'contains a JSON null placeholder. These are distinct facts. The current native review_hash uses `[problem, {}]`, '
                   'and no raw null or fictional prior report is inferred. Original substantive attempts stay 1/5; verification '
                   'and source-priority audits add no central proof-attempt turn.\n\n'
                   'No new paper, Zenodo upload, publication DOI or spreadsheet row accompanies this partial/prior-result acceptance. '
                   'Any DOI in the credited deduction is an earlier literature citation. AI tools were used extensively; the work '
                   'is unrefereed and has no conventional human peer-review or formal proof-assistant certification. State and '
                   'history contain one present-day acceptance mirror, without replaying historical lifecycle events.\n')
        (repo / (PREFIX + '/CURRENT_RESULT.md')).write_text(current)
        js = lambda v: json.dumps(v, sort_keys=True).encode()
        p = source['problem']
        event = {'at': now, 'event': 'acceptance_mirror_import', 'id': ID, 'pr': 55, 'status': 'already_solved',
                 'turns_used': 1, 'turn_limit': 5, 'review_hash': identity['review_hash'], 'source_record_hash': sha(js(p)),
                 'source_report_hash': sha(js({})), 'statement_hash': sha(p['statement'].encode()),
                 'note': QUEUE_NOTE, 'evidence': {'import_is_present_day_mirror': True, 'historical_transitions_asserted': False,
                 'reviewed_head': HEAD, 'canonical_acceptance': binding(repo / (PREFIX + '/acceptance.json')),
                 'original_budget_ledger': binding(repo / (PREFIX + '/turns.jsonl')), 'queue_explicit_budget': '1/5',
                 'current_source_identity': identity, 'final_gate': gate_pin, 'scope_decision': gate['scope_decision'],
                 'merge_commit': base, 'accepted_as': 'partial_attributed_prior_theorem_corollary',
                 'full_source_solved': False, 'broader_combinatorial_bijection_certified': False,
                 'new_paper': False, 'Zenodo_upload': False, 'new_publication_DOI': False, 'tracker_row': False}}
        event['event_id'] = sha(js(event))
        state[ID] = event
        (repo / STATE).write_bytes(jbytes(state))
        (repo / HISTORY).write_bytes(history_before + json.dumps(event, ensure_ascii=False, sort_keys=True).encode() + b'\n')
        must({k: v for k, v in json.loads((repo / STATE).read_bytes()).items() if k != ID} == json.loads(state_before), 'Other native states changed')
        must((repo / HISTORY).read_bytes().startswith(history_before)
             and len((repo / HISTORY).read_bytes()[len(history_before):].splitlines()) == 1, 'History prefix/event count differs')
        must((repo / QUEUE).read_bytes() == queue_before, 'Mirror changed native queue')
        must(git('rev-parse', 'HEAD').decode().strip() == base, 'Main moved before mirror staging')
        preserve()
        git('add', '--', *sorted(mirror_paths))
        must({p.decode() for p in git('diff', '--cached', '--name-only', '-z').split(b'\0') if p} == mirror_paths, 'Mirror staged domain differs')
        preserve()
        git('commit', '-m', 'Bind PR55 attributed scoped prior-result acceptance to exact merge and reviews')
        commit = git('rev-parse', 'HEAD').decode().strip()
        must(git('show', '-s', '--format=%P', commit).decode().strip() == base, 'Acceptance administrative parent differs')
        must({p.decode() for p in git('diff', '--name-only', '-z', base, commit).split(b'\0') if p} == mirror_paths, 'Committed mirror domain differs')
        committed_originals(commit)
        must(not git('diff', '--cached', '--name-only', '-z'), 'Index is not empty after acceptance commit')
        preserve()
        git('push', 'origin', 'main')
        must(git('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == commit, 'Actual acceptance push readback differs')
        preserve()
        receipt = {'schema': 'pr55-attributed-prior-result-native-mirror/v1', 'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
                   'actual_pid': os.getpid(), 'merge_commit': base, 'acceptance_commit': commit, 'remote_main': commit,
                   'gate': gate_pin, 'operative_source_bindings': inputs_pin,
                   'event_id': event['event_id'], 'acknowledged_shared_writer_window': window_pin,
                   'current_source_identity': identity, 'other_native_states_and_history_prefix_preserved': True,
                   'exactly_one_present_day_acceptance_event': True, 'foreign_dirty_path_set_bodies_modes_and_index_unchanged': True,
                   'all_16_original_bodies_modes_blobs_unchanged': True, 'queue_DOI_cell_empty': True,
                   'original_budget': '1/5', 'new_central_proof_attempts': 0,
                   'full_source_solved': False, 'broader_combinatorial_bijection_certified': False,
                   'new_paper': False, 'Zenodo_upload': False, 'new_publication_DOI': False, 'tracker_row': False,
                   'program_completion_not_conferred': True}
        out = own / 'NATIVE_ACCEPTANCE_RESULT.json'
    committed_originals(commit)
    must(not git('diff', '--cached', '--name-only', '-z'), 'Entire real index must be empty after phase')
    must(not out.exists(), 'Actual receipt already exists; preserve it')
    with out.open('x') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__': main()
