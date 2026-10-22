#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';R=A/'repairs/package01'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def check(p,r):
    need(p.is_file() and not p.is_symlink(),str(p)+' absent/nonregular')
    b=p.read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p)+' changed')
def read(p):return json.loads(p.read_text())
def rows(o):
    x=o.get('records',o.get('files'))
    return [{'path':k,**v} for k,v in x.items()] if isinstance(x,dict) else x
counts={}
changes={r['path']:r for r in read(R/'CHANGE_INVENTORY.json')['authorized_existing_changes']}
for filename,root,key in [('OUTPUT_PINS.json',R,'records'),('CURRENT_OUTPUT_PINS.json',P,'records'),('BASELINE_INPUT_PINS.json',A,'records'),('PROTECTED_UNCHANGED.json',A,'unchanged_records'),('PREPARATION_204_INPUT_RECHECK.json',A,'records')]:
    rr=read(R/filename)[key]
    for r in rr:
        p=root/r['path']
        if filename=='BASELINE_INPUT_PINS.json' and r['path'] in changes:p=A/changes[r['path']]['before_bytes_path_relative_to_audit']
        check(p,r)
    counts[filename]=len(rr)
rr=read(R/'PREPARATION_92_PIN_RESOLUTION.json')['records']
for r in rr:check(A/r['before_bytes_path_relative_to_audit'] if r['before_bytes_path_relative_to_audit'] else P/r['path'],r)
counts['historical_preparation_outputs']=len(rr)
rr=read(P/'FROZEN_INPUTS.json')['records']
for r in rr:check(A/r['path'],r)
check(Path(read(P/'FROZEN_INPUTS.json')['workspace_AGENTS']['path']),read(P/'FROZEN_INPUTS.json')['workspace_AGENTS'])
counts['preparation_inputs']=len(rr)
rr=read(P/'INPUT_COPY_MAP.json')['copies']
for r in rr:
    check(P/r['package_copy'],r);check(A/r.get('source_snapshot',r['original_path']),r)
    need((P/r['package_copy']).read_bytes()==(A/r.get('source_snapshot',r['original_path'])).read_bytes(),'Copy identity')
counts['source_equal_copy_map']=len(rr)
for name in ['priority_01','package_01']:
    q=A/'reviews'/name;rr=rows(read(q/'OUTPUT_PINS.json'))
    for r in rr:check(q/r['path'],r)
    counts[name+'_outputs']=len(rr)
rr=read(P/'WHOLE01_COPY_EXCLUSIONS.json')['records']
for r in rr:check(A/r['path'],r)
counts['individual_whole01_exclusions']=len(rr)
need(read(D/'INDEPENDENT_CHECKS_NORMAL.json')==read(D/'INDEPENDENT_CHECKS_OPTIMIZED.json'),'Independent mathematics under O')
counts['math_controls_exact_equal_both_modes']=True
rr=read(D/'INPUT_PINS.json')['files']
for r in rr:check(A/r['path'],r)
counts['review02_all_frozen_inputs_unchanged']=len(rr)
report={'status':'PASS','counts':counts,'all_actual_bytes_rehashed':True,'no_new_replay_of_omitted_programs':True,'historical_statuses_retained_with_dated_current_supersession':True}
(D/'CUSTODY_RECHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
