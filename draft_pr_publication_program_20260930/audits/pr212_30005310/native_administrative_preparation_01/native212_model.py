"""Pure conditional PR212 administrative model. No writer, transport or CLI."""
import base64,calendar,datetime,hashlib,json,math,os,re,stat,types
from pathlib import Path,PurePosixPath
BASE=Path(__file__).absolute().parent
LOCAL_CASE=BASE.parent
LOCAL_PROGRAM=LOCAL_CASE.parents[1]
CHECKOUT=LOCAL_PROGRAM.parent
PROGRAM='draft_pr_publication_program_20260930/'
CASE=PROGRAM+'audits/pr212_30005310/'
OLD_CASE=PROGRAM+'audits/pr211_5100063/'
ATTEMPT='unsolved_math_prioritization/attempts/30005310'
SHARED='draft_pr_descending_audit_20261002/audits/pr212_30005310'
QUEUE='unsolved_math_prioritization/QUEUE.md'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md',PROGRAM+'CURRENT_PROGRESS.json',PROGRAM+'CURRENT_PROGRESS.md',PROGRAM+'RESEARCH_LOG.md')
ANCHOR='ad3af31e26c29115d222142ae6b033115e195808'
ORIGINAL='c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7'
ORIGINAL_TREE='436c162cea349eb2d07041202d32fd27c00df926'
ORIGINAL_PARENT='8431d4eb9b4fbb56cc82f5a4ac61514053c2958d'
CURRENT='99af7a27a711271bcd0b9e7ce90e374e4100ea6d'
CURRENT_TREE='3dd6b7b24c6eef3306ba47d939c6d75a2d2308de'
CURRENT_QUEUE='75dd3438de4cd64c023595f67b9331392278315f'
CURRENT_ROW={'bytes':583,'sha256':'888486f42b1d43c32114cd971d988579926215f4050adf5dbe8c7d51fe86b691'}
CORE_PIN={'bytes':4719,'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}
WRITER_LOCK_REFERENCE={'path':PROGRAM+'ROOT_GLOBAL_FIVE_WRITER.lock','device':16777232,'inode':439078796,'bytes':153,'sha256':'61404e167a3dedccc0fd17a1a1823fd772bc12a9144a4f012ab26d5e2a26fc0a'}
PRIOR_TERMINAL_PATH=OLD_CASE+'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json'
PRIOR_TERMINAL_PIN={'bytes':9799,'sha256':'8acd4bb99e504f4fe59b9c28a91b8fdcfc5a71502b3b0f54cb98070a29467477'}
BASELINE_PIN={'bytes': 853, 'sha256': 'b4fe8858faebc0f14ab956d8849af28072837807f3fc87e85a2abe356bfb2f1e'}
MAX_BODY=4_000_000
MAX_FILES=600
MAX_TOTAL=8_000_000
BODY_POLICY='ACTUAL_NATIVE_SELECTED_BLOB_GETS_PER_API_INSTANCE'
QUEUE_POLICY='PARENT_AND_C_WHOLE_QUEUE_FIXED_R_FOREIGN_ROWS_ONLY_OWN_EXACT'

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


def matches(obj, expected, message):
    need(type(obj) is dict, message)
    for key, value in expected.items():
        need(key in obj and exact(obj[key],value), message+': '+key)


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
    need(hexid(tree) and type(parents) is list and len(parents) == 1 and parents[0] not in (ORIGINAL,CURRENT)
         and all(hexid(p) for p in parents), 'Exact deterministic commit tree/parents')
    author,committer = identity(m['commit_author']),identity(m['commit_committer'])
    need(m['commit_message']=='Archive PR212 administrative untouched nonclaimed disposition\n',
         'Only exact neutral archive message; auto-closing clauses forbidden')
    message = m['commit_message']
    need(type(message) is str and 1 <= len(message.encode()) <= 1000
         and message.endswith('\n') and '\r' not in message and '\0' not in message,
         'Explicit newline-terminated deterministic commit message required')
    raw = ('tree '+tree+'\n'+''.join('parent '+p+'\n' for p in parents)
           +'author '+author+'\ncommitter '+committer+'\n\n'+message).encode()
    request = {'message':message,'tree':tree,'parents':parents,
               'author':m['commit_author'],'committer':m['commit_committer']}
    return request,native('commit',raw)


class GetOnly:
    """Route firewall, with no transport and no retry. Import is inert."""
    def __init__(self, observer):
        self.observer = observer
        self.failed = False

    def __call__(self, method, path, body=None):
        need(not self.failed, 'Observer stopped after first uncertainty')
        allowed = path in ('git/ref/heads/main','pulls/212') or re.fullmatch(
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


def read_regular(path,cap=4_000_000,absent=False):
    """No-follow descriptor walk, exact readonly mode and identity stability."""
    need(path.is_absolute() and path.is_relative_to(CHECKOUT) and path.resolve()==path,
         'Canonical source/preimage inside checkout required')
    handles=[]
    fd=None
    try:
        current=Path('/')
        parent=os.open(current,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        handles.append((current,parent,os.fstat(parent)))
        for part in path.parent.parts[1:]:
            current=current/part
            parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
            handles.append((current,parent,os.fstat(parent)))
        try:
            fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
        except FileNotFoundError:
            need(absent,'Required regular file absent')
            need(not path.exists() and not path.is_symlink(),'File appeared during absence observation')
            for ancestor,descriptor,before in handles:
                a,b=os.fstat(descriptor),ancestor.lstat()
                need(stat.S_ISDIR(b.st_mode) and (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)==(before.st_dev,before.st_ino),
                     'Ancestor changed during absence observation')
            return None,None
        before=os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444
             and before.st_size<=cap,'Bounded readonly0444 regular file required')
        with os.fdopen(fd,'rb',closefd=False) as stream:
            raw=stream.read(cap+1)
        after,entry=os.fstat(fd),path.lstat()
        fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        need(fields(before)==fields(after)==fields(entry) and stat.S_ISREG(entry.st_mode)
             and stat.S_IMODE(entry.st_mode)==0o444 and len(raw)==after.st_size,'File changed during capture')
        for ancestor,descriptor,initial in handles:
            now,linked=os.fstat(descriptor),ancestor.lstat()
            need(stat.S_ISDIR(linked.st_mode) and (now.st_dev,now.st_ino)==(linked.st_dev,linked.st_ino)==(initial.st_dev,initial.st_ino),
                 'Source/preimage ancestor changed')
        return raw,{'device':after.st_dev,'inode':after.st_ino,'bytes':after.st_size,
                    'mtime_ns':after.st_mtime_ns,'ctime_ns':after.st_ctime_ns,'mode':'0444'}
    finally:
        if fd is not None:os.close(fd)
        for ancestor,descriptor,initial in reversed(handles):os.close(descriptor)


def core():
    raw = sealed('native_trees_readonly.py', CORE_PIN)
    result = types.ModuleType('pr211_readonly_native_trees')
    exec(compile(raw, str(BASE/'native_trees_readonly.py'), 'exec'), result.__dict__)
    return result


ROOT_EVIDENCE={'math': {'bytes': 7885, 'sha256': '790b6482fcc2ef5fe39ebb7fc12850213b67133de0221861ee6cb5eb122e4512'}, 'priority': {'bytes': 6441, 'sha256': '1ad1506d4a21c4d1b4cef16a3db059ad3609fab1a33e1834c7b813356b9a73d2'}, 'disposition': {'bytes': 4606, 'sha256': '6e2f3b82c2a6a23ec4e33d51a92d3a4d91e9a702b8896c0c2e90703d6beeb824'}, 'disposition_review': {'bytes': 3479, 'sha256': '51959e3a543d5cf5f5683cee0bb1aca6ed454337e1fad415863c0aff44af7700'}}
ROOT_EVIDENCE_PATHS={'math': 'ROOT_MATHEMATICAL_ACCEPTANCE_01.json', 'priority': 'ROOT_PRIORITY_ACCEPTANCE_01.json', 'disposition': 'ROOT_ADMINISTRATIVE_DISPOSITION_01.json', 'disposition_review': 'ROOT_ADMINISTRATIVE_REVIEW_ACCEPTANCE_01.json'}

def root_ref(row):
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['path']) is str,'Exact canonical file reference')
    path=Path(row['path']);need(path.is_absolute() and path.is_relative_to(CHECKOUT),'Checkout-owned input reference')
    raw,identity=read_regular(path)
    need(exact(pin(raw),bytepin({k:row[k] for k in ('bytes','sha256')})),'Referenced body changed')
    return decode(raw)

