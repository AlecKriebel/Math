"""Conditional PR210 already-merged final adoption model: pure computation and file reads.

No service transport, object writer, reference writer, local view writer, retry,
or operational CLI exists. A caller can supply an explicitly GET-only observer.
Outputs describe conditional objects; they are never actual Root acceptance.
"""
import base64
import calendar
import datetime
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
CASE = PROGRAM + 'audits/pr210_5100033/'
ATTEMPT = 'unsolved_math_prioritization/attempts/5100033/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
SHARED = 'draft_pr_descending_audit_20261002/audits/pr210_5100033'
VIEWS = (CASE+'CURRENT_CASE_STATUS.json', CASE+'RESEARCH_LOG.md',
         PROGRAM+'CURRENT_PROGRESS.json', PROGRAM+'CURRENT_PROGRESS.md', PROGRAM+'RESEARCH_LOG.md')
ANCHOR = '4477f00e0e27b185751b74f3ed7340ea3eccea0c'
ORIGINAL = '2180d64b648b81ac660a792f7823d0b715f9cf12'
ORIGINAL_TREE = 'd9b7b638b86248c62055acfe32e7f56c78a44730'
PREPARED = '27af3971bac399df78a397328f08d6633b6e13e8'
PREPARED_TREE = '20c0de1a0abb29ff1557e0c40ff194a0b1ec1941'
MERGED = '15cfbc62df85b211d6a5cbf257d25df06b4a044c'
MERGE_FIRST_PARENT = 'dbc32c6009c06b1cccfb8d123ebbf0decc2f02b2'
MERGED_AT = '2026-10-16T04:24:41Z'
ATTEMPT_TREE = '91980171ac7ae383d63ee8767b0520c45dd13207'
SHARED_TREE = '886e4b07e68b85d588e3d37d353e8898c6fcfbe8'
CORE_PIN = {'bytes':4719,'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}
BASELINE_PIN = {'bytes':1067,'sha256':'e985bbe84c9b056056ae47b4cd7863d3e7bdbdaf3ee1fe36b9e76e2723556b75'}
PROTECTED_REFERENCE_PIN = {'bytes':1978,'sha256':'63e7a16fb847284d87984b6d64d094dcf6120e7c939eead74c216f1dfd841819'}
LATE_ROOT_ALLOWLIST = {
    PROGRAM+'audits/pr209_5100015/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json':
        {'bytes':5452,'sha256':'1b735d456cedb146c25ebacc46912c8d539408be6861f43e244f8602b66c2b29'},
    PROGRAM+'ordered_intakes_after_PR209_20261017/PR210_PRESERVED_STATUS_INTAKE.json':
        {'bytes':24375,'sha256':'8d7b46458a82da6e9a3fe46528e7e28d5f92d44d6570dc87980961fa0cab27cb'},
}
PUBLIC_PINNED_EXCEPTIONS = {CASE+path:value for path,value in {'native_custody_01/PRIVATE_CUSTODY_BINDINGS.json': {'bytes': 1107, 'sha256': 'b55a0eb28bf236edecb6ae6c10da96b6bb47969c05435af8cb44ff798e12a367'}, 'native_custody_01/archive/native_commits/15cfbc62df85b211d6a5cbf257d25df06b4a044c.commit': {'bytes': 1237, 'sha256': 'af7cf049d6ab9edb9e828ad382739004e2463f52510f8af1c88dc7f5f57ba6d0'}, 'native_custody_01/archive/native_commits/2180d64b648b81ac660a792f7823d0b715f9cf12.commit': {'bytes': 273, 'sha256': '995e2cdeef1a4b51f00287e04453b7cfadff0855a2033292fbb0a39332038058'}, 'native_custody_01/archive/native_commits/27af3971bac399df78a397328f08d6633b6e13e8.commit': {'bytes': 386, 'sha256': '1d927702e6852e054aadd1493ba3c18a9cb9b729b99c1fe18cb7d1738a03c4cf'}, 'native_custody_01/archive/native_commits/308c0268f78fe345f5bb2f37f7ef21230e0d35af.commit': {'bytes': 291, 'sha256': '47601af30de8fdd2f0c9d7227cf6540c52be9abcb4f489f88d6a38a1401700b3'}, 'native_custody_01/archive/native_commits/4477f00e0e27b185751b74f3ed7340ea3eccea0c.commit': {'bytes': 348, 'sha256': '32be8fe26470d489d64ff063afec108440599fd7a555a6dba0da895dc8fd4536'}, 'native_custody_01/archive/native_commits/462ac1846ea0abc36cb0e617d05c120351d943a0.commit': {'bytes': 296, 'sha256': 'f5ea638aa48a09139fd0af452eb40f40f9d64b9c02a328cb7a37e407c511441e'}, 'native_custody_01/archive/native_commits/dbc32c6009c06b1cccfb8d123ebbf0decc2f02b2.commit': {'bytes': 555, 'sha256': 'db5ec7d1a49e86887907136ccb2b607d865aac5396af0e3e6df6b139922fda61'}, 'native_custody_01/archive/published/k605a-source-verification.zip': {'bytes': 604537, 'sha256': 'ae127ebe4d8962c1fe8894db16da72a6e215ddb51a6699804b26c6ace0143290'}, 'native_custody_01/archive/published/manuscript.pdf': {'bytes': 90186, 'sha256': 'efa4617d9b3ce2091afe472eb35b5144ec30f3117ffac22dc201498f95a0b731'}, 'native_custody_01/archive/published/manuscript.tex': {'bytes': 19892, 'sha256': '71e45462370c5314a2e43cc43678571931f8dc177536637e24cea050034b496e'}}.items()}
MAX_BODY = 4_000_000
WRITER_LOCK_REFERENCE = {'path':PROGRAM+'ROOT_GLOBAL_FIVE_WRITER.lock','device':16777232,
    'inode':439078796,'bytes':153,'sha256':'61404e167a3dedccc0fd17a1a1823fd772bc12a9144a4f012ab26d5e2a26fc0a'}
MAX_FILES = 600
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


def exact(left,right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact(left[k],right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact(a,b) for a,b in zip(left,right))
    return left == right


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
    handles = []
    fd = None
    try:
        current = Path('/')
        parentfd = os.open(current,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        handles.append((current,parentfd,os.fstat(parentfd)))
        for part in path.parent.parts[1:]:
            current = current/part
            parentfd = os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parentfd)
            handles.append((current,parentfd,os.fstat(parentfd)))
        fd = os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parentfd)
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
        for ancestor,descriptor,initial in handles:
            now,linked = os.fstat(descriptor),ancestor.lstat()
            need(stat.S_ISDIR(now.st_mode) and stat.S_ISDIR(linked.st_mode)
                 and (now.st_dev,now.st_ino) == (initial.st_dev,initial.st_ino) == (linked.st_dev,linked.st_ino),
                 'Owned source ancestor changed')
    finally:
        if fd is not None:
            os.close(fd)
        for ancestor,descriptor,initial in reversed(handles):
            os.close(descriptor)
    need(pin(raw) == bytepin(expected), 'Pinned owned source changed')
    return raw


def core():
    raw = sealed('native_trees_readonly.py', CORE_PIN)
    result = types.ModuleType('pr210_readonly_native_trees')
    exec(compile(raw, str(BASE/'native_trees_readonly.py'), 'exec'), result.__dict__)
    return result


def matches(obj, expected, message):
    need(type(obj) is dict, message)
    for key, value in expected.items():
        need(key in obj and exact(obj[key],value), message+': '+key)



def phase_facts(phase):
    need(phase == 'adoption100', 'Only final already-merged adoption100 supported')
    return {'active_PR':210,'case_workflow_estimate_percent':100,
            'fully_completed_count':52,'published_count':36,'last_completed_PR':210,
            'next_numeric_intake_cursor':211,'advance_to_next_PR_authorized_now':True,
            'completed':True,'publication_ready':True,'goal_complete':False}


def baseline_facts():
    return {'active_PR':209,'case_workflow_estimate_percent':100,
            'fully_completed_count':51,'published_count':35,'last_completed_PR':209,
            'next_numeric_intake_cursor':210,'advance_to_next_PR_authorized_now':True,
            'completed':True,'publication_ready':True,'goal_complete':False}


def phase_marker(phase):
    return ('<!-- PR210_NATIVE_PHASE_FACTS '+compact(phase_facts(phase))+' -->').encode()



def markdown_current(raw,phase,append_log):
    """The single PR210 terminal marker is current; prior PR209 bytes stay historical."""
    need(type(raw) is bytes and type(append_log) is bool, 'Explicit Markdown body/log policy')
    current = phase_marker(phase)
    prefix = b'<!-- PR210_NATIVE_PHASE_FACTS'
    lines = raw.splitlines()
    while lines and lines[-1] == b'':
        lines.pop()
    markers = [line for line in lines if line.startswith(prefix)]
    need(raw.count(prefix) == len(markers) == 1 and markers == [current]
         and bool(lines) and lines[-1] == current,
         'Exactly one canonical terminal PR210 marker; malformed/duplicate/stale markers refused')


def commit_request(m,tree,parents):
    def identity(value):
        need(type(value) is dict and set(value) == {'name','email','date'}, 'Explicit fixed commit identity')
        for key in ('name','email'):
            text = value[key]
            need(type(text) is str and 1 <= len(text.encode()) <= 200
                 and all(ord(ch) >= 32 and ch not in '<>\x7f' for ch in text), 'Safe fixed author/committer text')
        need(type(value['date']) is str and re.fullmatch(r'20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z',value['date']) is not None,
             'Explicit second-precision UTC commit date required')
        parsed = datetime.datetime.strptime(value['date'],'%Y-%m-%dT%H:%M:%SZ')
        seconds = calendar.timegm(parsed.timetuple())
        return value['name']+' <'+value['email']+'> '+str(seconds)+' +0000'
    need(hexid(tree) and type(parents) is list and 1 <= len(parents) <= 2
         and all(hexid(p) for p in parents), 'Exact deterministic commit tree/parents')
    author,committer = identity(m['commit_author']),identity(m['commit_committer'])
    message = m['commit_message']
    need(type(message) is str and 1 <= len(message.encode()) <= 1000
         and message.endswith('\n') and '\r' not in message and '\0' not in message,
         'Explicit newline-terminated deterministic commit message required')
    raw = ('tree '+tree+'\n'+''.join('parent '+p+'\n' for p in parents)
           +'author '+author+'\ncommitter '+committer+'\n\n'+message).encode()
    request = {'message':message,'tree':tree,'parents':parents,
               'author':m['commit_author'],'committer':m['commit_committer']}
    return request,native('commit',raw)



def public_payload_path(path):
    if not path.startswith(CASE) or path in VIEWS:
        return False
    if path in PUBLIC_PINNED_EXCEPTIONS:
        return True
    parts = path[len(CASE):].split('/')
    forbidden = ('private','_private','packet','journal','_runtime','runtime')
    if any(p.lower().startswith(forbidden) or p.lower() in ('extracted','objects','inputs','_synthetic') for p in parts):
        return False
    return Path(path).suffix.lower() in ('.json','.md','.py','.txt','.patch','.sha256') or parts[-1] == '.gitignore'





class GetOnly:
    """Route firewall, with no transport and no retry. Import is inert."""
    def __init__(self, observer):
        self.observer = observer
        self.failed = False

    def __call__(self, method, path, body=None):
        need(not self.failed, 'Observer stopped after first uncertainty')
        allowed = path in ('git/ref/heads/main','pulls/210') or re.fullmatch(
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
    """Conditional exact inputs only; never authority from peer status or source self-tests."""
    m = decode(sealed(manifest_name,manifest_pin))
    need(type(m) is dict and set(m) == {'schema','PR','problem_id','phase','helper_pin','core_pin','executor_pin',
         'expected_parent','expected_parent_tree','facts','files','public_allowlist','protected_queue',
         'reused_blobs','reused_trees','local_views','commit_message','commit_author','commit_committer',
         'candidate_journal','writer_lock','total_files','total_bytes','baseline_pin','protected_reference_pin'},
         'Exact final adoption manifest fields')
    matches(m,{'schema':'pr210-native-adoption-inputs-v1','PR':210,'problem_id':'5100033',
               'core_pin':CORE_PIN,'baseline_pin':BASELINE_PIN,'protected_reference_pin':PROTECTED_REFERENCE_PIN},
            'Frozen final adoption manifest identity')
    helper = pin(sealed(Path(__file__).name,m['helper_pin']))
    sealed('native210_future_executor.py',m['executor_pin'])
    need(exact(m['writer_lock'],WRITER_LOCK_REFERENCE), 'Pinned original stable writer lock identity required')
    need(type(m['candidate_journal']) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,79}',m['candidate_journal']) is not None,
         'Exactly one manifest-bound candidate journal required')
    need(hexid(m['expected_parent']) and hexid(m['expected_parent_tree']), 'Explicit fresh parent/tree required')
    facts = phase_facts(m['phase'])
    need(type(m['facts']) is dict and set(m['facts']) == set(facts) and exact(m['facts'],facts), 'Exact final adoption facts')
    baseline = decode(sealed('BASELINE_MEMBERSHIP.json',BASELINE_PIN))
    need(type(baseline.get('dated_eligible_total')) is int and baseline['dated_eligible_total'] == 99
         and len(baseline['fully_completed_eligible_PRs']) == 51 and len(baseline['published_PRs']) == 35
         and 210 not in baseline['fully_completed_eligible_PRs'] and 210 not in baseline['published_PRs'], 'Fixed baseline membership')
    reference = decode(sealed('PROTECTED_NATIVE_REFERENCE.json',PROTECTED_REFERENCE_PIN))
    need(exact(reference['own_attempt']['tuple'],['040000','tree',ATTEMPT_TREE])
         and exact(reference['shared_audit']['tuple'],['040000','tree',SHARED_TREE])
         and reference['anchor'] == ANCHOR, 'Protected immutable reference differs')
    queue = tuple_pin(m['protected_queue'])
    need(queue is not None, 'Exact existing whole-QUEUE tuple required')
    need(exact(m['reused_blobs'],[]), 'No redundant unchanged scientific body selection or fetch')
    need(exact(m['reused_trees'],[
         {'path':ATTEMPT[:-1],'mode':'040000','type':'tree','sha':ATTEMPT_TREE},
         {'path':SHARED,'mode':'040000','type':'tree','sha':SHARED_TREE}]), 'Exact protected own47 and existing published audit trees')
    public = m['public_allowlist']
    need(type(public) is list and 1 <= len(public) <= MAX_FILES-5 and all(type(p) is str for p in public)
         and len(set(public)) == len(public) and public == sorted(public)
         and all(public_payload_path(rel(p)) for p in public), 'Finite positive public payload allowlist required')
    overlay,pre = {},{}
    rows = m['files']
    need(type(rows) is list and 6 <= len(rows) <= MAX_FILES, 'Bounded exact five-plus-public final scope')
    for row in rows:
        need(type(row) is dict and set(row) == {'path','source','bytes','sha256','git_blob','preimage'}, 'Exact selected row fields')
        path = rel(row['path'])
        need(path not in overlay and (path in public or path in VIEWS or path in LATE_ROOT_ALLOWLIST),
             'Foreign, private, working or duplicate overlay refused')
        body = sealed(row['source'],{k:row[k] for k in ('bytes','sha256')})
        need(native('blob',body) == row['git_blob'], 'Selected body/native blob mismatch')
        if path in PUBLIC_PINNED_EXCEPTIONS:
            need(exact(pin(body),PUBLIC_PINNED_EXCEPTIONS[path]), 'Exact reviewed public custody exception bytes required')
        overlay[path],pre[path] = body,tuple_pin(row['preimage'])
        if path not in VIEWS:
            need(pre[path] in (None,('100644','blob',native('blob',body))),
                 'Public archive/late receipts may only be added or preserved exact, never replaced')
        if path in LATE_ROOT_ALLOWLIST:
            need(exact(pin(body),LATE_ROOT_ALLOWLIST[path]), 'Exact late Root receipt body required')
    need({p for p in overlay if p not in VIEWS and p not in LATE_ROOT_ALLOWLIST} == set(public)
         and all(p in overlay for p in VIEWS), 'Exact finite public payloads plus all five views required')
    need(type(m['total_files']) is int and m['total_files'] == len(overlay)
         and type(m['total_bytes']) is int and m['total_bytes'] == sum(map(len,overlay.values())) <= MAX_TOTAL,
         'Exact bounded selected totals')
    for path in (VIEWS[0],VIEWS[2]):
        obj = decode(overlay[path]);matches(obj,facts,'Structured adoption view facts')
        for alias,key in (('current_PR','active_PR'),('PR','active_PR'),
                          ('current_case_percent','case_workflow_estimate_percent'),
                          ('workflow_percent','case_workflow_estimate_percent'),('case_percent','case_workflow_estimate_percent'),
                          ('current_publication_ready','publication_ready')):
            if alias in obj:matches(obj,{alias:facts[key]},'Structured view alias')
    progress = decode(overlay[VIEWS[2]])
    for key in ('fully_completed_eligible_PRs','published_PRs'):
        need(exact(progress.get(key),baseline[key]+[210]), 'Exact ascending membership preserved: '+key)
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total'] == 99, 'Dated denominator99 preserved')
    if 'fully_completed_fraction_percent' in progress:
        value = progress['fully_completed_fraction_percent']
        need(type(value) in (int,float) and math.isfinite(value) and abs(value-5200/99) < 1e-12, 'Completion fraction alias')
    for path in (VIEWS[1],VIEWS[3],VIEWS[4]):
        markdown_current(overlay[path],m['phase'],path in (VIEWS[1],VIEWS[4]))
    local = m['local_views']
    need(type(local) is list and len(local) == 5 and all(type(r) is dict for r in local)
         and {r.get('path') for r in local} == set(VIEWS), 'Exact five separate local preimages')
    for row in local:
        need(set(row) == {'path','preimage','source'}, 'Exact local preimage fields')
        if row['preimage'] is None:need(row['source'] is None, 'Absent local source must be null')
        else:
            before = sealed(row['source'],bytepin(row['preimage']))
            if row['path'] in (VIEWS[1],VIEWS[4]):
                need(overlay[row['path']].startswith(before), 'Existing local research-log prefix changed')
    commit_request(m,'0'*40,['1'*40])
    a = decode(sealed(acceptance_name,acceptance_pin))
    matches(a,{'schema':'pr210-root-native-adoption-model-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
               'PR':210,'phase':'adoption100','accepted':True,'manifest_pin':manifest_pin,'helper_pin':helper,
               'core_pin':CORE_PIN,'executor_pin':m['executor_pin'],'facts':facts,
               'scientific_accepted':True,'priority_accepted':True,'whole_package_reviews_accepted':True,
               'existing_publication_verified':True,'existing_tracker_verified':True,'native_custody_accepted':True,
               'no_new_publication_or_tracker_action':True,'public_selection_reviewed':True,
               'original_PR_already_merged':True,'original_merge_commit':MERGED,
               'original_head':ORIGINAL,'prepared_head':PREPARED,'prepared_tree':PREPARED_TREE},
            'Actual external Root adoption acceptance required; peer status grants no authority')
    need(type(a.get('facts')) is dict and exact(a['facts'],facts), 'Root exact typed adoption fact fields')
    audits = a.get('native_audits')
    need(type(audits) is list and len(audits) == 2 and all(type(r) is dict for r in audits)
         and len({r.get('path') for r in audits}) == 2, 'Two distinct fresh Root-accepted source/exact-manifest audits required')
    for row in audits:
        need(set(row) == {'path','bytes','sha256','Root_accepted','helper_pin','executor_pin','manifest_pin'}
             and row['Root_accepted'] is True and exact(row['helper_pin'],helper)
             and exact(row['executor_pin'],m['executor_pin']) and exact(row['manifest_pin'],manifest_pin), 'Native audit binding differs')
        sealed(row['path'],{k:row[k] for k in ('bytes','sha256')})
    receipts = a.get('receipts')
    roles = {'scientific','priority','whole_package_one','whole_package_two','existing_publication',
             'existing_tracker','custody','actual_prior209_completion','PR210_status_intake'}
    need(type(receipts) is dict and set(receipts) == roles, 'Exact actual Root evidence roles')
    selected = {p:pin(body) for p,body in overlay.items()}
    for role,row in receipts.items():
        need(type(row) is dict and set(row) == {'path','bytes','sha256'} and row['path'] in selected
             and exact(selected[row['path']],{k:row[k] for k in ('bytes','sha256')}), 'Root evidence must be explicitly selected: '+role)
    need(receipts['whole_package_one']['path'] != receipts['whole_package_two']['path'],
         'Two distinct new whole-package receipt paths required')
    return core(),m,overlay,pre,{}



def pr_identity(api,m,after_ref=False):
    original = api('GET','git/commits/'+ORIGINAL)
    prepared = api('GET','git/commits/'+PREPARED)
    merged = api('GET','git/commits/'+MERGED)
    need(original.get('sha') == ORIGINAL and original['tree']['sha'] == ORIGINAL_TREE
         and [r['sha'] for r in original['parents']] == ['462ac1846ea0abc36cb0e617d05c120351d943a0']
         and prepared.get('sha') == PREPARED and prepared['tree']['sha'] == PREPARED_TREE
         and [r['sha'] for r in prepared['parents']] == [ORIGINAL,MERGE_FIRST_PARENT]
         and merged.get('sha') == MERGED and merged['tree']['sha'] == PREPARED_TREE
         and [r['sha'] for r in merged['parents']] == [MERGE_FIRST_PARENT,PREPARED],
         'Preserved/prepared/actual merged native metadata identity differs')
    pr = api('GET','pulls/210')
    need(type(pr.get('number')) is int and pr['number'] == 210 and pr['head']['sha'] == PREPARED
         and pr['base']['ref'] == 'main' and pr.get('draft') is False and pr.get('state') == 'closed'
         and pr.get('merged') is True and pr.get('merge_commit_sha') == MERGED
         and pr.get('merged_at') == MERGED_AT, 'Already genuinely merged PR210 identity differs')
    comparison = api('GET','compare/'+MERGED+'...'+m['expected_parent'])
    need(comparison.get('status') == 'ahead' and comparison['merge_base_commit']['sha'] == MERGED,
         'Actual original PR merge must be ancestor of fresh adoption parent')
    return pr



def state(c,m,overlay,pre,reused,observer,after_ref=False):
    need(type(after_ref) is bool and exact(reused,{}), 'Explicit readback mode and no unchanged body fetches')
    api = GetOnly(observer);parent = m['expected_parent']
    observed = api('GET','git/ref/heads/main')['object']['sha']
    if not after_ref:need(observed == parent, 'Fresh MAIN lease differs')
    commit = api('GET','git/commits/'+parent)
    need(commit.get('sha') == parent and commit['tree']['sha'] == m['expected_parent_tree'], 'Fresh parent/tree differs')
    if parent != ANCHOR:
        comparison = api('GET','compare/'+ANCHOR+'...'+parent)
        need(comparison.get('status') == 'ahead' and comparison['merge_base_commit']['sha'] == ANCHOR,
             'Fresh parent must descend from actual accepted PR209 terminal checkpoint')
    pr_identity(api,m,after_ref)
    trees = c.NativeTrees(api)
    need(trees.lookup(m['expected_parent_tree'],SHARED) == ('040000','tree',SHARED_TREE), 'Existing published audit tree differs')
    need(trees.lookup(m['expected_parent_tree'],ATTEMPT[:-1]) == ('040000','tree',ATTEMPT_TREE), 'Existing own47 tree differs')
    queue = tuple_pin(m['protected_queue'])
    need(trees.lookup(m['expected_parent_tree'],QUEUE) == queue, 'Fresh whole-QUEUE tuple differs')
    wanted,changed,dirs = expected(c,trees,m['expected_parent_tree'],overlay,pre)
    need(pre[VIEWS[2]] is not None, 'Existing ascending current progress required')
    progress = decode(read_blob(api,pre[VIEWS[2]][2]))
    matches(progress,baseline_facts(),'Refuse overwriting an intervening ascending checkpoint')
    baseline = decode(sealed('BASELINE_MEMBERSHIP.json',BASELINE_PIN))
    for key in ('fully_completed_eligible_PRs','published_PRs'):
        need(exact(progress.get(key),baseline[key]), 'Native ascending baseline membership changed: '+key)
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total'] == 99, 'Native dated denominator changed')
    for alias,key in (('current_PR','active_PR'),('current_case_percent','case_workflow_estimate_percent')):
        if alias in progress:matches(progress,{alias:baseline_facts()[key]},'Native baseline alias differs')
    for path in (VIEWS[1],VIEWS[4]):
        if pre[path] is not None:
            need(overlay[path].startswith(read_blob(api,pre[path][2])), 'Native research-log prefix changed')
    if not after_ref:need(api('GET','git/ref/heads/main')['object']['sha'] == parent, 'Fresh MAIN lease lost')
    return {'api':api,'parent':parent,'parent_tree':m['expected_parent_tree'],'wanted':wanted,
            'changed':changed,'dirs':dirs,'parents':[parent],'protected_queue':queue}


def plan(c,m,overlay,pre,reused,observer):
    s = state(c,m,overlay,pre,reused,observer)
    request,expected_commit = commit_request(m,s['wanted'],s['parents'])
    return {'schema':'pr210-native-conditional-plan-v1','evidence_scope':'CONDITIONAL_MODEL_NOT_ACTUAL_ACCEPTANCE',
            'phase':m['phase'],'facts':m['facts'],'parent':s['parent'],'parent_tree':s['parent_tree'],
            'modeled_commit':request,'expected_commit':expected_commit,
            'modeled_tree':{'base_tree':s['parent_tree'],'tree':[
                {'path':p,'mode':'100644','type':'blob','sha':native('blob',body)} for p,body in sorted(overlay.items())]},
            'changed_leaves':sorted(s['changed']),'new_directories':sorted(s['dirs']),
            'selected_files':len(overlay),'selected_bytes':sum(map(len,overlay.values())),
            'reused_body_files':0,'shared_tree_preserved':SHARED_TREE,'own47_tree_preserved':ATTEMPT_TREE,
            'native_objects_created':False,'ref_actions_performed':False,'local_views_modified':False,
            'publication_or_tracker_actions_performed':False,'actual_acceptance_inferred':False}


def commit_message_readback(canonical,metadata):
    need(type(canonical) is str and canonical.endswith('\n') and type(metadata) is str,
         'Canonical newline-terminated message and exact metadata text required')
    if metadata == canonical:
        omitted = 0
    else:
        need(metadata == canonical[:-1], 'Commit metadata differs beyond exactly one omitted terminalLF')
        omitted = 1
    return {'representation':'exact' if omitted == 0 else 'omits_exactly_one_terminal_LF',
            'terminal_LFs_omitted':omitted,'canonical_message_pin':pin(canonical.encode()),
            'metadata_message_pin':pin(metadata.encode())}


def verify(c,m,overlay,pre,reused,observer,candidate,after_ref=False):
    need(hexid(candidate), 'Explicit candidate native commit identity required')
    s = state(c,m,overlay,pre,reused,observer,after_ref)
    api = s['api']
    request,expected_commit = commit_request(m,s['wanted'],s['parents'])
    need(candidate == expected_commit, 'Candidate deterministic native commit identity differs')
    commit = api('GET','git/commits/'+candidate)
    need(commit.get('sha') == candidate and commit['tree']['sha'] == s['wanted']
         and [r['sha'] for r in commit['parents']] == s['parents'], 'Exact candidate SHA/parents/tree differ')
    matches(commit.get('author'),m['commit_author'],'Fixed canonical author metadata differs')
    matches(commit.get('committer'),m['commit_committer'],'Fixed canonical committer metadata differs')
    message_readback = commit_message_readback(m['commit_message'],commit.get('message'))
    trees = c.NativeTrees(api)  # Independent from construction/state cache.
    leaves,dirs,deleted = trees.changes(s['parent_tree'],s['wanted'])
    need(leaves == s['changed'] and dirs == s['dirs'] and not deleted, 'Full foreign/native changed scope differs')
    need(trees.lookup(s['wanted'],ATTEMPT[:-1]) == ('040000','tree',ATTEMPT_TREE), 'Candidate unchanged own47 is not exact')
    need(trees.lookup(s['wanted'],SHARED) == ('040000','tree',SHARED_TREE), 'Candidate shared case changed')
    need(trees.lookup(s['wanted'],QUEUE) == s['protected_queue'], 'Candidate whole QUEUE changed')
    selected = {}
    for path,body in sorted(overlay.items()):
        oid = native('blob',body)
        need(trees.lookup(s['wanted'],path) == ('100644','blob',oid), 'Selected native tuple differs')
        need(read_blob(api,oid) == body, 'Selected full native body differs')
        selected[path] = {**pin(body),'mode':'100644','type':'blob','git_blob':oid}
    observed = api('GET','git/ref/heads/main')['object']['sha']
    need(observed == (candidate if after_ref else s['parent']), 'Final MAIN identity differs')
    return {'schema':'pr210-native-conditional-verification-v1','evidence_scope':'GET_OBSERVATIONS_REQUIRE_ROOT_ACCEPTANCE',
            'phase':m['phase'],'facts':m['facts'],'parent':s['parent'],'parent_tree':s['parent_tree'],
            'candidate':candidate,'tree':s['wanted'],'parents':s['parents'],'selected_files':selected,
            'deterministic_canonical_commit_oid_verified':True,
            'fixed_author_and_committer_metadata_verified':True,'commit_message_readback':message_readback,
            'selected_file_count':len(selected),'selected_bytes':sum(row['bytes'] for row in selected.values()),
            'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'deleted_directories':[],
            'full_scope_verified':True,'all_selected_native_bodies_verified':True,
            'foreign_native_tuples_preserved':True,'shared_tree_preserved':SHARED_TREE,
            'own47_tree_preserved':ATTEMPT_TREE,'whole_QUEUE_tuple_preserved':list(s['protected_queue']),
            'original_PR_already_merged':True,'original_merge_commit':MERGED,
            'actual_MAIN_observed':observed,'native_objects_created':False,'ref_actions_performed':False,
            'local_views_modified':False,'actual_acceptance_inferred':False}
