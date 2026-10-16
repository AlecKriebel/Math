"""Record only an already applied and actually read-back credit repair."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,subprocess
D=Path(__file__).resolve().parent;P=D.parents[2]
repair=json.loads((D/'CLASSIFICATION_REPAIR_RECEIPT.json').read_text());assert repair['status']=='APPLIED_AND_VERIFIED'
plan=json.loads((D/'PROPOSED_NATIVE_CHANGES.json').read_text());h=repair['corrected_head']
gh='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';base='repos/AlecKriebel/Math/'
def get(path):
 p=subprocess.run([gh,'api',base+path],capture_output=True,text=True,timeout=60);assert p.returncode==0,p.stderr;return json.loads(p.stdout)
pr=get('pulls/212');assert pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['head']['sha']==h
q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+h);raw=base64.b64decode(q['content']);rows=[x for x in raw.decode().splitlines() if '30005310 / OWR-11695865-009' in x];assert rows==[plan['new_row']] and rows[0].split('|')[8].strip()=='already_solved'
now=datetime.now(timezone.utc).isoformat()
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text());state.update(utc=now,head=h,original_head=repair['original_head'],QUEUE_status='already_solved',completion_percent=100,completion_scope='Eligible-intake audit and exact historical credit disposition, not new-discovery completion',stage='verified_credit_correction_complete_immediate_scope_skip',priority_verdict='Exact earlier coverage of literal numerical negative answer; bare mechanisms remain unresolved',native_repair_cleared=True,native_repair_applied_and_read_back=True,preprint_upload_cleared=False,DOI=None)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
s=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text());assert s['current_PR']==212
s.update(utc=now,current_PR_head=h,status_at_current_PR_head='already_solved',Queue_blob=q['sha'],case_completion_percent=100,current_stage=state['stage'],priority_verdict=state['priority_verdict'],priority_classification_repairs_required=[],priority_credit_repairs_required=[],previous_credit_disposition_PR=212,previous_credit_disposition_head=h,current_DOI=None,current_tracker_range=None,preprint_preparation_cleared=False,preprint_upload_cleared=False)
if 212 not in s['skip_PRs']:s['skip_PRs'].append(212)
s['skip_reasons']['212']='Exact prior numerical negative coverage by GS2015+BS2017 and HKS2026; bare mechanisms unresolved; credited already_solved correction after eligible intake'
s['previous_scope_skip_PR']=212;s['previous_scope_skip_reason']=s['skip_reasons']['212']
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(s,indent=2)+'\n')
entry='\n## '+now+': PR212 credit correction applied and verified —100% of eligible-intake disposition\n\nMathematicsPASS under exactfixedmeanRCONhypotheses. Three fresh mathematical/source families and two independent primarypriorityfamilies, root reconstruction/replays and fresh wholepacketadversary completed. Earlier literalnumericalnegativecoverage established; bareSOS/intersection remains unresolved, exactprior tiedvariant andfirstrecognition unestablished. Corrected existingPRhead '+h+' by guardedsoleparent/nonforce nativecommit; all35 actualnativefilebytes fetched/compared,20originals byteexact, mathematicalSections2–7 unchanged; exactoneQueue row changesstatus/noteonly, author1/5 retained. Exactpre-reviewedPRtitle/body appliedandreadback. CorrectedPRopen/draft; immediate scope-skip. No paper/DOI/deposit/tracker/merge/closure/PRcomment. Counts42completed/19preprints/19merges/0pendingrows unchanged; held293,292,280,239 unchanged. Overallgoalactive/incomplete; next lower eligible draft remains to process.\n'
for p in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write(entry)
receipt=dict(utc=now,PR=212,corrected_head=h,Queue_blob=q['sha'],Queue_sha256=hashlib.sha256(raw).hexdigest(),completion_percent=100,scope=state['completion_scope'],immediate_scope_skip=True,open_draft=True,counts=[42,19,19,0],overall_goal_active_incomplete=True)
(D/'VERIFIED_CREDIT_COMPLETION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
