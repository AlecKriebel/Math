#!/usr/bin/env python3
"""Final metadata freeze only; ROOT closer/reader stay unexecuted SOURCE."""
from datetime import datetime,timezone
from pathlib import Path
import json,os,stat,hashlib
from closure_common import HERE,SELF,bind,load,require,external,science,builder_capture,inspect,sha
def utc():return datetime.now(timezone.utc).isoformat()
def put(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
for name in (SELF,'INDEX.json','READY.json','VERDICT.json'):
    require(not (HERE/name).exists(),'final metadata initially absent '+name)
cap=load(HERE/'READBACK_CAPTURE.json')
require(cap['exit_code']==0 and cap['sources_unchanged_after'] is True,'completed private science readback')
require(cap['child_pid']==13627 and cap['operator_pid']==13626,'real completed readback PIDs')
for row in cap['sources_and_operator_prelaunch']:
    body=row['full_prelaunch_utf8'].encode()
    require(len(body)==row['bytes'] and sha(body)==row['sha256'],'whole readback prelaunch input')
    require(Path(row['path']).read_bytes()==body,'readback sources remain unchanged')
for name in ('stdout','stderr'):
    body=cap[name]['full_utf8'].encode()
    require(len(body)==cap[name]['bytes'] and sha(body)==cap[name]['sha256'],'whole completed readback stream')
require(cap['stderr']['full_utf8']=='','complete empty stderr')
require(json.loads(cap['stdout']['full_utf8'])==cap['stdout_typed'],'whole typed readback stdout')
require(cap['stdout_typed']['integrity_checks']==1564,'actual private readback count')
ext=external();sci=science();builder=builder_capture()
require(builder['child_pid']==10798 and ext==273 and sci==39,'actual completed input preparation')
index=load(HERE/'SCIENCE_INDEX.json')
index['storage_mode_fields_are_dated_builder_epoch_facts']=True
index['actual_final_full_modes_are_bound_by']='INDEX.json and later actual ROOT SELF_MANIFEST.json; construction-mode 0644 fields are historical.'
put('SCIENCE_INDEX.json',index)
put('VERDICT.json',{'schema':'pr52-current-lean-source-disposition/v1','utc':utc(),
 'disposition':'READY_CURRENT_SOURCE_ONLY','problem_id':30000644,
 'original_head':'d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a',
 'recommended_status':'already_solved','new_independent_mathematical_verdict':False,
 'reused_preparer':'divergence_shear_adversary_family','new_discovery':False,
 'new_substantive_search_attempts':0,'original_substantive_search_attempts':0,
 'original_substantive_attempt_limit':5,'original_known_theorem_validation_activities':1,
 'original_separate_response_count_supplied':False,'science_files':39,
 'original_literal_files':19,'operative_files':20,'external_rows':273,
 'actual_private_builder_child':10798,'actual_private_readback_child':13627,
 'preparation_integrity_counts':[1927,1564],'current_math_assertion_count':0,
 'full_JPAA_article_read':False,'human_peer_review':False,'formal_proof_certificate':False,
 'ROOT_approval':False,'native_acceptance':False,'Git_or_remote_authority':False,
 'current_ROOT_closure_performed':False,'new_paper':False,'new_DOI':False,'tracker_authority':False,
 'report':bind(HERE/'REPORT.md',True,'0444')})
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+utc()+' — 100% current SOURCE preparation estimate. Real private builder10798 and separate readback13627 completed with1927/1564 integrity checks and complete captured streams. '
            'Their completed captures were checked after exit; final metadata is prepared now. '
            '39 science bodies and273 fixed in-place input rows remain intact. Final full file modes0444/directory modes0555 will be verified before successful stdout. '
            'No new math independence, ROOT closure, native/Git/remote change, paper, DOI or human contact.\n')
files=[p for p in sorted(HERE.rglob('*')) if p.is_file()]
require(len(files)+2<=60,'requested maximum60 small files')
require(sum(p.stat().st_size for p in files)<1000000,'bounded sub-megabyte packet')
dirs=[HERE]+sorted(p for p in HERE.rglob('*') if p.is_dir())
put('INDEX.json',{'schema':'pr52-current-lean-index/v1','utc':utc(),'family':str(HERE),
 'files':[bind(p,True,'0444') for p in files],
 'directories':[{'path':'.' if p==HERE else p.relative_to(HERE).as_posix(),'mode':'0555'} for p in dirs],
 'future_authority':False,'excludes_only':['INDEX.json','READY.json','SELF_MANIFEST.json']})
put('READY.json',{'schema':'pr52-current-lean-ready/v1','utc':utc(),
 'status':'SOURCE_READY_AFTER_PRIVATE_READBACK','family':str(HERE),
 'index':bind(HERE/'INDEX.json',True,'0444'),'final_payload_files_without_self':len(files)+2,
 'science_files':39,'fixed_external_rows':273,
 'ROOT_closure_performed':False,'SELF_manifest_absent_when_prepared':True,
 'new_independent_math_verdict':False,'native_acceptance':False,'new_paper':False,'new_DOI':False,
 'root_required_steps':['Read whole packet/exact science diffs and SOURCE.',
 'After preparer exit capture close_family.py --expected-index-sha256 PIN --expected-ready-sha256 PIN --after-preparer-exit.',
 'After closer exit capture read_closed_family.py with those pins and actual manifest pin.'],
 'no_future_manifest_hash_or_PID_invented':True})
for p in HERE.rglob('*'):
    if p.is_file():os.chmod(p,0o444)
for p in sorted(dirs,key=lambda p:len(p.parts),reverse=True):os.chmod(p,0o555)
result=inspect(False)
require(not (HERE/SELF).exists(),'actual ROOT self manifest remains absent')
print(json.dumps({'status':'SOURCE_READY_CURRENT_PR52','inspection':result,
 'ready':bind(HERE/'READY.json',True),'index':bind(HERE/'INDEX.json',True),
 'ROOT_closer_and_reader_executed':False,
 'total_bytes':sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file())},indent=2,sort_keys=True))
