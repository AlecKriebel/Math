"""Capture own authoring and private controls; never run proposed production or closure."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys
H = Path(__file__).resolve().parent
ALLOWED = {'author_sources_v2.py', 'bind_closed_adverse.py', 'independent_controls_v2.py', 'repair_sources_v2.py', 'prepare_closure_source_v2.py'}
def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p, b):
    with p.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
def enc(o): return (json.dumps(o, sort_keys=True, indent=2) + '\n').encode()
def main():
    parser = argparse.ArgumentParser(); parser.add_argument('capture'); parser.add_argument('script'); args = parser.parse_args()
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'): raise ValueError('Optimization prohibited')
    if args.script not in ALLOWED or not args.capture or '/' in args.capture or args.capture in {'.', '..'}: raise ValueError('Own allowlisted authoring/control source only')
    script = H / args.script; source = script.read_bytes(); operator = Path(__file__).read_bytes(); output = H / args.capture; output.mkdir()
    pre = {'schema':'pr46-source-v2-operation-prelaunch/v1', 'operator_pid':os.getpid(), 'script':str(script), 'source_sha256':sha(source), 'operator_sha256':sha(operator), 'cwd':str(H), 'created_utc':now(), 'argv':[sys.executable, '-B', str(script)], 'stdin_supplied':False}
    put(output/'PRELAUNCH_SOURCE.py', source); put(output/'PRELAUNCH_OPERATOR.py', operator); put(output/'PRELAUNCH.json', enc(pre))
    start = now(); child = subprocess.Popen(pre['argv'], cwd=H, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE); out, err = child.communicate(); end = now()
    record = {'schema':'pr46-source-v2-operation-actual-capture/v1', 'prelaunch':pre, 'operator_pid':os.getpid(), 'pid':child.pid, 'actual_execution':True, 'completed':True, 'exit_code':child.returncode, 'started_utc':start, 'finished_utc':end, 'source_unchanged':script.read_bytes()==source, 'operator_unchanged':Path(__file__).read_bytes()==operator}
    for channel, body in [('stdout',out), ('stderr',err)]:
        put(output/(channel+'.bin'), body); record[channel] = {'path':channel+'.bin','bytes':len(body),'sha256':sha(body)}
    record['status'] = 'PASS' if child.returncode == 0 and record['source_unchanged'] and record['operator_unchanged'] else 'FAIL'; put(output/'CAPTURE.json', enc(record))
    print(json.dumps({'capture':args.capture,'operator_pid':os.getpid(),'child_pid':child.pid,'status':record['status'],'exit_code':child.returncode,'stdout':out.decode(errors='replace'),'stderr':err.decode(errors='replace')}, sort_keys=True))
    return 0 if record['status']=='PASS' else 1
if __name__=='__main__': sys.exit(main())
