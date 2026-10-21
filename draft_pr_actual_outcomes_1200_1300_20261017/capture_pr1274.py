"""Read-only live admission and exact original Git-blob capture; no index use."""
import datetime, hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
A = ROOT / 'audits/pr1274_2307072'
A.mkdir(parents=True, exist_ok=True)
(A / '_local').mkdir(exist_ok=True)

def run(*args):
    return subprocess.check_output(args, cwd=ROOT.parent)

def put(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
p = json.loads(run('gh', 'pr', 'view', '1274', '--repo', 'AlecKriebel/Math', '--json',
    'number,title,url,state,isDraft,headRefOid,headRefName,baseRefName,body,files,commits'))
if p['state'] != 'OPEN' or not p['isDraft'] or p['headRefOid'] != 'fc334f4bd5d8cbc2a241293e2b1419d35c7eead1':
    raise ValueError('Live state/head changed: reconsider before admission')
evidence = 'Adds a self-contained negative answer to Hayman–Lingham Problem 7.72'
if evidence not in p['body'] or len(p['files']) != 6:
    raise ValueError('Original explicit full-target outcome or file count changed')
put(A / 'LIVE_PR_PREFLIGHT.json', p)
(A / '_local/ORIGINAL_PR_BODY.md').write_text(p['body'])
run('git', 'fetch', '--no-tags', 'origin',
    'refs/pull/1274/head:refs/math-audit/1200-1300-20261017/pr1274-original')
head = p['headRefOid']
parents = run('git', 'show', '-s', '--format=%P', head).decode().split()
rows = []
for d in ('submitted', 'current_edition'):
    (A / d).mkdir(exist_ok=True)
for f in p['files']:
    path = f['path']
    if not path.startswith('unsolved_math_prioritization/attempts/2307072/') or '/' in path.rsplit('2307072/', 1)[1]:
        raise ValueError('Unexpected path')
    blob = run('git', 'rev-parse', head + ':' + path).decode().strip()
    data = run('git', 'cat-file', 'blob', blob)
    if hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() != blob:
        raise ValueError('Git blob authentication failed')
    name = pathlib.PurePosixPath(path).name
    for d in ('submitted', 'current_edition'):
        dest = A / d / name
        if dest.exists() and dest.read_bytes() != data:
            raise ValueError('Refusing to overwrite different captured bytes')
        dest.write_bytes(data)
    rows.append(dict(path=path, local_path='submitted/' + name, bytes=len(data),
        sha256=hashlib.sha256(data).hexdigest(), git_blob_sha1=blob))
snapshot = dict(at_utc=now, pr=1274, problem_id=2307072, url=p['url'], title=p['title'],
    head=head, branch=p['headRefName'], parents=parents,
    body_sha256=hashlib.sha256(p['body'].encode()).hexdigest(), files=rows,
    scope='Exact current original six Git blob bodies at pinned submitted head; no math acceptance inferred.')
put(A / 'SUBMITTED_SNAPSHOT.json', snapshot)
put(A / 'ELIGIBILITY_REVALIDATION.json', dict(at_utc=now, pr=1274, head=head,
    body_sha256=snapshot['body_sha256'], decision='eligible_explicit_full_negative_original_target_claim',
    evidence=evidence, QUEUE_status_observed='queued',
    policy='Latest human actual-outcome rule; generic no-novelty limits do not override explicit full counterexample claim. Truth and priority remain untested.'))
statement = run('python3', 'unsolved_math_prioritization/queue.py', 'show', '2307072')
(A / '_local/ORIGINAL_PROBLEM_SHOW.json').write_bytes(statement)
with (A / 'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n## {now} — live admission (5%)\n\nOriginal six files authenticated against live head {head}. Actual outcome explicitly claims a full negative answer; queued status is stale. Mathematical and priority validation remain open. Shared main/index untouched.\n')
state_path = ROOT / 'PROGRAM_STATE.json'
s = json.loads(state_path.read_text())
s.update(current_pr=1274, current_pr_stage='independent_mathematical_review',
    current_pr_completion_estimate_percent=5, current_pr_math_gate_families=[])
put(state_path, s)
print(json.dumps(dict(at_utc=now, head=head, parents=parents, files=rows), indent=2))
