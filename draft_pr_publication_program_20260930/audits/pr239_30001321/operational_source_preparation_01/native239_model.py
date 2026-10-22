"""Inactive pure PR239 two-phase NEW-publication model. No transport/CLI/writer."""
import base64,calendar,datetime,hashlib,json,math,os,re,stat,types
from pathlib import Path,PurePosixPath
BASE=Path(__file__).absolute().parent
LOCAL_CASE=BASE.parent
LOCAL_PROGRAM=LOCAL_CASE.parents[1]
CHECKOUT=LOCAL_PROGRAM.parent
PROGRAM='draft_pr_publication_program_20260930/'
CASE=PROGRAM+'audits/pr239_30001321/'
OLD_CASE=PROGRAM+'audits/pr218_30006020/'
ATTEMPT='unsolved_math_prioritization/attempts/30001321'
SHARED='draft_pr_descending_audit_20261002/audits/pr239_30001321'
QUEUE='unsolved_math_prioritization/QUEUE.md'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md',PROGRAM+'CURRENT_PROGRESS.json',PROGRAM+'CURRENT_PROGRESS.md',PROGRAM+'RESEARCH_LOG.md')
ANCHOR='6f83668adece147040b81ead88625ba5214a37a2'
ORIGINAL=CURRENT='7f17eef77c52b2d9b2ec3ad0803c016267fa6496'
CURRENT_TREE=ORIGINAL_TREE='7b8730e5f1980eccf6999e320adf145b93dac4ea'
ORIGINAL_PARENT='7d0f9ca6a01d6fdfe8dcf9dd05b7ba15ec222ac4'
SUBMITTED_BASE='2216543dd372ed5afd41f67da7ad638edf3d339f'
SUBMITTED_CHAIN=['db5f4a96a5faf437c1108047838d6011f9518de6','1365eea33ceb7560f7c6d7225bec7dc8525e1708',ORIGINAL_PARENT,CURRENT]
SUBMITTED_BASE_ROW={'bytes':133,'sha256':'528036fd20279c1d390501bcfb5860c6fbd611ca2207fcf6f6831577f6f60cb8'}
FULL_SCOPE_PIN={'bytes':13567,'sha256':'8084a1df4a6e26e54dcecea96439ee4054f9572c807bed4634a9245777117673'}
CURRENT_QUEUE='204ac8c2ce16fb12c8b46a8326edc97f6bd88f85'
CURRENT_ROW={'bytes':445,'sha256':'3bf93b98d051439bf318a12a8e39f60f6e84531525de4d7125dc92a1dd3daf4e'}
CORE_PIN={'bytes':4719,'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}
WRITER_LOCK_REFERENCE={'path':PROGRAM+'ROOT_GLOBAL_FIVE_WRITER.lock','device':16777232,'inode':439078796,'bytes':153,'sha256':'61404e167a3dedccc0fd17a1a1823fd772bc12a9144a4f012ab26d5e2a26fc0a'}
PRIOR_TERMINAL_PIN={'bytes':20289,'sha256':'98b3fe2fbf90de4c16e2bc53254a0f7d6ceed0c9cf802412bda54efaa83aee9b'}
SPREADSHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
MAX_BODY=4_000_000
MAX_FILES=600
MAX_TOTAL=8_000_000
BODY_POLICY='ACTUAL_NATIVE_SELECTED_BLOB_GETS_PER_API_INSTANCE'
QUEUE_POLICY='EXACT_ROOT_OWN_PRE_POST_C_WHOLE_R_FOREIGN_ROWS_ONLY'
ROOT_EVIDENCE={'math':{'bytes':8814,'sha256':'41fab21edf43ea018613a6daee6ee53165172fbaabdf6e10f2e73ef9a9698262'},'custody':{'bytes':65348,'sha256':'4ddb9e5c9dc2487b9fb5fd8f993e562517b5efe2b4af2c2ae87c1a5c61feefa4'}}
ROOT_EVIDENCE_PATHS={'math':'ROOT_MATHEMATICAL_ACCEPTANCE_01.json','custody':'authenticated_sources_01/SOURCE_MATERIALIZATION_MANIFEST.json'}
BASELINE_PIN={'bytes': 889, 'sha256': '36258fde3b9a95d4ed8baf7aebff34030a25267b92b08d58256ebac2404b52ce'}
INVENTORY_PIN={'bytes': 9246, 'sha256': '983db9bb5d0f4be2ccca23b5ea2b9bdf430237d89837baf9ec4569dcdccad132'}
CARRY_PIN={'bytes': 5319, 'sha256': '3dbf7ac820e8c3b35d2b5713642411f6f8a7dc8320abf4345ecd77a0182a1800'}


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

class GetOnly:
    """Route firewall, with no transport and no retry. Import is inert."""
    def __init__(self, observer):
        self.observer = observer
        self.failed = False

    def __call__(self, method, path, body=None):
        need(not self.failed, 'Observer stopped after first uncertainty')
        allowed = path in ('git/ref/heads/main','pulls/239') or re.fullmatch(
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

def root_ref(row):
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['path']) is str,'Exact canonical file reference')
    path=Path(row['path']);need(path.is_absolute() and path.is_relative_to(CHECKOUT),'Checkout-owned input reference')
    raw,identity=read_regular(path)
    need(exact(pin(raw),bytepin({k:row[k] for k in ('bytes','sha256')})),'Referenced body changed')
    return decode(raw)

