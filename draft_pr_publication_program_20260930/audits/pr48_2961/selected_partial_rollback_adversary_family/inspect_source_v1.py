"""Read/AST-only candidate custody check; never imports or executes proposed code."""
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

if not __debug__ or sys.flags.optimize: raise RuntimeError('Optimized Python refused')
R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr48_2961'
P=A/'concurrent_finalize_failure_analysis/rollback_READY_candidate_v1_history'
H=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
def need(ok,message):
    if not ok: raise RuntimeError(message)
def ref(p):
    need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Safe source reference')
    before=p.stat(); body=p.read_bytes(); after=p.stat()
    ident=lambda z:(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
    need(ident(before)==ident(after),'Stable source observation')
    return {'path':p.relative_to(R).as_posix(),'bytes':len(body),'sha256':sha(body),'full_mode':stat.S_IMODE(before.st_mode)},body
started=utc()
readyref,readybody=ref(P/'SOURCE_READY.json')
need(readyref['sha256']=='595d61469762348ee143d1ed4ac3792439cc8bcd70271dacc3e324361e45ed28','Exact received v1 SOURCE')
ready=json.loads(readybody)
need(ready['payload_count']==7 and {q.name for q in P.iterdir()}==set(ready['payload_names'])|{'HISTORY_QUALIFICATION.json'},'Exact seven-source archive plus declared history note')
historyref,historybody=ref(P/'HISTORY_QUALIFICATION.json')
source_refs=[]
for expected in ready['source_rows_except_READY']:
    actual,body=ref(P/Path(expected['path']).name)
    need({**actual,'path':expected['path']}==expected,'Archived received SOURCE member differs')
    source_refs.append(actual)
helperref,helperbody=ref(P/'rollback_partial.py')
tree=ast.parse(helperbody)
functions={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
need(set(functions)>={'main','entry','environment','fresh_outside_baseline','dirty_domain','replace','canonical','git'},'Expected read candidate structure')
need(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'No removable assertion gates')
planref,planbody=ref(P/'PLAN.json'); plan=json.loads(planbody)
foot=json.loads((H/'ACTUAL_FOOTPRINT.json').read_bytes())
normalize=lambda z:{'path':z['path'],'bytes':z['bytes'],'sha256':z['sha256'],'full_mode':z['worktree_mode']}
need(plan['partial11']==sorted([normalize(z) for z in foot['selected_current_footprint']],key=lambda z:z['path']),'Exact independent fixed11 agreement')
need(plan['inventory_original']['sha256']=='171061fc88b5ca06e200cc2cead9d11fe1e7435f8f98435907937bdc0f9df0d8','Exact restore inventory')
need(plan['original_merge_commit']=='209581a4627b01745974837fe7adab62ab8c0af7' and len(plan['unrelated_native12'])==12 and len(plan['foreign_rows'])==7 and len(plan['owned_logs'])==2,'Exact fixed original/restoration envelope')
need(plan['preparation_outside_observations_are_execution_prerequisites'] is False,'Historical versions are not execution preconditions')
reads=json.loads((P/'SOURCE_READS.json').read_bytes())
for c in reads['complete_readonly_commands']:
    for stream in ['stdout','stderr']:
        b=c['entire_'+stream+'_utf8'].encode()
        need(len(b)==c[stream+'_bytes'] and sha(b)==c[stream+'_sha256'],'Complete actual source command stream digest')
capdir=A/'concurrent_finalize_failure_analysis/source_binding_final_actual_capture'
capref,capbody=ref(capdir/'CAPTURE.json'); cap=json.loads(capbody)
need(cap['pid']==19744 and cap['exit_code']==0 and cap['production_rollback_executed'] is False,'Actual SOURCE author, not rollback')
for stream in ['stdout','stderr']:
    rr,bb=ref(capdir/cap[stream]['path'])
    need(len(bb)==cap[stream]['bytes'] and sha(bb)==cap[stream]['sha256'],'Actual author full stream authentication')
prelaunchref,prelaunchbody=ref(capdir/'PRELAUNCH_SOURCE.py')
need(prelaunchref['sha256']==cap['prelaunch_source']['sha256']==ready['source_rows_except_READY'][-2]['sha256'],'Actual author prelaunch exact source')
source_refs.append(readyref)
archive=H/'reviewed_v1'
archive.mkdir()
for name,body in [('rollback_partial.py',helperbody),('SOURCE_READY.json',readybody)]:
    with (archive/name).open('xb') as f:f.write(body)
findings=[{'id':'F1','severity':'mandatory_SOURCE_evidence_repair','mechanism':'main pre-quarantine failures occur before its try; COMMANDS is not persisted by entry failure envelope','affected_function':'entry'}, {'id':'F2','severity':'mandatory_SOURCE_evidence_repair','mechanism':'native-critical completed result stays in memory until final post-release receipt; release/final-publication failure loses its completed operation ledger','affected_function':'main/entry'}, {'id':'F1a','severity':'part_of_F1','mechanism':'strict byte decoding happens while constructing COMMANDS.append, before record insertion; non-UTF8 refusal can lose genuine raw streams/PID','affected_function':'git'}]
result={'schema':'pr48-independent-rollback-v1-read-AST-check/v1','actual_inspector_pid':os.getpid(),'started_utc':started,'finished_utc':utc(),'source_body_execution_or_import':False,'Git_or_native_commands_executed':False,'production_mutation_executed':False,'ROOT_approval_claimed':False,'new_math_credit':0,'received_v1_SOURCE':readyref,'received_v1_helper':helperref,'received_v1_plan':planref,'all_seven_source_rows':sorted(source_refs,key=lambda z:z['path']),'additional_archive_history_note':historyref,'fixed11_independent_agreement':True,'source_author':capref,'source_author_pid':19744,'authenticated_source_author_streams':True,'source_subcommand_records_authenticated':len(reads['complete_readonly_commands']),'unexecuted_reviewer_findings':findings,'status':'MANDATORY_EVIDENCE_REPAIR_BEFORE_CLEAN_SOURCE_VERDICT','source_custody_and_AST_checks_completed':True,'adversarial_runtime_controls_executed':False}
print(json.dumps(result,sort_keys=True,indent=2))
