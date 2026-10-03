"""Independent private contract predicates. Production is read strictly as text."""
from pathlib import Path, PurePosixPath
import copy, ctypes, datetime as dt, hashlib, json, math, os, re, stat, sys
F=Path(__file__).absolute().parent
checks=0; rejected=[]
def check(value,label):
    global checks
    if not value: raise ValueError(label)
    checks+=1
def canonical(name):
    if type(name) is not str or not name or '\\' in name or '\0' in name: return False
    p=PurePosixPath(name)
    return not p.is_absolute() and str(p)==name and not set(p.parts)&{'.','..','.git','__pycache__'}
def row_valid(row):
    return type(row) is dict and set(row)=={'path','bytes','sha256'} and canonical(row['path']) and type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None
def closure_valid(rows,files,dirs):
    if type(rows) is not list or not all(row_valid(r) for r in rows) or len({r['path'] for r in rows})!=len(rows): return False
    if set(files)!={r['path'] for r in rows}|{'MANIFEST.json'} or 'MANIFEST.json' in {r['path'] for r in rows}: return False
    expected={p.as_posix() for n in files for p in PurePosixPath(n).parents if str(p)!='.'}
    return set(dirs)==expected
def typed_equal(a,b): return json.dumps(a,sort_keys=True,allow_nan=False,separators=(',',':'))==json.dumps(b,sort_keys=True,allow_nan=False,separators=(',',':'))
def private_approval(obj):
    return obj.get('reading_completed') is True and type(obj.get('root_flags')) is dict and len(obj['root_flags'])==9 and all(v is True for v in obj['root_flags'].values()) and all(type(obj.get(k)) is int and obj[k]==n for k,n in [('original_substantive_attempts',0),('original_source_verification_responses',1),('new_substantive_attempts',0),('audit_turns',0)])
def native_row_valid(row):
    return type(row) is dict and set(row)=={'path','bytes','sha256','full_mode'} and type(row['full_mode']) is int and 0<=row['full_mode']<0o10000 and row_valid({k:row[k] for k in ['path','bytes','sha256']})
