"""Conditional PR209 native integration model: pure computation and file reads.

No service transport, object writer, reference writer, local view writer, retry,
or operational CLI exists. A caller can supply an explicitly GET-only observer.
Outputs describe conditional objects; they are never actual Root acceptance.
"""
import base64
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import types

BASE = Path(__file__).absolute().parent
PROGRAM = 'draft_pr_publication_program_20260930/'
CASE = PROGRAM + 'audits/pr209_5100015/'
ATTEMPT = 'unsolved_math_prioritization/attempts/5100015/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
SHARED = 'draft_pr_descending_audit_20261002/audits/pr209_5100015'
VIEWS = (CASE+'CURRENT_CASE_STATUS.json', CASE+'RESEARCH_LOG.md',
         PROGRAM+'CURRENT_PROGRESS.json', PROGRAM+'CURRENT_PROGRESS.md', PROGRAM+'RESEARCH_LOG.md')
ANCHOR = 'a687f7f4b7c374c6f29feb99b5d0e017833244e8'
ORIGINAL = 'fd09a95b479f376234835a4494693bb1316c85ec'
ORIGINAL_TREE = 'e9f6b84b7cc13e86b97ec63643df45192ff37286'
PREPARED = 'd827ae3c46c01ff68df7fd86f26b230c0ab2ac97'
PREPARED_TREE = '45a7675f752f1a76f59603ef5dfb024f1664f6a3'
ATTEMPT_TREE = '7bf7c70929c0b14b5851bb33795a7bf76bf6b929'
SHARED_TREE = 'd036a7d104ffe002a7a9ac6bfd58f65c583e6526'
CORE_PIN = {'bytes':4719, 'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}
BASELINE_PIN = {'bytes':1338,'sha256':'0ca1c963c1cea92117d575c52b1a95c63f199448c2c87543ae848669a93f039b'}
REFERENCE_PINS = {
    'ORIGINAL_NATIVE_REFERENCE.json': {'bytes':5681,'sha256':'876b1e4d1db387008dd7ca6e9dc6bfd9edf9e988c1646428080fa2e589b320a0'},
    'REVISED_NATIVE_REFERENCE.json': {'bytes':13954,'sha256':'a4ead521af0590ca37fff679ad5c778f74be68d97ee1f48d1a9d08aaca70a350'},
    'QUEUE_REFERENCE.json': {'bytes':1884,'sha256':'b86f404b732a50d847992cbc1002cd4321afb68fdae707f2772761c482e3ad9d'},
    'CUSTODY_BODY_IDENTITIES.json': {'bytes':22693,'sha256':'dc556edc0a4b522029d86541fa97912ebab58bce01994644eca9d0e912d63f12'},
    'EXISTING_SHARED_BODY_IDENTITIES.json': {'bytes':75972,'sha256':'db2923d46cd9abad2c77f0cabdbc19f33172d1ee1166f23b6a68bf136f473d59'},
}
QUEUED_ROW_PIN = {'bytes':123,'sha256':'ef14f13d87ad4f8e1f25b83bb340cac8cd865a5db957addde5d04a3606786768'}
REVISED_ROW_PIN = {'bytes':264,'sha256':'27e14c1a66988f027a9e07af5d32d8042d74f63706c169963ace981fd9f46c43'}
MAX_BODY = 4_000_000
MAX_FILES = 200
MAX_TOTAL = 8_000_000


def need(ok, message):
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def pin(raw):
    return {'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()}


def native(kind, raw):
    return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def decode(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def finite(value):
        result = float(value)
        need(math.isfinite(result), 'Nonfinite JSON number')
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite,
                      parse_constant=lambda _: need(False, 'Nonfinite JSON constant'))


def hexid(value, length=40):
    return type(value) is str and re.fullmatch('[0-9a-f]{'+str(length)+'}', value) is not None


def rel(value):
    need(type(value) is str and value and not PurePosixPath(value).is_absolute()
         and '\\' not in value and all(32 <= ord(c) != 127 for c in value)
         and all(p not in ('', '.', '..') for p in value.split('/'))
         and len(value.encode()) <= 4096, 'Unsafe relative path')
    return value


def bytepin(value):
    need(type(value) is dict and set(value) == {'bytes','sha256'}
         and type(value['bytes']) is int and 0 <= value['bytes'] <= MAX_BODY
         and hexid(value['sha256'], 64), 'Exact bounded byte pin required')
    return value


def tuple_pin(value):
    if value is None:
        return None
    need(type(value) is dict and set(value) == {'mode','type','sha'}
         and (value['mode'],value['type']) == ('100644','blob')
         and hexid(value['sha']), 'Exact regular native preimage required')
    return value['mode'],value['type'],value['sha']


def sealed(name, expected):
    path = BASE / rel(name)
    need(path.resolve() == path, 'Canonical owned source required')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) == 0o444
             and before.st_size <= MAX_BODY, 'Bounded readonly regular source required')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            raw = stream.read(MAX_BODY+1)
        after = os.fstat(fd)
        entry = path.lstat()
        attributes = lambda s: (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        need(attributes(before) == attributes(after) == attributes(entry)
             and stat.S_ISREG(entry.st_mode) and stat.S_IMODE(entry.st_mode) == 0o444
             and len(raw) == after.st_size, 'Source changed during read')
    finally:
        os.close(fd)
    need(pin(raw) == bytepin(expected), 'Pinned owned source changed')
    return raw


def core():
    raw = sealed('native_trees_readonly.py', CORE_PIN)
    result = types.ModuleType('pr209_readonly_native_trees')
    exec(compile(raw, str(BASE/'native_trees_readonly.py'), 'exec'), result.__dict__)
    return result


def matches(obj, expected, message):
    need(type(obj) is dict, message)
    for key, value in expected.items():
        need(type(obj.get(key)) is type(value) and obj[key] == value, message+': '+key)


def phase_facts(phase):
    need(phase in ('merge95','completion100'), 'Exactly two phases supported')
    done = phase == 'completion100'
    return {'active_PR':209, 'case_workflow_estimate_percent':100 if done else 95,
            'fully_completed_count':51 if done else 50, 'published_count':35,
            'last_completed_PR':209 if done else 207,
            'next_numeric_intake_cursor':210 if done else 209,
            'advance_to_next_PR_authorized_now':done, 'completed':done,
            'publication_ready':True, 'goal_complete':False}


def split_queue(raw):
    lines = raw.splitlines(keepends=True)
    rows = [i for i,line in enumerate(lines) if re.match(rb'^\|[^|]*\|\s*5100015\s*/', line)]
    need(len(rows) == 1, 'Exactly one own QUEUE row required')
    return lines,rows[0]


def queue_change(old, new, phase):
    before,i = split_queue(old)
    after,j = split_queue(new)
    need(i == j and len(before) == len(after) and before[:i] == after[:j]
         and before[i+1:] == after[j+1:], 'Foreign QUEUE bytes or row order changed')
    a,b = before[i].split(b'|'),after[j].split(b'|')
    need(len(a) == len(b) == 14 and b[8].strip() == b'claimed_solved'
         and b[9].strip() == b'1/5' and pin(after[j]) == REVISED_ROW_PIN,
         'Exact preserved ready-HEAD own row required')
    need(all(a[k] == b[k] for k in range(14) if k not in (8,9,11,12)),
         'Only own status/effort/findings/DOI cells may change')
    if phase == 'merge95':
        need(pin(before[i]) == QUEUED_ROW_PIN, 'Exact fresh MAIN queued0/5 row required')
    else:
        need(phase == 'completion100' and old == new, 'Completion QUEUE must be byteexact unchanged')


class GetOnly:
    """Route firewall, with no transport and no retry. Import is inert."""
    def __init__(self, observer):
        self.observer = observer
        self.failed = False

    def __call__(self, method, path, body=None):
        need(not self.failed, 'Observer stopped after first uncertainty')
        allowed = path in ('git/ref/heads/main','pulls/209') or re.fullmatch(
            r'git/(?:commits|trees|blobs)/[0-9a-f]{40}', path) is not None or re.fullmatch(
            r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}', path) is not None
        need(method == 'GET' and allowed and body is None, 'Only bounded native GET routes allowed')
        try:
            value = self.observer('GET', path)
            need(type(value) is dict, 'GET observation must be an object')
            return value
        except BaseException:
            self.failed = True
            raise


def read_blob(api, oid):
    need(hexid(oid), 'Native blob identity')
    j = api('GET','git/blobs/'+oid)
    need(j.get('sha') == oid and j.get('encoding') == 'base64'
         and type(j.get('size')) is int and 0 <= j['size'] <= MAX_BODY
         and type(j.get('content')) is str, 'Bounded full native blob required')
    body = base64.b64decode(''.join(j['content'].split()), validate=True)
    need(len(body) == j['size'] and native('blob', body) == oid, 'Native blob body differs')
    return body


def expected(c, trees, root, overlay, pre):
    """Exact-preimage rebuild adapted from audited native207_v2.expected."""
    trie,changed,dirs = {},set(),set()
    for path,body in overlay.items():
        parts = rel(path).split('/')
        need(len(parts)-1 <= c.MAX_DEPTH, 'Overlay depth bound')
        node = trie
        for name in parts[:-1]:
            need(name not in node or type(node[name]) is dict, 'Overlay ancestor/file collision')
            node = node.setdefault(name,{})
        need(parts[-1] not in node, 'Overlay leaf/ancestor collision')
        node[parts[-1]] = body
    def rebuild(oid, node, prefix, depth):
        need(depth <= c.MAX_DEPTH, 'Overlay recursion bound')
        entries = dict(trees.get(oid,depth)) if oid is not None else {}
        for name,body in node.items():
            path,old = prefix+name,entries.get(name)
            if type(body) is bytes:
                need(old == pre[path], 'Fresh native preimage differs: '+path)
                wanted = ('100644','blob',native('blob',body))
                if old != wanted:
                    changed.add(path)
                entries[name] = wanted
            else:
                need(old is None or old[:2] == ('040000','tree'), 'Overlay native ancestor is a leaf')
                if old is None:
                    dirs.add(path)
                entries[name] = ('040000','tree',rebuild(old[2] if old else None,body,path+'/',depth+1))
        return c.tree_hash([(name,*entry) for name,entry in entries.items()])
    return rebuild(root,trie,'',0),changed,dirs


def load_inputs(manifest_name, manifest_pin, acceptance_name, acceptance_pin):
    """No authority is inferred from peer reports or this model's output."""
    m = decode(sealed(manifest_name,manifest_pin))
    need(type(m) is dict and set(m) == {'schema','PR','problem_id','phase','helper_pin','core_pin','executor_pin',
         'expected_parent','expected_parent_tree','facts','files','reused_blobs','reused_trees',
         'local_views','commit_message','total_files','total_bytes','baseline_pin'}, 'Exact manifest fields')
    matches(m,{'schema':'pr209-native-conditional-inputs-v1','PR':209,'problem_id':'5100015',
               'core_pin':CORE_PIN}, 'Frozen manifest identity')
    helper = pin(sealed(Path(__file__).name,m['helper_pin']))
    sealed('native209_future_executor.py',m['executor_pin'])
    need(hexid(m['expected_parent']) and hexid(m['expected_parent_tree']), 'Explicit fresh parent/tree required')
    facts = phase_facts(m['phase'])
    need(set(m['facts']) == set(facts), 'Exact phase fact fields')
    matches(m['facts'],facts,'Exact phase facts')
    need(m['baseline_pin'] == BASELINE_PIN, 'Fixed accepted ascending membership baseline required')
    baseline = decode(sealed('BASELINE_MEMBERSHIP.json',BASELINE_PIN))
    need(baseline['dated_eligible_total'] == 99 and len(baseline['fully_completed_eligible_PRs']) == 50
         and len(baseline['published_PRs']) == 34 and 209 not in baseline['fully_completed_eligible_PRs']
         and 209 not in baseline['published_PRs'], 'Baseline membership identity')
    overlay,pre = {},{}
    rows = m['files']
    need(type(rows) is list and 60 <= len(rows) <= MAX_FILES, 'Bounded explicit own54+QUEUE+five+curated scope')
    for row in rows:
        need(type(row) is dict and set(row) == {'path','source','bytes','sha256','git_blob','preimage'}, 'Exact selected row fields')
        path = rel(row['path'])
        need(path not in overlay and (path.startswith(ATTEMPT) or path.startswith(CASE)
             or path in VIEWS[2:] or path == QUEUE), 'Foreign or duplicate overlay refused')
        need('/_private/' not in '/'+path and '/journal' not in path.lower(), 'Private journal excluded')
        body = sealed(row['source'],{k:row[k] for k in ('bytes','sha256')})
        need(native('blob',body) == row['git_blob'], 'Selected body/native blob mismatch')
        overlay[path],pre[path] = body,tuple_pin(row['preimage'])
    need(type(m['total_files']) is int and m['total_files'] == len(overlay)
         and type(m['total_bytes']) is int and m['total_bytes'] == sum(map(len,overlay.values())) <= MAX_TOTAL,
         'Exact bounded selected totals')
    references = {name:decode(sealed(name,wanted)) for name,wanted in REFERENCE_PINS.items()}
    revised = references['REVISED_NATIVE_REFERENCE.json']
    own = {x['path']:('100644','blob',x['git_object']) for x in revised['leaves']}
    need(revised['root_tree'] == PREPARED_TREE and revised['leaf_count'] == 54 and len(own) == 54
         and {p for p in overlay if p.startswith(ATTEMPT)} == set(own), 'Exactly prepared own54 selected')
    need(sum(len(overlay[p]) for p in own) == 205547, 'Exact own54 byte total')
    for path,value in own.items():
        need(('100644','blob',native('blob',overlay[path])) == value, 'Prepared own54 identity changed')
    bodies = references['CUSTODY_BODY_IDENTITIES.json']['inventories']
    for row in bodies['revised']:
        need(pin(overlay[row['path']]) == {k:row[k] for k in ('bytes','sha256')}, 'Prepared own54 SHA256 differs')
    original = references['ORIGINAL_NATIVE_REFERENCE.json']
    need(original['leaf_count'] == 23 and original['root_tree'] == ORIGINAL_TREE, 'Original23 identity')
    for row in original['leaves']:
        archive = ATTEMPT+'history/original_submission_20261016/'+row['path'][len(ATTEMPT):]
        need(native('blob',overlay[archive]) == row['git_object'] and row['mode'] == '100644'
             and row['type'] == 'blob', 'Original23 archive differs')
    for row in bodies['original']:
        archive = ATTEMPT+'history/original_submission_20261016/'+row['path'][len(ATTEMPT):]
        need(pin(overlay[archive]) == {k:row[k] for k in ('bytes','sha256')}, 'Original23 archive SHA256 differs')
    need(all(p in overlay for p in (*VIEWS,QUEUE)), 'Exact five views and QUEUE required')
    for path in (VIEWS[0],VIEWS[2]):
        obj = decode(overlay[path])
        matches(obj,facts,'Structured view facts')
        for alias,key in (('current_case_percent','case_workflow_estimate_percent'),
                          ('workflow_percent','case_workflow_estimate_percent'),
                          ('case_percent','case_workflow_estimate_percent'),
                          ('current_publication_ready','publication_ready')):
            if alias in obj:
                matches(obj,{alias:facts[key]},'Structured view alias')
    progress = decode(overlay[VIEWS[2]])
    for key in ('fully_completed_eligible_PRs','published_PRs'):
        wanted = baseline[key] + ([209] if key == 'published_PRs' or m['phase'] == 'completion100' else [])
        need(progress.get(key) == wanted, 'Exact ascending membership preservation: '+key)
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total'] == 99,
         'Dated denominator99 preserved')
    if 'fully_completed_fraction_percent' in progress:
        value = progress['fully_completed_fraction_percent']
        need(type(value) in (int,float) and math.isfinite(value)
             and abs(value-100*facts['fully_completed_count']/99) < 1e-12, 'Completion fraction alias')
    marker = ('<!-- PR209_NATIVE_PHASE_FACTS '+compact(facts)+' -->').encode()
    for path in (VIEWS[1],VIEWS[3],VIEWS[4]):
        need(overlay[path].count(b'<!-- PR209_NATIVE_PHASE_FACTS ') == 1
             and marker in overlay[path].splitlines(), 'Exact markdown phase marker')
    local = m['local_views']
    need(type(local) is list and len(local) == 5 and {r['path'] for r in local} == set(VIEWS), 'Exact five local preimages')
    for row in local:
        need(type(row) is dict and set(row) == {'path','preimage','source'}, 'Exact local preimage fields')
        if row['preimage'] is None:
            need(row['source'] is None, 'Absent local source must be null')
        else:
            before = sealed(row['source'],bytepin(row['preimage']))
            if row['path'] in (VIEWS[1],VIEWS[4]):
                need(overlay[row['path']].startswith(before), 'Research log historical local prefix changed')
    need(type(m['commit_message']) is str and 1 <= len(m['commit_message'].encode()) <= 1000
         and '\0' not in m['commit_message'], 'Bounded explicit commit message')
    reused = {}
    need(type(m['reused_blobs']) is list and 225 <= len(m['reused_blobs']) <= 300, 'Explicit existing science closure required')
    need(m['reused_blobs'] == references['EXISTING_SHARED_BODY_IDENTITIES.json']['files'],
         'Exact225 existing science bodies plus three existing documentary bodies required')
    for row in m['reused_blobs']:
        need(type(row) is dict and set(row) == {'path','bytes','sha256','git_blob'}, 'Exact reused body fields')
        path = rel(row['path'])
        need(path.startswith(SHARED+'/') and '/private_render_' not in path and path not in overlay and path not in reused,
             'Only explicit existing shared science/publication bodies reused')
        bytepin({k:row[k] for k in ('bytes','sha256')})
        need(hexid(row['git_blob']), 'Reused blob identity')
        reused[path] = row
    need(m['reused_trees'] == [{'path':SHARED,'mode':'040000','type':'tree','sha':SHARED_TREE}],
         'Existing shared case must remain opaque and byte/mode identical')
    a = decode(sealed(acceptance_name,acceptance_pin))
    matches(a,{'schema':'pr209-root-native-conditional-model-acceptance-v1',
               'evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':209,'phase':m['phase'],'accepted':True,
               'manifest_pin':manifest_pin,'helper_pin':helper,'core_pin':CORE_PIN,'executor_pin':m['executor_pin'],'facts':facts,
               'scientific_accepted':True,'priority_accepted':True,'whole_package_reviews_accepted':True,
               'existing_publication_verified':True,'existing_tracker_verified':True,
               'native_custody_accepted':True,'no_new_publication_or_tracker_action':True,
               'original_head':ORIGINAL,'prepared_head':PREPARED,'prepared_tree':PREPARED_TREE},
            'Actual external Root acceptance required; peer status grants no authority')
    need(type(a.get('facts')) is dict and set(a['facts']) == set(facts), 'Root exact fact fields')
    matches(a['facts'],facts,'Root fact types')
    audits = a.get('native_audits')
    need(type(audits) is list and len(audits) == 2 and len({r['path'] for r in audits}) == 2,
         'Two distinct fresh native source/manifest audits accepted by Root required')
    for row in audits:
        need(type(row) is dict and set(row) == {'path','bytes','sha256','Root_accepted','helper_pin','executor_pin','manifest_pin'}
             and row['Root_accepted'] is True and row['helper_pin'] == helper
             and row['executor_pin'] == m['executor_pin'] and row['manifest_pin'] == manifest_pin, 'Native audit binding differs')
        sealed(row['path'],{k:row[k] for k in ('bytes','sha256')})
    roles = {'scientific','priority','whole_package_one','whole_package_two','existing_publication',
             'existing_tracker','custody','PR208_status_skip'}
    if m['phase'] == 'completion100':
        roles |= {'actual_merge95_acceptance','actual_original_PR_merge','actual_merge95_five_sync'}
    receipts = a.get('receipts')
    need(type(receipts) is dict and set(receipts) == roles, 'Exact actual Root evidence roles')
    selected = {p:pin(body) for p,body in overlay.items()}
    selected.update({p:{k:r[k] for k in ('bytes','sha256')} for p,r in reused.items()})
    for role,row in receipts.items():
        need(type(row) is dict and set(row) == {'path','bytes','sha256'}
             and row['path'] in selected and selected[row['path']] == {k:row[k] for k in ('bytes','sha256')},
             'Root accepted evidence must be explicitly native-selected: '+role)
    return core(),m,overlay,pre,reused


