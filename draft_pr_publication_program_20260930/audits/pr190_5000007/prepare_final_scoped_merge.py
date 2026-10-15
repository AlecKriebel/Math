"""Original-head-safe two-parent PR190 integration, exact scope on fresh MAIN."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,re,sys
A=Path(__file__).resolve().parent;P=A.parent.parent
s=importlib.util.spec_from_file_location('prior179',P/'audits/pr179_10800007/prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.TREE_CACHE_PATH=A/'integration_preparation/IMMUTABLE_TREE_CACHE.json'
api,require,save,lookup,changed_leaves,body_at,pin=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at,m.pin
PREFIX=m.PREFIX;CASE=PREFIX+'audits/pr190_5000007/';NATIVE='unsolved_math_prioritization/attempts/5000007/';HEAD='0c3346c8ebcb3b967a1d8bf9a283f027b44b738c';BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
def now():return datetime.datetime.now(datetime.UTC).isoformat()

alias_spec=importlib.util.spec_from_file_location('campaign190',A/'campaign_aliases.py');alias_module=importlib.util.module_from_spec(alias_spec);alias_spec.loader.exec_module(alias_module)
def require_selected_at_main(main,selected,reference_tree=None):
 actual_tree=api('git/commits/'+main)['tree']['sha']
 m.m.h.warm_selected_directories([reference_tree or actual_tree,actual_tree],selected)
 for name,x in selected.items():require(lookup(actual_tree,name)==('100644','blob',x['git_blob']),'Selected current MAIN identity drift '+name)
 return actual_tree

def gates():
 g=json.loads((A/'ROOT_PUBLICATION_GATE.json').read_text());z=json.loads((A/'ZENODO_PUBLICATION_READBACK.json').read_text());tr=json.loads((A/'TRACKER_ACCEPTANCE.json').read_text())
 require(g['status']=='READY_FOR_AUTHORIZED_PUBLICATION' and z['state']=='published','Scientific and actual publication gates')
 require(tr['status']=='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED' and tr['DOI']==z['doi'],'Actual tracker gate')
 require(not g['historical_priority_clearance'] and g['qualified_note_route_authorized'],'Priority claim level drift')
 for n,x in g['payloads'].items():require(pin(A/g['package_name']/n)['sha256']==x['SHA256'],'Reviewed bytes drift '+n)
 return g,z,tr
def original_ready():
 p=api('pulls/190');require(p['head']['sha']==HEAD and p['state']=='open' and not p['draft'] and not p['merged'],'Original PR head/state changed')
def prepare(gen):
 require(re.fullmatch('merge_preparation_[a-z0-9_]+',gen),'Bad generation');g,z,tr=gates();original_ready()
 e=api('git/ref/heads/main')['object']['sha'];parent=api('git/commits/'+e);plan=json.loads((A/'FINAL_MAIN_SCOPE.json').read_text());out=A/'integration_preparation'/gen;out.mkdir(exist_ok=False)
 q='unsolved_math_prioritization/QUEUE.md';before=body_at(q,e).decode();lines=before.splitlines(keepends=True);idx=[i for i,l in enumerate(lines) if '| 5000007 /' in l];require(len(idx)==1,'QUEUE target absent');i=idx[0];cells=lines[i].rstrip('\n').split('|');require(len(cells)==14,'QUEUE schema')
 originals=[l for l in body_at(q,HEAD).decode().splitlines() if '| 5000007 /' in l];bases=[l for l in body_at(q,BASE).decode().splitlines() if '| 5000007 /' in l]
 require(len(originals)==len(bases)==1 and originals[0].split('|')[8].strip()=='claimed_solved','Original eligibility absent');require(lines[i].rstrip('\n') in [originals[0],bases[0]],'Foreign target-row drift; reconcile')
 cells[8]=' claimed_solved ';cells[9]=' unknown/5 (interrupted) ';cells[11]=' Verified two-part answer: imported bare-angle distance-two exclusion FALSE by exactly two direct proper face diagonals; explicitly adopted parity-selected endpoint exclusion PROVED without length bound. Supported source disambiguation, not authenticated author erratum or uniquely forced printed intent. Classical AAH/Troubetzkoy midpoint mechanism and Ferudun contemporaneous exact overlap credited; current DOI-version files authenticated, historical firstness/awareness/independence uncertified; older body/version gaps disclosed. Exact optimization-safe reproduction separates valid16faceword from terminal-type and displayed-coordinate errors. Successive fresh whole-package reviews clean. Extensive AI; unrefereed. ';cells[12]=' ['+z['doi']+']('+z['doi_url']+') ';lines[i]='|'.join(cells)+'\n';after=''.join(lines)
 require(len(before.splitlines())==len(after.splitlines()) and sum(x!=y for x,y in zip(before.splitlines(),after.splitlines()))==1,'Foreign QUEUE row delta');(out/'QUEUE.md').write_text(after)
 j=json.loads(body_at(PREFIX+'CURRENT_PROGRESS.json',e));require(j['fully_completed_count']==38 and j['published_count']==22 and j['last_completed_PR']==184 and 190 not in j['fully_completed_eligible_PRs'] and j['current_PR']==190,'Own programme census changed')
 stamp=now();j.update(UTC=stamp,updated_UTC=stamp,current_status='QUALIFIED_NOTE_PUBLISHED_TRACKED_EXACT_INTEGRATION_PREPARED_ORIGINAL_HEAD_MERGE_PENDING',current_PR_workflow_percent=95,current_workflow_estimate_percent=95,current_mathematics_cleared=True,current_priority_clearance=False,current_bounded_priority_audit_complete=True,current_full_priority_body_coverage_complete=False,current_historical_firstness_or_guaranteed_novelty_certified=False,current_qualified_note_route_authorized=True,current_publication_ready=True,current_publication_package_reviews_complete=True,current_Zenodo_published=True,current_DOI=z['doi'],current_tracker_updated=True,current_tracker_range=tr['range'],current_original_PR_merged=False,current_closed=False,current_remaining_required_steps='Actual original-head two-parent MAIN merge with full semantic scope/parent/native/PR readback acceptance and factual completion checkpoint; then ordered intake191.',next_numeric_intake_cursor=191,advance_to_next_PR_authorized_now=False,persistent_goal_complete=False)
 alias_module.normalize(j,95);save(out/'CURRENT_PROGRESS.json',j)
 note='\n\n'+stamp+' — PR190 workflow95%: exact reviewed qualified two-part endpoint note '+z['doi_url']+' actually published and tracker '+tr['range']+' verified. Qualified bare-angle counterexamples and adopted parity-selected theorem cleared, historicalpriority unresolved with explicit gaps; no firstness/author-intent/independence claim. Successive NEW complete-package reviews accepted. Original-head integration prepared; actualmergepending.38completed/22published unchanged until factual acceptance.\n'
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:(out/n).write_bytes(body_at(PREFIX+n,e)+note.encode())
 cur=json.loads((A/'integration_preparation/CURRENT_TEMPLATE.json').read_text());require(cur['current_template']=='native_template_final_01','Native template not final');native=A/'integration_preparation'/cur['current_template']
 overlay={CASE+n:A/n for n in plan['case_paths']};overlay.update({NATIVE+n:native/n for n in cur['files']});overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']});overlay[q]=out/'QUEUE.md';require(set(overlay)==set(plan['selected_MAIN_paths']),'Final scope drift')
 pins={n:{**pin(p),'local_path':str(p)} for n,p in sorted(overlay.items())};entries=[]
 for n,p in sorted(overlay.items()):
  b=p.read_bytes();x={'path':n,'mode':'100644','type':'blob'}
  try:x['content']=b.decode()
  except UnicodeDecodeError:
   blob=api('git/blobs','POST',{'content':base64.b64encode(b).decode(),'encoding':'base64'});require(blob['sha']==pins[n]['git_blob'],'Binary identity drift');x['sha']=blob['sha']
  entries.append(x)
 tree=api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':entries});m.m.h.warm_selected_directories([parent['tree']['sha'],tree['sha']],pins)
 changed={n for n,x in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',x['git_blob'])};require(changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Fulltree foreign delta')
 for n,x in pins.items():require(lookup(tree['sha'],n)==('100644','blob',x['git_blob']),'Selected identity drift')
 co=api('git/commits','POST',{'message':'Merge PR190: two formulations of the dodecahedral endpoint question\n\nBare-angle exclusion false by two face diagonals; adopted parity-selected unbounded endpoint theorem proved. Classical inputs and exact contemporary overlap credited; current DOI files authenticated, historicalfirstness/sourceintent/independence not certified. Exactreviewed preprint '+z['doi_url']+' and tracker '+tr['range']+'. Originalhead/history preserved, optimization-safe scientific repairs propagated, foreignMAIN paths preserved.','tree':tree['sha'],'parents':[e,HEAD]})
 require([x['sha'] for x in api('git/commits/'+co['sha'])['parents']]==[e,HEAD],'Prepared parents drift');original_ready();r={'UTC':now(),'status':'PREPARED_TWO_PARENT_MAIN_NOT_MOVED','expected_main':e,'original_PR_head':HEAD,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':co['sha'],'selected_files':pins,'changed_paths':sorted(changed),'DOI':z['doi'],'tracker_range':tr['range'],'generation':gen,'peer_pause_or_atomic_all_writer_CAS_claimed':False};save(A/'SCOPED_MERGE_PREPARATION.json',r);require(api('git/ref/heads/main')['object']['sha']==e,'MAIN advanced; rebuild fromfresh tip');print(json.dumps({'expected_main':e,'commit':co['sha'],'tree':tree['sha'],'selected':len(pins),'changed':len(changed)}))
def accept():
 r=json.loads((A/'SCOPED_MERGE_PREPARATION.json').read_text());co=api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==[r['expected_main'],HEAD],'Actual parent/tree drift')
 m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],r['selected_files']);require(changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']),'Actual full scope drift')
 for n,x in r['selected_files'].items():require(lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Actual selected identity')
 actual=api('git/ref/heads/main')['object']['sha'];require(api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Merge not onMAIN');p=api('pulls/190');require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR not actually merged')
 require_selected_at_main(actual,r['selected_files'],r['tree'])
 g,_,_=gates()
 for n in [NATIVE+'PROOF_V2.md',NATIVE+'check_certificate.py',NATIVE+'independent_review/reviewer_exact_check.py',NATIVE+'source_record.json',NATIVE+'prior_imported_report.json',CASE+g['package_name']+'/dodecahedron_endpoint.tex',CASE+g['package_name']+'/zenodo-deposit.json',CASE+'TRACKER_ACCEPTANCE.json',CASE+g['package_name']+'/dodecahedron_endpoint.pdf',CASE+g['package_name']+'/verification-package.zip']:
  b=body_at(n,actual);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh native body drift')
 out={'UTC':now(),'status':'ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_AND_FRESH_NATIVE_READBACK_ACCEPTED','PR':190,'main_observed':actual,'merge_commit':r['commit'],'tree':r['tree'],'parents':[r['expected_main'],HEAD],'original_PR_head':HEAD,'PR_merged':True,'PR_closed':True,'PR_reported_merge_commit':p['merge_commit_sha'],'selected_files':len(r['selected_files']),'changed_paths':len(r['changed_paths']),'foreign_MAIN_paths_preserved':True,'actual_native_scientific_and_metadata_bytes_accepted':True,'every_selected_identity_checked_at_actual_observed_MAIN':True,'DOI':r['DOI'],'tracker_range':r['tracker_range'],'case_percent':100,'factual_programme_checkpoint_pending':True};save(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',out);print(json.dumps(out))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare(sys.argv[2])
 elif sys.argv[1]=='accept':accept()
 else:raise RuntimeError('Unknown action')