def negative(label,predicate,value): check(predicate(value) is False,label); rejected.append(label)
def chronology_and_v2_anchor_controls(builder,operator):
    # These are textual source-contract checks, not execution of the production guards.
    function=builder.split('    def git(*argv):',1)[1].split('    prep_raw=',1)[0]
    check('        finally:' in function and "(attempt/'GIT_COMMANDS.json').write_bytes(encode(commands))" in function,'inner command writes are inside live builder git finally')
    check(function.index('        finally:')<function.index("(attempt/'GIT_COMMANDS.json').write_bytes")<function.index('        return regular'), 'incremental write precedes each git return')
    check("'final_inner_GIT_COMMANDS_written_only_after_builder_exit':True" not in builder,'V1 mistaken emitted chronology absent from operative builder')
    for literal in ["'final_inner_GIT_COMMANDS_written_incrementally_by_builder_before_exit':True",
      "'frozen_inner_command_copy_is_prepublication_prefix':True",
      "'outer_operator_does_not_write_inner_GIT_COMMANDS':True",
      "'ROOT_final_original_inner_commands_inspection_required_AFTER_child_exit':True"]:
        check(literal in builder,'truthful V2 emitted chronology '+literal)
    check('GIT_COMMANDS' not in operator,'outer operator does not write original inner command records')
    check(operator.index("record['exit_code'] = child.wait")<operator.index("(capture / 'CAPTURE.json').write_bytes"),'OUTER CAPTURE write follows actual child wait')
    check("family.name == 'current_preparation_family_v2'" in operator and "script.parent.name=='current_preparation_family_v2'" in builder,'both operative source anchors are V2')
    check("'PR46_ROOT_BUILDER_PRELAUNCH_v2'" in builder and "'PR46_ROOT_BUILDER_PRELAUNCH_v2'" in operator,'same V2 prelaunch schema')
    check('PR46_ROOT_ACTUAL_BUILDER_OPERATION_v2' in operator,'V2 outer completed-capture schema')
    check('root_pr46_current_v2_build_' in builder and 'root_pr46_current_v2_outer_' in builder and 'root_pr46_current_v2_outer_' in operator,'distinct V2 inner and outer prefixes')
    check("os.environ.get('PR46_ROOT_OUTER_CAPTURE','')" in builder and 'PR46_ROOT_OUTER_CAPTURE=capture.relative_to(audit).as_posix()' in operator,'operator supplies exact inherited parent outer reference')
    for literal in ["outer['operator_pid']==os.getppid()", "outer['builder_sha256']==sha(regular(script))",
      "outer['operator_sha256']==sha(regular(script.parent/'capture_root_builder_operation.py'))",
      "outer['argv']==['/usr/bin/python3','-B',str(script),*sys.argv[1:]]", "outer['cwd']==str(repo)"]:
        check(literal in builder,'inherited actual parent guard '+literal)
    check("clock(outer['started_utc'])<=dt.datetime.now" in builder,'actual prelaunch chronology boundary')
    for name in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json']:
        check(json.loads((F/name).read_bytes())['operative_preparation_directory']=='current_preparation_family_v2','honest V2 draft anchor '+name)
    expected={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
    expected.add('draft_pr_publication_program_20260930/inventory.json')
    native_rows=[{'path':n,'bytes':0,'sha256':'a'*64,'full_mode':0o644} for n in sorted(expected)]
    check(len(expected)==len(native_rows)==13 and all(native_row_valid(r) for r in native_rows),'private exact13 typed mode fixture')
    def private_exact13(payload):
        return type(payload) is list and len(payload)==13 and all(native_row_valid(r) for r in payload) and {r['path'] for r in payload}==expected
    check(private_exact13(native_rows),'private exact13 positive')
    negative('native13 missing row',private_exact13,native_rows[:-1])
    negative('native13 duplicate row',private_exact13,[native_rows[0]]+native_rows[:-1])
    for literal in ["raw_audit['selected_prior_key_present'] is False", "equal(raw_audit['selected_prior_fallback'],{})",
      "raw_audit['raw_null_present'] is False", "'state_history_inventory_prospective':'UNCHANGED_BYTE_EXACT'",
      "'QUEUE_named_changes':['Status','Turns','Findings']", "'PENDING_NATIVE_ACCEPTANCE_LOCAL_PROPOSAL_ONLY'",
      "require(not destination.exists() and not destination.is_symlink()", "publish_absent(stage,destination)"]:
        check(literal in builder,'unchanged absent-only/native proposal guard '+literal)
    for name in ['CURRENT_OVERVIEW.md','SOURCE_PRECISION_QUALIFICATIONS.md','EXECUTION_CONTRACT.md','REPAIR_DECISION.md']:
        text=(F/name).read_text()
        check('incrementally' in text and 'AFTER' in text and ('OUTER CAPTURE' in text or 'OUTER CAPTURE.json' in text),'global corrected chronology '+name)


def main():
    builder=(F/'prepare_current_packet.py').read_text(); operator=(F/'capture_root_builder_operation.py').read_text()
    check('pr46_30004438' in builder and 'pr46_30004438' in operator,'exact anchors')
    for marker in ['full ambient','ordinary real-open','root_pr46_current_build_',"'original_attempts':'0/5'",'source_verification_responses',"ledger=load(original['turns.json'])",'Plain raw original source object','validate_native()',"rename(os.fsencode(source), os.fsencode(destination), 4)","stat.S_IMODE(path.stat().st_mode)==0o444",'complete_outer_capture_written_only_after_child_exit','genuine_closed_ROOT_evidence_fixed_rows','native4_proposal/PROPOSAL_SCOPE.json']:
        check(marker in builder,'production source marker '+marker)
    for residue in ['pr45_9900007','turns.jsonl','synchronous-obstruction','ROOT_CURRENT_PARTIAL','original885','independent3044','probability_metric_family','literal_priority_family']:
        check(residue not in builder and residue not in operator,'no scientific template residue '+residue)
    check('PR46_ROOT_BUILDER_PRELAUNCH_v1' in operator and 'PR46_ROOT_OUTER_CAPTURE' in operator,'actual ROOT outer protocol')
    good={'path':'folder/member.json','bytes':0,'sha256':'a'*64}
    check(row_valid(good),'positive typed row')
    for name,path in [('absolute','/tmp/x'),('traversal','a/../b'),('dot','a/./b'),('backslash','a\\b'),('double-slash','a//b'),('nul','a\0b'),('git','a/.git/x'),('pycache','__pycache__/x'),('empty','')]: negative(name,row_valid,dict(good,path=path))
    for name,value in [('bool bytes',False),('negative bytes',-1),('float bytes',0.0)]: negative(name,row_valid,dict(good,bytes=value))
    negative('bad SHA',row_valid,dict(good,sha256='A'*64)); negative('extra row key',row_valid,dict(good,extra=1))
    check(closure_valid([good],['folder/member.json','MANIFEST.json'],['folder']),'positive exact closure')
    negative('duplicate rows',lambda x:closure_valid(x,['folder/member.json','MANIFEST.json'],['folder']),[good,good])
    negative('extra file',lambda x:closure_valid([good],x,['folder']),['folder/member.json','MANIFEST.json','extra'])
    negative('missing self',lambda x:closure_valid([good],x,['folder']),['folder/member.json'])
    negative('extra empty directory',lambda x:closure_valid([good],['folder/member.json','MANIFEST.json'],x),['folder','empty'])
    check(not typed_equal(0,False) and not typed_equal(1,True) and not typed_equal(None,{}) and not typed_equal([],{}) and not typed_equal({'a':0},{'a':False}),'recursive type-sensitive equality')
    draft=json.loads((F/'DRAFT_ROOT_READ_LEDGER.json').read_bytes()); negative('real ROOT draft',private_approval,draft)
    toy=copy.deepcopy(draft); toy.update(reading_completed=True,root_flags={k:True for k in draft['root_flags']})
    check(private_approval(toy),'private in-memory positive predicate toy only')
    for key in ['original_substantive_attempts','original_source_verification_responses','new_substantive_attempts','audit_turns']: negative('bool '+key,private_approval,dict(toy,**{key:bool(toy[key])}))
    negative('false reading',private_approval,dict(toy,reading_completed=False))
    flags=dict(toy['root_flags']); flags[next(iter(flags))]=False; negative('false flag',private_approval,dict(toy,root_flags=flags))
    check(json.loads((F/'DRAFT_ROOT_EVIDENCE_BINDINGS.json').read_bytes())['approved_by_root'] is False,'false evidence draft')
    check(json.loads((F/'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes())['files']==[],'absent fresh13 draft')
    check('ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY' not in (F/'DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md').read_text(),'no draft approval sentinel')
    native=dict(good,full_mode=0o644); check(native_row_valid(native),'positive full native mode row')
    negative('native bool mode',native_row_valid,dict(native,full_mode=True)); negative('native out-of-range mode',native_row_valid,dict(native,full_mode=0o10000))
    for mode in range(0o10000): check((mode==0o444)==(stat.S_IMODE(mode)==0o444),'complete4096 fullmode predicate')
    accepted=[m for m in range(0o10000) if m==0o444]; check(accepted==[0o444],'sole full0444')
    directory=F/'private_controls'; directory.mkdir(exist_ok=False); mode_observations=[]
    for mode in [0o444,0o1444,0o2444,0o4444]:
        p=directory/('mode_%05o'%mode); p.write_bytes(b'private mode fixture\n'); p.chmod(mode); observed=stat.S_IMODE(p.stat().st_mode)
        check(observed==mode,'actual chmod retains full mode'); check((observed==0o444)==(mode==0o444),'actual full-mode acceptance')
        mode_observations.append({'path':p.relative_to(F).as_posix(),'requested_full_mode':mode,'observed_at_control':observed,'accepted_full0444':observed==0o444})
    check(sys.platform=='darwin','macOS private exclusive rename control')
    libc=ctypes.CDLL(None,use_errno=True); rename=libc.renamex_np; rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
    source=directory/'rename_source'; existing=directory/'rename_existing'; source.mkdir(); existing.mkdir()
    (source/'member').write_bytes(b'source'); (existing/'sentinel').write_bytes(b'preserve')
    outcome=rename(os.fsencode(source),os.fsencode(existing),4)
    check(outcome!=0 and source.is_dir() and (existing/'sentinel').read_bytes()==b'preserve','existing destination preserved by actual exclusive rename')
    absent=directory/'rename_absent'; check(rename(os.fsencode(source),os.fsencode(absent),4)==0 and (absent/'member').read_bytes()==b'source','actual private absent destination publication')
    link=directory/'temporary_link'; link.symlink_to(absent/'member'); check(link.is_symlink(),'actual local symlink detected'); link.unlink()
    chronology_and_v2_anchor_controls(builder,operator)
    bindings=json.loads((F/'STATIC_INPUT_BINDINGS.json').read_bytes())
    for row in [bindings['snapshot_manifest'],bindings['original_metadata'],bindings['original_preparation_manifest']]+bindings['original_preparation_members']+bindings['original_separate_closure_capture']+bindings['genuine_closed_ROOT_evidence_fixed_rows']+bindings['superseded_v1_closed_source_rows']: check(row_valid(row),'fixed typed individual dependency')
    for info in bindings['families'].values():
        for row in [info['manifest']]+info['members']+info['separate_excluded_closure']: check(row_valid(row),'family typed individual dependency')
    result={'schema':'PR46_PRIVATE_SOURCE_CONTRACT_CONTROLS_v2','actual_pid':os.getpid(),
      'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'independent_predicate_assertions':checks,
      'malformed_predicate_cases_rejected':rejected,'all4096_full_modes_enumerated':True,
      'actual_dated_full_mode_observations':mode_observations,'fixtures_to_be_frozen0444_at_SOURCE_closure':True,
      'actual_private_exclusive_rename_and_symlink_controls':True,'production_text_only':True,'chronology_and_v2_inherited_parent_capture_controls':True,
      'production_import_compile_or_execution':False,'ROOT_approval':None,'actual_current_freeze':False,
      'private_true_fixture_only_in_memory_never_saved_as_ROOT_approval':True}
    with (F/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').open('x') as out: json.dump(result,out,indent=2,allow_nan=False); out.write('\n'); out.flush(); os.fsync(out.fileno())
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
