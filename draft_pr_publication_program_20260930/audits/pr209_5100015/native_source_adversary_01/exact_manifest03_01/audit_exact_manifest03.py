"""Read-only exact manifest03/native metadata audit. No transport or production CLI."""
from pathlib import Path
import ast,base64,calendar,collections,datetime,hashlib,json,os,re,stat,sys,types
BASE=Path(__file__).absolute().parent
CASE=BASE.parents[1]
B=CASE/'native_integration_preparation_01'
FREEZE=BASE.parent/'message_normalization_01'/'source_freeze'
MP={'bytes':246659,'sha256':'153ef02f3eb7a7c701a75b7d68a6fe916fec118f0862680fc2b3da95bcfabaa6'}
EXPECTED={'native209_model.py':{'bytes':35600,'sha256':'207f30fc102f634dddf843b0f31d9b939a5e4dbc376b8ad8eff83537236c8c14'},'native209_future_executor.py':{'bytes':28678,'sha256':'f97661a3db96e9c89e141d13e16676adc55fef58b1be074dff0bcc071a99b93e'},'native_trees_readonly.py':{'bytes':4719,'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}}
CHECKS=[]
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def need(ok,name):
    if type(ok) is not bool or not ok:raise RuntimeError(name)
    CHECKS.append(name)
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def safe(path,maximum=4000000,readonly=False):
    if path.resolve()!=path:raise RuntimeError('Noncanonical path '+str(path))
    handles=[];fd=None
    try:
        current=Path('/');parent=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);handles.append((current,parent,os.fstat(parent)))
        for part in path.parent.parts[1:]:
            current=current/part;parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent);handles.append((current,parent,os.fstat(parent)))
        fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent);a=os.fstat(fd)
        if not(stat.S_ISREG(a.st_mode) and a.st_size<=maximum and (not readonly or stat.S_IMODE(a.st_mode)==0o444)):raise RuntimeError('Bounded regular file '+str(path))
        with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(maximum+1)
        z,e=os.fstat(fd),path.lstat();attrs=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
        if not(attrs(a)==attrs(z)==attrs(e) and len(raw)==z.st_size):raise RuntimeError('File changed '+str(path))
        for path,d,old in handles:
            now,entry=os.fstat(d),path.lstat()
            if not(stat.S_ISDIR(entry.st_mode) and (old.st_dev,old.st_ino)==(now.st_dev,now.st_ino)==(entry.st_dev,entry.st_ino)):raise RuntimeError('Ancestor changed')
        return raw
    finally:
        if fd is not None:os.close(fd)
        for _,d,_ in reversed(handles):os.close(d)

def load(name):
    raw=safe(FREEZE/name,readonly=True);need(pin(raw)==EXPECTED[name],'frozen source '+name)
    m=types.ModuleType('independent_exact_'+name.replace('.','_'));m.__file__=str(B/name)
    exec(compile(raw,str(FREEZE/name),'exec'),m.__dict__);return m
h=load('native209_model.py');c=load('native_trees_readonly.py')
for name,want in EXPECTED.items():need(pin(safe(B/name,readonly=True))==want,'actual source pin '+name)
raw=safe(B/'ROOT_EXACT_MERGE95_MANIFEST_03.json',readonly=True);need(pin(raw)==MP,'exact manifest03 pin');m=h.decode(raw)
class ReachedAuthorityBoundary(Exception):pass
original_sealed=h.sealed
def no_authority(name,expected):
    if name=='ABSENT_EXTERNAL_ROOT_ACTUAL_GATE':raise ReachedAuthorityBoundary()
    return original_sealed(name,expected)
