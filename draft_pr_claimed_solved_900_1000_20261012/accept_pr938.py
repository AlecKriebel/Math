#!/usr/bin/env python3
"""Accept only an externally pinned PR938 freeze after sequential NEW reviews."""
import argparse,hashlib,json,re,stat,subprocess,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;ROOT=P.parent;A=P/'audits/pr938_30003634';D=A/'publication'
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
KEY='30003634';PREFIX='unsolved_math_prioritization/attempts/'+KEY+'/'
QUEUE='unsolved_math_prioritization/QUEUE.md'
HELPERS=['accept_pr938.py','merge_pr938.py','run_pr938_zenodo.py','append_pr938_tracker.py','update_pr938_publication_ledger.py']
def need(ok,label):
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def data(p):
 need(stat.S_ISREG(p.lstat().st_mode),'Nonregular artifact');return p.read_bytes()
def fp(p):
 b=data(p);return {'bytes':len(b),'sha256':sha(b)}
def load(p):return json.loads(data(p))
def run(args,binary=False):return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=not binary).stdout
def safe(n):
 return type(n) is str and '\\' not in n and '\0' not in n and not PurePosixPath(n).is_absolute() and PurePosixPath(n).as_posix()==n and all(s not in ('','.','..') for s in n.split('/'))
def rest(raw):
 lines=raw.splitlines(keepends=True);hits=[s for s in lines if b'| 30003634 /' in s];need(len(hits)==1,'Ambiguous target row');return b''.join(s for s in lines if s!=hits[0]),hits[0]
def validate_review_sequence(specs):
 need(type(specs) is list and len(specs)>=2,'At least two NEW review rounds required')
 for expected,spec in enumerate(specs,1):
  number,pin=spec.split(':')
  need(number.isdigit() and int(number)==expected and re.fullmatch('[0-9a-f]{64}',pin) is not None,'Complete consecutive ordered review history starting at01 required')
def validate_review_inventory(mapping):
 records=mapping['files'];allowed=mapping['explicit_public_allowlist']
 mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json'}
 need(type(records) is dict and bool(records) and mandatory<=set(records),'Missing authenticated decisive verdict or mandatory review evidence')
 need(type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in records,'Review inventory not explicit/self-excluded')
 return records
