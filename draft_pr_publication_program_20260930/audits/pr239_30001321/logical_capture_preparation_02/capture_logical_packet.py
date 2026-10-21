"""Inactive PR239 GET-only factual capture then offline conditional finalization.
No actual source/gate/snapshot/Seed/Runtime/project-lock/native effect occurs on import.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,stat,sys,time,types
HERE=Path(__file__).absolute().parent
CASE=HERE.parent
PROGRAM=CASE.parents[1]
CHECKOUT=PROGRAM.parent
ENGINE=CASE/'operational_source_preparation_01'
ENGINE_MANIFEST_PIN={'bytes': 3198, 'sha256': '96b0b248f390f67860b435b57cde34b2d2142206b9fc5c8166417f9c98d0db6c'}
MODEL_PIN={'bytes': 51455, 'sha256': 'b6e4ea626d0f63aa6c01c8c923d0afdcb810ef629feb2b3dfd15dc3a1613e64e'}
PRIMITIVE_PIN={'bytes': 16405, 'sha256': '5d3d3072c7a9a95c640ecfbafef466cac50c83ce433b9d57024f772a2cb84d27'}
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


def helpers():
 h=load('capture_pinned_pr239_model',ENGINE/'native239_model.py',MODEL_PIN)
 e=load('capture_pinned_pr239_primitives',ENGINE/'native239_primitives.py',PRIMITIVE_PIN)
 return h,e,h.core()
def raw_commit(j):
 """Preserve exact signed folding, including a final empty signature line."""
 oid=j['sha'];root=j['tree']['sha'];parents=[p['sha'] for p in j['parents']]
 need(hexid(oid) and hexid(root) and 1<=len(parents)<=2 and all(hexid(p) for p in parents),'Native commit identities')
 verification=j.get('verification',{});payload=verification.get('payload');signature=verification.get('signature')
 def checked(raw):
  header=raw.split(b'\n\n',1)[0].split(b'\n')
  need(header[0]==('tree '+root).encode() and [v[7:].decode() for v in header if v.startswith(b'parent ')]==parents,'Raw tree/ordered parents vs metadata')
  need(native('commit',raw)==oid,'Exact complete raw commit SHA1');return raw
 if type(payload) is str and type(signature) is str:
  head,body=payload.encode().split(b'\n\n',1)
  return checked(head+b'\ngpgsig '+b'\n '.join(signature.encode().split(b'\n'))+b'\n\n'+body)
 need(verification.get('reason')=='unsigned' and payload is None and signature is None,'Unsupported native signed encoding')
 def who(meta,offset):
  stamp=int(datetime.datetime.fromisoformat(meta['date'].replace('Z','+00:00')).timestamp())
  a=abs(offset);zone=('+' if offset>=0 else '-')+str(a//60).zfill(2)+str(a%60).zfill(2)
  return (meta['name']+' <'+meta['email']+'> '+str(stamp)+' '+zone).encode()
 prefix=('tree '+root+'\n'+''.join('parent '+p+'\n' for p in parents)).encode()
 offsets=[0,-420,420]+[n for n in range(-840,841,15) if n not in (0,-420,420)]
 for a,c in [(n,n) for n in offsets]+[(a,c) for a in offsets for c in offsets if a!=c]:
  header=prefix+b'author '+who(j['author'],a)+b'\ncommitter '+who(j['committer'],c)+b'\n\n'
  for message in (j['message'],j['message']+'\n'):
   raw=header+message.encode()
   if native('commit',raw)==oid:return checked(raw)
 raise RuntimeError('Unsupported commit encoding; no guessed authentication')
def hexid(value):return type(value) is str and re.fullmatch('[0-9a-f]{40}',value) is not None
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def required_carry(h):return h.decode(h.sealed('CARRY_REQUIRED.json',h.CARRY_PIN))
def selection(h,value,phase,final=False):
 need(type(value) is dict and set(value)=={'schema','PR','operational_authority','files','total_files','total_bytes'},'Exact six-key finite selection')
 h.matches(value,{'schema':'pr239-root-positive-public-selection-v1','PR':239,'operational_authority':False},'Root finite selection')
 rows=value['files'];need(type(rows) is list and 0<len(rows)<=h.MAX_FILES-5,'Finite selected rows')
 out={};carry=required_carry(h);inventory=h.original_archives()
 for row in rows:
  need(type(row) is dict and set(row)=={'path','origin','bytes','sha256','git_blob','observed_source_mode','role','selection_basis'},'Exact selected source/target row')
  path=h.rel(row['path']);h.bytepin({k:row[k] for k in ('bytes','sha256')})
  allowed=h.public_path(path) or path in carry or h.carry_path(path) or (phase=='merge95' and h.science_path(path))
  need(allowed and path not in h.VIEWS and path!=h.QUEUE and path not in out,'Finite public/required carry/science only; no generated views/QUEUE')
  need(hexid(row['git_blob']) and type(row['observed_source_mode']) is int and row['observed_source_mode']==292
       and all(type(row[k]) is str and row[k] for k in ('origin','role','selection_basis')),'Exact source mode/native/provenance')
  origin=Path(row['origin']);need(origin.is_absolute() and origin.is_relative_to(CHECKOUT),'Explicit checkout-owned origin')
  if path in carry:need(h.exact({k:row[k] for k in ('bytes','sha256')},carry[path]),'Exact required carry')
  if path in inventory:
   source=inventory[path];need(row['git_blob']==source['native_blob'] and h.exact({k:row[k] for k in ('bytes','sha256')},{k:source[k] for k in ('bytes','sha256')}),'Exact original archive source')
  out[path]=row
 need(set(carry).issubset(out) and set(inventory).issubset(out),'All24 required carry and32 original archives selected')
 if phase=='merge95':
  for r in h.submitted_inventory():
   need(r['repository_path'] in out and out[r['repository_path']]['git_blob']==r['native_blob']
        and h.exact({k:out[r['repository_path']][k] for k in ('bytes','sha256')},{k:r[k] for k in ('bytes','sha256')}),'All32 exact attempt transplant rows')
 need(type(value['total_files']) is int and value['total_files']==len(out) and type(value['total_bytes']) is int
      and value['total_bytes']==sum(r['bytes'] for r in out.values())<=h.MAX_TOTAL,'Bounded exact selected totals')
 return out
def selected_bodies(h,rows):
 out={}
 for path,row in rows.items():
  raw,unused=read_regular(Path(row['origin']))
  need(pin(raw)=={k:row[k] for k in ('bytes','sha256')} and native('blob',raw)==row['git_blob'] and '\0' not in raw.decode('utf-8'),'Exact canonical0444 selected UTF8 body')
  out[path]=raw
 return out
def queue_postimage(h,before,own_post,phase):
 old,cells=h.own_queue_row(before)
 if phase=='completion100':
  need(own_post is None and cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'3/5','100 wholeQUEUE unchanged/claimed3of5')
  return before,old,old
 need(type(own_post) is bytes,'Root-supplied own postrow bytes required')
 row,after=h.own_queue_row(own_post)
 need(row==own_post and after[8].strip()==b'claimed_solved' and after[9].strip()==b'3/5','Single canonical exact own claimed3of5 row')
 lines=before.splitlines(keepends=True);need(lines.count(old)==1,'Unique own pre-row')
 result=b''.join(row if x==old else x for x in lines)
 h.queue_transition(before,result,{'phase':phase,'queue_pre_row_pin':pin(old),'protected_queue_row_pin':pin(row)})
 return result,old,row
def postimages(h,evidence,phase,native_views,local,utc):
 for label,body in (('native',native_views[h.VIEWS[2]]),('local',local[h.VIEWS[2]])):
  need(type(body) is bytes,label+' global progress is required')
  value=h.decode(body);h.matches(value,h.baseline_facts(phase),'Exact actual baseline counters/cursor '+label)
  for key,arr in h.source_baseline().items():need(h.exact(value.get(key),arr),'Exact baseline55/39 memberships '+label)
  need(type(value.get('dated_eligible_total')) is int and value['dated_eligible_total']==99,'Dated99 baseline')
 pub=h.publication_identity({'evidence_references':evidence})
 common={**h.phase_facts(phase),'conditional_proposal_only':True,'UTC':utc,'capture_performed_native_checkpoint':False,
  'actual_new_publication_receipt':evidence['publication'],'actual_tracker_receipt':evidence['tracker'],
  'actual_publication_DOI':pub['doi'],'actual_tracker_range':pub['range']}
 case={**common,'schema':'pr239-conditional-case-status-v1','PR':239,'problem_id':'30001321'}
 progress={**common,**h.phase_memberships(phase),'schema':'math-draft-publication-conditional-progress-v1',
  'dated_eligible_total':99,'dated_eligible_total_is_not_current_census':True,'current_PR':239}
 result={h.VIEWS[0]:enc(case),h.VIEWS[2]:enc(progress)}
 if phase=='merge95':
  text=b'Conditional PR239 merge95 proposal: actual cumulative55/39,last218 is retained; real new publication/tracker event receipts are separate. This capture performs no native checkpoint or numeric advance.'
 else:
  text=b'Conditional PR239 completion100 proposal:56/40,last239,cursor240 requires actual separate Root terminal. This capture performs no checkpoint and authorizes no240 intake.'
 for path in (h.VIEWS[1],h.VIEWS[4]):
  prefix=merge_prefix(local[path],native_views[path])
  if phase=='merge95':need(b'<!-- PR239_NATIVE_PHASE_FACTS' not in prefix,'Existing95/100 marker; do not duplicate capture proposal')
  else:h.markdown_current(prefix,'merge95',True)
  result[path]=prefix+b'\n\n'+utc.encode()+b' - '+text+b'\n\n'+h.phase_marker(phase)+b'\n'
 result[h.VIEWS[3]]=b'# Conditional publication program progress\n\n'+text+b' Dated99 is not a current census; goal remains incomplete.\n\n'+h.phase_marker(phase)+b'\n'
 for path in (h.VIEWS[1],h.VIEWS[3],h.VIEWS[4]):h.markdown_current(result[path],phase,path in (h.VIEWS[1],h.VIEWS[4]))
 return result
class Output:
 """Only new private capture/stage descendants; no arbitrary current-file writer."""
 def __init__(self,h,e,path,kind):
  root=HERE if kind=='capture' else ENGINE
  pattern='private_capture239_' if kind=='capture' else 'private_packet239_'
  need(path.parent==root and re.fullmatch(pattern+'[A-Za-z0-9_-]{1,40}',path.name) is not None,'Exact private owned output')
  need(not path.exists() and not path.is_symlink(),'One-use output directory must be absent')
  self.h,self.e,self.path=h,e,path;self.directory(path)
 def directory(self,path):
  with self.e.ParentHandle(path) as parent:
   parent.check();os.mkdir(path.name,mode=0o700,dir_fd=parent.fd);parent.check();os.fsync(parent.fd)
 def write(self,name,raw):
  self.h.rel(name);path=self.path/name
  need(path.is_relative_to(self.path) and type(raw) is bytes and len(raw)<=MAX_DECODED,'Owned bounded exact bytes')
  current=self.path
  for part in Path(name).parts[:-1]:
   current=current/part
   if not current.exists():self.directory(current)
  with self.e.ParentHandle(path) as parent:
   parent.check();fd=os.open(path.name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
   try:
    with os.fdopen(fd,'wb',closefd=False) as f:
     need(f.write(raw)==len(raw),'Full owned write');f.flush();os.fchmod(fd,0o444);os.fsync(fd)
   finally:os.close(fd)
   parent.check();os.fsync(parent.fd)
  return {'path':str(path),**pin(raw)}
 def json(self,name,value):return self.write(name,enc(value))
def source_guard(h,config_ref,selection_ref,acceptance_ref,action):
 source,unused=read_regular(Path(__file__).absolute())
 own_ref,own_raw=file_ref(HERE/'SOURCE_MANIFEST.json');engine_ref,engine_raw=file_ref(ENGINE/'SOURCE_MANIFEST.json',ENGINE_MANIFEST_PIN)
 config_ref,config_raw=file_ref(Path(config_ref['path']),{k:config_ref[k] for k in ('bytes','sha256')})
 selection_ref,selection_raw=file_ref(Path(selection_ref['path']),{k:selection_ref[k] for k in ('bytes','sha256')})
 acceptance_ref,acceptance_raw=file_ref(Path(acceptance_ref['path']),{k:acceptance_ref[k] for k in ('bytes','sha256')})
 h.matches(h.decode(acceptance_raw),{'schema':'pr239-root-logical-capture-source-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT_SOURCE_ONLY',
  'PR':239,'accepted':True,'action':action,'configuration_reference':config_ref,'selection_reference':selection_ref,
  'capture_source_pin':pin(source),'capture_source_manifest_pin':pin(own_raw),'engine_source_manifest_pin':ENGINE_MANIFEST_PIN,
  'Root_full_source_read':True,'independent_source_review_accepted':True,'only_readonly_capture_or_offline_conditional_staging_authorized':True,
  'Seed_Runtime_original_lock_actual_five_native_POST_ref_PR_provider_or_intake_authorized':False},'Separate exact Root source/config/selection acceptance')
 def guard():
  need(read_regular(Path(__file__).absolute())[0]==source and file_ref(HERE/'SOURCE_MANIFEST.json')[1]==own_raw,'Own immutable capture source closure')
  for root,raw,schema in ((HERE,own_raw,'pr239-logical-capture-source-manifest-v1'),(ENGINE,engine_raw,'pr239-completion-source-manifest-v1')):
   need(file_ref(root/'SOURCE_MANIFEST.json')[1]==raw,'Exact source manifest drift')
   value=h.decode(raw);h.matches(value,{'schema':schema,'source_only':True,'self_excluded':True},'Finite source closure')
   rows=value['files'];need(type(rows) is list and 1<=len(rows)<=20 and len({r.get('path') for r in rows})==len(rows),'Finite source rows')
   for row in rows:
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and Path(row['path']).name==row['path'],'Exact basename source closure')
    file_ref(root/row['path'],{k:row[k] for k in ('bytes','sha256')})
  need({'path':Path(__file__).name,**pin(source)} in h.decode(own_raw)['files'],'Capture source missing')
  for r,raw in ((config_ref,config_raw),(selection_ref,selection_raw),(acceptance_ref,acceptance_raw)):
   need(file_ref(Path(r['path']),{k:r[k] for k in ('bytes','sha256')})[1]==raw,'Exact Root-bound input drift')
 guard()
 return h.decode(config_raw),h.decode(selection_raw),guard,{'source':pin(source),'source_manifest':own_ref,'engine_manifest':engine_ref,
  'config':config_ref,'selection':selection_ref,'source_acceptance':acceptance_ref}
def capture(config,plan,h,e,c,guard,bindings):
 need(type(config) is dict and set(config)=={'schema','PR','phase','output_name','journal','evidence_references','own_row_post',
  'protected_body_paths','deferred_targets','retired_candidates'},'Exact factual capture configuration')
 h.matches(config,{'schema':'pr239-readonly-factual-capture-config-v1','PR':239},'Capture config')
 phase=config['phase'];h.phase_facts(phase)
 evidence=config['evidence_references'];need(type(evidence) is dict and set(evidence)==h.evidence_roles(phase)-{'case_ready'},'Precreated actual event/science/merge refs; no fabricated case-ready')
 for r in evidence.values():h.root_ref(r)
 m={'phase':phase,'evidence_references':evidence,'current_PR_opaque_body_pin':h.root_ref(evidence['ready'])['final_body_pin']}
 h.publication_identity(m)
 if phase=='completion100':h.merge_identity(m)
 rows=selection(h,plan,phase);selected=selected_bodies(h,rows)
 for r in evidence.values():
  path=Path(r['path']).relative_to(CHECKOUT).as_posix()
  need(path in selected and pin(selected[path])=={k:r[k] for k in ('bytes','sha256')},'Exact actual event/science evidence positively selected')
 deferred=config['deferred_targets']
 need(type(deferred) is dict and {'native_identity','case_ready','carry_inventory'}.issubset(deferred) and len(deferred)<=40,'Finite explicitly named future public target roles')
 need(len(set(deferred.values()))==len(deferred),'Distinct future receipt targets')
 for key,path in deferred.items():
  need(type(key) is str and key and type(path) is str and h.public_path(path) and path not in selected and path not in h.VIEWS,'Explicit safe deferred public target, not source permission')
 paths=config['protected_body_paths']
 need(type(paths) is list and paths==sorted(set(paths)) and len(paths)<=64
      and all(type(p) is str and (p.startswith(h.ATTEMPT+'/') or p.startswith(h.SHARED+'/')) for p in paths),'Finite own protected paths')
 retired=config['retired_candidates'];need(type(retired) is list and retired==sorted(set(retired)) and len(retired)<=100 and all(hexid(x) for x in retired),'Finite retired candidate list')
 need(type(config['journal']) is str and re.fullmatch('ROOT_COMPLETE239_READ_CAPTURE_[A-Za-z0-9_-]{1,35}',config['journal']) is not None,'Exact bounded GET namespace')
 need(len(rows)+len(deferred)+5+(1 if phase=='merge95' else 0)<=h.MAX_FILES,'Finite captured targets including deferred/five/QUEUE')
 out=Output(h,e,HERE/config['output_name'],'capture');guard();journal=e.journal_new(config['journal'])
 api=GET(h,e,journal,guard);trees=c.NativeTrees(h.GetOnly(api));pool=h.NativeBodyProofs();seen={};decoded=0
 def body(oid,wanted=None):
  nonlocal decoded
  raw=pool.get(api,oid,wanted)
  if oid not in seen:
   need(decoded+len(raw)<=MAX_DECODED,'Aggregate native decoded cap');seen[oid]=pin(raw);decoded+=len(raw)
  return raw
 def main_ref():
  value=api('GET','git/ref/heads/main')
  need(value.get('ref')=='refs/heads/main' and value['object']['type']=='commit' and hexid(value['object']['sha']),'Actual Main ref')
  return value['object']['sha']
 def commit(oid,label):
  value=api('GET','git/commits/'+oid);raw=raw_commit(value)
  need(value['sha']==oid and native('commit',raw)==oid,'Canonical native immutable commit')
  return {'sha':oid,'tree':value['tree']['sha'],'parents':[x['sha'] for x in value['parents']],'raw_commit':out.write('private/commits/'+label+'.commit',raw)}
 try:
  utc=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
  before=main_ref();parent=commit(before,'Main');root=parent['tree']
  if before!=h.ANCHOR:
   comp=api('GET','compare/'+h.ANCHOR+'...'+before)
   need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==h.ANCHOR,'Actual218 terminal ancestry; no CAS inference')
  base=commit(h.SUBMITTED_BASE,'submitted_base');chain=[];prior=h.SUBMITTED_BASE
  for index,oid in enumerate(h.SUBMITTED_CHAIN):
   item=commit(oid,'submitted_'+str(index));need(item['parents']==[prior],'Exact full four-commit submitted linear chain');chain.append(item);prior=oid
  need(chain[-1]['tree']==h.CURRENT_TREE and chain[-1]['parents']==[h.ORIGINAL_PARENT],'Exact H root/sole parent')
  need(trees.lookup(base['tree'],h.ATTEMPT) is None,'Attempt absent before first submitted commit')
  leaves,dirs,deleted=trees.changes(base['tree'],h.CURRENT_TREE)
  need(leaves==set([h.QUEUE]+[r['repository_path'] for r in h.submitted_inventory()]) and not deleted,'Complete33-path submitted scope/no foreign leaf')
  fullscope={'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'deleted_directories':[]}
  inventory_records=[]
  for r in h.submitted_inventory():
   need(trees.lookup(h.CURRENT_TREE,r['repository_path'])==('100644','blob',r['native_blob']),'All32 original native path/mode associations')
   raw=body(r['native_blob'],{k:r[k] for k in ('bytes','sha256')})
   inventory_records.append({'path':r['repository_path'],**pin(raw),'git_blob':r['native_blob'],'actual_origin':pool.origin(api,r['native_blob'])})
  oldqueue=trees.lookup(base['tree'],h.QUEUE);currentqueue=trees.lookup(h.CURRENT_TREE,h.QUEUE)
  need(oldqueue is not None and oldqueue[:2]==('100644','blob') and currentqueue==('100644','blob',h.CURRENT_QUEUE),'Original base/H wholeQUEUE native associations')
  bq=body(oldqueue[2]);hq=body(currentqueue[2]);base_row,base_cells=h.own_queue_row(bq);head_row,head_cells=h.own_queue_row(hq)
  need(pin(base_row)==h.SUBMITTED_BASE_ROW and base_cells[8].strip()==b'queued' and base_cells[9].strip()==b'0/5'
       and pin(head_row)==h.CURRENT_ROW and head_cells[8].strip()==b'claimed_solved' and head_cells[9].strip()==b'3/5','Original eligibility/native row evidence')
  need([x for x in bq.splitlines(keepends=True) if x!=base_row]==[x for x in hq.splitlines(keepends=True) if x!=head_row],'Whole submitted QUEUE foreign bytes preserved')
  out.write('private/submitted_base_QUEUE.md',bq);out.write('private/submitted_H_QUEUE.md',hq)
  full_ref={'path':str(CASE/'root_full_submitted_scope_01/ROOT_COMPLETE_SUBMITTED_SCOPE.json'),**h.FULL_SCOPE_PIN};h.root_ref(full_ref)
  pr_before=h.validate_pr_metadata(api('GET','pulls/239'),m)
  if phase=='completion100':
   merge=h.merge_identity(m);merged=commit(merge['merge_candidate'],'merge95')
   need(merged['tree']==merge['merge_tree'] and merged['parents']==merge['ordered_parents'],'Actual C1 native root/ordered P,H parents')
   comp=api('GET','compare/'+merged['sha']+'...'+before)
   need((before==merged['sha'] and comp.get('status')=='identical') or (comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==merged['sha']),'100 parent descends from actual Root C1')
  nodes={p:trees.lookup(root,p) for p in (h.ATTEMPT,h.SHARED)}
  for node in nodes.values():h.preserved_tuple(None if node is None else dict(zip(('mode','type','sha'),node)),True)
  if phase=='completion100':
   need(nodes[h.ATTEMPT] is not None and trees.lookup(merged['tree'],h.ATTEMPT)==nodes[h.ATTEMPT],'100 own science attempt unchanged from actual C1; fresh old-audit stays opaque')
  queue=trees.lookup(root,h.QUEUE);need(queue is not None and queue[:2]==('100644','blob'),'Ordinary Main wholeQUEUE')
  qb=body(queue[2]);out.write('private/Main_QUEUE.md',qb)
  own_post=None
  if config['own_row_post'] is not None:
   r=config['own_row_post'];need(type(r) is dict and set(r)=={'path','bytes','sha256'},'Exact own row reference')
   own_post=file_ref(Path(r['path']),h.bytepin({k:r[k] for k in ('bytes','sha256')}))[1]
  if config['own_row_post'] is not None:need(pin(own_post)=={k:config['own_row_post'][k] for k in ('bytes','sha256')},'Externally pinned own postrow')
  queue_after,own_before,own_after=queue_postimage(h,qb,own_post,phase)
  targets=sorted(set(rows)|set(h.VIEWS)|set(deferred.values())|({h.QUEUE} if phase=='merge95' else set()))
  pre={p:trees.lookup(root,p) for p in targets};native_views={};local={};native_refs={};local_refs={};identities={}
  for i,p in enumerate(h.VIEWS):
   item=pre[p]
   if item is None:native_views[p]=None;native_refs[p]=None
   else:
    need(item[:2]==('100644','blob'),'Ordinary native view')
    raw=body(item[2]);native_views[p]=raw;native_refs[p]=out.write('private/native_views/'+str(i)+'.txt',raw)
   raw,ident=read_regular(CHECKOUT/p,absent=True);local[p]=raw;identities[p]=ident
   local_refs[p]=None if raw is None else out.write('private/local_views/'+str(i)+'.txt',raw)
  protected=[]
  for p in paths:
   item=trees.lookup(root,p);need(item is not None and item[:2]==('100644','blob'),'Existing protected own regular blob')
   raw=body(item[2]);protected.append({'path':p,'mode':item[0],'type':item[1],'sha':item[2],**pin(raw)})
  views=postimages(h,evidence,phase,native_views,local,utc)
  payload={**selected,**views}
  if phase=='merge95':payload[h.QUEUE]=queue_after
  for p,raw in payload.items():
   if p not in h.VIEWS and p!=h.QUEUE:need(pre[p] in (None,('100644','blob',native('blob',raw))),'Nonview add-or-exact-noop; conflicting own state requires Root decision')
  need(len(targets)<=h.MAX_FILES and sum(map(len,payload.values()))<=h.MAX_TOTAL,'Reserved finite target/body bounds')
  expected,changed,newdirs=h.expected(c,trees,root,payload,{p:pre[p] for p in payload})
  post_attempt=projected_attempt(h,c,trees,root,payload,pre)
  protected_nodes={p:None if node is None else dict(zip(('mode','type','sha'),node)) for p,node in nodes.items()}
  guard();need(selected_bodies(h,rows)==selected,'Selected source drift')
  for p,raw in local.items():
   now,ident=read_regular(CHECKOUT/p,absent=True);need(now==raw and ident==identities[p],'Separate local bytes/absence/inode changed')
  need(h.exact(h.validate_pr_metadata(api('GET','pulls/239'),m),pr_before),'PR changed during factual capture')
  after=main_ref();need(after==before,'Main changed; no silent retry/rebind or successful summary')
  observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
  for i,(p,raw) in enumerate(sorted(payload.items())):out.write('private/postimages/'+str(i).zfill(4)+'.txt',raw)
  selected_refs={p:{'path':str(out.path/'private/postimages'/str(i).zfill(4))+'.txt',**pin(raw)} for i,(p,raw) in enumerate(sorted(payload.items()))}
  tree_ref=out.json('private/AUTHENTICATED_TREES.json',trees.cache)
  summary={'schema':'pr239-factual-logical-capture-v1','PR':239,'phase':phase,'evidence_scope':'DATED_GET_AND_LOCAL_PREIMAGES_NOT_ROOT_ACCEPTANCE',
   'capture_UTC':utc,'native_final_ref_UTC':observed_utc,'end_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bindings':bindings,'coherent_before_after_Main':True,
   'Main_before':before,'Main_after':after,'parent_commit':parent,'submitted_base_commit':base,'submitted_commit_chain':chain,
   'original_commit':chain[-1],'original_parent_commit':chain[-2],'submitted_base_queue':dict(zip(('mode','type','sha'),oldqueue)),
   'full_submitted_scope_reference':full_ref,'submitted_scope':fullscope,'original32_native_bodies':inventory_records,
   'protected_nodes':protected_nodes,'post_attempt_tree':dict(zip(('mode','type','sha'),post_attempt)),'protected_bodies':protected,
   'protected_queue':dict(zip(('mode','type','sha'),queue)),'queue_postimage':{'mode':'100644','type':'blob','sha':native('blob',queue_after)},
   'queue_pre_row_pin':pin(own_before),'protected_queue_row_pin':pin(own_after),'current_PR_opaque_body_pin':m['current_PR_opaque_body_pin'],
   'native_preimages':{p:None if item is None else dict(zip(('mode','type','sha'),item)) for p,item in pre.items()},
   'native_view_body_references':native_refs,'separate_local_view_references':local_refs,'separate_local_view_identities':identities,
   'known_postimage_references':selected_refs,'deferred_targets':deferred,'science_allowlist':[{'path':p,**pin(raw)} for p,raw in sorted(payload.items()) if h.science_path(p)],
   'evidence_references':evidence,'authenticated_trees':tree_ref,'retired_candidates':retired,'native_QUEUE_body_pin':pin(qb),
   'conditional_facts':h.phase_facts(phase),'actual_membership_baseline':h.source_baseline(),'initial_projected_tree':expected,
   'initial_changed_paths':sorted(changed),'initial_new_directories':sorted(newdirs),'GET_invocations':api.calls,'actual_stdout_bytes':api.wire,'unique_decoded_bytes':decoded,
   'private_raw_GET_journal':str(journal),'Root_acceptance_candidate_CAS_sync_completion_or_numeric_advance_inferred':False}
  guard()
  return out.json('FACTUAL_CAPTURE_SUMMARY.json',summary)
 except BaseException as error:
  out.json('CAPTURE_STOPPED.json',{'exception':type(error).__name__,'reason':str(error),'automatic_retry':False,'successful_summary_or_checkpoint_authority':False});raise
def projected_attempt(h,c,trees,root,payload,pre):
 """Reuse the frozen exact-preimage rebuild for the own subtree, no POST."""
 node=trees.lookup(root,h.ATTEMPT);need(node is None or node[:2]==('040000','tree'),'Own attempt tree/absence')
 own={p[len(h.ATTEMPT)+1:]:raw for p,raw in payload.items() if p.startswith(h.ATTEMPT+'/')}
 if not own:return node
 own_pre={p[len(h.ATTEMPT)+1:]:pre[p] for p in payload if p.startswith(h.ATTEMPT+'/')}
 oid,unused,unused_dirs=h.expected(c,trees,None if node is None else node[2],own,own_pre)
 return ('040000','tree',oid)
def authenticated_tree_replay(h,c,saved):
 need(type(saved) is dict and len(saved)<=c.MAX_ENTRIES,'Bounded authenticated immediate-tree inventory')
 def tree_get(method,route,body=None):
  need(method=='GET' and body is None and re.fullmatch('git/trees/[0-9a-f]{40}',route) is not None,'Offline authenticated immediate-tree replay only')
  oid=route.rsplit('/',1)[1];need(oid in saved,'Missing authenticated capture tree')
  entries=saved[oid];need(type(entries) is dict,'Exact authenticated immediate-tree cache')
  values=[{'path':name,'mode':item[0],'type':item[1],'sha':item[2]} for name,item in entries.items()]
  values.sort(key=lambda row:row['path'].encode()+(b'/' if row['mode']=='040000' else b''))
  return {'sha':oid,'truncated':False,'tree':values}
 return c.NativeTrees(tree_get)
def final_target_admissibility(h,payload,carry,science,phase):
 """Match frozen load_inputs target policy using the actual accepted carry."""
 h.phase_facts(phase)
 need(type(payload) is dict and type(carry) is dict and set(carry).issubset(payload),'All accepted carry selected')
 need(type(science) is list and len(science)<=200,'Finite actual science allowlist')
 sc={}
 for row in science:
  need(type(row) is dict and set(row)=={'path','bytes','sha256'} and h.science_path(row['path'])
       and row['path'] not in sc,'Exact unique own science target')
  sc[row['path']]=h.bytepin({k:row[k] for k in ('bytes','sha256')})
 need(phase=='merge95' or not sc,'Completion100 cannot select science')
 for path,raw in payload.items():
  h.rel(path)
  need(path in h.VIEWS or h.public_path(path) or path in carry or path in sc
       or (path==h.QUEUE and phase=='merge95'),'Target outside actual Root public/carry/science scope')
  if path in carry:need(h.exact(pin(raw),h.bytepin(carry[path])),'Actual carry body differs')
  if path in sc:need(h.exact(pin(raw),sc[path]),'Actual science body differs')
def finalize(config,plan,h,e,c,guard,bindings):
 need(type(config) is dict and set(config)=={'schema','PR','snapshot','stage_name','native_identity','case_ready','carry_inventory'},'Exact offline finalize config')
 h.matches(config,{'schema':'pr239-offline-logical-finalize-config-v1','PR':239},'Offline finalize')
 snapshot=h.root_ref(config['snapshot']);phase=snapshot['phase'];h.phase_facts(phase)
 h.matches(snapshot,{'schema':'pr239-factual-logical-capture-v1','PR':239,'coherent_before_after_Main':True,
  'Root_acceptance_candidate_CAS_sync_completion_or_numeric_advance_inferred':False},'Successful actual factual capture required')
 need(snapshot['Main_before']==snapshot['Main_after']==snapshot['parent_commit']['sha'],'Closed factual parent bracket')
 rows=selection(h,plan,phase,True);selected=selected_bodies(h,rows)
 captured=set(snapshot['native_preimages']);deferred=snapshot['deferred_targets']
 need(set(rows)==(set(snapshot['known_postimage_references'])-set(h.VIEWS)-{h.QUEUE})|set(deferred.values()),'Exact captured known+deferred targets only')
 for role in ('native_identity','case_ready','carry_inventory'):
  reference=config[role];target=Path(reference['path']).relative_to(CHECKOUT).as_posix()
  need(target==deferred[role] and target in selected and pin(selected[target])=={k:reference[k] for k in ('bytes','sha256')},'Actual Root future receipt at its reserved exact natural target')
 evidence={**snapshot['evidence_references'],'case_ready':config['case_ready']}
 payload=dict(selected)
 for p,r in snapshot['known_postimage_references'].items():
  raw=file_ref(Path(r['path']),{k:r[k] for k in ('bytes','sha256')})[1]
  if p in h.VIEWS or p==h.QUEUE:payload[p]=raw
  else:need(payload[p]==raw,'Known selected source changed after capture')
 pre={p:h.tuple_pin(snapshot['native_preimages'][p]) for p in payload}
 need(set(payload)==captured and len(payload)<=h.MAX_FILES and sum(map(len,payload.values()))<=h.MAX_TOTAL,'Exact complete captured target universe and payload bounds')
 local={}
 for p,r in snapshot['separate_local_view_references'].items():local[p]=None if r is None else file_ref(Path(r['path']),{k:r[k] for k in ('bytes','sha256')})[1]
 carry=h.carry_inventory(config['carry_inventory'])
 final_target_admissibility(h,payload,carry,snapshot['science_allowlist'],phase)
 m={'phase':phase,'facts':h.phase_facts(phase),'native_identity_receipt':config['native_identity'],'evidence_references':evidence,
  **{k:snapshot[k] for k in ('protected_nodes','post_attempt_tree','protected_bodies','protected_queue','queue_postimage','queue_pre_row_pin','protected_queue_row_pin','current_PR_opaque_body_pin','science_allowlist')}}
 identity=h.native_identity(m);h.validate_ready_value(m,evidence,h.root_ref(config['case_ready']))
 def same_commit(left,right):
  for k in ('sha','tree','parents'):need(h.exact(left[k],right[k]),'Exact captured native commit identity')
  need(h.exact({k:left['raw_commit'][k] for k in ('bytes','sha256')},{k:right['raw_commit'][k] for k in ('bytes','sha256')}),'Exact raw captured commit bytes; public alias may differ')
 for key in ('submitted_base_commit','original_commit','original_parent_commit'):same_commit(identity[key],snapshot[key])
 need(len(identity['submitted_commit_chain'])==len(snapshot['submitted_commit_chain'])==4,'Captured four commits')
 for left,right in zip(identity['submitted_commit_chain'],snapshot['submitted_commit_chain']):same_commit(left,right)
 for key in ('submitted_base_queue','full_submitted_scope_reference','submitted_scope'):
  need(h.exact(identity[key],snapshot[key]),'Actual Root native receipt must bind exact captured original history')
 # Replay only authenticated immutable tree envelopes; never a transport/cache from another run.
 trees_raw=file_ref(Path(snapshot['authenticated_trees']['path']),{k:snapshot['authenticated_trees'][k] for k in ('bytes','sha256')})[1]
 saved=h.decode(trees_raw)
 trees=authenticated_tree_replay(h,c,saved);root=snapshot['parent_commit']['tree']
 expected,changed,dirs=h.expected(c,trees,root,payload,pre)
 need(projected_attempt(h,c,trees,root,payload,pre)==h.preserved_tuple(m['post_attempt_tree'],True),'Final projected attempt identity')
 for p,raw in payload.items():
  need(type(raw) is bytes and len(raw)<=h.MAX_BODY and '\0' not in raw.decode('utf-8'),'Finite UTF8 logical postimage')
  if p not in h.VIEWS and p!=h.QUEUE:need(pre[p] in (None,('100644','blob',native('blob',raw))),'Nonview add-or-exact-noop')
 guard();need(selected_bodies(h,rows)==selected,'Final selected bytes drift')
 out=Output(h,e,ENGINE/config['stage_name'],'stage');files=[];locals=[]
 for i,(p,raw) in enumerate(sorted(payload.items())):
  name='sources/'+str(i).zfill(4)+'.txt';out.write(name,raw)
  files.append({'path':p,'source':out.path.name+'/'+name,**pin(raw),'git_blob':native('blob',raw),
    'preimage':snapshot['native_preimages'][p]})
 for i,p in enumerate(h.VIEWS):
  raw=local[p];name=None if raw is None else 'local_preimages/'+str(i)+'.txt'
  if name is not None:out.write(name,raw)
  locals.append({'path':p,'preimage':None if raw is None else pin(raw),'source':None if name is None else out.path.name+'/'+name})
 manifest={'schema':'pr239-conditional-publication-logical-packet-v1','PR':239,'problem_id':'30001321',**m,
  'files':files,'total_files':len(files),'total_bytes':sum(map(len,payload.values())),'local_views':locals,
  'carry_inventory':config['carry_inventory'],'expected_new_directories':sorted(dirs),'expected_changed_paths':sorted(changed),
  'carryforward':[{'path':p,**wanted} for p,wanted in sorted(carry.items())],
  'commit_author':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},'commit_committer':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},
  'commit_message':h.commit_message(phase),'retired_candidates':snapshot['retired_candidates'],'body_proof_policy':h.BODY_POLICY,
  'QUEUE_policy':h.QUEUE_POLICY,'writer_lock':h.WRITER_LOCK_REFERENCE}
 guard();need(selected_bodies(h,rows)==selected,'Selection drift after private staging')
 manifest_ref=out.json('LOGICAL_MANIFEST.json',manifest)
 receipt={'schema':'pr239-offline-conditional-packet-construction-v1','PR':239,'phase':phase,'bindings':bindings,'snapshot':config['snapshot'],
  'manifest':manifest_ref,'projected_tree':expected,'conditional_facts':h.phase_facts(phase),
  'actual_Root_logical_acceptance_or_checkpoint_or_numeric_advance':False,
  'boundary':'Exact captured dated parent/preimages plus later actual Root evidence and conditional bytes. No fresh Main lease, Seed/Runtime, candidate, CAS, sync or terminal is performed.'}
 return out.json('CONDITIONAL_CONSTRUCTION_RECEIPT.json',receipt)
def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Use Python3.11 -E -S -B -P without optimization')
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('capture','finalize'))
 for name in ('config','selection','source-acceptance'):
  p.add_argument('--'+name,required=True);p.add_argument('--'+name+'-bytes',type=int,required=True);p.add_argument('--'+name+'-sha256',required=True)
 args=p.parse_args()
 def supplied(name):
  k=name.replace('-','_');return {'path':getattr(args,k),'bytes':getattr(args,k+'_bytes'),'sha256':getattr(args,k+'_sha256')}
 h,e,c=helpers()
 config,plan,guard,bindings=source_guard(h,supplied('config'),supplied('selection'),supplied('source-acceptance'),args.action)
 result=capture(config,plan,h,e,c,guard,bindings) if args.action=='capture' else finalize(config,plan,h,e,c,guard,bindings)
 print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
