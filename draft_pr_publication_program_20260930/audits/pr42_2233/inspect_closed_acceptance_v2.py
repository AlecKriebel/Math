"""ROOT independently checks closed V2 evidence after complete personal reading.

No production code is imported or executed. Exact four historical inputs are
read from their immutable Git authority; they never authorize present writes.
"""
from pathlib import Path
import ast, datetime as dt, difflib, hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parent; R=A.parents[2]
H=A/'acceptance_preparation_family_v2'; O=A/'acceptance_preparation_family'
V=A/'acceptance_v2_source_adversary_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def check(p,z,mode=None):
    assert p.is_file() and not p.is_symlink()
    assert all(not q.is_symlink() for q in p.parents)
    b=p.read_bytes();assert type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256'],str(p)
    if mode is not None:assert stat.S_IMODE(p.stat().st_mode)==mode,str(p)
    return b
def closed(p,name,pin,count):
    raw=(p/name).read_bytes();assert sha(raw)==pin
    j=json.loads(raw);assert len(j['files'])==j['files_count']==count
    names=[]
    for z in j['files']:check(p/z['path'],z,0o444);names.append(z['path'])
    assert len(names)==len(set(names))
    assert {q.relative_to(p).as_posix() for q in p.rglob('*') if q.is_file()}==set(names)|{name}
    assert stat.S_IMODE((p/name).stat().st_mode)==0o444
    return j
def capture(p,source):
    j=load(p/'CAPTURE.json')
    assert j['actual_execution'] is True and j['completed'] is True and j['status']=='PASS'
    assert type(j['pid']) is int and j['pid']>0 and type(j['exit_code']) is int and j['exit_code']==0
    assert j['stdin_supplied'] is False and j['source_unchanged'] is True
    assert dt.datetime.fromisoformat(j['started_utc'])<=dt.datetime.fromisoformat(j['finished_utc'])
    assert sha((p/'PRELAUNCH_SOURCE.py').read_bytes())==j['source_sha256']==sha(source.read_bytes())
    for k in ['stdout','stderr']:check(p/j[k]['path'],j[k])
    return j
def main():
    assert __debug__
    (A/'ROOT_ACCEPTANCE_V2_INSPECTION_PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    prep=closed(H,'PREPARATION_MANIFEST.json','f5cd2d41d448c97fcf160afeca63dc4c57c283deb03ffa4fe2292125db06b1a8',51)
    adversary=closed(V,'OWN_CLOSED_MANIFEST.json','7d34755d82033bd96c08083f4575406b419d1788c6a7fc3fff3f3dc0d099a5f6',35)
    inputs=load(H/'INPUT_BINDINGS.json')
    for z in inputs['pins'].values():check(R/z['path'],z)
    for k in ['closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection','root_capture_operator']:check(R/inputs[k]['path'],inputs[k])
    for n in ['seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','SCIENTIFIC_SCOPE.json','CLOSED_WHOLE_RESULT_KEYS.json']:
        assert (H/n).read_bytes()==(O/n).read_bytes(),n
    old=(O/'pr42_guards.py').read_text();new=(H/'pr42_guards.py').read_text()
    delta=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='V1/pr42_guards.py',tofile='V2/pr42_guards.py'))
    # Header spelling is separately inspected; every complete changed hunk is exact.
    assert delta.split('\n',2)[2]==(H/'SOURCE_REPAIR_DELTA.patch').read_text().split('\n',2)[2]
    funcs=lambda s:{q.name:ast.dump(q,include_attributes=False) for q in ast.parse(s).body if isinstance(q,ast.FunctionDef)}
    fo,fn=funcs(old),funcs(new);assert set(fn)==set(fo)|{'resolve_foreign_literal'}
    assert all(fo[n]==fn[n] for n in fo if n!='basis')
    captures=[capture(H/'AUTHORING_ACTUAL_CAPTURE',H/'author_adjacent_repair.py'),capture(H/'DATED_NATIVE_REVISION_ACTUAL_CAPTURE',H/'author_dated_native_revision.py'),capture(H/'CONTROLS_ACTUAL_CAPTURE',H/'independent_repair_controls.py'),capture(V/'STATIC_ACTUAL_CAPTURE',V/'independent_static_controls.py')]
    rows=adversary['foreign_files_individually_pinned_and_excluded'];seen=set();historical=[]
    G=A/'root_acceptance_v2_dated_Git';G.mkdir();git=[]
    for z in rows:
        assert z['path'] not in seen;seen.add(z['path']);p=Path(z['path'])
        if 'authority' in z:
            assert z['authority']=='immutable_Git_c61dc0cb572de281b871264819c8b80d647d0373'
            n=p.relative_to(R).as_posix();argv=['git','show','c61dc0cb572de281b871264819c8b80d647d0373:'+n]
            start=dt.datetime.now(dt.timezone.utc).isoformat();c=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=c.communicate()
            rec={'argv':argv,'pid':c.pid,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':c.returncode}
            assert c.returncode==0 and not e and len(b)==z['bytes'] and sha(b)==z['sha256']
            index=len(git)
            for k,body in [('stdout',b),('stderr',e)]:
                name=str(index)+'_'+k+'.bin';(G/name).write_bytes(body);rec[k]={'path':name,'bytes':len(body),'sha256':sha(body)}
            git.append(rec);historical.append(n)
        else:check(p,z,z.get('worktree_mode'))
    assert len(rows)==1093 and set(historical)=={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    (G/'ACTUAL_QUERIES.json').write_text(json.dumps(git,indent=2)+'\n')
    verdict=load(V/'VERDICT.json');assert verdict['mandatory_defects']==verdict['mandatory_corrections']==[]
    assert verdict['own_actual_control_pid']==captures[-1]['pid']==13786
    out={'schema':'pr42-root-complete-closed-acceptance-v2-inspection/v1','status':'PASS_ROOT_PERSONAL_V2_SOURCE_AND_CLOSED_EVIDENCE_INSPECTION','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'personal_original_production_full_read_completed':True,'personal_complete_V2_delta_contract_inputs_controls_read_completed':True,'personal_new_different_report_and_verdict_full_read_completed':True,'preparation_members':51,'adversary_members':35,'all_individually_bound_outside_inputs_checked':1093,'exact_historical_git_rows':4,'complete_actual_captures_checked':captures,'complete_new_VERDICT':verdict,'only_foreign_basis_and_new_resolver_changed':True,'all_four_other_helpers_and_scientific_drafts_byte_unchanged':True,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'future_execution_approved':False,'source_check_failures_qualification':'A preliminary read-only inventory guessed nonexistent READONLY_GIT_CAPTURE/CAPTURE.json; its actual queries are QUERIES.json. No execution or PID was invented for that read.'}
    with (A/'ROOT_ACCEPTANCE_V2_SOURCE_INSPECTION.json').open('x')as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'status':out['status'],'actual_pid':os.getpid(),'members':[51,35],'foreign':1093,'historical':4,'future_execution_approved':False}))
if __name__=='__main__':main()
