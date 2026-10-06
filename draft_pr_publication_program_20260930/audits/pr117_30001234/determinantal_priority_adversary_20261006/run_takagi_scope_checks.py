from pathlib import Path
import datetime,hashlib,json,os,subprocess
ROOT=Path(__file__).resolve().parent
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
ENV={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
receipt={'actual_pid':os.getpid(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':[]};answers=[]
for optimized in [False,True]:
    for false in [False,True]:
        label='takagi_'+('optimized' if optimized else 'normal')+('_false_control' if false else '')
        cmd=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(ROOT/'takagi_scope_checks.py')]+(['--false-control'] if false else [])
        p=subprocess.Popen(cmd,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=ROOT)
        a,b=p.communicate();(ROOT/(label+'.stdout.txt')).write_bytes(a);(ROOT/(label+'.stderr.txt')).write_bytes(b)
        receipt['runs'].append({'label':label,'actual_pid':p.pid,'argv':cmd,'exit_code':p.returncode,'stdout_bytes':len(a),'stderr_bytes':len(b),'stdout_sha256':hashlib.sha256(a).hexdigest(),'stderr_sha256':hashlib.sha256(b).hexdigest()})
        (ROOT/'TAKAGI_SCOPE_PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        if false:
            if p.returncode==0 or b'deliberate false source-bridge guard' not in b:raise ValueError('False control failed')
        else:
            if p.returncode!=0 or b:raise ValueError('Scope check failed')
            answers.append(json.loads(a))
if answers[0]!=answers[1]:raise ValueError('Normal and optimized results differ')
receipt.update(result='PASS',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(ROOT/'TAKAGI_SCOPE_PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
(ROOT/'TAKAGI_SCOPE_CHECK_RESULT.json').write_text(json.dumps(answers[0],indent=2)+'\n')
print(json.dumps({'result':'PASS','actual_pid':os.getpid(),'runs':4,'exception_checks_per_positive_run':answers[0]['explicit_exception_checks']}))