def phase_facts(phase='administrative100'):
    need(phase=='administrative100','Only conditional administrative checkpoint')
    return {'active_PR':212,'administrative_checkpoint_percent':100,
            'disposition':'ADMINISTRATIVE_ADVANCE_CORRECTED_NONCLAIMED_DRAFT_UNTOUCHED',
            'original_eligible_status':'claimed_solved','current_corrected_status':'already_solved',
            'original_eligibility_rewritten_or_erased':False,'current_PR_open_draft_unmerged':True,'fully_completed_count':53,'published_count':37,
            'last_completed_PR':211,'next_numeric_intake_cursor':213,'goal_complete':False,
            'completed_eligible_workflow':False,'publication_workflow_completed':False,'publication_ready':False,
            'administrative_checkpoint_complete':True,'numeric_advance_conditional_on_actual_Root_terminal':True,
            'advance_to_next_PR_authorized_now':False}

def baseline_facts():
    return {'fully_completed_count':53,'published_count':37,'last_completed_PR':211,
            'next_numeric_intake_cursor':212,'goal_complete':False}

def phase_marker(phase='administrative100'):
    return ('<!-- PR212_ADMINISTRATIVE_FACTS '+compact(phase_facts(phase))+' -->').encode()

def markdown_current(raw,phase,append_log):
    need(type(raw) is bytes and type(append_log) is bool,'Explicit Markdown body/log policy')
    current=phase_marker(phase);stem=b'<!-- PR212_ADMINISTRATIVE_FACTS'
    lines=raw.splitlines()
    while lines and lines[-1]==b'':lines.pop()
    markers=[line for line in lines if line.startswith(stem)]
    need(raw.count(stem)==len(markers)==1 and markers==[current] and lines[-1]==current,
         'One canonical current administrative terminal marker; historical other-case markers preserved')

