"""Specific PR195 integration/completion. No ref moves or PR mutations here.
Each phase binds actual prior receipts, exact current parent, full leaf delta,
and every inherited identity. Root separately adopts and accepts each phase.
"""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr195_30004601/'
NATIVE='unsolved_math_prioritization/attempts/30004601/';QUEUE='unsolved_math_prioritization/QUEUE.md';HEAD='e776a961293116775fed2cb2a3019d577b84c04a'
PHASES={'merge':('publication_checkpoint_01/ready90_01','publication_ready',95),'factual':('publication_lifecycle_01/merge01','actual_merge_accepted',98),'completion':('publication_lifecycle_01/factual01','actual_factual_accepted',100)}
MUTABLE={CASE+x for x in ['CURRENT_CASE_STATUS.json','RESEARCH_LOG.md']}|{PREFIX+x for x in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}|{QUEUE}
def read(p):return json.loads(p.read_bytes())
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 path=A/'publication_checkpoint_01/checkpoint_ready195.py';assert pin(path.read_bytes())=={'bytes':10460,'sha256':'f9aee59266d54eb7ec0154f18c49efcbc7e2b95e6267090dde7b92ab9a88129a'}
 sp=importlib.util.spec_from_file_location('approved195ready',path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);v,c,h=m.load();h.m.TREE_CACHE_PATH=A/'LIFECYCLE_PRIVATE_TREE_CACHE.json'
 p=A/'native_publication_preparation_01/make_native.py';assert pin(p.read_bytes())=={'bytes':13953,'sha256':'4196af19cd19eaf1786c2695f8e6c91ecbc2db9de32910a07d80ac975d26f0d8'}
 sp=importlib.util.spec_from_file_location('pure195native',p);n=importlib.util.module_from_spec(sp);sp.loader.exec_module(n);return c,h,n

