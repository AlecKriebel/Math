"""PR203 bounded priority/editorial60 checkpoint. No local Git or ref mutation."""
from pathlib import Path
import datetime,importlib.util,json,sys,atexit
D=Path(__file__).resolve().parent;A=D.parent
sp=importlib.util.spec_from_file_location('math203_native_primitives',A/'science_checkpoint_01/checkpoint_math203.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
Q=v.Q;CASE=v.CASE;PREFIX=v.PREFIX;HEAD=v.HEAD
PRIOR=A/'science_checkpoint_01/math45_01'
def load():
 c,h,rv=v.load();atexit.unregister(h.m.persist_authenticated_tree_cache);return c,h,rv
def baseline(c):
 r=v.read(PRIOR/'PREPARATION.json');a=v.read(PRIOR/'ACCEPTANCE.json');x=v.read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and r['commit']==a['checkpoint_commit']=='64f6a8a8694496430bafdf58c897bc91c6a3d027'
 assert len(r['selected_files'])==a['selected_files']==3055 and r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='9c5e29b66a18e39afa0366b25306fc6406f492c3e5f7feb2a5d2d7785628ab63'
 assert v.pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file']=={'bytes':913628,'sha256':'4d5049e9d92147fded3fdd7d0d46de881ce92939a67cce7b58f2f8a1e12c9661'}
 assert x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def overlay(h,parent,stamp):
 gp=A/'ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json';assert v.pin(gp.read_bytes())=={'bytes':4472,'sha256':'eec0f861971d69968b33297b89fadb4857914d24f04bc5fbb3228d98adae98eb'};g=v.read(gp)
 assert g['bounded_priority_audit_complete'] and g['qualified_attributed_note_editorially_cleared'] and not g['historical_priority_established'] and not g['publication_ready'];out={}
 def add(rel,x=None):
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,rel;b=p.read_bytes()
  if x is not None:assert v.pin(b)==x,rel
  out[CASE+rel]=b
 add(gp.name)
 for rel,x in g['safe_files'].items():add(rel,x)
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json','LOCAL_GLOBAL_FIVE_SYNC.json']:add('science_checkpoint_01/math45_01/'+name)
 add('science_checkpoint_01/sync_actual_checkpoint.py');add('priority_checkpoint_01/checkpoint_priority203.py')
 status='BOUNDED_PRIORITY_COMPLETE_ATTRIBUTED_INCIDENCE_CURVE_NOTE_PREPARATION'
 remain='Prepare attributed incidence-curve proof note and verification package; NEW whole-package adversary/repair/fresh-independent-review loop, exact Zenodo publication/tracker, original-HEAD-safe merge and actual factual completion before204.'
 scope=g['priority_clearance_scope']
 case=json.loads(h.body_at(CASE+'CURRENT_CASE_STATUS.json',parent));assert (case['PR'],case['case_percent'],case['original_head'])==(203,45,HEAD)
 case.update(UTC=stamp,status=status,case_percent=60,priority_audit_active=False,priority_audit_complete=True,priority_clearance=True,priority_clearance_scope=scope,priority_gate=gp.name,qualified_attributed_note_editorially_cleared=True,exact_contemporary_theorem_overlap=True,theorem_novelty_cleared=False,proof_method_novelty_cleared=False,independent_discovery_certified=False,historical_novelty_or_firstness_established=False,publication_ready=False,remaining_required_steps=remain)
 out[CASE+'CURRENT_CASE_STATUS.json']=v.enc(case)
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(203,45,29,201,45)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':203,'prior_phase':45,'values':{k:z for k,z in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=60,current_workflow_estimate_percent=60,current_priority_audit_active=False,current_priority_clearance=True,current_priority_audit_complete=True,current_priority_clearance_scope=scope,current_priority_gate='audits/pr203_5100011/'+gp.name,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_exact_contemporary_theorem_overlap=True,current_theorem_novelty_cleared=False,current_proof_method_novelty_cleared=False,current_publication_ready=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,program_snapshot_semantics='PR203 scoped signed original-side every-fixed-M leastN0mod4 theorem verified. Bounded priority complete: exact Ferudun DOI23400541 TheoremA overlap, classical Steiner radial principle, Bialy-TabachnikovN4 corollary, established flag/pole methods credited. Original Oct1PR/server record precedes Oct15deposit; no firstness/independence/novelty certification. Attributed alternative presentation only.45completed/29published,last201,cursor203/advancefalse.',program_snapshot_authority_condition='Priority60 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. No publication, merge or204 authority.')
 assert not p['current_completed'] and not p['advance_to_next_PR_authorized_now'];out[PREFIX+'CURRENT_PROGRESS.json']=v.enc(p)
 note='\n'+stamp+' — PR203 priority60%: two NEW source-first priority families and Root primary-text/chronology comparison complete. Exact Ferudun DOI10.5281/zenodo.23400541 TheoremA p2 overlaps the full scoped target; original PR203 Oct1 server record and original proof match precede Oct15deposit, without historical visibility, first disclosure or independence certificate. Steiner radial principle, Bialy-Tabachnikov completeN4 implication, Schwartz-Tabachnikov/AST/Chavez flag-pole methods credited. Signed crossing centroid-degeneracy qualification retained; no historical Steiner refutation claimed. Explicit least-period theorem and false unrestricted repeated-list control preserved. Attributed incidence-curve note preparation editorially cleared under standing authorization, no theorem/method novelty. Actual publication/package reviews/tracker/merge/completion remain.45completed/29published,last201,cursor203/advancefalse; goal active.\n'
 for rel in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[rel]=h.body_at(rel,parent)+note.encode()
 return out
def selected(c,b,out):
 for k,z in out.items():
  assert k.startswith(CASE) or k in v.MUTABLE,k
  if k in b and k not in v.MUTABLE and k not in {CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md'}:assert c.byte_pin(z)==b[k],k
 assert Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out)
 return {**b,**{k:c.byte_pin(z) for k,z in out.items()}}
def message(d):return 'PR203 bounded priority60: attributed incidence-curve proof note\n\nExact contemporary theorem, classical N4 implication and established methods credited. Verified object chronology does not certify firstness or independence.45completed/29published,last201; no publication yet.\nPR203 selected-map SHA256: '+d
v.message=message
def run(c,h,rv,mode,gen):
 base=baseline(c);dest=D/gen
 if mode=='prepare':
  parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=v.queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);v.original(h)
  assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead']
  stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.mkdir();v.save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',v.enc(ack))
 else:
  r=v.read(dest/'PREPARATION.json');ack=v.read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');parent=r['expected_main'];stamp=r['UTC'];pt=r['parent_tree'];inherited={**base['selected_files'],Q:ack['current_QUEUE']}
 out=overlay(h,parent,stamp);out[CASE+'priority_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=selected(c,inherited,out)
 if mode=='prepare':
  tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':k,'mode':'100644','type':'blob','content':z.decode()} for k,z in sorted(out.items())]})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex)
  r={'UTC':stamp,'PR':203,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};v.save(dest/'PREPARATION.json',v.enc(r))
 v.verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha']
 if mode=='prepare':
  pre={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_trueparent_fullforeignscope_everyselectedidentity_verified':True,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'no_QUEUE_native_or_PR_mutation':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_firstness_independence_certified':False,'publication_ready':False,'case_percent':60};v.save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',v.enc(pre));print(json.dumps({k:r[k] for k in ['expected_main','commit','tree','selected_map_sha256']}|{'observed_main':main,'selected':len(ex),'changed':len(r['changed_paths'])}));return
 assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=v.queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);v.original(h)
 for k,z in out.items():assert c.byte_pin(z)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=v.enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});v.save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
 accepted={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':v.pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_firstness_independence_established':False,'publication_ready':False,'case_percent':60,'fully_completed_count':45,'published_count':29,'last_completed_PR':201,'next_numeric_intake_cursor':203,'advance_to_next_PR_authorized_now':False,'goal_complete':False};v.save(dest/'ACCEPTANCE.json',v.enc(accepted));print(json.dumps(accepted))
if __name__=='__main__':
 assert sys.dont_write_bytecode and not sys.flags.optimize
 c,h,rv=load();run(c,h,rv,sys.argv[1],sys.argv[2])

