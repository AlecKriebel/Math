#!/usr/bin/env python3
"""Readonly full actual-capture check, with derived own bindings only."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, sys
assert __debug__ and not sys.flags.optimize
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
def t(v):
    x=dt.datetime.fromisoformat(v.replace('Z','+00:00')); assert x.utcoffset()==dt.timedelta(0); return x
rows=[]; full=[]
def bind(p):
    assert not p.is_symlink() and stat.S_ISREG(p.stat().st_mode)
    b=p.read_bytes(); rows.append({'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}); return b
C=R/'draft_pr_publication_program_20260930/audits/pr45_9900007/root_pr47_source_preparation_closure_actual_capture'
c=json.loads(bind(C/'CAPTURE.json')); assert c['pid']==87649 and c['exit_code']==0 and c['actual_execution'] is True and c['completed'] is True and c['status']=='PASS'
assert t(c['started_utc'])<=t(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
assert c['argv']==['/usr/bin/python3','-B',str(A/'current_preparation_family/close_source_preparation.py')]
for k in ['stdout','stderr']:
    b=bind(C/c[k]['path']); assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
op=bind(C/'prelaunch_operator.py'); assert sha(op)==c['operator_sha256']
s=bind(A/'ROOT_SOURCE_CLOSURE_PRELAUNCH_SOURCE.py'); assert sha(s)=='4bcf06f6d4ea613cd3e41dd6ef8c2c2343b31d917aaa718a2775e61ceec96e35' and s==(A/'current_preparation_family/close_source_preparation.py').read_bytes()
full.append(c)
for name,exitcode in [('controls_actual_capture',1),('controls_actual_capture_v2',1),('controls_actual_capture_v3',1),('controls_actual_capture_v4',0),('extended_actual_capture',0)]+[('negative_'+n,1) for n in ['null_Git_source_as_helper','nine_bit_mode','null_absence_fallback','future_current_approval']]:
    D=F/name; cap=json.loads((D/'CAPTURE.json').read_bytes()); pre=json.loads((D/'PRELAUNCH.json').read_bytes())
    assert cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['exit_code']==exitcode and cap['source_unchanged'] is True and cap['operator_unchanged'] is True and cap['stdin_supplied'] is False
    assert t(pre['started_utc'])<=t(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
    for k in ['stdout','stderr']:
        b=(D/cap[k]['path']).read_bytes(); assert len(b)==cap[k]['bytes'] and sha(b)==cap[k]['sha256']
    assert sha((D/'PRELAUNCH_SOURCE.py').read_bytes())==cap['source_sha256'] and sha((D/'PRELAUNCH_OPERATOR.py').read_bytes())==cap['operator_sha256']
    full.append(cap)
out={'schema':'pr47-source-completed-actual-capture-validation/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'status':'PASS_COMPLETE_CAPTURE_BYTES_TYPED_HISTORY','external_full_bindings':rows,'complete_prior_actual_captures':full,'production_execution':False,'future_acceptance_approved':False,'original_cover_tool_only_chronology_not_reconstructed':True}
(F/'CLOSURE_CAPTURE_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps({'status':out['status'],'captures':len(full),'external_bindings':len(rows),'pid':os.getpid()},indent=2))
