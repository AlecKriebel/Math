"""Full isolated normal and optimized replays; expected JSON checked without asserts."""
import json, math, os, pathlib, shutil, subprocess, sys, tempfile, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
def require(ok, why):
    if not ok: raise RuntimeError(why)
TIMED_CASES=frozenset(('exact_n5.json','exact_n7.json','exact_n8.json'))
def comparable(value, result):
    require(isinstance(value,dict), 'Result must be a JSON object')
    if result not in TIMED_CASES: return value
    require('seconds' in value, 'Missing top-level runtime')
    runtime=value['seconds']
    require(type(runtime) in (int,float), 'Runtime must be numeric, not bool')
    require(runtime>=0 and math.isfinite(runtime), 'Runtime must be finite and nonnegative')
    return {k:v for k,v in value.items() if k!='seconds'}
def equivalent(actual, expected, result):
    # Only the documented top-level timing field in exact recurrence outputs is ignored.
    # Nested objects and every field of untimed cases are compared without normalization.
    return json.dumps(comparable(actual,result),sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(comparable(expected,result),sort_keys=True,separators=(',',':'),allow_nan=False)

def main():
    records=[]
    tasks=[('explore.py',['5'],'exact_n5.json'),('explore.py',['7'],'exact_n7.json'),('explore.py',['8'],'exact_n8.json'),('audit_pipe_dreams.py',['5'],'independent_pipe_audit_n5.json'),('audit_pipe_dreams.py',['6'],'independent_pipe_audit_n6.json'),('audit_skew_sums.py',[],'independent_skew_sum_audit.json'),('check_posets.py',[],'poset_n7.json')]
    log=[]
    for mode in ('normal','optimized'):
        with tempfile.TemporaryDirectory(prefix='groth-replay-') as tmp:
            for f in (ROOT/'research').glob('*.py'): shutil.copyfile(f,pathlib.Path(tmp)/f.name)
            for script,args,result in tasks:
                cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+['-B',script]+args
                start=time.monotonic();r=subprocess.run(cmd,cwd=tmp,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
                log.append(f'=== {mode}: {script} {args} ===\n{r.stdout}\n{r.stderr}\nexit={r.returncode}\n')
                require(r.returncode==0,f'{mode} {script} failed: {r.stderr}')
                actual=json.loads((pathlib.Path(tmp)/result).read_text());expected=json.loads((ROOT/'research'/result).read_text())
                require(equivalent(actual,expected,result),f'{mode} {result} semantic mismatch')
                records.append({'mode':mode,'script':script,'args':args,'result':result,'exit_code':r.returncode,'semantic_match':True,'seconds':round(time.monotonic()-start,3)})
                print(mode,script,args,'PASS',flush=True)
    output=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path.cwd()
    output.mkdir(parents=True,exist_ok=True)
    (output/'REPLAY_LOG.txt').write_text('\n'.join(log))
    (output/'REPLAY_RESULTS.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