h.sealed=no_authority
try:h.load_inputs('ROOT_EXACT_MERGE95_MANIFEST_03.json',MP,'ABSENT_EXTERNAL_ROOT_ACTUAL_GATE',{'bytes':0,'sha256':'0'*64})
except ReachedAuthorityBoundary:need(True,'actual full load_inputs passed all checks before external Root authority')
else:raise RuntimeError('Unexpected Root authority supplied')
h.sealed=original_sealed
need(m['phase']=='merge95' and h.exact(m['facts'],h.phase_facts('merge95')),'exact95 facts')
need(m['helper_pin']==EXPECTED['native209_model.py'] and m['executor_pin']==EXPECTED['native209_future_executor.py'] and m['core_pin']==EXPECTED['native_trees_readonly.py'],'manifest all executable pins')
need(len(m['files'])==m['total_files']==381 and m['total_bytes']==4533496,'exact381 selected total')
need(len(m['reused_blobs'])==228,'exact228 reused count')
origins_raw=safe(B/'packet95v3'/'SELECTION_ORIGINS_03.json',readonly=True);origins=h.decode(origins_raw)
need(h.exact(origins['native_manifest_pin'],MP),'origins manifest03 pin')
originmap={r['path']:r for r in origins['files']};need(len(originmap)==len(origins['files'])==381,'unique381 origins')
overlay={};pre={};inventory=[]
for row in m['files']:
    path=h.rel(row['path']);need(path not in overlay,'unique selected '+path)
    need(row['source']=='packet95v3/objects/'+row['sha256']+'.data','exact body-addressed source '+path)
    body=original_sealed(row['source'],{k:row[k] for k in ('bytes','sha256')})
    need(native('blob',body)==row['git_blob'],'independent native blob '+path)
    origin=originmap[path];need(pin(body)=={k:origin[k] for k in ('bytes','sha256')},'origin recorded pin '+path)
    op=Path(origin['original_local_source']);need(op.is_absolute() and op.is_relative_to(B.parents[3]),'bounded origin path '+path)
    need(safe(op)==body,'original source bytes '+path)
    need(MP['sha256'].encode() not in body,'no manifest03 self hash in selected body '+path)
    overlay[path]=body;pre[path]=h.tuple_pin(row['preimage']);inventory.append({'path':path,**pin(body),'git_blob':row['git_blob'],'native_preimage':row['preimage'],'source':row['source'],'original_source':str(op)})
need(sum(map(len,overlay.values()))==4533496,'independent selected bytes total')
need(set(originmap)==set(overlay),'no origin extra or missing')
need(not any('/_private/' in p or '/packet95/' in p or '/packet95v3/' in p or '/journal' in p.lower() for p in overlay),'no selected private journals/working packets')
need(not any(p.endswith('.pdf') or 'full_tracker' in p.lower() for p in overlay if not p.startswith(h.ATTEMPT)),'no new full papers or full tracker export')
forbidden=['AUTHENTICATED_NATIVE_TREES.json','REVISED_COMMIT_ACTUAL_FIRST_PARENT_DELTA.json','RECURSIVE_METADATA_AUTHENTICATION.json','RECURSIVE_METADATA_CACHE_BRIDGE.json']
need(not any(p.split('/')[-1] in forbidden for p in overlay),'large private custody metadata bodies excluded')
# Public manifest closures: current source declaration and dated initial source audit are finite.
closures=[]
for group,index,field in [('analytic_trace_adversary_01','PUBLIC_MANIFEST.json','files'),('geometry_adversary_01','PUBLIC_MANIFEST.json','files'),('whole_package_adversary_01','PUBLIC_MANIFEST.json','files'),('whole_package_adversary_02','PUBLIC_MANIFEST_02.json','files'),('native_custody_01','PUBLIC_ALLOWLIST_V3.json','files'),('native_source_adversary_01','PUBLIC_MANIFEST.json','files'),('native_integration_preparation_01','SOURCE_MANIFEST.json','source_files')]:
    prefix=h.CASE+group+'/';obj=h.decode(overlay[prefix+index]);listed=set()
    for r in obj[field]:
        name=h.rel(r['path']);path=prefix+name;need(path in overlay,'closure selected '+path);need(pin(overlay[path])=={k:r[k] for k in ('bytes','sha256')},'closure body '+path);listed.add(path)
    selected={p for p in overlay if p.startswith(prefix)};extras=selected-listed
    if group=='native_integration_preparation_01':need(extras=={prefix+index,prefix+'ROOT_ABANDONED_CANDIDATE95_MANIFEST02_01.json'} and len(listed)==59,'explicit59 source closure plus declaration and unique abandonment receipt')
    elif group=='native_custody_01':need(extras=={prefix+x for x in obj['control_files_without_recursive_self_pins']} and len(listed)==112,'exact112 custody plus2 controls')
    else:need(len(extras)==2 and prefix+index in extras and any('SEAL' in p.split('/')[-1] for p in extras),'finite public closure controls '+group)
    closures.append({'group':group,'declared_files':len(listed),'selected_with_controls':len(selected),'control_files':sorted(extras)})
