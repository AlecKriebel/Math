"""Bounded private V2 source/capture readback; no production import/compile/run."""
from pathlib import Path
import json,hashlib,datetime as dt,stat,os
F=Path(__file__).absolute().parent
R=F.parents[3]
def need(v,m):
    if not v:raise ValueError(m)
def raw(p):need(p.is_file() and not p.is_symlink() and all(not x.is_symlink() for x in p.parents),'Regular owned input');return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):b=raw(p);return {'path':p.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)}
def load(p):return json.loads(raw(p))
def eq(a,b):return type(a) is type(b) and (a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def main():
    d=F/'private_mode_repair_v2_actual_capture';c=load(d/'CAPTURE.json');pre=load(d/'PRELAUNCH.json')
    need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Exact private CAP6')
    need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==13772 and type(c['exit_code']) is int and c['exit_code']==0 and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['production_import_compile_or_execution'] is False,'Genuine complete private model run')
    need(c['argv']==['/usr/bin/python3','-B',str(F/'private_mode_repair_controls.py')] and c['cwd']==str(R) and all(eq(c[k],v) for k,v in pre.items() if k!='schema'),'Entire actual private prelaunch')
    need(sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256']==sha(raw(F/'private_mode_repair_controls.py')) and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256']==sha(raw(F/'capture_owned_operation.py')),'Entire actual private source/operator')
    for ch in ['stdout','stderr']:need(c[ch]['path']==ch+'.bin' and eq(c[ch],{'path':ch+'.bin','bytes':len(raw(d/(ch+'.bin'))),'sha256':sha(raw(d/(ch+'.bin')))}),'Whole actual streams')
    result=load(F/'PRIVATE_MODE_REPAIR_RESULT.json');need(raw(d/'stderr.bin')==b'' and eq(json.loads(raw(d/'stdout.bin')),result),'Entire printed/saved private result')
    start=dt.datetime.fromisoformat(c['started_utc']);end=dt.datetime.fromisoformat(c['finished_utc']);need(start.tzinfo is not None and end.tzinfo is not None and start<=dt.datetime.fromisoformat(result['utc'])<=end<=dt.datetime.now(dt.timezone.utc),'Actual private aware UTC')
    for row in result['replacement_models']:
        z=row['after'];p=F/z['path'];need(eq(ref(p),z) and type(row['after_mode']) is int and stat.S_IMODE(p.stat().st_mode)==row['after_mode']==row['before_mode']==row['expected_mode'],'Actual selected private body/mode readback')
    names=['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py','ROOT_POST_CONTRACT.json','CONTRACT.md','REPORT.md','VERDICT.json','close_source.py','verify_closed_source.py','SUPERSEDED_SOURCE_BINDINGS.json','CHANGE_MAP.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json']
    refs={n:{k:v for k,v in ref(F/n).items() if k!='path'} for n in names}
    out={'schema':'pr48-acceptance-SOURCE-v2-bounded-final-readback/v1','status':'READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source_files':refs,'entire_private_model_capture':c,'entire_private_model_result':result,'production_imported_compiled_executed':False,'actual_PR47_predecessor_completed':False,'future_acceptance_approved':False,'new_SOURCE_review_pending':True,'discovery_completion_percent':0}
    with (F/'FINAL_READY_CHECK.json').open('x') as h:h.write(json.dumps(out,sort_keys=True,indent=2)+'\n');h.flush();os.fsync(h.fileno())
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
