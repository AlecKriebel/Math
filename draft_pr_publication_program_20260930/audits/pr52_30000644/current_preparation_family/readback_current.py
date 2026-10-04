#!/usr/bin/env python3
"""Actual private readback with complete source/operator/stream data in one JSON.

The compact representation avoids another copied administrative directory.
Neither branch imports or executes mathematical or production helpers.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
def utc():return datetime.now(timezone.utc).isoformat()
def digest(body):return {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
def child():
    from closure_common import external,science,builder_capture,require,COUNTER
    ext=external();sci=science();cap=builder_capture()
    source=(HERE/'build_current.py').read_bytes()
    operator=(HERE/'capture_builder.py').read_bytes()
    require(cap['source']==digest(source),'complete original builder source binding')
    require(cap['operator']==digest(operator),'complete original builder operator binding')
    require(cap['ROOT_or_production_execution'] is False,'private text builder only')
    value={'schema':'pr52-current-private-readback-result/v1','status':'PASS_CURRENT_SCIENCE_AND_INPUTS',
           'utc':utc(),'actual_pid':os.getpid(),'integrity_checks':COUNTER[0],
           'science_files':sci,'external_full_body_rows':ext,
           'completed_builder_child_pid':cap['child_pid'],
           'new_math_checker_execution':False,'new_mathematical_verdict':False,
           'ROOT_native_Git_remote_publication_authority':False,
           'scope':'Whole 39 science bodies, original Git blobs, unchanged mathematical sections, all 273 fixed predecessor/CAP4 bodies/full modes and completed private builder. Later final metadata is not called already written.'}
    print(json.dumps(value,indent=2,sort_keys=True))
def parent():
    destination=HERE/'READBACK_CAPTURE.json'
    if destination.exists():raise AssertionError('readback capture initially absent')
    sources=[]
    for name in ('readback_current.py','closure_common.py'):
        p=HERE/name;b=p.read_bytes()
        sources.append({'path':str(p),**digest(b),'mode':format(p.stat().st_mode&0o7777,'04o'),
                        'full_prelaunch_utf8':b.decode('utf-8')})
    argv=['/usr/bin/python3','-B',str(Path(__file__).resolve()),'--child']
    start=utc()
    p=subprocess.Popen(argv,cwd=str(HERE),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    pid=p.pid;out,err=p.communicate();end=utc()
    value={'schema':'pr52-current-private-compact-readback-capture/v1',
           'argv':argv,'cwd':str(HERE),'child_pid':pid,'operator_pid':os.getpid(),
           'utc_start':start,'utc_end':end,'exit_code':p.returncode,
           'sources_and_operator_prelaunch':sources,
           'sources_unchanged_after':all(Path(r['path']).read_bytes()==r['full_prelaunch_utf8'].encode() for r in sources),
           'stdout':{**digest(out),'full_utf8':out.decode('utf-8')},
           'stderr':{**digest(err),'full_utf8':err.decode('utf-8')},
           'ROOT_or_production_execution':False,
           'earlier_builder_import_snapshot_qualification':'Earlier builder capture pins its main source/operator. This later readback additionally pins the full private closure_common input before execution; no earlier import snapshot is fabricated.'}
    if p.returncode==0:value['stdout_typed']=json.loads(out)
    destination.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in value.items() if k not in ('sources_and_operator_prelaunch','stdout','stderr','stdout_typed')},indent=2,sort_keys=True))
    if p.returncode==0:print(out.decode('utf-8'),end='')
    sys.exit(p.returncode)
if __name__=='__main__':
    if sys.argv[1:]==['--child']:child()
    elif not sys.argv[1:]:parent()
    else:raise SystemExit('unexpected arguments')
