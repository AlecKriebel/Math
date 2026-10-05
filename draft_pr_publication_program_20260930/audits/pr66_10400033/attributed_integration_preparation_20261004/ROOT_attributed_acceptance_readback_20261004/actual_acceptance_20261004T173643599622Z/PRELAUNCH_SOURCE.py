"""Independent ROOT readback; writes only this preparation's actual readback files.

Run merge after the merge phase. Run acceptance after the five-file mirror and
ROOT's separate GitHub title/body correction. No native state or progress edit.
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
Q = 'unsolved_math_prioritization/QUEUE.md'
T = 'unsolved_math_prioritization/attempts/' + ID
S = 'unsolved_math_prioritization/state.json'
H = 'unsolved_math_prioritization/history.jsonl'

def sha(b): return hashlib.sha256(b).hexdigest()
def read(path): return json.loads(path.read_bytes())
def canon(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def same(a,b): return canon(a) == canon(b)
def require(ok, msg):
    if not ok: raise RuntimeError(msg)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=['merge','acceptance'])
    args = ap.parse_args()
    require(not sys.flags.optimize and __debug__ and sys.flags.ignore_environment and sys.flags.dont_write_bytecode, 'Invoke -E -B without optimization')
    F = PREP / 'ROOT_attributed_acceptance_readback_20261004'
    F.mkdir(exist_ok=True)
    result_path = F / (args.phase.upper() + '_READBACK.json')
    require(not result_path.exists(), 'Readback receipt exists; preserve it')
    D = F / ('actual_' + args.phase + '_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    D.mkdir(exist_ok=False); (D / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    commands = []
    def run(argv):
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = child.communicate(); n = str(len(commands) + 1)
        row = {'argv':argv, 'cwd':str(R), 'actual_child_pid':child.pid, 'started_utc':started,
               'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code':child.returncode}
        for name, body in [('stdout',out),('stderr',err)]:
            path = D / (n + '.' + name); path.write_bytes(body)
            row[name] = {'path':str(path), 'bytes':len(body), 'sha256':sha(body)}
        commands.append(row); (D / 'ACTUAL_COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
        require(child.returncode == 0, 'Read command failed; inspect retained actual streams')
        return out
    def git(*args): return run(['git','--no-optional-locks',*args])
    O = PREP / 'native_attributed_result_operations_20261004'
    merge = read(O / 'NATIVE_MERGE_RESULT.json')
    acceptance_receipt = read(O / 'NATIVE_ACCEPTANCE_RESULT.json') if args.phase == 'acceptance' else None
    require(merge['submitted_head'] == HEAD, 'Merge receipt identity differs')
    current = merge['merge_commit'] if args.phase == 'merge' else acceptance_receipt['acceptance_commit']
    if acceptance_receipt:
        require(acceptance_receipt['submitted_head'] == HEAD and acceptance_receipt['merge_commit'] == merge['merge_commit'] and acceptance_receipt['gate'] == merge['gate'], 'Acceptance continuity differs')
    require(git('branch','--show-current').strip() == b'main' and git('rev-parse','HEAD').decode().strip() == current, 'Native branch/head differs')
    require(not git('diff','--cached','--name-only','-z'), 'Shared index occupied')
    require(git('ls-remote','--heads','origin','main').decode().split()[0] == current, 'Remote exact current commit differs')
    pr = json.loads(run(['gh','pr','view','66','--repo','AlecKriebel/Math','--json','number,state,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,title,body,url']))
    require(pr['number'] == 66 and pr['state'] == 'MERGED' and pr['headRefOid'] == HEAD and pr['headRefName'] == 'dot/math-' + ID and pr['baseRefName'] == 'main' and pr['mergeCommit']['oid'] == merge['merge_commit'] and pr['mergedAt'], 'GitHub exact merge identity differs')
    require(git('show','-s','--format=%P',merge['merge_commit']).decode().split() == [merge['base'], HEAD], 'Merge is not exact two-parent integration')
    if acceptance_receipt:
        require(git('show','-s','--format=%P',current).decode().strip() == merge['merge_commit'], 'Acceptance parent differs')
    gate_path = R / merge['gate']['path']; gate = read(gate_path)
    require(len(gate_path.read_bytes()) == merge['gate']['bytes'] and sha(gate_path.read_bytes()) == merge['gate']['sha256'] and gate['PR'] == 66 and gate['expected_original_head'] == HEAD and gate['audited_outcome'] == 'already_solved' and gate['ROOT_authorizes_guarded_attributed_prior_result_acceptance'] is True, 'Final gate identity differs')
    for row in gate['bound_prospective_inputs'] + [gate['prospective_manifest'],gate['operational_byte_plan']] + gate['bound_current_evidence'] + gate['bound_original_evidence'] + gate['bound_operational_preparation']:
        path = R / row['path']; path.resolve().relative_to(R)
        require(not path.is_symlink() and path.is_file() and len(path.read_bytes()) == row['bytes'] and sha(path.read_bytes()) == row['sha256'], 'Bound evidence drift')
    source_root = A / 'original_source_authentication_20261004'
    manifest = read(source_root / 'ORIGINAL_BLOB_MANIFEST.json')
    originals = [x for x in manifest['artifacts'] if x['incoming_changed_domain'] and x['path'] != Q]
    require(manifest['head'] == HEAD and len(originals) == 25 and all(x['mode'] == '100644' and x['path'].startswith(T + '/') for x in originals), 'Original 25-file scope differs')
    original_paths = {x['path'] for x in originals}
    for row in originals:
        path = R / row['path']; stored = source_root / row['retained_path']
        require(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode) and stat.S_IMODE(path.lstat().st_mode) == 0o644 and path.read_bytes() == stored.read_bytes(), 'Original native whole body/mode differs')
        b = git('show',current + ':' + row['path'])
        require(len(b) == row['bytes'] and sha(b) == row['sha256'], 'Original current commit body differs')
        require(git('ls-tree',current,'--',row['path']).decode().split()[:3] == [row['mode'],'blob',row['git_blob_SHA1']], 'Original Git mode/blob differs')
    require({x.decode() for x in git('diff','--name-only','-z',merge['base'],merge['merge_commit']).split(b'\0') if x} == original_paths | {Q}, 'Merge 26-path domain differs')
    before = git('show',merge['base'] + ':' + Q)
    now = (R / Q).read_bytes()
    require(now == git('show',current + ':' + Q), 'Native queue is not current committed body')
    old_lines = before.splitlines(keepends=True); new_lines = now.splitlines(keepends=True)
    require(len(old_lines) == len(new_lines), 'Queue line count differs')
    changed = [(x,y) for x,y in zip(old_lines,new_lines) if x != y]
    require(len(changed) == 1 and b'| 10400033 /' in changed[0][0] and b'| 10400033 /' in changed[0][1], 'Other queue rows changed')
    old_cells = changed[0][0].decode().split('|'); cells = changed[0][1].decode().split('|')
    require(old_cells[8].strip() == 'queued' and old_cells[9].strip() == '0/5' and cells[8].strip() == 'already_solved' and cells[9].strip() == '1/5' and not cells[12].strip() and all(old_cells[i] == cells[i] for i in range(len(cells)) if i not in {8,9,11}), 'Target queue scope/budget/DOI differs')
    original_queue = source_root / 'original' / Q
    submitted = [x for x in original_queue.read_text().splitlines() if '| ' + ID + ' /' in x]
    require(len(submitted) == 1 and submitted[0].split('|')[8].strip() == 'claimed_solved' and submitted[0].split('|')[9].strip() == '1/5', 'Initial literal intake differs')
    api_queue = json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/' + Q + '?ref=' + HEAD]))
    require(base64.b64decode(api_queue['content']) == original_queue.read_bytes(), 'Remote immutable submitted queue differs')
    ledger = (R / (T + '/turns.jsonl')).read_bytes(); status = read(R / (T + '/status.json'))
    require([json.loads(x)['turn'] for x in ledger.splitlines()] == [1,1,1] and type(status['turns_used']) is int and status['turns_used'] == 1 and 'turn_limit' not in status and status['status'] == 'claimed_solved', 'Original one-turn ledger/status was rewritten')
    source = read(R / (T + '/source_record.json'))
    require(set(source) == {'dataset_revision','problem','prior_upstream_report'} and type(source['prior_upstream_report']) is dict and source['prior_upstream_report'], 'Original report wrapper shape differs')
    raw_manifest = read(R / 'unsolved_math_prioritization/manifest.json')
    require(raw_manifest['revision'] == source['dataset_revision'], 'Current raw revision differs')
    for name in ('problems.json','research_results.json'):
        b = (R / 'unsolved_math_prioritization/cache' / name).read_bytes()
        require({'bytes':len(b),'sha256':sha(b)} == raw_manifest['files'][name], 'Current raw manifest/body differs')
    problems = read(R / 'unsolved_math_prioritization/cache/problems.json'); reports = read(R / 'unsolved_math_prioritization/cache/research_results.json')
    require(same([x for x in problems if str(x['id']) == ID],[source['problem']]) and CODE in reports and same(reports[CODE],source['prior_upstream_report']), 'Current raw typed source pair differs')
    with sqlite3.connect('file:' + str(R / 'unsolved_math_prioritization/cache/catalog.sqlite') + '?mode=ro',uri=True) as db:
        pair = db.execute('SELECT payload,report FROM records WHERE key=?',(ID,)).fetchone()
        revisions = db.execute('SELECT revision FROM metadata').fetchall()
    require(pair is not None and same(json.loads(pair[0]),source['problem']) and pair[1] is not None and same(json.loads(pair[1]),source['prior_upstream_report']) and revisions == [(source['dataset_revision'],)], 'Current SQL typed source pair differs')
    review_hash = sha(json.dumps([source['problem'],source['prior_upstream_report']],sort_keys=True).encode())
    catalog = [x for x in read(R / 'unsolved_math_prioritization/catalog.json') if x['id'] == ID]
    require(len(catalog) == 1 and catalog[0]['review_hash'] == review_hash, 'Current review fingerprint differs')
    # Check each phase's exact retained foreign body snapshots independently.
    receipt = acceptance_receipt or merge
    actual = Path(receipt['actual_stream_directory'])
    require(actual.resolve().is_relative_to(PREP.resolve()), 'Receipt stream directory escaped preparation')
    require((R / 'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json').read_bytes() == (actual / 'ACKNOWLEDGED_WINDOW.json').read_bytes(), 'Acknowledged writer window changed before readback')
    owned = original_paths | {Q,T + '/acceptance.json',T + '/CURRENT_RESULT.md',T + '/CURRENT_PRIORITY_SPECIALIZATION.md',S,H}
    foreign_index = b'\0'.join(x for x in git('ls-files','--stage','-z').split(b'\0') if x and x.split(b'\t',1)[1].decode() not in owned)
    require(foreign_index == (actual / 'FOREIGN_INDEX.bin').read_bytes(), 'Foreign index differs from acknowledged baseline')
    snapshots = read(actual / 'FOREIGN_BODY_SNAPSHOT.json')
    require({x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x and x.decode() not in owned} == {x['path'] for x in snapshots}, 'Foreign tracked dirty scope differs')
    for row in snapshots:
        path = R / row['path']
        if not row['exists']: require(not path.exists() and not path.is_symlink(), 'Foreign deleted path was recreated')
        else: require(not path.is_symlink() and path.is_file() and path.lstat().st_mode == row['lstat_mode'] and path.read_bytes() == Path(row['private_body_path']).read_bytes(), 'Foreign tracked whole body/mode changed')
    if args.phase == 'acceptance':
        mirror_paths = {T + '/acceptance.json',T + '/CURRENT_RESULT.md',T + '/CURRENT_PRIORITY_SPECIALIZATION.md',S,H}
        require({x.decode() for x in git('diff','--name-only','-z',merge['merge_commit'],current).split(b'\0') if x} == mirror_paths, 'Mirror five-file domain differs')
        plan_path = R / gate['operational_byte_plan']['path']
        require(plan_path.resolve().is_relative_to(PREP.resolve()), 'Operational plan escaped preparation')
        plan = read(plan_path)
        for row in plan['files']:
            final = (R / row['planned_path']).read_bytes()
            require(len(final) == row['planned_bytes'] and sha(final) == row['planned_sha256'], 'Reviewed final document drift')
            name = Path(row['source_path']).name
            if name == 'PR_BODY.md': require(pr['body'] == final.decode() and pr['title'] == plan['title'], 'GitHub accepted title/body differs')
            else: require((R / (T + '/' + name)).read_bytes() == final and git('show',current + ':' + T + '/' + name) == final, 'Native accepted document differs')
        accept = read(R / (T + '/acceptance.json'))
        require(accept['schema'] == 'pr66-current-attributed-prior-result-acceptance/v1' and accept['status'] == 'already_solved' and accept['accepted_as'] == 'attributed_partial_prior_result' and accept['full_source_solved'] is True and accept['new_open_problem_resolution'] is False and accept['new_solution_priority_clearance'] is False, 'Accepted scientific meaning differs')
        require(accept['reviewed_head'] == HEAD and accept['merge_commit'] == merge['merge_commit'] and accept['merged_at'] == pr['mergedAt'] and accept['original_budget'] == '1/5' and accept['original_turn_event_count'] == 3 and accept['original_status_turn_limit_field'] == 'ABSENT' and type(accept['new_original_proof_turns']) is int and accept['new_original_proof_turns'] == 0, 'Acceptance identity/budget differs')
        require(accept['new_paper'] is False and accept['Zenodo_upload'] is False and accept['new_publication_DOI'] is None and accept['tracker_append'] is False and accept['exact2000printedbody_read'] is False and accept['stronger_prior_p8_extremality_certified'] is False, 'Excluded action/claim differs')
        require(accept['even_prior_ingredient_verified'] is True and accept['exact_even_formula_earlier_explicitly_printed'] is False and accept['tournament_mechanism_novelty'] == 'unestablished', 'Even-ingredient attribution/remaining priority boundary differs')
        require(accept['final_ROOT_gate'] == merge['gate'] and same(accept['bound_prospective_inputs'],gate['bound_prospective_inputs']) and accept['current_source_identity']['review_hash'] == review_hash and accept['current_source_identity']['native_report_field'] == 'prior_upstream_report', 'Acceptance evidence/source identity differs')
        old_state = json.loads(git('show',merge['merge_commit'] + ':' + S)); state = read(R / S)
        old_history = git('show',merge['merge_commit'] + ':' + H); history = (R / H).read_bytes()
        require(ID not in old_state and same({k:v for k,v in state.items() if k != ID},old_state) and history.startswith(old_history), 'Other state entries/history prefix changed')
        events = history[len(old_history):].splitlines(); require(len(events) == 1, 'Expected one current import event')
        event = json.loads(events[0]); event_copy = dict(event); event_id = event_copy.pop('event_id')
        require(same(event,state[ID]) and event['event'] == 'acceptance_mirror_import' and event['id'] == ID and event['pr'] == 66 and event['status'] == 'already_solved' and type(event['turns_used']) is int and event['turns_used'] == 1 and event['turn_limit'] == 5 and event['event_id'] == acceptance_receipt['event_id'] == sha(json.dumps(event_copy,sort_keys=True).encode()) and event['evidence']['historical_transitions_asserted'] is False, 'Actual present-day event/state differs')
        require(event['at'] == accept['at'] and event['note'] == cells[11].strip() and event['review_hash'] == review_hash and event['evidence']['canonical_acceptance']['sha256'] == sha((R / (T + '/acceptance.json')).read_bytes()), 'Current event does not bind actual acceptance')
        for path in mirror_paths: require((R / path).read_bytes() == git('show',current + ':' + path), 'Native mirror body differs from acceptance commit')
    result = {'UTC':dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_controller_pid':os.getpid(), 'status':'PASS', 'phase':args.phase, 'PR':66, 'reviewed_head':HEAD, 'merge_commit':merge['merge_commit'], 'current_commit':current, 'gate':merge['gate'], 'GitHub_exact_two_parent_merge_verified':True, 'GitHub_accepted_metadata_verified':args.phase == 'acceptance', 'original_25_whole_bodies_modes_blobs_preserved':True, 'original_budget':'1/5', 'original_turn_events':[1,1,1], 'original_status_turn_limit':'ABSENT', 'other_queue_rows_and_foreign_tracked_whole_bodies_modes_index_preserved':True, 'raw_SQL_wrapper_typed_source_pair_verified':True, 'native_acceptance_verified':args.phase == 'acceptance', 'one_actual_current_import_event':args.phase == 'acceptance', 'outcome':'already_solved', 'accepted_as':'attributed_partial_prior_result', 'even_prior_ingredient_verified':True, 'exact_even_formula_earlier_explicitly_printed':False, 'tournament_mechanism_novelty':'unestablished', 'new_open_problem_resolution':False, 'new_paper':False, 'new_DOI':None, 'tracker_append':False, 'scoped_checkpoint_and_program_completion_not_conferred':True, 'actual_stream_directory':str(D), 'actual_command_count':len(commands)}
    with result_path.open('x') as f: f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__': main()
