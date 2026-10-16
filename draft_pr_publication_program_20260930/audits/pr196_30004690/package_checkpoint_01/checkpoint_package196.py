"""PR196 package75; preserve exact actual parent and foreign QUEUE rows.
Ref adoption remains a separate expected-SHA connector operation.
"""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;A=D.parent
p=A/'intake_checkpoint_01/checkpoint196.py';assert hashlib.sha256(p.read_bytes()).hexdigest()=='c7e9ee0e90aad851bf8e5111bd0dd8b42b339e39dfea6ba712ba9c730c5fb9d3'
s=importlib.util.spec_from_file_location('frozen196intake',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.D=D;m.MUTABLE|={m.CASE+'CURRENT_CASE_STATUS.json',m.CASE+'RESEARCH_LOG.md'}
Q='unsolved_math_prioritization/QUEUE.md';PRIOR=A/'science_checkpoint_01/math45_01'
def baseline(c):
 r=m.read(PRIOR/'PREPARATION.json');a=m.read(PRIOR/'ACCEPTANCE.json')
 assert a['accepted'] is True and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True
 assert r['commit']==a['checkpoint_commit']=='520b11437c3a17c892c096318e0d1cdc3521af13' and len(r['selected_files'])==a['selected_files']==1552
 assert r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='924ffe9c96c3edb7ec36601b3f34a10594063a9e7f8c902db7907c4c34ae34ab'
 return r
def queue_reconcile(c,h,base,parent):
 old=h.body_at(Q,base['commit']);new=h.body_at(Q,parent);assert c.byte_pin(old)==base['selected_files'][Q]
 protected={n.split('/')[2] for n in base['selected_files'] if n.startswith('unsolved_math_prioritization/attempts/')};protected.add('30004690')
 ol=old.splitlines(keepends=True);nl=new.splitlines(keepends=True);assert len(ol)==len(nl);changes=[]
 for i,(x,y) in enumerate(zip(ol,nl)):
  if x==y:continue
  def ident(b):
   z=b.decode().split('|');assert len(z)==14 and z[1].strip().isdigit();return z[2].strip().split(' / ')[0]
  ident_old=ident(x);assert ident(y)==ident_old and ident_old not in protected
  changes.append({'one_based_line':i+1,'foreign_problem_id':ident_old,'old_line':m.pin(x),'new_line':m.pin(y)})
 assert [x for x in ol if b'| 30004690 / OWR-7155446-005 |' in x]==[x for x in nl if b'| 30004690 / OWR-7155446-005 |' in x]
 ex={**base['selected_files'],Q:c.byte_pin(new)}
 return ex,{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_actual_commit':base['commit'],'observed_actual_MAIN':parent,'scope':'Acknowledge only concurrent foreign QUEUE row bytes; no mathematical endorsement of those rows. Own overlay never writes QUEUE.','old_QUEUE':c.byte_pin(old),'current_QUEUE':c.byte_pin(new),'protected_own_native_problem_ids':sorted(protected),'foreign_changed_rows':changes,'all_other_QUEUE_bytes_identical':True,'all_protected_own_QUEUE_rows_identical':True}
def overlay(h,parent,stamp):
 out={}
 def add(rel,pin=None):
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,rel;b=p.read_bytes()
  if pin is not None:assert m.pin(b)==pin,rel
  out[m.CASE+rel]=b
 pg=m.read(A/'ROOT_PRIORITY_GATE_01.json');assert m.pin((A/'ROOT_PRIORITY_GATE_01.json').read_bytes())=={'bytes':6150,'sha256':'b0218349ce2b55f9f49cc2f4dc26707f62d6e9425c5decf3179166fa8fecbe8a'}
 qa=m.read(A/'ROOT_PACKAGE_PREPARATION_REVIEW_01.json');assert m.pin((A/'ROOT_PACKAGE_PREPARATION_REVIEW_01.json').read_bytes())=={'bytes':3844,'sha256':'3df66b02743a045784610b9ff80d5a021816b430769bb0933cef965ee0839c24'}
 assert pg['bounded_priority_audit_complete'] and pg['priority_clearance'] and not pg['historical_priority_established'] and not qa['publication_ready']
 for name in ['ROOT_PRIORITY_GATE_01.json','ROOT_PACKAGE_PREPARATION_REVIEW_01.json']:add(name)
 for n,x in pg['safe_priority_files'].items():add('priority_audit_01/'+n,x)
 for n,x in qa['package_safe_files'].items():add('publication_package_v1/'+n,x)
 for n in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json']:add('science_checkpoint_01/math45_01/'+n)
 add('package_work_01/build_package.py');add('package_checkpoint_01/checkpoint_package196.py')
 case=json.loads(h.body_at(m.CASE+'CURRENT_CASE_STATUS.json',parent));assert case['case_percent']==45 and case['original_head']==m.HEAD
 status='ATTRIBUTED_PROOF_NOTE_PACKAGE_PREPARED_FIRST_NEW_WHOLE_ADVERSARY_ACTIVE'
 remain='Finish first NEW whole-package adversarial review, repair globally, then a distinct NEW full review until clean; only then actual Zenodo upload, tracker, original-HEAD-safe merge and factual completion. Historical priority unresolved; no197 intake.'
 case.update(UTC=stamp,status=status,case_percent=75,priority_audit_complete=True,priority_audit_active=False,priority_clearance=True,priority_clearance_scope=pg['priority_clearance_scope'],historical_priority_established=False,historical_novelty_or_firstness_established=False,independent_discovery_certified=False,qualified_note_preparation_authorized=True,priority_gate='ROOT_PRIORITY_GATE_01.json',publication_ready=False,publication_package='publication_package_v1',package_safe_files=14,package_archive_entries=71,whole_publication_package_reviews_complete=False,NEW_whole_package_review_active=True,NEW_whole_package_review_names=['pr196_whole_package_adversary_01'],NEW_whole_package_reviews_completed=0,source_provenance_warning='OWR2021 already announces/sketches interior construction; this is an attributed detailed proof/application of prior contact-arc geometry, with historical priority unresolved.',remaining_required_steps=remain)
 out[m.CASE+'CURRENT_CASE_STATUS.json']=m.enc(case)
 p=json.loads(h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(196,42,26,195,45)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':196,'prior_phase':45,'values':{k:v for k,v in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=75,current_workflow_estimate_percent=75,current_priority_audit_active=False,current_priority_audit_complete=True,current_priority_clearance=True,current_priority_clearance_scope=pg['priority_clearance_scope'],current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_qualified_note_preparation_authorized=True,current_source_provenance_warning=case['source_provenance_warning'],current_priority_gate='audits/pr196_30004690/ROOT_PRIORITY_GATE_01.json',current_publication_package='audits/pr196_30004690/publication_package_v1',current_publication_ready=False,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=True,current_NEW_whole_publication_package_review_names=['pr196_whole_package_adversary_01'],current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,program_snapshot_semantics='PR196 mathematics verified; bounded18-entry/64-query priority audit complete, no exact complete predecessor found within inspected scope, historical priority unresolved. Attributed five-page proof note and71-entry authored verification archive prepared; first NEW whole-package adversary active. Prior OWR announcement and known flow/duality credited.42completed/26published,last195,cursor196/advancefalse.',program_snapshot_authority_condition='Package75 postimage effective only after actual true-parent/fullscope/all-current-selected-identities acceptance, permitting exact acknowledged foreign QUEUE rows while every own protected row is retained. No publication or merge authority.')
 assert p['current_completed'] is False and p['advance_to_next_PR_authorized_now'] is False
 out[m.PREFIX+'CURRENT_PROGRESS.json']=m.enc(p)
 note='\n'+stamp+' — PR196 package75%: three math families PASS; bounded18-entry/64-query priority audit complete. Prior OWR2021 interior announcement and Ross–Witt Nystrom contact geometry/duality credited; historical priority/firstness unresolved. Root judges detailed Green-slope/Legendre application useful as attributed proof note. Five-page PDF/source and71-entry authored-only archive sealed; built-in compile and all5page visual QA clean;3 exact scalar replays pass, scalar-only scope explicit. First NEW whole-package adversary active, no completed whole-package clearance or publication. Earlier priority60 candidates were not adopted after concurrent foreign MAIN/QUEUE updates; this combined checkpoint preserves actual foreign bytes and all protected own rows.42completed/26published,last195;cursor196/advancefalse.\n'
 for path in [m.CASE+'RESEARCH_LOG.md',m.PREFIX+'CURRENT_PROGRESS.md',m.PREFIX+'RESEARCH_LOG.md']:out[path]=h.body_at(path,parent)+note.encode()
 return out
m.message=lambda d:'Record PR196 attributed proof-note package75 and first fresh whole-package audit\n\nKnown Ross–Witt Nystrom construction and2021 interior announcement credited; historical priority unresolved.42completed/26published,last195.\nPR196 package selected-map SHA256: '+d
def prepare(c,h,gen):
 base=baseline(c);parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);m.original(h);assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(h,parent,stamp);dest=D/gen;dest.mkdir(exist_ok=False);ackpath=m.CASE+'package_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json';raw=m.enc(ack);m.save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',raw);out[ackpath]=raw;ex=m.selected(c,inherited,out);entries=[]
 for name,b in sorted(out.items()):
  e={'path':name,'mode':'100644','type':'blob'}
  if name.endswith(('.pdf','.zip')):
   sha=h.api('git/blobs','POST',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha'];assert sha==c.byte_pin(b)['git_blob'];e['sha']=sha
  else:e['content']=b.decode()
  entries.append(e)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':m.message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex)
 r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(n for n,x in ex.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};m.save(dest/'PREPARATION.json',m.enc(r));m.verify(c,h,r,ex);assert Q not in r['changed_paths'] and not any(n.startswith('unsolved_math_prioritization/attempts/') for n in r['changed_paths']);observed=h.api('git/ref/heads/main')['object']['sha'];j={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':co,'expected_main':parent,'MAIN_observed_before_adoption':observed,'sole_parent_full_tree_scope_every_selected_identity_verified':True,'all_inherited_protected_rows_retained':True,'foreign_QUEUE_reconciliation':m.pin(raw),'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'publication_ready':False,'case_percent':75};m.save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',m.enc(j));print(json.dumps({'Root_pre_move_verified':True,'expected_main':parent,'observed_main':observed,'commit':co,'tree':tree,'selected':len(ex),'changed':len(r['changed_paths']),'selected_map_sha256':r['selected_map_sha256']}))
def accept(c,h,gen):
 base=baseline(c);dest=D/gen;r=m.read(dest/'PREPARATION.json');ack=m.read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out=overlay(h,r['expected_main'],r['UTC']);out[m.CASE+'package_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=m.selected(c,inherited,out);m.verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);m.original(h)
 for n,b in out.items():assert c.byte_pin(b)==ex[n] and h.lookup(tree,n)==('100644','blob',ex[n]['git_blob'])
 mapbody=m.enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});m.save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',mapbody)
 receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':196,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':m.pin(mapbody),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_and_native_untouched_by_own_checkpoint':True,'exact_foreign_QUEUE_acknowledgement_if_changed':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':True,'priority_clearance_scope':'Bounded audit and attributed proof/application note; historical priority unresolved.','historical_priority_established':False,'publication_ready':False,'case_percent':75,'fully_completed_count':42,'published_count':26,'last_completed_PR':195,'next_numeric_intake_cursor':196,'advance_to_next_PR_authorized_now':False,'goal_complete':False};m.save(dest/'ACCEPTANCE.json',m.enc(receipt));print(json.dumps(receipt))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h=m.load();h.m.TREE_CACHE_PATH=A/'PACKAGE_PRIVATE_TREE_CACHE.json';{'prepare':prepare,'accept':accept}[sys.argv[1]](c,h,sys.argv[2])