def preserved_tuple(row,tree_only=False):
    if row is None:return None
    need(type(row) is dict and set(row)=={'mode','type','sha'} and hexid(row['sha']),'Exact protected tuple')
    need((row['mode'],row['type'])==(('040000','tree') if tree_only else ('100644','blob')),'Protected mode/type')
    return row['mode'],row['type'],row['sha']

def public_path(path):
    rel(path)
    if not path.startswith(CASE) or path in VIEWS:return False
    parts=path[len(CASE):].split('/')
    forbidden=('private','_private','packet','journal','runtime','_runtime','sandbox','_synthetic','root_admin','root_complete','raw','_raw')
    if any(p.lower().startswith(forbidden) or p.lower() in ('extracted','objects','inputs') or any(x in p.lower() for x in ('raw_stdout','raw_stderr','api_receipt')) for p in parts):return False
    return Path(path).suffix.lower() in ('.json','.md','.py','.txt','.tex','.csv','.patch','.sha256')

def authenticated_commit(row):
    need(type(row) is dict and set(row)=={'sha','tree','parents','raw_commit'},'Exact authenticated commit record')
    need(hexid(row['sha']) and hexid(row['tree']) and type(row['parents']) is list
         and all(hexid(x) for x in row['parents']),'Explicit immutable commit identity')
    rawref=row['raw_commit']
    need(type(rawref) is dict and set(rawref)=={'path','bytes','sha256'},'Exact raw commit reference')
    raw,unused=read_regular(Path(rawref['path']))
    need(exact(pin(raw),bytepin({k:rawref[k] for k in ('bytes','sha256')}))
         and native('commit',raw)==row['sha'],'Full raw native commit SHA1/SHA256/length')
    header=raw.split(b'\n\n',1)
    need(len(header)==2 and header[0].startswith(b'tree '),'Canonical commit header')
    lines=header[0].split(b'\n')
    need([x[5:].decode('ascii') for x in lines if x.startswith(b'tree ')]==[row['tree']]
         and [x[7:].decode('ascii') for x in lines if x.startswith(b'parent ')]==row['parents'],
         'Raw ordered parent and root association')
    # Signed raw bytes are authenticated verbatim. Do not refold gpgsig with
    # splitlines(): its trailing empty continuation line is identity-bearing.
    return row

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
    need(hexid(tree) and type(parents) is list and bool(parents) and exact(parents,commit_parents(m,parents[0]))
         and all(hexid(p) for p in parents), 'Exact deterministic commit tree/parents')
    author,committer = identity(m['commit_author']),identity(m['commit_committer'])
    need(m['commit_message']==commit_message(m['phase']),
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

def phase_facts(phase='completion100'):
    need(phase in ('merge95','completion100'),'Two explicit phases only')
    done=phase=='completion100'
    return {'active_PR':239,'phase':phase,'workflow_percent':100 if done else 95,'completed':done,
        'fully_completed_count':56 if done else 55,'published_count':40 if done else 39,
        'last_completed_PR':239 if done else 218,'next_numeric_intake_cursor':240 if done else 239,
        'goal_complete':False,'completed_eligible_workflow':done,'publication_workflow_completed':done,
        'publication_ready':True,'original_eligible_status':'claimed_solved','current_status':'claimed_solved',
        'current_head':CURRENT,'new_publication_workflow':True,'adopted_existing_publication':False,
        'no_new_provider_publication_or_tracker_append':False,
        'numeric_advance_conditional_on_actual_Root_terminal':True,'advance_to_next_PR_authorized_now':False}

def baseline_facts(phase='merge95'):
    need(phase in ('merge95','completion100'),'Explicit phase baseline')
    return {'fully_completed_count':55,'published_count':39,'last_completed_PR':218,
        'next_numeric_intake_cursor':219 if phase=='merge95' else 239,'goal_complete':False}

def phase_marker(phase='completion100'):
    return ('<!-- PR239_NATIVE_PHASE_FACTS '+compact(phase_facts(phase))+' -->').encode()

def markdown_current(raw,phase,append_log):
    need(type(raw) is bytes and type(append_log) is bool,'Explicit Markdown/log policy')
    stem=b'<!-- PR239_NATIVE_PHASE_FACTS';current=phase_marker(phase);lines=raw.splitlines()
    while lines and lines[-1]==b'':lines.pop()
    markers=[line for line in lines if line.startswith(stem)]
    need(raw.count(stem)==len(markers),'Every namespace marker must be a complete canonical line')
    history=[phase_marker('merge95'),phase_marker('completion100')]
    allowed=([history] if append_log else [[current],history]) if phase=='completion100' else [[current]]
    need(markers in allowed and raw.count(current)==1 and bool(lines) and lines[-1]==current,
         'Unique latest marker; exact95-to100 history and all prefixes preserved')

def commit_parents(m,parent):
    need(hexid(parent) and parent!=CURRENT,'Fresh Main first parent, never PR snapshot')
    return [parent,CURRENT] if m['phase']=='merge95' else [parent]

def commit_message(phase):
    need(phase in ('merge95','completion100'),'Explicit commit phase')
    return 'Integrate PR239 reviewed publication and submitted history\n' if phase=='merge95' else 'Archive PR239 actual new-publication completion\n'

def own_queue_row(raw):
    need(type(raw) is bytes and len(raw)<=MAX_BODY,'Bounded authenticated QUEUE')
    found=[]
    for line in raw.splitlines(keepends=True):
        cells=line.lstrip(b' \t').split(b'|')
        suspected=any(re.search(rb'(?<![0-9])30001321(?![0-9])',cell) for cell in cells[:4])
        if not suspected:continue
        need(line.startswith(b'|') and len(cells)==14 and cells[2].strip()==b'30001321 / OWR-4081-005',
             'Noncanonical/indented/malformed own row')
        found.append((line,cells))
    need(len(found)==1,'Exactly one own row; ambiguous forms refused')
    return found[0]

def submitted_inventory():
    rows=decode(sealed('SUBMITTED_INVENTORY.json',INVENTORY_PIN))
    need(type(rows) is list and len(rows)==32,'Exact original32')
    return rows

def original_archives():
    return {CASE+'submitted_snapshot_01/'+r['repository_path'][len(ATTEMPT)+1:]:r for r in submitted_inventory()}

def source_baseline():
    return decode(sealed('BASELINE_MEMBERSHIP.json',BASELINE_PIN))

def completion_memberships():
    return {key:value+[239] for key,value in source_baseline().items()}

def phase_memberships(phase):
    return source_baseline() if phase=='merge95' else completion_memberships()

def native_identity(m):
    r=root_ref(m['native_identity_receipt'])
    matches(r,{'schema':'pr239-root-native-identity-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':239,'phase':m['phase'],'accepted':True,'raw_original_and_parent_commit_authentication_verified':True,
        'whole_submitted_HEAD_changed_scope_verified':True,'exact_original32_archive_verified':True,
        'fresh_Main_finite_preimages_and_own_row_verified':True,
        'protected_nodes':m['protected_nodes'],'protected_bodies':m['protected_bodies'],
        'post_attempt_tree':m['post_attempt_tree'],'science_allowlist':m['science_allowlist'],
        'protected_queue':m['protected_queue'],'queue_postimage':m['queue_postimage'],
        'queue_pre_row_pin':m['queue_pre_row_pin'],'protected_queue_row_pin':m['protected_queue_row_pin'],
        'current_PR_opaque_body_pin':m['current_PR_opaque_body_pin']},'Exact future Root native acceptance, not this source')
    for key,oid,tree,parents in [('original_commit',CURRENT,CURRENT_TREE,[ORIGINAL_PARENT]),
                               ('original_parent_commit',ORIGINAL_PARENT,None,None)]:
        row=authenticated_commit(r[key]);need(row['sha']==oid,'Original/parent commit identity')
        if tree is not None:need(row['tree']==tree and exact(row['parents'],parents),'Original root/sole parent')
    need(tuple_pin(r.get('submitted_base_queue')) is not None,'Authenticated full-submission base QUEUE tuple')
    scope=r.get('submitted_scope')
    scope_ref=r.get('full_submitted_scope_reference')
    need(exact(scope_ref,{'path':str(LOCAL_CASE/'root_full_submitted_scope_01/ROOT_COMPLETE_SUBMITTED_SCOPE.json'),**FULL_SCOPE_PIN}),'Exact independently captured full four-commit scope reference')
    root_ref(scope_ref)
    chain=r.get('submitted_commit_chain');base=authenticated_commit(r['submitted_base_commit'])
    need(base['sha']==SUBMITTED_BASE and type(chain) is list and len(chain)==4,'Authenticated full submitted base/chain')
    prior=SUBMITTED_BASE
    for expected_oid,entry in zip(SUBMITTED_CHAIN,chain):
        item=authenticated_commit(entry)
        need(item['sha']==expected_oid and item['parents']==[prior],'Exact ordered linear submitted chain; no author-turn inference')
        prior=item['sha']
    need(chain[-1]['tree']==CURRENT_TREE,'Full submitted final root')
    need(exact(scope.get('changed_leaves'),sorted([QUEUE]+[row['repository_path'] for row in submitted_inventory()])),'Full PR scope is32 attempt additions plusQUEUE, not final eight-leaf review commit')
    need(type(scope) is dict and set(scope)=={'changed_leaves','new_directories','deleted_directories'},'Exact immutable submission scope')
    need(scope['deleted_directories']==[] and type(scope['changed_leaves']) is list
         and scope['changed_leaves']==sorted(set(scope['changed_leaves'])) and scope['changed_leaves']
         and all(path==QUEUE or path.startswith(ATTEMPT+'/') for path in scope['changed_leaves']),'No foreign submitted patch')
    need(type(scope['new_directories']) is list and scope['new_directories']==sorted(set(scope['new_directories'])),'Exact submitted new directories')
    for path in scope['changed_leaves']+scope['new_directories']:rel(path)
    return r

def evidence_roles(phase):
    return {'math','custody','priority','whole_package','publication','tracker','ready','case_ready'}|({'merge'} if phase=='completion100' else set())

def publication_identity(m):
    e=m['evidence_references'];pub=root_ref(e['publication']);track=root_ref(e['tracker'])
    matches(pub,{'schema':'pr239-root-actual-publication-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,
        'accepted':True,'published':True,'actual_submitted_record_verified_by_top_level_kit':True,
        'public_body_downloads_SHA256_verified':True,'new_publication':True,'unknown_outcome':False},
        'Actual NEW publication receipt required')
    need(type(pub.get('record_id')) is int and pub['record_id']>0 and type(pub.get('doi')) is str
         and re.fullmatch(r'10\.5281/zenodo\.[0-9]+',pub['doi']) is not None,'Actual own new DOI/id')
    need(pub['doi']=='10.5281/zenodo.'+str(pub['record_id']),'Exact DOI and actual record association')
    rows=pub.get('files');need(type(rows) is list and 2<=len(rows)<=64
         and len({r.get('name') for r in rows})==len(rows),'Finite unique actual uploads')
    for row in rows:
        need(type(row) is dict and type(row.get('name')) is str and Path(row['name']).name==row['name']
             and type(row.get('size')) is int and 0<row['size']<=100_000_000 and hexid(row.get('sha256'),64),'Actual upload name/bytes/hash')
    need(any(r['name'].lower().endswith('.pdf') for r in rows) and any(r['name'].lower().endswith('.zip') for r in rows),'Published PDF and source ZIP')
    matches(track,{'schema':'pr239-root-actual-tracker-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,
        'accepted':True,'appended_once':True,'native_readback_verified':True,'fresh_duplicate_check_accepted':True,
        'publication_receipt':e['publication'],'spreadsheet_id':SPREADSHEET,'tab':'Math Puzzles'},'Actual one-append tracker receipt')
    row=track.get('row');range_=track.get('range')
    need(type(row) is list and len(row)==4 and all(type(x) is str for x in row)
         and '30001321' in row[0] and row[2]=='https://doi.org/'+pub['doi']
         and 'https://github.com/AlecKriebel/Math/pull/239' in row[3]
         and type(range_) is str and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",range_) is not None,
         'Exact actual four-cell row/own DOI/range')
    return {'doi':pub['doi'],'record_id':pub['record_id'],'range':range_,'files':rows}

def merge_identity(m):
    need(m['phase']=='completion100','Actual merge receipt exists only for completion100')
    r=root_ref(m['evidence_references']['merge'])
    matches(r,{'schema':'pr239-root-actual-original-pr-merge-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':239,'accepted':True,'actual_original_PR_merged':True,'actual_original_head':CURRENT,
        'actual_original_PR_state':'closed','actual_original_PR_is_draft':False,
        'merge95_full_scope_and_all_selected_bodies_verified':True,'merge95_all_five_verified':True,
        'actual_Root_expected_SHA_force_false_CAS_and_readback_accepted':True},'Separate actual merge95 Root receipt')
    need(hexid(r.get('merge_candidate')) and hexid(r.get('merge_tree')) and hexid(r.get('parent'))
         and exact(r.get('ordered_parents'),[r['parent'],CURRENT]),'Exact actual two-parent merge')
    cas=root_ref(r['actual_CAS_acceptance'])
    matches(cas,{'schema':'pr239-root-completion-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':239,'accepted':True,'candidate':r['merge_candidate'],'tree':r['merge_tree'],'parent':r['parent'],
        'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
        'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False,'facts':phase_facts('merge95')},
        'True earlier phase95 CAS evidence required')
    request=root_ref(cas['actual_tool_request']);response=root_ref(cas['actual_tool_response'])
    matches(request,{'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
        'expected_sha':r['parent'],'sha':r['merge_candidate'],'force':False},'Actual merge CAS request')
    matches(response,{'isError':False,'structuredContent':{'success':True}},'Actual successful merge CAS response')
    return r

def validate_ready_value(m,evidence,ready):
    matches(ready,{'schema':'pr239-root-case-ready-publication-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':239,'accepted':True,'mathematical_review_accepted':True,'priority_review_accepted':True,
        'two_distinct_fresh_whole_package_reviews_accepted':True,'final_package_frozen':True,
        'actual_new_publication_and_unique_tracker_append_verified':True,'actual_ready_PR_verified':True,
        'original_and_current_claimed_solved_3of5_preserved':True,'ordered239_intake_and234_bridge_accepted':True,
        'native_identity_receipt':m['native_identity_receipt'],'current_head':CURRENT,
        'evidence_references':{k:v for k,v in evidence.items() if k not in ('case_ready','merge')},
        'numeric_advance_authorized_by_this_file':False,'phase95_cumulative_publication_membership_held_at39':True},
        'Future exact Root final-publication gate required')
    publication_identity(m)
    r=root_ref(evidence['ready'])
    matches(r,{'schema':'pr239-root-actual-ready-PR-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,
        'accepted':True,'actual_PR_ready_for_review':True,'actual_draft':False,'actual_merged':False,
        'actual_state':'open','actual_original_head':CURRENT,'final_body_pin':m['current_PR_opaque_body_pin']},
        'Actual Root ready presentation receipt required')
    need(type(r.get('final_title')) is str and re.match(r'^30001321\s*:',r['final_title']) is not None,'Root-bound ready title')
    return r

def validate_pr_metadata(value,m,allow_post=False,post=False):
    ready=root_ref(m['evidence_references']['ready'])
    matches(value,{'number':239,'title':ready['final_title'],'draft':False},'Exact accepted ready presentation')
    need(value['head']['sha']==CURRENT and value['head']['ref']=='dot/math-30001321'
         and value['base']['ref']=='main' and exact(pin(compact(value.get('body')).encode()),m['current_PR_opaque_body_pin']),'Exact ready HEAD/branch/base/body')
    if m['phase']=='completion100':
        oid=merge_identity(m)['merge_candidate']
        matches(value,{'state':'closed','merged':True,'merge_commit_sha':oid},'Actual original PR merged')
    elif value.get('merged') is True:
        need(allow_post or post,'PR closed before admitted merge effect')
        need(hexid(m.get('expected_candidate')),'Exact admitted merge candidate required')
        matches(value,{'state':'closed','merge_commit_sha':m['expected_candidate']},'Actual merge must match admitted C1')
    else:
        need(not post,'Post-CAS closure requires actual merged PR, not ancestry alone')
        matches(value,{'state':'open','merged':False},'Open ready/unmerged before C1')
    if value.get('merged') is True:need(type(value.get('merged_at')) is str and bool(value['merged_at']),'Actual merged timestamp')
    return value

def pr_identity(observer,m,pool,allow_post=False,post=False):
    api=GetOnly(observer);identity=native_identity(m);trees=core().NativeTrees(api)
    for row in [identity['submitted_base_commit']]+identity['submitted_commit_chain']:
        value=api('GET','git/commits/'+row['sha'])
        need(value.get('sha')==row['sha'] and value['tree']['sha']==row['tree']
             and [x['sha'] for x in value['parents']]==row['parents'],'Authenticated immutable original/parent association')
    base_root=identity['submitted_base_commit']['tree']
    need(trees.lookup(base_root,ATTEMPT) is None,'Original full attempt was added, not inherited or overwritten')
    need(trees.lookup(base_root,QUEUE)==tuple_pin(identity['submitted_base_queue']),'Exact full-submission base QUEUE association')
    base_queue=pool.get(observer,identity['submitted_base_queue']['sha'])
    leaves,dirs,deleted=trees.changes(base_root,CURRENT_TREE)
    need(leaves==set(identity['submitted_scope']['changed_leaves']) and dirs==set(identity['submitted_scope']['new_directories'])
         and deleted==set(identity['submitted_scope']['deleted_directories']),'Complete submitted first-parent to H scope')
    before=validate_pr_metadata(api('GET','pulls/239'),m,allow_post,post)
    for row in submitted_inventory():
        need(trees.lookup(CURRENT_TREE,row['repository_path'])==('100644','blob',row['native_blob']),'All original32 path associations')
        pool.get(observer,row['native_blob'],{k:row[k] for k in ('bytes','sha256')})
    need(trees.lookup(CURRENT_TREE,QUEUE)==('100644','blob',CURRENT_QUEUE),'Original current QUEUE association')
    raw=pool.get(observer,CURRENT_QUEUE);row,cells=own_queue_row(raw)
    need(exact(pin(row),CURRENT_ROW) and cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'3/5','Original status/3of5 unchanged')
    base_row,base_cells=own_queue_row(base_queue)
    need(exact(pin(base_row),SUBMITTED_BASE_ROW) and base_cells[8].strip()==b'queued' and base_cells[9].strip()==b'0/5','Original full-scope pre-row queued0of5')
    need([x for x in base_queue.splitlines(keepends=True) if x!=base_row]==[x for x in raw.splitlines(keepends=True) if x!=row],'All full-submission QUEUE foreign bytes preserved')
    after=validate_pr_metadata(api('GET','pulls/239'),m,allow_post,post)
    if after['merged']:
        if m['phase']=='completion100':
            merge=merge_identity(m);wanted_tree=merge['merge_tree'];parents=merge['ordered_parents']
        else:wanted_tree=m['expected_tree'];parents=commit_parents(m,m['expected_parent'])
        value=api('GET','git/commits/'+after['merge_commit_sha'])
        need(value.get('sha')==after['merge_commit_sha'] and value['tree']['sha']==wanted_tree
             and [x['sha'] for x in value['parents']]==parents,'Actual original merge native root and ordered P,H parents')
    need(exact(before,after),'PR changed during identity bracket')
    return {'HEAD':CURRENT,'state':after['state'],'draft':False,'merged':after['merged'],
        'current_status':'claimed_solved','original_merge_commit':after.get('merge_commit_sha') if after['merged'] else None,
        'same_selected_PR_identity':True}

def queue_transition(before,after,m):
    pre,cells=own_queue_row(before);post,postcells=own_queue_row(after)
    need(exact(pin(pre),m['queue_pre_row_pin']) and exact(pin(post),m['protected_queue_row_pin']),'Exact Root-bound own row pre/post')
    need(postcells[8].strip()==b'claimed_solved' and postcells[9].strip()==b'3/5','Own final status/3of5')
    need([x for x in before.splitlines(keepends=True) if x!=pre]==[x for x in after.splitlines(keepends=True) if x!=post],
         'All foreign QUEUE bytes/order/endings preserved')
    if m['phase']=='completion100':need(before==after,'Completion100 cannot rewrite QUEUE')

def queue_observation(observer,trees,root,m,pool,allow_foreign_rows,post=False):
    item=trees.lookup(root,QUEUE);need(item is not None and item[:2]==('100644','blob'),'Ordinary whole QUEUE')
    expected=m['queue_postimage'] if post else m['protected_queue']
    if not allow_foreign_rows:need(item==tuple_pin(expected),'Exact parent/C whole QUEUE')
    body=pool.get(observer,item[2]);row,cells=own_queue_row(body)
    wanted=m['protected_queue_row_pin'] if post else m['queue_pre_row_pin']
    need(exact(pin(row),wanted),'Exact own row at this phase')
    if post:need(cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'3/5','Own claimed3of5 preserved')
    return {'parent_QUEUE_oid':m['protected_queue']['sha'],'candidate_QUEUE_oid':m['queue_postimage']['sha'],
        'observed_QUEUE_oid':item[2],'whole_body_pin':pin(body),'own_row_pin':pin(row),
        'foreign_rows_may_differ':allow_foreign_rows,'policy':QUEUE_POLICY,'actual_native_body_origin':pool.origin(observer,item[2])}

def carry_path(path):
    rel(path);required=decode(sealed('CARRY_REQUIRED.json',CARRY_PIN))
    if path in required:return True
    if not path.startswith(OLD_CASE):return False
    parts=path[len(OLD_CASE):].split('/')
    forbidden=('private','_private','packet','journal','runtime','_runtime','sandbox','_synthetic','root_admin','root_complete','raw','_raw')
    return not any(p.lower().startswith(forbidden) or p.lower() in ('extracted','objects','inputs') or any(x in p.lower() for x in ('raw_stdout','raw_stderr','api_receipt')) for p in parts) and Path(path).suffix.lower() in ('.json','.md','.py','.txt','.tex','.csv','.patch','.sha256')

def carry_inventory(reference):
    r=root_ref(reference)
    matches(r,{'schema':'pr239-root-prior-operational-carry-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':239,'accepted':True,'prior_terminal_pin':PRIOR_TERMINAL_PIN,'finite_positive_public_selection_reviewed':True,
        'ordered239_intake_and_additive234_skip_preserved':True},'Root finite carry gate')
    rows=r.get('files');need(type(rows) is list and 1<=len(rows)<=MAX_FILES,'Finite carry')
    out={}
    for row in rows:
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'Exact carry row')
        path=rel(row['path']);need(carry_path(path) and path not in out,'Finite safe carry path')
        out[path]=bytepin({k:row[k] for k in ('bytes','sha256')})
    required=decode(sealed('CARRY_REQUIRED.json',CARRY_PIN))
    need(all(exact(out.get(k),v) for k,v in required.items()),'Exact218terminal/status chain/234 bridge required')
    return out

def validate_carryforward(carry,reference):
    pins=carry_inventory(reference)
    need(type(carry) is list and len(carry)==len(pins) and all(type(r) is dict and set(r)=={'path','bytes','sha256'} for r in carry)
         and len({r['path'] for r in carry})==len(pins),'Exact finite carry records')
    need(exact({r['path']:{k:r[k] for k in ('bytes','sha256')} for r in carry},pins),'Exact carry body pins')
    return pins

def science_path(path):
    rel(path)
    return path.startswith(ATTEMPT+'/') and Path(path).suffix.lower() in ('.json','.md','.py','.txt','.tex','.csv','.patch','.sha256')


def load_inputs(manifest_ref,acceptance_ref,source_manifest_pin,protocol_pin,primitive_pin):
    m=root_ref(manifest_ref)
    keys={'schema','PR','problem_id','phase','facts','files','total_files','total_bytes','local_views','carry_inventory',
        'protected_queue','queue_postimage','queue_pre_row_pin','protected_queue_row_pin','protected_nodes','post_attempt_tree',
        'science_allowlist','current_PR_opaque_body_pin','expected_new_directories','expected_changed_paths','carryforward',
        'commit_author','commit_committer','commit_message','retired_candidates','body_proof_policy','QUEUE_policy',
        'writer_lock','evidence_references','native_identity_receipt','protected_bodies'}
    need(type(m) is dict and set(m)==keys,'Exact239 logical packet fields')
    phase=m['phase'];matches(m,{'schema':'pr239-conditional-publication-logical-packet-v1','PR':239,'problem_id':'30001321',
        'facts':phase_facts(phase),'body_proof_policy':BODY_POLICY,'QUEUE_policy':QUEUE_POLICY,'writer_lock':WRITER_LOCK_REFERENCE},'Typed phase facts/policies')
    need(type(m['retired_candidates']) is list and m['retired_candidates']==sorted(set(m['retired_candidates']))
         and len(m['retired_candidates'])<=100 and all(hexid(x) for x in m['retired_candidates']),'RetiredOID denylist')
    for key in ('protected_queue','queue_postimage'):need(tuple_pin(m[key]) is not None,'Existing regular QUEUE tuple')
    for key in ('queue_pre_row_pin','protected_queue_row_pin','current_PR_opaque_body_pin'):bytepin(m[key])
    need(type(m['protected_nodes']) is dict and set(m['protected_nodes'])=={ATTEMPT,SHARED},'Only exact attempt/old-audit opaque roots')
    for row in m['protected_nodes'].values():preserved_tuple(row,True)
    need(preserved_tuple(m['post_attempt_tree'],True) is not None,'Explicit positive post-attempt tree')
    if phase=='completion100':need(exact(m['post_attempt_tree'],m['protected_nodes'][ATTEMPT]),'Terminal science stays opaque unchanged')
    bodyrows=m['protected_bodies']
    need(type(bodyrows) is list and len(bodyrows)<=64 and len({r.get('path') for r in bodyrows})==len(bodyrows),'Finite protected bodies')
    for r in bodyrows:
        need(type(r) is dict and set(r)=={'path','mode','type','sha','bytes','sha256'}
             and (rel(r['path']).startswith(ATTEMPT+'/') or r['path'].startswith(SHARED+'/')),'Explicit own protected body only')
        preserved_tuple({k:r[k] for k in ('mode','type','sha')});bytepin({k:r[k] for k in ('bytes','sha256')})
    science=m['science_allowlist'];need(type(science) is list and len(science)<=200 and len({r.get('path') for r in science})==len(science),'Finite explicit science targets')
    sc={}
    for r in science:
        need(type(r) is dict and set(r)=={'path','bytes','sha256'} and science_path(r['path']),'Exact own science row, no folder permission')
        sc[r['path']]=bytepin({k:r[k] for k in ('bytes','sha256')})
    if phase=='merge95':
        for r in submitted_inventory():need(r['repository_path'] in sc and exact(sc[r['repository_path']],{k:r[k] for k in ('bytes','sha256')}),'All32 exact current science bodies required')
    else:need(not sc and exact(m['protected_queue'],m['queue_postimage']),'Terminal no attempt/QUEUE overlay')
    identity=native_identity(m);carrypins=validate_carryforward(m['carryforward'],m['carry_inventory'])
    rows=m['files'];need(type(rows) is list and 5<len(rows)<=MAX_FILES and len({r.get('path') for r in rows})==len(rows),'Finite distinct selected rows')
    overlay={};pre={}
    for row in rows:
        need(type(row) is dict and set(row)=={'path','source','bytes','sha256','git_blob','preimage'},'Exact selected row fields')
        path=rel(row['path'])
        need(path in VIEWS or public_path(path) or path in carrypins or path in sc or (path==QUEUE and phase=='merge95'),'Positive owned scope only')
        raw=sealed(row['source'],{k:row[k] for k in ('bytes','sha256')})
        need(hexid(row['git_blob']) and native('blob',raw)==row['git_blob'] and '\0' not in raw.decode('utf-8'),'Finite UTF8 only; no PDF/ZIP native uploads')
        overlay[path]=raw;pre[path]=tuple_pin(row['preimage'])
        if path not in VIEWS and path not in sc and path!=QUEUE:need(pre[path] in (None,('100644','blob',row['git_blob'])),'Archive/carry add-or-exact-noop')
        if path in sc:need(exact(pin(raw),sc[path]),'Root science allowlist exact bytes')
        if path in carrypins:need(exact(pin(raw),carrypins[path]),'Exact carry bytes')
    need(set(VIEWS).issubset(overlay) and set(carrypins).issubset(overlay) and set(sc).issubset(overlay),'All five/carry/science bodies present')
    for path,row in original_archives().items():
        need(path in overlay and exact(pin(overlay[path]),{k:row[k] for k in ('bytes','sha256')})
             and native('blob',overlay[path])==row['native_blob'],'All32 original archives verbatim')
    if QUEUE in overlay:
        need(pre[QUEUE]==tuple_pin(m['protected_queue']) and native('blob',overlay[QUEUE])==m['queue_postimage']['sha'],'Exact QUEUE pre/post association')
    else:need(exact(m['protected_queue'],m['queue_postimage']),'No implicit QUEUE correction')
    need(type(m['total_files']) is int and m['total_files']==len(rows) and type(m['total_bytes']) is int
         and m['total_bytes']==sum(map(len,overlay.values()))<=MAX_TOTAL,'Exact bounded totals')
    for key in ('expected_changed_paths','expected_new_directories'):
        values=m[key];need(type(values) is list and values==sorted(set(values)) and len(values)<=600,'Finite canonical expected scope')
        for path in values:rel(path)
    need(m['expected_changed_paths'] and set(m['expected_changed_paths']).issubset(overlay),'Nonempty exact changed leaves')
    for path in (VIEWS[0],VIEWS[2]):
        obj=decode(overlay[path]);matches(obj,phase_facts(phase),'Exact conditional view facts')
        need(obj.get('conditional_proposal_only') is True,'No Root terminal authority from proposed views')
    progress=decode(overlay[VIEWS[2]])
    for key,arr in phase_memberships(phase).items():need(exact(progress.get(key),arr),'Exact conservative phase memberships')
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Dated99 unchanged')
    for path in (VIEWS[1],VIEWS[3],VIEWS[4]):markdown_current(overlay[path],phase,path in (VIEWS[1],VIEWS[4]))
    local=m['local_views'];need(type(local) is list and len(local)==5 and [r.get('path') for r in local]==list(VIEWS),'Separate ordered local five preimages')
    for row in local:
        need(type(row) is dict and set(row)=={'path','preimage','source'},'Exact separate local view')
        if row['preimage'] is None:need(row['source'] is None,'Absent local source null')
        else:
            raw=sealed(row['source'],row['preimage'])
            if row['path'] in (VIEWS[1],VIEWS[4]):need(overlay[row['path']].startswith(raw),'Preserve local log bytes')
    for key in ('commit_author','commit_committer'):need(exact(m[key],{'name':'Alec Kriebel','email':'me@aleckriebel.com'}),'Fixed identity')
    need(m['commit_message']==commit_message(phase),'Exact neutral no-autoclose message')
    evidence=m['evidence_references'];need(type(evidence) is dict and set(evidence)==evidence_roles(phase),'Exact Root evidence roles')
    for role,reference in evidence.items():
        value=root_ref(reference);path=Path(reference['path'])
        need(path.is_relative_to(LOCAL_CASE),'Case-owned Root evidence')
        target=path.relative_to(CHECKOUT).as_posix()
        need(target in overlay and exact(pin(overlay[target]),{k:reference[k] for k in ('bytes','sha256')}),'All Root evidence positively archived')
        if role in ROOT_EVIDENCE:need(exact({k:reference[k] for k in ('bytes','sha256')},ROOT_EVIDENCE[role]) and path==LOCAL_CASE/ROOT_EVIDENCE_PATHS[role],'Pinned existing math/custody inputs')
    ready=root_ref(evidence['case_ready']);validate_ready_value(m,evidence,ready)
    for role in ('priority','whole_package'):matches(root_ref(evidence[role]),{'PR':239,'accepted':True},'Actual Root priority/full-package acceptance')
    if phase=='completion100':merge_identity(m)
    for reference in (m['native_identity_receipt'],m['carry_inventory']):
        target=Path(reference['path']).relative_to(CHECKOUT).as_posix()
        need(target in overlay and exact(pin(overlay[target]),{k:reference[k] for k in ('bytes','sha256')}),'Actual native/carry acceptance body archived')
    gate=root_ref(acceptance_ref)
    matches(gate,{'schema':'pr239-root-completion-logical-packet-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':239,'phase':phase,'accepted':True,'manifest_pin':{k:manifest_ref[k] for k in ('bytes','sha256')},
        'source_manifest_pin':source_manifest_pin,'protocol_pin':protocol_pin,'primitive_pin':primitive_pin,
        'facts':phase_facts(phase),'native_identity_receipt':m['native_identity_receipt'],'case_ready_receipt':evidence['case_ready'],
        'public_selection_reviewed':True,'actual_new_publication_tracker_ready_verified':True,
        'no_provider_or_PR_writer_in_engine':True,'exact_baseline_plus239_only_at_completion100':True,
        'QUEUE_policy':QUEUE_POLICY,'Root_full_source_read':True,'independent_source_adversarial_review_accepted':True,
        'independent_exact_packet_review_accepted':True},'Separate actual exact logical/source gate')
    audits=gate.get('audit_receipts');need(type(audits) is list and len(audits)==2 and len({r.get('path') for r in audits})==2,'Two distinct source/exact audit refs')
    for row in audits:root_ref(row)
    return m,overlay,pre
