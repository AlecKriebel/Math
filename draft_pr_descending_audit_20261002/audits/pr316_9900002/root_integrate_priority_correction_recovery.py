"""Prepare, then separately publish, an exactly scoped correction using a private index."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, os, stat, subprocess, sys
A = Path(__file__).resolve().parent
ROOT = A.parents[2]
D = A / 'priority_correction_packet'
MODE = sys.argv[1]
require_mode = MODE in ['prepare', 'publish', 'recover']
if not require_mode:
    raise RuntimeError('Unknown mode')
CAP = A / ('integration_' + MODE + '_private')
CAP.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
pin = lambda p: {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
def require(test, label):
    if not test:
        raise RuntimeError(label)
def save(p, value):
    require(not p.exists(), 'Artifact already exists: ' + str(p))
    p.write_text(json.dumps(value, indent=2) + '\n')
calls = 0
def run(args, data=None, env=None, ok=(0,)):
    global calls
    calls += 1
    f = CAP / ('call_' + str(calls).zfill(3))
    f.mkdir()
    spec = {'argv': args, 'cwd': str(ROOT), 'started_utc': utc(), 'stdin_bytes': 0 if data is None else len(data), 'stdin_sha256': None if data is None else sha(data), 'private_index': None if env is None else env.get('GIT_INDEX_FILE')}
    save(f / 'spec.json', spec)
    r = subprocess.run(args, input=data, capture_output=True, cwd=ROOT, env=env)
    (f / 'stdout.bin').write_bytes(r.stdout)
    (f / 'stderr.bin').write_bytes(r.stderr)
    spec.update(ended_utc=utc(), exit_code=r.returncode, stdout=pin(f / 'stdout.bin'), stderr=pin(f / 'stderr.bin'))
    save(f / 'execution.json', spec)
    require(r.returncode in ok, 'Native command failed: ' + str(args) + '\n' + r.stderr.decode(errors='replace'))
    return r
def git(*args, data=None, env=None, ok=(0,)):
    return run(['/usr/bin/git', *args], data=data, env=env, ok=ok)
def gh(*args):
    return run(['/opt/homebrew/bin/gh', *args])
def text_git(*args):
    return git(*args).stdout.decode().strip()
def local_state():
    require(text_git('branch', '--show-current') == 'main', 'Working branch changed')
    paths = git('diff', '--name-only', '-z', 'HEAD').stdout.split(b'\0')
    tracked = {}
    for raw in paths:
        if raw:
            p = ROOT / os.fsdecode(raw)
            tracked[os.fsdecode(raw)] = dict(pin(p), mode=stat.S_IMODE(p.stat().st_mode))
    index_path = Path(text_git('rev-parse', '--git-path', 'index'))
    if not index_path.is_absolute():
        index_path = ROOT / index_path
    return {'main': text_git('rev-parse', 'HEAD'), 'index': pin(index_path), 'tracked_dirty_bytes_modes': tracked}
def remote():
    return json.loads(gh('pr', 'view', '316', '--json', 'state,isDraft,headRefOid,headRefName,title,body,url').stdout)
original = json.loads((A / 'snapshot_manifest.json').read_bytes())
OLD = original['head']
Q = 'unsolved_math_prioritization/QUEUE.md'
T = original['target_prefix']
require(OLD == 'c96a3b2019ed3d6aabe0612b31491161dcb275e8' and T == 'unsolved_math_prioritization/attempts/9900002', 'Original head/prefix changed')
final = json.loads((A / 'PRIORITY_CORRECTION_FINALIZATION.json').read_bytes())
for name, expected in final['final_packet'].items():
    require(pin(D / name) == expected, 'Final packet changed: ' + name)
before = local_state()
if MODE == 'prepare':
    live = remote()
    require(live['state'] == 'OPEN' and live['isDraft'] and live['headRefOid'] == OLD, 'Original PR changed')
    git('fetch', 'origin', 'main')
    MAIN = text_git('rev-parse', 'origin/main')
    require(MAIN == before['main'], 'Main differs from authenticated remote; refresh before preparing')
    for e in original['files']:
        p = A / 'snapshot' / e['path']
        b = p.read_bytes()
        require(len(b) == e['bytes'] and sha(b) == e['sha256'], 'Snapshot changed')
        require(git('show', OLD + ':' + e['path']).stdout == b, 'Original Git bytes differ')
    merged = git('merge-tree', '--write-tree', OLD, MAIN, ok=(0,1))
    tree = merged.stdout.decode().splitlines()[0]
    if merged.returncode:
        conflicts = [s.rsplit('\t', 1)[1] for s in merged.stdout.decode().splitlines() if '\t' in s]
        require(conflicts and set(conflicts) == {Q}, 'Unexpected conflict')
    raw = git('show', MAIN + ':' + Q).stdout
    lines = raw.splitlines(keepends=True)
    matches = [i for i,l in enumerate(lines) if len(l.split(b'|')) > 9 and l.split(b'|')[2].strip().split(b' / ')[0] == b'9900002']
    require(len(matches) == 1, 'Own main row not unique')
    i = matches[0]
    prior = lines[i]
    cells = prior.split(b'|')
    require([cells[j].strip() for j in [8,9]] == [b'queued', b'0/5'], 'Main own row unexpectedly changed')
    old_rows = (A / 'snapshot' / Q).read_bytes().splitlines()
    old_matches = [l for l in old_rows if len(l.split(b'|')) > 9 and l.split(b'|')[2].strip().split(b' / ')[0] == b'9900002']
    require(len(old_matches) == 1 and [old_matches[0].split(b'|')[j].strip() for j in [8,9]] == [b'claimed_solved', b'1/5'], 'Original eligible status/count changed')
    cells[8], cells[9] = b' already_solved ', b' 1/5 '
    lines[i] = b'|'.join(cells)
    new_queue = b''.join(lines)
    require([j for j,(x,y) in enumerate(zip(prior.split(b'|'), cells)) if x != y] == [8,9], 'Unexpected own queue cells')
    index = CAP / 'private_index'
    env = dict(os.environ, GIT_INDEX_FILE=str(index))
    git('read-tree', tree, env=env)
    def insert(path, b):
        blob = git('hash-object', '-w', '--stdin', data=b).stdout.decode().strip()
        git('update-index', '--add', '--cacheinfo', '100644,' + blob + ',' + path, env=env)
    insert(Q, new_queue)
    for name in ['CURRENT_STATUS.json', 'README.md', 'PUBLICATION_MANIFEST.json', 'CURRENT_PRIORITY_NOTE.md']:
        insert(T + '/' + name, (D / name).read_bytes())
    tree = git('write-tree', env=env).stdout.decode().strip()
    expected = {e['path'] for e in original['files']} | {T + '/CURRENT_PRIORITY_NOTE.md'}
    changed = set(git('diff', '--name-only', MAIN, tree).stdout.decode().splitlines())
    require(changed == expected and len(changed) == 20, 'Integration scope differs')
    preserve = []
    for e in original['files']:
        if e['path'] != Q and e['path'] not in {T + '/' + n for n in ['CURRENT_STATUS.json','README.md','PUBLICATION_MANIFEST.json']}:
            require(git('show', tree + ':' + e['path']).stdout == (A / 'snapshot' / e['path']).read_bytes(), 'Historical bytes changed')
            preserve.append(e['path'])
    require(len(preserve) == 15, 'Historical count differs')
    commit = git('commit-tree', tree, '-p', OLD, '-p', MAIN, data=b'Correct PR316 classical priority; preserve valid lacunary result and author 1/5\n').stdout.decode().strip()
    S = A / 'priority_corrected_snapshot'
    S.mkdir(exist_ok=False)
    files = []
    for path in sorted(changed):
        b = git('show', commit + ':' + path).stdout
        p = S / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
        files.append({'path': path, **pin(p), 'git_blob_sha': hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()})
    save(A / 'priority_corrected_snapshot_manifest.json', {'pr':316,'head':commit,'base':MAIN,'original_head':OLD,'utc':utc(),'files':files})
    require(local_state() == before, 'Main/index/tracked state changed')
    save(A / 'PRIORITY_CORRECTION_PUSH_INTENT.json', {'utc':utc(),'status':'PREPARED_PRIVATE_TREE_NO_BRANCH_PUSH','head':commit,'tree':tree,'parents':[OLD,MAIN],'branch':live['headRefName'],'expected_scope':sorted(changed),'preserved_historical_files':preserve,'queue_row':i+1,'old_main_row':prior.decode(),'new_row':lines[i].decode(),'queue_cells':[8,9],'all_other_queue_bytes_preserved':True,'packet':final['final_packet'],'snapshot_manifest':pin(A/'priority_corrected_snapshot_manifest.json'),'state_unchanged':before,'workflow_percent':85,'paper':False,'merge':False,'zenodo':False,'tracker':False})
    print(json.dumps({'status':'PREPARED_PRIVATE_TREE_NO_BRANCH_PUSH','commit':commit,'paths':len(changed),'preserved':len(preserve),'queue_row':i+1,'workflow_percent':85},indent=2))
else:
    intent = json.loads((A / 'PRIORITY_CORRECTION_PUSH_INTENT.json').read_bytes())
    gate = json.loads((A / 'ROOT_FINAL_CORRECTION_ACCEPTANCE.json').read_bytes())
    require(gate['status'] == 'PASS_FINAL_PRIORITY_CORRECTION_READY_FOR_BRANCH_UPDATE' and gate['final_packet'] == final['final_packet'], 'Final recheck not cleared')
    live = remote()
    require(live['state'] == 'OPEN' and live['isDraft'] and live['headRefOid'] == (OLD if MODE == 'publish' else intent['head']) and live['headRefName'] == intent['branch'], 'Live PR changed before push')
    require(before['main'] == intent['parents'][1] and text_git('rev-parse','origin/main') == before['main'], 'Main changed after preparation')
    require(text_git('show','-s','--format=%T',intent['head']) == intent['tree'], 'Commit tree changed')
    require(text_git('show','-s','--format=%P',intent['head']).split() == intent['parents'], 'Parents differ')
    if MODE == 'publish':
        git('push','origin',intent['head']+':refs/heads/'+intent['branch'])
    else:
        prior = A/'integration_publish_private/call_009'
        prior_execution = json.loads((prior/'execution.json').read_bytes())
        require(prior_execution['exit_code'] == 0 and prior_execution['argv'] == ['/usr/bin/git','push','origin',intent['head']+':refs/heads/'+intent['branch']], 'Original push not authenticated')
        require(prior_execution['stderr'] == pin(prior/'stderr.bin') and prior_execution['stdout'] == pin(prior/'stdout.bin'), 'Original push streams changed')
        require(git('ls-remote','origin','refs/heads/'+intent['branch']).stdout.decode().split()[0] == intent['head'], 'Remote Git head differs')
    pushed = remote()
    require(pushed['state'] == 'OPEN' and pushed['isDraft'] and pushed['headRefOid'] == intent['head'], 'Exact pushed head not yet authenticated; do not repeat push')
    title = (D / 'PR_TITLE.txt').read_text().rstrip('\n')
    body = (D / 'PR_BODY.md').read_text()
    gh('pr','edit','316','--title',title,'--body-file',str(D/'PR_BODY.md'))
    observed = remote()
    require(observed['state'] == 'OPEN' and observed['isDraft'] and observed['headRefOid'] == intent['head'] and observed['title'] == title and observed['body'] == body, 'PR readback differs')
    snap = json.loads((A/'priority_corrected_snapshot_manifest.json').read_bytes())
    for e in snap['files']:
        p = A/'priority_corrected_snapshot'/e['path']
        require(pin(p) == {k:e[k] for k in ['bytes','sha256']}, 'Frozen corrected bytes changed')
        api = json.loads(gh('api','repos/AlecKriebel/Math/contents/'+e['path']+'?ref='+intent['head']).stdout)
        require(api['encoding'] == 'base64' and api['sha'] == e['git_blob_sha'] and api['size'] == e['bytes'], 'API blob differs')
        require(base64.b64decode(api['content'],validate=False) == p.read_bytes(), 'API bytes differ')
    require(local_state() == before, 'Main/index/tracked work changed during publication')
    save(A/'PRIORITY_CORRECTION_DISPOSITION.json',{'utc':utc(),'status':'PASS_RECLASSIFIED_ALREADY_SOLVED_LEFT_DRAFT_BY_CLAIMED_ONLY_SCOPE','pr':316,'original_submitted_status':'claimed_solved','operational_status':'already_solved','author_turns':'1/5','head':intent['head'],'parents':intent['parents'],'exact_remote_readback':observed,'all_20_remote_files_exact':True,'all_15_historical_files_preserved':True,'queue_cells':[8,9],'all_other_queue_bytes_preserved':True,'nonforce_branch_push':True,'recovered_stale_PR_API_without_repeating_push':MODE == 'recover','shared_state_unchanged':before,'mathematical_percent':100,'bounded_priority_percent':100,'workflow_percent':100,'paper':False,'zenodo':False,'doi':None,'tracker':False,'merge':False,'close':False,'external_contact':False})
    print(json.dumps({'status':'PASS_RECLASSIFIED_ALREADY_SOLVED_LEFT_DRAFT_BY_CLAIMED_ONLY_SCOPE','head':intent['head'],'remote_paths':20,'workflow_percent':100,'paper':False,'merge':False},indent=2))
