"""In-place PR49 closed-whole reconciliation reader; writes nothing."""
from pathlib import Path
from datetime import datetime
import os,json,stat,hashlib
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr49_30000703';C=A/'reviewed_candidate';W=A/'current_whole_adversary_family';A45=A.parent/'pr45_9900007'
CM='8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47';WM='b3d91982e7a2cfbda0ffce7fe0e45141dabafcb374aecd52078ad3d66a1e9736';REPORT='4b991d3913f50d4f750e9bf7ed0187bd48fe99a7f1addc1db32fe80be5f87c73'
N4={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/state.json'}
def observed(p):
    p=Path(p);assert p.is_relative_to(R)
    for q in [p,*p.parents]:
        if q==R.parent:break
        assert not q.is_symlink(),str(q)
    s=p.lstat();assert stat.S_ISREG(s.st_mode),str(p)
    b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=stat.S_IMODE(s.st_mode))
def tree(p):
    fs=[];ds=[]
    for root,dirs,files in os.walk(p,followlinks=False):
        for n in dirs:
            q=Path(root)/n;assert q.is_dir() and not q.is_symlink();ds.append(str(q.relative_to(p)))
        for n in files:
            q=Path(root)/n;assert q.is_file() and not q.is_symlink();fs.append(str(q.relative_to(p)))
    return sorted(fs),sorted(ds)
