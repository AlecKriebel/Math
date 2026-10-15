#!/usr/bin/env python3
"""Verify completed PR938 receipts, record outcome, then status-gate later PRs.

Run only after actual merge, publication, DOI tracker and native publication
receipt exist. No publication/merge/Sheet/native-write operation is invoked.
The only external mutation is the authorized final PR title/body after all
completed-outcome checks. Subsequent candidates receive status-only inspection
until an exact claimed_solved immutable-head row passes the gate.
"""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,importlib.util,io,json,stat,subprocess,tarfile
P=Path(__file__).resolve().parent;ROOT=P.parent;A=P/'audits/pr938_30003634';D=A/'publication'
KEY='30003634';HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
QUEUE='unsolved_math_prioritization/QUEUE.md';STATE='unsolved_math_prioritization/state.json';HISTORY='unsolved_math_prioritization/history.jsonl'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def load(path):return json.loads(path.read_text())
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def run(args):return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True).stdout
def blob(ref,name):return subprocess.run(['git','show',ref+':'+name],cwd=ROOT,check=True,capture_output=True).stdout

def queue_without(raw):
 rows=raw.splitlines(keepends=True);hits=[i for i,line in enumerate(rows) if b'| 30003634 /' in line];need(len(hits)==1,'Ambiguous target queue row');row=rows.pop(hits[0]);return b''.join(rows),row

def raw_json_values(raw):
 """Independently preserve each other JSON member's literal key/colon/value."""
 text=raw.decode();dec=json.JSONDecoder();need(text.lstrip().startswith('{'),'State not object');pos=text.index('{')+1;values={}
 while True:
  while text[pos].isspace() or text[pos]==',':pos+=1
  if text[pos]=='}':break
  start=pos;key,pos=dec.raw_decode(text,pos);need(type(key) is str and key not in values,'Duplicate state key')
  while text[pos].isspace():pos+=1
  need(text[pos]==':','State colon');pos+=1
  while text[pos].isspace():pos+=1
  _,pos=dec.raw_decode(text,pos);values[key]=text[start:pos]
 return values

def verify_completed():
 publication=load(D/'ZENODO_PUBLISH.json');merge=load(A/'PR_MERGE_RECEIPT.json');tracker=load(A/'TRACKER_RECEIPT.json');native=load(A/'NATIVE_PUBLICATION_RECEIPT.json');accepted=load(A/'ACCEPTANCE.json')
 spec=importlib.util.spec_from_file_location('pr938_completed_receipt_checks',P/'append_pr938_tracker.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 freeze=load(D/'PREPUBLICATION_FREEZE.json');need(hashlib.sha256((P/'append_pr938_tracker.py').read_bytes()).hexdigest()==freeze['future_helpers']['append_pr938_tracker.py']['sha256'],'Reviewed receipt checker changed')
 m.verify_receipt_links(A,publication,merge,accepted,tracker,native)
 need(accepted['all_prior_required_and_optional_findings_resolved'] is True and accepted['proof_gap'] is None and len(accepted['full_package_reviews'])>=3,'Complete fresh review chain absent')
 live=json.loads(run(['gh','pr','view','938','--repo','AlecKriebel/Math','--json','number,state,headRefOid,mergeCommit,mergedAt,url']))
 need(live['number']==938 and live['state']=='MERGED' and live['headRefOid']==merge['headRefOid'] and live['mergeCommit']==merge['mergeCommit'],'Fresh actual merged head differs')
 # Fresh exact DOI-row readback; no append/write is performed here.
 readback=json.loads(run(['gws','sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':m.SID,'range':tracker['updated_range']})]))
 need(readback.get('range')==tracker['updated_range'] and readback.get('values')==[tracker['row']],'Fresh actual tracker row differs')
 ref=native['commit'];parent=native['parent'];run(['git','fetch','--no-write-fetch-head','origin',ref]);remote=run(['git','ls-remote','origin','refs/heads/main']).split()[0];run(['git','fetch','--no-write-fetch-head','origin',remote]);run(['git','merge-base','--is-ancestor',ref,remote])
 need(run(['git','show','-s','--format=%P',ref]).strip()==parent,'Native commit parent differs')
 changed=run(['git','diff','--name-only',parent,ref]).splitlines();need(set(changed)<={QUEUE,STATE,HISTORY} and changed==native['paths'],'Unexpected native publication path')
 old_queue=blob(parent,QUEUE);new_queue=blob(ref,QUEUE);before,_=queue_without(old_queue);after,row=queue_without(new_queue);cells=row.decode().split('|');doi=publication['doi']
 need(before==after and cells[8].strip()=='preprint_published' and cells[9].strip()=='2/5' and doi in row.decode(),'Native target/other queue bytes mismatch')
 old_state=blob(parent,STATE);new_state=blob(ref,STATE);old_members=raw_json_values(old_state);new_members=raw_json_values(new_state)
 need({k:v for k,v in old_members.items() if k!=KEY}=={k:v for k,v in new_members.items() if k!=KEY},'Other state members changed')
 event=json.loads(new_state)[KEY];need(event==native['published_event'],'Native state differs from recorded event')
 need(event.get('status')=='preprint_published' and event.get('doi')==doi and type(event.get('turns_used')) is int and event['turns_used']==2 and event['candidate_turn']==2 and event['turn_limit']==5 and event['verified_candidate_approaches']==2 and event['original_total_attempt_count_known'] is False and event['proof_search_turns_added_by_audit']==1 and event['turn_count_status']=='original_observed_one_plus_one_genuinely_recorded_strengthening','Known2/5 native accounting differs')
 old_history=blob(parent,HISTORY);new_history=blob(ref,HISTORY);need(new_history.startswith(old_history),'Prior native history bytes changed')
 appended=new_history[len(old_history):].splitlines();events=[json.loads(x) for x in appended if x.strip()];need(events==[event],'Native history must append exactly the same one publication event')
 original_row=queue_without(blob(HEAD,QUEUE))[1];need(original_row.decode().split('|')[9].strip()=='1/5','Original observed accounting altered')
 snapshot=load(A/'ORIGINAL_SNAPSHOT.json');need(snapshot['head']==HEAD and len(snapshot['files'])==44,'Wrong original inventory')
 for name,pin in snapshot['files'].items():need(hashlib.sha256(blob(merge['mergeCommit']['oid'],name)).hexdigest()==pin,'Merged original bytes changed')
 save(A/'PUBLICATION_FINAL_VERIFICATION.json',{'utc':datetime.now(timezone.utc).isoformat(),'accepted_freeze_sha256':accepted['freeze_sha256'],'actual_merged_head_and_original44_match':True,'actual_tracker_exact_row_readback':True,'native_commit_on_current_remote_main':True,'native_other_queue_bytes_state_members_history_prefix_preserved':True,'native_known_turns':'2/5','original_observed_turns':'1/5 preserved','new_complete_stronger_mechanisms':1,'native_state_and_history_event_exact':True,'publication_metadata_and_file_receipt_links_match':True,'workflow_completion_percent':100})
 return publication,merge,tracker,native,accepted