def base(c,phase):
 directory=A/PHASES[phase][0];r=read(directory/'PREPARATION.json');a=read(directory/'ACCEPTANCE.json')
 assert a['accepted'] is True and a['checkpoint_commit']==r['commit'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True
 assert a['selected_files']==len(r['selected_files']) and a['selected_map_sha256']==r['selected_map_sha256']==c.selected_digest(r['selected_files'])
 if phase=='merge':assert r['commit']=='6795078453531794226bcf63e314f1a1f9063f77' and len(r['selected_files'])==1446
 else:assert a[PHASES[phase][1]] is True and a['original_head']==HEAD
 return r,a

def facts(stamp,phase):
 gate=read(A/'ROOT_PUBLICATION_GATE_01.json');pub=read(A/'ROOT_PUBLICATION_RECEIPT.json');tracker=read(A/'ROOT_TRACKER_RECEIPT.json')
 assert gate['publication_ready_gate_accepted'] is True and gate['historical_priority_established'] is False
 assert pub['state']=='published' and pub['actual_publication_verified'] is True and pub['metadata_exact_verified'] is True and pub['doi']=='10.5281/zenodo.23395703' and pub['id']==23395703
 assert pub['gate_sha256']==tracker['gate_sha256']==pin((A/'ROOT_PUBLICATION_GATE_01.json').read_bytes())['sha256']
 assert tracker['actual_tracker_row_verified'] is True and tracker['own_row_readback_verified'] is True and tracker['foreign_rows_retained'] is True and tracker['doi']==pub['doi'] and tracker['range']=="'Math Puzzles'!A110:D110"
 for name,x in gate['package_safe_files'].items():assert pin((A/'publication_package_v2'/name).read_bytes())==x
 assert {x['name']:{'bytes':x['size'],'sha256':x['sha256']} for x in pub['files']}==gate['intended_upload_files']
 f={'UTC':stamp,'publication_ready_gate_accepted':True,'DOI':pub['doi'],'record_id':pub['id'],'actual_publication_verified':True,'actual_tracker_row_verified':True,'package':'publication_package_v2','whole_package_review_events':gate['whole_package_review_events'],'historical_priority_established':False,'tracker_range':tracker['range']}
 if phase!='merge':f['actual_merge_receipt']=read(A/'publication_lifecycle_01/merge01/ACCEPTANCE.json')
 if phase=='completion':f['actual_factual_receipt']=read(A/'publication_lifecycle_01/factual01/ACCEPTANCE.json')
 return f

def queue(old,doi):
 lines=old.decode().splitlines(keepends=True);own=[i for i,x in enumerate(lines) if '| 30004601 / OWR-4990374-004 |' in x];assert len(own)==1;i=own[0];cells=lines[i].rstrip('\n').split('|');assert len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5'
 cells[8]=' claimed_solved ';cells[9]=' prior unknown; 1 recovered ';cells[10]=' https://github.com/AlecKriebel/Math/pull/195 '
 cells[11]=' Seven-plane characteristic-zero ambient-Jacobian counterexample: second-variable gin cutoff8 and degree7 minimal generator involving third variable, with nonempty-open-set proof; corrected primary conjecture, valid three-variable theorem respected. Classical parallel connection/tools and applicable Migliore–Nagel distinct unmixed-ideal resolution credited. Bounded36-source/120-query audit plus19 exact earlier-example checks; historical novelty, firstness and independence unestablished; Ilardi2018 full-text gap explicit. Two successive NEW whole-package adversaries clean (v1 then entire final v2). Extensive AI; unrefereed; no conventional human peer review. '
 cells[12]=' ['+doi+'](https://doi.org/'+doi+') ';lines[i]='|'.join(cells)+'\n';new=''.join(lines).encode();assert [j for j,(x,y) in enumerate(zip(old.decode().splitlines(keepends=True),lines)) if x!=y]==[i];return new

def overlay(c,h,n,parent,stamp,phase):
 out={};f=facts(stamp,phase);stage={'merge':'published_pending_merge','factual':'actual_merge_accepted','completion':'factual_checkpoint_accepted'}[phase];native=n.construct(stage,f);out.update(native)
 def add(rel):
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,rel;out[CASE+rel]=p.read_bytes()
 for name in ['ROOT_PUBLICATION_RECEIPT.json','ROOT_TRACKER_RECEIPT.json']:add(name)
 prior=PHASES[phase][0]
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json']:add(prior+'/'+name)
 add('publication_lifecycle_01/finish195.py')
 if phase=='merge':
  assert all(h.lookup(h.api('git/commits/'+parent)['tree']['sha'],x) is None for x in native), 'Native PR195 already present before original-HEAD merge'
  out[QUEUE]=queue(h.body_at(QUEUE,parent),f['DOI'])
 else:
  q=h.body_at(QUEUE,parent);assert f['DOI'].encode() in q
 case=json.loads(h.body_at(CASE+'CURRENT_CASE_STATUS.json',parent));assert case['PR']==195 and case['original_head']==HEAD and case['original_effort']=='prior unknown; 1 recovered'
 prior_percent={'merge':90,'factual':95,'completion':98}[phase];assert case['case_percent']==prior_percent
 complete=phase=='completion';merged=phase!='merge';status={'merge':'PUBLISHED_TRACKED_ORIGINAL_HEAD_SAFE_MERGE_PREPARED','factual':'ORIGINAL_HEAD_SAFE_MERGE_ACCEPTED_FACTUAL_CHECKPOINT','completion':'QUALIFIED_NOTE_PUBLISHED_TRACKED_MERGED_FACTUAL_COMPLETION_ACCEPTED'}[phase]
 remain={'merge':'Verify actual original PR merge and full current MAIN; actual factual acceptance and completion reconciliation before196 intake.','factual':'Accept actual factual checkpoint and reconcile completed metadata from that receipt before196 intake.','completion':'PR195 complete after this completion checkpoint actual fullscope acceptance; then original-status-only196 intake. Broader programme remains active.'}[phase]
 case.update(UTC=stamp,status=status,case_percent=PHASES[phase][2],publication_ready=True,whole_publication_package_reviews_complete=True,actual_Zenodo_published=True,actual_tracker_updated=True,actual_original_PR_merged=merged,actual_publication_verified=True,actual_tracker_row_verified=True,actual_merge_accepted=merged,actual_factual_MAIN_accepted=complete,completed=complete,DOI=f['DOI'],Zenodo_record_id=f['record_id'],tracker_range=f['tracker_range'],actual_merge_receipt=f.get('actual_merge_receipt'),actual_factual_receipt=f.get('actual_factual_receipt'),historical_priority_established=False,historical_novelty_or_firstness_established=False,fully_completed_count=42 if complete else 41,published_count=26 if complete else 25,last_completed_PR=195 if complete else 193,remaining_required_steps=remain,completion_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance=True)
 out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(195,41,25,193,prior_percent)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':195,'prior_phase':prior_percent,'values':{k:v for k,v in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=PHASES[phase][2],current_workflow_estimate_percent=PHASES[phase][2],current_completed=complete,current_closed=False,current_original_PR_merged=merged,current_original_PR_open_draft=False,current_Zenodo_published=True,current_DOI=f['DOI'],current_tracker_updated=True,current_tracker_range=f['tracker_range'],current_actual_publication_verified=True,current_actual_tracker_row_verified=True,current_actual_merge_accepted=merged,current_actual_factual_checkpoint_accepted=complete,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=True,current_publication_package_reviews_complete=True,current_NEW_whole_publication_package_reviews_completed=2,current_NEW_whole_publication_package_review_active=False,current_whole_package_review_loop_complete=True,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,current_actual_merge_receipt=f.get('actual_merge_receipt'),current_actual_factual_receipt=f.get('actual_factual_receipt'),next_numeric_intake_cursor=196 if complete else 195,conditional_next_numeric_intake_cursor=196,advance_to_next_PR_authorized_now=complete,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=195,next_status_only_intake_performed=False,persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR195 exact theorem verified and published as qualified note. Historical priority/firstness/independence unresolved; classical credits and access gaps explicit. '+('42completed/26published,last195;196 intake only after actual own completion checkpoint acceptance.' if complete else '41completed/25published,last193; current195 publication verified but factual completion pending;advancefalse.'),program_snapshot_authority_condition='This phase postimage effective only after actual true-parent/fullscope/every-current-selected-identity acceptance. Later phases bind already actual prior receipts; no future acceptance is self-certified.')
 if complete:
  oldmeta={k:p[k] for k in list(p) if k.startswith(('last_completed_','last_published_'))};p.setdefault('historical_prior_completion_metadata',[]).append({'UTC':stamp,'PR':193,'superseded_by':195,'values':oldmeta})
  for k in oldmeta:del p[k]
  assert len(set(p['fully_completed_eligible_PRs']))==len(p['fully_completed_eligible_PRs'])==41 and 195 not in p['fully_completed_eligible_PRs'];assert len(set(p['published_PRs']))==len(p['published_PRs'])==25 and 195 not in p['published_PRs']
  p['fully_completed_eligible_PRs'].append(195);p['published_PRs'].append(195)
  fraction=round(100*42/p['dated_eligible_total'],1)
  p.update(fully_completed_count=42,published_count=26,fully_completed_fraction_percent=fraction,workflow_estimate_percent=fraction,workflow_estimate_definition='42/dated99 completed,26 published; dated denominator is not a fresh eligibility census.',last_completed_PR=195,last_completed_PR_workflow_percent=100,last_completed_original_head=HEAD,last_completed_original_QUEUE_status='claimed_solved',last_completed_original_budget='prior unknown; 1 recovered',last_completed_mathematical_result_valid=True,last_completed_priority_clearance=True,last_completed_priority_clearance_scope='Bounded priority audit and qualified-note scope accepted; historical priority, firstness and independence unresolved.',last_completed_historical_firstness_or_guaranteed_novelty_certified=False,last_completed_bounded_priority_audit_complete=True,last_completed_outcome='Verified seven-plane counterexample published as fully credited qualified unrefereed research note; tracked and original-HEAD-safe merged.',last_completed_DOI=f['DOI'],last_completed_DOI_file_identity_verified=True,last_completed_merge_commit=f['actual_merge_receipt']['checkpoint_commit'],last_completed_tracker_range=f['tracker_range'],last_completed_record='audits/pr195_30004601/CURRENT_CASE_STATUS.json',last_completed_actual_final_receipt='audits/pr195_30004601/publication_lifecycle_01/factual01/ACCEPTANCE.json',last_completed_actual_final_receipt_sha256=pin((A/'publication_lifecycle_01/factual01/ACCEPTANCE.json').read_bytes())['sha256'],last_published_PR=195,last_published_DOI=f['DOI'],last_published_tracker_range=f['tracker_range'])
  p.setdefault('historical_completed_case_records',[]).append({'UTC':stamp,'PR':195,'original_head':HEAD,'DOI':f['DOI'],'actual_merge':f['actual_merge_receipt']['checkpoint_commit'],'actual_factual_receipt':f['actual_factual_receipt'],'qualified_priority_unestablished':True})
 out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
 note='\n'+stamp+' — PR195 '+phase+' '+str(PHASES[phase][2])+'% checkpoint: '+status+'. DOI '+f['DOI']+', exact three Zenodo files/metadata/resolver verified; tracker '+f['tracker_range']+' exact readback and foreign retention verified. Two successive NEW whole-package reviews clean (v1 then entire final v2). Original23 archive/scientific12 bytes preserved. Historical priority unresolved; classical arrangement/tools and distinct unmixed-family result credited. Original effort unknown/nonzero plus one recovered. '+remain+'\n'
 for path in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[path]=h.body_at(path,parent)+note.encode()
 return out