def public_path(path):
    rel(path)
    if not path.startswith(CASE) or path in VIEWS:return False
    parts=path[len(CASE):].split('/')
    forbidden=('private','_private','packet','journal','runtime','_runtime','sandbox','_synthetic','root_admin212_')
    if any(p.lower().startswith(forbidden) or p.lower() in ('extracted','objects','inputs') for p in parts):return False
    return Path(path).suffix.lower() in ('.json','.md','.py','.txt','.tex','.csv','.patch','.sha256')

def preserved_tuple(row,tree_only=False):
    if row is None:return None
    need(type(row) is dict and set(row)=={'mode','type','sha'} and hexid(row['sha']),'Exact protected tuple')
    need((row['mode'],row['type'])==(('040000','tree') if tree_only else ('100644','blob')),'Protected mode/type')
    return row['mode'],row['type'],row['sha']

def own_queue_row(raw):
    need(type(raw) is bytes and len(raw)<=MAX_BODY,'Bounded authenticated wholeQUEUE body')
    found=[]
    for line in raw.splitlines(keepends=True):
        # Markdown permits optional leading whitespace/outer pipes. Detect
        # suspected own-ID cells before requiring our exact canonical form;
        # malformed/indented duplicates must never disappear from uniqueness.
        stripped=line.lstrip(b' \t');cells=stripped.split(b'|')
        suspected=any(re.search(rb'(?<![0-9])30005310(?![0-9])',cell) for cell in cells[:4])
        if not suspected:continue
        need(line.startswith(b'|') and len(cells)==14
             and cells[2].strip()==b'30005310 / OWR-11695865-009',
             'Indented/malformed own QUEUE row or noncanonical own code')
        found.append((line,cells))
    need(len(found)==1,'Exactly one own QUEUE row; missing/duplicate refused')
    return found[0]

def pr_identity(observer,m,pool):
    api=GetOnly(observer)
    for oid,root,parents in ((ORIGINAL,ORIGINAL_TREE,[ORIGINAL_PARENT]),(CURRENT,CURRENT_TREE,[ORIGINAL])):
        commit=api('GET','git/commits/'+oid)
        need(commit.get('sha')==oid and commit['tree']['sha']==root
             and [x['sha'] for x in commit['parents']]==parents,'Exact original/current immutable commit association')
    def pr():
        value=api('GET','pulls/212')
        matches(value,{'number':212,'title':'30005310: Credited prior counterexamples to literal numerical scenarios',
            'state':'open','draft':True,'merged':False,'commits':3,'merged_at':None},'Corrected nonclaimed draft must remain untouched')
        need(value['head']['sha']==CURRENT and value['head']['ref']=='math/30005310-colored-threshold-wip'
             and value['base']['ref']=='main','Exact current HEAD/branch/base')
        need(exact(pin(compact(value.get('body')).encode()),m['current_PR_opaque_body_pin']),'Opaque current PR body changed')
        return value
    first=pr()
    trees=core().NativeTrees(api)
    need(trees.lookup(CURRENT_TREE,QUEUE)==('100644','blob',CURRENT_QUEUE),'Current HEAD native QUEUE path association')
    body=pool.get(observer,CURRENT_QUEUE)
    row,cells=own_queue_row(body)
    need(exact(pin(row),CURRENT_ROW) and cells[8].strip()==b'already_solved' and cells[9].strip()==b'1/5',
         'Fresh current native nonclaimed QUEUE status required')
    final=pr()
    return {'HEAD':CURRENT,'state':'open','draft':True,'merged':False,'current_status':'already_solved',
            'current_QUEUE_oid':CURRENT_QUEUE,'current_row_pin':pin(row),'same_selected_PR_identity':True}

