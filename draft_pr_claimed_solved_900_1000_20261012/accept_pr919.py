#!/usr/bin/env python3
"""Accept only the exact reviewed PR919 candidate after a clean third review."""
import argparse
from datetime import datetime,timezone
import hashlib,json,re,stat,subprocess,zipfile
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;ROOT=P.parent;A=P/'audits/pr919_30002555';D=A/'publication'
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
FREEZE='c2c04a478b9f865655fb71b2b87945f01a2f4e41b4a78140e2eea42157f422cd'
PACKAGE='b1881fcc385141e3f54a24dcc04cc35d4b76365a588cd18c2e832a4a4efb8364'
BODY='04c3f4da7357a0d8f6ba86c95530145a48a897f37c9c3b22d80ca2325c9e6bbd'
EARLIER={1:'5bf7174357ccf4e228aeb14e1d25e44c9692b253919cde867c42b1a65956d3a1',2:'98cbe02d1862614c0696a44b0ad8f5a3d8f3afe49dbd4fd55806c87311bcd0b2'}
HELPERS=['merge_pr919.py','run_pr919_zenodo.py','append_pr919_tracker.py','update_pr919_publication_ledger.py','finalize_pr919_and_gate_next.py']
PREFIX='unsolved_math_prioritization/attempts/30002555/';QUEUE='unsolved_math_prioritization/QUEUE.md'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def data(q):
 need(stat.S_ISREG(q.lstat().st_mode),'Nonregular artifact: '+str(q));return q.read_bytes()
def fp(q):
 b=data(q);return {'bytes':len(b),'sha256':sha(b)}
def load(q):return json.loads(data(q))
def save(q,v):q.write_text(json.dumps(v,indent=2)+'\n')
def run(args,binary=False):return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=not binary).stdout
def safe_name(n):
 q=PurePosixPath(n);return type(n) is str and q.as_posix()==n and not q.is_absolute() and all(s not in ('','.','..') for s in n.split('/')) and '\\' not in n
def review(number,pin):
 f=A/'reviews'/f'full_package_{number:02}';need(fp(f/'MANIFEST.json')['sha256']==pin,'Unexpected review seal');m=load(f/'MANIFEST.json');records=m['files'];allowed=m['explicit_public_allowlist'];need(type(records) is dict and type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in allowed,'Review map not explicit/self-excluded')
 for n,r in records.items():need(safe_name(n) and fp(f/n)==r,'Sealed review drift: '+n)
 r=load(f/'RESULT.json');need(r['pr']==919 and r['problem_id']=='30002555' and r['original_pr_head']==HEAD,'Wrong review target');need(r['mathematical_remaining_gap_for_stated_theorem'] is None,'Unresolved proof gap');need(r['executed_validations']['full_reproducer_completed'] is True and r['executed_validations']['final_endpoint_authentication_after_seal_verifier_and_full_reproducer'] is True,'Full reproduction/final endpoint absent');need(load(f/'REPRODUCTION_RECEIPT.json')['status']=='PASS','Reproducer did not pass');return r,len(records)
