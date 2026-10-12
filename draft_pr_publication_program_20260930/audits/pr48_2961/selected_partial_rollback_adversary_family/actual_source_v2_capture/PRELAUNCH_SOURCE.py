"""Read/AST-only revised SOURCE and exact unrelated QUEUE delta; no helper import/run."""
import ast
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
if not __debug__ or sys.flags.optimize: raise RuntimeError('Optimized Python refused')
R=Path('/Users/alec/Documents/Math'); A=R/'draft_pr_publication_program_20260930/audits/pr48_2961'
P=A/'partial_finalize_v6_rollback_preparation'; H=Path(__file__).resolve().parent
OLD=A/'concurrent_finalize_failure_analysis/rollback_READY_candidate_v1_history'
COMMANDS=[]; sha=lambda b:hashlib.sha256(b).hexdigest(); utc=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def ref(p):
    need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Regular safe reference')
    s=p.stat(); b=p.read_bytes(); t=p.stat()
    ident=lambda q:(q.st_dev,q.st_ino,q.st_mode,q.st_size,q.st_mtime_ns,q.st_ctime_ns)
    need(ident(s)==ident(t),'Stable source/reference body')
    return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(s.st_mode)},b
def git_blob(commit):
    argv=['git','show',commit+':unsolved_math_prioritization/QUEUE.md']
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_LITERAL_PATHSPECS='1')
    for n in ['GIT_INDEX_FILE','GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']: env.pop(n,None)
    start=utc(); child=subprocess.Popen(argv,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=30)
    COMMANDS.append({'argv':argv,'pid':child.pid,'started_utc':start,'finished_utc':utc(),'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr_utf8':err.decode(errors='replace'),'stdout_consumed_in_memory_retrievable_from_named_Git_object':True,'stdout_body_duplicated_in_review_packet':False})
    need(child.returncode==0 and not err,'Exact historical/current Git blob retrieval')
    return out
started=utc(); readyref,readybody=ref(P/'SOURCE_READY.json'); ready=json.loads(readybody)
need(readyref['sha256']=='4029c8c79447c9d3a3cb57749c01712237afe41ecf07806cbc48757a53dd078c','Exact received revised READY')
need(ready['payload_count']==7 and {q.name for q in P.iterdir()}==set(ready['payload_names']) and stat.S_IMODE(P.stat().st_mode)==0o755,'Exact current seven-source topology/full modes')
refs=[readyref]
for expected in ready['source_rows_except_READY']:
    rr,b=ref(R/expected['path']); need(rr==expected and rr['full_mode']==0o644,'Exact revised complete source/mode'); refs.append(rr)
helperref,helperbody=ref(P/'rollback_partial.py')
need(helperref['sha256']=='6346ef27ed595bb13e895d35d94de108ef8125477bf6b3bb8e72608345894c3e','Exact revised helper')
old_tree=ast.parse((OLD/'rollback_partial.py').read_bytes()); new_tree=ast.parse(helperbody)
funcs=lambda tree:{x.name:x for x in tree.body if isinstance(x,ast.FunctionDef)}
old,new=funcs(old_tree),funcs(new_tree)
unchanged=[]
for name in sorted(set(old)-{'main','entry','git'}):
    need(ast.dump(old[name])==ast.dump(new[name]),'Changed mutation/preservation primitive '+name); unchanged.append(name)
need(set(old)==set(new) and not any(isinstance(x,ast.Assert) for x in ast.walk(new_tree)),'No unexpected function/removable assert')
main=copy.deepcopy(new['main'])
for node in ast.walk(main):
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='receipt':
        node.value.keywords=[k for k in node.value.keywords if k.arg not in {'overall_rollback_success_claimed','lock_release_pending'}]
        for k in node.value.keywords:
            if k.arg=='status': k.value=ast.Constant(value='PASS_EXACT_SELECTED_ROLLBACK_ONLY')
need(ast.dump(main)==ast.dump(old['main']),'Native main changes exceed pending-release receipt fields')
planref,planbody=ref(P/'PLAN.json'); plan=json.loads(planbody)
v1=json.loads((OLD/'PLAN.json').read_bytes())
for key in ['partial11','partial_manifest','original_overlay','inventory_original','owned_logs','fixed_failed_evidence','fixed_directory_modes','original_merge_commit']:
    need(plan[key]==v1[key],'Changed strict fixed restoration/failure input '+key)
