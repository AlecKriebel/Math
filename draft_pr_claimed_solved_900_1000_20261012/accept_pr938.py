#!/usr/bin/env python3
"""Accept only an externally pinned PR938 freeze after sequential NEW reviews."""
import argparse,hashlib,json,re,stat,subprocess,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;ROOT=P.parent;A=P/'audits/pr938_30003634';D=A/'publication'
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
KEY='30003634';PREFIX='unsolved_math_prioritization/attempts/'+KEY+'/'
QUEUE='unsolved_math_prioritization/QUEUE.md'
HELPERS=['accept_pr938.py','merge_pr938.py','run_pr938_zenodo.py','append_pr938_tracker.py','update_pr938_publication_ledger.py','finalize_pr938_and_gate_next.py']
def need(ok,label):
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def data(p):
 need(stat.S_ISREG(p.lstat().st_mode),'Nonregular artifact');return p.read_bytes()
def fp(p):
 b=data(p);return {'bytes':len(b),'sha256':sha(b)}
def strict_json(raw):
 def pairs(items):
  result={}
  for key,value in items:need(key not in result,'Duplicate JSON key');result[key]=value
  return result
 def invalid(value):raise RuntimeError('Nonfinite JSON constant '+value)
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=invalid)
def load(p):return strict_json(data(p))
def run(args,binary=False):return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=not binary).stdout
def safe(n):
 return type(n) is str and '\\' not in n and '\0' not in n and not PurePosixPath(n).is_absolute() and PurePosixPath(n).as_posix()==n and all(s not in ('','.','..') for s in n.split('/'))
def rest(raw):
 lines=raw.splitlines(keepends=True);hits=[s for s in lines if b'| 30003634 /' in s];need(len(hits)==1,'Ambiguous target row');return b''.join(s for s in lines if s!=hits[0]),hits[0]
def validate_review_sequence(specs):
 need(type(specs) is list and len(specs)>=2,'At least two NEW review rounds required')
 for expected,spec in enumerate(specs,1):
  number,pin=spec.split(':')
  need(number==f'{expected:02d}' and re.fullmatch('[0-9a-f]{64}',pin) is not None,'Canonical complete consecutive ordered review history starting at01 required')
def validate_review_inventory(mapping):
 records=mapping['files'];allowed=mapping['explicit_public_allowlist']
 mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json'}
 need(type(records) is dict and bool(records) and mandatory<=set(records),'Missing authenticated decisive verdict or mandatory review evidence')
 need(type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in records,'Review inventory not explicit/self-excluded')
 return records
def authenticate_review_records(folder,mapping):
 records=validate_review_inventory(mapping)
 for n,r in records.items():
  need(safe(n) and type(r) is dict and set(r)=={'bytes','sha256'} and type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) is not None and fp(folder/n)==r,'Review payload drift/schema')
 for name in ['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json']:
  raw=data(folder/name);need(records[name]['bytes']>0 and bool(raw.decode('utf-8').strip()),'Empty mandatory review evidence '+name)
  if name.endswith('.json'):need(type(strict_json(raw)) is dict and bool(strict_json(raw)),'Mandatory JSON evidence must be a nonempty object')
  else:need(any(c.isalpha() for c in raw.decode('utf-8')),'Mandatory audit/log lacks text')
 return records
def exact(a,b):
 return json.dumps(a,sort_keys=True,allow_nan=False,separators=(',',':'))==json.dumps(b,sort_keys=True,allow_nan=False,separators=(',',':'))
def alias(record,*names):
 values=[record[name] for name in names if name in record]
 need(bool(values) and all(exact(value,values[0]) for value in values),'Missing or contradictory historical evidence field aliases')
 return values[0]
def utc(value):
 need(type(value) is str,'Missing evidence timestamp');stamp=datetime.fromisoformat(value.replace('Z','+00:00'));need(stamp.tzinfo is not None and stamp.utcoffset()==timezone.utc.utcoffset(stamp),'Evidence timestamp must be UTC');return stamp