def state(c,m,overlay,pre,reused,observer,after_ref=False):
    need(type(after_ref) is bool, 'Explicit readback mode')
    api = GetOnly(observer)
    parent = m['expected_parent']
    observed = api('GET','git/ref/heads/main')['object']['sha']
    if not after_ref:
        need(observed == parent, 'Fresh MAIN lease differs')
    commit = api('GET','git/commits/'+parent)
    need(commit.get('sha') == parent and commit['tree']['sha'] == m['expected_parent_tree'], 'Fresh parent/tree differs')
    if parent != ANCHOR:
        comparison = api('GET','compare/'+ANCHOR+'...'+parent)
        need(comparison.get('status') == 'ahead' and comparison['merge_base_commit']['sha'] == ANCHOR,
             'Fresh parent must descend from actual accepted PR207 checkpoint')
    original = api('GET','git/commits/'+ORIGINAL)
    prepared = api('GET','git/commits/'+PREPARED)
    need(original.get('sha') == ORIGINAL and original['tree']['sha'] == ORIGINAL_TREE
         and prepared.get('sha') == PREPARED and prepared['tree']['sha'] == PREPARED_TREE
         and [r['sha'] for r in prepared['parents']] == [ORIGINAL,'53b8291b2247008172f1fc3f596c96708faf8903'],
         'Preserved/prepared native custody identity')
    pr = api('GET','pulls/209')
    need(type(pr.get('number')) is int and pr['number'] == 209 and pr['head']['sha'] == PREPARED
         and pr['base']['ref'] == 'main' and pr.get('draft') is False, 'Ready PR209 identity differs')
    merged = pr.get('state') == 'closed' and pr.get('merged') is True and hexid(pr.get('merge_commit_sha'))
    opened = pr.get('state') == 'open' and pr.get('merged') is False
    need(merged if m['phase'] == 'completion100' else (opened or (after_ref and merged)), 'Actual PR merge phase differs')
    if m['phase'] == 'completion100':
        comparison = api('GET','compare/'+PREPARED+'...'+parent)
        need(comparison.get('status') == 'ahead' and comparison['merge_base_commit']['sha'] == PREPARED,
             'Prepared HEAD must be ancestor of completion parent')
    trees = c.NativeTrees(api)
    need(trees.lookup(m['expected_parent_tree'],SHARED) == ('040000','tree',SHARED_TREE), 'Shared science/publication tree differs')
    old_attempt = trees.lookup(m['expected_parent_tree'],ATTEMPT[:-1])
    need(old_attempt in (None,('040000','tree',ATTEMPT_TREE)), 'Existing own subtree has unexpected contents/modes')
    if m['phase'] == 'completion100':
        need(old_attempt == ('040000','tree',ATTEMPT_TREE), 'Completion own54 absent')
    wanted,changed,dirs = expected(c,trees,m['expected_parent_tree'],overlay,pre)
    need(pre[QUEUE] is not None, 'QUEUE cannot be added')
    queue_change(read_blob(api,pre[QUEUE][2]),overlay[QUEUE],m['phase'])
    for path in (VIEWS[1],VIEWS[4]):
        if pre[path] is not None:
            need(overlay[path].startswith(read_blob(api,pre[path][2])), 'Native research-log prefix changed')
    for path,row in reused.items():
        need(trees.lookup(m['expected_parent_tree'],path) == ('100644','blob',row['git_blob']), 'Reused native tuple differs')
        need(pin(read_blob(api,row['git_blob'])) == {k:row[k] for k in ('bytes','sha256')}, 'Reused full body differs')
    if not after_ref:
        need(api('GET','git/ref/heads/main')['object']['sha'] == parent, 'Fresh MAIN lease lost')
    return {'api':api,'parent':parent,'parent_tree':m['expected_parent_tree'],'wanted':wanted,
            'changed':changed,'dirs':dirs,'parents':[parent,PREPARED] if m['phase'] == 'merge95' else [parent]}


