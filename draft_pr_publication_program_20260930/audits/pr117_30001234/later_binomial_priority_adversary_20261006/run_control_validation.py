#!/usr/bin/env python3
import datetime,hashlib,json,os,pathlib,subprocess
D=pathlib.Path(__file__).resolve().parent
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'runs':[],'status':'RUNNING'}
for name,optimized,false in [('normal',False,False),('optimized',True,False),('normal_false',False,True),('optimized_false',True,True)]:
    argv=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(D/'priority_implication_controls.py')]+(['--false-control'] if false else [])
    p=subprocess.Popen(argv,cwd=D,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate(timeout=30)
    (D/(name+'.stdout.txt')).write_bytes(out);(D/(name+'.stderr.txt')).write_bytes(err)
    r={'name':name,'actual_PID':p.pid,'argv':argv,'actual_returncode':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()}
    if false:
        if p.returncode==0 or b'ValueError: deliberately false assertion' not in err:raise ValueError('False control accepted')
        r['deliberate_false_control_rejected']=True
    else:
        if p.returncode or err:raise ValueError('Positive control failed')
        v=json.loads(out)
        if v['status']!='PASS' or v['actual_PID']!=p.pid:raise ValueError('Control output authentication failed')
        if v['code_sha256']!=hashlib.sha256((D/'priority_implication_controls.py').read_bytes()).hexdigest():raise ValueError('Code hash mismatch')
        r['summary']=v
    receipt['runs'].append(r)
    (D/'CONTROL_PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
if receipt['runs'][0]['summary']['guard_count']!=receipt['runs'][1]['summary']['guard_count']:raise ValueError('Normal/optimized guards differ')
receipt['status']='PASS';receipt['completed_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(D/'CONTROL_PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':receipt['status'],'actual_operator_PID':os.getpid(),'normal_guard_count':receipt['runs'][0]['summary']['guard_count'],'optimized_guard_count':receipt['runs'][1]['summary']['guard_count'],'false_controls_rejected':2},indent=2,sort_keys=True))