def validate_review_evidence(folder,result,freeze,base):
 """Crosscheck recorded provenance; this does not certify execution or proof."""
 pins=result['candidate_pins'];manifest=freeze['package_manifest_sha256']
 need(pins['manifest']==manifest and pins['pdf']==freeze['files']['output/pdf/note.pdf']['sha256'],'Review candidate identities disagree')
 for name,record in freeze['files'].items():need(safe(name) and fp(base/name)==record,'Reviewed candidate file no longer authenticated')
 for name,record in freeze['future_helpers'].items():
  source=P/name if base==D else base/'future_helpers'/name
  need(safe(name) and fp(source)==record,'Reviewed helper copy no longer authenticated')
 snap=load(A/'ORIGINAL_SNAPSHOT.json');need(snap['head']==HEAD and len(snap['files'])==44,'Wrong expected original inventory')
 expected={}
 for name,pin in snap['files'].items():
  raw=data(A/'original'/name);need(sha(raw)==pin,'Expected original bytes changed')
  expected[name]={'sha256':pin,'bytes':len(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
 started=utc(result['started_utc']);completed=utc(result['completed_utc']);times=[]
 built=load(base/'BUILD_RECEIPT.json')
 for index,name in enumerate(['AUTHENTICATION_START.json','AUTHENTICATION_END.json']):
  record=load(folder/name);need(record['original_pr_head']==HEAD and record['freeze_sha256']==pins['freeze'] and alias(record,'package_manifest_sha256','manifest_sha256')==manifest,'Cross-target/stale authentication evidence')
  need(exact(record['future_helpers'],freeze['future_helpers']) and exact(result['inspected_helper_hashes'],freeze['future_helpers']),'Authentication helper pins disagree')
  need(type(record['payloads']) is int and record['payloads']==built['payload_files'] and type(record['archive_members']) is int and record['archive_members']==built['zip_members'],'Authentication archive inventory disagrees')
  if 'candidate_files' in record:need(exact(record['candidate_files'],freeze['files']),'Authentication candidate map disagrees')
  else:need(type(record['frozen_files']) is int and record['frozen_files']==len(freeze['files']),'Authentication frozen-file count disagrees')
  if 'pdf_sha256' in record:need(record['pdf_sha256']==pins['pdf'],'Authentication paper pin disagrees')
  originals=alias(record,'originals','all_actual_git_blob_mode_disk_archive_checks')
  need(type(originals) is dict and set(originals)==set(expected),'Incomplete or cross-target original authentication map')
  for path,want in expected.items():
   item=originals[path];need(type(item) is dict and type(item.get('bytes')) is int and all(item.get(k)==v for k,v in want.items()) and item.get('git_mode')=='100644' and item.get('disk_and_archive_match') is True,'Wrong original authentication fingerprint/mode')
   if index==1:need(item.get('disk_mode')=='0644' and item.get('archive_mode')=='100644','Endpoint original disk/archive modes missing')
  if index==1 or 'status' in record:need(record.get('status')=='PASS','Failed authentication endpoint')
  else:need(record.get('label')=='START','Unrecognized historical start record')
  times.append(utc(record['utc']))
 need(started<=times[0]<=times[1]<=completed,'Authentication chronology outside review interval')
 cold=load(folder/'COLD_REPLAY.json');need(cold.get('status')=='PASS' and cold.get('package_manifest_sha256')==manifest and cold.get('externally_pinned_verifier_sha256')==freeze['files']['verify_package.py']['sha256'] and alias(cold,'cold_extraction','fresh_archive_extraction') is True,'Failed/stale/non-cold replay evidence')
 need(times[0]<=utc(cold['utc'])<=times[1],'Cold replay not before final authentication')
 rows=cold.get('modes');need(type(rows) is list and len(rows)==4,'Four actual outer modes required')
 for row,label,optimization in zip(rows,['normal','O','OO','env2'],[0,1,2,2]):
  # Historical round02 calls the same inherited environment probe environment2.
  reported_mode='env2' if row.get('mode')=='environment2' else row.get('mode')
  observed=alias(row,'observed_outer_optimization','actual_outer_optimization');need(reported_mode==label and type(observed) is int and observed==optimization,'Wrong actual optimization mode evidence')
  if 'returncode' in row:need(type(row['returncode']) is int and row['returncode']==0,'Failed cold child process')
  replay=alias(row,'receipt','result');saved=load(base/('PACKAGE_REPLAY_'+label+'.json'))
  need(type(replay) is dict and exact(replay,saved),'Cold receipt differs from exact reviewed author/planar/Meyer replay')
  need(replay.get('status')=='PASS' and type(replay.get('pr')) is int and replay['pr']==938 and replay.get('problem_id')==KEY and replay.get('package_manifest_sha256')==manifest and type(replay.get('original_files_unchanged')) is int and replay['original_files_unchanged']==44 and type(replay.get('worker_optimization')) is int and replay['worker_optimization']==0 and replay.get('exact_json_type_comparison') is True and replay.get('floating_tolerance_used') is False,'Replay status/target/worker claims disagree')
  need(exact(replay['child_execution_guards'],[{'script':s,'optimization':0,'isolated':1} for s in ['original_packet/original/verify.py','reviews/goeritz_family/independent_goeritz.py','reviews/meyer_algebra_family/reproduce.py']]),'Cold checker execution guards disagree')
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
  folder=A/'reviews'/f'full_package_{int(number):02d}';need(fp(folder/'MANIFEST.json')['sha256']==pin,'Review seal mismatch');mapping=load(folder/'MANIFEST.json');records=authenticate_review_records(folder,mapping)
  result=load(folder/'RESULT.json');need(result['pr']==938 and result['problem_id']==KEY and result['original_pr_head']==HEAD,'Cross-target review')
  need(result['clean_context'] is True and result['full_reproducer_completed'] is True,'Fresh context/full reproduction absent')
  start=datetime.fromisoformat(result['started_utc']);end=datetime.fromisoformat(result['completed_utc']);need(start<end and (last_completion is None or last_completion<start),'Reviews not sequential and new');last_completion=end
  review_freeze=freeze;review_base=D
  if result['candidate_pins']['freeze']!=args.freeze:
   old_folder=D/'reviewed_candidates'/('candidate'+str(result['candidate_revision']).zfill(2))
   need(fp(old_folder/'PREPUBLICATION_FREEZE.json')['sha256']==result['candidate_pins']['freeze'],'Prior candidate snapshot missing')
   review_freeze=load(old_folder/'PREPUBLICATION_FREEZE.json');review_base=old_folder
   for n,r in review_freeze['files'].items():need(safe(n) and fp(old_folder/n)==r,'Prior candidate snapshot drift')
  need(result['candidate_pins']['manifest']==review_freeze['package_manifest_sha256'],'Review cleared different package')
  need(result['inspected_helper_hashes']==review_freeze['future_helpers'],'Review inspected different helpers')
  validate_review_evidence(folder,result,review_freeze,review_base)
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
