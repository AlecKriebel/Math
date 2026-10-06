#!/usr/bin/env python3
"""Capture actual offline normal/optimized fixture envelopes, with no live action."""
import datetime, hashlib, json, os, pathlib, subprocess, sys
D=pathlib.Path(__file__).resolve().parent
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
dest=D/('fixture_runs_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
dest.mkdir()
environment={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}
if sys.platform=='darwin':environment['__CF_USER_TEXT_ENCODING']='0x'+format(os.getuid(),'X')+':0x0:0x0'
programs={n:pin((D/n).read_bytes()) for n in ['protocol.py','test_protocol.py','capture_fixture_runs.py']}
records=[]
for role,flags in [('normal',[]),('optimized',['-O'])]:
    argv=[sys.executable,'-E','-S','-B',*flags,str(D/'test_protocol.py')]
    start=utc();proc=subprocess.Popen(argv,cwd=D,env=environment,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=proc.communicate(timeout=30)
    (dest/(role+'.stdout')).write_bytes(out);(dest/(role+'.stderr')).write_bytes(err)
    result=json.loads(out.decode().splitlines()[-1])
    record={'role':role,'argv':argv,'cwd':str(D),'environment':environment,'PID':proc.pid,'UTC_start':start,'UTC_end':utc(),
      'exit_code':proc.returncode,'reaped':True,'stdout':pin(out),'stderr':pin(err),'termination_reason':None,
      'program_sources':programs,'result':result,'synthetic_fixture_only':True}
    records.append(record)
    if proc.returncode!=0 or result['failures'] or result['errors']:raise ValueError('Offline fixtures failed; actual streams retained')
if programs!={n:pin((D/n).read_bytes()) for n in programs}:raise ValueError('Fixture source changed during run')
write(dest/'ACTUAL_PROCESS_JOURNAL.json',{'schema':'pr110-actual-offline-fixture-processes/v1','operator_PID':os.getpid(),
  'UTC':utc(),'processes':records,'actual_service_calls':0,'actual_native_execution_count':0,'Git_mutations':0})
for record in records:write(D/(record['role'].upper()+'_FIXTURE_RESULTS.json'),record['result'])
write(D/'FIXTURE_CUSTODY.json',{'schema':'pr110-offline-fixture-custody/v1','actual_process_journal':str(dest/'ACTUAL_PROCESS_JOURNAL.json'),
  'journal':pin((dest/'ACTUAL_PROCESS_JOURNAL.json').read_bytes()),'program_sources':programs,'UTC':utc(),'operator_PID':os.getpid(),
  'normal_and_optimized_pass':True,'synthetic_fixture_only':True,'native_execution_count':0,'service_calls':0})
print(json.dumps({'fixture_directory':str(dest),'tests_per_mode':records[0]['result']['tests_run'],'normal_and_optimized_pass':True}))
