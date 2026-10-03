#!/usr/bin/env python3
"""Own actual inspection launch followed by self-only source closure."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def dump(value):return (json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
here=Path(__file__).absolute().parent
manifest=here/'PREPARATION_MANIFEST.json'
assert not manifest.exists()
source=here/'inspect_closure_inputs.py'
body=source.read_bytes();operator=Path(__file__).read_bytes()
capture=here/'CLOSURE_INPUT_INSPECTION_ACTUAL_CAPTURE'
capture.mkdir(exist_ok=False)
(capture/'PRELAUNCH_SOURCE.py').write_bytes(body)
(capture/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
argv=['/usr/bin/python3','-B',str(source)]
record={'schema':'PR44_OWN_PREPARATION_ACTUAL_CAPTURE_v1','operator_pid':os.getpid(),
        'argv':argv,'cwd':str(here),'started_utc':stamp(),'source_sha256':digest(body),'operator_sha256':digest(operator),
        'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False,'production_executed':False}
with (capture/'stdout.bin').open('xb') as out,(capture/'stderr.bin').open('xb') as err:
    child=subprocess.Popen(argv,cwd=here,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
    record.update(actual_execution=True,pid=child.pid)
    try:
        record['exit_code']=child.wait(timeout=60);record['completed']=True
    except BaseException:
        child.kill();record['exit_code']=child.wait();raise
record['finished_utc']=stamp()
for channel in ['stdout','stderr']:
    content=(capture/(channel+'.bin')).read_bytes()
    record[channel]={'path':channel+'.bin','bytes':len(content),'sha256':digest(content)}
record['source_unchanged']=source.read_bytes()==body
record['operator_unchanged']=Path(__file__).read_bytes()==operator
record['status']='PASS_OWN_SOURCE_PREPARATION' if record['exit_code']==0 and record['source_unchanged'] and record['operator_unchanged'] else 'FAILED_OWN_SOURCE_PREPARATION_PRESERVED'
(capture/'CAPTURE.json').write_bytes(dump(record))
assert record['status']=='PASS_OWN_SOURCE_PREPARATION'
log=here/'SOURCE_PREPARATION_RESEARCH_LOG.md'
with log.open('a') as handle:
    handle.write(stamp()+' — self-only source closure; source preparation100%, full discovery0%. Independent own controls5208/17mutants,294fullinputs; source-only production still unexecuted. ROOT genuine prerequisites, new source adversary and new whole-current review pending. Original2/5,new0,audit0.\n')
files=[];dirs=[]
for path in sorted(here.rglob('*')):
    assert not path.is_symlink() and all(not parent.is_symlink() for parent in path.parents)
    name=path.relative_to(here).as_posix()
    if path.is_file():
        assert stat.S_ISREG(path.stat().st_mode)
        path.chmod(0o444)
        assert stat.S_IMODE(path.stat().st_mode)==0o444
        raw=path.read_bytes()
        files.append({'path':name,'bytes':len(raw),'sha256':digest(raw)})
    else:
        assert path.is_dir();dirs.append(name)
needed={parent.as_posix() for row in files for parent in PurePosixPath(row['path']).parents if parent.as_posix()!='.'}
assert set(dirs)==needed
value={'schema':'PR44_CURRENT_SOURCE_ONLY_CLOSURE_v1','utc':stamp(),
       'status':'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','files_count':len(files),'files':files,
       'self_excluded':['PREPARATION_MANIFEST.json'],'directories':dirs,'full_permission_mode':'0444',
       'production_builder_executed':False,'production_operator_executed':False,
       'ROOT_reading_or_future_approval_claimed':False,'new_source_adversary_passed':False,
       'whole_current_review_completed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,
       'audit_turns':0,'source_preparation_completion_percent':100,'full_discovery_completion_percent':0,
       'foreign_primary_bodies_copied_into_family':False}
manifest.write_bytes(dump(value));manifest.chmod(0o444)
assert stat.S_IMODE(manifest.stat().st_mode)==0o444
for row in files:
    raw=(here/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and digest(raw)==row['sha256'] and stat.S_IMODE((here/row['path']).stat().st_mode)==0o444
print(json.dumps({'status':value['status'],'files_count':len(files),'self_excluded':value['self_excluded'],
                  'manifest_sha256':digest(manifest.read_bytes()),'actual_inspector_pid':child.pid,
                  'production_executed':False},indent=2))
