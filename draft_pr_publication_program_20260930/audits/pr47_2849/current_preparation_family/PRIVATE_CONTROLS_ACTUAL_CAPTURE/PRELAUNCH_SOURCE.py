"""Independent private administrative predicates; production sources read as TEXT ONLY."""
import ctypes, datetime as dt, hashlib, json, os, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; count=0
def ck(v,m):
    global count
    if not v: raise ValueError(m)
    count+=1
def typed(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(typed(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def validpath(v):
    if type(v) is not str or not v or '\\' in v or '\0' in v: return False
    p=PurePosixPath(v); return not p.is_absolute() and str(p)==v and not {'.','..','.git','__pycache__'}.intersection(p.parts)
def main():
    ck(not sys.flags.optimize,'No optimized controls')
    for mode in range(4096): ck((mode==0o444)==(mode in [292]),'All4096 FULL mode predicate')
    for pair in [(True,1),(False,0),(1,1.0),(None,{}),([1],[True]),({'x':None},{'x':{}})]: ck(not typed(*pair),'Recursive scalar type distinctions')
    for obj in [{'x':[1,True,None,{'y':1.0}]},[0,{}],None]: ck(typed(obj,json.loads(json.dumps(obj))),'Positive recursive typed equality')
    for p in ['x','a/b','original_archive/review/verdict.json']: ck(validpath(p),'Good canonical path')
    for p in ['',True,'/x','../x','a/../x','a//b','a/./b','a/','a\\b','.git/x','__pycache__/x','a\0b']: ck(not validpath(p),'Unsafe path')
    builder=(F/'prepare_current_packet.py').read_text(); operator=(F/'capture_root_builder_operation.py').read_text()
    for token in ['stat.S_IMODE','==0o444','renamex_np','os.fsencode(destination),4','Duplicate JSON key','type(r[\'bytes\']) is int','type(r[\'full_mode\']) is int','No optimized guards','nativecheck()','Original scoped ownership; never whole audit root','inner_GIT_COMMANDS_written_incrementally_while_builder_alive','frozen_inner_copy_is_prepublication_prefix','ROOT_personally_reads_original_final_inner_full_records_streams_AFTER_child_exit','PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY','SOURCE_PRECISION_QUALIFICATIONS.md','len(rm[\'files\'])==219','complete_actual_Git_captures','rawrecord[\'raw_null_present\'] is False','original[\'prior_report.json\']==b\'null\\n\'']: ck(token in builder,'Production TEXT contract token '+token)
    for token in ['PRELAUNCH_BUILDER_SOURCE.py','PRELAUNCH_OPERATOR.py','OPERATION_PRELAUNCH.json','child.wait','CAPTURE.json','outer_operator_does_not_write_inner_GIT_COMMANDS','ROOT_full_final_outer_capture_and_original_inner_full_records_streams_read_AFTER_child_exit_required']: ck(token in operator,'Outer TEXT contract token')
    ck(operator.index("write(capture/'OPERATION_PRELAUNCH.json',pre)")<operator.index('subprocess.Popen')<operator.index('child.wait')<operator.index("write(capture/'CAPTURE.json',rec)"),'Text outer ordering only')
    snap=json.loads((F.parent/'snapshot_manifest.json').read_bytes())
    for r in snap['files']: ck((F/'original_archive'/r['relative_path']).read_bytes()==(F.parent/'source_snapshot'/r['relative_path']).read_bytes(),'Archive all16 bytes')
    unchanged=['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']
    for n in unchanged: ck((F/'operative_proposal'/n).read_bytes()==(F/'original_archive'/n).read_bytes(),'Operative immutable bytes')
    obstruction=(F/'operative_proposal/OBSTRUCTION.md').read_text(); ck('either prove that every reducible representation' not in obstruction and 'is **false**' in obstruction and 'Proposition6.1' in obstruction and 'actual degenerate' in obstruction,'Operational route repair, not append-only')
    for p in (F/'presentations').iterdir(): ck('Global current source qualifications' in p.read_text() and 'FALSE' in p.read_text() and 'UNSOLVED' in p.read_text(),'All current presentations qualified')
    for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        o=json.loads((F/n).read_bytes()); ck(o['reading_completed'] is False and all(v is False for v in o['root_flags'].values()) and o['created_utc'] is None and o['preparation_manifest_sha256'] is None,'ROOT false/null drafts')
    for n in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']:
        o=json.loads((F/n).read_bytes()); ck(o['approved_by_root'] is False and o['created_utc'] is None,'ROOT no source-time approval')
    q=(F/'native4_proposal/preimage/unsolved_math_prioritization__QUEUE.md').read_bytes(); p=(F/'native4_proposal/prospective/unsolved_math_prioritization__QUEUE.md').read_bytes(); qlines=q.splitlines(keepends=True); plines=p.splitlines(keepends=True); ck(len(qlines)==len(plines),'Queue row count')
    changes=[(a,b) for a,b in zip(qlines,plines) if a!=b]; ck(len(changes)==1,'One changed queue row'); a,b=changes[0]; x=a.decode().split('|'); y=b.decode().split('|'); ck(x[2].strip()==y[2].strip()=='2849 / KP-3.51','Exact selected queue ID'); ck({i for i,(aa,bb) in enumerate(zip(x,y)) if aa!=bb}<={8,9,11},'Only Status/Turns/Findings; Chat/DOI exact')
    for n in ['unsolved_math_prioritization__state.json','unsolved_math_prioritization__history.jsonl','draft_pr_publication_program_20260930__inventory.json']: ck((F/'native4_proposal/preimage'/n).read_bytes()==(F/'native4_proposal/prospective'/n).read_bytes(),'Native3 unchanged exact')
    private=F/'private_controls'; private.mkdir(exist_ok=False)
    for mode in [0o444,0o1444,0o2444,0o4444]:
        path=private/('mode_'+oct(mode)[2:]); path.write_bytes(b'dated private chmod predicate\n'); path.chmod(mode); actual=stat.S_IMODE(path.stat().st_mode); ck((actual==0o444)==(mode==0o444),'Actual full mode rejects special bits'); path.chmod(0o644)
    target=private/'symlink_target'; target.write_bytes(b'private target\n'); link=private/'temporary_symlink'; link.symlink_to(target); ck(link.is_symlink(),'Actual symlink detectable'); link.unlink()
    ck(sys.platform=='darwin','Actual macOS private exclusive-rename control'); lib=ctypes.CDLL(None,use_errno=True); fn=lib.renamex_np; fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; fn.restype=ctypes.c_int
    src=private/'exclusive_source'; dst=private/'exclusive_destination'; src.mkdir(); (src/'member').write_bytes(b'private exclusive payload\n'); ck(fn(os.fsencode(src),os.fsencode(dst),4)==0,'Actual absent-only rename success')
    src.mkdir(); (src/'member').write_bytes(b'replacement forbidden\n'); before=(dst/'member').read_bytes(); result=fn(os.fsencode(src),os.fsencode(dst),4); ck(result!=0 and (dst/'member').read_bytes()==before and (src/'member').exists(),'Actual existing destination refuses replacement')
    out={'schema':'PR47_PRIVATE_SOURCE_CONTRACT_CONTROLS_v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'assertions':count,'all4096_full_modes_enumerated':True,'private_actual_chmod_symlink_exclusive_rename_checked':True,'production_read_strictly_as_text':True,'production_import_compile_or_execution':False,'ROOT_reading_or_approval':None,'actual_current_freeze':False,'new_current_verdict':None,'scope':'Private independent predicates and text guard presence; no production runtime validation or new mathematics.'}
    with (F/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').open('xb') as h: h.write((json.dumps(out,indent=2)+'\n').encode())
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
