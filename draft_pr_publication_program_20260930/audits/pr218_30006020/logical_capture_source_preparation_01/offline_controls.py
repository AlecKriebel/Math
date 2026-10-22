"""Pure and owned synthetic capture-source controls; never run capture or real API."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,types,tempfile,time
HERE=Path(__file__).absolute().parent
def main():
 def module(path,name):
  m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
 s=module(HERE/'capture_logical_packet.py','inactive_capture')
 h=module(s.ENGINE/'native218_model.py','pure_model')
 c=h.core();checks=[]
 def yes(value,label):s.need(value,label);checks.append(label)
 def no(fn,label):
  try:fn()
  except (RuntimeError,ValueError,KeyError,TypeError,FileNotFoundError):checks.append(label);return
  raise RuntimeError('Accepted negative '+label)
 baseline={**h.baseline_facts(),**h.source_baseline(),'dated_eligible_total':99}
 native={path:None for path in h.VIEWS};local=dict(native)
 native[h.VIEWS[2]]=local[h.VIEWS[2]]=s.enc(baseline)
 native[h.VIEWS[4]]=b'old native\n';local[h.VIEWS[4]]=b'old native\nlocal append'
 ready={'scientific_disposition':'Synthetic qualification only'}
 images=s.postimages(h,ready,native,local,'2026-10-18T01:30:00Z')
 yes(images[h.VIEWS[4]].startswith(local[h.VIEWS[4]]) and h.phase_marker() in images[h.VIEWS[4]],'separate_log_prefix_longer_preserved_and_final_marker')
 yes(h.decode(images[h.VIEWS[2]])['fully_completed_count']==55 and h.decode(images[h.VIEWS[2]])['conditional_proposal_only'] is True,'conditional55_39_not_actual_authority')
 yes(h.decode(images[h.VIEWS[2]])['fully_completed_eligible_PRs']==h.source_baseline()['fully_completed_eligible_PRs']+[218],'only218_added_no_skips')
 for a,b in [(b'left',b'right'),(b'',1)]:no(lambda a=a,b=b:s.merge_prefix(a,b),'divergent_or_typed_log_prefix')
 bad=copy.deepcopy(local);bad[h.VIEWS[2]]=s.enc({**baseline,'last_completed_PR':218})
 no(lambda:s.postimages(h,ready,native,bad,'2026-10-18T01:30:00Z'),'intervening_ascending_checkpoint_refused')
 bad=copy.deepcopy(local);bad[h.VIEWS[2]]=s.enc({**baseline,'fully_completed_count':54.0})
 no(lambda:s.postimages(h,ready,native,bad,'2026-10-18T01:30:00Z'),'float_baseline_refused')
 bad=copy.deepcopy(local);bad[h.VIEWS[4]]=h.phase_marker()
 no(lambda:s.postimages(h,ready,native,bad,'2026-10-18T01:30:00Z'),'existing_case_marker_refused')
 row={'path':h.CASE+'summary.md','origin':str(HERE/'synthetic_summary.md'),'bytes':0,'sha256':hashlib.sha256(b'').hexdigest(),'git_blob':h.native('blob',b''),'observed_source_mode':292,'role':'owned authored synthetic','selection_basis':'explicit Root-positive synthetic'}
 plan={'schema':'pr218-root-positive-public-selection-v1','PR':218,'operational_authority':False,'files':[row],'total_files':1,'total_bytes':0}
 yes(len(s.selection(h,plan,{}))==1,'exact_six_header_eight_row_keys_int292_empty_text_supported')
 for mode in ('0444',292.0,True,420):
  v=copy.deepcopy(plan);v['files'][0]['observed_source_mode']=mode
  no(lambda v=v:s.selection(h,v,{}),'non_exact_mode_'+repr(mode))
 for field,value in [('extra','not permitted'),('PR',218.0),('operational_authority',True),('total_files',1.0)]:
  no(lambda field=field,value=value:s.selection(h,{**plan,field:value},{}),'header_or_type_'+field)
 for path in [h.VIEWS[0],h.CASE+'ROOT_COMPLETE218_READ_X/raw.json',h.CASE+'private/evidence.txt',h.PROGRAM+'foreign.md']:
  v=copy.deepcopy(plan);v['files'][0]['path']=path
  no(lambda v=v:s.selection(h,v,{}),'forbidden_selection_'+path)
 no(lambda:s.selection(h,plan,{h.CASE+'required.json':{'bytes':1,'sha256':'a'*64}}),'missing_positive_carry_refused')
 node={'mode':'040000','type':'tree','sha':'a'*40}
 yes(h.preserved_tuple(node,tree_only=True)==('040000','tree','a'*40),'actual_opaque_tree_uses_tree_validator')
 no(lambda:h.tuple_pin(node),'regular_preimage_helper_rejects_tree')
 objects={}
 def tree(flat):
  trie={}
  for path,item in flat.items():
   n=trie
   for part in path.split('/')[:-1]:n=n.setdefault(part,{})
   n[path.split('/')[-1]]=item
  def walk(n):
   rows=[(name,'040000','tree',walk(item)) if type(item) is dict else (name,*item) for name,item in n.items()]
   rows.sort(key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''));oid=c.tree_hash(rows)
   objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':name,'mode':mode,'type':kind,'sha':sha} for name,mode,kind,sha in rows]};return oid
  return walk(trie)
 flat={h.VIEWS[2]:('100644','blob',h.native('blob',native[h.VIEWS[2]])),'foreign-symlink':('120000','blob','b'*40)}
 root=tree(flat);ts=c.NativeTrees(lambda method,path:copy.deepcopy(objects[path.rsplit('/',1)[1]]))
 payload={**images,row['path']:b''};pre={path:ts.lookup(root,path) for path in payload}
 identity={'_capture_queue':{'mode':'100644','type':'blob','sha':'c'*40},'own_Main_QUEUE_row_pin':s.pin(b'row'),'protected_nodes':{},'protected_bodies':[],'current_PR_opaque_body_pin':s.pin(b'opaque')}
 ref={'path':str(HERE/'synthetic-ref.json'),'bytes':2,'sha256':hashlib.sha256(b'{}').hexdigest()}
 manifest,sources=s.materialize_manifest(h,payload,pre,local,'private_packet218_TEST',identity,{},ref,ref,{},[],ts,root)
 yes(len(manifest['files'])==6 and manifest['facts']==h.phase_facts() and manifest['carry_inventory']==ref,'pure_manifest_exact_model_keys_and_zero_body')
 yes(all(r['source'].startswith('private_packet218_TEST/') for r in manifest['files']) and len(manifest['local_views'])==5,'private_staging_schedule_and_separate_local_five')
 badpre=dict(pre);badpre[row['path']]=('100644','blob','d'*40)
 no(lambda:s.materialize_manifest(h,payload,badpre,local,'private_packet218_TEST',identity,{},ref,ref,{},[],ts,root),'different_existing_nonview_never_overwritten')
 with tempfile.TemporaryDirectory(prefix='_synthetic_capture_controls_',dir=HERE) as temp:
  journal=Path(temp)
  def put(name,data):
   p=journal/name;p.write_bytes(data);p.chmod(0o444);return {'path':str(p),**s.pin(data)}
  class FakeAPI:
   def __init__(self,mode='valid'):self.number=0;self.calls=0;self.mode=mode;self.actual_GET_origins={}
   def __call__(self,method,path):
    self.calls+=1;self.number+=1;num=str(self.number).zfill(5);value={'sha':'a'*40,'scope':'OWNED_SYNTHETIC'}
    if self.mode=='missing':return value
    if self.number==1:
     out=put(num+'.RAW_STDOUT.json',s.enc(value));err=put(num+'.RAW_STDERR.txt',b'')
     r={'method':'GET','path':path,'request_pin':None,'exit':0,'stdout_pin':s.pin(s.enc(value)),'stderr_pin':s.pin(b''),'raw_stdout':out,'raw_stderr':err}
     put(num+'.API_RECEIPT.json',s.enc(r));self.original=r
    else:
     hit={'method':'GET','path':path,'request_pin':None,'canonical_cache_pin':s.pin(s.enc(value)),'actual_response_origin':{'receipt':'00001.API_RECEIPT.json','actual_stdout_pin':self.original['stdout_pin']}}
     if self.mode=='bad_cache':hit['canonical_cache_pin']=s.pin(b'wrong')
     put(num+'.IMMUTABLE_GET_CACHE_HIT.json',s.enc(hit))
    return value
  def wrapper(mode='valid',guard=lambda:None):
   g=s.GET.__new__(s.GET);g.h=h;g.e=types.SimpleNamespace(enc=s.enc);g.seen_receipts=set();g.inner=FakeAPI(mode);g.journal=journal;g.guard=guard;g.calls=0;g.wire=0;g.deadline=time.monotonic()+300;g.failed=False;return g
  g=wrapper();g('GET','git/commits/'+'a'*40);wire=g.wire;g('GET','git/commits/'+'a'*40)
  yes(g.calls==2 and g.wire==wire and len(g.seen_receipts)==1,'valid_current_invocation_cache_hit_preserves_origin_no_double_wire')
  # Use fresh synthetic number ranges/directories to avoid accidental fixture reuse.
  g=wrapper('missing');g.inner.number=90
  no(lambda:g('GET','git/commits/'+'a'*40),'unknown_missing_receipt_and_cache_hit_refused')
  yes(g.failed and g.inner.calls==1,'failed_observer_no_hidden_success')
  no(lambda:g('GET','git/commits/'+'a'*40),'failed_observer_cannot_redispatch')
  g=wrapper('missing');g.inner.number=95;g.calls=s.MAX_GETS
  no(lambda:g('GET','git/commits/'+'a'*40),'aggregate250_cap_before_dispatch');yes(g.inner.calls==0,'count_cap_no_underlying_call')
  g=wrapper('missing');g.deadline=time.monotonic()-1
  no(lambda:g('GET','git/commits/'+'a'*40),'overall_deadline_before_dispatch')
  g=wrapper('missing');no(lambda:g('POST','git/commits'),'no_POST_before_dispatch');yes(g.inner.calls==0,'POST_no_underlying_call')
  def revoke():raise RuntimeError('synthetic source gate revoked')
  g=wrapper('missing',revoke);no(lambda:g('GET','git/commits/'+'a'*40),'source_guard_before_API');yes(g.inner.calls==0,'revoked_gate_no_underlying_call')
 raw=(HERE/'capture_logical_packet.py').read_bytes();t=ast.parse(raw)
 gate_dicts=[n for n in ast.walk(t) if isinstance(n,ast.Dict) and any(isinstance(k,ast.Constant) and k.value=='selection_reference' for k in n.keys)]
 yes(any(any(isinstance(k,ast.Constant) and k.value=='selection_reference' and isinstance(v,ast.Name) and v.id=='selected_ref' for k,v in zip(n.keys,n.values)) for n in gate_dicts),'actual_source_gate_binds_exact_CLI_selection_reference')
 expected={'selection_reference':ref}
 h.matches(expected,expected,'synthetic exact selection gate')
 yes(True,'exact_selection_gate_reference_accepts')
 for key,value in [('path',str(HERE/'different.json')),('bytes',2.0),('sha256','f'*64)]:
  bad=copy.deepcopy(expected);bad['selection_reference'][key]=value
  no(lambda bad=bad:h.matches(bad,expected,'pinned selection differs'),'selection_gate_rejects_'+key)
 yes(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('Seed','Runtime','WriterLock','candidate','sync','hold_CAS') for n in ast.walk(t)),'no_Seed_Runtime_original_lock_or_ops_constructor')
 yes(s.MAX_GETS==250 and s.MAX_DECODED==32000000 and s.MAX_WIRE==64000000,'fixed_bounded_capture_caps')
 return {'schema':'pr218-logical-capture-owned-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'PURE_AND_OWNED_SYNTHETIC_ONLY','checks':len(checks),'all_passed':True,'controls':checks,'capture_source_pin':s.pin(raw),'actual_capture_API_Seed_Runtime_original_lock_five_or_other_ops_executed':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))