def selected(c,b,out):
 for name,raw in out.items():
  assert name.startswith((CASE,NATIVE)) or name in MUTABLE,name
  if name in b and name not in MUTABLE and not name.startswith(NATIVE):assert c.byte_pin(raw)==b[name],name
 return {**b,**{name:c.byte_pin(raw) for name,raw in out.items()}}
def message(phase,digest):return 'PR195 '+phase+': verified seven-plane counterexample; qualified note10.5281/zenodo.23395703\n\nClassical credits and historical-priority limits explicit. Original submitted HEAD retained; exact published package and tracker accepted.\nPR195 '+phase+' selected-map SHA256: '+digest

def verify(c,h,r,expected,phase):
 assert r['selected_files']==expected and r['selected_map_sha256']==c.selected_digest(expected)
 co=h.api('git/commits/'+r['commit']);pt=h.api('git/commits/'+r['expected_main'])['tree']['sha'];parents=[r['expected_main'],HEAD] if phase=='merge' else [r['expected_main']]
 assert [x['sha'] for x in co['parents']]==parents and co['tree']['sha']==r['tree'] and pt==r['parent_tree'] and co['message']==message(phase,c.selected_digest(expected))
 h.m.m.h.warm_selected_directories([pt,r['tree']],expected)
 for n,x in expected.items():assert h.lookup(r['tree'],n)==('100644','blob',x['git_blob']),n
 changes={n for n,x in expected.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob'])}
 assert changes==h.changed_leaves(pt,r['tree'])==set(r['changed_paths']) and changes<=set(r['overlay_paths'])

def original(h,phase,merged=False):
 p=h.api('pulls/195');assert p['head']['sha']==HEAD
 if phase=='merge' and not merged:assert p['state']=='open' and p['merged'] is False and p['draft'] is False
 if merged or phase!='merge':assert p['state']=='closed' and p['merged'] is True and p['merge_commit_sha']==read(D/'merge01/PREPARATION.json')['commit']
 return p

def prepare(c,h,n,phase,gen):
 b,a=base(c,phase);parent=h.api('git/ref/heads/main')['object']['sha'];pt=c.selected_current(h,parent,b['selected_files'],b['tree']);original(h,phase)
 assert h.api('compare/'+b['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(c,h,n,parent,stamp,phase);ex=selected(c,b['selected_files'],out);dest=D/gen;dest.mkdir(exist_ok=False)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':name,'mode':'100644','type':'blob','content':raw.decode()} for name,raw in sorted(out.items())]})['sha'];parents=[parent,HEAD] if phase=='merge' else [parent]
 co=h.api('git/commits','POST',{'tree':tree,'parents':parents,'message':message(phase,c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex)
 r={'UTC':stamp,'PR':195,'phase':phase,'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(name for name,x in ex.items() if h.lookup(pt,name)!=('100644','blob',x['git_blob'])),'MAIN_moved':False}
 save(dest/'PREPARATION.json',enc(r));verify(c,h,r,ex,phase);assert h.api('git/ref/heads/main')['object']['sha']==parent
 print(json.dumps({'phase':phase,'expected_main':parent,'commit':co,'tree':tree,'selected':len(ex),'changed':len(r['changed_paths'])}))

def accept(c,h,n,phase,gen):
 b,a=base(c,phase);r=read(D/gen/'PREPARATION.json');out=overlay(c,h,n,r['expected_main'],r['UTC'],phase);ex=selected(c,b['selected_files'],out);verify(c,h,r,ex,phase)
 main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];tree=c.selected_current(h,main,ex,r['tree']);pr=original(h,phase,True)
 for name,raw in out.items():assert c.byte_pin(raw)==ex[name] and h.lookup(tree,name)==('100644','blob',ex[name]['git_blob'])
 receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':195,'phase':phase,'accepted':True,'checkpoint_commit':r['commit'],'expected_main':r['expected_main'],'parents':[x['sha'] for x in h.api('git/commits/'+r['commit'])['parents']],'main_observed':main,'actual_tree':tree,'original_head':HEAD,'original_PR_actual_merged':True,'actual_merge_accepted':True,'actual_factual_accepted':phase in ['factual','completion'],'completion_metadata_accepted':phase=='completion','DOI':'10.5281/zenodo.23395703','tracker_range':"'Math Puzzles'!A110:D110",'actual_publication_verified':True,'actual_tracker_row_verified':True,'historical_priority_established':False,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'every_selected_identity_checked_at_actual_observed_MAIN':True,'full_foreign_tree_scope_preserved':True,'all_output_body_identities_verified':True,'original_effort':'prior unknown; 1 recovered','fully_completed_count':42 if phase=='completion' else 41,'published_count':26 if phase=='completion' else 25,'last_completed_PR':195 if phase=='completion' else 193,'case_percent':PHASES[phase][2],'next_numeric_intake_cursor':196 if phase=='completion' else 195,'advance_to_next_PR_authorized_now':phase=='completion','goal_complete':False}
 save(D/gen/'ACCEPTANCE.json',enc(receipt));print(json.dumps(receipt))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h,n=load();{'prepare':prepare,'accept':accept}[sys.argv[1]](c,h,n,sys.argv[2],sys.argv[3])
