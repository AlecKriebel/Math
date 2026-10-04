"""Private exact replay of the two unchanged PR50 helpers; finite diagnostics only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,stat
from capture_readonly import capture
H=Path(__file__).resolve().parent;O=H/'original'
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(items):
        o={}
        for k,v in items:assert k not in o;o[k]=v
        return o
    def finite(x):
        v=float(x);assert math.isfinite(v);return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def typed(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def main():
    assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
    manifest=parse((H/'ORIGINAL_MANIFEST.json').read_bytes());whole=[]
    for row in manifest['files']:
        p=O/row['path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
        if p.suffix=='.json':parse(b)
        if p.suffix=='.jsonl':
            for line in b.splitlines():parse(line)
        whole.append({'path':row['path'],'bytes':len(b),'sha256':sha(b)})
    w=H/'private_reproduction';w.mkdir();runs=[]
    for name,script,receipt in [('author_replay','verify_even_moves.py','even_move_verification.json'),('prior_independent_replay','review/independent_checks.py','review/independent_results.json')]:
        c,out,err=capture(name,['/usr/bin/python3','-B',str(O/script)],cwd=w,source=O/script)
        assert c['exit_code']==0 and not err and c['source_unchanged'] is True
        actual=parse(out);old=(O/receipt).read_bytes();assert typed(actual,parse(old)) and out==old
        assert actual['status']=='PASS' and type(actual['exact_assertions']) is int
        runs.append({'capture':name,'child_pid':c['child_pid'],'actual_output_byte_identical':True,'exact_assertions':actual['exact_assertions'],'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':0,'literal_script_sha256':c['child_source']['sha256'],'result':actual})
    assert runs[0]['exact_assertions']==3219 and runs[1]['exact_assertions']==6641
    assert len(list(w.iterdir()))==0;w.rmdir()
    for row in whole:assert sha((O/row['path']).read_bytes())==row['sha256']
    result={'schema':'pr50-original-private-reproduction/v1','utc':datetime.now(timezone.utc).isoformat(),'actual_pid':os.getpid(),'status':'PASS_LITERAL_ORIGINAL_HELPERS_AND_RECEIPTS','complete_original_files_read':whole,'runs':runs,'finite_diagnostics_prove_target':False,'fundamental_Markov_theorems_proved_here':False,'snapshot_unchanged':True,'live_native_index_ref_or_remote_mutated':False,'acceptance_approved':False}
    with (H/'ORIGINAL_REPRODUCTION.json').open('x') as f:f.write(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'actual_pid':os.getpid(),'author_assertions':3219,'independent_assertions':6641,'original_files':len(whole),'literal_receipts_byte_identical':True},sort_keys=True))
if __name__=='__main__':main()
