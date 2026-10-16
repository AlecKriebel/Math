"""PR201 bounded-priority checkpoint. Native objects; no local Git commands."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent
f=A/'science_checkpoint_01/checkpoint_math201.py'
if hashlib.sha256(f.read_bytes()).hexdigest()!='f4399cb29e4c7a36e57c627497cb1df46b4f2bd0c615ccf8cb1fc4c1d6ee5bba':raise ValueError('math helper changed')
s=importlib.util.spec_from_file_location('prior_math201',f);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);m=v.m;Q=v.Q
PRIOR=A/'science_checkpoint_01/math45_01'
def load():
 c,h,rv=m.load();h.m.TREE_CACHE_PATH=A/'PRIORITY_PRIVATE_TREE_CACHE.json';return c,h,rv
def baseline(c):
 r=m.read(PRIOR/'PREPARATION.json');a=m.read(PRIOR/'ACCEPTANCE.json');x=m.read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and r['commit']==a['checkpoint_commit']=='c8cc8e6dbc78692c9b662926a86358c6bbdda501'
 assert len(r['selected_files'])==a['selected_files']==2307 and r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='3b56b13a34a74203aa716f1bf7846713ca15d81a5a2dc27b95e6f896812085df'
 assert m.pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file'] and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def overlay(h,parent,stamp):
 gp=A/'ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json';assert m.pin(gp.read_bytes())=={'bytes':8367,'sha256':'b0a08cc08d5362271f175ad9cd321367fb462909a67bd12bb182a8a8cb43ec4f'};g=m.read(gp)
 assert g['bounded_priority_audit_complete'] and g['qualified_attributed_note_editorially_cleared'] and g['source_contract_clearance'] and not g['publication_ready'];out={}
 def add(rel,x=None):
  f=A/rel;assert f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444;z=f.read_bytes()
  if x is not None:assert m.pin(z)==x,rel
  out[m.CASE+rel]=z
 add(gp.name)
 for rel,x in g['safe_files'].items():add(rel,x)
 for n in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json']:add('science_checkpoint_01/math45_01/'+n)
 add('priority_checkpoint_01/checkpoint_priority201.py')
 status='BOUNDED_PRIORITY_COMPLETE_ATTRIBUTED_FLAG_CURVE_NOTE_PREPARATION';remain='Prepare attributed alternative flag-curve proof note; fresh whole-package review loop, exact Zenodo publication/tracker, original-HEAD-safe integration and actual completion before202.'
 scope='Bounded priority and qualified contemporaneous alternative-proof framing only. Exact Ferudun theorem overlap credited; no theorem/method novelty, firstness or independence established.'
 case=json.loads(h.body_at(m.CASE+'CURRENT_CASE_STATUS.json',parent));assert (case['PR'],case['case_percent'],case['original_head'])==(201,45,m.HEAD)
 case.update(UTC=stamp,status=status,case_percent=60,priority_audit_active=False,priority_audit_complete=True,priority_clearance=True,priority_clearance_scope=scope,priority_gate=gp.name,qualified_attributed_note_editorially_cleared=True,exact_contemporary_theorem_overlap=True,theorem_novelty_cleared=False,proof_method_novelty_cleared=False,independent_discovery_certified=False,historical_novelty_or_firstness_established=False,publication_ready=False,remaining_required_steps=remain)
 out[m.CASE+'CURRENT_CASE_STATUS.json']=m.enc(case)
 p=json.loads(h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(201,44,28,200,45)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':201,'prior_phase':45,'values':{k:z for k,z in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=60,current_workflow_estimate_percent=60,current_priority_audit_active=False,current_priority_clearance=True,current_priority_audit_complete=True,current_priority_clearance_scope=scope,current_priority_gate='audits/pr201_5100014/'+gp.name,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_exact_contemporary_theorem_overlap=True,current_theorem_novelty_cleared=False,current_proof_method_novelty_cleared=False,current_publication_ready=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,program_snapshot_semantics='PR201 scoped signed every-M theorem verified. Exact Ferudun theorem, six formula and repeated-list caveat credited; Steiner radiality/Chavez framework and AA-prime credited. Alternative two-pole presentation only, no novelty/firstness/independence certificate.44completed/28published,last200,cursor201/advancefalse.',program_snapshot_authority_condition='Priority60 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. No publication or202 authority.')
 assert not p['current_completed'] and not p['advance_to_next_PR_authorized_now'];out[m.PREFIX+'CURRENT_PROGRESS.json']=m.enc(p)
 note='\n'+stamp+' — PR201 priority60%: three NEW distinct priority families and Root general/classical ordinary-optimized replay complete; all8pages archived Ferudunv1.0 read. Exact DOI10.5281/zenodo.23087221 theorem/formulas/caveat overlap and v1.1 DOI10.5281/zenodo.23088516 credited. Observed Oct1PRcreation precedes archive registration, without first-public-visibility or independence certificate. Steiner radiality/classical elliptic methods/Chavez AA-prime credited. Qualified alternative flag-curve proof note preparation authorized; no theorem/method novelty claim or publication yet.44completed/28published,last200,cursor201/advancefalse; goal active.\n'
 for rel in [m.CASE+'RESEARCH_LOG.md',m.PREFIX+'CURRENT_PROGRESS.md',m.PREFIX+'RESEARCH_LOG.md']:out[rel]=h.body_at(rel,parent)+note.encode()
 return out
def message(d):return 'Record PR201 bounded priority and attributed alternative-proof framing60\n\nExact contemporary theorem overlap and classical methods credited; firstness/independence unresolved. No publication yet.\nPR201 selected-map SHA256: '+d
def verify(c,h,r,ex):
 assert r['selected_files']==ex and r['selected_map_sha256']==c.selected_digest(ex);co=h.api('git/commits/'+r['commit']);assert [x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(c.selected_digest(ex));assert h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'];h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],ex)
 for k,x in ex.items():assert h.lookup(r['tree'],k)==('100644','blob',x['git_blob']),k
 changes={k for k,x in ex.items() if h.lookup(r['parent_tree'],k)!=('100644','blob',x['git_blob'])};assert changes==h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and changes<=set(r['overlay_paths']) and Q not in changes and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in changes)
def run(c,h,rv,mode,gen):
 b=baseline(c);dest=D/gen
 if mode=='prepare':
  parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=v.queue_reconcile(c,h,b,parent);pt=c.selected_current(h,parent,inherited,b['tree']);m.original(h);assert h.api('compare/'+b['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.mkdir();m.save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',m.enc(ack))
 else:
  r=m.read(dest/'PREPARATION.json');ack=m.read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');parent=r['expected_main'];stamp=r['UTC'];pt=r['parent_tree'];inherited={**b['selected_files'],Q:ack['current_QUEUE']}
 out=overlay(h,parent,stamp);out[m.CASE+'priority_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=m.selected(c,inherited,out)
 if mode=='prepare':
  tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':k,'mode':'100644','type':'blob','content':z.decode()} for k,z in sorted(out.items())]})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex);r={'UTC':stamp,'PR':201,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};m.save(dest/'PREPARATION.json',m.enc(r))
 verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha']
 if mode=='prepare':
  m.save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',m.enc({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'expected_main':parent,'observed_MAIN':main,'commit':r['commit'],'exact_trueparent_fullforeignscope_allselectedidentities_verified':True,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'case_percent':60,'publication_ready':False}));print(json.dumps({k:r[k] for k in ['expected_main','commit','tree','selected_map_sha256']}|{'observed_main':main,'selected':len(ex),'changed':len(r['changed_paths'])}));return
 assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=v.queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);m.original(h)
 for k,z in out.items():assert c.byte_pin(z)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=m.enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});m.save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body);a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':201,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':m.pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_firstness_independence_established':False,'publication_ready':False,'case_percent':60,'fully_completed_count':44,'published_count':28,'last_completed_PR':200,'next_numeric_intake_cursor':201,'advance_to_next_PR_authorized_now':False,'goal_complete':False};m.save(dest/'ACCEPTANCE.json',m.enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode;c,h,rv=load();run(c,h,rv,sys.argv[1],sys.argv[2])
