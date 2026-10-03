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
    bindings=json.loads((F/'STATIC_INPUT_BINDINGS.json').read_bytes())
    for row in [bindings['snapshot_manifest'],bindings['original_metadata'],bindings['original_preparation_manifest']]+bindings['original_preparation_members']+bindings['original_separate_closure_capture']+bindings['genuine_closed_ROOT_evidence_fixed_rows']: check(row_valid(row),'fixed typed individual dependency')
    for info in bindings['families'].values():
        for row in [info['manifest']]+info['members']+info['separate_excluded_closure']: check(row_valid(row),'family typed individual dependency')
    result={'schema':'PR46_PRIVATE_SOURCE_CONTRACT_CONTROLS_v1','actual_pid':os.getpid(),
      'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'independent_predicate_assertions':checks,
      'malformed_predicate_cases_rejected':rejected,'all4096_full_modes_enumerated':True,
      'actual_dated_full_mode_observations':mode_observations,'fixtures_to_be_frozen0444_at_SOURCE_closure':True,
      'actual_private_exclusive_rename_and_symlink_controls':True,'production_text_only':True,
      'production_import_compile_or_execution':False,'ROOT_approval':None,'actual_current_freeze':False,
      'private_true_fixture_only_in_memory_never_saved_as_ROOT_approval':True}
    with (F/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').open('x') as out: json.dump(result,out,indent=2,allow_nan=False); out.write('\n'); out.flush(); os.fsync(out.fileno())
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