class NativeBodyProofs:
    """Actual GET bytes only, retained and rehashed in this invocation/API instance."""
    def __init__(self):self.instances={}
    def get(self,observer,oid,wanted=None):
        key=id(observer)
        if key not in self.instances:self.instances[key]=(observer,{})
        held,objects=self.instances[key]
        need(held is observer,'Native body proof instance identity')
        if oid not in objects:
            body=read_blob(GetOnly(observer),oid)
            origins=getattr(observer,'actual_GET_origins',{})
            origin=origins.get('git/blobs/'+oid)
            need(origin is not None,'Actual raw native GET origin required; no source/cache impersonation')
            matches(origin,{'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math','route':'git/blobs/'+oid},'Actual native blob provenance')
            response=origin['raw_response'];raw,unused=read_regular(Path(response['path']),cap=12_000_000)
            need(exact(pin(raw),{k:response[k] for k in ('bytes','sha256')}),'Actual raw native response changed')
            stderr_ref=origin['raw_stderr'];stderr,unused=read_regular(Path(stderr_ref['path']),cap=65536)
            need(exact(pin(stderr),{k:stderr_ref[k] for k in ('bytes','sha256')}),'Actual raw native stderr changed')
            receipt=root_ref({'path':origin['receipt'],**origin['receipt_pin']})
            matches(receipt,{'method':'GET','path':'git/blobs/'+oid,'exit':0,'raw_stdout':response,
                             'raw_stderr':origin['raw_stderr']},'Raw native GET receipt association')
            j=decode(raw)
            need(j.get('sha')==oid and j.get('encoding')=='base64' and type(j.get('size')) is int
                 and j['size']==len(body) and base64.b64decode(''.join(j['content'].split()),validate=True)==body,
                 'Actual raw envelope/body differs')
            need(len(objects)<MAX_FILES+64 and sum(len(v[0]) for v in objects.values())+len(body)<=32_000_000,'In-memory actual native body proof bounds')
            objects[oid]=(body,pin(body),origin)
        body,expected,origin=objects[oid]
        need(type(body) is bytes and exact(pin(body),expected) and native('blob',body)==oid,'In-memory authenticated native bytes changed')
        if wanted is not None:need(exact(expected,bytepin(wanted)),'Native body SHA256/length differs')
        return body
    def origin(self,observer,oid):return self.instances[id(observer)][1][oid][2]

def queue_observation(observer,trees,root,m,pool,allow_foreign_rows):
    item=trees.lookup(root,QUEUE)
    need(item is not None and item[:2]==('100644','blob'),'Regular native MainQUEUE mode required')
    if not allow_foreign_rows:need(item==tuple_pin(m['protected_queue']),'Parent/C whole MainQUEUE changed')
    body=pool.get(observer,item[2]);row,cells=own_queue_row(body)
    need(exact(pin(row),m['protected_queue_row_pin']),'Own MainQUEUE row/status/body changed')
    return {'parent_QUEUE_oid':m['protected_queue']['sha'],'candidate_QUEUE_oid':m['protected_queue']['sha'],
            'observed_QUEUE_oid':item[2],'whole_body_pin':pin(body),'own_row_pin':pin(row),
            'foreign_rows_may_differ':allow_foreign_rows,'policy':QUEUE_POLICY,
            'actual_native_body_origin':pool.origin(observer,item[2])}

def source_baseline():
    return decode(sealed('BASELINE_MEMBERSHIP.json',BASELINE_PIN))

