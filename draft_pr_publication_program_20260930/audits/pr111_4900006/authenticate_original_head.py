#!/usr/bin/env python3
"""Acquire exact immutable submitted PR111 originals without checkout/index changes."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys
A=Path(__file__).resolve().parent;P=A.parents[1];C=P.parent;D=A/'original_head_authentication_20261006';previous=P/'audits/pr110_5100032'
f=previous/'native_post_assess_carryforward_v3_20261006/native_acceptance_actions_v4.py'
s=importlib.util.spec_from_file_location('bounded_source_reader',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
need=m.need
need(dict(os.environ)==m.START_ENV and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path,'Exact clean physical startup')
packet=m.loads(m.read(previous/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json',512*1024));rt=packet['runtime'];m.validate_runtime(rt)
capture=m.Capture(A/'actual_original_head_authentication_20261006')
head='8a7270989d7064a4b97badecaa4b311db5e6d49f';prefix='unsolved_math_prioritization/attempts/4900006/'
before=m.git(capture,rt,'rev-parse','HEAD');index=m.git(capture,rt,'write-tree');changes=m.git(capture,rt,'diff','--name-only','--diff-filter=ACMRTUXB','-z')
need(m.git(capture,rt,'symbolic-ref','--short','HEAD').strip()==b'main' and not m.git(capture,rt,'diff','--cached','--name-only','-z'),'main only, empty index')
m.git(capture,rt,'fetch','--no-tags','--no-write-fetch-head',m.URL,'refs/pull/111/head',authenticated=True,deadline=60)
need(m.git(capture,rt,'cat-file','-t',head).strip()==b'commit','Original immutable commit object')
raw=m.git(capture,rt,'ls-tree','-r','-z',head,'--',prefix);entries=[]
for line in raw.split(b'\0'):
    if not line:continue
    metadata,path=line.split(b'\t',1);mode,kind,sha=metadata.split();name=path.decode();need(mode==b'100644' and kind==b'blob' and name.startswith(prefix),'Regular original attempt Git blob')
    body=m.git(capture,rt,'show',head+':'+name)
    need(hashlib.sha1(('blob '+str(len(body))+'\0').encode()+body).hexdigest()==sha.decode(),'Complete original Git blob authenticated')
    rel=name[len(prefix):];m.relpath(rel);destination=D/'original_attempt'/rel;m.atomic(destination,body)
    entries.append({'path':rel,'Git_blob':sha.decode(),**m.pin(body)})
need(len(entries)>0,'Nonempty complete original attempt')
queue=m.git(capture,rt,'show',head+':unsolved_math_prioritization/QUEUE.md');intake=P/'ordered_intake_20261006/after_PR110/PR111_AUTHENTICATED_HEAD_QUEUE.md';need(queue==intake.read_bytes(),'Exact API/Git head QUEUE agreement')
m.atomic(D/'ORIGINAL_HEAD_QUEUE.md',queue)
for name in ('manifest.json','review_v2/related_target_groups.json'):
    body=m.git(capture,rt,'show',head+':unsolved_math_prioritization/'+name);m.atomic(D/name.replace('/','_'),body)
need(m.git(capture,rt,'rev-parse','HEAD')==before and m.git(capture,rt,'write-tree')==index and m.git(capture,rt,'diff','--name-only','--diff-filter=ACMRTUXB','-z')==changes and not m.git(capture,rt,'diff','--cached','--name-only','-z'),'Fetch left own main/index/materialized tracking unchanged')
result={'schema':'immutable-draft-original-attempt-authentication/v1','UTC':m.now(),'actual_operator_PID':os.getpid(),'PR':111,'problem_id':4900006,'original_head':head,'literal_original_status':'claimed_solved','original_effort':'2/5','all_original_files':entries,'original_file_count':len(entries),'original_queue_pin':m.pin(queue),'local_main_unchanged':before.decode().strip(),'index_unchanged':True,'materialized_tracked_changes_unchanged':True,'source_cache_readonly':True,'new_substantive_proof_turns':0,'remote_ref_or_PR_mutations':0,'GitHub_release_created':False}
m.save(D/'ORIGINAL_AUTHENTICATION.json',result);print(json.dumps({'actual_operator_PID':os.getpid(),'PR':111,'original_head':head,'original_file_count':len(entries),'original_files':[x['path'] for x in entries],'main_index_unchanged':True}))
