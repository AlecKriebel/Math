#!/usr/bin/env python3
"""Seal this static review only. No native, Git or service mutation."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
O=Path(__file__).resolve().parent
A=O.parent
C=A.parents[2]
D=A/'native_publication_integration_plan_20261006'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(name,obj): (O/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def pin(path):
    b=path.read_bytes()
    return {'path':str(path.relative_to(O)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
scope=json.loads((O/'SOURCE_READ_SCOPE.json').read_bytes())
normal=json.loads((O/'RESULTS_NORMAL.json').read_bytes())
optimized=json.loads((O/'RESULTS_OPTIMIZED.json').read_bytes())
process_receipts=[]
def git(args):
    start=utc(); proc=subprocess.Popen(['/usr/bin/git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try: out,err=proc.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill(); out,err=proc.communicate(); raise RuntimeError('Final bounded read timed out')
    process_receipts.append({'argv':['/usr/bin/git',*args],'cwd':str(C),'PID':proc.pid,'UTC_start':start,
      'UTC_end':utc(),'exit_code':proc.returncode,'stdout':out.decode(errors='replace'),'stderr':err.decode(errors='replace')})
    if proc.returncode: raise RuntimeError('Read-only Git failed')
    return out
head=git(['rev-parse','HEAD']).decode().strip()
branch=git(['symbolic-ref','--short','HEAD']).decode().strip()
native_diff=git(['diff','--name-only',scope['frozen_native_source_parent'],head,'--','unsolved_math_prioritization/'])
if branch!='main' or native_diff: raise RuntimeError('Native review source changed before seal')
dump('FINAL_READBACK.json',{'UTC':utc(),'actual_operator_PID':os.getpid(),'HEAD':head,'branch':branch,
   'frozen_native_source_parent':scope['frozen_native_source_parent'],'native_diff_empty':not native_diff,
   'read_only_process_receipts':process_receipts})
writer=json.loads((D/'OUTPUT_MANIFEST.json').read_bytes())
for e in writer['files']:
    b=(D/e['path']).read_bytes()
    if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:
        raise RuntimeError('Writer source changed at seal: '+e['path'])
verdict={'schema':'pr108-native-helper-static-adversary-verdict/v1','UTC':utc(),'actual_operator_PID':os.getpid(),
  'reviewed_helper_sha256':normal['helper_sha256'],'sealed_writer_file_count_reverified':len(writer['files']),
  'frozen_native_source_parent':scope['frozen_native_source_parent'],'final_observed_main_parent':head,
  'static_review_completion_percent':100,'native_execution_completion_percent':0,
  'verdict':'REQUIRED_REPAIRS_BEFORE_COMMISSIONING','native_integration_clearance':False,
  'pre_execution_adversary_clearance':False,'actual_future_configuration_reviewed':False,
  'manuscript_whole_package_R1':False,'manuscript_whole_package_R2':False,
  'normal_and_optimized_original_writer_tests_per_mode':normal['original_writer_fixture_tests'],
  'additional_checks_per_mode':len(normal['additional_controls_or_counterexamples']),
  'counterexample_entries_per_mode':sum(e['status']=='counterexample_reproduced' for e in normal['additional_controls_or_counterexamples']),
  'normal_and_optimized_check_names_agree':[e['name'] for e in normal['additional_controls_or_counterexamples']]==[e['name'] for e in optimized['additional_controls_or_counterexamples']],
  'required_findings':[
    {'id':'F01','priority':'high','title':'Actual post-Zenodo Google Workspace CLI Sheet receipt absent'},
    {'id':'F02','priority':'high','title':'Exact execution configuration not bound to independent review'},
    {'id':'F03','priority':'medium','title':'CSV line-span replacement corrupts Unicode/control-separator unrelated fields'},
    {'id':'F04','priority':'medium','title':'Aggregate capacity and process bounds incomplete'},
    {'id':'F05','priority':'medium','title':'Original authentication path map and selected-row hash not enforced'},
    {'id':'F06','priority':'low','title':'Eligibility drift explanation incomplete despite safe baseline restoration'}],
  'prior_conclusions_frozen':{'mathematics':'Existing root scoped 100% clearance; not independently reproved here',
       'priority':'Existing root scoped note preparation supported; package/publication not cleared'},
  'actual_native_prepare_assess_backend_export_install_Git_index_remote_service_or_cache_write_executed':False,
  'external_communication_or_outreach_prepared':False,'new_central_proof_search_turns':0}
dump('VERDICT.json',verdict)
with (O/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n- '+utc()+': Pure normal and optimized runs both pass the writer\'s 13 fixtures and reproduce 13 adversary controls/counterexamples (nine counterexample entries). Current original manifests are correct; the extracted guard nevertheless accepts swapped historical names and a false selected-row hash. Final bounded main readback has no native source change from the frozen source parent. Completion estimate: 100% static review; 0% native execution/publication. Verdict: required repairs before commissioning. No manuscript R1/R2 credit.\n')
excluded={'OUTPUT_MANIFEST.json','SHA256SUMS','SEAL.json'}
files=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in excluded]
dump('OUTPUT_MANIFEST.json',{'schema':'pr108-native-helper-static-adversary-output-manifest/v1','UTC':utc(),
    'actual_operator_PID':os.getpid(),'excluded_self_seal_and_checksum_files':sorted(excluded),'files':files,
    'total_bytes':sum(e['bytes'] for e in files)})
sumfiles=files+[pin(O/'OUTPUT_MANIFEST.json')]
(O/'SHA256SUMS').write_text(''.join(e['sha256']+'  '+e['path']+'\n' for e in sumfiles))
dump('SEAL.json',{'schema':'pr108-native-helper-static-adversary-seal/v1','UTC':utc(),'actual_operator_PID':os.getpid(),
  'output_manifest_pin':pin(O/'OUTPUT_MANIFEST.json'),'checksum_file_pin':pin(O/'SHA256SUMS'),
  'verdict_pin':pin(O/'VERDICT.json'),'report_pin':pin(O/'REPORT.md'),'file_count':len(files),
  'total_manifested_bytes':sum(e['bytes'] for e in files),'reviewed_writer_helper_pin':scope['writer_helper_pin'],
  'static_review_completion_percent':100,'native_execution_clearance':False})
print(json.dumps({'UTC':utc(),'PID':os.getpid(),'file_count':len(files),'total_bytes':sum(e['bytes'] for e in files),
 'verdict':'REQUIRED_REPAIRS_BEFORE_COMMISSIONING','SEAL':pin(O/'SEAL.json')}))
