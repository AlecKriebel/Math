#!/usr/bin/env python3
"""Seal explicit small public preparation payload, leaving all native scratch private."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, zipfile
import protocol as p
D=pathlib.Path(__file__).resolve().parent;A=D.parent;C=A.parents[2]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,value):(D/name).write_bytes(p.canonical(value))
review=p.loads((D/'protocol_adversary_20261006/REVIEW.json').read_bytes())
custody=p.loads((D/'FIXTURE_CUSTODY.json').read_bytes())
program=(D/'protocol.py').read_bytes();tests=(D/'test_protocol.py').read_bytes()
p.need(review['source_sha256']==p.sha(program) and review['fixture_support_sha256']==p.sha(tests) and
       review['unexpected_outcomes']==[] and review['review_completion_percent']==100,'Final independently reviewed source pin')
p.need(custody['program_sources']['protocol.py']==p.pin(program) and custody['program_sources']['test_protocol.py']==p.pin(tests),
       'Authoritative normal/optimized source pins')
for role in ['NORMAL','OPTIMIZED']:
    result=p.loads((D/(role+'_FIXTURE_RESULTS.json')).read_bytes())
    p.need(result['tests_run']==36 and result['errors']==0 and result['failures']==0 and result['synthetic_fixture_only'] is True and
           result['actual_service_calls']==0 and result['native_assess_executions']==0,'Final fixture results')
template=(D/'EXECUTION_INPUTS_TEMPLATE_DO_NOT_USE_AS_EVIDENCE.json').read_bytes()
try:p.validate_execution(template,{}, {},{},utc())
except ValueError:pass
else:raise ValueError('Template unexpectedly accepted')
journal_path=pathlib.Path(custody['actual_process_journal'])
p.need(journal_path.is_relative_to(D) and p.pin(journal_path.read_bytes())==custody['journal'],'Actual fixture journal custody')
public_names=['PLAN.md','protocol.py','test_protocol.py','capture_fixture_runs.py','write_protocol_metadata.py',
 'INPUT_OUTPUT_PROTOCOL.json','PREPARATION_STATUS.json','RESEARCH_LOG.md',
 'EXECUTION_INPUTS_TEMPLATE_DO_NOT_USE_AS_EVIDENCE.json','NORMAL_FIXTURE_RESULTS.json','OPTIMIZED_FIXTURE_RESULTS.json',
 'FIXTURE_CUSTODY.json','protocol_adversary_20261006/REVIEW.md','protocol_adversary_20261006/REVIEW.json',
 'protocol_adversary_20261006/final_current_COMMAND_ENVELOPES.json',str(journal_path.relative_to(D)),'seal_preparation.py']
files=[]
for name in public_names:
    path=D/name;p.need(path.is_file() and not path.is_symlink(),'Explicit regular public file')
    p.need(all(not parent.is_symlink() for parent in path.parents),'No public symlink ancestors')
    files.append({'path':name,**p.pin(path.read_bytes())})
manifest={'schema':'pr110-offline-native-preparation-public-manifest/v1','UTC':utc(),'PR':110,'problem_id':5100032,
 'files':files,'public_file_count':len(files),'public_bytes':sum(x['bytes'] for x in files),
 'source_sha256':p.sha(program),'fixture_support_sha256':p.sha(tests),
 'preparation_percent':100,'native_acceptance_or_export_executed':False,'service_calls':0,'new_central_proof_search_turns':0,
 'private_original_native_context_and_probe_bodies_included':False,'actual_future_execution_inputs_included':False}
write('PUBLIC_PAYLOAD_MANIFEST.json',manifest)
payload=D/'PUBLIC_PREPARATION_PAYLOAD.zip'
with zipfile.ZipFile(payload,'w',compression=zipfile.ZIP_DEFLATED) as archive:
    for name in public_names:archive.writestr(name,(D/name).read_bytes())
    archive.writestr('PUBLIC_PAYLOAD_MANIFEST.json',(D/'PUBLIC_PAYLOAD_MANIFEST.json').read_bytes())
with zipfile.ZipFile(payload) as archive:
    p.need(set(archive.namelist())==set(public_names)|{'PUBLIC_PAYLOAD_MANIFEST.json'} and
           len(archive.namelist())==len(public_names)+1,'Exact public archive inventory')
    for name in public_names:p.need(archive.read(name)==(D/name).read_bytes(),'Public archive file readback')
    p.need(archive.read('PUBLIC_PAYLOAD_MANIFEST.json')==(D/'PUBLIC_PAYLOAD_MANIFEST.json').read_bytes(),'Manifest readback')
git_records=[];env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC','GIT_CONFIG_NOSYSTEM':'1',
                   'GIT_CONFIG_GLOBAL':'/dev/null','GIT_OPTIONAL_LOCKS':'0','GIT_NO_REPLACE_OBJECTS':'1'}
for args in [('symbolic-ref','--short','HEAD'),('rev-parse','HEAD')]:
    start=utc();proc=subprocess.Popen(['/usr/bin/git','-c','core.fsmonitor=false',*args],cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=proc.communicate(timeout=10)
    p.need(proc.returncode==0,'Closing read-only Git context')
    git_records.append({'argv':proc.args,'cwd':str(C),'PID':proc.pid,'UTC_start':start,'UTC_end':utc(),'exit_code':proc.returncode,
      'stdout':p.pin(out),'stderr':p.pin(err),'context_only_stdout':out.decode().strip(),'Git_mutation':False})
p.need(git_records[0]['context_only_stdout']=='main','Stay main')
receipt={'schema':'pr110-offline-preparation-seal/v1','UTC':utc(),'actual_sealer_PID':os.getpid(),
 'manifest':p.pin((D/'PUBLIC_PAYLOAD_MANIFEST.json').read_bytes()),'public_payload':p.pin(payload.read_bytes()),
 'all_public_members_readback_exact':True,'independent_adversary':p.pin((D/'protocol_adversary_20261006/REVIEW.json').read_bytes()),
 'normal_and_optimized_actual_custody':custody['journal'],'closing_read_only_main_context':git_records,
 'preparation_percent':100,'new_central_proof_search_turns':0,'native_execution_count':0,'service_calls':0,'Git_mutations':0,
 'primary_checkout_edited':False,'future_native_source_family_not_authored_or_executed':True,
 'no_actual_DOI_or_Sheet_row_selected':True,'overall_publication_native_goal_complete':False}
write('SEAL_RECEIPT.json',receipt)
print(json.dumps({'preparation_percent':100,'public_file_count':len(files),'public_payload':receipt['public_payload'],
 'manifest':receipt['manifest'],'native_execution_count':0,'service_calls':0}))