need(pin(overlay[h.CASE+'native_integration_preparation_01/SOURCE_MANIFEST.json'])=={'bytes':12686,'sha256':'247a829181e5fcd7d75cf75a25cbf4cc31a405b8f5afd17baffec418437d009d'},'final explicit source declaration selected')
need(not any('/phase_transition_01/' in p or '/exact_manifest02_01/' in p or '/exact_manifest03_01/' in p or '/message_normalization_01/' in p or '/native_exact_packet_adversary_02/' in p for p in overlay),'current source extension and exact audits external to avoid hash cycles')

oldraw=safe(BASE.parent/'exact_manifest02_01'/'INPUT_MANIFEST_02.json',readonly=True)
need(pin(oldraw)=={'bytes':239460,'sha256':'1b282ab9e11c5e384b8260099bbe6c039ee0a2a079d709822010b80d5c8f97ca'},'preserved earlier manifest02 pin')
old=h.decode(oldraw);oldmap={r['path']:r for r in old['files']};newmap={r['path']:r for r in m['files']}
need(not(set(oldmap)-set(newmap)),'no selected path removed relative to02')
added_selection=sorted(set(newmap)-set(oldmap));changed_selection=[]
for path in sorted(set(newmap)&set(oldmap)):
    if any(newmap[path][k]!=oldmap[path][k] for k in ('bytes','sha256','git_blob','preimage')):changed_selection.append(path)
prep=h.CASE+'native_integration_preparation_01/'
need(len(added_selection)==14 and all(p.startswith(prep) for p in added_selection),'exact14 added repair/history/abandonment rows only')
need(len(changed_selection)==11 and all(p.startswith(prep) or p in h.VIEWS for p in changed_selection),'exact11 changed source/view body rows only')
need(all(oldmap[p]['preimage']==newmap[p]['preimage'] for p in set(oldmap)&set(newmap)),'all native preimages unchanged from02')
need(h.exact(m['reused_blobs'],old['reused_blobs']) and h.exact(m['local_views'],[{**r,'source':None if r['source'] is None else r['source'].replace('packet95/','packet95v3/')} for r in old['local_views']]),'228 reuse and all5 local preimages unchanged from02')
need(m['candidate_journal']!=old['candidate_journal'],'new immutable intent journal distinct from abandoned02')
abandon= h.decode(overlay[prep+'ROOT_ABANDONED_CANDIDATE95_MANIFEST02_01.json'])
need(abandon['candidate']=='45d77dd0d8780135182dcab3fc6ac518e9ac7564' and h.exact(abandon['manifest_pin'],pin(oldraw)) and abandon['abandoned_for_any_ref_or_sync'] is True and abandon['actual_ref_update_performed'] is False and abandon['actual_local5_sync_performed'] is False,'explicit old45d/manifest02 abandonment receipt selected; no ref or sync claimed')
need(abandon['current_expected_MAIN_unchanged']==m['expected_parent'] and abandon['counts']=={'fully_completed':50,'published':34},'abandonment receipt baseline stays50/34')

# Exactly one current95 marker and truthful structured view aliases/prefixes.
for path in (h.VIEWS[1],h.VIEWS[3],h.VIEWS[4]):h.markdown_current(overlay[path],'merge95',path in (h.VIEWS[1],h.VIEWS[4]))
for row in m['local_views']:
    target=B.parents[3]/row['path']
    if row['preimage'] is None:need(not target.exists() and not target.is_symlink(),'actual new local JSON remains absent')
    else:need(pin(safe(target))==row['preimage'],'actual local preimage '+row['path'])
# Read-only actual stable-lock and unreserved-attempt observations.
lock=B.parents[3]/m['writer_lock']['path'];lockbody=safe(lock,readonly=True);ls=lock.stat()
need(pin(lockbody)=={k:m['writer_lock'][k] for k in ('bytes','sha256')} and (ls.st_dev,ls.st_ino)==(m['writer_lock']['device'],m['writer_lock']['inode']),'actual stable lock inode and payload unchanged without acquiring/replacing it')
need(not (B/m['candidate_journal']).exists() and not (B/m['candidate_journal']).is_symlink(),'manifest-bound candidate attempt not yet reserved')
# Prior independently authenticated immutable native metadata is reused; mutable observations retain their original UTC. No network here.
receipts=h.decode(safe(BASE/'READONLY_NATIVE_GET_RECEIPTS.json'));need(len(receipts['requests'])<=20,'bounded metadata GET count')
metadata={}
for row in receipts['requests']:
    body=safe(BASE/'_private_native_metadata'/row['private_body'],readonly=True);need(pin(body)=={k:row[k] for k in ('bytes','sha256')},'native GET response pin '+row['path']);metadata[row['path']]=h.decode(body)
