from pathlib import Path
import ast,hashlib,json,stat,gzip,lzma,uuid,os,datetime
D=Path("/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/operations17_whole_review01");ROOT=REVIEW=D;DEST=D/'private/pair_fidelity17_normal';ARCHIVES=D/'private/case_archives_phase17';ORIGINAL_PATH_READ=Path.read_bytes;MEMORY_PATHS={};MEMORY_BODIES={};VIRTUAL_DIRECTORIES=set();VIRTUAL_LOSS_CASES={'literal_pair_title_pair_coalescence_create'}
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
source=(D/'ENGINE17.py').read_bytes();tree=ast.parse(source)
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in {'allocated','archive_completed'}]
need(len(functions)==3,'Expected stub and final archive declarations plus allocation')
for f in functions:
 exec(compile(ast.Module(body=[f],type_ignores=[]),str(D/'ENGINE17.py')+'[own available-physical-only recovery]','exec',dont_inherit=True,optimize=0),globals())
before=allocated();archive_completed()
p=ARCHIVES/'pair_fidelity17_normal__literal_pair_title_pair_coalescence_create.case.json.gz';idx=json.loads(gzip.decompress(p.read_bytes()))
need(idx['historical_virtual_scope_complete']is False and not idx['virtual_paths']and not idx['virtual_bodies'],'Original missing volatile data not marked exactly')
v={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ALL_AVAILABLE_PHYSICAL_BYTES_PRESERVED_ORIGINAL_VOLATILE_READONLY_VFS_LOST','cause':'First completed literal-pair create finding/cold check followed by free-reserve archive and emergency-VFS refusal; process exited. Numeric full parsed spy/rawSDK bytes/actor receipt/finding/cold result and every physical file survive. Original readonly VFS memory was not saved and is not reconstructed or represented as complete.','case':idx['case'],'recipe':{'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())},'physical_files':len(idx['files']),'physical_directories':len(idx['directories']),'partial_VFS_flag':True,'archive_before_allocated_bytes':before,'archive_after_allocated_bytes':allocated(),'frozen_actor_changed':False,'real_effects':0,'next':'Fresh separate complete repro worlds with numeric full spies and waiting evidence retention; never reinterpret this partial case as complete'}
(D/'private/PAIR_FIRST_ATTEMPT_VFS_LOSS_AND_PHYSICAL_RECOVERY.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps(v))
