"""Original-head-safe two-parent PR184 integration, exact scope on fresh MAIN."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,re,sys
A=Path(__file__).resolve().parent;P=A.parent.parent
s=importlib.util.spec_from_file_location('prior179',P/'audits/pr179_10800007/prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.TREE_CACHE_PATH=A/'integration_preparation/IMMUTABLE_TREE_CACHE.json'
api,require,save,lookup,changed_leaves,body_at,pin=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at,m.pin
PREFIX=m.PREFIX;CASE=PREFIX+'audits/pr184_10300044/';NATIVE='unsolved_math_prioritization/attempts/10300044/';HEAD='fbd6561971368a0867df83453454427863d7f910';BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def gates():
 g=json.loads((A/'ROOT_PUBLICATION_GATE.json').read_text());z=json.loads((A/'ZENODO_PUBLICATION_READBACK.json').read_text());tr=json.loads((A/'TRACKER_ACCEPTANCE.json').read_text())
 require(g['status']=='READY_FOR_AUTHORIZED_PUBLICATION' and z['state']=='published','Scientific and actual publication gates')
 require(tr['status']=='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED' and tr['DOI']==z['doi'],'Actual tracker gate')
 require(not g['historical_priority_clearance'] and g['qualified_note_route_authorized'],'Priority claim level drift')
 for n,x in g['payloads'].items():require(pin(A/g['package_name']/n)['sha256']==x['SHA256'],'Reviewed bytes drift '+n)
 return g,z,tr
def original_ready():
 p=api('pulls/184');require(p['head']['sha']==HEAD and p['state']=='open' and not p['draft'] and not p['merged'],'Original PR head/state changed')
def prepare(gen):
 require(re.fullmatch('merge_preparation_[a-z0-9_]+',gen),'Bad generation');g,z,tr=gates();original_ready()
 e=api('git/ref/heads/main')['object']['sha'];parent=api('git/commits/'+e);plan=json.loads((A/'FINAL_MAIN_SCOPE.json').read_text());out=A/'integration_preparation'/gen;out.mkdir(exist_ok=False)
 q='unsolved_math_prioritization/QUEUE.md';before=body_at(q,e).decode();lines=before.splitlines(keepends=True);idx=[i for i,l in enumerate(lines) if '| 10300044 /' in l];require(len(idx)==1,'QUEUE target absent');i=idx[0];cells=lines[i].rstrip('\n').split('|');require(len(cells)==14,'QUEUE schema')
 originals=[l for l in body_at(q,HEAD).decode().splitlines() if '| 10300044 /' in l];bases=[l for l in body_at(q,BASE).decode().splitlines() if '| 10300044 /' in l]
 require(len(originals)==len(bases)==1 and originals[0].split('|')[8].strip()=='claimed_solved','Original eligibility absent');require(lines[i].rstrip('\n') in [originals[0],bases[0]],'Foreign target-row drift; reconcile')
 cells[8]=' claimed_solved ';cells[9]=' 2/5 ';cells[11]=' Verified negative answer to literal Calegari2002v1 Question10.6: one fixed closed hyperbolic M, smooth cooriented taut F_N with ordinary GV=Na, a>0, same embedded positive closed transversal meeting every leaf. Credited classical suspension/replacement/hyperbolization consequence; historical priority unresolved after bounded primary-body audit, specific unread-source/version gaps disclosed. No firstness/guaranteed novelty/minimal-foliation claim. Repaired optimization-safe local controls, successive fresh whole-package reviews clean. Extensive AI; unrefereed. ';cells[12]=' ['+z['doi']+']('+z['doi_url']+') ';lines[i]='|'.join(cells)+'\n';after=''.join(lines)
 require(len(before.splitlines())==len(after.splitlines()) and sum(x!=y for x,y in zip(before.splitlines(),after.splitlines()))==1,'Foreign QUEUE row delta');(out/'QUEUE.md').write_text(after)
 j=json.loads(body_at(PREFIX+'CURRENT_PROGRESS.json',e));require(j['fully_completed_count']==37 and j['published_count']==21 and j['last_completed_PR']==179 and 184 not in j['fully_completed_eligible_PRs'] and j['current_PR']==184,'Own programme census changed')
 stamp=now();j.update(UTC=stamp,updated_UTC=stamp,current_status='QUALIFIED_NOTE_PUBLISHED_TRACKED_EXACT_INTEGRATION_PREPARED_ORIGINAL_HEAD_MERGE_PENDING',current_PR_workflow_percent=95,current_workflow_estimate_percent=95,current_mathematics_cleared=True,current_priority_clearance=False,current_bounded_priority_audit_complete=True,current_full_priority_body_coverage_complete=False,current_historical_firstness_or_guaranteed_novelty_certified=False,current_qualified_note_route_authorized=True,current_publication_ready=True,current_publication_package_reviews_complete=True,current_Zenodo_published=True,current_DOI=z['doi'],current_tracker_updated=True,current_tracker_range=tr['range'],current_original_PR_merged=False,current_closed=False,current_remaining_required_steps='Actual original-head two-parent MAIN merge with full semantic scope/parent/native/PR readback acceptance and factual completion checkpoint; then ordered intake185.',next_numeric_intake_cursor=185,advance_to_next_PR_authorized_now=False,persistent_goal_complete=False)
 save(out/'CURRENT_PROGRESS.json',j)
 note='\n\n'+stamp+' — PR184 workflow95%: exact reviewed qualified classical-consequence note '+z['doi_url']+' actually published and tracker '+tr['range']+' verified. Fixed hyperbolic-M/Na/commontransversal mathematics cleared, historicalpriority unresolved with explicit gaps; no firstness/minimality claim. Successive NEW complete-package reviews accepted. Original-head integration prepared; actualmergepending.37completed/21published unchanged until factual acceptance.\n'
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
 co=api('git/commits','POST',{'message':'Merge PR184: unbounded taut Godbillon-Vey numbers on fixed hyperbolic manifold\n\nCredited classical consequence answering literal Calegari2002v1 Q10.6. Historicalpriority unresolved, bounded body/version access gaps disclosed; nofirstness or minimality claim. Exactreviewed preprint '+z['doi_url']+' and tracker '+tr['range']+'. Originalhead/history preserved, optimization-safe scientific repairs propagated, foreignMAIN paths preserved.','tree':tree['sha'],'parents':[e,HEAD]})
 require([x['sha'] for x in api('git/commits/'+co['sha'])['parents']]==[e,HEAD],'Prepared parents drift');original_ready();r={'UTC':now(),'status':'PREPARED_TWO_PARENT_MAIN_NOT_MOVED','expected_main':e,'original_PR_head':HEAD,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':co['sha'],'selected_files':pins,'changed_paths':sorted(changed),'DOI':z['doi'],'tracker_range':tr['range'],'generation':gen,'peer_pause_or_atomic_all_writer_CAS_claimed':False};save(A/'SCOPED_MERGE_PREPARATION.json',r);require(api('git/ref/heads/main')['object']['sha']==e,'MAIN advanced; rebuild fromfresh tip');print(json.dumps({'expected_main':e,'commit':co['sha'],'tree':tree['sha'],'selected':len(pins),'changed':len(changed)}))
def accept():
 r=json.loads((A/'SCOPED_MERGE_PREPARATION.json').read_text());co=api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==[r['expected_main'],HEAD],'Actual parent/tree drift')
 m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],r['selected_files']);require(changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']),'Actual full scope drift')
 for n,x in r['selected_files'].items():require(lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Actual selected identity')
 actual=api('git/ref/heads/main')['object']['sha'];require(api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Merge not onMAIN');p=api('pulls/184');require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR not actually merged')
 g,_,_=gates()
 for n in [NATIVE+'CANDIDATE.md',NATIVE+'verify.py',NATIVE+'review/independent_checks.py',NATIVE+'source_record.json',NATIVE+'prior_imported_report.json',CASE+g['package_name']+'/taut_godbillon_vey.tex',CASE+g['package_name']+'/zenodo-deposit.json',CASE+'TRACKER_ACCEPTANCE.json']:
  b=body_at(n,actual);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh native body drift')
 out={'UTC':now(),'status':'ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_AND_FRESH_NATIVE_READBACK_ACCEPTED','PR':184,'main_observed':actual,'merge_commit':r['commit'],'tree':r['tree'],'parents':[r['expected_main'],HEAD],'original_PR_head':HEAD,'PR_merged':True,'PR_closed':True,'PR_reported_merge_commit':p['merge_commit_sha'],'selected_files':len(r['selected_files']),'changed_paths':len(r['changed_paths']),'foreign_MAIN_paths_preserved':True,'actual_native_scientific_and_metadata_bytes_accepted':True,'DOI':r['DOI'],'tracker_range':r['tracker_range'],'case_percent':100,'factual_programme_checkpoint_pending':True};save(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',out);print(json.dumps(out))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare(sys.argv[2])
 elif sys.argv[1]=='accept':accept()
 else:raise RuntimeError('Unknown action')