for z in plan['unrelated_native12']:
    if z['path']!='unsolved_math_prioritization/QUEUE.md': need(z in v1['unrelated_native12'],'Changed other native11')
qref,q=ref(R/'unsolved_math_prioritization/QUEUE.md')
need(qref['bytes']==383256 and qref['sha256']=='b93679ffbcf51aead7f34d82679c528d3157efdffe46ca16ea3118c8c4ba2826' and qref['full_mode']==0o644 and qref in plan['unrelated_native12'],'Exact fixed current whole QUEUE pin')
oldq=git_blob('11590683569346ea67151a497e798094347c8d29')
newq=git_blob('08adf9cb444d365fd148a2bb3e2951a7f49c6808')
need(len(oldq)==383248 and sha(oldq)=='f8ec5b412e40a4258a861907e9ad96a1ede62f3a55694b290f31e6c2e627dfdc' and newq==q,'Exact dated old/current authentic blobs')
line=lambda b,id:[z for z in b.splitlines(keepends=True) if ('| '+id+' /').encode() in z]
oldrow=line(oldq,'2303002'); newrow=line(q,'2303002')
need(len(oldrow)==len(newrow)==1 and newrow[0]==oldrow[0].replace(b'| queued |',b'| already_solved |',1) and oldq.replace(oldrow[0],newrow[0],1)==q,'Only exact unrelated status delta')
need(len(line(q,'2961'))==1 and line(oldq,'2961')==line(q,'2961'),'Selected2961 byte-exact unchanged')
reads=json.loads((P/'SOURCE_READS.json').read_bytes())
for c in reads['complete_readonly_commands']:
    for stream in ['stdout','stderr']:
        b=c['entire_'+stream+'_utf8'].encode(); need(len(b)==c[stream+'_bytes'] and sha(b)==c[stream+'_sha256'],'Exact revised SOURCE-author full command stream')
capdir=A/'concurrent_finalize_failure_analysis/source_binding_repaired_final_actual_capture'
capref,capbody=ref(capdir/'CAPTURE.json'); cap=json.loads(capbody)
need(cap['pid']==29022 and cap['exit_code']==0 and cap['production_rollback_executed'] is False,'Actual revised SOURCE author only')
for stream in ['stdout','stderr']:
    rr,b=ref(capdir/cap[stream]['path']); need(len(b)==cap[stream]['bytes'] and sha(b)==cap[stream]['sha256'],'Revised actual author full stream')
rr,b=ref(capdir/'PRELAUNCH_SOURCE.py'); need(rr['sha256']==cap['prelaunch_source']['sha256'],'Revised author authentic prelaunch')
result={'schema':'pr48-independent-repaired-SOURCE-read-AST-check/v1','actual_inspector_pid':os.getpid(),'started_utc':started,'finished_utc':utc(),'received_SOURCE':readyref,'received_helper':helperref,'received_plan':planref,'all_seven_source_rows':refs,'unchanged_native_and_preservation_functions_AST':unchanged,'native_main_AST_unchanged_except_pending_release_receipt':True,'all_strict_fixed_inputs_unchanged_except_explicit_QUEUE_refresh':True,'current_fixed_QUEUE':qref,'queue_old_bytes':len(oldq),'queue_old_sha256':sha(oldq),'QUEUE_only_unrelated2303002_status_delta':True,'selected2961_row_byte_unchanged':True,'current_QUEUE_checkpoint':'08adf9cb444d365fd148a2bb3e2951a7f49c6808','read_only_Git_blob_queries':COMMANDS,'source_author_capture':capref,'source_author_pid':29022,'source_author_command_count_verified':len(reads['complete_readonly_commands']),'F1_F1a_F2_repair_personally_read':True,'runtime_controls_executed':False,'proposed_helper_import_or_execution':False,'native_Git_index_ref_or_remote_mutation':False,'new_math_review_credit':0,'ROOT_approval_or_actual_rollback_claimed':False,'status':'PASS_READ_AST_AND_EXACT_QUEUE_SCOPE_CHECKS'}
print(json.dumps(result,sort_keys=True,indent=2))