def collect():
    rows={};groups={};captures=[]
    def add(p,v=None):
        key=str(p.relative_to(R))
        if key not in rows:rows[key]=observed(p)
        q=rows[key]
        if v:
            for k in ['bytes','sha256','full_mode']:
                if k in v:assert type(q[k]) is type(v[k]) and q[k]==v[k],(key,k)
        return key
    def load(p):add(p);return json.loads(p.read_bytes())
    add(C/'MANIFEST.json',dict(sha256=CM,full_mode=0o444));cm=load(C/'MANIFEST.json')
    assert len(cm['files'])==cm['files_count']==1544
    groups['current_payload']=[add(C/v['path'],v) for v in cm['files']]
    fs,ds=tree(C);assert fs==sorted([v['path'] for v in cm['files']]+['MANIFEST.json']) and len(ds)==273
    groups['current_manifest']=[str((C/'MANIFEST.json').relative_to(R))]
    add(W/'SELF_MANIFEST.json',dict(sha256=WM,full_mode=0o444));wm=load(W/'SELF_MANIFEST.json')
    assert wm['schema']=='pr49-current-whole-adversary-self-only-closure/v2' and wm['files_count']==127 and len(wm['files'])==127
    groups['closed_whole_payload']=[add(W/v['path'],v) for v in wm['files']]
    fs,wd=tree(W);assert fs==sorted([v['path'] for v in wm['files']]+['SELF_MANIFEST.json']) and wd==wm['directories'] and len(wd)==16
    for v in wm['directory_full_modes']:assert stat.S_IMODE((W/v['path']).lstat().st_mode)==v['full_mode']
    verdict=load(W/'VERDICT.json');add(W/'REPORT.md',dict(sha256=REPORT,full_mode=0o444))
    assert verdict['mandatory_corrections']==[] and verdict['verdict']=='PASS_CREDITED_KNOWN_UNRESTRICTED_REFLECTION_CURRENT_PACKET_CUSTODY_REPAIRED'
    assert verdict['status']=='already_solved' and verdict['original_substantive_attempts']==verdict['new_substantive_attempts']==verdict['audit_turns']==0
    assert verdict['blind_new_math_family'] is False and verdict['full_2007_journal_proof_independently_certified'] is False
    assert all(verdict[k] is False for k in ['project_solved','novelty_claimed','future_acceptance_approved','ROOT_approval_created','paper_created','new_DOI_created','tracker_row_created'])
    fixed=wm['external_body_mode_bindings'];assert len(fixed)==3083 and not ({v['path'] for v in fixed}&N4)
    groups['whole_fixed_inputs']=[add(R/v['path'],v) for v in fixed]
    dated=wm['dated_native4'];assert len(dated)==4 and {v['original_observed_row']['path'] for v in dated}==N4
    dated_by_path={v['original_observed_row']['path']:v for v in dated}
    for v in dated:
        old=v['original_observed_row'];snap=v['whole_historical_snapshot'];add(R/snap['path'],snap)
        assert old['bytes']==snap['bytes'] and old['sha256']==snap['sha256'] and old['full_mode']==0o644 and snap['full_mode']==0o444
        assert v['live_unchanged_required_by_review_closure'] is False and v['future_fresh13_ROOT_required'] is True
        add(R/v['freeze_input_authority']['path'],v['freeze_input_authority'])
    assert wm['native4_is_dated_only'] is True and wm['future_fresh13_ROOT_required'] is True
    groups['retained_failed_closure_bindings']=[add(R/v['path'],v) for v in wm['retained_ROOT_failed_closure_fixed_members']]
    assert len(groups['retained_failed_closure_bindings'])==5
    dep=load(C/'CURRENT_DEPENDENCIES.json');assert len(dep['files'])==1407
    groups['current_fixed_dependencies']=[];dated_deps=[]
    for v in dep['files']:
        if v['path'] in N4:
            old=dated_by_path[v['path']]['original_observed_row']
            for k in ['path','bytes','sha256','full_mode']:assert v[k]==old[k] and type(v[k]) is type(old[k])
            dated_deps.append(v['path'])
        else:groups['current_fixed_dependencies'].append(add(R/v['path'],v))
    assert len(groups['current_fixed_dependencies'])==1403 and set(dated_deps)==N4
    def cap4(name,pid,rc):
        d=A45/name;q=load(d/'CAPTURE.json');members=[add(d/n) for n in ['CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin']]
        assert q['pid']==pid and q['exit_code']==rc and q['completed'] is True and q['actual_execution'] is True and q['operator_unchanged'] is True
        assert rows[str((d/'prelaunch_operator.py').relative_to(R))]['sha256']==q['operator_sha256']
        assert datetime.fromisoformat(q['started_utc'])<datetime.fromisoformat(q['finished_utc'])
        for k in ['stdout','stderr']:add(d/q[k]['path'],q[k])
        out=(d/'stdout.bin').read_bytes();err=(d/'stderr.bin').read_bytes()
        parsed=json.loads(out) if rc==0 else None
        captures.append(dict(capture=q,members=members,complete_stdout_object=parsed,stderr_utf8=err.decode('utf-8')))
        return q,parsed
    fail,_=cap4('root_pr49_current_whole_closure_actual_capture',82903,1)
    close,co=cap4('root_pr49_current_whole_closure_v2_actual_capture',267,0)
    wrong,_=cap4('root_pr49_current_whole_closed_readback_v2_actual_capture',444,1)
    read,ro=cap4('root_pr49_current_whole_closed_readback_v3_actual_capture',755,0)
    assert co['manifest_sha256']==ro['manifest_sha256']==WM and co['actual_closing_pid']==267 and ro['actual_readback_pid']==755
    assert co['files_count']==ro['files_count']==127 and ro['external_rows']==3083
    assert wrong['argv'][-1]=='3b2f84c9c72a91be96ed8032ba727bd9ab680082ec65febd8fda3da39cb70a11'
    assert close['argv'][-1]==REPORT and read['argv'][-1]==WM
    assert datetime.fromisoformat(fail['finished_utc'])<datetime.fromisoformat(close['started_utc'])<datetime.fromisoformat(close['finished_utc'])<datetime.fromisoformat(wrong['started_utc'])<datetime.fromisoformat(wrong['finished_utc'])<datetime.fromisoformat(read['started_utc'])
    assert (A/'ROOT_WHOLE_CLOSURE_PRELAUNCH_SOURCE.py').read_bytes()==(W/'historical_v1/close_review_ROOT_only.py').read_bytes()
    assert (A/'ROOT_WHOLE_CLOSURE_V2_PRELAUNCH_SOURCE.py').read_bytes()==(W/'close_review_ROOT_only.py').read_bytes()
    add(A/'ROOT_WHOLE_CLOSURE_PRELAUNCH_SOURCE.py');add(A/'ROOT_WHOLE_CLOSURE_V2_PRELAUNCH_SOURCE.py')
    math=[]
    for name,key,count in [('boundary_analysis_family/MANIFEST.json','members',473),('hyperbolic_geometry_family/SELF_MANIFEST.json','payload_files',107),('root_original_actual_reproduction/MANIFEST.json','files',192)]:
        p=A/name;q=load(p);assert len(q[key])==count
        group=[]
        for v in q[key]:
            v=dict(v)
            if 'mode' in v:v['full_mode']=int(v.pop('mode'),8)
            group.append(add(p.parent/v['path'],v))
        groups[name]=group;math.append(dict(manifest=str(p.relative_to(R)),schema=q['schema'],payloads=count,actual_member_convention=key))
    frozen=load(A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json')
    assert frozen['candidate_manifest']['sha256']==CM and frozen['frozen48_honest_prefix_of_actual50'] is True
    for key in ['complete_outer_members','complete100_inner_streams']:
        for v in frozen[key]:add(R/v['path'],v)
    add(R/frozen['original_inner_record']['path'],frozen['original_inner_record'])
    assert len(frozen['entire_final_original_inner_commands'])==50 and len(frozen['complete100_inner_streams'])==100
    for v in frozen['complete_current_payload']:add(R/v['path'],v)
    for v in frozen['complete_dependencies']:
        if v['path'] in N4:assert v==dated_by_path[v['path']]['original_observed_row']
        else:add(R/v['path'],v)
    ordered=sorted(rows.values(),key=lambda v:v['path']);index={v['path']:i for i,v in enumerate(ordered)}
    return dict(normalized_complete_fixed_bindings=ordered,binding_groups={k:[index[n] for n in v] for k,v in groups.items()},dated_native4=dated,current_payload_count=1544,current_relative_directories=ds,current_dependency_count=1407,current_fixed_dependency_count=1403,closed_whole_payload_count=127,closed_whole_relative_directories=wd,whole_fixed_input_count=3083,retained_failed_closure_binding_count=5,complete_actual_closure_and_readback_captures=captures,entire_VERDICT_object=verdict,prior_closed_mathematical_and_reproduction_families=math,current_manifest=rows[str((C/'MANIFEST.json').relative_to(R))],closed_whole_manifest=rows[str((W/'SELF_MANIFEST.json').relative_to(R))],whole_report=rows[str((W/'REPORT.md').relative_to(R))],original_final_inner_commands=50,frozen_inner_prefix=48,original_full_inner_streams=100,future_fresh13_ROOT_required=True,current_live_native4_or_main_authority=False,future_acceptance_approved=False,paper=False,DOI=False,tracker=False)
def recheck(q):
    for v in q['normalized_complete_fixed_bindings']:assert observed(R/v['path'])==v
