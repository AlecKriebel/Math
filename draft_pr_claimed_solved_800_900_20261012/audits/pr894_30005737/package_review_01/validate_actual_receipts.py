#!/usr/bin/env python3
"""Independently validate actual streams/metadata, including nested replay events.
Usage: python -I -S -B validate_actual_receipts.py CANDIDATE REVIEW
Raw streams and local paths never enter the public result.
"""
from pathlib import Path
from datetime import datetime
import hashlib,json,sys
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(ok,why):
    if not ok:raise ValueError(why)
def validate(meta,stdout,stderr):
    check(pin(stdout)==meta['stdout'] and pin(stderr)==meta['stderr'],'actual raw stream pins')
    check(type(meta['pid']) is int and meta['pid']>0 and type(meta['returncode']) is int,'real PID/return code')
    check(datetime.fromisoformat(meta['started_utc'])<=datetime.fromisoformat(meta['launched_utc'])<=datetime.fromisoformat(meta['ended_utc']),'UTC timestamp order')
    check(type(meta['elapsed_monotonic_ns']) is int and meta['elapsed_monotonic_ns']>0 and not meta.get('timeout',False),'monotonic duration/timeout')
def main():
    C=Path(sys.argv[1]);R=Path(sys.argv[2]);P=R/'private_tmp';replays=[];allpids=[]
    wantorder=['positive','positive','semantic_negative','require_false','corrupt','semantic_negative','require_false','corrupt']
    wantmodes=[0,1,0,0,0,1,1,1]
    expected=(C/'verification/source/authored/CHECK_RESULTS.json').read_bytes()
    sourcepins=json.loads((C/'verification/root_evidence/SOURCE_MANIFEST.json').read_bytes())['files']
    for name,mode in [('normal-replay',0),('optimized-replay',1),('hostile-replay',0)]:
        D=P/name;wm=json.loads((D/'root-wrapper.json').read_bytes());wb=(D/'root-wrapper.stdout.bin').read_bytes();we=(D/'root-wrapper.stderr.bin').read_bytes();validate(wm,wb,we)
        check(wm['returncode']==0 and not we,'wrapper success');w=json.loads(wb)
        check(w['root_compile_optimize']==mode and w['root_flags']=={'optimize':mode,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True},'actual wrapper flags')
        rootexec=json.loads((D/'processes/original-root.execution.json').read_bytes());rootout=(D/'processes/original-root.stdout.bin').read_bytes();rooterr=(D/'processes/original-root.stderr.bin').read_bytes()
        check(pin(rootout)==rootexec['stdout']==w['root_stdout'] and pin(rooterr)==rootexec['stderr'] and not rooterr and rootexec['exception_type'] is None,'actual unchanged root output')
        check(json.loads(rootout)==w['root_output'] and w['root_output']['packet_files']==18 and w['root_output']['finite_diagnostic_conditions_per_run']==2896,'root semantic output')
        check(w['root_sha256']==pin((C/'verification/source/verify_publication.py').read_bytes())['sha256'],'original root code pin')
        check([e['kind'] for e in w['events']]==wantorder,'actual event order')
        entries=[]
        for i,(e,m) in enumerate(zip(w['events'],wantmodes)):
            stem=D/'processes'/('child-%02d'%i);actual=json.loads(Path(str(stem)+'.json').read_bytes());out=Path(str(stem)+'.stdout.bin').read_bytes();err=Path(str(stem)+'.stderr.bin').read_bytes();validate(actual,out,err)
            flags=json.loads(Path(str(stem)+'.flags.json').read_bytes());event=json.loads(Path(str(stem)+'.event.json').read_bytes());check(e==event and e['process']==actual,'event/process binding')
            check(flags==e['measured_flags']=={'optimize':m,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True},'genuine child flags')
            check(e['compile_optimize']==m and e['original_execution_began']==Path(str(stem)+'.began').exists(),'execution marker binding')
            if e['kind']=='positive':check(actual['returncode']==0 and not err and out==expected and e['original_execution_began'],'positive byte exact output')
            elif e['kind']=='semantic_negative':check(actual['returncode']!=0 and e['original_execution_began'] and b'RuntimeError: semantic_negative: PA2' in err,'real PA2 rejection')
            elif e['kind']=='require_false':check(actual['returncode']!=0 and e['original_execution_began'] and b'RuntimeError: explicit_false_control' in err,'real original require rejection')
            else:check(actual['returncode']!=0 and not e['original_execution_began'] and b'CORRUPT_REJECTED_BEFORE_EXECUTION' in err,'preexecution corrupt rejection')
            allpids.append(actual['pid']);entries.append({'kind':e['kind'],'flags':flags,'compile_optimize':m,'original_execution_began':e['original_execution_began'],**actual})
        allpids.append(wm['pid'])
        for row in sourcepins:check(pin((D/'frozen'/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']},'unchanged original replay copy')
        replays.append({'label':name,'genuine_OS_processes':9,'root_executes_inside_wrapper':True,'wrapper':wm,'root_execution_stdout':pin(rootout),'root_execution_stderr':pin(rooterr),'root_flags':w['root_flags'],'events':entries,'all_18_frozen_inputs_unchanged':True})
    check(len(allpids)==len(set(allpids))==27,'27 distinct genuine replay PIDs')
    processes=[]
    for p in sorted(P.rglob('*.json')):
        try:meta=json.loads(p.read_bytes())
        except (ValueError,UnicodeError):continue
        if not isinstance(meta,dict) or not {'started_utc','launched_utc','ended_utc','pid','returncode','elapsed_monotonic_ns','stdout','stderr'}<=set(meta):continue
        stem=p.with_suffix('');outpath=Path(str(stem)+'.stdout.bin');errpath=Path(str(stem)+'.stderr.bin')
        if not outpath.is_file() or not errpath.is_file():continue
        validate(meta,outpath.read_bytes(),errpath.read_bytes())
        processes.append({'label':p.relative_to(P).as_posix(),**{k:meta[k] for k in ['started_utc','launched_utc','ended_utc','elapsed_monotonic_ns','pid','returncode','stdout','stderr']}})
    result={'status':'PASS','raw_process_receipts_validated':len(processes),'all_actual_stream_pins_and_timestamp_orders_valid':True,'genuine_nested_replay_processes':27,'replays':replays,'processes':processes,'raw_streams_and_private_paths_excluded':True}
    # Environment policy fields are safe; no argv/cwd/raw tracebacks are copied.
    (R/'ACTUAL_PROCESS_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','raw_process_receipts_validated':len(processes),'genuine_nested_replay_processes':27},sort_keys=True))
if __name__=='__main__':main()
