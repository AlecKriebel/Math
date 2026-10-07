"""Checkpoint048: GET-only preparation, tree/commit/expected-old main CAS.

Preparation cannot grant authority or write Git/maps. Future execution requires
fresh exact ROOT acceptance/peer window/one-use grant. The primary checkout's
branch, HEAD, index and held-map bodies are preserved. Only the exact selected
remote main tree overlay may be published after fresh ROOT review and grant.
No PR, queue, author branch, release, Zenodo or tracker operation exists here.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse, base64, hashlib, importlib.util, json, os, re, stat, sys, time
B=Path(__file__).resolve().parent; R=B.parents[1]
P='draft_pr_descending_audit_20261002'; V=P+'/audits/pr278_30005468'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'; GIT='/usr/bin/git'
ENDPOINT='https://github.com/AlecKriebel/Math.git'; PREFIX='repos/AlecKriebel/Math/'
RID,RN,UID=1307717439,'R_kgDOTfIvPw',6109370
PYTHON_ENGINE='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'
EXPECTED_REMOTE=None  # Supplied by a new literal read-only prepare invocation; no old ref authority.
PRIMARY_HEAD='6144d964777214c6963a915288c18fcf97b42026'
LAST='b351c22a4a8fe70a45c670183b8bb1c17aabd1bf'
MAPS=[P+'/CURRENT_SCOPE.json',P+'/inventory.json',P+'/RESEARCH_LOG.md',V+'/CURRENT_AUDIT_STATUS.json',V+'/RESEARCH_LOG.md',P+'/SHARED_GIT_WINDOW_STATUS.json']
def need(x,m):
    if not x: raise RuntimeError(m+'; preserve genuine state, reconcile read-only, no automatic mutation retry')
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def oid(k,b): return hashlib.sha1(k.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def valid(h): return type(h) is str and re.fullmatch('[0-9a-f]{40}',h) is not None
def pin(p):
    p=Path(p);need(p.is_file() and not p.is_symlink(),'literal regular input')
    need(p.is_absolute() and p.resolve()==p,'no ancestor symlink or relative input');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def same(z):
    need(pin(z['path'])==z,'complete same-byte/mode input');return Path(z['path']).read_bytes()
def save(p,d):
    p=Path(p);need(p.resolve().is_relative_to(B),'own output namespace');p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write((json.dumps(d,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
def sources(): return {n:pin(B/n) for n in ['checkpoint049.py','native_capture.py','README.md','COMMIT_MESSAGE.txt']}
def packet():
    z=pin(B/'FULL_CATALOG.json');need(z['mode']==0o444,'sealed source catalogue');c=json.loads(same(z))
    need(c['schema']=='checkpoint049-full-source-domain-catalogue-v1' and c['execution_authority'] is False,'literal source catalogue')
    for x in c['files']:same(x)
    def included(p):
        first=p.relative_to(B).parts[0]
        return first not in ['FULL_CATALOG.json','FINAL_SEAL.json','ROOT_CHECKPOINT049_GRANT_01.json','ROOT_CHECKPOINT049_SOURCE_PLAN_ACCEPTANCE_01.json'] and not re.fullmatch(r'(read_only_prepare|prepare_capture|ROOT_readback)_[0-9]{2}|ROOT_actual_checkpoint049_01',first)
    observed={str(p) for p in B.rglob('*') if p.is_file() and included(p)}
    need(observed=={x['path'] for x in c['files']},'no omitted or additional source-domain file')
    need({str(B)}|{str(p) for p in B.rglob('*') if p.is_dir() and included(p)}==set(c['directories']),'complete source directory census')
    need(not any(p.is_symlink() for p in B.rglob('*') if included(p)),'no source-domain symlink')
    return z
def primary_files():
    need((R/'.git/HEAD').read_bytes()==b'ref: refs/heads/main\n' and (R/'.git/refs/heads/main').read_text()==PRIMARY_HEAD+'\n','exact primary main/HEAD files')
    z=pin(R/'.git/index');need(z['bytes']==25693551 and z['sha256']=='0f5fe3d0ff7ec985d62110af00a8a8e511737de5b0de93353d39ec5ca743376f','whole fixed primary index')
    return dict(HEAD=pin(R/'.git/HEAD'),main_ref=pin(R/'.git/refs/heads/main'),index=z)
def completed_native_ledger(run,actor):
    rows=[];seen=set()
    for d in sorted(x.parent for x in run.rglob('execution.json') if x.parent.parent.name=='native'):
        need(d.is_dir() and not d.is_symlink(),'literal closed native directory')
        q=json.loads(same(pin(d/'request.json')));s=json.loads(same(pin(d/'started.json')));e=json.loads(same(pin(d/'execution.json')))
        need(q['schema']=='checkpoint049-native-request-v1' and e['schema']=='checkpoint049-native-completed-observation-v1' and s['schema']=='checkpoint049-native-start-v1','exact native schemas')
        need(type(actor) is int and actor>0 and all(type(x['actual_recorder_PID']) is int for x in [q,s,e]) and q['actual_recorder_PID']==s['actual_recorder_PID']==e['actual_recorder_PID']==actor and type(e['actual_child_PID']) is int and type(s['actual_child_PID']) is int and e['actual_child_PID']>0 and e['actual_child_PID']==s['actual_child_PID'] and e['actual_child_PID'] not in seen,'typed actor/child process linkage');seen.add(e['actual_child_PID'])
        need(type(e['returncode']) is int and e['returncode']==0 and e['reaped'] is True and e['communication_complete'] is True and e['wait_completed'] is True and e['failure'] is None and e['cleanup_errors']==[],'successful complete direct wait/reap')
        need(e['argv']==q['argv'] and e['cwd']==q['cwd']==str(B) and e['request']==pin(d/'request.json'),'full literal child request/receipt')
        stamps=[datetime.fromisoformat(x['UTC']) for x in [q,s,e]];need(all(x.utcoffset()==timedelta(0) for x in stamps) and stamps[0]<=stamps[1]<=stamps[2],'real ordered UTC child timestamps')
        need(type(q['timeout_seconds']) in [int,float] and type(e['elapsed_seconds']) in [int,float] and 0<q['timeout_seconds']<=600 and 0<=e['elapsed_seconds']<=q['timeout_seconds']+10,'typed child timeout/cleanup budget')
        argv=q['argv'];is_get=argv[:7]==[GH,'api','--hostname','github.com','--include','-X','GET'] and len(argv)==12 and argv[8:]==['-H','Accept: application/vnd.github+json','-H','X-GitHub-Api-Version: 2022-11-28'];is_git=argv[:4]==[GIT,'--no-optional-locks','-C',str(R)] and argv[4:] in [['branch','--show-current'],['rev-parse','HEAD'],['diff','--cached','--quiet','--exit-code'],['ls-files','--stage','-z'],['ls-files','-v','-z']];need(is_get or is_git,'only exact read-only provider/Git child')
        need(q['stdin_bytes']==0 and q['stdin_sha256'] is None and not (d/'stdin.gz').exists(),'read-only children have no stdin')
        allowed={'request.json','started.json','execution.json','recorder_PRELAUNCH.py','stdout.gz','stderr.gz'};need({x.name for x in d.iterdir()}==allowed,'complete child file census')
        need((d/'recorder_PRELAUNCH.py').read_bytes()==same(q['recorder_source']) and q['recorder_source']==pin(B/'native_capture.py'),'exact recorder prelaunch source')
        for k in ['executable','python_launcher','python_engine']:same(q[k])
        for name,z in e['streams'].items():
            need(name in ['stdout','stderr'] and z['complete'] is True and z['stored']==pin(d/(name+'.gz')) and type(z['logical_bytes']) is int and z['logical_bytes']>=0,'typed complete same-mode immutable stream')
            import gzip
            raw=gzip.decompress(same(z['stored']));need(len(raw)==z['logical_bytes'] and sha(raw)==z['logical_sha256'],'whole gzip logical body')
        need(set(e['streams'])=={'stdout','stderr'},'both full streams')
        if is_get:
            route=argv[7];need(route in ['user',PREFIX.rstrip('/'),PREFIX+'git/ref/heads/main'] or re.fullmatch(re.escape(PREFIX)+r'git/(trees|commits|blobs)/[0-9a-f]{40}',route) or re.fullmatch(re.escape(PREFIX)+r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}\?per_page=1&page=2',route),'literal GET route')
            raw=gzip.decompress(same(e['streams']['stdout']['stored']));sep=b'\r\n\r\n' if b'\r\n\r\n' in raw else b'\n\n';head,body=raw.split(sep,1);tokens=head.splitlines()[0].split();need(tokens[0] in [b'HTTP/1.1',b'HTTP/2.0',b'HTTP/2'] and tokens[1]==b'200','actual original GET200 status')
            response=d.parents[2]/(d.name+'_RESPONSE.json');need(json.loads(body)==json.loads(same(pin(response))),'whole source response matches captured native HTTP body')
        rows.append(dict(directory=str(d),request=pin(d/'request.json'),started=pin(d/'started.json'),execution=pin(d/'execution.json'),recorder_prelaunch=pin(d/'recorder_PRELAUNCH.py'),argv=argv,actual_recorder_PID=actor,actual_child_PID=e['actual_child_PID'],streams=e['streams']))
    need(rows,'actual completed children exist');return dict(schema='checkpoint049-complete-get-only-native-ledger-v1',execution_authority=False,fixture_only=False,actor_PID=actor,records=rows)
def native():
    z=pin(B/'native_capture.py');need(z==json.loads((B/'SOURCE_PINS.json').read_bytes())['native_capture.py'],'external local native source pin')
    spec=importlib.util.spec_from_file_location('checkpoint049_native',B/'native_capture.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def selected():
    z=pin(B/'SELECTOR.json');need(z['mode']==0o444,'sealed selector');s=json.loads(same(z))
    need(s['schema']=='checkpoint049-public-closed-content-selection-v1' and s['execution_authority'] is False and s['writer_window_authority'] is False,'inactive literal selection')
    need(s['counters']==[33,13,12,0] and s['held_uncompleted']==[293,292,280] and s['progress']==dict(case=80,mathematics=100,bounded_priority=100,publication=100,tracker=100,historical_author_integration=100,native_merge=0),'honest current progress')
    files={}
    for x in s['entries']:
        n=x['target'];p=Path(n);need(type(n) is str and n==p.as_posix() and '\0' not in n and '\n' not in n and not p.is_absolute() and all(a not in ('..','.') for a in p.parts) and n.startswith(P+'/') and n not in files,'unique literal selected path')
        need(n in MAPS or n.startswith(P+'/checkpoint049_preparation_01/'),'only six owned maps or owned reader/source')
        q=B/'frozen'/n;need(x['input']['path']==str(q) and x['input']['mode']==0o444,'own frozen literal input')
        b=same(x['input']);need(len(b)<600000 and b.decode().encode()==b,'bounded whole UTF8')
        files[n]=dict(input=x['input'],blob=oid('blob',b),kind=x['kind'])
    need(len(files)==s['selected_file_count'] and sum(x['input']['bytes'] for x in files.values())==s['selected_bytes'],'complete closed selection')
    scope=json.loads(same(files[MAPS[0]]['input']));inv=json.loads(same(files[MAPS[1]]['input']));audit=json.loads(same(files[MAPS[3]]['input']))
    need(scope['current_original_head']=='deb9d7491a0bf887f7615717a5b484caf212cfd6' and scope['current_original_status']=='claimed_solved' and scope['current_original_author_budget']=='1/5' and scope['current_additional_author_search_turns']==0,'exact original eligibility/budget')
    need([scope[k] for k in ['completed_count','published_count','native_merged_count','tracker_pending_count']]==[33,13,12,0] and scope['current_workflow_percent']==80 and scope['current_author_integration_percent']==100 and scope['current_native_merge_percent']==0,'accepted historical author, failed native plan')
    need(scope['current_publication_complete'] is True and scope['current_DOI']=='10.5281/zenodo.23196750' and scope['current_tracker_range']=="'Math Puzzles'!A34:D34" and scope['current_native_merge_pending'] is True,'actual publication/tracker and incomplete native case')
    item=next(x for x in inv['items'] if x['number']==278)
    need(item['paper'] is True and item['tracker'] is True and item['DOI']==scope['current_DOI'] and all(item[k] is False for k in ['merged','closed','case_completed']) and item['workflow_percent']==audit['workflow_percent']==80 and item['author_integration_percent']==audit['author_integration_percent']==100,'same explicit incomplete case')
    need(inv['completed_by_descending']==33 and len(inv['claimed_solved_published_by_descending'])==13 and len(inv['claimed_solved_merged_by_descending'])==12 and inv['claimed_solved_tracker_pending_by_descending']==[],'same physical inventory counters')
    return z,files
def tree_raw(rows):
    out=b''
    for x in sorted(rows,key=lambda x:x['path'].encode()+(b'/' if x['type']=='tree' else b'')):
        need(x['mode'] in ['040000','100644','100755','120000','160000'] and valid(x['sha']),'canonical tree modes/hash')
        out+=(('40000' if x['mode']=='040000' else x['mode'])+' '+x['path']).encode()+b'\0'+bytes.fromhex(x['sha'])
    return out
def checked_tree(x,h):
    need(x['sha']==h and x.get('truncated') is False and type(x['tree']) is list,'complete nonrecursive tree')
    rows={}
    for z in x['tree']:
        n=z['path'];need(type(n) is str and n and '/' not in n and n not in ('.','..') and '\0' not in n and n not in rows,'unique literal tree leaf')
        need(z['mode'] in ['040000','100644','100755','120000','160000'] and z['type']==({'040000':'tree','100644':'blob','100755':'blob','120000':'blob','160000':'commit'}[z['mode']]),'canonical tree mode/type correspondence')
        rows[n]={k:z[k] for k in ['mode','type','sha']}
    need(oid('tree',tree_raw([dict(path=n,**z) for n,z in rows.items()]))==h,'full canonical original tree hash')
    return rows
def derive(api,files,root):
    trie={}
    for n,x in sorted(files.items()):
        node=trie
        for a in n.split('/')[:-1]:node=node.setdefault(a,{})
        node[n.split('/')[-1]]=x['blob']
    before={};after=[];preserved=[]
    def walk(node,h,d):
        rows=checked_tree(api.get(PREFIX+'git/trees/'+h),h) if h else {};before[d]=dict(sha=h,entries=rows);out=dict(rows)
        for n,z in sorted(node.items()):
            if type(z) is str:out[n]=dict(mode='100644',type='blob',sha=z)
            else:
                old=rows.get(n);need(old is None or old['type']=='tree','selected ancestor never replaces a non-tree')
                new=walk(z,old['sha'] if old else None,d+'/'+n if d else n);out[n]=dict(mode='040000',type='tree',sha=new)
        for n in sorted(set(rows)-set(node)):preserved.append(dict(directory=d,path=n,entry=rows[n]))
        body=[dict(path=n,**z) for n,z in sorted(out.items())];new=oid('tree',tree_raw(body));after.append(dict(directory=d,sha=new,entries=out));return new
    new=walk(trie,root,'');need(len(after)<=40,'bounded touched ancestors')
    return dict(before_trees=before,after_trees=after,after_tree=new,unselected_siblings=preserved)
def commit_raw(c):
    b=('tree '+c['tree']+'\nparent '+c['parent']+'\n').encode()
    for k in ['author','committer']:b+=(k+' Alec Kriebel <me@aleckriebel.com> '+str(c['timestamp'])+' +0000\n').encode()
    return b+b'\n'+c['message'].encode()
class API:
    def __init__(self,run,write=False):
        self.run=run;self.n=0;self.N=native();self.write=write;self.posts=[];self.src=sources();self.packet=packet();self.sp,self.files=selected();self.rp=runtime();self.held=read_held();self.primary_files=primary_files();self.externals=json.loads((B/'inputs/ACTUAL_SOURCE_PINS.json').read_bytes())['files'];self.deadline=time.monotonic()+500
        for z in self.externals.values():same(z)
        save(run/'API_PRELAUNCH.json',dict(UTC=utc(),actual_PID=os.getpid(),sources=self.src,selector=self.sp,runtimes=self.rp,write=write,automatic_retry=False))
    def guards(self):
        need(sources()==self.src and packet()==self.packet and selected()==(self.sp,self.files) and runtime()==self.rp and read_held()==self.held and primary_files()==self.primary_files,'same full source/selector/runtime/eight-map/primary files before and after every child')
        for z in self.externals.values():same(z)
    def request(self,method,path,payload=None):
        allowed=path in ['user',PREFIX.rstrip('/'),PREFIX+'git/ref/heads/main'] or re.fullmatch(re.escape(PREFIX)+r'git/(trees|commits|blobs)/[0-9a-f]{40}',path) or re.fullmatch(re.escape(PREFIX)+r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}\?per_page=1&page=2',path)
        need(method=='GET' and payload is None and allowed or method=='POST' and self.write and path in [PREFIX+'git/trees',PREFIX+'git/commits','graphql'],'narrow literal provider methods/routes')
        self.guards();self.n+=1;need(self.n<=250 and self.deadline-time.monotonic()>15,'bounded provider request count/stage')
        if method=='POST':
            need(len(self.posts)<3 and path==[PREFIX+'git/trees',PREFIX+'git/commits','graphql'][len(self.posts)],'exact three POST sequence without retry');self.posts.append(path)
        label=f'{method}_{self.n:04d}';argv=[GH,'api','--hostname','github.com','--include','-X',method,path,'-H','Accept: application/vnd.github+json','-H','X-GitHub-Api-Version: 2022-11-28']
        body=(json.dumps(payload,separators=(',',':'),sort_keys=True)+'\n').encode() if payload is not None else None
        if body is not None:argv+=['--input','-']
        save(self.run/(label+'_INTENT.json'),dict(UTC=utc(),method=method,route=path,request_bytes=len(body or b''),request_sha256=sha(body) if body is not None else None,automatic_retry=False))
        raw=self.N.call(self.run,label,argv,B,stdin=body,timeout=min(40,self.deadline-time.monotonic()-8))
        sep=b'\r\n\r\n' if b'\r\n\r\n' in raw else b'\n\n';head,body=raw.split(sep,1)
        status=head.splitlines()[0].split();code=b'200' if method=='GET' or path=='graphql' else b'201'
        need(len(status)>=2 and status[0] in [b'HTTP/1.1',b'HTTP/2.0',b'HTTP/2'] and status[1]==code and not body.startswith(b'HTTP/'),'one exact original HTTP status')
        x=json.loads(body);need(type(x) is dict and not x.get('errors'),'whole actual JSON provider response')
        self.guards();save(self.run/(label+'_RESPONSE.json'),x);return x
    def get(self,path):return self.request('GET',path)
    def post(self,path,payload):return self.request('POST',path,payload)

def identity(api,expected=None):
    u=api.get('user');r=api.get(PREFIX.rstrip('/'));f=api.get(PREFIX+'git/ref/heads/main')
    need(u['login']=='AlecKriebel' and type(u['id']) is int and u['id']==UID and r['full_name']=='AlecKriebel/Math' and type(r['id']) is int and r['id']==RID and r['node_id']==RN and r['owner']['id']==UID and r['permissions']['push'] is True,'fresh account/repository identity')
    need(f['ref']=='refs/heads/main' and f['object']['type']=='commit' and valid(f['object']['sha']),'actual main ref')
    h=f['object']['sha'];need(expected is None or expected==h,'fresh exact before main');return h
def read_held():
    d=json.loads((B/'inputs/HELD_MAP_PINS.json').read_bytes())['files']
    for z in d.values():same(z)
    return d
def primary(run,materialized=False):
    N=native(); count=0
    def git(*a):
        nonlocal count;count+=1;return N.call(run,'PRIMARY_'+str(count),[GIT,'--no-optional-locks','-C',str(R),*a],B)
    need(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==PRIMARY_HEAD,'unchanged primary main/HEAD')
    index=R/'.git/index';need(index.is_file(),'ordinary primary index path');z=pin(index);need(z['bytes']==25693551 and z['sha256']=='0f5fe3d0ff7ec985d62110af00a8a8e511737de5b0de93353d39ec5ca743376f','fixed entire primary index');need(git('diff','--cached','--quiet','--exit-code')==b'','primary cached diff empty')
    tracked=git('ls-files','--stage','-z');flags=git('ls-files','-v','-z')
    rows={}
    if materialized:
        for row in tracked.split(b'\0'):
            if not row:continue
            meta,n=row.split(b'\t',1);n=n.decode();need(meta.split()[2]==b'0','no conflicted primary index')
            if n in MAPS:continue
            p=R/n
            if p.is_symlink():rows[n]=dict(kind='symlink',target=os.readlink(p),mode=stat.S_IMODE(p.lstat().st_mode))
            elif p.is_file():rows[n]=dict(kind='file',**pin(p))
            elif p.exists():rows[n]=dict(kind='other',mode=stat.S_IMODE(p.lstat().st_mode))
            else:rows[n]=dict(kind='absent')
    return dict(branch='main',HEAD=PRIMARY_HEAD,HEAD_file=pin(R/'.git/HEAD'),main_ref_file=pin(R/'.git/refs/heads/main'),cached_diff_empty=True,index=z,tracked_stage_bytes=len(tracked),tracked_stage_sha256=sha(tracked),index_flags_sha256=sha(flags),materialized_nonselected=rows)
def runtime():return {n:pin(Path(p).resolve()) for n,p in [('git',GIT),('gh',GH),('python_launcher',sys.executable),('python_engine',PYTHON_ENGINE)]}
def prepare(run,expected):
    need(valid(expected),'new literal full expected MAIN required')
    need(run.parent==B and re.fullmatch('read_only_prepare_[0-9]{2}',run.name),'own exclusive read-only namespace');run.mkdir(exist_ok=False)
    s,files=selected();held=read_held();src=sources();rp=runtime();gate_pins=json.loads((B/'inputs/ACTUAL_SOURCE_PINS.json').read_bytes())['files'];[same(z) for z in gate_pins.values()];first=primary(run)
    api=API(run);h=identity(api,expected);c=api.get(PREFIX+'git/commits/'+h);need(c['sha']==h and valid(c['tree']['sha']),'actual remote commit tree')
    anc=api.get(PREFIX+'compare/'+LAST+'...'+h+'?per_page=1&page=2');need(anc['merge_base_commit']['sha']==LAST and anc['behind_by']==0 and anc['status'] in ['ahead','identical'],'remote descends from actual checkpoint047')
    overlay=derive(api,files,c['tree']['sha'])
    # Every selected existing path must be absent or equal to an authenticated
    # checkpoint047/046 value or this exact candidate. Never roll back a peer edit.
    old={}
    historical=json.loads((R/P/'checkpoint048_preparation_01/SELECTOR.json').read_bytes())
    for x in historical['entries']:
        b=same(x['input']);old.setdefault(x['target'],set()).add(oid('blob',b))
    safe=[]
    for n,z in files.items():
        d,leaf=n.rsplit('/',1);v=overlay['before_trees'][d]['entries'].get(leaf)
        allowed=old.get(n,set())|{z['blob']}
        need(v is None or v==dict(mode='100644',type='blob',sha=z['blob']) or v['type']=='blob' and v['mode']=='100644' and v['sha'] in allowed,'selected remote existing path differs from historical/candidate: '+n)
        safe.append(dict(path=n,before_entry=v,authenticated_allowed_blobs=sorted(allowed)))
    timestamp=int(datetime.now(timezone.utc).timestamp());cp=dict(tree=overlay['after_tree'],parent=h,timestamp=timestamp,message=(B/'COMMIT_MESSAGE.txt').read_text())
    raw=commit_raw(cp);identity(api,h);need(read_held()==held and sources()==src and runtime()==rp,'stable preparation actual full inputs')
    # A separate namespace gives distinct actual primary receipts, without
    # claiming the currently running preparation has a completed outer receipt.
    tail=run/'primary_tail';tail.mkdir();need(primary(tail)==first,'whole primary/index unchanged')
    ledger=completed_native_ledger(run,os.getpid());save(run/'NATIVE_LEDGER.json',ledger)
    plan=dict(schema='checkpoint049-get-only-provider-plan-v1',UTC=utc(),execution_authority=False,writer_window_authority=False,fixture_only=False,actual_plan_actor_PID=os.getpid(),complete_get_only_native_ledger=pin(run/'NATIVE_LEDGER.json'),source_domain=packet(),provider_mutations=0,local_Git_mutations=0,
      sources=src,runtimes=rp,selector=s,files=files,actual_gate_pins=gate_pins,actual_gate_pin_file=pin(B/'inputs/ACTUAL_SOURCE_PINS.json'),held_map_before=held,primary_before=first,before_main=h,before_tree=c['tree']['sha'],overlay=overlay,no_rollback=safe,
      commit_payload=cp,canonical_commit_raw_base64=base64.b64encode(raw).decode(),anticipated_after_commit=oid('commit',raw),anticipated_after_tree=cp['tree'],
      future_run=str(B/'ROOT_actual_checkpoint049_01'),provider_tree_payload=dict(base_tree=c['tree']['sha'],tree=[dict(path=n,mode='100644',type='blob',content=same(z['input']).decode()) for n,z in sorted(files.items())]),
      provider_commit_payload=dict(message=cp['message'],tree=cp['tree'],parents=[h],author=dict(name='Alec Kriebel',email='me@aleckriebel.com',date=datetime.fromtimestamp(timestamp,timezone.utc).isoformat().replace('+00:00','Z')),committer=dict(name='Alec Kriebel',email='me@aleckriebel.com',date=datetime.fromtimestamp(timestamp,timezone.utc).isoformat().replace('+00:00','Z'))),
      mutation_sequence=[PREFIX+'git/trees',PREFIX+'git/commits','graphql'],mutation_count=3,main_ref_update_count=1,
      fresh_peer_window_required=True,independent_source_plan_review_required=True,new_ROOT_grant_required=True,remote_updates=1,push_force=False,no_automatic_retries=True,
      proposed_map_paths=MAPS,live_map_replacements_by_this_actor=[],primary_branch_HEAD_and_entire_index_unchanged=True,all_live_maps_untouched_by_this_actor=True,selected_maps_future_only=True,
      live_sealer_or_future_receipts_claimed=False,own_prepare_outer_receipt='Absent until genuine parent recorder observes completion')
    save(run/'PLAN.json',plan);(run/'PLAN.json').chmod(0o444)
    print(json.dumps(dict(status='GET_ONLY_REVIEWABLE_PLAN_NO_EXECUTION_AUTHORITY',plan=pin(run/'PLAN.json'),before_main=h,anticipated_commit=plan['anticipated_after_commit'],selected_files=len(files))))
def checked_plan(path):
    z=pin(path);need(z['mode']==0o444 and Path(path).resolve().is_relative_to(B),'own sealed plan');p=json.loads(same(z));s,f=selected()
    need(p['schema']=='checkpoint049-get-only-provider-plan-v1' and p['execution_authority'] is False and p['writer_window_authority'] is False and p['fixture_only'] is False and type(p['provider_mutations']) is int and p['provider_mutations']==p['local_Git_mutations']==0,'inactive actual read-only plan')
    need(p['source_domain']==packet() and p['complete_get_only_native_ledger']['mode']==0o444,'whole sealed source/actual ledger')
    ledger=json.loads(same(p['complete_get_only_native_ledger']));need(completed_native_ledger(Path(path).parent,p['actual_plan_actor_PID'])==ledger,'complete actual native ledger replay')
    need(p['sources']==sources() and p['runtimes']==runtime() and p['selector']==s and p['files']==f and valid(p['before_main']) and p['push_force'] is False and p['remote_updates']==1 and p['no_automatic_retries'] is True,'exact source/runtime/selector/remote contract')
    class Offline:
        def get(self,path):
            h=path.rsplit('/',1)[-1];rows=[x for x in p['overlay']['before_trees'].values() if x['sha']==h];need(rows,'recorded full old tree');return dict(sha=h,truncated=False,tree=[dict(path=n,**v) for n,v in rows[0]['entries'].items()])
    need(derive(Offline(),f,p['before_tree'])==p['overlay'],'offline full canonical overlay including every unselected sibling')
    need(p['mutation_sequence']==[PREFIX+'git/trees',PREFIX+'git/commits','graphql'] and p['mutation_count']==3 and p['main_ref_update_count']==1 and p['live_map_replacements_by_this_actor']==[],'exact provider-only mutation contract')
    expected_tree=dict(base_tree=p['before_tree'],tree=[dict(path=n,mode='100644',type='blob',content=same(z['input']).decode()) for n,z in sorted(f.items())]);need(p['provider_tree_payload']==expected_tree,'full exact tree request')
    cp=p['commit_payload'];need(cp['tree']==p['anticipated_after_tree']==p['overlay']['after_tree'] and cp['parent']==p['before_main'] and cp['message']==(B/'COMMIT_MESSAGE.txt').read_text() and type(cp['timestamp']) is int,'exact canonical commit selected tree/parent/message/typed timestamp');date=datetime.fromtimestamp(cp['timestamp'],timezone.utc).isoformat().replace('+00:00','Z');person=dict(name='Alec Kriebel',email='me@aleckriebel.com',date=date)
    need(p['provider_commit_payload']==dict(message=cp['message'],tree=cp['tree'],parents=[cp['parent']],author=person,committer=person),'full exact provider commit payload')
    need(pin(B/'inputs/ACTUAL_SOURCE_PINS.json')==p['actual_gate_pin_file'] and json.loads(same(p['actual_gate_pin_file']))['files']==p['actual_gate_pins'],'exact actual prerequisite gate pin source');[same(z) for z in p['actual_gate_pins'].values()]
    raw=commit_raw(p['commit_payload']);need(base64.b64decode(p['canonical_commit_raw_base64'],validate=True)==raw and oid('commit',raw)==p['anticipated_after_commit'],'canonical exact single-parent unsigned commit')
    return z,p,f
def actual_plan_outer(z,pp,p):
    import gzip
    need(z['mode']==0o444 and Path(z['path']).is_relative_to(B),'own immutable actual outer execution');e=json.loads(same(z));q=json.loads(same(e['request']));d=Path(z['path']).parent;s=json.loads(same(pin(d/'started.json')))
    need(e['schema']=='checkpoint049-native-completed-observation-v1' and q['schema']=='checkpoint049-native-request-v1' and s['schema']=='checkpoint049-native-start-v1','literal outer custody schemas')
    stamps=[datetime.fromisoformat(x['UTC']) for x in [q,s,e]];need(all(x.utcoffset()==timedelta(0) for x in stamps) and stamps[0]<=stamps[1]<=stamps[2],'ordered actual outside UTC timestamps')
    expected=[p['runtimes']['python_launcher']['path'],'-E','-B',str(B/'checkpoint049.py'),'prepare','--run',str(Path(pp['path']).parent),'--expected-main',p['before_main']]
    need(q['argv']==e['argv']==expected and q['cwd']==e['cwd']==str(B) and q['program']==p['sources']['checkpoint049.py'] and q['recorder_source']==p['sources']['native_capture.py'],'exact outside-launch source/argv/cwd')
    need(type(e['actual_child_PID']) is int and e['actual_child_PID']==s['actual_child_PID']==p['actual_plan_actor_PID'] and type(e['actual_recorder_PID']) is int and e['actual_recorder_PID']==q['actual_recorder_PID']==s['actual_recorder_PID'] and e['actual_recorder_PID']!=e['actual_child_PID'],'typed completed plan parent/child linkage')
    need(type(e['returncode']) is int and e['returncode']==0 and e['communication_complete'] is e['wait_completed'] is e['reaped'] is True and e['failure'] is None and e['cleanup_errors']==[],'actual plan completed/full/direct wait/reap')
    need({x.name for x in d.iterdir()}=={'request.json','started.json','execution.json','recorder_PRELAUNCH.py','program_PRELAUNCH.py','stdout.gz','stderr.gz'},'closed actual outer custody')
    need((d/'program_PRELAUNCH.py').read_bytes()==same(q['program']) and (d/'recorder_PRELAUNCH.py').read_bytes()==same(q['recorder_source']),'whole actual outer prelaunch bodies')
    for name,zs in e['streams'].items():
        need(name in ['stdout','stderr'] and zs['complete'] is True and zs['stored']==pin(d/(name+'.gz')) and type(zs['logical_bytes']) is int,'typed outside full stream')
        raw=gzip.decompress(same(zs['stored']));need(len(raw)==zs['logical_bytes'] and sha(raw)==zs['logical_sha256'],'whole outside logical body')
        if name=='stdout':need(json.loads(raw)['plan']==pp and json.loads(raw)['status']=='GET_ONLY_REVIEWABLE_PLAN_NO_EXECUTION_AUTHORITY','outside child output binds exact genuine plan')
    need(set(e['streams'])=={'stdout','stderr'},'both outside streams')
def grant(path,pp,p):
    z=pin(path);need(Path(path).name=='ROOT_CHECKPOINT049_GRANT_01.json' and Path(path).parent==B and z['mode']==0o444,'literal external ROOT grant');g=json.loads(same(z))
    need(g['schema']=='root-checkpoint049-one-use-provider-grant-v1' and g['execution_authority'] is True and g['fixture_only'] is False and g['issues']==[] and g['required_repairs']==[],'genuine issue-free production ROOT grant')
    need(g['plan']==pp and g['sources']==p['sources'] and g['selector']==p['selector'] and g['runtimes']==p['runtimes'] and g['future_run']==p['future_run'],'exact reviewed source/plan/runtime binding')
    need(g['writer_window_owner']=='descending_root' and g['peer_writer_window_explicitly_released'] is True and g['fresh_peer_window_verified'] is True and g['before_main']==p['before_main'] and g['force'] is False and type(g['maximum_mutations']) is int and g['maximum_mutations']==3 and type(g['maximum_main_ref_updates']) is int and g['maximum_main_ref_updates']==1 and g['branch']=='refs/heads/main' and g['no_automatic_retries'] is True and re.fullmatch('[0-9a-f]{48}',g['nonce']),'fresh exact one-use nonforce peer window')
    now=datetime.now(timezone.utc);issued=datetime.fromisoformat(g['issued_UTC']);expires=datetime.fromisoformat(g['expires_UTC']);need(issued.utcoffset()==expires.utcoffset()==timedelta(0) and issued<=now<expires and timedelta(0)<expires-issued<=timedelta(minutes=30),'fresh grant lifetime')
    need(g['source_plan_acceptance']['mode']==0o444,'immutable ROOT source/plan acceptance');a=json.loads(same(g['source_plan_acceptance']));need(a['schema']=='root-checkpoint049-source-plan-acceptance-v1' and a['fixture_only'] is False and a['accepted'] is True and a['execution_authority'] is False and a['writer_window_authority'] is False and a['issues']==[] and a['required_repairs']==[] and a['plan']==pp and a['sources']==p['sources'] and a['selector']==p['selector'] and a['runtimes']==p['runtimes'],'independently reviewed ROOT source/plan acceptance')
    need(a['independent_verdict']['mode']==a['independent_review']['mode']==0o444,'immutable independent verdict/review');verdict=json.loads(same(a['independent_verdict']));same(a['independent_review']);need(verdict['schema']=='independent-checkpoint049-source-plan-verdict-v1' and verdict['fixture_only'] is False and verdict['accepted'] is True and verdict['issues']==[] and verdict['required_repairs']==[] and verdict['execution_authority'] is False and verdict['writer_window_authority'] is False and verdict['plan']==pp and verdict['sources']==p['sources'] and verdict['selector']==p['selector'] and verdict['runtimes']==p['runtimes'],'fresh adversarial review before grant')
    need(g['fresh_peer_window_evidence']['mode']==0o444,'immutable actual peer evidence');same(g['fresh_peer_window_evidence']);need(g['source_plan_acceptance']['path']==str(B/'ROOT_CHECKPOINT049_SOURCE_PLAN_ACCEPTANCE_01.json'),'fixed literal ROOT acceptance role');need(a['whole_actual_plan_native_custody_consumed'] is True and a['whole_original_source_and_held_custody_consumed'] is True,'explicit genuine whole ROOT plan consumption');actual_plan_outer(a['actual_completed_plan_outer_custody'],pp,p);return z,g
def execute(path,grant_path):
    pp,p,files=checked_plan(path);gp,g=grant(grant_path,pp,p);run=Path(p['future_run']);need(run==B/'ROOT_actual_checkpoint049_01','exact future attempt');run.mkdir(exist_ok=False)
    save(run/'ATTEMPT_CONSUMED.json',dict(UTC=utc(),plan=pp,grant=gp,nonce=g['nonce'],outcome='UNCERTAIN_UNTIL_ACTUAL_COMPLETION',automatic_retry=False))
    api=API(run,True);held=read_held();probe=run/'primary_begin';probe.mkdir();first=primary(probe);need(first==p['primary_before'],'same whole primary branch/HEAD/index baseline')
    h=identity(api,p['before_main']);c=api.get(PREFIX+'git/commits/'+h);need(c['tree']['sha']==p['before_tree'],'fresh exact before main tree')
    need(derive(api,files,c['tree']['sha'])==p['overlay'],'fresh full canonical original tree and all unselected siblings')
    for route,payload,expected in [(PREFIX+'git/trees',p['provider_tree_payload'],p['anticipated_after_tree']),(PREFIX+'git/commits',p['provider_commit_payload'],p['anticipated_after_commit'])]:
        grant(grant_path,pp,p);need(read_held()==held,'all eight live held maps stay untouched');x=api.post(route,payload);need(x['sha']==expected,'exact newly created object hash')
    for z in p['overlay']['after_trees']:need(checked_tree(api.get(PREFIX+'git/trees/'+z['sha']),z['sha'])==z['entries'],'all created canonical trees before reference update')
    created=api.get(PREFIX+'git/commits/'+p['anticipated_after_commit']);cp=p['provider_commit_payload']
    need(created['tree']['sha']==cp['tree'] and [z['sha'] for z in created['parents']]==cp['parents'] and created['message']==cp['message'].rstrip('\n') and created['author']==cp['author'] and created['committer']==cp['committer'],'whole exact new unsigned commit')
    identity(api,h);grant(grant_path,pp,p);need(read_held()==held,'all held maps unchanged before sole CAS')
    query='mutation($input: UpdateRefsInput!) { updateRefs(input: $input) { clientMutationId } }';client='checkpoint049_'+g['nonce']
    repository=api.get(PREFIX.rstrip('/'));need(repository['full_name']=='AlecKriebel/Math' and repository['id']==RID and repository['node_id']==RN,'exact repository before CAS')
    payload=dict(query=query,variables=dict(input=dict(repositoryId=RN,refUpdates=[dict(name='refs/heads/main',beforeOid=h,afterOid=p['anticipated_after_commit'],force=False)],clientMutationId=client)))
    grant(grant_path,pp,p);identity(api,h);x=api.post('graphql',payload);need(x['data']['updateRefs']['clientMutationId']==client,'single expected-before force-false CAS acknowledgement')
    identity(api,p['anticipated_after_commit']);need(api.posts==p['mutation_sequence'],'exact three POSTs and one main reference update')
    tail=run/'primary_end';tail.mkdir();need(primary(tail)==first and read_held()==held,'whole primary branch/HEAD/index and all held maps unchanged')
    save(run/'RESULT.json',dict(status='ACTUAL_THREE_POSTS_ONE_EXPECTED_OLD_FORCE_FALSE_MAIN_CAS_ACKNOWLEDGED_FULL_REMOTE_READBACK_PENDING',UTC=utc(),actual_commit=p['anticipated_after_commit'],sole_parent=h,tree=p['anticipated_after_tree'],plan=pp,grant=gp,
      force=False,POST_count=3,main_ref_update_count=1,local_Git_mutations=0,live_map_writes=0,primary_full_index_HEAD_branch_and_all_held_maps_preserved=True,ROOT_actual_acceptance=False))
    print(json.dumps(dict(status='ACTUAL_CAS_ACKNOWLEDGED_INDEPENDENT_READBACK_AND_ROOT_REVIEW_PENDING',commit=p['anticipated_after_commit'],result=pin(run/'RESULT.json'))))

def readback(path,run):
    pp,p,files=checked_plan(path);need(run.parent==B and re.fullmatch('ROOT_readback_[0-9]{2}',run.name),'new exact read-only namespace');run.mkdir(exist_ok=False);api=API(run);h=identity(api)
    ancestor=api.get(PREFIX+'compare/'+p['anticipated_after_commit']+'...'+h+'?per_page=1&page=2');need(ancestor['merge_base_commit']['sha']==p['anticipated_after_commit'] and ancestor['behind_by']==0,'remote actual checkpoint or preserved descendant')
    c=api.get(PREFIX+'git/commits/'+p['anticipated_after_commit']);need(c['tree']['sha']==p['anticipated_after_tree'] and [z['sha'] for z in c['parents']]==[p['before_main']] and c['message']==p['commit_payload']['message'].rstrip('\n'),'actual exact checkpoint tree/sole parent/message')
    for z in p['overlay']['after_trees']:need(checked_tree(api.get(PREFIX+'git/trees/'+z['sha']),z['sha'])==z['entries'],'complete whole created canonical tree with unselected siblings')
    for n,z in files.items():
        x=api.get(PREFIX+'git/blobs/'+z['blob']);body=base64.b64decode(re.sub(r'\s','',x['content']),validate=True);need(x['encoding']=='base64' and x['sha']==z['blob'] and type(x['size']) is int and x['size']==len(body) and body==same(z['input']),'full exact remote selected blob')
    current=api.get(PREFIX+'git/commits/'+h);now=derive(api,files,current['tree']['sha'])
    for n,z in files.items():d,leaf=n.rsplit('/',1);need(now['before_trees'][d]['entries'].get(leaf)==dict(mode='100644',type='blob',sha=z['blob']),'remote descendant preserves selected content')
    identity(api,h);save(run/'RESULT.json',dict(status='FULL_READONLY_REMOTE_CHECKPOINT049_VERIFIED_ROOT_COMPLETED_OPERATION_ADVERSARY_PENDING',UTC=utc(),actual_commit=p['anticipated_after_commit'],observed_remote_main=h,plan=pp,whole_blobs=len(files),remote_mutations=0,ROOT_actual_acceptance=False))
    print(json.dumps(dict(status='FULL_REMOTE_READBACK_PENDING_ROOT_ADVERSARIAL_ACCEPTANCE',result=pin(run/'RESULT.json'))))
if __name__=='__main__':
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'Python -E -B without optimization')
    need(not any(k.startswith('GIT_') for k in os.environ),'no ambient Git redirection')
    for k in ['GH_DEBUG','GITHUB_DEBUG','DEBUG','NODE_DEBUG']:os.environ.pop(k,None)
    os.environ['GH_PROMPT_DISABLED']='1';os.environ['GH_NO_UPDATE_NOTIFIER']='1'
    q=argparse.ArgumentParser();q.add_argument('mode',choices=['prepare','execute','readback']);q.add_argument('--run',type=Path);q.add_argument('--plan',type=Path);q.add_argument('--grant',type=Path);q.add_argument('--expected-main');a=q.parse_args()
    if a.mode=='prepare':prepare(a.run,a.expected_main)
    elif a.mode=='execute':execute(a.plan,a.grant)
    else:readback(a.plan,a.run)
