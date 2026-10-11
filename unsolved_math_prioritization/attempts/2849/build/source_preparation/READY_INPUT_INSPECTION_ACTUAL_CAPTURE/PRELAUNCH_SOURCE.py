"""Read complete fixed SOURCE dependencies and actual private captures; no approval."""
import datetime as dt, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
reads={}; assertions=0
def need(v,m):
    global assertions
    if not v: raise ValueError(m)
    assertions+=1
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink read');b=p.read_bytes();rr={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)};need(rr['path'] not in reads or reads[rr['path']]==rr,'Repeated full body unchanged');reads[rr['path']]=rr;return b
def check(rr):
    need(type(rr) is dict and set(rr)=={'path','bytes','sha256','full_mode'} and type(rr['bytes']) is int and type(rr['full_mode']) is int,'Exact fixed typed full mode row');p=R/rr['path'];b=raw(p);need(len(b)==rr['bytes'] and sha(b)==rr['sha256'] and stat.S_IMODE(p.stat().st_mode)==rr['full_mode'],'Exact fixed full body/mode')
def clock(s):
    t=dt.datetime.fromisoformat(s.replace('Z','+00:00'));need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'AwareUTC');return t
def main():
    need(__debug__ and not (A/'reviewed_candidate').exists(),'No current freeze')
    fixed=json.loads(raw(F/'STATIC_INPUT_BINDINGS.json'));root=json.loads(raw(F/'ROOT_FIXED_EVIDENCE.json'));repair=json.loads(raw(F/'SOURCE_V1_REPAIR_BINDINGS.json'))
    for rr in fixed['complete_fixed_member_reads']+[root['manifest']]+root['members']+root['separate_actual_closure_members']+repair['complete_fixed_member_reads']+repair['external_ROOT_closure_and_readback_members']:check(rr)
    expected={'AUTHORING_ACTUAL_CAPTURE':(17487,0),'PRIVATE_CONTROLS_ACTUAL_CAPTURE':(19224,0),'PRIVATE_EXPECTED_NEGATIVE_ACTUAL_CAPTURE':(19709,1),'FINAL_QUALIFICATION_ACTUAL_CAPTURE':(20983,0),'PRIVATE_CONTROLS_FINAL_ACTUAL_CAPTURE':(21205,1),'PRIVATE_CONTROLS_FINAL_V2_ACTUAL_CAPTURE':(21786,0)};caps=[]
    # Our own live outer is deliberately unfinished during this read-only child.
    for name,(pid,exitcode) in expected.items():
        d=F/name;need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Actual six-member completed capture');c=json.loads(raw(d/'CAPTURE.json'));pre=json.loads(raw(d/'PRELAUNCH.json'));need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==exitcode and c['stdin_supplied'] is False and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['production_import_compile_or_execution'] is False,'Exact completed own child')
        need(clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Completed own awareUTC interval');need(sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Literal prelaunch source/operator hashes')
        for k,v in pre.items():need(c[k]==v if k!='schema' else v=='PR47_SOURCE_V2_PREPARATION_PRELAUNCH_v1','Real prelaunch record')
        for ch in ['stdout','stderr']:
            b=raw(d/c[ch]['path']);need(len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256'],'Complete own separate stream')
        caps.append(c)
    result={'schema':'PR47_SOURCE_V2_FULL_READY_INPUT_INSPECTION_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_readonly_pid':os.getpid(),'assertions':assertions,'entire_unique_fixed_body_read_rows':list(reads.values()),'full_unique_fixed_read_bytes':sum(rr['bytes'] for rr in reads.values()),'complete_prior_six_own_actual_captures':caps,'own_live_outer_not_claimed_completed':True,'production_import_compile_or_execution':False,'future_acceptance_approved':False,'new_different_clean_SOURCE_adversary_required':True,'foreign_bodies_copied':False}
    with (F/'READY_INPUT_INSPECTION.json').open('x') as h:json.dump(result,h,indent=2,ensure_ascii=False,allow_nan=False);h.write('\n');h.flush();os.fsync(h.fileno())
    print(json.dumps({'status':'PASS_ALL_FIXED_FIRST_PARTY_INPUTS_AND_SIX_PRIOR_ACTUAL_CAPTURES','assertions':assertions,'unique_full_body_reads':len(reads),'full_read_bytes':result['full_unique_fixed_read_bytes'],'production_executed':False}))
if __name__=='__main__':main()
