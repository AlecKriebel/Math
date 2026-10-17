"""PR212 finite actual native custody; GitHub GET only, science never executed."""
import argparse,ast,base64,datetime,hashlib,json,os,posixpath,re,stat,sys,types
from pathlib import Path
from urllib.parse import unquote,urlsplit
BASE=Path(__file__).absolute().parent
ORIGINAL='c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7'
CURRENT='99af7a27a711271bcd0b9e7ce90e374e4100ea6d'
ROOTS={ORIGINAL:'436c162cea349eb2d07041202d32fd27c00df926',CURRENT:'3dd6b7b24c6eef3306ba47d939c6d75a2d2308de'}
PARENT='8431d4eb9b4fbb56cc82f5a4ac61514053c2958d'
OWN='unsolved_math_prioritization/attempts/30005310'
OLD='draft_pr_descending_audit_20261002/audits/pr212_30005310'
QUEUE='unsolved_math_prioritization/QUEUE.md'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
ACCEPT={'bytes':1985,'sha256':'5a40df678183a6254efc47ffb2150ba05d29a040b174237a9cba9f22df5d8439'}
INTAKE={'bytes':24331,'sha256':'7372c92dea26f315f3f2718f77965fb2b757b4c163b44396634b4694d8430e7c'}
CORE={'bytes':4719,'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}
PRIMITIVES={'bytes': 3794, 'sha256': '808149b347a61809e37a0b71fc4dc602ec17e63e38e985d99123827268286e09'}
MAX_GETS=1500
ROLE_FILES=300
ROLE_BYTES=8_000_000
ALL_BYTES=32_000_000

def need(value,message):
    if type(value) is not bool or not value:raise RuntimeError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rel(value):
    need(type(value) is str and value and '\\' not in value and '\0' not in value
         and not value.startswith('/') and all(s not in ('','.','..') for s in value.split('/')),'Safe relative path')
    return value
def read(path):
    path=Path(path);need(path.is_absolute() and path.resolve()==path,'Canonical source/evidence path')
    parent=os.open('/',os.O_RDONLY|os.O_DIRECTORY);fds=[]
    try:
        for part in path.parts[1:-1]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent);fds.append(parent);parent=nxt
        fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
        try:
            a=os.fstat(fd);need(stat.S_ISREG(a.st_mode) and stat.S_IMODE(a.st_mode)==0o444 and a.st_size<=16_000_000,'Readonly bounded ordinary file')
            with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read(a.st_size+1)
            ident=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
            need(ident(a)==ident(os.fstat(fd))==ident(os.stat(path.name,dir_fd=parent,follow_symlinks=False))
                 and len(raw)==a.st_size and path.resolve()==path,'Source/evidence changed during read')
            return raw
        finally:os.close(fd)
    finally:
        os.close(parent)
        for fd in reversed(fds):os.close(fd)
def module(name,path,wanted):
    raw=read(path);need(pin(raw)==wanted,'Pinned inherited primitive differs')
    out=types.ModuleType(name);out.__file__=str(path);exec(compile(raw,str(path),'exec'),out.__dict__);return out
def helpers():
    return module('get_primitives',BASE/'get_primitives.py',PRIMITIVES),module('native_core',BASE/'native_trees_readonly.py',CORE)
def put(name,raw):
    path=BASE/rel(name);need(path.resolve()==path,'Canonical owned output')
    path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    with path.open('xb') as f:
        need(f.write(raw)==len(raw),'Short output');f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
    return {'path':name,**pin(raw)}
def save(name,value):return put(name,enc(value))
def phase(percent,text):
    with (BASE/'RESEARCH_LOG.md').open('a') as f:f.write(now()+f' — {percent}% assigned custody. '+text+'\n')

