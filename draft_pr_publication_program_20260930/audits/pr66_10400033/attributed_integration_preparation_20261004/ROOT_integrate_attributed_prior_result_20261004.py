"""ROOT-only sequential native integration; preparation does not authorize execution.

Invoke python3 -E -B this_file.py merge, then mirror after independent merge
readback. An existing final scientific gate and fresh other-writer freeze are
mandatory. Failure preserves partial state for inspection; no rollback occurs.
"""
from pathlib import Path
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import sqlite3
import stat
import subprocess
import sys

PREP = Path(__file__).resolve().parent
A = PREP.parent
P = A.parents[1]
R = P.parent
HEAD = '78f4a7fadac0fd24e147a617956cb409eb6a579e'
ID = '10400033'
CODE = 'AMR-103-0033'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
PREFIX = 'unsolved_math_prioritization/attempts/' + ID
STATE = 'unsolved_math_prioritization/state.json'
HISTORY = 'unsolved_math_prioritization/history.jsonl'
GOAL = Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
GOAL_SHA = '1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04'
PAUSE = 'PR66 attributed prior-result integration 20261004'
NOTE = 'Verified classical Willerton crossing bound and even estimate; original target already implied by Fiedler-Stoimenow dated 2002 author body, binomial bound and vt3=4v3; even estimate also follows from prior FS formula and Stoimenow2003 even-valence lemma; earlier explicit even formula not located; exact2000 printed body and stronger p8 extremality not certified; tournament mechanism novelty unestablished; accepted attributed progress; AI-assisted unrefereed; original1/5; no new paper/DOI/tracker'

