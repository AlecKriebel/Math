"""Execute the independent controls and retain complete small process outputs."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent
PYTHON = Path('/opt/homebrew/bin/python3').resolve()


def sha(body):
    return hashlib.sha256(body).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    rows = []
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        argv = [str(PYTHON),'-E','-S','-B']+flags+[str(HERE/'independent_exact_controls.py')]
        env = {'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}
        start = now()
        proc = subprocess.Popen(argv,cwd=HERE,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = proc.communicate(timeout=30)
        end = now()
        (HERE/(mode+'.stdout.json')).write_bytes(out)
        (HERE/(mode+'.stderr.txt')).write_bytes(err)
        row = {'mode':mode,'argv':argv,'cwd':str(HERE),'environment':env,
               'PID':proc.pid,'start_UTC':start,'end_UTC':end,'exit_code':proc.returncode,
               'stdout_bytes':len(out),'stdout_sha256':sha(out),
               'stderr_bytes':len(err),'stderr_sha256':sha(err),
               'full_stdout_and_stderr_retained':True,'timed_out':False,'reaped':True}
        rows.append(row)
        (HERE/'EXACT_CONTROL_PROCESS_RECEIPTS.json').write_text(json.dumps(
            {'operator_PID':os.getpid(),'operator_UTC':now(),'python_binary':
             {'path':str(PYTHON),'bytes':PYTHON.stat().st_size,'sha256':sha(PYTHON.read_bytes())},
             'processes':rows},indent=2)+'\n')
        if proc.returncode:
            raise RuntimeError(mode+' controls exited '+str(proc.returncode))
        result=json.loads(out)
        if not result['all_passed'] or result['checks'] <= 0:
            raise RuntimeError('Missing substantive actual controls')
        print(mode+': '+str(result['checks'])+' checks; '+
              str(result['purposeful_admissible_cases'])+' curated admissible cases; '+
              str(result['negative_controls_detected'])+' negative controls detected; PID '+str(proc.pid))


if __name__ == '__main__':
    main()
