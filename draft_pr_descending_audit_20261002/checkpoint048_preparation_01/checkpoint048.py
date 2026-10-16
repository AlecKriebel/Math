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
EXPECTED_REMOTE='5de48499b84f168099d0273a340f4976f841f691'
PRIMARY_HEAD='6144d964777214c6963a915288c18fcf97b42026'
LAST='bc30acf203a01f1541e5feab62a58c3d12847c82'
MAPS=[P+'/CURRENT_SCOPE.json',P+'/inventory.json',P+'/RESEARCH_LOG.md',V+'/CURRENT_AUDIT_STATUS.json',V+'/RESEARCH_LOG.md',P+'/SHARED_GIT_WINDOW_STATUS.json']
def need(x,m):
    if not x: raise RuntimeError(m+'; preserve genuine state, reconcile read-only, no automatic mutation retry')
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def oid(k,b): return hashlib.sha1(k.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def valid(h): return type(h) is str and re.fullmatch('[0-9a-f]{40}',h) is not None
def pin(p):
    p=Path(p);need(p.is_file() and not p.is_symlink(),'literal regular input')
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def same(z):
    need(pin(z['path'])==z,'complete same-byte/mode input');return Path(z['path']).read_bytes()
def save(p,d):
    p=Path(p);need(p.resolve().is_relative_to(B),'own output namespace');p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write((json.dumps(d,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
def sources(): return {n:pin(B/n) for n in ['checkpoint048.py','native_capture.py','README.md','COMMIT_MESSAGE.txt']}
def native():
    z=pin(B/'native_capture.py');need(z==json.loads((B/'SOURCE_PINS.json').read_bytes())['native_capture.py'],'external local native source pin')
    spec=importlib.util.spec_from_file_location('checkpoint048_native',B/'native_capture.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def selected():
    z=pin(B/'SELECTOR.json');need(z['mode']==0o444,'sealed selector');s=json.loads(same(z))
    need(s['schema']=='checkpoint048-public-closed-content-selection-v1' and s['execution_authority'] is False and s['writer_window_authority'] is False,'inactive actual content selector')
    need(s['counters']==[33,13,12,0] and s['held_uncompleted']==[293,292,280] and s['progress']==dict(case=80,publication=100,tracker=100,author_integration=0,native_merge=0),'genuine current point')
    files={}
    for x in s['entries']:
        n=x['target'];p=Path(n);need(type(n) is str and not p.is_absolute() and all(a not in ('..','.') for a in p.parts) and n.startswith(P+'/') and n not in files,'unique literal selected path')
        q=B/'frozen'/n;need(x['input']['path']==str(q) and x['input']['mode']==0o444,'literal own immutable frozen body')
        b=same(x['input']);need(len(b)<600000 and b.decode().encode()==b,'complete bounded UTF8 body')
        files[n]=dict(input=x['input'],blob=oid('blob',b),kind=x['kind'])
    need(len(files)==s['selected_file_count'] and sum(x['input']['bytes'] for x in files.values())==s['selected_bytes'],'closed complete content count')
    scope=json.loads(same(files[MAPS[0]]['input']));inv=json.loads(same(files[MAPS[1]]['input']));audit=json.loads(same(files[MAPS[3]]['input']))
    need(scope['current_original_head']=='deb9d7491a0bf887f7615717a5b484caf212cfd6' and scope['current_original_status']=='claimed_solved' and scope['current_original_author_budget']=='1/5' and scope['current_additional_author_search_turns']==0,'retained exact eligibility/budget')
    need([scope[k] for k in ['completed_count','published_count','native_merged_count','tracker_pending_count']]==[33,13,12,0] and scope['last_completed_pr']==283 and scope['current_complete_package_rounds_accepted']==2,'current publication distinct from completed historical case')
    need(scope['current_publication_complete'] and scope['current_DOI']=='10.5281/zenodo.23196750' and scope['current_tracker_range']=="'Math Puzzles'!A34:D34" and scope['current_native_merge_pending'],'actual publication/tracker with native merge pending')
    item=next(x for x in inv['items'] if x['number']==278)
    need(item['paper'] and item['tracker'] and item['DOI']==scope['current_DOI'] and not any(item[k] for k in ['merged','closed','case_completed']) and item['workflow_percent']==audit['workflow_percent']==80,'same explicit incomplete case')
    need(inv['completed_by_descending']==33 and len(inv['claimed_solved_published_by_descending'])==13 and len(inv['claimed_solved_merged_by_descending'])==12 and inv['claimed_solved_tracker_pending_by_descending']==[],'matching inventory counters')
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
        self.run=run;self.n=0;self.N=native();self.write=write;self.posts=[];self.src=sources();self.sp,self.files=selected();self.rp=runtime();self.deadline=time.monotonic()+300
        save(run/'API_PRELAUNCH.json',dict(UTC=utc(),actual_PID=os.getpid(),sources=self.src,selector=self.sp,runtimes=self.rp,write=write,automatic_retry=False))
    def guards(self):need(sources()==self.src and selected()==(self.sp,self.files) and runtime()==self.rp,'same exact source/selector/runtimes before and after every child')
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
        need(head.startswith(b'HTTP/') and head.splitlines()[0].split()[1] in ([b'200'] if method=='GET' else [b'200',b'201']),'original numeric successful HTTP status token')
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
    index=R/'.git/index';need(index.is_file(),'ordinary primary index path');z=pin(index)
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
    return dict(branch='main',HEAD=PRIMARY_HEAD,index=z,tracked_stage_bytes=len(tracked),tracked_stage_sha256=sha(tracked),index_flags_sha256=sha(flags),materialized_nonselected=rows)
def runtime():return {n:pin(Path(p).resolve()) for n,p in [('git',GIT),('gh',GH),('python_launcher',sys.executable),('python_engine',PYTHON_ENGINE)]}
def prepare(run):
    need(run.parent==B and re.fullmatch('read_only_prepare_[0-9]{2}',run.name),'own exclusive read-only namespace');run.mkdir(exist_ok=False)
    s,files=selected();held=read_held();src=sources();rp=runtime();gate_pins=json.loads((B/'inputs/ACTUAL_GATE_PINS.json').read_bytes())['gates'];[same(z) for z in gate_pins.values()];first=primary(run)
    api=API(run);h=identity(api,EXPECTED_REMOTE);c=api.get(PREFIX+'git/commits/'+h);need(c['sha']==h and valid(c['tree']['sha']),'actual remote commit tree')
    anc=api.get(PREFIX+'compare/'+LAST+'...'+h+'?per_page=1&page=2');need(anc['merge_base_commit']['sha']==LAST and anc['behind_by']==0 and anc['status'] in ['ahead','identical'],'remote descends from actual checkpoint047')
    overlay=derive(api,files,c['tree']['sha'])
    # Every selected existing path must be absent or equal to an authenticated
    # checkpoint047/046 value or this exact candidate. Never roll back a peer edit.
    old={}
    for path in [R/V/'checkpoint047_preparation_01/SELECTOR.json',R/P/'audits/pr283_30005460/checkpoint046_preparation_01/SELECTOR.json']:
        for x in json.loads(path.read_bytes())['files']:
            b=Path(x['source_frozen_path']).read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'] and oid('blob',b)==x['Git_blob_SHA1'],'historical selected full body')
            old.setdefault(x['path'],set()).add(x['Git_blob_SHA1'])
    # Primary HEAD supplies a further authenticated historical tracked value,
    # particularly the shared-window snapshot omitted by046/047 selection.
    base_raw=api.N.call(run,'PRIMARY_HISTORICAL_SELECTED_TREE',[GIT,'--no-optional-locks','-C',str(R),'ls-tree','-r','-z',PRIMARY_HEAD,'--',*sorted(files)],B)
    for row in base_raw.split(b'\0'):
        if not row:continue
        meta,n=row.split(b'\t',1);mode,kind,digest=meta.decode().split()
        if mode=='100644' and kind=='blob':old.setdefault(n.decode(),set()).add(digest)
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
    plan=dict(schema='checkpoint048-get-only-provider-plan-v1',UTC=utc(),execution_authority=False,writer_window_authority=False,provider_mutations=0,local_Git_mutations=0,
      sources=src,runtimes=rp,selector=s,files=files,actual_gate_pins=gate_pins,actual_gate_pin_file=pin(B/'inputs/ACTUAL_GATE_PINS.json'),held_map_before=held,primary_before=first,before_main=h,before_tree=c['tree']['sha'],overlay=overlay,no_rollback=safe,
      commit_payload=cp,canonical_commit_raw_base64=base64.b64encode(raw).decode(),anticipated_after_commit=oid('commit',raw),anticipated_after_tree=cp['tree'],
      future_run=str(B/'ROOT_actual_checkpoint048_01'),provider_tree_payload=dict(base_tree=c['tree']['sha'],tree=[dict(path=n,mode='100644',type='blob',content=same(z['input']).decode()) for n,z in sorted(files.items())]),
      provider_commit_payload=dict(message=cp['message'],tree=cp['tree'],parents=[h],author=dict(name='Alec Kriebel',email='me@aleckriebel.com',date=datetime.fromtimestamp(timestamp,timezone.utc).isoformat().replace('+00:00','Z')),committer=dict(name='Alec Kriebel',email='me@aleckriebel.com',date=datetime.fromtimestamp(timestamp,timezone.utc).isoformat().replace('+00:00','Z'))),
      mutation_sequence=[PREFIX+'git/trees',PREFIX+'git/commits','graphql'],mutation_count=3,main_ref_update_count=1,
      fresh_peer_window_required=True,independent_source_plan_review_required=True,new_ROOT_grant_required=True,remote_updates=1,push_force=False,no_automatic_retries=True,
      proposed_map_paths=MAPS,live_map_replacements_by_this_actor=[],primary_branch_HEAD_and_entire_index_unchanged=True,all_live_maps_untouched_by_this_actor=True,selected_maps_future_only=True,
      live_sealer_or_future_receipts_claimed=False,own_prepare_outer_receipt='Absent until genuine parent recorder observes completion')
    save(run/'PLAN.json',plan);(run/'PLAN.json').chmod(0o444)
    print(json.dumps(dict(status='GET_ONLY_REVIEWABLE_PLAN_NO_EXECUTION_AUTHORITY',plan=pin(run/'PLAN.json'),before_main=h,anticipated_commit=plan['anticipated_after_commit'],selected_files=len(files))))
def checked_plan(path):
    z=pin(path);need(z['mode']==0o444 and Path(path).resolve().is_relative_to(B),'own sealed plan');p=json.loads(same(z));s,f=selected()
    need(p['schema']=='checkpoint048-get-only-provider-plan-v1' and p['execution_authority'] is False and p['provider_mutations']==p['local_Git_mutations']==0,'inactive actual read-only plan')
    need(p['sources']==sources() and p['runtimes']==runtime() and p['selector']==s and p['files']==f and p['before_main']==EXPECTED_REMOTE and p['push_force'] is False and p['remote_updates']==1 and p['no_automatic_retries'] is True,'exact source/runtime/selector/remote contract')
    class Offline:
        def get(self,path):
            h=path.rsplit('/',1)[-1];rows=[x for x in p['overlay']['before_trees'].values() if x['sha']==h];need(rows,'recorded full old tree');return dict(sha=h,truncated=False,tree=[dict(path=n,**v) for n,v in rows[0]['entries'].items()])
    need(derive(Offline(),f,p['before_tree'])==p['overlay'],'offline full canonical overlay including every unselected sibling')
    need(p['mutation_sequence']==[PREFIX+'git/trees',PREFIX+'git/commits','graphql'] and p['mutation_count']==3 and p['main_ref_update_count']==1 and p['live_map_replacements_by_this_actor']==[],'exact provider-only mutation contract')
    expected_tree=dict(base_tree=p['before_tree'],tree=[dict(path=n,mode='100644',type='blob',content=same(z['input']).decode()) for n,z in sorted(f.items())]);need(p['provider_tree_payload']==expected_tree,'full exact tree request')
    cp=p['commit_payload'];need(cp['tree']==p['anticipated_after_tree']==p['overlay']['after_tree'] and cp['parent']==p['before_main'] and cp['message']==(B/'COMMIT_MESSAGE.txt').read_text() and type(cp['timestamp']) is int,'exact canonical commit selected tree/parent/message/typed timestamp');date=datetime.fromtimestamp(cp['timestamp'],timezone.utc).isoformat().replace('+00:00','Z');person=dict(name='Alec Kriebel',email='me@aleckriebel.com',date=date)
    need(p['provider_commit_payload']==dict(message=cp['message'],tree=cp['tree'],parents=[cp['parent']],author=person,committer=person),'full exact provider commit payload')
    need(pin(B/'inputs/ACTUAL_GATE_PINS.json')==p['actual_gate_pin_file'] and json.loads(same(p['actual_gate_pin_file']))['gates']==p['actual_gate_pins'],'exact actual prerequisite gate pin source');[same(z) for z in p['actual_gate_pins'].values()]
    raw=commit_raw(p['commit_payload']);need(base64.b64decode(p['canonical_commit_raw_base64'],validate=True)==raw and oid('commit',raw)==p['anticipated_after_commit'],'canonical exact single-parent unsigned commit')
    return z,p,f
def grant(path,pp,p):
    z=pin(path);need(Path(path).name=='ROOT_CHECKPOINT048_GRANT_01.json' and Path(path).parent==B and z['mode']==0o444,'literal external ROOT grant');g=json.loads(same(z))
    need(g['schema']=='root-checkpoint048-one-use-provider-grant-v1' and g['execution_authority'] is True and g['fixture'] is False and g['issues']==[],'genuine issue-free production ROOT grant')
    need(g['plan']==pp and g['sources']==p['sources'] and g['selector']==p['selector'] and g['runtimes']==p['runtimes'] and g['future_run']==p['future_run'],'exact reviewed source/plan/runtime binding')
    need(g['writer_window_owner']=='descending_root' and g['peer_writer_window_explicitly_released'] is True and g['fresh_peer_window_verified'] is True and g['before_main']==p['before_main'] and g['force'] is False and type(g['maximum_mutations']) is int and g['maximum_mutations']==3 and type(g['maximum_main_ref_updates']) is int and g['maximum_main_ref_updates']==1 and g['branch']=='refs/heads/main' and g['no_automatic_retries'] is True and re.fullmatch('[0-9a-f]{48}',g['nonce']),'fresh exact one-use nonforce peer window')
    now=datetime.now(timezone.utc);issued=datetime.fromisoformat(g['issued_UTC']);expires=datetime.fromisoformat(g['expires_UTC']);need(issued.utcoffset()==expires.utcoffset()==timedelta(0) and issued<=now<expires and timedelta(0)<expires-issued<=timedelta(minutes=30),'fresh grant lifetime')
    a=json.loads(same(g['source_plan_acceptance']));need(a['accepted'] is True and a['execution_authority'] is False and a['issues']==[] and a['plan']==pp and a['sources']==p['sources'] and a['selector']==p['selector'] and a['runtimes']==p['runtimes'],'independently reviewed ROOT source/plan acceptance')
    verdict=json.loads(same(a['independent_verdict']));same(a['independent_review']);need(verdict['accepted'] is True and verdict['issues']==[] and verdict['execution_authority'] is False,'fresh adversarial review before grant')
    same(g['fresh_peer_window_evidence']);return z,g
def execute(path,grant_path):
    pp,p,files=checked_plan(path);gp,g=grant(grant_path,pp,p);run=Path(p['future_run']);need(run==B/'ROOT_actual_checkpoint048_01','exact future attempt');run.mkdir(exist_ok=False)
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
    query='mutation($input: UpdateRefsInput!) { updateRefs(input: $input) { clientMutationId } }';client='checkpoint048_'+g['nonce']
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
    identity(api,h);save(run/'RESULT.json',dict(status='FULL_READONLY_REMOTE_CHECKPOINT048_VERIFIED_ROOT_COMPLETED_OPERATION_ADVERSARY_PENDING',UTC=utc(),actual_commit=p['anticipated_after_commit'],observed_remote_main=h,plan=pp,whole_blobs=len(files),remote_mutations=0,ROOT_actual_acceptance=False))
    print(json.dumps(dict(status='FULL_REMOTE_READBACK_PENDING_ROOT_ADVERSARIAL_ACCEPTANCE',result=pin(run/'RESULT.json'))))
if __name__=='__main__':
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'Python -E -B without optimization')
    need(not any(k.startswith('GIT_') for k in os.environ),'no ambient Git redirection')
    for k in ['GH_DEBUG','GITHUB_DEBUG','DEBUG','NODE_DEBUG']:os.environ.pop(k,None)
    os.environ['GH_PROMPT_DISABLED']='1';os.environ['GH_NO_UPDATE_NOTIFIER']='1'
    q=argparse.ArgumentParser();q.add_argument('mode',choices=['prepare','execute','readback']);q.add_argument('--run',type=Path);q.add_argument('--plan',type=Path);q.add_argument('--grant',type=Path);a=q.parse_args()
    if a.mode=='prepare':prepare(a.run)
    elif a.mode=='execute':execute(a.plan,a.grant)
    else:readback(a.plan,a.run)