def authenticate_review_records(folder,mapping):
 records=validate_review_inventory(mapping)
 for n,r in records.items():need(safe(n) and fp(folder/n)==r,'Review payload drift')
 return records
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--freeze',required=True);ap.add_argument('--review',action='append',required=True,help='ROUND:EXTERNALLY_REPORTED_MANIFEST_SHA256');args=ap.parse_args()
 validate_review_sequence(args.review)
 need(not (A/'ACCEPTANCE.json').exists(),'Existing acceptance; inspect instead of overwriting')
 need(re.fullmatch('[0-9a-f]{64}',args.freeze) is not None,'External freeze pin required');need(fp(D/'PREPUBLICATION_FREEZE.json')['sha256']==args.freeze,'Freeze drift')
 freeze=load(D/'PREPUBLICATION_FREEZE.json');need(freeze['pr']==938 and freeze['problem_id']==KEY and freeze['original_pr_head']==HEAD,'Wrong freeze target')
 for n,r in freeze['files'].items():need(safe(n) and fp(D/n)==r,'Frozen member drift '+n)
 need(set(freeze['future_helpers'])==set(HELPERS),'Unexpected helper inventory')
 for n,r in freeze['future_helpers'].items():need(fp(P/n)==r,'Reviewed helper changed '+n)
 snap=load(A/'ORIGINAL_SNAPSHOT.json');need(snap['head']==HEAD and len(snap['files'])==44,'Original scope changed');original={}
 for n,pin in snap['files'].items():
  need(n.startswith(PREFIX),'Wrong original prefix');b=run(['git','show',HEAD+':'+n],True);need(sha(b)==pin and data(A/'original'/n)==b,'Actual original Git/disk mismatch');original[n]=b
 archive=D/'deep-derived-pure-braids-source-verification-v1.0.zip'
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();raw=z.read('PACKAGE_MANIFEST.json');need(sha(raw)==freeze['package_manifest_sha256'],'Wrong archive anchor');m=json.loads(raw)
  need(len(names)==len(set(names)) and set(names)==set(m['files'])|{'PACKAGE_MANIFEST.json'},'Closed archive inventory')
  for i in z.infolist():
   need(safe(i.filename) and stat.S_ISREG(i.external_attr>>16),'Nonregular archive member')
   if i.filename!='PACKAGE_MANIFEST.json':
    b=z.read(i);need({'bytes':len(b),'sha256':sha(b)}==m['files'][i.filename],'Archive payload drift')
  for n,b in original.items():need(z.read('original_packet/'+n[len(PREFIX):])==b,'Archive original differs from Git')
  need(z.read('note.pdf')==data(D/'output/pdf/note.pdf'),'Separate PDF mismatch')
 reviews=[];prior_ids=set();last_completion=None
 for spec in args.review:
  number,pin=spec.split(':');need(number.isdigit() and re.fullmatch('[0-9a-f]{64}',pin) is not None,'Malformed external review pin')
  folder=A/'reviews'/('full_package_'+number.zfill(2));need(fp(folder/'MANIFEST.json')['sha256']==pin,'Review seal mismatch');mapping=load(folder/'MANIFEST.json');records=authenticate_review_records(folder,mapping)
  result=load(folder/'RESULT.json');need(result['pr']==938 and result['problem_id']==KEY and result['original_pr_head']==HEAD,'Cross-target review')
  need(result['clean_context'] is True and result['full_reproducer_completed'] is True,'Fresh context/full reproduction absent')
  start=datetime.fromisoformat(result['started_utc']);end=datetime.fromisoformat(result['completed_utc']);need(start<end and (last_completion is None or last_completion<start),'Reviews not sequential and new');last_completion=end
  review_freeze=freeze
  if result['candidate_pins']['freeze']!=args.freeze:
   old_folder=D/'reviewed_candidates'/('candidate'+str(result['candidate_revision']).zfill(2))
   need(fp(old_folder/'PREPUBLICATION_FREEZE.json')['sha256']==result['candidate_pins']['freeze'],'Prior candidate snapshot missing')
   review_freeze=load(old_folder/'PREPUBLICATION_FREEZE.json')
   for n,r in review_freeze['files'].items():need(safe(n) and fp(old_folder/n)==r,'Prior candidate snapshot drift')
  need(result['candidate_pins']['manifest']==review_freeze['package_manifest_sha256'],'Review cleared different package')
  need(result['inspected_helper_hashes']==review_freeze['future_helpers'],'Review inspected different helpers')
  issues=result['required_issues']+result['optional_issues'];need(all(type(x.get('id')) is str for x in issues),'Issue IDs missing')
  reviews.append({'round':int(number),'manifest_sha256':pin,'public_files_authenticated':len(records),'required_repairs':result['required_issues'],'optional_improvements':result['optional_issues'],'completed_utc':result['completed_utc']})
  if int(number)!=int(args.review[-1].split(':')[0]):prior_ids.update(x['id'] for x in issues)
 latest=result
 need(latest['candidate_pins']['freeze']==args.freeze,'Latest review did not clear current freeze')
 need(len(reviews)>=2 and len({r['round'] for r in reviews})==len(reviews),'At least two distinct sequential NEW reviews required')
 need(latest['required_issues']==[] and latest['optional_issues']==[] and latest['clean_for_preprint'] is True and latest['mathematical_remaining_gap_for_stated_theorem'] is None,'Latest full review not clean')
 need(all(latest.get('prior_issue_resolution',{}).get(i,{}).get('verified') is True for i in prior_ids),'Prior required/optional issue unresolved')
 disposition=load(A/'PUBLICATION_DISPOSITION.json');need(disposition['decision']=='PREPARE_ALL_FINITE_DERIVED_DEPTH_RESEARCH_NOTE' and disposition['no_firstness_current_openness_or_new_general_quasimorphism_theorem_claim'] is True,'Disposition drift')
 ledger=load(A/'strengthening/unsolved_math_prioritization/attempts/30003634/ATTEMPT_LEDGER.json');need(ledger['turns_used']==2 and ledger['candidate_turn']==2 and load(A/'NEW_PRIORITY_MECHANISM_LEDGER.json')['configured_budget']==5,'Native accounting drift')
 pr=json.loads(run(['gh','pr','view','938','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,url']))
 need(pr['number']==938 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==HEAD and pr['baseRefName']=='main','Live eligible head drift')
 need(sha(pr['body'].encode())==freeze['pr_description_sha256'],'Reviewed PR description drift')
 before,row=rest(run(['git','show',HEAD+':'+QUEUE],True));cells=row.decode().split('|');need(cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5','Exact original claimed_solved1/5 gate changed')
 parent=run(['git','ls-remote','origin','refs/heads/main']).split()[0];run(['git','fetch','--no-write-fetch-head','origin',parent]);base=run(['git','merge-base',HEAD,parent]).strip();need(rest(run(['git','show',base+':'+QUEUE],True))[0]==before,'Original PR changes other queue rows')
 changed=run(['gh','api','repos/AlecKriebel/Math/pulls/938/files','--paginate','--jq','.[].filename']).splitlines();need(set(changed)<=set(snap['files'])|{QUEUE},'Unexpected PR scope')
 source=load(A/'TARGET_IDENTITY_PREFLIGHT.json');catalog=json.loads(run(['git','show',parent+':unsolved_math_prioritization/catalog.json']));targets=[x for x in catalog if str(x['id'])==KEY];need(len(targets)==1,'Current source ambiguous');target=targets[0]
 need(target.get('present') is True and target.get('holds')==[] and target['statement_hash']==source['statement_hash'] and target['review_hash']==source['review_hash'],'Current source identity/holds changed')
 now=datetime.now(timezone.utc).isoformat();accepted={'utc':now,'accepted':True,'pr':938,'problem_id':KEY,'original_pr_head':HEAD,'live_gate_status':'claimed_solved','original_attempt_turns':'1/5 preserved','native_turns_used_to_record':2,'new_author_proof_search_turns_added':1,'freeze_sha256':args.freeze,'files':freeze['files'],'future_helpers':freeze['future_helpers'],'package_manifest_sha256':freeze['package_manifest_sha256'],'exact_claim':latest['strongest_verified_theorem'],'proof_gap':None,'priority':'Bounded primary search; prior general tools credited; no complete earlier braid-solvability answer established; no firstness/current-open/new-general-quasimorphism claim','full_package_reviews':reviews,'all_prior_required_and_optional_findings_resolved':True,'AI_assisted':True,'unrefereed':True,'independent_human_peer_review':False,'formal_machine_proof_certification':False,'merge_and_publication_authorized_by_user':True}
 (A/'FINAL_ACCEPTANCE_GATE.json').write_text(json.dumps({'utc':now,'pr':{k:v for k,v in pr.items() if k!='body'},'remote_main':parent,'source_identity_unchanged':True,'original44_actual_Git_disk_archive_unchanged':True,'other_original_queue_rows_unchanged':True,'exact_queue_status':'claimed_solved','original_observed_turns':'1/5','current_known_turns':'2/5'},indent=2)+'\n')
 (A/'ACCEPTANCE.json').write_text(json.dumps(accepted,indent=2)+'\n');print(json.dumps({'accepted':True,'freeze_sha256':args.freeze,'review_count':len(reviews),'original_files_verified':44}))
if __name__=='__main__':main()
