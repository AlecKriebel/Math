"""Private source-only evidence recheck. Outer operator closes after actual child exits."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat
H=Path(__file__).resolve().parent;R=H.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def verify(base,z):
    p=base/z['path']
    if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(base.resolve()):raise ValueError('Unsafe individual closure input')
    for q in p.parents:
        if q==base:break
        if q.is_symlink():raise ValueError('Symlink individual ancestor')
    h=hashlib.sha256();n=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b);n+=len(b)
    if n!=z['bytes'] or h.hexdigest()!=z['sha256']:raise ValueError('Changed individual input')
def main():
    inputs=load(H/'INDIVIDUAL_INPUTS.json');result=load(H/'CONTROL_RESULTS.json');verdict=load(H/'VERDICT.json')
    if inputs['files_count']!=1267 or len(inputs['files'])!=1267 or result['status']!='PASS_HANDWRITTEN_SOURCE_CONTRACT_CONTROLS_ONLY' or verdict['verdict']!='PASS_SOURCE_ONLY_SCOPED' or verdict['mandatory_corrections']!=[] or verdict['production_imported_compiled_executed'] is not False or verdict['future_acceptance_approved'] is not False:raise ValueError('Complete source-only disposition required')
    for z in inputs['files']:verify(R,z)
    captures=[]
    for n,expected in [('REVIEW_ACTUAL_CAPTURE','FAIL'),('REVIEW_ACTUAL_CAPTURE_V2','PASS')]:
        d=H/n;c=load(d/'CAPTURE.json');p=load(d/'PRELAUNCH.json')
        if c['prelaunch']!=p or c['status']!=expected or c['actual_execution'] is not True or c['completed'] is not True or type(c['pid']) is not int or c['pid']<=0 or c['source_unchanged'] is not True or c['operator_unchanged'] is not True:raise ValueError('Genuine retained complete capture')
        if sha((d/'PRELAUNCH_SOURCE.py').read_bytes())!=p['source_sha256'] or sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())!=p['operator_sha256']:raise ValueError('Exact complete prelaunch sources')
        for k in ['stdout','stderr']:verify(d,c[k])
        if dt.datetime.fromisoformat(c['started_utc'])>dt.datetime.fromisoformat(c['finished_utc']):raise ValueError('Actual capture clocks')
        captures.append({'path':n+'/CAPTURE.json','pid':c['pid'],'status':c['status'],'sha256':sha((d/'CAPTURE.json').read_bytes())})
    git_count=0
    for p in sorted((H/'ACTUAL_GIT').rglob('CAPTURE.json')):
        c=load(p);pre=load(p.parent/'PRELAUNCH.json')
        if c['argv']!=pre['argv'] or c['cwd']!=pre['cwd'] or c['actual_execution'] is not True or c['completed'] is not True or c['exit_code']!=0 or type(c['pid']) is not int or c['pid']<=0:raise ValueError('Complete actual read-only Git')
        for k in ['stdout','stderr']:verify(H,c[k])
        git_count+=1
    if git_count!=21:raise ValueError('Expected all21 actual read-only queries including failed run')
    o={'schema':'pr44-source-adversary-final-inspection/v1','utc':utc(),'actual_closure_child_pid':os.getpid(),'status':'PASS_SOURCE_ONLY_CLOSURE_INSPECTION','individual_inputs_rechecked':1267,'genuine_own_review_captures':captures,'all_actual_readonly_Git_queries':21,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'source_review_completion_percent':100,'acceptance_completion_percent':0,'discovery_completion_percent':0}
    with (H/'FINAL_INSPECTION.json').open('x') as f:json.dump(o,f,sort_keys=True,indent=2);f.write('\n')
    with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — Final scoped source checkpoint. Completion100% source review/0% acceptance/0% discovery. All1,267 individual inputs and both genuine own review captures rechecked, including failed22511 and operative23325. All21 actual read-only Git queries preserved. No mandatory source defect; all future ROOT/acceptance gates unperformed. Outer capture will add only genuine completed closure evidence, freeze full0444, and exclude only SELF_MANIFEST.json.\n')
    print(json.dumps(o,sort_keys=True))
if __name__=='__main__':main()