def load_inputs(manifest_ref,acceptance_ref,source_manifest_pin,protocol_pin,primitive_pin):
    m=root_ref(manifest_ref)
    keys={'schema','PR','problem_id','phase','facts','files','total_files','total_bytes','local_views',
          'protected_queue','protected_queue_row_pin','protected_nodes','current_PR_opaque_body_pin',
          'expected_new_directories','expected_changed_paths','carryforward','commit_author','commit_committer','commit_message',
          'retired_candidates','body_proof_policy','QUEUE_policy','writer_lock','evidence_references'}
    need(type(m) is dict and set(m)==keys,'Exact administrative logical packet fields')
    matches(m,{'schema':'pr212-conditional-administrative-logical-packet-v1','PR':212,'problem_id':'30005310',
        'phase':'administrative100','facts':phase_facts(),'body_proof_policy':BODY_POLICY,'QUEUE_policy':QUEUE_POLICY,
        'writer_lock':WRITER_LOCK_REFERENCE},'Typed administrative facts/policies')
    need(type(m['retired_candidates']) is list and len(m['retired_candidates'])<=100
         and m['retired_candidates']==sorted(set(m['retired_candidates'])) and all(hexid(x) for x in m['retired_candidates']),'Explicit retired candidate denylist')
    preserved_tuple(m['protected_queue']);bytepin(m['protected_queue_row_pin']);bytepin(m['current_PR_opaque_body_pin'])
    need(type(m['protected_nodes']) is dict and set(m['protected_nodes'])=={ATTEMPT,SHARED},'Protect fresh Main attempt and old audit including absence')
    for row in m['protected_nodes'].values():preserved_tuple(row,tree_only=True)
    need(type(m['expected_new_directories']) is list and len(m['expected_new_directories'])<=600
         and m['expected_new_directories']==sorted(set(m['expected_new_directories'])),'Finite exact expected directories')
    for path in m['expected_new_directories']:rel(path)
    carry=m['carryforward']
    need(type(carry) is list and len(carry)<=200 and all(type(r) is dict and set(r)=={'path','bytes','sha256'} for r in carry)
         and len({r['path'] for r in carry})==len(carry),'Finite positive old-case carryforward')
    carrypins={}
    for row in carry:
        path=rel(row['path']);bytepin({k:row[k] for k in ('bytes','sha256')})
        need(path.startswith(OLD_CASE) and not any(s.lower().startswith(('private','_private','packet','journal','runtime','_runtime','ROOT_CONCURRENT_READ_'.lower(),'ROOT_CONCURRENT_SYNC_'.lower())) for s in path[len(OLD_CASE):].split('/'))
             and Path(path).suffix.lower() in ('.json','.md','.py','.txt','.patch','.sha256'),'Positive public old-case receipt/source only')
        carrypins[path]={k:row[k] for k in ('bytes','sha256')}
    need(exact(carrypins.get(PRIOR_TERMINAL_PATH),PRIOR_TERMINAL_PIN),'Exact211 actual terminal natural-path carryforward required')
    rows=m['files']
    need(type(rows) is list and 5<len(rows)<=MAX_FILES and all(type(r) is dict and set(r)=={'path','source','bytes','sha256','git_blob','preimage'} for r in rows)
         and len({r['path'] for r in rows})==len(rows),'Finite positive selected body records')
    overlay={};pre={}
    for row in rows:
        path=rel(row['path']);need(path in VIEWS or public_path(path) or path in carrypins,'Selected target outside exact own/public/carry scope')
        body=sealed(row['source'],{k:row[k] for k in ('bytes','sha256')})
        need(hexid(row['git_blob']) and native('blob',body)==row['git_blob'] and '\0' not in body.decode('utf-8'),'Exact UTF8 selected body/native identity; no binary POSTs')
        overlay[path]=body;pre[path]=tuple_pin(row['preimage'])
        if path not in VIEWS:need(pre[path] in (None,('100644','blob',row['git_blob'])),'New archives/carry are add-or-exact-noop, never overwrite')
        if path in carrypins:need(exact(pin(body),carrypins[path]),'Carryforward exact body differs')
    need(set(VIEWS).issubset(overlay) and set(carrypins).issubset(overlay),'All five and exact carryforward present')
    need(type(m['expected_changed_paths']) is list and m['expected_changed_paths']==sorted(set(m['expected_changed_paths']))
         and set(m['expected_changed_paths']).issubset(overlay) and len(m['expected_changed_paths'])>0,'Exact finite nonempty changed-leaf scope')
    need(type(m['total_files']) is int and m['total_files']==len(rows) and type(m['total_bytes']) is int
         and m['total_bytes']==sum(map(len,overlay.values()))<=MAX_TOTAL,'Exact bounded selected totals')
    for path in (VIEWS[0],VIEWS[2]):
        obj=decode(overlay[path]);matches(obj,phase_facts(),'Conditional administrative structured view')
        matches(obj,{'conditional_proposal_only':True},'No false actual completion')
        if 'completed' in obj:need(obj['completed'] is False,'Generic completedTrue forbidden for administrative skip')
        for alias,key in (('current_PR','active_PR'),('PR','active_PR'),('current_publication_ready','publication_ready')):
            if alias in obj:matches(obj,{alias:phase_facts()[key]},'Structured administrative alias')
        for key in ('active_publication_DOI','active_tracker_range'):
            if key in obj:need(obj[key] is None,'No current PR212 publication/tracker metadata')
        for key in ('original_PR_merged','actual_original_PR_merged','new_publication_or_tracker_append_performed'):
            if key in obj:need(obj[key] is False,'No merged/publication action claim')
    progress=decode(overlay[VIEWS[2]]);baseline=source_baseline()
    for key in baseline:need(exact(progress.get(key),baseline[key]),'Completed/publication lists must remain exact53/37')
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Dated99 unchanged')
    for path in (VIEWS[1],VIEWS[3],VIEWS[4]):markdown_current(overlay[path],m['phase'],path in (VIEWS[1],VIEWS[4]))
    local=m['local_views']
    need(type(local) is list and len(local)==5 and all(type(r) is dict and set(r)=={'path','preimage','source'} for r in local)
         and [r['path'] for r in local]==list(VIEWS),'Exact ordered five separate local preimages')
    for row in local:
        if row['preimage'] is None:need(row['source'] is None,'Absent local preimage source null')
        else:
            raw=sealed(row['source'],row['preimage'])
            if row['path'] in (VIEWS[1],VIEWS[4]):need(overlay[row['path']].startswith(raw),'Existing local log prefix changed')
    for key in ('commit_author','commit_committer'):
        need(exact(m[key],{'name':'Alec Kriebel','email':'me@aleckriebel.com'}),'Fixed archive commit identity')
    need(m['commit_message']=='Archive PR212 administrative untouched nonclaimed disposition\n','Fixed no-merge archival commit message')
    evidence=m['evidence_references']
    need(type(evidence) is dict and set(evidence)==set(ROOT_EVIDENCE),'Exact existing accepted Root evidence roles')
    for role,wanted in ROOT_EVIDENCE.items():
        value=root_ref(evidence[role]);need(exact({k:evidence[role][k] for k in ('bytes','sha256')},wanted),'Exact existing Root evidence pin')
        need(evidence[role]['path']==str(LOCAL_CASE/ROOT_EVIDENCE_PATHS[role]),'Expected Root evidence natural path')
    for role,row in evidence.items():
        target=CASE+ROOT_EVIDENCE_PATHS[role]
        need(target in overlay and exact(pin(overlay[target]),ROOT_EVIDENCE[role]),'Existing accepted Root evidence must be positively archived')
    disposition=root_ref(evidence['disposition'])
    matches(disposition,{'schema':'pr212-root-conservative-administrative-disposition-v1','accepted':True,
        'completed_eligible_workflow':False,'publication_ready':False,'actual_completed_count_retained':53,
        'actual_published_count_retained':37,'last_completed_eligible_PR_retained':211,
        'conditional_target_numeric_cursor':213,'numeric_advance_authorized_by_this_file':False,
        'current_PR_open_draft_unmerged':True,'current_corrected_status':'already_solved',
        'new_paper_DOI_tracker_row_merge_close_comment_release_or_attempt_QUEUE_edit_authorized':False},'Root disposition authority only')
    gate=root_ref(acceptance_ref)
    matches(gate,{'schema':'pr212-root-administrative-logical-packet-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':212,'accepted':True,'manifest_pin':{k:manifest_ref[k] for k in ('bytes','sha256')},
        'source_manifest_pin':source_manifest_pin,'protocol_pin':protocol_pin,'primitive_pin':primitive_pin,
        'facts':phase_facts(),'public_selection_reviewed':True,'administrative_disposition_review_accepted':True,
        'no_PR_or_publication_actions':True,'all53_37_memberships_unchanged':True,'QUEUE_policy':QUEUE_POLICY,
        'Root_full_source_read':True,'independent_source_adversarial_review_accepted':True,
        'independent_exact_packet_review_accepted':True},'Separate actual Root logical/source/exact packet acceptance required')
    audits=gate.get('audit_receipts')
    need(type(audits) is list and len(audits)==2 and len({r.get('path') for r in audits})==2,'Distinct source/exact audit receipts')
    for row in audits:root_ref(row)
    return m,overlay,pre
