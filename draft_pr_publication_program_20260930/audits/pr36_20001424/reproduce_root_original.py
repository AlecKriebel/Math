"""Actually replay original PR36 code and verify full immutable source/Git bindings."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, shutil, sqlite3, subprocess, sys

ROOT = Path('/Users/alec/Documents/Math')
HERE = Path(__file__).resolve().parent
SNAP = HERE / 'source_snapshot'
QUEUE = ROOT / 'unsolved_math_prioritization'
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())

def command(args):
    return subprocess.check_output(args, cwd=ROOT)

def main():
    assert not (HERE / 'ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json').exists()
    snap = load(HERE / 'snapshot_manifest.json')
    assert command(['git', 'branch', '--show-current']).decode().strip() == 'main'
    assert len(snap['files']) == 16
    for z in snap['files']:
        data = (SNAP / z['path']).read_bytes()
        assert len(data) == z['size'] and sha(data) == z['sha256']
        assert command(['git', 'show', snap['head'] + ':unsolved_math_prioritization/attempts/20001424/' + z['path']]) == data
        if z['path'].endswith('.json'):
            json.loads(data)
        elif z['path'].endswith('.jsonl'):
            for line in data.splitlines(): json.loads(line)
    assert command(['git', 'diff', '--name-only', snap['base'], snap['head']]).decode().splitlines() == snap['changed_paths']
    assert command(['git', 'diff', snap['base'], snap['head']]) == (HERE / 'pr_input/diff.patch').read_bytes()
    manifest = load(QUEUE / 'manifest.json')
    raw = {}
    for name, binding in manifest['files'].items():
        data = (QUEUE / 'cache' / name).read_bytes()
        assert len(data) == binding['bytes'] and sha(data) == binding['sha256']
        raw[name] = json.loads(data)
    problems = raw['problems.json']; reports = raw['research_results.json']
    assert len(problems) == 15458
    selected = [p for p in problems if p['id'] == 20001424]
    assert len(selected) == 1
    p = selected[0]
    assert sum(q['problem_number'] == p['problem_number'] for q in problems) == 1
    r = reports.get(p['problem_number'], {})
    source = load(SNAP / 'source_record.json')
    assert source['problem'] == p and source['upstream_prior_report'] == r
    db = sqlite3.connect((QUEUE / 'cache/catalog.sqlite').as_uri() + '?mode=ro', uri=True)
    row = db.execute('SELECT payload,report FROM records WHERE key=?', ('20001424',)).fetchone()
    assert json.loads(row[0]) == p and json.loads(row[1]) == r
    assert db.execute('SELECT revision FROM metadata').fetchone()[0] == manifest['revision']
    db.close()
    spec = importlib.util.spec_from_file_location('pure_queue_score_pr36', QUEUE / 'queue.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    score = mod.score(p, r, load(QUEUE / 'policy.json'))
    assert score['review_hash'] == sha(json.dumps([p, r], sort_keys=True).encode())
    assert score['statement_hash'] == sha(p['statement'].encode())
    for name, obj in [('pinned_problem.json', p), ('pinned_prior_report.json', r)]:
        out = HERE / name
        assert not out.exists()
        out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    ready = load(SNAP / 'readiness.json'); status = load(SNAP / 'status.json')
    turns = [json.loads(line) for line in (SNAP / 'turns.jsonl').read_bytes().splitlines()]
    assert ready['turns_used'] == status['turns_used'] == len(turns) == 1
    assert ready['turn_limit'] == status['turn_limit'] == 5 and turns[0]['turn'] == 1
    review = load(SNAP / 'review/review_summary.json')
    assert sha((SNAP / 'CANDIDATE.md').read_bytes()) == status['proof_sha256'] == review['reviewed_sha256']
    assert sha((SNAP / 'review/REVIEW.md').read_bytes()) == status['review_sha256'] == review['review_sha256']
    assert sha((SNAP / 'verify_graph.py').read_bytes()) == status['verifier_sha256']
    runs = []
    for code, expected in [('verify_graph.py', 'graph_verification.json'), ('review/independent_checks.py', 'review/independent_results.json')]:
        dest = HERE / 'tmp/root_original_replay' / code
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SNAP / code, dest)
        actual = subprocess.run([sys.executable, str(dest)], cwd=dest.parent, capture_output=True)
        (dest.parent / 'actual_stdout.txt').write_bytes(actual.stdout)
        (dest.parent / 'actual_stderr.txt').write_bytes(actual.stderr)
        assert actual.returncode == 0 and not actual.stderr
        assert actual.stdout == (SNAP / expected).read_bytes()
        runs.append({'program': code, 'implementation_sha256': sha(dest.read_bytes()), 'returncode': actual.returncode,
                     'stdout_sha256': sha(actual.stdout), 'stderr_sha256': sha(actual.stderr), 'whole_result_BYTE_identical': True})
    out = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'head': snap['head'], 'base': snap['base'],
           'original16_actual_Git_blobs_and17_diff_paths_verified': True, 'complete_raw_corpus_bytes': sum(x['bytes'] for x in manifest['files'].values()),
           'complete_raw_problem_prior_match_snapshot_SQL': True, 'source_revision': manifest['revision'],
           'source_pair_review_hash': score['review_hash'], 'statement_hash': score['statement_hash'],
           'separate_prior_report_present': p['problem_number'] in reports, 'original_budget': '1/5', 'new_research_attempts': 0,
           'actual_unchanged_original_runs': runs, 'scope': 'Source/Git accounting and finite diagnostics only. The universal mathematical mechanism and priority remain separately under adversarial audit.'}
    (HERE / 'ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