def main():
 publication,merge,tracker,native,accepted=verify_completed();now=datetime.now(timezone.utc).isoformat();doi=publication['doi']
 record={'utc':now,'pr':938,'problem_id':KEY,'outcome':'accepted_merged_preprint_published','original_pr_head':HEAD,'integrated_pr_head':merge['headRefOid'],'merge_commit':merge['mergeCommit']['oid'],'doi':doi,'record_url':publication['record_url'],'tracker_range':tracker['updated_range'],'native_ledger_commit':native['commit'],'native_ledger_readback_confirmed':True,'original_turns_preserved':'Original observed1/5; one separately counted complete strengthening, known combined2/5','priority_limit':'General signature/quasimorphism tools explicitly credited, including stronger Kawasaki etal2025Lemma7.12. Bounded primary searches did not establish an earlier complete answer to the exact braid-solvability question; no firstness/current-openness or new general group theorem asserted.','AI_and_peer_review':'Extensive AI assistance; unrefereed; no independent human or formal proof certification','full_package_review_count':len(accepted['full_package_reviews']),'clean_final_review_manifest_sha256':accepted['full_package_reviews'][-1]['manifest_sha256'],'paper_candidate_revision':load(D/'PREPUBLICATION_FREEZE.json')['revision_candidate'],'all_prior_required_and_optional_findings_resolved':True}
 save(A/'PUBLICATION_RECORD.json',record)
 body=f'''Accepted and published after independent topology, planar Goeritz, Burau--Meyer, source/model and reproduction audits, two deep primary priority audits, fresh all-depth mechanism falsification, and sequential NEW whole-package adversarial reviews with every required and optional finding addressed.

For every m>=3 and every finite k>=1, the ordinary derived subgroup P_m^(k) contains a braid whose standard closure is not integrally smoothly 1-solvable. Therefore P_m^(n+2) is not contained in F_n^m for every integer n>=1, answering negatively Question 3 of Harvey's contribution, joint work with Park and Ray, Pure braids, Whitney towers, and 0-solvability, in Mini-Workshop: Interactions between Low-dimensional Topology and Complex Algebraic Geometry, OWR50/2017, p3021, published2018. Distinct existential witnesses may depend on depth; no common braid in the derived intersection is asserted. For m=1,2 the positive derived terms are trivial.

Preprint: **Deep derived pure braids need not be 1-solvable**, version1.0, Alec Kriebel. DOI: [{doi}](https://doi.org/{doi}). The [Zenodo record]({publication['record_url']}) contains the four-page note and source/verification archive.

The signature quasimorphism and its values are established Gambaudo--Ghys inputs; amenable rigidity is recalled by Calegari, and Kawasaki--Kimura--Maruyama--Matsushita--Mimura2025Lemma7.12 already proves a stronger general defect-restriction fact. Otto's actual integral solution definition and Toffoli's pointwise surgery formula support the universal signature obstruction, including -1 Alexander roots and twisted radicals. Taking a power converts nonzero homogeneous signature to nonzero ordinary signature. No new general quasimorphism theorem is claimed. Bounded primary searches did not establish an earlier complete answer to the precise braid-solvability question; no first-priority or continued-openness certificate is asserted.

All44 original PR files remain unchanged. The explicit104-letter P3^(3) braid has signature-2 by independent complete planar Goeritz and Burau--Meyer calculations, with the actual trefoil convention and mixed-parity control. This finite n=1 witness is distinct from the all-depth existential proof. The standard-library release verifier authenticates the closed inventory and copied checker bytes before isolated nonoptimized replay; exact finite checks supplement the written universal proof and do not certify priority or provide an operating-system sandbox. Historical source-indexing, relocation, optimization and transport limitations are retained with corrections. Raw third-party source bodies are excluded.

AI tools were used extensively in research, proof development, source checking, computation, writing and adversarial verification. This is an unrefereed preprint; AI-assisted reviews are not independent human or journal peer review, and no such review or formal proof-assistant certification is claimed. Exact reviewed metadata/files, the published DOI and tracker row {tracker['updated_range']} were read back. The immutable original observed1/5 is preserved; one separately completed stronger mechanism was recorded by the genuine unmodified native CLI, for a known combined2/5. Verification adds no further proof-search response.

Original audited head: `{HEAD}`. Merged head: `{merge['headRefOid']}`. Audit/publication receipts: `draft_pr_claimed_solved_900_1000_20261012/audits/pr938_30003634/`.
'''
 body_path=A/'PR_PUBLISHED_BODY.md';body_path.write_text(body);current=json.loads(run(['gh','pr','view','938','--repo','AlecKriebel/Math','--json','title,body']))
 title='30003634: accepted all-depth pure-braid counterexamples and published preprint'
 if current['body']!=body or current['title']!=title:run(['gh','pr','edit','938','--repo','AlecKriebel/Math','--title',title,'--body-file',str(body_path)])
 confirmed=json.loads(run(['gh','pr','view','938','--repo','AlecKriebel/Math','--json','number,title,body,state,headRefOid,mergeCommit,url']))
 need(confirmed['state']=='MERGED' and confirmed['headRefOid']==merge['headRefOid'] and confirmed['mergeCommit']==merge['mergeCommit'] and confirmed['body']==body and confirmed['title']==title,'Final PR metadata readback differs');save(A/'PR_PUBLISHED_METADATA.json',confirmed)
 state=load(P/'CURRENT_STATE.json');already=938 in state['completed_prs'];need(state.get('active_pr') in (938,None) or already,'Unexpected active target')
 if already and state.get('active_pr') not in (938,None):print(json.dumps({'already_finalized':True,'next_pr':state['active_pr']}));return
 completed=sorted([r for r in state['completed_results'] if r['pr']!=938]+[record],key=lambda r:r['pr']);state.update(utc=now,completed_results=completed,completed_prs=[r['pr'] for r in completed],published_prs=[r['pr'] for r in completed if r['outcome']=='accepted_merged_preprint_published'],closed_prs=[r['pr'] for r in completed if r['outcome'].startswith('closed_')],active_pr=None,active_problem_id=None,active_pr_completion_estimate_percent=0,phase='next_status_gate_after_PR938')
 inventory=load(P/'inventory.json')
 for row in inventory:
  if row['number']==938:row.update(disposition=record['outcome'],doi=doi,tracker_range=tracker['updated_range'])
 if not already:
  with (P/'README.md').open('a') as out:out.write(f'\nPR #938 accepted, merged and published: [{doi}](https://doi.org/{doi}); tracker {tracker["updated_range"]}. All finite derived depths, credited prior general inputs, bounded priority and unrefereed AI disclosures explicit; original observed1/5 preserved with one separately counted strengthening, known2/5.\n')
  for path in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
   with path.open('a') as out:out.write(f'\n{now} — PR938 workflow100%; eight of initial12workflows handled, seven published and one verified priority closure (shard66.67%). Actual merge {record["merge_commit"]}; published {doi}; tracker {tracker["updated_range"]}; native ledger {native["commit"]}. Exact readbacks verified, original44/observed1of5 retained and known2of5 native accounting verified; other target queue/state/history bytes preserved.\n')
 save(P/'CURRENT_STATE.json',state);save(P/'inventory.json',inventory);skipped=[]
 for old in sorted((r for r in inventory if 938<r['number']<=1000),key=lambda r:r['number']):
  number=old['number'];pr=json.loads(run(['gh','pr','view',str(number),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url']))
  if pr['state']!='OPEN' or not pr['isDraft']:
   skipped.append({'pr':number,'action':'SKIP_NOT_OPEN_DRAFT','math_source_read':False})
   if number in state['eligible_prs'] and number not in state['completed_prs']:state['eligible_prs'].remove(number)
   continue
  ids=[str(e['id']) for e in old['entries']];need(len(ids)==1,'Multiple target metadata requires narrow reconciliation');key=ids[0]
  queue=run(['gh','api','repos/AlecKriebel/Math/contents/'+QUEUE+'?ref='+pr['headRefOid'],'-H','Accept: application/vnd.github.raw+json']);rows=[r for r in queue.splitlines() if '| '+key+' /' in r];need(len(rows)==1,'Ambiguous next-target queue row');status=rows[0].split('|')[8].strip()
  if status!='claimed_solved':
   skipped.append({'pr':number,'problem_id':key,'status':status,'action':'SKIP_STATUS_ONLY','math_source_read':False});old.update(eligible=False,disposition='skipped_status_gate')
   if number in state['eligible_prs'] and number not in state['completed_prs']:state['eligible_prs'].remove(number)
   continue
  need(pr['baseRefName']=='main','Next selected target base changed');folder=P/'audits'/f'pr{number}_{key}';folder.mkdir(exist_ok=True);need(not (folder/'ORIGINAL_SNAPSHOT.json').exists(),'Next snapshot already exists; inspect before replacing');stamp=datetime.now(timezone.utc).isoformat();pr.update(problem_id=key,status=status,eligible=True,gate_utc=stamp,queue_row_sha256=hashlib.sha256(rows[0].encode()).hexdigest());save(folder/'ELIGIBILITY_GATE.json',pr);(folder/'GATED_QUEUE_ROW.md').write_text(rows[0]+'\n')
  run(['git','fetch','--no-write-fetch-head','origin',pr['headRefOid']]);prefix='unsolved_math_prioritization/attempts/'+key;raw=subprocess.run(['git','archive',pr['headRefOid'],prefix],cwd=ROOT,check=True,capture_output=True).stdout;original=folder/'original';original.mkdir(exist_ok=True)
  with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
   for member in archive.getmembers():
    name=member.name.rstrip('/');safe=(not name.startswith('/') and '..' not in Path(name).parts and '\\' not in name);inside=name.startswith(prefix+'/');ancestor=member.isdir() and (name==prefix or prefix.startswith(name+'/'));need(safe and (member.isfile() or member.isdir()) and (inside or ancestor),'Unsafe next original archive member')
   archive.extractall(original,filter='data')
  files={f.relative_to(original).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(original.rglob('*')) if f.is_file()};save(folder/'ORIGINAL_SNAPSHOT.json',{'utc':stamp,'head':pr['headRefOid'],'files':files})
  if number not in state['eligible_prs']:state['eligible_prs'].append(number);state['eligible_prs'].sort()
  for field in ['active_original_head','original_candidate_turns','review_families','priority_families','publication_disposition','priority_status','full_package_reviews','candidate_revision02_frozen','operational_helper_revision','active_candidate_revision','active_freeze_sha256','active_package_manifest_sha256','new_priority_research_positive_turns','known_effort_positive_turns','new_mechanism_status']:state.pop(field,None)
  state.update(utc=stamp,active_pr=number,active_problem_id=key,next_pr=number,active_original_head=pr['headRefOid'],phase=f'PR{number}_exact_claimed_solved_gate_passed_before_math_reading',active_pr_completion_estimate_percent=0);old.update(eligible=True,status='claimed_solved');break
 state['shard_completion_estimate_percent']=100*len(state['completed_prs'])/len(state['eligible_prs']);state['publication']='PR904_PR905_PR906_PR908_PR909_PR919_PR938_published_tracker_native_ledgers_verified';save(P/'CURRENT_STATE.json',state);save(P/'inventory.json',inventory);save(P/'POST_PR938_STATUS_GATES.json',{'utc':datetime.now(timezone.utc).isoformat(),'skipped':skipped,'next_pr':state.get('active_pr')});print(json.dumps({'PR938':record,'next_pr':state.get('active_pr'),'status_only_skips':skipped},indent=2))
if __name__=='__main__':main()