need(metadata['git/ref/heads/main']['object']['sha']==m['expected_parent'],'earlier observed MAIN lease; freshness is external future guard')
parent=metadata['git/commits/'+m['expected_parent']];need(parent['sha']==m['expected_parent'] and parent['tree']['sha']==m['expected_parent_tree'],'fresh actual parent/tree identity')
pr=metadata['pulls/209'];need(type(pr['number']) is int and pr['number']==209 and pr['state']=='open' and pr['draft'] is False and pr['merged'] is False and pr['head']['sha']==h.PREPARED and pr['base']['ref']=='main','earlier observed ready PR209 HEAD; future guard must refresh')
for oid,tree in [(h.ORIGINAL,h.ORIGINAL_TREE),(h.PREPARED,h.PREPARED_TREE)]:need(metadata['git/commits/'+oid]['sha']==oid and metadata['git/commits/'+oid]['tree']['sha']==tree,'fresh custody commit '+oid)
need([x['sha'] for x in metadata['git/commits/'+h.PREPARED]['parents']]==[h.ORIGINAL,'53b8291b2247008172f1fc3f596c96708faf8903'],'prepared commit original ancestry')
# Independent canonical serializer plus the previously audited canonical core agree.
def treehash(rows):
    rows=sorted(rows,key=lambda r:r[0].encode()+ (b'/' if r[1]=='040000' else b''))
    raw=b''.join((mode.lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(sha) for name,mode,kind,sha in rows)
    return native('tree',raw)
def api(method,path,body=None):
    if method!='GET' or body is not None:raise RuntimeError('Offline GET-only metadata adapter')
    return metadata[path]
trees=c.NativeTrees(api)
for route,j in metadata.items():
    if route.startswith('git/trees/'):
        rows=[(x['path'],x['mode'],x['type'],x['sha']) for x in j['tree']];need(treehash(rows)==route.split('/')[-1],'independent immediate tree hash '+route);trees.get(j['sha'],0)
for path,entry in pre.items():need(trees.lookup(m['expected_parent_tree'],path)==entry,'fresh native preimage '+path)
need(trees.lookup(m['expected_parent_tree'],h.SHARED)==('040000','tree',h.SHARED_TREE),'whole existing shared tree unchanged anchor')
trie={}
for path,body in overlay.items():
    node=trie;parts=path.split('/')
    for part in parts[:-1]:node=node.setdefault(part,{})
    node[parts[-1]]=body
newtrees={};ind_changed=set();ind_dirs=set()
def rebuild(old,node,prefix=''):
    entries={} if old is None else {x['path']:(x['mode'],x['type'],x['sha']) for x in metadata['git/trees/'+old]['tree']}
    for name,value in node.items():
        path=prefix+name;before=entries.get(name)
        if type(value) is bytes:
            if before!=pre[path]:raise RuntimeError('Independent stale preimage '+path)
            after=('100644','blob',native('blob',value));entries[name]=after
            if before!=after:ind_changed.add(path)
        else:
            if before is not None and before[:2]!=('040000','tree'):raise RuntimeError('Native ancestor collision')
            if before is None:ind_dirs.add(path)
            child=rebuild(None if before is None else before[2],value,path+'/');entries[name]=('040000','tree',child)
    rows=sorted([(name,*entry) for name,entry in entries.items()],key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''));oid=treehash(rows)
    newtrees[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':md,'type':k,'sha':sh} for n,md,k,sh in rows]};return oid
wanted=rebuild(m['expected_parent_tree'],trie)
corewanted,corechanges,coredirs=h.expected(c,c.NativeTrees(api),m['expected_parent_tree'],overlay,pre)
need((wanted,ind_changed,ind_dirs)==(corewanted,corechanges,coredirs),'independent rebuild equals audited exact-preimage rebuild')
def delta_api(method,path,body=None):
    if method!='GET' or body is not None:raise RuntimeError('Conditional metadata only')
    oid=path.removeprefix('git/trees/');return newtrees[oid] if oid in newtrees else api(method,path,body)
reader=c.NativeTrees(delta_api);leaves,added,deleted=reader.changes(m['expected_parent_tree'],wanted)
need(leaves==set(overlay)==ind_changed and added==ind_dirs and not deleted,'conditional complete native delta only381 selected leaves, no deletions')
need(reader.lookup(wanted,h.ATTEMPT[:-1])==('040000','tree',h.ATTEMPT_TREE),'conditional exact prepared own54 subtree')
need(reader.lookup(wanted,h.SHARED)==('040000','tree',h.SHARED_TREE),'conditional shared foreign subtree tuple preserved')
for path,body in overlay.items():need(reader.lookup(wanted,path)==('100644','blob',native('blob',body)),'conditional selected tuple '+path)
# Actual QUEUE body snapshot is authenticated by its fresh native tuple and blob hash.
snapshot=h.decode(safe(CASE/'root_native_snapshot_01'/'READONLY_SNAPSHOT.json'));queueentry=next(r for r in snapshot['entries'] if r['path']==h.QUEUE);oldqueue=safe(CASE/'root_native_snapshot_01'/queueentry['source']);need(pin(oldqueue)=={k:queueentry[k] for k in ('bytes','sha256')} and native('blob',oldqueue)==pre[h.QUEUE][2],'old QUEUE full bytes match fresh blob identity');h.queue_change(oldqueue,overlay[h.QUEUE],'merge95')
request,commit=h.commit_request(m,wanted,[m['expected_parent'],h.PREPARED]);need(request['parents']==[m['expected_parent'],h.PREPARED],'conditional commit current ready HEAD second parent')

def independent_identity(role):
    r=m[role];d=datetime.datetime.strptime(r['date'],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    return r['name']+' <'+r['email']+'> '+str(int(d.timestamp()))+' +0000'
canonical_raw=('tree '+wanted+'\n'+''.join('parent '+p+'\n' for p in request['parents'])+'author '+independent_identity('commit_author')+'\ncommitter '+independent_identity('commit_committer')+'\n\n'+m['commit_message']).encode()
need(native('commit',canonical_raw)==commit,'independent canonical raw commit serialization agrees with helperOID')
need(commit!='45d77dd0d8780135182dcab3fc6ac518e9ac7564','new03 deterministic commit differs from abandoned45d')
reuse_ref=original_sealed('EXISTING_SHARED_BODY_IDENTITIES.json',h.REFERENCE_PINS['EXISTING_SHARED_BODY_IDENTITIES.json']);need(h.exact(m['reused_blobs'],h.decode(reuse_ref)['files']) and sum(r['bytes'] for r in m['reused_blobs'])==5435888,'exact228 existing-body identities5435888B no copies')
output={'schema':'pr209-independent-exact-manifest03-assessment-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_EXACT_MANIFEST_CONDITIONAL_ONLY','manifest_pin':MP,'source_pins':EXPECTED,'phase':'merge95','facts':m['facts'],'expected_parent':m['expected_parent'],'expected_parent_tree':m['expected_parent_tree'],'expected_conditional_tree':wanted,'expected_conditional_commit':commit,'expected_parents':request['parents'],'selected_files':381,'selected_bytes':4533496,'unchanged_reused_files':228,'unchanged_reused_bytes':5435888,'changed_leaves':sorted(leaves),'new_directories':sorted(added),'deleted_directories':[],'source_public_closures':closures,'check_count':len(CHECKS),'prior_native_metadata_GET_observations_reused':len(receipts['requests']),'new_native_metadata_GETs':0,'mutable_observation_UTC':receipts['UTC'],'mutable_freshness_required_externally':True,'selected_body_delta_vs02':{'added':added_selection,'removed':[],'changed':changed_selection},'old45d_abandonment_receipt_verified':True,'canonical_raw_commit_pin':pin(canonical_raw),'actual_native_reused_full_bodies_fetched':False,'actual_manifest03_candidate_accepted':False,'actual_Root_gate_created':False,'ref_or_local_sync_performed':False,'manifest01_cleared':False,'mandatory_findings':[],'optional_findings':[],'goal_complete':False}
for name,value in [('ASSESSMENT.json',output),('EXACT_BODY_INVENTORY.json',{'manifest_pin':MP,'files':inventory}),('CHECKS.json',{'check_count':len(CHECKS),'checks':CHECKS})]:
    dest=BASE/name
    if dest.exists():
        import tempfile
        fd,replay=tempfile.mkstemp(prefix='REPLAY_'+dest.stem+'_',suffix='.json',dir=BASE)
        with os.fdopen(fd,'wb') as stream:stream.write(enc(value))
    else:dest.write_bytes(enc(value))
print(json.dumps({k:output[k] for k in ('status','check_count','expected_conditional_tree','expected_conditional_commit','new_native_metadata_GETs')},sort_keys=True))