def plan(c,m,overlay,pre,reused,observer):
    s = state(c,m,overlay,pre,reused,observer)
    return {'schema':'pr209-native-conditional-plan-v1','evidence_scope':'CONDITIONAL_MODEL_NOT_ACTUAL_ACCEPTANCE',
            'phase':m['phase'],'facts':m['facts'],'parent':s['parent'],'parent_tree':s['parent_tree'],
            'modeled_commit':{'message':m['commit_message'],'tree':s['wanted'],'parents':s['parents']},
            'modeled_tree':{'base_tree':s['parent_tree'],'tree':[
                {'path':p,'mode':'100644','type':'blob','sha':native('blob',body)} for p,body in sorted(overlay.items())]},
            'changed_leaves':sorted(s['changed']),'new_directories':sorted(s['dirs']),
            'selected_files':len(overlay),'selected_bytes':sum(map(len,overlay.values())),
            'reused_body_files':len(reused),'shared_tree_preserved':SHARED_TREE,
            'native_objects_created':False,'ref_actions_performed':False,'local_views_modified':False,
            'publication_or_tracker_actions_performed':False,'actual_acceptance_inferred':False}


def verify(c,m,overlay,pre,reused,observer,candidate,after_ref=False):
    need(hexid(candidate), 'Explicit candidate native commit identity required')
    s = state(c,m,overlay,pre,reused,observer,after_ref)
    api = s['api']
    commit = api('GET','git/commits/'+candidate)
    need(commit.get('sha') == candidate and commit['tree']['sha'] == s['wanted']
         and [r['sha'] for r in commit['parents']] == s['parents']
         and commit.get('message') == m['commit_message'], 'Exact candidate parents/tree/message differ')
    trees = c.NativeTrees(api)  # Independent from construction/state cache.
    leaves,dirs,deleted = trees.changes(s['parent_tree'],s['wanted'])
    need(leaves == s['changed'] and dirs == s['dirs'] and not deleted, 'Full foreign/native changed scope differs')
    need(trees.lookup(s['wanted'],ATTEMPT[:-1]) == ('040000','tree',ATTEMPT_TREE), 'Candidate own54 is not exact')
    need(trees.lookup(s['wanted'],SHARED) == ('040000','tree',SHARED_TREE), 'Candidate shared case changed')
    selected = {}
    for path,body in sorted(overlay.items()):
        oid = native('blob',body)
        need(trees.lookup(s['wanted'],path) == ('100644','blob',oid), 'Selected native tuple differs')
        need(read_blob(api,oid) == body, 'Selected full native body differs')
        selected[path] = {**pin(body),'mode':'100644','type':'blob','git_blob':oid}
    for path,row in reused.items():
        need(trees.lookup(s['wanted'],path) == ('100644','blob',row['git_blob']), 'Candidate reused tuple differs')
        need(pin(read_blob(api,row['git_blob'])) == {k:row[k] for k in ('bytes','sha256')}, 'Candidate reused full body differs')
        selected[path] = {**{k:row[k] for k in ('bytes','sha256')},'mode':'100644','type':'blob','git_blob':row['git_blob']}
    observed = api('GET','git/ref/heads/main')['object']['sha']
    need(observed == (candidate if after_ref else s['parent']), 'Final MAIN identity differs')
    return {'schema':'pr209-native-conditional-verification-v1','evidence_scope':'GET_OBSERVATIONS_REQUIRE_ROOT_ACCEPTANCE',
            'phase':m['phase'],'facts':m['facts'],'parent':s['parent'],'parent_tree':s['parent_tree'],
            'candidate':candidate,'tree':s['wanted'],'parents':s['parents'],'selected_files':selected,
            'selected_file_count':len(selected),'selected_bytes':sum(row['bytes'] for row in selected.values()),
            'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'deleted_directories':[],
            'full_scope_verified':True,'all_selected_native_bodies_verified':True,
            'foreign_native_tuples_preserved':True,'shared_tree_preserved':SHARED_TREE,
            'actual_MAIN_observed':observed,'native_objects_created':False,'ref_actions_performed':False,
            'local_views_modified':False,'actual_acceptance_inferred':False}
