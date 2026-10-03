"""Independent private predicate controls; production is read strictly as text."""
from pathlib import Path, PurePosixPath
import copy, ctypes, datetime as dt, hashlib, json, os, re, stat, sys
F=Path(__file__).resolve().parent
checks=0; rejected=[]
def check(v,label):
    global checks
    assert v,label; checks+=1
def canonical(name):
    if type(name) is not str or not name or '\\' in name or '\0' in name: return False
    p=PurePosixPath(name)
    return not p.is_absolute() and str(p)==name and not set(p.parts)&{'.','..','.git','__pycache__'}
def row_valid(r):
    return type(r) is dict and set(r)=={'path','bytes','sha256'} and canonical(r['path']) and type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) is not None
def closure_valid(rows,files):
    return type(rows) is list and all(row_valid(r) for r in rows) and len({r['path'] for r in rows})==len(rows) and set(files)=={r['path'] for r in rows}|{'MANIFEST.json'}
def typed_same(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)
def private_approval(o):
    return o.get('reading_completed') is True and type(o.get('root_flags')) is dict and len(o['root_flags'])==9 and all(v is True for v in o['root_flags'].values()) and type(o.get('original_substantive_attempts')) is int and o['original_substantive_attempts']==1 and type(o.get('new_substantive_attempts')) is int and o['new_substantive_attempts']==0 and type(o.get('audit_turns')) is int and o['audit_turns']==0
def rejected_case(name,fun,value):
    check(fun(value) is False,name); rejected.append(name)
def main():
    builder=(F/'prepare_current_packet.py').read_text(); operator=(F/'capture_root_builder_operation.py').read_text()
    check('pr45_9900007' in builder and 'pr45_9900007' in operator,'correct anchor')
    for literal in ['MERGE_BASE','mismatch tends to1/2','finite_checks_do_not_prove_universal_coupling_or_full_problem','root_pr45_current_build_',"'original_attempts': '1/5'",'validate_native()',"rename(os.fsencode(source), os.fsencode(destination), 4)","stat.S_IMODE(path.stat().st_mode) == 0o444"]:
        check(literal in builder,'source literal '+literal)
    for bad in ['c772dc5','KP-4.36','2912','29933','507','source_snapshot_v2','original_diff_v2','Original2/5']:
        check(bad not in builder,'no scientific template residue '+bad)
    check('PR45_ROOT_BUILDER_PRELAUNCH_v1' in operator and 'PR45_ROOT_OUTER_CAPTURE' in operator,'actual ROOT protocol')
    good={'path':'folder/member.json','bytes':0,'sha256':'a'*64}
    check(row_valid(good),'positive typed row')
    cases=[('absolute','/tmp/x'),('traversal','a/../b'),('dot','a/./b'),('backslash','a\\b'),('double-slash','a//b'),('nul','a\0b'),('git','a/.git/x'),('pycache','__pycache__/x')]
    for name,path in cases: rejected_case(name,row_valid,dict(good,path=path))
    rejected_case('boolean bytes',row_valid,dict(good,bytes=False))
    rejected_case('negative bytes',row_valid,dict(good,bytes=-1))
    rejected_case('bad SHA',row_valid,dict(good,sha256='A'*64))
    rejected_case('extra row key',row_valid,dict(good,extra=1))
    check(closure_valid([good],['folder/member.json','MANIFEST.json']),'positive exact topology')
    rejected_case('duplicate rows',lambda x:closure_valid(x,['folder/member.json','MANIFEST.json']),[good,good])
    rejected_case('extra member',lambda x:closure_valid([good],x),['folder/member.json','MANIFEST.json','extra'])
    check(not typed_same(1,True) and not typed_same(0,False) and not typed_same(None,{}),'typed equality distinguishes bool/int/null')
    draft=json.loads((F/'DRAFT_ROOT_READ_LEDGER.json').read_bytes())
    rejected_case('real false draft',private_approval,draft)
    toy=copy.deepcopy(draft); toy.update(reading_completed=True,root_flags={k:True for k in draft['root_flags']})
    check(private_approval(toy),'private in-memory true predicate fixture only')
    for name,mut in [('originalbool',{'original_substantive_attempts':True}),('newbool',{'new_substantive_attempts':False}),('auditbool',{'audit_turns':False}),('falseread',{'reading_completed':False})]:
        rejected_case(name,private_approval,dict(toy,**mut))
    check(json.loads((F/'DRAFT_ROOT_EVIDENCE_BINDINGS.json').read_bytes())['approved_by_root'] is False,'evidence draft false')
    check(json.loads((F/'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes())['files']==[],'fresh13 absent draft')
    check('ROOT_SCOPE_ACCEPTED_SYNCHRONOUS_OBSTRUCTION_ONLY' not in (F/'DRAFT_ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md').read_text(),'scope draft has no sentinel')
    modes=[mode for mode in range(0o10000) if mode==0o444]
    check(modes==[0o444],'4096 full-mode predicate rejects all special bits')
    D=F/'private_controls'; D.mkdir(); mode_results=[]
    for mode in [0o444,0o1444,0o2444,0o4444]:
        p=D/('mode_%05o'%mode); p.write_bytes(b'private mode fixture\n'); os.chmod(p,mode)
        observed=stat.S_IMODE(p.stat().st_mode); check(observed==mode,'actual mode retained')
        check((observed==0o444)==(mode==0o444),'actual full mode decision')
        mode_results.append({'path':p.relative_to(F).as_posix(),'requested':mode,'observed_at_control':observed,'accepted_full0444':observed==0o444})
    # Exercise actual exclusive rename in this private directory only.
    check(sys.platform=='darwin','macOS private exclusive rename')
    libc=ctypes.CDLL(None,use_errno=True); ren=libc.renamex_np; ren.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; ren.restype=ctypes.c_int
    src=D/'rename_source'; dest=D/'rename_existing'; src.mkdir(); dest.mkdir(); (src/'member').write_bytes(b'source'); (dest/'sentinel').write_bytes(b'preserve')
    errno=ren(os.fsencode(src),os.fsencode(dest),4); check(errno!=0 and src.is_dir() and (dest/'sentinel').read_bytes()==b'preserve','actual existing destination not replaced')
    absent=D/'rename_absent'; check(ren(os.fsencode(src),os.fsencode(absent),4)==0 and (absent/'member').read_bytes()==b'source','actual absent destination published privately')
    # Test that a nonsymlink predicate detects actual local symbolic links.
    link=D/'temporary_link'; link.symlink_to(absent/'member'); check(link.is_symlink(),'actual symlink detected'); link.unlink()
    for o,name in [(json.loads((F/'STATIC_INPUT_BINDINGS.json').read_bytes()),'fixed bindings')]:
        for r in [o['snapshot_manifest'],o['original_metadata']]+o['auxiliary']: check(row_valid(r),name+' row')
        for info in o['families'].values():
            for r in info['copied_members']+info['foreign_members']+[info['manifest']]: check(row_valid(r),'family individual row')
    result={'schema':'PR45_PRIVATE_SOURCE_CONTRACT_CONTROLS_v1','actual_pid':os.getpid(),'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'independent_predicate_assertions':checks,'malformed_predicate_cases_rejected':rejected,'all4096_full_modes_enumerated':True,
      'actual_dated_mode_observations':mode_results,'fixtures_will_be_frozen0444_after_observation':True,
      'actual_private_exclusive_rename_and_symlink_controls':True,'production_text_only':True,
      'production_import_compile_or_execution':False,'ROOT_approval':None,'current_freeze':False,
      'private_true_fixture_only_in_memory_never_saved_as_ROOT_approval':True}
    with (F/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').open('x') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
