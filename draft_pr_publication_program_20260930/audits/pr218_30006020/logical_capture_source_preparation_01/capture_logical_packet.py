"""Inactive Root-reviewed PR218 native GET capture and private conditional staging.
No live call occurs on import. No Seed/Runtime/lock/object/ref/provider/PR/five writer.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,stat,sys,time,types
HERE=Path(__file__).absolute().parent
CASE=HERE.parent
PROGRAM=CASE.parents[1]
CHECKOUT=PROGRAM.parent
ENGINE=CASE/'native_completion_preparation_01'
ENGINE_MANIFEST_PIN={'bytes':2654,'sha256':'cbb3620cfddce929aa60c96fdd8abcc3f8f29ebf2981ba3595441bf698016c99'}
MODEL_PIN={'bytes':40648,'sha256':'5f6136ae4335dea22e219c7b1b9d62d416a975e9a8d590a9ca617d732627ae3d'}
PRIMITIVE_PIN={'bytes':16405,'sha256':'6f0162bab7e080445fca633818167476501de9920d566d567fddb1b26f97177c'}
CONTEXT=CASE/'native_source_custody_preparation_02/capture_native_custody.py'
CONTEXT_PIN={'bytes':22852,'sha256':'7576a49d1cb508a73e04421e518e8b7fdb973879e953a15cf85e4d3c40aa4933'}
KNOWN={
 'identity':('ROOT_NATIVE_COMPLETION_IDENTITY_ACCEPTANCE_02.json',{'bytes':17190,'sha256':'07b3b4ca633f6fc571fcb06b3e72c35e8b1e66e554d580ef05d99824dec3cef6'}),
 'ready':('ROOT_CASE_READY_ADOPTION_ACCEPTANCE_02.json',{'bytes':5513,'sha256':'24976f2bc7abb3638fd13fc4f8655f8e94464923feafc76ebece066f3abe08e0'}),
 'carry':('ROOT_PRIOR_OPERATIONAL_CARRY_ACCEPTANCE_02.json',{'bytes':7619,'sha256':'b6f021061cc307fa8a34e91a09d0e1c213a83fb5864605174013bafc72ee1035'})}
MAX_GETS=250
MAX_WIRE=64_000_000
MAX_DECODED=32_000_000
SECONDS=300
def need(x,message):
 if type(x) is not bool or not x:raise RuntimeError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
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
def load(name,path,wanted):
 raw,unused=read_regular(path);need(pin(raw)==wanted,'Pinned inert module changed: '+path.name)
 module=types.ModuleType(name);module.__file__=str(path);exec(compile(raw,str(path),'exec'),module.__dict__);return module
def file_ref(path,wanted=None):
 raw,unused=read_regular(path)
 if wanted is not None:need(pin(raw)==wanted,'Exact file ref differs')
 return {'path':str(path),**pin(raw)},raw
def merge_prefix(local,native):
 need(all(value is None or type(value) is bytes for value in (local,native)),'Separate log byte/absence states')
 if local is None:return native or b''
 if native is None:return local
 if local.startswith(native):return local
 if native.startswith(local):return native
 raise RuntimeError('Divergent native/local log prefixes')
def postimages(h,ready,native,local,utc):
 baseline=h.source_baseline()
 for name,body in (('native',native[h.VIEWS[2]]),('local',local[h.VIEWS[2]])):
  need(type(body) is bytes,name+' global progress required')
  value=h.decode(body);h.matches(value,h.baseline_facts(),'Intervening actual progress checkpoint: '+name)
  for key,arr in baseline.items():need(h.exact(value.get(key),arr),'Exact54/38 membership baseline: '+name)
  need(type(value.get('dated_eligible_total')) is int and value['dated_eligible_total']==99,'Dated99 baseline')
 common={**h.phase_facts(),'conditional_proposal_only':True,'UTC':utc,'phase_facts':h.phase_facts(),'new_publication_or_tracker_append_performed':False}
 case={**common,'schema':'pr218-conditional-case-status-v1','PR':218,'problem_id':'30006020',
       'scientific_disposition':ready['scientific_disposition'],'historical_priority':'See exact accepted Root priority receipt; no firstness inference by capture.'}
 progress={**common,**h.completion_memberships(),'schema':'math-draft-publication-conditional-progress-v1','dated_eligible_total':99,
  'dated_eligible_total_is_not_current_census':True,'current_PR':218,'active_publication_DOI':h.EXISTING_DOI,'active_tracker_range':h.EXISTING_TRACKER}
 result={h.VIEWS[0]:enc(case),h.VIEWS[2]:enc(progress)}
 for path in (h.VIEWS[1],h.VIEWS[4]):
  prefix=merge_prefix(local[path],native[path]);need(b'<!-- PR218_NATIVE_PHASE_FACTS' not in prefix,'Existing218 phase marker; no duplicate proposal')
  result[path]=prefix+b'\n\n'+utc.encode()+b' - Conditional PR218 adoption proposal only. Actual54/38,last214 remains the accepted baseline. Proposed55/39,last218,cursor219 requires actual Root native CAS/five/terminal; no new publication, tracker or PR action.\n\n'+h.phase_marker()+b'\n'
 result[h.VIEWS[3]]=b'# Conditional publication program progress\n\nActual baseline54 completed/38 published-or-adopted,last214; original215-217 unsolved skips remain untouched. Proposed PR21855/39,last218,cursor219 is conditional on separate actual Root terminal. Dated99 is not a current census; goal remains incomplete.\n\n'+h.phase_marker()+b'\n'
 for path in (h.VIEWS[1],h.VIEWS[3],h.VIEWS[4]):h.markdown_current(result[path],'completion100',path in (h.VIEWS[1],h.VIEWS[4]))
 return result
def selection(h,value,carry):
 need(type(value) is dict and set(value)=={'schema','PR','operational_authority','files','total_files','total_bytes'},'Exact six-key Root selection header')
 h.matches(value,{'schema':'pr218-root-positive-public-selection-v1','PR':218,'operational_authority':False},'Externally pinned Root finite selection')
 rows=value.get('files');need(type(rows) is list and 0<len(rows)<=h.MAX_FILES-5,'Bounded finite rows')
 out={}
 required={'path','origin','bytes','sha256','git_blob','observed_source_mode','role','selection_basis'}
 for row in rows:
  need(type(row) is dict and set(row)==required,'Exact positive selection row')
  path=h.rel(row['path']);h.bytepin({k:row[k] for k in ('bytes','sha256')})
  need(path not in out and path not in h.VIEWS and (h.public_path(path) or path in carry),'Selected public/carry path only, no reserved five')
  need(h.hexid(row['git_blob']) and type(row['observed_source_mode']) is int and row['observed_source_mode']==292 and all(type(row[k]) is str and row[k] for k in ('origin','role','selection_basis')),'Explicit frozen provenance/native OID/mode')
  origin=Path(row['origin']);need(origin.is_absolute() and origin.is_relative_to(CHECKOUT),'Checkout-owned explicit origin')
  if path in carry:need(h.exact({k:row[k] for k in ('bytes','sha256')},carry[path]),'Exact21 carry bytes')
  out[path]=row
 need(set(carry).issubset(out),'All21 carry files required')
 need(type(value.get('total_files')) is int and value['total_files']==len(out) and type(value.get('total_bytes')) is int and value['total_bytes']==sum(r['bytes'] for r in out.values())<=h.MAX_TOTAL,'Exact finite selected totals')
 return out
def materialize_manifest(h,payload,pre,local,stage_name,identity,evidence,identity_ref,carry_ref,carry,retired,trees,parent_root):
 need(set(h.VIEWS).issubset(payload) and len(payload)<=h.MAX_FILES and sum(map(len,payload.values()))<=h.MAX_TOTAL,'Bounded final selected+five payload')
 need(set(pre)==set(payload),'Separate complete native preimage tuples')
 for path,raw in payload.items():
  need(type(raw) is bytes and 0<=len(raw)<=h.MAX_BODY and '\0' not in raw.decode('utf-8'),'UTF8 bounded postimage')
  if path not in h.VIEWS:need(pre[path] in (None,('100644','blob',h.native('blob',raw))),'Nonview add-or-exact-noop')
 unused,changed,dirs=h.expected(h.core(),trees,parent_root,payload,pre)
 sources={};rows=[];locals=[]
 for i,(path,raw) in enumerate(sorted(payload.items())):
  relative=stage_name+'/sources/'+str(i).zfill(4)+'.txt';sources[relative]=raw
  old=pre[path];rows.append({'path':path,'source':relative,**pin(raw),'git_blob':h.native('blob',raw),'preimage':None if old is None else dict(zip(('mode','type','sha'),old))})
 for i,path in enumerate(h.VIEWS):
  raw=local[path];relative=None if raw is None else stage_name+'/local_preimages/'+str(i)+'.txt'
  if raw is not None:sources[relative]=raw
  locals.append({'path':path,'preimage':None if raw is None else pin(raw),'source':relative})
 manifest={'schema':'pr218-conditional-completion-logical-packet-v1','PR':218,'problem_id':'30006020','phase':'completion100',
  'facts':h.phase_facts(),'files':rows,'total_files':len(rows),'total_bytes':sum(map(len,payload.values())),'local_views':locals,
  'carry_inventory':carry_ref,'protected_queue':identity['_capture_queue'],'protected_queue_row_pin':identity['own_Main_QUEUE_row_pin'],
  'protected_nodes':identity['protected_nodes'],'protected_bodies':identity['protected_bodies'],'current_PR_opaque_body_pin':identity['current_PR_opaque_body_pin'],
  'expected_new_directories':sorted(dirs),'expected_changed_paths':sorted(changed),'carryforward':[{'path':path,**p} for path,p in sorted(carry.items())],
  'commit_author':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},'commit_committer':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},
  'commit_message':h.COMMIT_MESSAGE,'retired_candidates':retired,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
  'writer_lock':h.WRITER_LOCK_REFERENCE,'evidence_references':evidence,'native_identity_receipt':identity_ref}
 return manifest,sources
class GET:
 def __init__(self,h,e,journal,guard):
  self.h=h;self.e=e;self.seen_receipts=set();self.inner=e.API(h,journal,mutate=False);self.journal=journal;self.guard=guard;self.calls=0;self.wire=0;self.deadline=time.monotonic()+SECONDS;self.failed=False
 @property
 def actual_GET_origins(self):return self.inner.actual_GET_origins
 def __call__(self,method,path,body=None):
  need(not self.failed and method=='GET' and body is None and self.calls<MAX_GETS and time.monotonic()<=self.deadline,'GET-only capture count/deadline/failstop')
  self.guard();self.calls+=1
  try:
   value=self.inner('GET',path)
   number=str(self.inner.number).zfill(5);receipt=self.journal/(number+'.API_RECEIPT.json')
   hit=None
   if not receipt.exists():
    need(re.fullmatch(r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',path) is not None,'Mutable route has no successful receipt')
    raw,unused=read_regular(self.journal/(number+'.IMMUTABLE_GET_CACHE_HIT.json'));hit=self.h.decode(raw)
    need(hit['method']=='GET' and hit['path']==path and hit['request_pin'] is None and hit['canonical_cache_pin']==pin(self.e.enc(value)),'Exact same-observer canonical immutable cache hit')
    name=hit['actual_response_origin']['receipt'];need(re.fullmatch(r'[0-9]{5}\.API_RECEIPT\.json',name) is not None,'Retained successful cache origin basename');receipt=self.journal/name
   raw,unused=read_regular(receipt);r=self.h.decode(raw)
   need(r['method']=='GET' and r['path']==path and r['request_pin'] is None and r['exit']==0,'Actual successful GET receipt required')
   for key,field,cap in (('raw_stdout','stdout_pin',12_000_000),('raw_stderr','stderr_pin',65536)):
    reference=r[key];origin=Path(reference['path']);need(origin.parent==self.journal,'Actual raw origin inside this invocation journal')
    data,unused=read_regular(origin,cap=cap);need(pin(data)==r[field]=={k:reference[k] for k in ('bytes','sha256')},'Actual raw response/stdout/stderr pin')
    if key=='raw_stdout':need(self.h.exact(self.h.decode(data),value),'Returned native value differs from retained actual response')
    else:need(data==b'','Successful native GET stderr must be empty')
   if hit is not None:need(hit['actual_response_origin']['actual_stdout_pin']==r['stdout_pin'],'Cache origin actual stdout pin')
   if receipt.name not in self.seen_receipts:
    self.seen_receipts.add(receipt.name);self.wire+=r['stdout_pin']['bytes'];need(self.wire<=MAX_WIRE,'Aggregate actual GET stdout cap')
   need(time.monotonic()<=self.deadline,'Capture dispatch deadline expired');return value
  except BaseException:self.failed=True;raise
def run(args):
 source,source_identity=read_regular(Path(__file__).absolute());source_pin=pin(source)
 h=load('capture_pinned_pr218_model',ENGINE/'native218_model.py',MODEL_PIN)
 e=load('capture_pinned_pr218_primitives',ENGINE/'native218_primitives.py',PRIMITIVE_PIN);c=h.core()
 context=load('capture_pinned_native_commit_only',CONTEXT,CONTEXT_PIN)
 def supplied(name):
  key=name.replace('-','_');return {'path':getattr(args,key),'bytes':getattr(args,key+'_bytes'),'sha256':getattr(args,key+'_sha256')}
 selected_ref=supplied('selection');acceptance_ref=supplied('source-acceptance')
 selected_ref,plan_raw=file_ref(Path(selected_ref['path']),{k:selected_ref[k] for k in ('bytes','sha256')})
 acceptance_ref,acceptance_raw=file_ref(Path(acceptance_ref['path']),{k:acceptance_ref[k] for k in ('bytes','sha256')})
 own_manifest_ref,own_raw=file_ref(HERE/'SOURCE_MANIFEST.json')
 engine_ref,engine_raw=file_ref(ENGINE/'SOURCE_MANIFEST.json',ENGINE_MANIFEST_PIN)
 engine=h.decode(engine_raw);own=h.decode(own_raw)
 h.matches(own,{'schema':'pr218-logical-capture-preparation-source-manifest-v1','source_only':True,'self_excluded':True},'Capture source-only closure')
 def guard():
  need(read_regular(Path(__file__).absolute())[0]==source and file_ref(HERE/'SOURCE_MANIFEST.json')[1]==own_raw,'Own capture source/closure drift')
  need(file_ref(ENGINE/'SOURCE_MANIFEST.json',ENGINE_MANIFEST_PIN)[1]==engine_raw,'Frozen16 engine source manifest')
  for root,value in ((ENGINE,engine),(HERE,own)):
   rows=value.get('files');need(type(rows) is list and 1<=len(rows)<=20 and len({r.get('path') for r in rows})==len(rows),'Finite positive source closure')
   for row in rows:
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and Path(row['path']).name==row['path'],'Basename-only source rows')
    file_ref(root/row['path'],{k:row[k] for k in ('bytes','sha256')})
  need({'path':Path(__file__).name,**source_pin} in own['files'],'Own script positively bound')
  file_ref(CONTEXT,CONTEXT_PIN);need(file_ref(Path(acceptance_ref['path']),{k:acceptance_ref[k] for k in ('bytes','sha256')})[1]==acceptance_raw,'Root source acceptance changed')
 guard()
 acceptance=h.decode(acceptance_raw)
 h.matches(acceptance,{'schema':'pr218-root-logical-capture-source-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT_SOURCE_ONLY','PR':218,'accepted':True,
  'selection_reference':selected_ref,'capture_source_pin':source_pin,'capture_source_manifest_pin':{k:own_manifest_ref[k] for k in ('bytes','sha256')},'engine_source_manifest_pin':ENGINE_MANIFEST_PIN,
  'Root_full_source_read':True,'readonly_native_GET_and_private_conditional_staging_authorized':True,'externally_pinned_finite_selection_required':True,
  'Seed_Runtime_original_lock_actual_five_or_native_POST_authorized':False},'Separate actual Root capture source acceptance required')
 fixed={}
 for role,(name,wanted) in KNOWN.items():
  reference,raw=file_ref(CASE/name,wanted);fixed[role]=(reference,h.decode(raw))
 identity_ref,identity=fixed['identity'];ready_ref,ready=fixed['ready'];carry_ref,unused_carry=fixed['carry']
 carry=h.carry_inventory(carry_ref);need(len(carry)==21,'Exact current21 carry')
 rows=selection(h,h.decode(plan_raw),carry)
 selected={}
 def reread_selected():
  need(file_ref(Path(selected_ref['path']),{k:selected_ref[k] for k in ('bytes','sha256')})[1]==plan_raw,'Externally pinned selection drift')
  for path,row in rows.items():
   raw,unused=read_regular(Path(row['origin']));need(pin(raw)=={k:row[k] for k in ('bytes','sha256')} and h.native('blob',raw)==row['git_blob'] and '\0' not in raw.decode('utf-8'),'Selected local source bytes/mode/native pin')
   if path in selected:need(selected[path]==raw,'Selected source changed')
   else:selected[path]=raw
 reread_selected()
 evidence={**ready['evidence_references'],'case_ready':ready_ref}
 m={'native_identity_receipt':identity_ref,'protected_nodes':identity['protected_nodes'],'protected_bodies':identity['protected_bodies'],'current_PR_opaque_body_pin':identity['current_PR_opaque_body_pin']}
 h.native_identity(m);h.validate_ready_value(m,evidence,ready)
 need(len(identity['protected_nodes'])==2 and len(identity['protected_bodies'])==35,'Current accepted2nodes/35bodies')
 for reference in [identity_ref,ready_ref,carry_ref,*evidence.values(),identity['post_merge_Main_drift_extension']]:
  path=Path(reference['path']).relative_to(CHECKOUT).as_posix()
  need(path in selected and pin(selected[path])=={k:reference[k] for k in ('bytes','sha256')},'Every exact Root gate/reference body positively selected')
 for row in engine['files']:
  target=(ENGINE/row['path']).relative_to(CHECKOUT).as_posix();need(target in selected and pin(selected[target])=={k:row[k] for k in ('bytes','sha256')},'Complete frozen16 engine selected')
 target=(ENGINE/'SOURCE_MANIFEST.json').relative_to(CHECKOUT).as_posix();need(target in selected and pin(selected[target])==ENGINE_MANIFEST_PIN,'Engine manifest selected')
 need(re.fullmatch(r'private_capture218_[A-Za-z0-9_-]{1,40}',args.output_name) is not None and re.fullmatch(r'private_packet218_[A-Za-z0-9_-]{1,40}',args.stage_name) is not None,'Fresh private capture/stage names')
 need(re.fullmatch(r'ROOT_COMPLETE218_READ_CAPTURE_[A-Za-z0-9_-]{1,35}',args.journal) is not None,'Exact private GET journal namespace')
 datetime.datetime.strptime(args.UTC,'%Y-%m-%dT%H:%M:%SZ')
 retired=sorted(args.retired_candidate or []);need(len(retired)<=100 and len(retired)==len(set(retired)) and all(h.hexid(x) for x in retired),'Explicit finite retired candidate identities')
 out=HERE/args.output_name;stage=ENGINE/args.stage_name
 need(not out.exists() and not out.is_symlink() and not stage.exists() and not stage.is_symlink(),'Fresh one-use output/stage only')
 def directory(path):
  with e.ParentHandle(path) as parent:
   parent.check();os.mkdir(path.name,mode=0o700,dir_fd=parent.fd);parent.check();os.fsync(parent.fd)
 def write(root,relative,raw):
  h.rel(relative);path=root/relative;need(path.is_relative_to(root),'Owned private output')
  for parent in reversed(path.parent.parents):
   if parent==root or parent.is_relative_to(root):
    if not parent.exists():directory(parent)
  if not path.parent.exists():directory(path.parent)
  with e.ParentHandle(path) as parent:
   parent.check();fd=os.open(path.name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
   try:
    with os.fdopen(fd,'wb',closefd=False) as stream:need(stream.write(raw)==len(raw),'Full private evidence write');stream.flush();os.fchmod(fd,0o444);os.fsync(fd)
   finally:os.close(fd)
   parent.check();os.fsync(parent.fd)
 guard();directory(out);journal=e.journal_new(args.journal)
 api=GET(h,e,journal,guard);trees=c.NativeTrees(h.GetOnly(api));pool=h.NativeBodyProofs();decoded={};decoded_bytes=0
 def body(oid,wanted=None):
  nonlocal decoded_bytes
  raw=pool.get(api,oid,wanted)
  if oid not in decoded:
   need(decoded_bytes+len(raw)<=MAX_DECODED,'Aggregate decoded preimage/protected bytes');decoded[oid]=pin(raw);decoded_bytes+=len(raw)
  return raw
 def main_ref():
  value=api('GET','git/ref/heads/main');need(value.get('ref')=='refs/heads/main' and value['object']['type']=='commit' and h.hexid(value['object']['sha']),'Fresh native Main ref');return value['object']['sha']
 try:
  before=main_ref();commit=api('GET','git/commits/'+before);raw_commit=context.raw_commit(commit)
  need(commit['sha']==before and h.native('commit',raw_commit)==before,'Exact Main raw commit identity')
  root=commit['tree']['sha'];write(out,'private/native_Main.commit',raw_commit)
  pr_before=h.pr_identity(api,m,pool);body(h.CURRENT_QUEUE)
  for anchor in (h.ANCHOR,h.MERGED):
   comparison=api('GET','compare/'+anchor+'...'+before)
   need(comparison.get('status') in ('ahead','identical') and comparison['merge_base_commit']['sha']==anchor,'Fresh Main must descend from actual214 observation and existing218 merge; no CAS inference')
  targets=sorted(set(selected)|set(h.VIEWS));pre={path:trees.lookup(root,path) for path in targets}
  native={};local={};native_records={};local_records={};local_identities={}
  for index,path in enumerate(h.VIEWS):
   node=pre[path]
   if node is None:native[path]=None;native_records[path]=None
   else:
    need(node[:2]==('100644','blob'),'Ordinary native view tuple');raw=body(node[2]);native[path]=raw
    write(out,'private/native_views/'+str(index)+'.txt',raw);native_records[path]={'mode':node[0],'type':node[1],'sha':node[2],**pin(raw)}
   raw,ident=read_regular(CHECKOUT/path,absent=True);local[path]=raw;local_identities[path]=ident
   if raw is None:local_records[path]=None
   else:write(out,'private/local_views/'+str(index)+'.txt',raw);local_records[path]={'body_pin':pin(raw),'file_identity':ident}
  for path,node in identity['protected_nodes'].items():
   need(trees.lookup(root,path)==h.preserved_tuple(node,tree_only=True),'Actual fresh-parent opaque protected tuple differs')
  for row in identity['protected_bodies']:
   need(trees.lookup(root,row['path'])==h.tuple_pin({k:row[k] for k in ('mode','type','sha')}),'Native protected path association')
   body(row['sha'],{k:row[k] for k in ('bytes','sha256')})
  queue=trees.lookup(root,h.QUEUE);need(queue is not None and queue[:2]==('100644','blob'),'Whole ordinary native Main QUEUE')
  qb=body(queue[2]);own,cells=h.own_queue_row(qb)
  need(pin(own)==identity['own_Main_QUEUE_row_pin'] and cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'1/5','Exact unique Main own303byte row/status; foreign rows preserved')
  write(out,'private/QUEUE.md',qb);identity={**identity,'_capture_queue':dict(zip(('mode','type','sha'),queue))}
  views=postimages(h,ready,native,local,args.UTC);payload={**selected,**views}
  manifest,sources=materialize_manifest(h,payload,pre,local,args.stage_name,identity,evidence,identity_ref,carry_ref,carry,retired,trees,root)
  need(main_ref()==before,'Main moved during capture; no silent rebind/staging')
  guard();reread_selected()
  for path,old in local.items():
   raw,ident=read_regular(CHECKOUT/path,absent=True);need(raw==old and ident==local_identities[path],'Separate local bytes/absence/inode changed before staging')
  need(h.pr_identity(api,m,pool)==pr_before,'PR changed during logical capture')
  after=main_ref();need(after==before,'Final native Main bracket moved; no staged packet')
  directory(stage)
  for relative,raw in sources.items():
   need(relative.startswith(args.stage_name+'/'),'Explicit stage-relative source')
   write(stage,relative[len(args.stage_name)+1:],raw)
  guard();reread_selected()
  write(out,'LOGICAL_MANIFEST_01.json',enc(manifest))
  write(out,'AUTHENTICATED_TREES.json',enc(trees.cache))
  receipt={'schema':'pr218-root-readonly-logical-capture-and-conditional-construction-v1','PR':218,'evidence_scope':'ACTUAL_ROOT_READONLY_CAPTURE_PRIVATE_CONDITIONAL_STAGING_NOT_CHECKPOINT',
   'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':selected_ref,'source_acceptance':acceptance_ref,
   'capture_source_pin':source_pin,'capture_source_manifest':own_manifest_ref,'engine_source_manifest':engine_ref,
   'native_identity_receipt':identity_ref,'case_ready_receipt':ready_ref,'carry_acceptance':carry_ref,'Main_before':before,'Main_tree':root,'Main_after':after,
   'coherent_before_after_Main':True,'native_view_preimages':native_records,'separate_local_view_preimages':local_records,
   'native_preimages':manifest['files'],'whole_Main_QUEUE':{**identity['_capture_queue'],**pin(qb)},'own_Main_QUEUE_row_pin':pin(own),
   'protected_nodes_verified':2,'protected_bodies_verified':35,'unique_decoded_bytes':decoded_bytes,'GET_invocations':api.calls,'actual_stdout_bytes':api.wire,
   'private_raw_GET_journal':str(journal),'private_stage':str(stage),'logical_manifest':{'path':str(out/'LOGICAL_MANIFEST_01.json'),**pin(enc(manifest))},
   'conditional_postimage_files':manifest['total_files'],'conditional_postimage_bytes':manifest['total_bytes'],'actual_counts':{'completed':54,'published':38,'last_completed_PR':214},
   'actual_Seed_Runtime_original_lock_five_native_POST_ref_PR_provider_or_219_authority':False,
   'boundary':'Dated native/local preimage observation and conditional bytes only. No admission/lease, candidate objects, packet/source acceptance or actual completion is inferred; Root exact packet review and actual terminal remain separate.'}
  write(out,'CAPTURE_AND_CONSTRUCTION_RECEIPT_01.json',enc(receipt))
  return {'receipt':str(out/'CAPTURE_AND_CONSTRUCTION_RECEIPT_01.json'),'receipt_pin':pin(enc(receipt)),'manifest':receipt['logical_manifest'],'coherent_Main':before,'selected_files':manifest['total_files'],'actual_219_authority':False}
 except BaseException as error:
  write(out,'CAPTURE_STOPPED.json',enc({'exception':type(error).__name__,'reason':str(error),'automatic_retry':False,'no_packet_or_checkpoint_acceptance':True}));raise
def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Use Python3.11 -E -S -B -P without optimization')
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('selection','source-acceptance'):
  p.add_argument('--'+name,required=True);p.add_argument('--'+name+'-bytes',type=int,required=True);p.add_argument('--'+name+'-sha256',required=True)
 p.add_argument('--output-name',required=True);p.add_argument('--stage-name',required=True);p.add_argument('--journal',required=True);p.add_argument('--UTC',required=True);p.add_argument('--retired-candidate',action='append')
 print(json.dumps(run(p.parse_args()),sort_keys=True,indent=2))
if __name__=='__main__':main()
