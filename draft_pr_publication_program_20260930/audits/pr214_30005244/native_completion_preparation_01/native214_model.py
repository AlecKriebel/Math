"""Pure conditional PR214 adopted-publication completion model. No writer, transport or CLI."""
import base64,calendar,datetime,hashlib,json,math,os,re,stat,types
from pathlib import Path,PurePosixPath
BASE=Path(__file__).absolute().parent
LOCAL_CASE=BASE.parent
LOCAL_PROGRAM=LOCAL_CASE.parents[1]
CHECKOUT=LOCAL_PROGRAM.parent
PROGRAM='draft_pr_publication_program_20260930/'
CASE=PROGRAM+'audits/pr214_30005244/'
OLD_CASE=PROGRAM+'audits/pr212_30005310/'
ATTEMPT='unsolved_math_prioritization/attempts/30005244'
SHARED='draft_pr_descending_audit_20261002/audits/pr214_30005244'
QUEUE='unsolved_math_prioritization/QUEUE.md'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md',PROGRAM+'CURRENT_PROGRESS.json',PROGRAM+'CURRENT_PROGRESS.md',PROGRAM+'RESEARCH_LOG.md')
ANCHOR='cc8bddeff9f8e27848b94808915c22473b7e68e7'
ORIGINAL='36d5ef15098163e74bf14c2e696f560ce592affd'
ORIGINAL_TREE='6788a74181eb1730ec961f78c3ddee6c763b728c'
ORIGINAL_PARENT='37e5d6ee0f3e03de5636edf2b00dd6df77f9a494'
CURRENT='95ba37055ebf1e7b4f9d76aa43816c9978c7bce8'
CURRENT_TREE='eb7cdb30bff245e3f36ea282fbcaa099e1038c57'
CURRENT_PARENTS=[ORIGINAL,'5fde5b9aa46bb620d7a0d3b036ceb914076c6303']
MERGED='4abf30daa991860a275b3d25745159852757ad35'
MERGED_TREE=CURRENT_TREE
MERGED_PARENTS=['5fde5b9aa46bb620d7a0d3b036ceb914076c6303',CURRENT]
CURRENT_QUEUE='db667ab8e5eab5cabe907f00d7ba2eebba496a3f'
CURRENT_ROW={'bytes':279,'sha256':'5959bcc920b7eb0026004888f85a038caaea9f6950b232e6b4ca04d95a38d9b5'}
EXISTING_DOI='10.5281/zenodo.23390551'
EXISTING_TRACKER="'Math Puzzles'!A105:D105"
COMMIT_MESSAGE='Archive PR214 accepted existing publication completion\n'
CORE_PIN={'bytes':4719,'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}
WRITER_LOCK_REFERENCE={'path':PROGRAM+'ROOT_GLOBAL_FIVE_WRITER.lock','device':16777232,'inode':439078796,'bytes':153,'sha256':'61404e167a3dedccc0fd17a1a1823fd772bc12a9144a4f012ab26d5e2a26fc0a'}
PRIOR_TERMINAL_PATH=OLD_CASE+'ROOT_ACTUAL_ADMINISTRATIVE_SKIP_VERIFICATION_01.json'
PRIOR_TERMINAL_PIN={'bytes':15982,'sha256':'abe1832e140850c6ac935042775e6180a0c8483738b311abe04de7272a551611'}
CARRY_INVENTORY=LOCAL_PROGRAM/'audits/pr212_30005310/next_checkpoint_carry_preparation_01/PROPOSED_CARRY_INVENTORY.json'
CARRY_INVENTORY_PIN={'bytes':150305,'sha256':'47c291d5f4c3bb86ad6745a10d72628d850825d10733707584416550d546ec13'}
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
    need(hexid(tree) and type(parents) is list and len(parents) == 1 and parents[0] not in (ORIGINAL,CURRENT,MERGED)
         and all(hexid(p) for p in parents), 'Exact deterministic commit tree/parents')
    author,committer = identity(m['commit_author']),identity(m['commit_committer'])
    need(m['commit_message']==COMMIT_MESSAGE,
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
        allowed = path in ('git/ref/heads/main','pulls/214') or re.fullmatch(
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


ROOT_EVIDENCE={'math':{'bytes':8102,'sha256':'bbe3367361a402b920d6576ed8ab398f96998a28077d7278e7b8a0ee7727b5ad'},
 'custody':{'bytes':3365,'sha256':'529fbbb3ca2b850e530434b7d10f2d356e58a7e2c18a1349bc45fff08343075e'}}
ROOT_EVIDENCE_PATHS={'math':'ROOT_MATHEMATICAL_ACCEPTANCE_01.json','custody':'ROOT_NATIVE_CUSTODY_ACCEPTANCE_01.json'}
EVIDENCE_ROLES={'math','custody','priority','adoption','case_ready'}

def root_ref(row):
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['path']) is str,'Exact canonical file reference')
    path=Path(row['path']);need(path.is_absolute() and path.is_relative_to(CHECKOUT),'Checkout-owned input reference')
    raw,identity=read_regular(path)
    need(exact(pin(raw),bytepin({k:row[k] for k in ('bytes','sha256')})),'Referenced body changed')
    return decode(raw)

def phase_facts(phase='completion100'):
    need(phase=='completion100','Only conditional adopted-publication completion')
    return {'active_PR':214,'workflow_percent':100,'completed':True,
            'fully_completed_count':54,'published_count':38,'last_completed_PR':214,
            'next_numeric_intake_cursor':215,'goal_complete':False,
            'completed_eligible_workflow':True,'publication_workflow_completed':True,'publication_ready':True,
            'original_eligible_status':'claimed_solved','current_status':'claimed_solved',
            'actual_original_PR_merged':True,'adopted_existing_publication':True,
            'no_new_provider_publication_or_tracker_append':True,
            'current_head':CURRENT,'original_merge_commit':MERGED,
            'existing_publication_DOI':EXISTING_DOI,'existing_tracker_range':EXISTING_TRACKER,
            'numeric_advance_conditional_on_actual_Root_terminal':True,
            'advance_to_next_PR_authorized_now':False}

def baseline_facts():
    # PR213 status-only skip need not have rewritten the previous native five.
    return {'fully_completed_count':53,'published_count':37,'last_completed_PR':211,
            'next_numeric_intake_cursor':213,'goal_complete':False}

def phase_marker(phase='completion100'):
    return ('<!-- PR214_NATIVE_PHASE_FACTS '+compact(phase_facts(phase))+' -->').encode()

def markdown_current(raw,phase,append_log):
    need(type(raw) is bytes and type(append_log) is bool,'Explicit Markdown body/log policy')
    current=phase_marker(phase);stem=b'<!-- PR214_NATIVE_PHASE_FACTS'
    lines=raw.splitlines()
    while lines and lines[-1]==b'':lines.pop()
    markers=[line for line in lines if line.startswith(stem)]
    need(raw.count(stem)==len(markers)==1 and markers==[current] and lines[-1]==current,
         'One canonical current completion terminal marker; historical other-case markers preserved')

def public_path(path):
    rel(path)
    if not path.startswith(CASE) or path in VIEWS:return False
    parts=path[len(CASE):].split('/')
    forbidden=('private','_private','packet','journal','runtime','_runtime','sandbox','_synthetic','root_admin214_')
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
        suspected=any(re.search(rb'(?<![0-9])30005244(?![0-9])',cell) for cell in cells[:4])
        if not suspected:continue
        need(line.startswith(b'|') and len(cells)==14
             and cells[2].strip()==b'30005244 / OWR-11101924-008',
             'Indented/malformed own QUEUE row or noncanonical own code')
        found.append((line,cells))
    need(len(found)==1,'Exactly one own QUEUE row; missing/duplicate refused')
    return found[0]

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

def native_identity(m):
    receipt=root_ref(m['native_identity_receipt'])
    matches(receipt,{'schema':'pr214-root-native-completion-identity-acceptance-v1',
        'evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':214,'accepted':True,
        'raw_commit_SHA1_SHA256_and_ordered_parents_verified':True,
        'fresh_Main_existing_merged_science_association_verified':True,
        'whole_existing_science_and_old_audit_protected_without_rewrite':True,
        'post_merge_Main_drift_extension_accepted':True,
        'protected_nodes':m['protected_nodes'],'protected_bodies':m['protected_bodies'],
        'current_PR_opaque_body_pin':m['current_PR_opaque_body_pin']},
        'Later exact Root native identity/custody acceptance required')
    drift=root_ref(receipt.get('post_merge_Main_drift_extension'))
    matches(drift,{'PR':214,'accepted':True},'Exact accepted Root post-merge drift extension required')
    rows=receipt.get('commits')
    need(type(rows) is list and len(rows)==3,'Original, prepared and actual merge separately authenticated')
    for row,oid,tree,parents in zip(rows,[ORIGINAL,CURRENT,MERGED],
            [ORIGINAL_TREE,CURRENT_TREE,MERGED_TREE],[[ORIGINAL_PARENT],CURRENT_PARENTS,MERGED_PARENTS]):
        authenticated_commit(row)
        matches(row,{'sha':oid,'tree':tree,'parents':parents},'Actual immutable native association')
    return receipt

def validate_pr_metadata(value,m):
    matches(value,{'number':214,'title':'30005244: audited DDA spectral convergence under (G) and published preprint',
        'state':'closed','draft':False,'merged':True,'merged_at':'2026-10-15T09:28:52Z',
        'merge_commit_sha':MERGED},'Already merged original PR must remain unchanged')
    need(value['head']['sha']==CURRENT and value['head']['ref']=='dot/math-30005244'
         and value['base']['ref']=='main','Exact current HEAD/branch/base')
    need(exact(pin(compact(value.get('body')).encode()),m['current_PR_opaque_body_pin']),'Opaque PR body changed')
    return value

def validate_ready_value(m,evidence,ready):
    matches(ready,{'schema':'pr214-root-case-ready-adoption-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':214,'accepted':True,'mathematical_review_accepted':True,'priority_review_accepted':True,
        'existing_publication_adoption_accepted':True,'two_sequential_fresh_whole_package_reviews_accepted':True,
        'original_and_current_claimed_solved_eligibility_preserved':True,'already_merged_original_PR_verified':True,
        'existing_DOI_and_unique_tracker_row_reused':True,'no_new_provider_publication_or_tracker_append':True,
        'existing_scientific_package_frozen':True,'prior_PR213_status_only_skip_accepted':True,
        'native_identity_receipt':m['native_identity_receipt'],
        'current_head':CURRENT,'original_merge_commit':MERGED,'existing_publication_DOI':EXISTING_DOI,
        'existing_tracker_range':EXISTING_TRACKER,
        'evidence_references':{k:v for k,v in evidence.items() if k!='case_ready'},
        'numeric_advance_authorized_by_this_file':False},
        'Later exact Root case-ready/adoption gate required; no optimistic clearance')


def pr_identity(observer,m,pool):
    api=GetOnly(observer);identity=native_identity(m)
    for row in identity['commits']:
        commit=api('GET','git/commits/'+row['sha'])
        need(commit.get('sha')==row['sha'] and commit['tree']['sha']==row['tree']
             and [x['sha'] for x in commit['parents']]==row['parents'],
             'Actual original/prepared/merge ordered association differs')
    def pr():
        value=api('GET','pulls/214')
        validate_pr_metadata(value,m)
        return value
    pr()
    trees=core().NativeTrees(api)
    need(trees.lookup(CURRENT_TREE,QUEUE)==('100644','blob',CURRENT_QUEUE),'Prepared HEAD QUEUE association')
    body=pool.get(observer,CURRENT_QUEUE);row,cells=own_queue_row(body)
    need(exact(pin(row),CURRENT_ROW) and cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'2/5',
         'Original eligible/current native claimed_solved status required')
    pr()
    return {'HEAD':CURRENT,'state':'closed','draft':False,'merged':True,'current_status':'claimed_solved',
            'original_merge_commit':MERGED,'current_QUEUE_oid':CURRENT_QUEUE,
            'current_row_pin':pin(row),'same_selected_PR_identity':True}

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

def completion_memberships():
    return {key:value+[214] for key,value in source_baseline().items()}

def carry_inventory():
    raw,unused=read_regular(CARRY_INVENTORY)
    need(exact(pin(raw),CARRY_INVENTORY_PIN),'Exact finite149-file carry inventory required')
    value=decode(raw)
    rows=value.get('files')
    if rows is None:rows=value.get('proposed_files')
    need(type(rows) is list and len(rows)==149,'Exact prior149 positive carry records')
    result={}
    for row in rows:
        path=rel(row['path']);p=bytepin({k:row[k] for k in ('bytes','sha256')})
        need(path not in result,'Duplicate positive carry path');result[path]=p
    need(exact(result.get(PRIOR_TERMINAL_PATH),PRIOR_TERMINAL_PIN),'Exact actual212 terminal carry')
    return result

def validate_carryforward(carry):
    carrypins=carry_inventory()
    need(type(carry) is list and len(carry)==149 and all(type(r) is dict and set(r)=={'path','bytes','sha256'} for r in carry)
         and len({r['path'] for r in carry})==149,'Exactly the reviewed finite149 carry paths')
    need(exact({r['path']:{k:r[k] for k in ('bytes','sha256')} for r in carry},carrypins),
         'Carry exceptions are exact path/body pins, no folder permission')
    return carrypins

def load_inputs(manifest_ref,acceptance_ref,source_manifest_pin,protocol_pin,primitive_pin):
    m=root_ref(manifest_ref)
    keys={'schema','PR','problem_id','phase','facts','files','total_files','total_bytes','local_views',
          'protected_queue','protected_queue_row_pin','protected_nodes','current_PR_opaque_body_pin',
          'expected_new_directories','expected_changed_paths','carryforward','commit_author','commit_committer','commit_message',
          'retired_candidates','body_proof_policy','QUEUE_policy','writer_lock','evidence_references','native_identity_receipt','protected_bodies'}
    need(type(m) is dict and set(m)==keys,'Exact completion logical packet fields')
    matches(m,{'schema':'pr214-conditional-completion-logical-packet-v1','PR':214,'problem_id':'30005244',
        'phase':'completion100','facts':phase_facts(),'body_proof_policy':BODY_POLICY,'QUEUE_policy':QUEUE_POLICY,
        'writer_lock':WRITER_LOCK_REFERENCE},'Typed completion facts/policies')
    need(type(m['retired_candidates']) is list and len(m['retired_candidates'])<=100
         and m['retired_candidates']==sorted(set(m['retired_candidates'])) and all(hexid(x) for x in m['retired_candidates']),'Explicit retired candidate denylist')
    preserved_tuple(m['protected_queue']);bytepin(m['protected_queue_row_pin']);bytepin(m['current_PR_opaque_body_pin'])
    need(type(m['protected_nodes']) is dict and set(m['protected_nodes'])=={ATTEMPT,SHARED},'Protect fresh Main attempt and old audit including absence')
    for row in m['protected_nodes'].values():preserved_tuple(row,tree_only=True)
    bodies=m['protected_bodies']
    need(type(bodies) is list and len(bodies)<=64 and len({r.get('path') for r in bodies})==len(bodies)
         and all(type(r) is dict and set(r)=={'path','mode','type','sha','bytes','sha256'} for r in bodies),
         'Finite explicit already-published protected body association')
    for row in bodies:
        path=rel(row['path']);need(path.startswith(SHARED+'/') or path.startswith(ATTEMPT+'/'),'Protected own scientific source only')
        preserved_tuple({k:row[k] for k in ('mode','type','sha')});bytepin({k:row[k] for k in ('bytes','sha256')})
    native_receipt=native_identity(m)
    need(type(m['expected_new_directories']) is list and len(m['expected_new_directories'])<=600
         and m['expected_new_directories']==sorted(set(m['expected_new_directories'])),'Finite exact expected directories')
    for path in m['expected_new_directories']:rel(path)
    carrypins=validate_carryforward(m['carryforward'])
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
    for reference in (m['native_identity_receipt'],native_receipt['post_merge_Main_drift_extension']):
        target=Path(reference['path']).relative_to(CHECKOUT).as_posix()
        need(public_path(target) and target in overlay
             and exact(pin(overlay[target]),{k:reference[k] for k in ('bytes','sha256')}),
             'Exact Root native identity/drift acceptance positively archived')
    need(set(VIEWS).issubset(overlay) and set(carrypins).issubset(overlay),'All five and exact carryforward present')
    need(type(m['expected_changed_paths']) is list and m['expected_changed_paths']==sorted(set(m['expected_changed_paths']))
         and set(m['expected_changed_paths']).issubset(overlay) and len(m['expected_changed_paths'])>0,'Exact finite nonempty changed-leaf scope')
    need(type(m['total_files']) is int and m['total_files']==len(rows) and type(m['total_bytes']) is int
         and m['total_bytes']==sum(map(len,overlay.values()))<=MAX_TOTAL,'Exact bounded selected totals')
    for path in (VIEWS[0],VIEWS[2]):
        obj=decode(overlay[path]);matches(obj,phase_facts(),'Conditional completion structured view')
        matches(obj,{'conditional_proposal_only':True},'No false actual completion')
        for alias,key in (('current_PR','active_PR'),('PR','active_PR'),('current_publication_ready','publication_ready')):
            if alias in obj:matches(obj,{alias:phase_facts()[key]},'Structured completion alias')
        for alias,key in (('active_publication_DOI','existing_publication_DOI'),('active_tracker_range','existing_tracker_range')):
            if alias in obj:matches(obj,{alias:phase_facts()[key]},'Exact existing publication identity')
        if 'new_publication_or_tracker_append_performed' in obj:
            need(obj['new_publication_or_tracker_append_performed'] is False,'No new provider action')
    progress=decode(overlay[VIEWS[2]])
    for key,value in completion_memberships().items():
        need(exact(progress.get(key),value),'Exact baseline plus214 only')
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
    need(m['commit_message']==COMMIT_MESSAGE,'Fixed no-merge archival commit message')
    evidence=m['evidence_references']
    need(type(evidence) is dict and set(evidence)==EVIDENCE_ROLES,'Math/custody/priority/adoption/case-ready exact roles')
    for role,row in evidence.items():
        value=root_ref(row);path=Path(row['path'])
        need(path.is_relative_to(LOCAL_CASE),'Root case evidence natural path')
        target=path.relative_to(CHECKOUT).as_posix()
        need(target in overlay and exact(pin(overlay[target]),{k:row[k] for k in ('bytes','sha256')}),
             'Every exact Root evidence body positively archived')
        if role in ROOT_EVIDENCE:
            need(exact({k:row[k] for k in ('bytes','sha256')},ROOT_EVIDENCE[role])
                 and path==LOCAL_CASE/ROOT_EVIDENCE_PATHS[role],'Pinned existing Root math/custody')
    ready=root_ref(evidence['case_ready'])
    validate_ready_value(m,evidence,ready)
    for role in ('priority','adoption'):
        matches(root_ref(evidence[role]),{'PR':214,'accepted':True},'Actual separate priority/adoption acceptance')
    gate=root_ref(acceptance_ref)
    matches(gate,{'schema':'pr214-root-completion-logical-packet-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':214,'accepted':True,'manifest_pin':{k:manifest_ref[k] for k in ('bytes','sha256')},
        'source_manifest_pin':source_manifest_pin,'protocol_pin':protocol_pin,'primitive_pin':primitive_pin,
        'facts':phase_facts(),'case_ready_receipt':evidence['case_ready'],'native_identity_receipt':m['native_identity_receipt'],'public_selection_reviewed':True,'case_ready_adoption_gate_accepted':True,
        'no_new_provider_or_PR_actions':True,'exact_baseline_plus214_memberships':True,'QUEUE_policy':QUEUE_POLICY,
        'Root_full_source_read':True,'independent_source_adversarial_review_accepted':True,
        'independent_exact_packet_review_accepted':True},'Separate actual Root logical/source/exact packet acceptance required')
    audits=gate.get('audit_receipts')
    need(type(audits) is list and len(audits)==2 and len({r.get('path') for r in audits})==2,'Distinct source/exact audit receipts')
    for row in audits:root_ref(row)
    return m,overlay,pre
