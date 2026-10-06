#!/usr/bin/env python3
"""R2 final full public readback + independent immutable output seal. Excludes private bodies."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
R=Path(__file__).resolve().parent
EXCLUDED={'OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'}
def now():return datetime.now(timezone.utc).isoformat()
def require(v,s):
 if not v:raise RuntimeError(s)
def pin(p,label=None):
 b=p.read_bytes();return {'path':label or str(p.relative_to(R)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 start=now();require(not any((R/n).exists() for n in EXCLUDED),'Seal only once; never overwrite sealed review outputs')
 files=sorted(p for p in R.rglob('*') if p.is_file() and 'private_scratch' not in p.relative_to(R).parts and p.name not in EXCLUDED)
 require(all(not p.is_symlink() for p in files),'No public symlink')
 required={'REPORT.md','VERDICT.json','INPUT_PINS.json','verify.py','EXECUTION_RECEIPTS.json','REPLAY_execution_envelope.json','REPLAY_verification_normal.json','REPLAY_verification_optimized.json','RESEARCH_LOG.md','READ_SCOPE.json','VISUAL_REVIEW.json','PRIMARY_SOURCE_REVIEW.json','BOOK_SOURCE_AUTHENTICATION.json','seal_outputs.py'}
 require(required<={p.name for p in files},'Required public review artifacts')
 for p in files:
  body=p.read_bytes();body.decode('utf-8')
  if p.suffix=='.json':json.loads(body)
 v=json.loads((R/'VERDICT.json').read_text());require(v['required_findings']==[] and v['verdict']=='PASS_EXACT_IMMUTABLE_CANDIDATE','sealed verdict')
 receipts=json.loads((R/'EXECUTION_RECEIPTS.json').read_text())
 for op in receipts['operations']:
  require(op['actual_PID']>0 and op['UTC_start']<=op['UTC_end'],'real process format')
  for stream in ('stdout','stderr'):
   q=pin(R/op[stream]['path']);require(q['bytes']==op[stream]['bytes'] and q['sha256']==op[stream]['sha256'],'stream byte authentication')
  if op['tag'].startswith('invalid_'):
   result=json.loads((R/op['stderr']['path']).read_text());require(result['actual_verifier_PID']==op['actual_PID'] and op['exit_code']==2 and op['stdout']['bytes']==0,'genuine negative subprocess')
  elif op['tag'].startswith(('r2_','portable_normal','portable_optimized')):
   result=json.loads((R/op['stdout']['path']).read_text());require(result.get('actual_PID',result.get('actual_verifier_PID'))==op['actual_PID'] and op['exit_code']==0,'positive process identity')
 require(len([r for r in receipts['operations'] if r['tag'].startswith('invalid_')])==8,'8 additional captured negative processes')
 normal=json.loads((R/'r2_normal_stdout.txt').read_text());opt=json.loads((R/'r2_optimized_stdout.txt').read_text())
 require(normal['explicit_guards']==opt['explicit_guards']==v['review_guard_count']==21011,'final own normal/-O counts')
 require(normal['optimization']==0 and opt['optimization']==1,'final own modes')
 for key in ('custody','independent_chords','independent_odd_star_cycles','invalid_average_transfer_counterexample'):
  require(normal[key]==opt[key],'stable independent normal/-O evidence')
 replay=json.loads((R/'REPLAY_execution_envelope.json').read_text());require(replay['positive_runs']==2 and replay['required_failed_subprocess_controls']==8 and len(replay['operations'])==10,'portable genuine runner envelope')
 runner=next(r for r in receipts['operations'] if r['tag']=='portable_runner');require(replay['actual_runner_PID']==runner['actual_PID'],'real replay runner')
 for op in replay['operations']:
  if op['invalid_control'] is not None:
   r=op['verified_rejection'];raw=(json.dumps({'status':r['status'],'reason':r['reason'],'actual_verifier_PID':r['actual_verifier_PID'],'optimization_level':r['optimization_level']})+'\n').encode()
   require(op['exit_code']==2 and r['actual_verifier_PID']==op['child_PID'] and hashlib.sha256(raw).hexdigest()==op['stderr']['sha256'] and len(raw)==op['stderr']['bytes'],'replay negative exact stream')
  else:
   name='REPLAY_verification_optimized.json' if op['optimization'] else 'REPLAY_verification_normal.json';b=(R/name).read_bytes();r=json.loads(b)
   require(op['exit_code']==0 and r['actual_verifier_PID']==op['child_PID'] and len(b)==op['stdout']['bytes'] and hashlib.sha256(b).hexdigest()==op['stdout']['sha256'],'replay positive exact stream')
 candidate=json.loads((R/'INPUT_PINS.json').read_text())
 for row in candidate['candidate_files']+candidate['candidate_research_inputs']+candidate['primary_and_boundary_inputs']:
  q=pin(Path(row['path']),row['path']);require(q['bytes']==row['bytes'] and q['sha256']==row['sha256'],'inputs unchanged at seal')
 q=pin(Path(candidate['external_candidate_seal']['path']),candidate['external_candidate_seal']['path']);require(q==candidate['external_candidate_seal'],'external seal unchanged at closure')
 rows=[pin(p) for p in files]
 manifest={'schema':'r2-public-output-manifest/v1','UTC':now(),'actual_manifest_builder_PID':os.getpid(),'files':rows,'excluded_files':sorted(EXCLUDED),'excluded_private_prefixes':['private_scratch/'],'scope':'Original R2 report, derivation, evidence pins and real execution receipts; no third-party source bodies, extracted PDF pages or scratch copies.'}
 (R/'OUTPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for row in rows:require(pin(R/row['path'])==row,'full public readback hash '+row['path'])
 receipt={'schema':'r2-independent-output-seal/v1','UTC_start':start,'UTC_end':now(),'actual_sealer_PID':os.getpid(),'argv':[sys.executable]+sys.argv,'cwd':str(Path.cwd()),'output_manifest':pin(R/'OUTPUT_MANIFEST.json'),'public_file_count':len(rows),'public_total_bytes':sum(r['bytes'] for r in rows),'full_public_readback_passed':True,'all_candidate_and_input_bytes_unchanged':True,'normal_optimized_own_explicit_guards':21011,'portable_runner_real_failed_processes':8,'additional_real_failed_processes_raw_streams':8,'earlier_R1_review_read':False,'review_completion_percent':100,'publication_permission_issued':False,'immutable_after_seal':True,'excluded_files':sorted(EXCLUDED),'excluded_private_prefixes':['private_scratch/']}
 (R/'SEAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 require(json.loads((R/'SEAL_RECEIPT.json').read_text())==receipt,'receipt readback')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