def without_target(b):
 lines=b.splitlines(keepends=True);target=[s for s in lines if b'| 30002555 /' in s];need(len(target)==1,'Target row missing/ambiguous');return b''.join(s for s in lines if s not in target),target[0]
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--review03-manifest',required=True);args=ap.parse_args();need(re.fullmatch('[0-9a-f]{64}',args.review03_manifest) is not None,'External final review seal required');need(not (A/'ACCEPTANCE.json').exists(),'Acceptance exists; inspect instead of overwriting')
 now=datetime.now(timezone.utc).isoformat();need(fp(D/'PREPUBLICATION_FREEZE.json')['sha256']==FREEZE,'Frozen candidate changed');freeze=load(D/'PREPUBLICATION_FREEZE.json');need(freeze['revision_candidate']==2 and freeze['pr']==919 and freeze['problem_id']=='30002555' and freeze['original_pr_head']==HEAD and len(freeze['files'])==14 and freeze['package_manifest_sha256']==PACKAGE,'Wrong release scope')
 for n,r in freeze['files'].items():need(safe_name(n) and fp(D/n)==r,'Frozen member changed: '+n)
 snapshot=load(A/'ORIGINAL_SNAPSHOT.json');need(snapshot['head']==HEAD and len(snapshot['files'])==27,'Wrong original packet');objects={}
 for n,pin in snapshot['files'].items():
  need(n.startswith(PREFIX),'Wrong original prefix');b=run(['git','show',HEAD+':'+n],True);need(sha(b)==pin and data(A/'original'/n)==b,'Original Git/disk drift: '+n);objects[n]=b
 with zipfile.ZipFile(D/'rotational-veech-source-verification-v1.0.zip') as z:
  names=z.namelist();need(len(names)==134 and len(set(names))==134,'Wrong archive inventory');raw=z.read('PACKAGE_MANIFEST.json');need(sha(raw)==PACKAGE,'Wrong package anchor');m=json.loads(raw);need(len(m['files'])==133 and set(names)==set(m['files'])|{'PACKAGE_MANIFEST.json'},'Wrong payload inventory')
  for i in z.infolist():
   need(safe_name(i.filename) and stat.S_ISREG(i.external_attr>>16),'Nonregular/unsafe archive member')
   if i.filename!='PACKAGE_MANIFEST.json':
    b=z.read(i);need({'bytes':len(b),'sha256':sha(b)}==m['files'][i.filename],'Archive payload drift')
  for n,b in objects.items():need(z.read('original_packet/'+n[len(PREFIX):])==b,'Archive original differs from Git')
  need(z.read('note.pdf')==data(D/'output/pdf/note.pdf'),'Separate/archived PDF mismatch')
 pins={**EARLIER,3:args.review03_manifest};results={};counts={}
 for n,pin in pins.items():results[n],counts[n]=review(n,pin)
 need({x['id'] for x in results[1]['required_issues']}=={'R1','R2'} and {x['id'] for x in results[1]['optional_issues']}=={'O1','O2'},'First-review repair inventory changed');need(results[2]['required_issues']==[] and {x['id'] for x in results[2]['optional_issues']}=={'O3'},'Second-review repair inventory changed')
 latest=results[3];need(latest['required_issues']==[] and latest['optional_issues']==[] and latest['clean_for_preprint'] is True,'Third full review is not clean');need(latest['candidate_pins']['freeze']==FREEZE and latest['candidate_pins']['manifest']==PACKAGE and latest['candidate_pins']['pdf']==freeze['files']['output/pdf/note.pdf']['sha256'],'Latest review cleared different bytes')
 need(datetime.fromisoformat(results[1]['completed_utc'])<datetime.fromisoformat(results[2]['completed_utc'])<datetime.fromisoformat(latest['started_utc'])<datetime.fromisoformat(latest['completed_utc']),'Fresh reviews not sequential')
 for ident in ['R1','R2','O1','O2','O3']:need(latest['prior_issue_resolution'][ident]['verified'] is True,'Prior issue not independently resolved: '+ident)
 prep=load(A/'FUTURE_HELPERS_PREPARATION.json');need(prep['revision']==3 and set(prep['future_helpers'])==set(HELPERS),'Wrong current helper revision')
 for n in HELPERS:
  need(fp(P/n)==prep['future_helpers'][n],'Helper preparation drift');seen=latest['inspected_helper_hashes'][n];need(seen['sha256']==fp(P/n)['sha256'] and seen['bytes']==fp(P/n)['bytes'],'Latest review inspected different helper: '+n)
 seen=latest['inspected_acceptance_gate'];need(seen==fp(Path(__file__)),'Acceptance gate changed since latest review')
 decision=load(A/'PUBLICATION_DISPOSITION.json');need(decision['decision']=='PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE' and decision['no_firstness_current_openness_or_new_general_theorem_claim'] is True and decision['novelty_threshold_invented'] is False,'Disposition changed')
 scope=load(A/'PREMERGE_QUEUE_SCOPE_CHECK.json');need(scope['original_head']==HEAD and scope['non_target_queue_bytes_identical'] is True,'Original queue scope not verified')
 pr=json.loads(run(['gh','pr','view','919','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url,title,body']));need(pr['number']==919 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==HEAD and pr['baseRefName']=='main','Live exact eligibility changed');need(sha(pr['body'].encode())==BODY and pr['title']=='30002555: attributed prescribed-end rotational counterexample; claimed_solved','Reviewed title/body changed')
 headq=run(['git','show',HEAD+':'+QUEUE],True);nontarget,row=without_target(headq);cells=row.decode().split('|');need(cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5','Exact claimed_solved1/5 gate changed');base=scope['merge_base'];need(without_target(run(['git','show',base+':'+QUEUE],True))[0]==nontarget,'Unrelated queue bytes changed in original PR')
 changed=run(['gh','api','repos/AlecKriebel/Math/pulls/919/files','--paginate','--jq','.[].filename']).splitlines();need(set(changed)<=set(snapshot['files'])|{QUEUE},'Unexpected PR changes')
 parent=run(['git','ls-remote','origin','refs/heads/main']).split()[0];run(['git','fetch','--no-write-fetch-head','origin',parent]);source=load(A/'TARGET_IDENTITY_PREFLIGHT.json');catalog=json.loads(run(['git','show',parent+':unsolved_math_prioritization/catalog.json']));targets=[r for r in catalog if str(r['id'])=='30002555'];need(len(targets)==1,'Target source identity ambiguous');target=targets[0];need(target.get('present') is True and target.get('holds')==[] and target['statement_hash']==source['statement_hash'] and target['review_hash']==source['review_hash'],'Current source identity/holds changed')
 record={'utc':now,'accepted':True,'original_pr_head':HEAD,'live_gate_status':'claimed_solved','original_attempt_turns':'1/5','original_recorded_turns_used':1,'native_turns_used_to_record':1,'new_author_proof_search_turns_added':0,'candidate_revision':2,'operational_helper_revision':3,'freeze_sha256':FREEZE,'package_manifest_sha256':PACKAGE,'files':freeze['files'],'exact_claim':latest['strongest_verified_theorem'],'proof_gap':None,'source_scope':'Explicit prescribed matrix-group negative witness X={0,2/3,1}, infinite norm-preserving G generated by (1/5)[[3,-4],[4,3]]; OWR2014Question4 and included countable all-nonplanar subcase of broader RMV2017Question0.2. No exclusion of abstract cyclic groups under other matrices, n1/n2 or finite rotations.','priority':'Explicit attributed application of the complete APV2020preprint/2021journal corollary and explicit ARSVW2023 translation finiteness principle. No new general theorem/construction/classification, firstness or continued-openness assertion. Earlier literal named-question negative answer/witness not established by bounded search.','all_prior_required_and_optional_findings_resolved':True,'full_package_reviews':[{'round':n,'clean_context':True,'manifest_sha256':pins[n],'public_files_authenticated':counts[n],'required_repairs':[x['id'] for x in results[n]['required_issues']],'optional_improvements':[x['id'] for x in results[n]['optional_issues']],'remaining_findings_resolved_by_latest_review':True,'clean_for_publication_under_attributed_framing':n==3,'freeze_sha256':results[n].get('freeze_sha256',results[n].get('candidate_pins',{}).get('freeze'))} for n in (1,2,3)],'AI_assisted':True,'unrefereed':True,'independent_human_peer_review':False,'formal_machine_proof_certification':False,'merge_and_publication_authorized_by_user':True}
 save(A/'FINAL_ACCEPTANCE_GATE.json',{'utc':now,'pr':{k:v for k,v in pr.items() if k!='body'},'corrected_body_sha256':BODY,'remote_main':parent,'source_identity_unchanged':True,'review_manifests':pins,'original_files_unchanged':27,'freeze_sha256':FREEZE,'exact_queue_status':'claimed_solved','non_target_original_queue_bytes_unchanged':True,'reviewed_acceptance_gate':seen})
 (A/'ACCEPTANCE.md').write_text('Accept the exact prescribed-matrix counterexample as an explicitly attributed application of the complete APV2020/2021 corollary and explicit ARSVW2023 finiteness principle. Three sequential NEW whole-package reviews are preserved honestly: rounds1/2 found required/optional repairs, all independently resolved by clean round3. Current frozen14 files, original27 actual Git/disk/archive files, current reviewed helpers, target identity/holds and live claimed_solved1/5 description are unchanged. No mathematical gap or remaining required/optional finding was found by the latest full review. No new general theorem, firstness, continued-openness or separate abstract-group/n1/n2/Jacobs-ladder/finite-area claim is asserted. Publish the exact three-page unrefereed extensively AI-assisted note and verification archive with reviewed metadata; no independent human or formal proof review claimed. Preserve original author1/5 and zero new author proof-search turns. Historical pending records remain accurate at their timestamps and are superseded administratively by this acceptance.\n')
 state=load(P/'CURRENT_STATE.json');state.update(utc=now,phase='PR919_accepted_merge_and_publish_next',active_pr_completion_estimate_percent=96,shard_completion_estimate_percent=(5+.96)/12*100,publication_disposition='Accepted exact prescribed-end rotational witness as attributed application; all prior repairs independently resolved and third whole-package review clean');state['full_package_reviews']['03']='sealed clean; no remaining required or optional issue';save(P/'CURRENT_STATE.json',state)
 for q in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
  with q.open('a') as h:h.write('\n'+now+' — PR919 accepted checkpoint96% workflow/shard49.667%: all three sequential NEW whole-package seals authenticated; rounds1/2 findings honestly preserved and all independently resolved by clean round3. Frozen14/current helpers/original27 actual Git, source identity/holds, live body and exact claimed_solved1/5 unchanged. Attributed APV2020/2021+ARSVW2023 application only; no firstness/current-openness claim. Exact merge and reviewed-metadata publication next.\n')
 save(A/'ACCEPTANCE.json',record)
 print(json.dumps({'accepted':True,'freeze_sha256':FREEZE,'review_files_authenticated':counts,'live_status':'claimed_solved'},indent=2))
if __name__=='__main__':main()
