"""ROOT-only completion of the independently reviewed PR46 V2 SOURCE records.

Requires actual separate closing/readback captures. No production module runs.
"""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, math, os, re, stat, sys
A=Path(__file__).absolute().parent;R=A.parents[2]
S=A/'acceptance_preparation_family_v2';F=A/'acceptance_source_adversary_family_v2';B=A.parent/'pr45_9900007'
PREP='f44ccf65fa4397736305881de926eafcf211c33ef9e6fec5e5596c99d252ef40'
def need(v,s):
    if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');return p.read_bytes()
def load(p):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'Duplicate key');d[k]=v
        return d
    o=json.loads(raw(p),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
    def finite(v):
        if type(v) is float:need(math.isfinite(v),'Finite float')
        elif type(v) is dict:
            for x in v.values():finite(x)
        elif type(v) is list:
            for x in v:finite(x)
    finite(o);return o
def eq(a,b):
    return type(a) is type(b) and (a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def safe(n):
    p=PurePosixPath(n);need(type(n) is str and n and p.as_posix()==n and not p.is_absolute() and not {'.','..','.git','__pycache__'}&set(p.parts) and '\\' not in n,'Canonical member');return n
def ref(p,mode=False):
    b=raw(p);o=dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
    if mode:o['full_mode']=stat.S_IMODE(p.stat().st_mode)
    return o
def check(z):
    safe(z['path']);need(type(z['bytes']) is int and z['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Typed reference')
    q=ref(R/z['path'],'full_mode' in z);need(all(eq(q[k],z[k]) for k in q),'Full body/mode changed');return q
def closure(d,n,pin,count):
    need(sha(raw(d/n))==pin,'Exact manifest');m=load(d/n);need(m['self_excluded']==[n] and type(m['files_count']) is int and m['files_count']==len(m['files'])==count,'Exact self count')
    names=set();out=[]
    for z in m['files']:
        safe(z['path']);need(z['path'] not in names,'Unique member');names.add(z['path']);q=check(dict(z,path=d.relative_to(R).as_posix()+'/'+z['path']));need(stat.S_IMODE((R/q['path']).stat().st_mode)==292,'Full0444');out.append(ref(R/q['path'],True))
    files=set();dirs=set()
    for p in d.rglob('*'):
        need(not p.is_symlink(),'No symlink');x=safe(p.relative_to(d).as_posix())
        if p.is_file():files.add(x);need(stat.S_IMODE(p.stat().st_mode)==292,'All full0444')
        else:need(p.is_dir(),'No special file');dirs.add(x)
    need(files==names|{n} and dirs=={str(p) for x in files for p in PurePosixPath(x).parents if str(p)!='.'},'Exact recursive self topology')
    return m,out
def clock(s):
    t=dt.datetime.fromisoformat(s);need(t.utcoffset()==dt.timedelta(0),'Aware UTC');return t
def capture(p):
    c=load(p);d=p.parent;need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int,'True completed child')
    need(clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(now()),'Actual chronology')
    for k in ['stdout','stderr']:
        z=c[k];b=raw(d/safe(z['path']));need(type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256'],'Complete streams')
    if (d/'PRELAUNCH.json').exists():
        pre=load(d/'PRELAUNCH.json');need(sha(raw(d/'PRELAUNCH_SOURCE.py'))==pre['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==pre['operator_sha256'],'Retained complete prelaunch sources')
        need(c['source_unchanged'] is True and c['operator_unchanged'] is True,'Captured sources unchanged at actual exit')
    else:need(c['operator_unchanged'] is True and sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256'],'CAP4 operator source')
    return dict(reference=ref(p),complete_capture=c,complete_members=[ref(x,True) for x in sorted(d.iterdir()) if x.is_file()])
def put(n,o):
    with (A/n).open('x') as f:json.dump(o,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
def main():
    need(__debug__ and len(sys.argv)==2,'ROOT personally read report/source before giving actual closed manifest SHA')
    prep,prepared=closure(S,'PREPARATION_MANIFEST.json',PREP,109);fm,owned=closure(F,'SELF_MANIFEST.json',sys.argv[1],55)
    v=load(F/'VERDICT.json');need(v['schema']=='pr46-acceptance-source-adversary-verdict/v1' and v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['preparation_manifest_sha256']==PREP and v['mandatory_corrections']==[] and v['production_imported_compiled_executed'] is False and v['future_acceptance_approved'] is False,'Exact new scoped SOURCE verdict')
    fixed=load(F/'FIXED_CORPUS_RESULT_V3.json');external={}
    for z in fixed['complete_read_bindings']:
        p=Path(z['canonical_path']);need(p.is_absolute() and p.is_relative_to(R) and p==p.resolve() and not p.is_symlink(),'Canonical in-repository input')
        q=dict(path=p.relative_to(R).as_posix(),bytes=z['bytes'],sha256=z['sha256'],full_mode=z['full_mode']);check(q)
        need(q['path'] not in external or eq(external[q['path']],q),'Consistent repeated input');external[q['path']]=q
    need(len(external)==2851 and len(fixed['complete_read_bindings'])==9244,'Entire independent corpus')
    actual=[capture(p) for d in [S,F] for p in sorted(d.rglob('CAPTURE.json'))]
    pair=[capture(B/n/'CAPTURE.json') for n in ['root_pr46_acceptance_source_v2_adversary_closure_actual_capture','root_pr46_acceptance_source_v2_adversary_closed_readback_actual_capture']]
    c,d=[z['complete_capture'] for z in pair];need(c['exit_code']==d['exit_code']==0 and c['argv'][2]==str(F/'close_family.py') and d['argv'][2]==str(F/'verify_closed_family.py') and c['pid']==fm['actual_closing_pid'] and clock(c['started_utc'])<=clock(fm['created_utc'])<=clock(c['finished_utc'])<clock(d['started_utc']),'Genuine ROOT closure and separate postexit readback')
    actual+=pair;inputs=load(S/'INPUT_BINDINGS.json')
    for z in list(inputs['pins'].values())+[inputs[k] for k in ['previous_mirror','previous_post','previous_root_post','closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection']]:check(z)
    previous=load(R/inputs['previous_mirror']['path']);post=load(R/inputs['previous_post']['path']);rp=load(R/inputs['previous_root_post']['path'])
    need(eq(post,load(S/'EXPECTED_PREVIOUS_POST.json')) and eq(rp,load(S/'EXPECTED_PREVIOUS_ROOT_POST.json')) and eq(rp['entire_post'],post) and rp['schema']=='pr45-root-complete-actual-post-inspection/v1' and len(previous['entries'])==35,'Entire actual PR45 predecessor personally completed earlier and independently rebound')
    operator=A/'capture_root_final_operation.py';need(not operator.exists(),'Never replace deployed source');operator.write_bytes(raw(S/operator.name))
    inspection=dict(schema='pr46-root-complete-acceptance-source-inspection/v1',status='PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION',utc=now(),all_prepared_source_and_controls_fully_read=True,exact_preparation_closure_and_full_modes_checked=True,all_individual_source_adversary_inputs_checked=True,all_complete_actual_captures_checked=True,complete_VERDICT_object=v,preparation_manifest_sha256=PREP,acceptance_source_manifest=ref(F/'SELF_MANIFEST.json'),acceptance_source_verdict=ref(F/'VERDICT.json'),mandatory_corrections=[],future_execution_approved=False,complete_prepared_bindings=prepared,complete_closed_adversary_bindings=owned,individual_external_bindings=list(external.values()),all_complete_source_captures=actual,entire_fixed_result=fixed,ROOT_personal_reading='ROOT fully read six operative helpers, final controls, contract and post contract, complete new report/verdict/invariant/primary qualifications/closer/verifier as text. Runtime reconciliation reads all closed payloads/full modes and2851 unique external inputs plus all actual captures/streams; historical preparing prelaunch snapshots remain separate from final revised sources. PR45 full actual post was personally completed earlier; no future execution inferred.')
    put('ROOT_SOURCE_ACCEPTANCE_REVIEW.json',inspection)
    bindings=load(S/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');bindings.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR45_EVIDENCE',created_utc=now(),root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR45_predecessor_read_completed=True)
    paths=dict(whole_manifest=A/'current_whole_adversary_family/MANIFEST.json',root_whole_inspection=A/'ROOT_WHOLE_CURRENT_REVIEW.json',root_capture_operator=operator,acceptance_source_manifest=F/'SELF_MANIFEST.json',acceptance_source_verdict=F/'VERDICT.json',root_source_inspection=A/'ROOT_SOURCE_ACCEPTANCE_REVIEW.json')
    paths.update({k:R/inputs[k]['path'] for k in ['previous_mirror','previous_post','previous_root_post']})
    for k,p in paths.items():bindings[k]=ref(p)
    put('ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json',bindings)
    repair=load(S/'SOURCE_REPAIR_BINDINGS.json');refs=[{k:z[k] for k in ['path','bytes','sha256']} for z in repair['complete_first_party_refs']]+list(inputs['pins'].values())
    refs+=[ref(A/'reviewed_candidate/MANIFEST.json'),ref(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json'),inputs['closed_whole_manifest'],inputs['closed_whole_result'],inputs['closed_whole_report'],inputs['closed_whole_external_inventory'],bindings['root_whole_inspection'],ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')]+[bindings[k] for k in ['previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
    dedup={}
    for z in refs:check(z);need(z['path'] not in dedup or eq(dedup[z['path']],z),'Conflicting plan identity');dedup[z['path']]=z
    plan=load(S/'DRAFT_FINAL_PLAN.json');plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=PREP,whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_bindings=ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')['path'],root_bindings_sha256=sha(raw(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')),root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,root_actual_PR45_predecessor_read_completed=True,independent_whole_current_pass=True,immutable_evidence_references=sorted(dedup.values(),key=lambda z:z['path']))
    put('ROOT_FINAL_PLAN.json',plan)
    print(json.dumps(dict(status='PASS_ROOT_COMPLETE_V2_SOURCE_AND_ACTUAL_PR45_BINDINGS',actual_pid=os.getpid(),prepared=109,adversary=55,unique_external=len(external),actual_captures=len(actual),plan_refs=len(dedup),future_execution_approved=False)))
if __name__=='__main__':main()
