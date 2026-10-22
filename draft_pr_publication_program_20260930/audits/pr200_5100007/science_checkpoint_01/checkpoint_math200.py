"""PR200 mathematics checkpoint. No local Git commands or ref changes."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent
f=A/'intake_checkpoint_01/checkpoint200.py'
assert hashlib.sha256(f.read_bytes()).hexdigest()=='21f273177819087abd0da1bf3a219f3f23302fb77a98e366817b02a142ef1be1'
sp=importlib.util.spec_from_file_location('frozen200intake',f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
m.D=D;m.MUTABLE|={m.CASE+'CURRENT_CASE_STATUS.json',m.CASE+'RESEARCH_LOG.md'}
PRIOR=A/'intake_checkpoint_01/intake15_01';Q='unsolved_math_prioritization/QUEUE.md'
def baseline(c):
 r=m.read(PRIOR/'PREPARATION.json');a=m.read(PRIOR/'ACCEPTANCE.json');x=m.read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit']=='dbc32c6009c06b1cccfb8d123ebbf0decc2f02b2'
 assert len(r['selected_files'])==a['selected_files']==1701 and r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='b120c57fb39e09203f71cac95f738a49b0d3169ccbf87ba372e7849c4ef2718e'
 assert m.pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file'] and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def queue_reconcile(c,h,base,parent):
 old=h.body_at(Q,base['commit']);new=h.body_at(Q,parent);assert c.byte_pin(old)==base['selected_files'][Q]
 protected={n.split('/')[2] for n in base['selected_files'] if n.startswith('unsolved_math_prioritization/attempts/')};protected.add('5100007');ol=old.splitlines(keepends=True);nl=new.splitlines(keepends=True);assert len(ol)==len(nl);changes=[]
 for i,(x,y) in enumerate(zip(ol,nl)):
  if x==y:continue
  def ident(b):
   z=b.decode().split('|');assert len(z)==14 and z[1].strip().isdigit();return z[2].strip().split(' / ')[0]
  pid=ident(x);assert ident(y)==pid and pid not in protected;changes.append({'one_based_line':i+1,'foreign_problem_id':pid,'old_line':m.pin(x),'new_line':m.pin(y)})
 assert [x for x in ol if b'| 5100007 / AMR-050-0007 |' in x]==[x for x in nl if b'| 5100007 / AMR-050-0007 |' in x]
 return {**base['selected_files'],Q:c.byte_pin(new)},{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_actual_commit':base['commit'],'observed_actual_MAIN':parent,'scope':'Only authenticate concurrent foreign QUEUE bytes; no mathematical endorsement. Own checkpoint never writes QUEUE.','old_QUEUE':c.byte_pin(old),'current_QUEUE':c.byte_pin(new),'protected_own_native_problem_ids':sorted(protected),'foreign_changed_rows':changes,'all_other_QUEUE_bytes_identical':True,'all_protected_own_QUEUE_rows_identical':True}
def gate():
 g=m.read(A/'ROOT_MATHEMATICAL_GATE_01.json');assert g['PR']==200 and g['original_head']==m.HEAD and g['mathematical_clearance'] and g['source_contract_clearance'] and g['Root_all_family_reports_code_derivations_read'] and g['Root_reproductions_completed'] and len(g['three_NEW_independent_audit_families'])==3 and g['priority_clearance'] is False and g['publication_ready'] is False;return g

def overlay(h,parent,stamp):
 g=gate();out={}
 def add(rel,x=None):
  assert not rel.startswith('/') and '..' not in Path(rel).parts;f=A/rel;assert f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444,rel;b=f.read_bytes()
  if x is not None:assert m.pin(b)==x,rel
  out[m.CASE+rel]=b
 add('ROOT_MATHEMATICAL_GATE_01.json')
 for rel,x in g['safe_files'].items():add(rel,x)
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json']:add('intake_checkpoint_01/intake15_01/'+name)
 add('science_checkpoint_01/checkpoint_math200.py')
 case=json.loads(h.body_at(m.CASE+'CURRENT_CASE_STATUS.json',parent));assert (case['PR'],case['case_percent'],case['original_head'])==(200,15,m.HEAD)
 status='MATHEMATICS_AND_LITERAL_SOURCE_CLEARED_DEEP_PRIORITY_ACTIVE';remain='Deep bounded priority audit of exactk115 and general Poncelet/elliptic-function results; determine precise attributed contribution before any manuscript. No publication,merge or201 intake clearance.'
 warning='Literal arxivv11 and published Table2p345 match k115 for primitiveN divisibleby4 within nested confocalellipses. Repeating an excluded primitive orbit can fail. Stachel printed dn-shift sign error observed in both versions; correct DLMF identity used. Historical tables do not establish currentworldopenness.'
 case.update(UTC=stamp,status=status,case_percent=45,mathematical_clearance=True,mathematical_result_valid=True,source_contract_clearance=True,independent_mathematical_families_active=False,independent_mathematical_families_complete=3,mathematical_gate='ROOT_MATHEMATICAL_GATE_01.json',priority_audit_active=True,priority_audit_complete=False,priority_clearance=False,historical_novelty_or_firstness_established=False,publication_ready=False,source_provenance_warning=warning,remaining_required_steps=remain)
 out[m.CASE+'CURRENT_CASE_STATUS.json']=m.enc(case)
 p=json.loads(h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(200,43,27,196,15)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':200,'prior_phase':15,'values':{k:v for k,v in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=45,current_workflow_estimate_percent=45,current_mathematical_clearance=True,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_source_contract_clearance=True,current_source_provenance_warning=warning,current_independent_mathematical_audit_active=False,current_independent_mathematical_audit_families_complete=3,current_mathematical_gate='audits/pr200_5100007/ROOT_MATHEMATICAL_GATE_01.json',current_priority_audit_active=True,current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_publication_ready=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,program_snapshot_semantics='PR200 exact primitiveperiodk115 mathematics/source cleared after three NEW independent families and Root proof/primary/code/reproduction checks; allperiod divisor proof supplies universality. Deep priority active, historicalfirstness unresolved.43completed/27published,last196,cursor200/advancefalse.',program_snapshot_authority_condition='Math45 postimage takes effect only after actual trueparent/fullforeignscope/everyselectedidentity acceptance; no priority,publication,merge or201intake authority.')
 assert p['current_completed'] is False and p['advance_to_next_PR_authorized_now'] is False
 out[m.PREFIX+'CURRENT_PROGRESS.json']=m.enc(p)
 note='\n'+stamp+' — PR200 math45%: three NEW independent geometry/directonefocus, exactalgebra/directphysicalorbit reproduction and literalsource/quantifier families verified. Root read complete reports/derivations/code and reproduced controls; original19 archive unchanged. PrimitiveNdiv4 and nestedconfocalellipses essential; inadmissible covers fail. Exact compacttorus divisor cancellation proves alladmissibleperiods, ordinarypositivefocalproducts equal. Historical table proofgap and printed source dn-sign discrepancy explicitly qualified. Deep priority starts, no firstness/publication clearance.43completed/27published,last196,cursor200/advancefalse; broader goal active.\n'
 for rel in [m.CASE+'RESEARCH_LOG.md',m.PREFIX+'CURRENT_PROGRESS.md',m.PREFIX+'RESEARCH_LOG.md']:out[rel]=h.body_at(rel,parent)+note.encode()
 return out
m.overlay=overlay
m.message=lambda d:'Record PR200 exact k115 mathematics/source clearance45; deep priority active\n\nPrimitive Ndiv4, nested confocal ellipses, stars and N4 exception verified.43completed/27published,last196; no publication clearance.\nPR200 mathematical selected-map SHA256: '+d

def prepare(c,h,rv,gen):
 base=baseline(c);parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);m.original(h);assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(h,parent,stamp);dest=D/gen;dest.mkdir();raw=m.enc(ack);m.save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',raw);out[m.CASE+'science_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=raw;ex=m.selected(c,inherited,out)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':k,'mode':'100644','type':'blob','content':b.decode()} for k,b in sorted(out.items())]})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':m.message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex);r={'UTC':stamp,'PR':200,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};m.save(dest/'PREPARATION.json',m.enc(r));m.verify(c,h,r,ex);assert Q not in r['changed_paths'] and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in r['changed_paths']);observed=h.api('git/ref/heads/main')['object']['sha'];pre={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':co,'expected_main':parent,'observed_MAIN':observed,'exact_trueparent_fullforeignscope_allselectedidentities_verified':True,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':False,'publication_ready':False,'case_percent':45};m.save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',m.enc(pre));print(json.dumps({'expected_main':parent,'observed_main':observed,'commit':co,'tree':tree,'selected':len(ex),'changed':len(r['changed_paths'])}))
def accept(c,h,rv,gen):
 base=baseline(c);dest=D/gen;r=m.read(dest/'PREPARATION.json');ack=m.read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out=overlay(h,r['expected_main'],r['UTC']);out[m.CASE+'science_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=m.selected(c,inherited,out);m.verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);m.original(h)
 for k,b in out.items():assert c.byte_pin(b)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=m.enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});m.save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body);a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':200,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':m.pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':False,'priority_audit_active':True,'publication_ready':False,'case_percent':45,'fully_completed_count':43,'published_count':27,'last_completed_PR':196,'next_numeric_intake_cursor':200,'advance_to_next_PR_authorized_now':False,'goal_complete':False};m.save(dest/'ACCEPTANCE.json',m.enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h,rv=m.load();h.m.TREE_CACHE_PATH=A/'MATH_PRIVATE_TREE_CACHE.json';{'prepare':prepare,'accept':accept}[sys.argv[1]](c,h,rv,sys.argv[2])