def sha(b): return hashlib.sha256(b).hexdigest()
def jb(v): return (json.dumps(v, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def same(a, b): return canonical(a) == canonical(b)
def must(ok, msg):
    if not ok: raise RuntimeError(msg)
def utc(value):
    d = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    must(d.tzinfo is not None, 'Timestamp must specify timezone')
    return d.astimezone(dt.timezone.utc)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=['merge', 'mirror'])
    args = ap.parse_args()
    must(not sys.flags.optimize and __debug__ and sys.flags.ignore_environment and sys.flags.dont_write_bytecode, 'Invoke -E -B without optimization')
    O = PREP / 'native_attributed_result_operations_20261004'
    O.mkdir(exist_ok=True)
    D = O / ('actual_' + args.phase + '_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    D.mkdir(exist_ok=False)
    (D / 'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    commands = []
    def run(argv, allowed=(0,)):
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = child.communicate()
        n = str(len(commands) + 1)
        row = {'argv':argv, 'cwd':str(R), 'actual_child_pid':child.pid,
               'started_utc':started, 'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code':child.returncode}
        for key, body in [('stdout', out), ('stderr', err)]:
            path = D / (n + '.' + key); path.write_bytes(body)
            row[key] = {'path':str(path), 'bytes':len(body), 'sha256':sha(body)}
        commands.append(row); (D / 'ACTUAL_COMMANDS.json').write_bytes(jb(commands))
        must(child.returncode in allowed, 'Operation failed; preserve partial state and inspect actual streams')
        return out, child.returncode
    def git(*parts): return run(['git', '--no-optional-locks', *parts])[0]
    def pin(path):
        must(not path.is_symlink() and path.is_file(), 'Evidence must be regular and present')
        return {'path':str(path.relative_to(R)), 'bytes':len(path.read_bytes()), 'sha256':sha(path.read_bytes())}
    def check_pin(row):
        path = R / row['path']; path.resolve().relative_to(R)
        must(pin(path) == row, 'Reviewed evidence drift: ' + row['path'])
    G = A / 'ROOT_FINAL_PRIOR_DISPOSITION_20261004.json'
    gate = json.loads(G.read_bytes()); gate_pin = pin(G)
    must(gate['PR'] == 66 and gate['expected_original_head'] == HEAD, 'Final ROOT disposition identity differs')
    for key in ['ROOT_authorizes_guarded_attributed_prior_result_acceptance', 'fresh_final_adversary_clean',
                'ROOT_personally_read_all_required_reports', 'candidate_mathematics_verified',
                'prior_resolution_of_exact_original_problem_verified', 'ROOT_reviewed_exact_operational_byte_plan',
                'initial_literal_claimed_solved_gate_only', 'initially_nonclaim_targets_untouched', 'even_prior_ingredient_verified']:
        must(gate[key] is True, 'Final ROOT gate not satisfied: ' + key)
    must(type(gate['mathematics_percent']) is int and gate['mathematics_percent'] == 100 and
         type(gate['bounded_priority_percent']) is int and gate['bounded_priority_percent'] == 100, 'Scientific review incomplete')
    must(gate['audited_outcome'] == 'already_solved' and gate['accepted_as'] == 'attributed_partial_prior_result', 'Current scientific meaning differs')
    must(gate['original_proof_turns'] == '1/5' and type(gate['new_original_proof_turns']) is int and gate['new_original_proof_turns'] == 0, 'Target/budget gate differs')
    for key in ['new_solution_priority_clearance', 'publication_authorized', 'new_paper', 'tracker_append',
                'PR50_exception_extended', 'exact2000printedbody_read', 'stronger_prior_p8_extremality_certified', 'exact_even_formula_earlier_explicitly_printed']:
        must(gate[key] is False, 'Excluded claim/action present: ' + key)
    must(gate['new_DOI'] is None and sha(GOAL.read_bytes()) == GOAL_SHA == gate['goal_objective_sha256'], 'Goal/publication identity differs')
    must(utc(gate['minimum_writer_ack_utc']) >= utc(gate['UTC']), 'Minimum writer acknowledgement predates final gate')
    F = R / gate['prospective_packet_directory']
    F.resolve().relative_to(A.resolve())
    must(gate['prospective_manifest'] == pin(F / 'MANIFEST.json'), 'Prospective manifest pin differs')
    packet = json.loads((F / 'MANIFEST.json').read_bytes())
    must(len(packet['files']) == 4, 'Prospective input count differs')
    prospective = []
    for row in packet['files']:
        must(('name' in row) != ('path' in row), 'Packet filename schema is absent or ambiguous')
        key = 'name' if 'name' in row else 'path'
        must(set(row) == {key,'bytes','sha256'} and type(row['bytes']) is int and row['bytes'] >= 0, 'Packet pin schema differs')
        name = row[key]; must(type(name) is str and Path(name).name == name, 'Packet name is not one filename')
        prospective.append({'path':str((F / name).relative_to(R)), 'bytes':row['bytes'], 'sha256':row['sha256']})
    must({Path(x['path']).name for x in prospective} == {'CURRENT_RESULT.md', 'CURRENT_PRIORITY_SPECIALIZATION.md', 'PR_BODY.md', 'DISPOSITION_PROPOSAL.json'}, 'Four prospective filenames differ')
    must(same(sorted(gate['bound_prospective_inputs'], key=lambda x:x['path']), sorted(prospective, key=lambda x:x['path'])), 'Four prospective pins differ')
    for row in prospective + [gate['prospective_manifest'], gate['operational_byte_plan']] + gate['bound_current_evidence'] + gate['bound_original_evidence'] + gate['bound_operational_preparation']: check_pin(row)
    proposal = json.loads((F / 'DISPOSITION_PROPOSAL.json').read_bytes())
    must(proposal['stage'] == 'PROSPECTIVE_REVIEW_PACKET_NOT_NATIVE_ACCEPTANCE' and proposal['PR'] == 66 and proposal['original_head'] == HEAD and proposal['original_literal_status'] == 'claimed_solved' and proposal['original_budget'] == '1/5' and proposal['even_refinement_prior_ingredient_corollary_verified'] is True and proposal['earlier_explicit_even_formula_located'] is False and proposal['distinct_tournament_mechanism_novelty_established'] is False, 'Selected prospective scientific boundaries differ')
    required_original = {PREFIX + '/' + x for x in ['CANDIDATE.md', 'source_record.json', 'status.json', 'turns.jsonl']}
    source_root = A / 'original_source_authentication_20261004'
    required_original = {str((source_root / 'original' / x).relative_to(R)) for x in required_original}
    must(required_original <= {x['path'] for x in gate['bound_original_evidence']}, 'Gate does not bind original proof/wrapper/status/ledger')
    plan_path = R / gate['operational_byte_plan']['path']
    plan_path.resolve().relative_to(PREP.resolve())
    required_plan = {str(x.relative_to(R)) for x in [plan_path, Path(__file__), PREP / 'ROOT_readback_attributed_acceptance_20261004.py']}
    must(required_plan <= {x['path'] for x in gate['bound_operational_preparation']}, 'Gate does not bind operator/readback/operational plan')
    plan = json.loads(plan_path.read_bytes())
    must(plan['scientific_changes'] is False and plan['stage'] == 'PLANNED_FUTURE_BYTES_NOT_NATIVE_ACCEPTANCE_OR_MERGE_RECEIPT', 'Operational plan meaning differs')
    finals = {}
    for row in plan['files']:
        must((R / row['source_path']).resolve().parent == F.resolve(), 'Operational plan does not use selected reviewed packet')
        source = (R / row['source_path']).read_bytes()
        must(len(source) == row['source_bytes'] and sha(source) == row['source_sha256'], 'Operational source drift')
        text = source.decode('utf-8')
        for change in row['literal_edits']:
            must(change['required_occurrences'] == 1 and text.count(change['old']) == 1, 'Operational edit no longer unique')
            text = text.replace(change['old'], change['new'])
        final = text.encode('utf-8')
        must(len(final) == row['planned_bytes'] and sha(final) == row['planned_sha256'] and final == (R / row['planned_path']).read_bytes(), 'Reviewed final bytes differ')
        finals[Path(row['source_path']).name] = final
    must(set(finals) == {'CURRENT_RESULT.md', 'CURRENT_PRIORITY_SPECIALIZATION.md', 'PR_BODY.md'}, 'Final document scope differs')
    manifest = json.loads((source_root / 'ORIGINAL_BLOB_MANIFEST.json').read_bytes())
    originals = [x for x in manifest['artifacts'] if x['incoming_changed_domain'] and x['path'] != QUEUE]
    must(manifest['head'] == HEAD and len(originals) == 25 and all(x['mode'] == '100644' and x['path'].startswith(PREFIX + '/') for x in originals), 'Original 25-file incoming domain differs')
    original_paths = {x['path'] for x in originals}
    merge_paths = original_paths | {QUEUE}
    mirror_paths = {PREFIX + '/acceptance.json', PREFIX + '/CURRENT_RESULT.md', PREFIX + '/CURRENT_PRIORITY_SPECIALIZATION.md', STATE, HISTORY}
    for row in manifest['artifacts']:
        b = (source_root / row['retained_path']).read_bytes()
        must(len(b) == row['bytes'] and sha(b) == row['sha256'] and hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == row['git_blob_SHA1'], 'Authenticated original retained body differs')
    source = json.loads((source_root / 'original' / PREFIX / 'source_record.json').read_bytes())
    must(set(source) == {'dataset_revision', 'problem', 'prior_upstream_report'} and type(source['prior_upstream_report']) is dict and bool(source['prior_upstream_report']) and 'upstream_report' not in source, 'PR66 source wrapper typed shape differs')
    def check_originals(commit):
        for row in originals:
            b = git('show', commit + ':' + row['path'])
            must(len(b) == row['bytes'] and sha(b) == row['sha256'], 'Original body drift')
            must(git('ls-tree', commit, '--', row['path']).decode().split()[:3] == [row['mode'], 'blob', row['git_blob_SHA1']], 'Original mode/blob drift')
    def foreign_index():
        return b'\0'.join(x for x in git('ls-files', '--stage', '-z').split(b'\0') if x and x.split(b'\t', 1)[1].decode() not in merge_paths | mirror_paths)
    def foreign_dirty(): return {x.decode() for x in git('diff', '--name-only', '-z').split(b'\0') if x and x.decode() not in merge_paths | mirror_paths}
    def whole_body(path):
        q = R / path
        if not q.exists() and not q.is_symlink(): return (False, None, None)
        must(stat.S_ISREG(q.lstat().st_mode), 'Foreign tracked nonregular path; inspect')
        return (True, q.lstat().st_mode, q.read_bytes())
    must(git('branch', '--show-current').strip() == b'main', 'Stay on main')
    must(not git('diff', '--cached', '--name-only', '-z'), 'Shared index occupied; preserve staging')
    mh = Path(git('rev-parse', '--git-path', 'MERGE_HEAD').decode().strip())
    if not mh.is_absolute(): mh = R / mh
    must(not mh.exists(), 'Existing merge must remain untouched')
    base = git('rev-parse', 'HEAD').decode().strip()
    expected_native_head = [base]
    originals_imported = [args.phase == 'mirror']
    must(git('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == base, 'Main/remote diverged')
    bases = {base}
    out = O / ('NATIVE_MERGE_RESULT.json' if args.phase == 'merge' else 'NATIVE_ACCEPTANCE_RESULT.json')
    must(not out.exists(), 'Actual receipt already exists; preserve it')
    if args.phase == 'mirror':
        prior = json.loads((O / 'NATIVE_MERGE_RESULT.json').read_bytes())
        must(prior['submitted_head'] == HEAD and prior['merge_commit'] == base and prior['gate'] == gate_pin, 'Actual merge continuity differs')
        must(git('show', '-s', '--format=%P', base).decode().split() == [prior['base'], HEAD], 'Exact two-parent merge differs')
        independent = json.loads((PREP / 'ROOT_attributed_acceptance_readback_20261004/MERGE_READBACK.json').read_bytes())
        must(independent['status'] == 'PASS' and independent['phase'] == 'merge' and independent['reviewed_head'] == HEAD and independent['current_commit'] == base and independent['gate'] == gate_pin, 'Independent actual merge readback is absent or stale')
        bases.add(prior['base'])
    ack_path = R / 'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
    ack_body = ack_path.read_bytes()
    def check_window():
        must(ack_path.read_bytes() == ack_body, 'Other-writer acknowledgement body changed')
        w = json.loads(ack_body)
        must(w['shared_git_writes_paused'] is True and w['paused_for'] == PAUSE, 'Fresh exact other-writer acknowledgement absent')
        must(w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True and type(w['all_staged_path_count']) is int and w['all_staged_path_count'] == 0 and w['owned_staged_paths'] == [], 'Writer body/index freeze absent')
        must(w['local_main_at_pause'] == w['remote_main_at_pause'] and w['local_main_at_pause'] in bases, 'Acknowledged baseline differs')
        must(utc(w.get('utc', w.get('UTC', ''))) >= utc(gate['minimum_writer_ack_utc']), 'Writer acknowledgement is stale')
        return w
    check_window(); (D / 'ACKNOWLEDGED_WINDOW.json').write_bytes(ack_body)
    fi = foreign_index(); fd = foreign_dirty(); fb = {path:whole_body(path) for path in fd}
    if args.phase == 'mirror':
        previous_streams = Path(prior['actual_stream_directory'])
        must(previous_streams.resolve().is_relative_to(PREP.resolve()), 'Prior stream directory escaped preparation')
        must((previous_streams / 'ACKNOWLEDGED_WINDOW.json').read_bytes() == ack_body and (previous_streams / 'FOREIGN_INDEX.bin').read_bytes() == fi, 'Merge-to-mirror writer/index continuity differs')
        previous_bodies = json.loads((previous_streams / 'FOREIGN_BODY_SNAPSHOT.json').read_bytes())
        must({x['path'] for x in previous_bodies} == fd, 'Merge-to-mirror foreign dirty scope differs')
        for row in previous_bodies:
            expected = (row['exists'], row['lstat_mode'], Path(row['private_body_path']).read_bytes() if row['exists'] else None)
            must(fb[row['path']] == expected, 'Merge-to-mirror foreign whole body/mode differs')
    (D / 'FOREIGN_INDEX.bin').write_bytes(fi)
    foreign_records = []
    for n, path in enumerate(sorted(fb)):
        exists, mode, body = fb[path]; saved = D / ('FOREIGN_' + str(n) + '.bin')
        if exists: saved.write_bytes(body)
        foreign_records.append({'path':path,'exists':exists,'lstat_mode':mode,'private_body_path':str(saved) if exists else None,'bytes':len(body) if exists else None,'sha256':sha(body) if exists else None})
    (D / 'FOREIGN_BODY_SNAPSHOT.json').write_bytes(jb(foreign_records))
    def preserve():
        check_window()
        must(git('branch', '--show-current').strip() == b'main' and git('rev-parse', 'HEAD').decode().strip() == expected_native_head[0], 'Native branch/head changed during exclusive phase')
        must(foreign_index() == fi and foreign_dirty() == fd and all(whole_body(path) == body for path, body in fb.items()), 'Foreign tracked body/mode/index changed')
        if originals_imported[0]:
            for row in originals:
                path = R / row['path']
                must(not path.is_symlink() and path.is_file() and path.read_bytes() == (source_root / row['retained_path']).read_bytes() and stat.S_IMODE(path.stat().st_mode) == 0o644, 'Native original body/mode drift')
        must(pin(G) == gate_pin and sha(GOAL.read_bytes()) == GOAL_SHA, 'Final gate/goal changed')
        for row in prospective + [gate['prospective_manifest'], gate['operational_byte_plan']] + gate['bound_current_evidence'] + gate['bound_original_evidence'] + gate['bound_operational_preparation']: check_pin(row)
    raw_manifest = json.loads((R / 'unsolved_math_prioritization/manifest.json').read_bytes())
    must(raw_manifest['revision'] == source['dataset_revision'], 'Raw dataset revision differs')
    for name in ('problems.json', 'research_results.json'):
        b = (R / 'unsolved_math_prioritization/cache' / name).read_bytes()
        must({'bytes':len(b), 'sha256':sha(b)} == raw_manifest['files'][name], 'Raw manifest/body differs')
    problems = json.loads((R / 'unsolved_math_prioritization/cache/problems.json').read_bytes())
    reports = json.loads((R / 'unsolved_math_prioritization/cache/research_results.json').read_bytes())
    must(same([x for x in problems if str(x['id']) == ID], [source['problem']]) and CODE in reports and same(reports[CODE], source['prior_upstream_report']), 'Exact raw typed problem/report differs')
    with sqlite3.connect('file:' + str(R / 'unsolved_math_prioritization/cache/catalog.sqlite') + '?mode=ro', uri=True) as db:
        row = db.execute('SELECT payload,report FROM records WHERE key=?', (ID,)).fetchone()
        revisions = db.execute('SELECT revision FROM metadata').fetchall()
    must(row is not None and same(json.loads(row[0]), source['problem']) and row[1] is not None and same(json.loads(row[1]), source['prior_upstream_report']) and revisions == [(source['dataset_revision'],)], 'Exact SQL typed pair differs')
    review_hash = sha(json.dumps([source['problem'], source['prior_upstream_report']], sort_keys=True).encode())
    catalog = [x for x in json.loads((R / 'unsolved_math_prioritization/catalog.json').read_bytes()) if x['id'] == ID]
    must(len(catalog) == 1 and catalog[0]['review_hash'] == review_hash, 'Current source review fingerprint differs')
    identity = {'review_hash':review_hash, 'dataset_revision':source['dataset_revision'], 'native_report_field':'prior_upstream_report', 'raw_problem_SQL_wrapper_identical':True, 'raw_report_present_nonNULL_nonempty_and_SQL_wrapper_identical':True, 'historical_OPEN_TRIAGE_not_current_priority_authority':True}
    preserve()
    pr = json.loads(run(['gh', 'pr', 'view', '66', '--repo', 'AlecKriebel/Math', '--json', 'number,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,url'])[0])
    must(pr['number'] == 66 and pr['headRefOid'] == HEAD and pr['baseRefName'] == 'main' and pr['headRefName'] == 'dot/math-' + ID, 'Fresh PR identity differs')
    aq = json.loads(run(['gh', 'api', 'repos/AlecKriebel/Math/contents/' + QUEUE + '?ref=' + HEAD])[0]); qb = base64.b64decode(aq['content'])
    qpin = next(x for x in manifest['artifacts'] if x['path'] == QUEUE)
    must(len(qb) == qpin['bytes'] and sha(qb) == qpin['sha256'] and aq['sha'] == qpin['git_blob_SHA1'], 'Fresh submitted QUEUE differs')
    target = [s for s in qb.decode().splitlines() if '| ' + ID + ' /' in s]
    must(len(target) == 1 and target[0].split('|')[8].strip() == 'claimed_solved' and target[0].split('|')[9].strip() == '1/5', 'Fresh initial eligibility/budget differs')
    _, available = run(['git', '--no-optional-locks', 'cat-file', '-e', HEAD + '^{commit}'], allowed=(0,128))
    if available:
        must(args.phase == 'merge', 'Merge object disappeared')
        preserve(); git('fetch', '--no-tags', '--no-write-fetch-head', 'origin', 'refs/pull/66/head')
        check = json.loads(run(['gh', 'pr', 'view', '66', '--repo', 'AlecKriebel/Math', '--json', 'headRefOid,state,isDraft'])[0])
        must(check['headRefOid'] == HEAD and check['state'] == 'OPEN' and check['isDraft'] is True, 'Head drift during exact object import')
    check_originals(HEAD)
    ledger = git('show', HEAD + ':' + PREFIX + '/turns.jsonl')
    status = json.loads(git('show', HEAD + ':' + PREFIX + '/status.json'))
    must([json.loads(s)['turn'] for s in ledger.splitlines()] == [1,1,1] and type(status['turns_used']) is int and status['turns_used'] == 1 and 'turn_limit' not in status, 'Original ledger/status shape differs')
    qbefore = (R / QUEUE).read_bytes()
    must(qbefore == git('show', base + ':' + QUEUE), 'Native queue has uncommitted changes')
    if args.phase == 'merge':
        must(pr['state'] == 'OPEN' and pr['isDraft'] is True, 'Reviewed original open draft required')
        incoming = json.loads(run(['gh', 'api', 'repos/AlecKriebel/Math/pulls/66/files?per_page=100'])[0])
        must(len(incoming) == 26 and {x['filename'] for x in incoming} == merge_paths, 'Incoming 26-path scope differs')
        common = git('merge-base', base, HEAD).decode().strip()
        must({x.decode() for x in git('diff', '--name-only', '-z', common, HEAD).split(b'\0') if x} == merge_paths, 'Local incoming scope differs')
        must(all(not (R / path).exists() and not (R / path).is_symlink() for path in original_paths), 'Native original destination already exists')
        lines = qbefore.decode().splitlines(keepends=True); ii = [i for i,s in enumerate(lines) if '| ' + ID + ' /' in s]
        must(len(ii) == 1, 'Native target row is not unique'); i = ii[0]; cells = lines[i].split('|')
        must(len(cells) == 14 and cells[8].strip() == 'queued' and cells[9].strip() == '0/5' and not cells[12].strip(), 'Native target baseline differs')
        cells[8] = ' already_solved '; cells[9] = ' 1/5 '; cells[11] = ' ' + NOTE + ' '; lines[i] = '|'.join(cells); accepted = ''.join(lines).encode()
        preserve(); _, exit_merge = run(['git', '--no-optional-locks', 'merge', '--no-ff', '--no-commit', HEAD], allowed=(0,1))
        conflicts = {x.decode() for x in git('diff', '--name-only', '--diff-filter=U', '-z').split(b'\0') if x}
        must(conflicts <= {QUEUE} and mh.exists() and mh.read_text().strip() == HEAD, 'Unexpected merge state; inspect retained partial merge')
        preserve(); (R / QUEUE).write_bytes(accepted)
        for row in originals:
            b = (R / row['path']).read_bytes()
            must(len(b) == row['bytes'] and sha(b) == row['sha256'] and stat.S_IMODE((R / row['path']).stat().st_mode) == 0o644, 'Imported original body/mode differs')
        originals_imported[0] = True
        git('add', '--', QUEUE)
        must(not git('diff', '--name-only', '--diff-filter=U', '-z') and {x.decode() for x in git('diff', '--cached', '--name-only', '-z').split(b'\0') if x} == merge_paths, 'Merge staged scope differs')
        preserve(); git('commit', '-m', 'Accept PR66 verified crossing bound as attributed prior-result progress')
        commit = git('rev-parse', 'HEAD').decode().strip()
        expected_native_head[0] = commit
        must(git('show', '-s', '--format=%P', commit).decode().split() == [base, HEAD] and {x.decode() for x in git('diff', '--name-only', '-z', base, commit).split(b'\0') if x} == merge_paths, 'Exact two-parent merge commit differs')
        check_originals(commit); preserve(); git('push', 'origin', 'main')
        receipt = {'phase':'merge', 'base':base, 'submitted_head':HEAD, 'merge_commit':commit, 'gate':gate_pin, 'merge_exit_code':exit_merge, 'conflicts':sorted(conflicts), 'native_mirror_pending':True}
    else:
        must(pr['state'] == 'MERGED' and pr['mergeCommit']['oid'] == base, 'GitHub has not confirmed exact merge')
        check_originals(base)
        sb = (R / STATE).read_bytes(); hb = (R / HISTORY).read_bytes()
        must(sb == git('show', base + ':' + STATE) and hb == git('show', base + ':' + HISTORY), 'Native state/history contain uncommitted changes')
        state = json.loads(sb)
        must(ID not in state and all(str(json.loads(s).get('id')) != ID for s in hb.splitlines()), 'Acceptance already exists')
        must(not hb or hb.endswith(b'\n'), 'Incomplete history tail')
        must(all(not (R / path).exists() and not (R / path).is_symlink() for path in mirror_paths - {STATE,HISTORY}), 'Current acceptance destination exists')
        qt = [s for s in qbefore.decode().splitlines() if '| ' + ID + ' /' in s]
        must(len(qt) == 1 and qt[0].split('|')[8].strip() == 'already_solved' and qt[0].split('|')[9].strip() == '1/5' and qt[0].split('|')[11].strip() == NOTE and not qt[0].split('|')[12].strip(), 'Current accepted queue differs')
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        preserve()
        (R / (PREFIX + '/CURRENT_RESULT.md')).write_bytes(finals['CURRENT_RESULT.md'])
        (R / (PREFIX + '/CURRENT_PRIORITY_SPECIALIZATION.md')).write_bytes(finals['CURRENT_PRIORITY_SPECIALIZATION.md'])
        acceptance = {'schema':'pr66-current-attributed-prior-result-acceptance/v1', 'at':now, 'actual_author_pid':os.getpid(), 'problem_id':ID, 'problem_code':CODE, 'pr':66, 'reviewed_head':HEAD, 'merge_commit':base, 'merged_at':pr['mergedAt'], 'status':'already_solved', 'accepted_as':'attributed_partial_prior_result', 'full_source_solved':True, 'full_source_solved_meaning':'The exact Willerton target follows from the verified Fiedler-Stoimenow dated 2002 author body and is separately proved by the submitted tournament proof; no new open-problem resolution.', 'new_open_problem_resolution':False, 'new_solution_priority_clearance':False, 'identical_algorithm_or_earliest_priority_certified':False, 'exact2000printedbody_read':False, 'stronger_prior_p8_extremality_certified':False, 'even_prior_ingredient_verified':True, 'exact_even_formula_earlier_explicitly_printed':False, 'exact_even_formula_earlier_explicitly_printed_meaning':'Not located or certified by this audit; no assertion that no earlier printing exists.', 'tournament_mechanism_novelty':'unestablished', 'original_budget':'1/5', 'original_turn_ledger':pin(R / (PREFIX + '/turns.jsonl')), 'original_turn_event_count':3, 'original_status_turn_limit_field':'ABSENT', 'turn_limit_authority':'Authenticated submitted QUEUE.md literal 1/5; not an invented status.json field.', 'new_original_proof_turns':0, 'final_ROOT_gate':gate_pin, 'bound_current_evidence':gate['bound_current_evidence'], 'bound_prospective_inputs':gate['bound_prospective_inputs'], 'operational_byte_plan':pin(plan_path), 'current_source_identity':identity, 'original_scientific_bodies_are_dated_inputs':True, 'current_priority_specialization':pin(R / (PREFIX + '/CURRENT_PRIORITY_SPECIALIZATION.md')), 'new_paper':False, 'Zenodo_upload':False, 'new_publication_DOI':None, 'tracker_append':False, 'AI_tools_used_extensively':True, 'human_peer_review':False, 'formal_proof_certification':False, 'historical_lifecycle_transitions_reconstructed':False}
        (R / (PREFIX + '/acceptance.json')).write_bytes(jb(acceptance))
        event = {'at':now, 'event':'acceptance_mirror_import', 'id':ID, 'pr':66, 'status':'already_solved', 'turns_used':1, 'turn_limit':5, 'review_hash':review_hash, 'source_record_hash':sha(json.dumps(source['problem'], sort_keys=True).encode()), 'source_report_hash':sha(json.dumps(source['prior_upstream_report'], sort_keys=True).encode()), 'statement_hash':sha(source['problem']['statement'].encode()), 'note':NOTE, 'evidence':{'import_is_present_day_mirror':True, 'historical_transitions_asserted':False, 'reviewed_head':HEAD, 'merge_commit':base, 'canonical_acceptance':pin(R / (PREFIX + '/acceptance.json')), 'final_ROOT_gate':gate_pin, 'original_budget_ledger':pin(R / (PREFIX + '/turns.jsonl')), 'turn_limit_authority':'submitted QUEUE.md 1/5; original status.json has no turn_limit', 'full_source_solved':True, 'new_open_problem_resolution':False, 'accepted_as':'attributed_partial_prior_result', 'new_paper':False, 'new_publication_DOI':None, 'tracker_append':False}}
        event['event_id'] = sha(json.dumps(event, sort_keys=True).encode())
        # Preserve every existing state's entry bytes; insert one new key before
        # the final object delimiter, without reserializing historical entries.
        end = len(sb.rstrip()) - 1; must(sb[end:end+1] == b'}', 'State object terminator differs')
        prefix = sb[:end]; cut = len(prefix.rstrip()); whitespace = prefix[cut:]
        pretty_event = json.dumps(event, ensure_ascii=False, sort_keys=True, indent=2).replace('\n', '\n  ').encode()
        inserted = (b',' if state else b'') + b'\n  ' + json.dumps(ID).encode() + b': ' + pretty_event
        (R / STATE).write_bytes(prefix[:cut] + inserted + whitespace + sb[end:])
        (R / HISTORY).write_bytes(hb + json.dumps(event, ensure_ascii=False, sort_keys=True).encode() + b'\n')
        state_after = json.loads((R / STATE).read_bytes()); history_after = (R / HISTORY).read_bytes()
        must(same({k:v for k,v in state_after.items() if k != ID}, state) and same(state_after[ID], event) and history_after.startswith(hb) and len(history_after[len(hb):].splitlines()) == 1, 'Other native state/history changed')
        must((R / QUEUE).read_bytes() == qbefore, 'Mirror changed queue')
        preserve(); git('add', '--', *sorted(mirror_paths))
        must({x.decode() for x in git('diff', '--cached', '--name-only', '-z').split(b'\0') if x} == mirror_paths, 'Mirror staged five-file scope differs')
        preserve(); git('commit', '-m', 'Bind PR66 credited prior-result acceptance to exact merge and source audits')
        commit = git('rev-parse', 'HEAD').decode().strip()
        expected_native_head[0] = commit
        must(git('show', '-s', '--format=%P', commit).decode().strip() == base and {x.decode() for x in git('diff', '--name-only', '-z', base, commit).split(b'\0') if x} == mirror_paths, 'Mirror commit scope differs')
        check_originals(commit); preserve(); git('push', 'origin', 'main')
        receipt = {'phase':'mirror', 'merge_commit':base, 'acceptance_commit':commit, 'submitted_head':HEAD, 'gate':gate_pin, 'event_id':event['event_id'], 'other_native_states_and_history_prefix_preserved':True, 'one_present_day_acceptance_event':True, 'program_completion_not_conferred':True}
    must(git('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == commit, 'Push readback differs')
    must(not git('diff', '--cached', '--name-only', '-z'), 'Shared index not empty after phase')
    check_originals(commit); preserve()
    receipt.update(UTC=dt.datetime.now(dt.timezone.utc).isoformat(), actual_controller_pid=os.getpid(), remote_main=commit, foreign_tracked_whole_bodies_modes_and_index_preserved=True, original_25_bodies_modes_blobs_preserved=True, original_budget='1/5', current_source_identity=identity, new_paper=False, new_DOI=None, tracker_append=False, actual_stream_directory=str(D), actual_command_count=len(commands))
    with out.open('xb') as f: f.write(jb(receipt))
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__': main()