def route_ok(route):
    return route in ('pulls/212','pulls/212/commits?per_page=100&page=1') or re.fullmatch(r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',route) is not None

class API:
    def __init__(self,g):
        self.g=g;self.count=0;self.cache={};self.failed=False;self.records=[];self.raw_bytes=0
        need(not (BASE/'_private_transport').exists(),'One-use collection only; no automatic retry/resume')
    def __call__(self,method,route,body=None):
        need(method=='GET' and body is None and route_ok(route) and not self.failed,'Only bounded native/selected-PR GET')
        if route.startswith('git/') and route in self.cache:return self.g.decode(self.cache[route])
        need(self.count<MAX_GETS,'GET count bound')
        self.count+=1;stem='_private_transport/'+str(self.count).zfill(4)
        argv=[GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+route]
        intent=save(stem+'.intent.json',{'UTC':now(),'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math',
            'route':route,'argv':argv,'automatic_retries':0})
        try:
            r=self.g.bounded_get(argv)
            out=put(stem+'.stdout.json',r.stdout);err=put(stem+'.stderr.txt',r.stderr)
            self.raw_bytes+=len(r.stdout)+len(r.stderr);need(self.raw_bytes<=64_000_000,'Aggregate transport bound')
            receipt=save(stem+'.receipt.json',{'UTC':now(),'method':'GET','hostname':'github.com',
                'repository':'AlecKriebel/Math','route':route,'exit':r.returncode,'intent':intent,'stdout':out,'stderr':err,'no_retry':True})
            self.records.append({'route':route,'response':out,'receipt':receipt,'stderr':err,'intent':intent})
            need(r.returncode==0,'Actual native GET failed; no retry')
            result=self.g.decode(r.stdout);need(type(result) in (dict,list),'Strict JSON object/list')
            if route.startswith('git/'):
                need(result.get('sha')==route.rsplit('/',1)[1],'Routed immutable identity differs')
                self.cache[route]=r.stdout
            return result
        except BaseException:self.failed=True;raise

def authenticate_commit(g,value,oid):
    """Exact native SHA1 finds supported unsigned canonical raw representation.

    UTC API metadata does not retain original header timezone. Enumerate only
    UTC and local Pacific offsets; acceptance requires an exact native SHA1,
    so enumeration is a representation search, never an assumption of identity.
    Unsupported headers/timezones fail closed and retain raw GET evidence.
    """
    need(value.get('sha')==oid and g.hexid(value['tree']['sha']) and type(value['parents']) is list,'Commit metadata identity')
    parents=[r['sha'] for r in value['parents']];need(all(g.hexid(x) for x in parents) and len(parents)<=16,'Ordered native commit parents')
    def identity(row,offset):
        need(type(row) is dict and type(row.get('name')) is str and type(row.get('email')) is str
             and all('\n' not in row[k] and '\r' not in row[k] and '\0' not in row[k] for k in ('name','email')),'Canonical author metadata')
        dt=datetime.datetime.fromisoformat(row['date'].replace('Z','+00:00'))
        need(dt.tzinfo is not None and dt.microsecond==0,'Exact commit seconds')
        return f"{row['name']} <{row['email']}> {int(dt.timestamp())} {offset}"
    text=value['message'];need(type(text) is str and '\0' not in text,'Commit message metadata')
    matches=[]
    for author_offset in ('+0000','-0700','-0800'):
        for committer_offset in ('+0000','-0700','-0800'):
            prefix='tree '+value['tree']['sha']+'\n'+''.join('parent '+p+'\n' for p in parents)
            prefix+='author '+identity(value['author'],author_offset)+'\ncommitter '+identity(value['committer'],committer_offset)+'\n\n'
            for omitted in range(3):
                raw=(prefix+text+'\n'*omitted).encode()
                if g.native('commit',raw)==oid:matches.append((raw,author_offset,committer_offset,omitted))
    need(len(matches)==1,'Unsupported native raw commit representation; Root scope decision needed')
    raw,ao,co,lf=matches[0]
    return raw,{'sha':oid,'tree':value['tree']['sha'],'parents':parents,'native_SHA1_verified':True,
        'author_header_offset':ao,'committer_header_offset':co,'terminal_LFs_added_to_API_representation':lf,'raw_pin':pin(raw)}

def inventory(c,trees,root,path):
    item=trees.lookup(root,path)
    if item is None:return {'root':root,'path':path,'absent':True,'leaves':[],'directories':[]}
    need(item[:2]==('040000','tree'),'Owned root must be native tree')
    leaves=[];dirs=[]
    def walk(oid,p,depth):
        rows=trees.get(oid,depth);dirs.append({'path':p,'sha':oid})
        for name,row in sorted(rows.items()):
            target=p+'/'+name
            if row[:2]==('040000','tree'):walk(row[2],target,depth+1)
            else:
                need(len(leaves)<ROLE_FILES,'Role file bound exceeded; metadata/raw retained for Root decision')
                leaves.append({'path':target,'mode':row[0],'type':row[1],'sha':row[2]})
    walk(item[2],path,len(path.split('/')))
    return {'root':root,'path':path,'absent':False,'native_tree':item[2],'directories':dirs,'leaves':leaves}

class Bodies:
    def __init__(self,g,api):self.g=g;self.api=api;self.cache={};self.total=0
    def get(self,oid):
        if oid in self.cache:return self.cache[oid]
        j=self.api('GET','git/blobs/'+oid)
        need(j.get('sha')==oid and j.get('encoding')=='base64' and type(j.get('size')) is int
             and 0<=j['size']<=ROLE_BYTES and type(j.get('content')) is str,'Strict bounded native blob')
        b=base64.b64decode(''.join(j['content'].split()),validate=True)
        need(len(b)==j['size'] and self.g.native('blob',b)==oid,'Native blob SHA1/size')
        self.cache[oid]=b;return b
    def role(self,inv,label):
        rows=[];total=0
        for row in inv['leaves']:
            need(row['type']=='blob' and row['mode'] in ('100644','100755','120000'),'Unsupported owned gitlink; Root decision required')
            b=self.get(row['sha']);total+=len(b);self.total+=len(b)
            need(total<=ROLE_BYTES and self.total<=ALL_BYTES,'Role/aggregate decoded body cap exceeded; Root scope decision required')
            copy=put('_private_native/'+label+'/'+row['path'],b)
            rows.append({**row,**pin(b),'private_copy':copy['path']})
        return {**inv,'role':label,'files':rows,'file_count':len(rows),'decoded_bytes':total,'all_native_blobs_authenticated':True}

def pr_guard(pr,intake):
    before=intake['actual_PR']
    need(type(pr.get('number')) is int and pr['number']==212 and pr.get('state')=='open' and pr.get('draft') is True
         and pr.get('merged') is False and pr['head']['sha']==CURRENT and pr['head']['ref']=='math/30005310-colored-threshold-wip'
         and pr.get('title')=='30005310: Credited prior counterexamples to literal numerical scenarios'
         and type(pr.get('commits')) is int and pr['commits']==3 and pr['base']['ref']=='main','Current exact accepted open-draft PR identity')
    for key in ('number','title','state','draft','merged','commits','merge_commit_sha','merged_at','created_at','updated_at'):
        need(g_exact(pr.get(key),before.get(key)),'PR changed since Root status intake: '+key)

def g_exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(g_exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(g_exact(x,y) for x,y in zip(a,b))
    return a==b

def queue(g,trees,bodies,root,label,intake):
    e=trees.lookup(root,QUEUE);need(e is not None and e[:2]==('100644','blob'),'Whole native QUEUE')
    raw=bodies.get(e[2]);put('_private_native/'+label+'/'+QUEUE,raw);bodies.total+=len(raw)
    need(bodies.total<=ALL_BYTES,'Queue aggregate cap')
    found=[]
    for row in raw.splitlines(keepends=True):
        cells=row.decode().split('|')
        if len(cells)==14 and cells[2].strip().split(' / ')[0]=='30005310':found.append((row,cells))
    need(len(found)==1,'Unique exact own QUEUE row')
    row,cells=found[0]
    if label=='original':
        wanted=intake['preserved_QUEUE_blob']
        need(e[2]==wanted['git_blob'] and pin(raw)=={k:wanted[k] for k in ('bytes','sha256')}
             and pin(row)==intake['preserved_QUEUE_row_pin'] and cells[8].strip()=='claimed_solved'
             and cells[9].strip()=='1/5','Original submitted status/row must match Root intake')
    record={'mode':e[0],'type':e[1],'sha':e[2],**pin(raw),'row_pin':pin(row),'status':cells[8].strip(),
            'effort':cells[9].strip(),'private_QUEUE':'_private_native/'+label+'/'+QUEUE}
    return record

def linked_sources(g,trees,bodies,original):
    candidates=set();unfollowed=[]
    for row in original['files']:
        if Path(row['path']).suffix.lower() not in ('.md','.txt','.tex'):continue
        raw=read(BASE/row['private_copy'])
        targets=re.findall(rb'\]\(([^)\s]+)(?:\s+[^)]*)?\)',raw)
        for token in targets:
            text=token.decode('utf-8',errors='strict');parts=urlsplit(text)
            if parts.scheme or parts.netloc:continue
            path=posixpath.normpath(posixpath.join(posixpath.dirname(row['path']),unquote(parts.path)))
            if path==OWN or path.startswith(OWN+'/') or not parts.path:continue
            if (path.startswith('unsolved_math_prioritization/') and '/attempts/' not in path
                and re.search(r'(?:question|source|candidate|problem|30005310)',posixpath.basename(path),re.I)
                and Path(path).suffix.lower() in ('.json','.jsonl','.md','.txt','.tex','.csv','.yaml','.yml')):
                rel(path);candidates.add(path)
            else:unfollowed.append({'from':row['path'],'relative_target':text,'resolved':path,'reason':'Outside finite linked original question/candidate policy'})
    need(len(candidates)<=30,'Linked original source count bound')
    leaves=[];missing=[]
    for path in sorted(candidates):
        item=trees.lookup(ROOTS[ORIGINAL],path)
        if item is None:missing.append(path);continue
        need(item[0:2] in (('100644','blob'),('100755','blob')),'Linked original source must be regular native blob')
        leaves.append({'path':path,'mode':item[0],'type':item[1],'sha':item[2]})
    inv={'root':ROOTS[ORIGINAL],'path':'EXPLICIT_LINKED_ORIGINAL_QUESTION_CANDIDATE_FILES','leaves':leaves,
         'directories':[],'absent':not leaves}
    result=bodies.role(inv,'original_linked_sources')
    return {'bodies':result,'unresolved_linked_paths':missing,'unfollowed_relative_links':unfollowed,
            'external_links_not_fetched':True,'link_token_parsing_only_no_math_interpretation':True}

def source_guard():
    manifest=json.loads(read(BASE/'SOURCE_MANIFEST.json'))
    for row in manifest['files']:need(pin(read(BASE/rel(row['path'])))=={k:row[k] for k in ('bytes','sha256')},'Own collector source closure changed')
    return pin(read(BASE/'SOURCE_MANIFEST.json'))

def collect():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Use -E -S -B -P')
    g,c=helpers();source_pin=source_guard();program=BASE.parents[2]
    accepted_raw=read(BASE.parent/'ROOT_STATUS_INTAKE_ACCEPTANCE_01.json')
    intake_raw=read(program/'ordered_intakes_after_PR211_20261017/PR212_PRESERVED_STATUS_INTAKE.json')
    need(pin(accepted_raw)==ACCEPT and pin(intake_raw)==INTAKE,'Root accepted status input pins')
    accepted=g.decode(accepted_raw);intake=g.decode(intake_raw)
    need(accepted.get('accepted') is True and accepted.get('PR')==212 and intake.get('eligible') is True,'Actual Root status authority')
    save('INPUT_PINS.json',{'UTC':now(),'Root_status_acceptance':ACCEPT,'actual_intake':INTAKE,'source_manifest_pin':source_pin})
    api=API(g);trees=c.NativeTrees(api);bodies=Bodies(g,api)
    phase(15,'Source/pins checked. Actual GET-only capture starts; mathematics remains unreviewed.')
    start=api('GET','pulls/212');pr_guard(start,intake)
    commits={};raw_commits={}
    for label,oid,parents in (('original',ORIGINAL,[PARENT]),('current',CURRENT,[ORIGINAL])):
        value=api('GET','git/commits/'+oid);raw,metadata=authenticate_commit(g,value,oid)
        need(metadata['tree']==ROOTS[oid] and metadata['parents']==parents,'Exact original/current root and ordered parent')
        metadata['raw_commit']=put('_private_native_commits/'+oid+'.raw',raw)
        commits[label]=metadata;raw_commits[oid]=value
    history=api('GET','pulls/212/commits?per_page=100&page=1')
    need(type(history) is list and len(history)==3 and [r['sha'] for r in history]==[PARENT,ORIGINAL,CURRENT],'Exact complete native PR commit history')
    parent=api('GET','git/commits/'+PARENT);raw,metadata=authenticate_commit(g,parent,PARENT)
    metadata['raw_commit']=put('_private_native_commits/'+PARENT+'.raw',raw);commits['original_parent']=metadata
    # Full foreign scope is metadata-only. Equal native trees remain opaque.
    changed,added,deleted=trees.changes(ROOTS[ORIGINAL],ROOTS[CURRENT])
    diff=[{'path':path,'before':trees.lookup(ROOTS[ORIGINAL],path),'after':trees.lookup(ROOTS[CURRENT],path),
           'classification':'own_attempt' if path.startswith(OWN+'/') else 'old_owned_audit' if path.startswith(OLD+'/') else 'QUEUE' if path==QUEUE else 'foreign_metadata_only'} for path in sorted(changed)]
    save('FULL_NATIVE_CHANGE_SCOPE.json',{'before':ORIGINAL,'after':CURRENT,'before_root':ROOTS[ORIGINAL],'after_root':ROOTS[CURRENT],
        'changed_leaves':diff,'added_directories':sorted(added),'deleted_directories':sorted(deleted),
        'foreign_blob_bodies_downloaded_for_diff':False})
    roles={}
    for label,oid in (('original',ORIGINAL),('current',CURRENT)):
        inv=inventory(c,trees,ROOTS[oid],OWN);need(not inv['absent'],'Required own attempt tree absent')
        roles[label]=bodies.role(inv,label)
        save(label.upper()+'_BODY_CUSTODY.json',roles[label])
        old=inventory(c,trees,ROOTS[oid],OLD)
        roles[label+'_old_owned_audit']=bodies.role(old,label+'_old_owned_audit')
        save(label.upper()+'_OLD_OWNED_AUDIT_CUSTODY.json',roles[label+'_old_owned_audit'])
        phase(45 if label=='original' else 65,label+' exact native attempt/old-owned roles captured.')
    queues={label:queue(g,trees,bodies,ROOTS[oid],label,intake) for label,oid in (('original',ORIGINAL),('current',CURRENT))}
    save('QUEUE_CUSTODY_COMPARISON.json',{'original':queues['original'],'current':queues['current'],
        'whole_QUEUE_identical':queues['original']['sha']==queues['current']['sha'],
        'own_row_identical':queues['original']['row_pin']==queues['current']['row_pin'],
        'status_eligibility_remains_original_only':True})
    linked=linked_sources(g,trees,bodies,roles['original']);save('ORIGINAL_LINKED_SOURCE_CUSTODY.json',linked)
    original_by_relative={r['path'][len(OWN)+1:]:r for r in roles['original']['files']}
    history_matches=[]
    for r in roles['current']['files']:
        relative=r['path'][len(OWN)+1:]
        if '/original' not in '/'+relative and not relative.startswith('history/'):continue
        for oldpath,old in original_by_relative.items():
            if relative.endswith('/'+oldpath) and r['sha']==old['sha'] and r['mode']==old['mode']:
                history_matches.append({'original_path':old['path'],'current_history_path':r['path'],'sha':r['sha'],**{k:r[k] for k in ('bytes','sha256')}})
    covered={r['original_path'] for r in history_matches}
    history_report={'matched_original_files':len(covered),'original_total':len(original_by_relative),
        'all_original_files_have_exact_current_history_copies':len(covered)==len(original_by_relative),
        'matches':history_matches,'unmatched_original_paths':sorted(set(r['path'] for r in roles['original']['files'])-covered)}
    save('ORIGINAL_HISTORY_COPY_ASSOCIATIONS.json',history_report)
    final=api('GET','pulls/212');pr_guard(final,intake)
    keys=('number','title','state','draft','merged','commits','merge_commit_sha','merged_at','created_at','updated_at','body')
    need(all(g.exact(start.get(k),final.get(k)) for k in keys),'PR changed across full actual custody; stale failstop')
    source_guard()
    save('AUTHENTICATED_NATIVE_TREES.json',{oid:{name:list(row) for name,row in value.items()} for oid,value in trees.cache.items()})
    save('ACTUAL_TRANSPORT_INDEX.json',{'GET_attempts':api.count,'records':api.records,'hostname':'github.com','repository':'AlecKriebel/Math','raw_bytes':api.raw_bytes,'automatic_retries':0})
    factual={'schema':'pr212-native-original-current-custody-v1','UTC':now(),'evidence_scope':'ACTUAL_GET_CUSTODY_ONLY_NOT_ROOT_MATHEMATICAL_OR_WORKFLOW_ACCEPTANCE',
        'PR':212,'problem_id':'30005310','original':commits['original'],'current':commits['current'],'original_parent':commits['original_parent'],
        'roles':{k:{'files':v['file_count'],'bytes':v['decoded_bytes'],'absent':v['absent'],
                         'native_tree':v.get('native_tree')} for k,v in roles.items()},
        'linked_original_files':linked['bodies']['file_count'],'linked_original_bytes':linked['bodies']['decoded_bytes'],
        'unresolved_linked_source_paths':linked['unresolved_linked_paths'],'history':history_report,
        'QUEUE':queues,'changed_leaf_count':len(diff),'foreign_changed_leaf_count':sum(r['classification']=='foreign_metadata_only' for r in diff),
        'GET_attempts':api.count,'decoded_role_bytes_including_duplicates_and_QUEUE':bodies.total,'source_manifest_pin':source_pin,
        'fresh_end_PR_HEAD':CURRENT,'fresh_start_end_PR_metadata_identical':True,
        'mathematics_priority_or_source_question_acceptance':False,'submitted_or_review_script_executions':0,
        'Git_PR_provider_ref_currentfive_or_original_lock_mutations':False,'author_turns_or_opening_transaction_inferred':False}
    save('FACTUAL_CUSTODY_SUMMARY.json',factual)
    phase(90,'Actual capture complete; local raw-envelope/native/body re-verification remains.')
    print(json.dumps({'GET_attempts':api.count,'roles':factual['roles'],'changed_leaves':len(diff),'decoded_bytes':bodies.total,'linked_original_files':linked['bodies']['file_count']},sort_keys=True))

def verify():
    """Local retained raw response and private body proof; no transport execution."""
    g,c=helpers();source_guard();summary=g.decode(read(BASE/'FACTUAL_CUSTODY_SUMMARY.json'))
    index=g.decode(read(BASE/'ACTUAL_TRANSPORT_INDEX.json'));responses={}
    for row in index['records']:
        for key in ('response','receipt','stderr','intent'):
            r=row[key];need(pin(read(BASE/rel(r['path'])))=={k:r[k] for k in ('bytes','sha256')},'Raw transport linked pin differs')
        response_raw=read(BASE/row['response']['path']);value=g.decode(response_raw)
        receipt=g.decode(read(BASE/row['receipt']['path']));intent=g.decode(read(BASE/row['intent']['path']))
        need(receipt['method']=='GET' and receipt['hostname']=='github.com' and receipt['repository']=='AlecKriebel/Math'
             and receipt['exit']==0 and type(receipt['exit']) is int and receipt['no_retry'] is True
             and receipt['route']==row['route'] and receipt['stdout']==row['response'] and receipt['stderr']==row['stderr']
             and receipt['intent']==row['intent'],'Exact successful GET receipt')
        argv=[GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+row['route']]
        need(route_ok(row['route']) and intent['argv']==argv and intent['method']=='GET' and g.exact(intent['automatic_retries'],0),'Explicit host/route/GET intent')
        if row['route'] not in responses:responses[row['route']]=value
    def replay(method,route,body=None):
        need(method=='GET' and body is None,'Local replay only GET identity');return responses[route]
    trees=c.NativeTrees(replay)
    before=ROOTS[ORIGINAL];after=ROOTS[CURRENT]
    changed,added,deleted=trees.changes(before,after)
    scope=g.decode(read(BASE/'FULL_NATIVE_CHANGE_SCOPE.json'))
    need(sorted(changed)==[r['path'] for r in scope['changed_leaves']] and sorted(added)==scope['added_directories']
         and sorted(deleted)==scope['deleted_directories'],'Whole native diff reproduces from retained raw GETs')
    for row in scope['changed_leaves']:
        for key,root in (('before',before),('after',after)):
            observed=trees.lookup(root,row['path'])
            need(g.exact(row[key],list(observed) if observed is not None else None),'Native diff pre/post tuple differs')
    roles=[g.decode(read(BASE/(label.upper()+'_BODY_CUSTODY.json'))) for label in ('original','current')]
    roles += [g.decode(read(BASE/(label.upper()+'_OLD_OWNED_AUDIT_CUSTODY.json'))) for label in ('original','current')]
    roles += [g.decode(read(BASE/'ORIGINAL_LINKED_SOURCE_CUSTODY.json'))['bodies']]
    body_count=0;total=0
    for role in roles:
        if role['path']!='EXPLICIT_LINKED_ORIGINAL_QUESTION_CANDIDATE_FILES':
            inv=inventory(c,trees,role['root'],role['path'])
            need(g.exact(inv['leaves'],role['leaves']) and inv['absent']==role['absent'],'Exact complete owned tree inventory')
        projected=[{k:r[k] for k in ('path','mode','type','sha')} for r in role['files']]
        need(g.exact(projected,role['leaves']) and type(role['file_count']) is int and len(role['files'])==role['file_count']<=ROLE_FILES
             and sum(r['bytes'] for r in role['files'])==role['decoded_bytes']<=ROLE_BYTES,'Exact complete role body set/bounds')
        for r in role['files']:
            b=read(BASE/rel(r['private_copy']))
            need(pin(b)=={k:r[k] for k in ('bytes','sha256')} and g.native('blob',b)==r['sha'],'Private body exact native SHA1/SHA256')
            need(trees.lookup(role['root'],r['path'])==(r['mode'],r['type'],r['sha']),'Fresh native tree-path/body association')
            j=responses['git/blobs/'+r['sha']]
            raw=base64.b64decode(''.join(j['content'].split()),validate=True)
            need(j['sha']==r['sha'] and j['encoding']=='base64' and type(j['size']) is int and j['size']==len(raw)
                 and raw==b,'Full actual raw native body envelope matches saved private copy')
            total+=len(b);body_count+=1
    for oid in (PARENT,ORIGINAL,CURRENT):
        raw,metadata=authenticate_commit(g,responses['git/commits/'+oid],oid)
        need(raw==read(BASE/'_private_native_commits'/ (oid+'.raw')),'Raw native commit SHA1 reproducible')
    queues=g.decode(read(BASE/'QUEUE_CUSTODY_COMPARISON.json'))
    for label,oid in (('original',ORIGINAL),('current',CURRENT)):
        row=queues[label];b=read(BASE/row['private_QUEUE']);total+=len(b)
        need(trees.lookup(ROOTS[oid],QUEUE)==(row['mode'],row['type'],row['sha'])
             and pin(b)=={k:row[k] for k in ('bytes','sha256')} and g.native('blob',b)==row['sha'],'Whole QUEUE exact native body')
        j=responses['git/blobs/'+row['sha']]
        decoded=base64.b64decode(''.join(j['content'].split()),validate=True)
        need(j['sha']==row['sha'] and j['encoding']=='base64' and type(j['size']) is int and j['size']==len(decoded)
             and decoded==b,'Full actual QUEUE raw body envelope')
    need(total<=ALL_BYTES and total==summary['decoded_role_bytes_including_duplicates_and_QUEUE'],'Aggregate body bounds')
    intake=g.decode(read(BASE.parents[2]/'ordered_intakes_after_PR211_20261017/PR212_PRESERVED_STATUS_INTAKE.json'))
    need(pin(read(BASE.parents[2]/'ordered_intakes_after_PR211_20261017/PR212_PRESERVED_STATUS_INTAKE.json'))==INTAKE,'Pinned actual intake unchanged')
    observed_PRs=[g.decode(read(BASE/r['response']['path'])) for r in index['records'] if r['route']=='pulls/212']
    keys=('number','title','state','draft','merged','commits','merge_commit_sha','merged_at','created_at','updated_at','body')
    need(len(observed_PRs)==2 and all(g.exact(observed_PRs[0].get(k),observed_PRs[1].get(k)) for k in keys),
         'Retained actual fresh PR identity/body observations identical')
    for value in observed_PRs:pr_guard(value,intake)
    need(len(index['records'])==index['GET_attempts']<=MAX_GETS
         and summary['fresh_start_end_PR_metadata_identical'] is True and summary['fresh_end_PR_HEAD']==CURRENT,'Complete actual capture and end identity')
    return {'schema':'pr212-local-native-custody-reverification-v1','UTC':now(),'status':'PASS','network_calls':0,
        'actual_raw_GET_records':len(index['records']),'private_owned_body_copies':body_count,'decoded_bytes_including_QUEUE':total,
        'all_native_commits_trees_blobs_and_body_SHA256_reverified':True,'full_changed_scope_reproduced':True,
        'mathematical_or_Root_workflow_acceptance':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('collect','verify'))
    args=parser.parse_args()
    if args.action=='collect':collect()
    else:print(json.dumps(verify(),sort_keys=True,indent=2))
