"""Own handwritten source-contract controls; proposed production is text-only input."""
from pathlib import Path, PurePosixPath
import argparse, ctypes, datetime, hashlib, json, os, re, stat, sys
F=Path(__file__).absolute().parent
A=F.parent
EXPECTED={
 'PREPARATION_MANIFEST.json':'be1217cc9c67dad1d5e528b547d332463e0b742dd1592602efe601b4c2d165a1',
 'prepare_current_packet.py':'7bde800ce050ddf1a9ac071ff54551813e87309eae9834805b3ef632b4342aff',
 'capture_root_builder_operation.py':'7f9c717bd3b8ef32160d4388f38ddaf3617c04c1e5c8c3884dd04725684acd3f'}
checks=[]
def ck(label,truth):
 if truth is not True: raise AssertionError(label)
 checks.append(label)
def digest(data): return hashlib.sha256(data).hexdigest()
def document(raw):
 def keys(pairs):
  out={}
  for key,value in pairs:
   if key in out: raise ValueError('duplicate key')
   out[key]=value
  return out
 def invalid(value): raise ValueError(value)
 return json.loads(raw,object_pairs_hook=keys,parse_constant=invalid)
def safe_name(name):
 if type(name) is not str or not name or '\x00' in name or '\\' in name: return False
 components=name.split('/')
 return not name.startswith('/') and all(x and x not in {'.','..','.git','__pycache__'} for x in components)
def valid_record(row):
 return type(row) is dict and set(row)=={'path','bytes','sha256'} and safe_name(row['path']) and type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None
def valid_records(records):
 return type(records) is list and all(valid_record(row) for row in records) and len({r['path'] for r in records})==len(records)
def typed_equal(left,right):
 return json.dumps(left,sort_keys=True,allow_nan=False,separators=(',',':'))==json.dumps(right,sort_keys=True,allow_nan=False,separators=(',',':'))
def physical_files(directory):
 if directory.is_symlink() or not directory.is_dir() or any(p.is_symlink() for p in directory.parents): raise ValueError('directory chain')
 files=set();dirs=set()
 for member in directory.rglob('*'):
  if member.is_symlink(): raise ValueError('symlink')
  name=member.relative_to(directory).as_posix()
  if not safe_name(name): raise ValueError('member path')
  mode=member.stat().st_mode
  if stat.S_ISREG(mode): files.add(name)
  elif stat.S_ISDIR(mode): dirs.add(name)
  else: raise ValueError('special member')
 needed=set()
 for name in files:
  components=name.split('/')
  needed.update('/'.join(components[:i]) for i in range(1,len(components)))
 if dirs!=needed: raise ValueError('extra or empty directory')
 return files

def rejects(call):
 try: call()
 except (ValueError,FileNotFoundError): return True
 return False

def inspect_inputs():
 prep=A/'current_preparation_family'; observed=[]
 for name,wanted in EXPECTED.items(): ck('exact source pin '+name,digest((prep/name).read_bytes())==wanted)
 manifest=document((prep/'PREPARATION_MANIFEST.json').read_bytes())
 ck('preparation47+self',manifest['files_count']==47 and len(manifest['files'])==47 and physical_files(prep)=={r['path'] for r in manifest['files']}|{'PREPARATION_MANIFEST.json'})
 ck('preparation13581B',(prep/'PREPARATION_MANIFEST.json').stat().st_size==13581)
 ck('typed preparation rows',valid_records(manifest['files']))
 def inspect(base,row,role):
  body=(base/row['path']).read_bytes()
  ck('input byte/hash '+role+' '+row['path'],len(body)==row['bytes'] and digest(body)==row['sha256'])
  ck('input full0444 '+role+' '+row['path'],stat.S_IMODE((base/row['path']).stat().st_mode)==0o444)
  if (base/row['path']).is_symlink() or any(p.is_symlink() for p in (base/row['path']).parents): raise ValueError('input symlink')
  if row['path'].endswith('.json'): document(body)
  elif row['path'].endswith('.jsonl'):
   for line in body.splitlines(): document(line)
  observed.append(dict(row,role=role))
  return body
 for row in manifest['files']: inspect(prep,row,'source-preparation')
 ck('manifest full0444',stat.S_IMODE((prep/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444)
 pins=document((prep/'STATIC_INPUT_BINDINGS.json').read_bytes())
 for row in [pins['snapshot_manifest'],pins['original_metadata']]+pins['auxiliary']: inspect(A,row,'original-preparation')
 snap=document((A/'snapshot_manifest.json').read_bytes())
 ck('original18 correct identity',snap['head']=='d9b4acf5d070d1f04ffac86a4f08916a5629ff16' and snap['github_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0' and snap['merge_base']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737' and snap['github_base']!=snap['merge_base'])
 ck('original18 topology',physical_files(A/'source_snapshot')=={r['relative_path'] for r in snap['files']} and len(snap['files'])==18)
 original={}
 for row in snap['files']:
  original[row['relative_path']]=inspect(A/'source_snapshot',{'path':row['relative_path'],'bytes':row['bytes'],'sha256':row['sha256']},'original18')
 ck('author helper duplicate exact',original['verify_binary_process.py']==original['review/verify_binary_process.py'])
 ck('author results duplicate exact',original['binary_verification.json']==original['review/submitted_results.json'])
 ck('proof duplicate exact',original['PARTIAL.md']==original['review/PARTIAL.md'])
 author=document(original['binary_verification.json']); independent=document(original['review/independent_results.json'])
 ck('whole historical885',type(author['exact_assertions']) is int and author['exact_assertions']==885 and len(author['window_receipts'])==42)
 ck('whole historical3044',type(independent['passed']) is int and independent['passed']==3044 and type(independent['failed']) is int and independent['failed']==0 and len(independent['checks'])==3044 and all(v=='PASS' for v in independent['checks'].values()))
 ck('whole original ledger',len(original['turns.jsonl'].splitlines())==1 and document(original['turns.jsonl'])['turn']==1)
 group_counts={}
 for key in independent['checks']:
  group=key.rsplit('_',1)[0]
  if key.startswith('conditional_'): group='conditional'
  elif key.startswith('max_finite_history_correlation_'): group='max_finite_history_correlation'
  elif key.startswith('anticipative_'): group=key.split('_')[1]
  elif key.startswith('window_'):group='window_TV'
  elif key.startswith('no_flip_'):group='no_flip_window'
  elif key.startswith('metric_'):group='metric'
  elif key.startswith('offset_'):group='offset'
  group_counts[group]=group_counts.get(group,0)+1
 family_totals={};foreign=[]
 for family,info in pins['families'].items():
  own={r['path'] for r in info['copied_members']};bad={r['path'] for r in info['foreign_members']}
  ck('family partition '+family,not own&bad and physical_files(A/family)==own|bad|{info['manifest']['path']})
  inspect(A/family,info['manifest'],'family-manifest')
  for row in info['copied_members']: inspect(A/family,row,'authored-family')
  for row in info['foreign_members']:
   inspect(A/family,row,'foreign-hash-only');foreign.append(dict(row,path=family+'/'+row['path']))
  ck('family directory modes '+family,all(stat.S_IMODE((A/family/name).stat().st_mode)==mode for name,mode in info['directory_modes'].items()))
  family_totals[family]={'copied_including_manifest':len(own)+1,'foreign_individually_bound':len(bad)}
 ck('foreign64 exactly',len(foreign)==64)
 ck('both exact family counts',family_totals=={'literal_priority_family':{'copied_including_manifest':50,'foreign_individually_bound':64},'probability_metric_family':{'copied_including_manifest':17,'foreign_individually_bound':0}})
 # The foreign bodies above are read in place for hashing. They are never emitted or copied.
 capture=A/'current_preparation_closure_actual_capture';cap=document((capture/'CAPTURE.json').read_bytes())
 ck('final closure capture exact pin',digest((capture/'CAPTURE.json').read_bytes())=='f5a6df56392e64600f67839f1f33834de3f991823c0b7376c80c02879cf33782')
 ck('five final closure members',physical_files(capture)=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'})
 ck('genuine final closure child',cap['operator_pid']==76170 and cap['pid']==76179 and cap['exit_code']==0 and cap['actual_execution'] is True and cap['completed'] is True)
 for channel in ['stdout','stderr']:
  row=cap[channel];body=(capture/row['path']).read_bytes();ck('finalclosure stream '+channel,len(body)==row['bytes'] and digest(body)==row['sha256'])
 ck('finalclosure sources',(capture/'PRELAUNCH_SOURCE.py').read_bytes()==(prep/'close_source_preparation.py').read_bytes() and (capture/'PRELAUNCH_OPERATOR.py').read_bytes()==(prep/'capture_source_closure.py').read_bytes())
 for name in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
  draft=document((prep/name).read_bytes());ck('real draft false '+name,draft['reading_completed'] is False and draft['created_utc'] is None and all(v is False for v in draft['root_flags'].values()))
 ck('no sentinel in draft','ROOT_SCOPE_ACCEPTED_SYNCHRONOUS_OBSTRUCTION_ONLY' not in (prep/'DRAFT_ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md').read_text())
 for name in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json']:
  draft=document((prep/name).read_bytes());ck('real approval draft false '+name,draft['approved_by_root'] is False and draft['created_utc'] is None)
 names=['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json','root_original_actual_reproduction','reviewed_candidate']
 existence={name:(A/name).exists() for name in names}
 builder=(prep/'prepare_current_packet.py').read_text();operator=(prep/'capture_root_builder_operation.py').read_text()
 ck('nine exact source flags',len(document((prep/'DRAFT_ROOT_READ_LEDGER.json').read_bytes())['root_flags'])==9 and 'new_source_adversary_closed_clean_complete_report_personally_read' in builder)
 ck('no production administrative mutator source',all(x not in builder+operator for x in ['git push','git commit','git add','requests.post(','urllib.request.urlopen(']))
 ck('honest final receipt gap',"'future_complete_outer_capture_or_whole_PASS_certified_by_freeze': False" in builder and "'current_inner_GIT_COMMANDS_record_is_final_only_after_builder_exit': True" in builder)
 return {'inputs_read_in_full_for_hash_and_structure':observed,'foreign_body_contents_never_copied':True,'individual_foreign_hash_bindings':foreign,'historical_receipt_groups':group_counts,'family_counts':family_totals,'actual_ROOT_paths_existence_at_read':existence,'all_inputs_source_only':True}

def contract_controls(mutant):
 # Own oracle; only the affected narrow source predicate is transcribed into a logical witness.
 good={'path':'one/two.json','bytes':2,'sha256':'a'*64}
 ck('positive row',valid_record(good))
 for name in ['/x','a/../x','a/./x','a//x','a/x/','a\\x','a\x00x','.git/x','__pycache__/x','']:
  validator=(lambda x:True) if mutant=='path' else safe_name
  ck('reject path '+repr(name),validator(name) is False)
 for value in [False,True,-1,2.0,'2',None]:
  validator=(lambda row:True) if mutant=='types' else valid_record
  ck('reject bytes '+repr(value),validator(dict(good,bytes=value)) is False)
 ck('duplicate rows rejected',valid_records([good,dict(good)]) is False)
 ck('extra row key rejected',valid_record(dict(good,x=1)) is False)
 for left,right in [(1,True),(0,False),(None,{}),([],{}),(1,1.0)]: ck('scalar conservation '+repr((left,right)),typed_equal(left,right) is False)
 ck('duplicates JSON rejected',rejects(lambda:document('{"a":1,"a":2}')))
 ck('nonfinite JSON rejected',rejects(lambda:document('{"a":NaN}')))
 accepted=[mode for mode in range(4096) if ((mode&0o777)==0o444 if mutant=='modes' else mode==0o444)]
 ck('all4096 full modes only0444',accepted==[0o444])
 # All toy approvals remain only in RAM; these are not genuine ROOT prerequisites.
 draft=document((A/'current_preparation_family/DRAFT_ROOT_READ_LEDGER.json').read_bytes())
 approval=lambda obj:obj['reading_completed'] is True and all(v is True for v in obj['root_flags'].values()) and obj['created_utc'] is not None
 ck('false approval is rejected',approval(draft) is False)
 ck('missing genuine prerequisite path fails closed',rejects(lambda:(F/'private_controls/no_genuine_ROOT_input.json').read_bytes()))
 # Source-local duplicate witness. This proves acceptance by that narrow guard, not by production build.
 row={'path':'root_original_actual_reproduction/helper/CAPTURE.json','bytes':1,'sha256':'a'*64}
 narrow=lambda refs:type(refs) is list and len(refs)==2
 strengthened=lambda refs:narrow(refs) and valid_records(refs)
 ck('source duplicate-list guard accepts local witness',narrow([row,dict(row)]) is True)
 choose=narrow if mutant=='duplicate_capture' else strengthened
 ck('stronger duplicate-reference rejection',choose([row,dict(row)]) is False)
 # Whole queue byte conservation with a deliberate special Chat/DOI and mixed line endings.
 header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
 before=b'preamble\r\n| '+b' | '.join(x.encode() for x in header)+b' |\r\n| 7 | 9900007 / AMR-098-0007 | Q | .2 | 5 | 3 | unknown | queued | 0/5 | literal chat | original finding | doi:X |\r\ntrailer\n'
 lines=before.splitlines(keepends=True);selected=lines[2];parts=selected.decode().split('|');changed=list(parts)
 for k,v in [(8,' unsolved '),(9,' 1/5 '),(11,' scoped pending finding ')]:changed[k]=v
 if mutant=='queue':changed[10]=' lost chat '
 after=b''.join('|'.join(changed).encode() if line==selected else line for line in lines)
 ck('queue other whole lines conserved',after.splitlines(keepends=True)[:2]==lines[:2] and after.splitlines(keepends=True)[3:]==lines[3:])
 ck('queue all unapproved fields byte conserved',all(parts[k]==changed[k] for k in range(len(parts)) if k not in {8,9,11}))
 ck('queue Chat DOI conserved',parts[10]==changed[10] and parts[12]==changed[12])
 d=F/'private_controls';d.mkdir(exist_ok=True)
 topology=d/'topology';topology.mkdir(exist_ok=False);(topology/'member').write_bytes(b'own')
 ck('physical positive topology',physical_files(topology)=={'member'})
 (topology/'empty').mkdir();ck('emptydir physically rejected',rejects(lambda:physical_files(topology)));(topology/'empty').rmdir()
 (topology/'link').symlink_to(topology/'member');ck('symlink physically rejected',rejects(lambda:physical_files(topology)));(topology/'link').unlink()
 mode_observations=[]
 for mode in [0o444,0o1444,0o2444,0o4444]:
  path=d/('mode_%04o'%mode);path.write_bytes(b'own mode fixture\n');path.chmod(mode);observed=stat.S_IMODE(path.stat().st_mode)
  ck('actual full mode '+oct(mode),observed==mode);mode_observations.append({'path':path.relative_to(F).as_posix(),'observed_at_run':observed,'accepted':observed==0o444})
 ck('actual macOS rename API',sys.platform=='darwin')
 libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
 source=d/'source';source.mkdir();(source/'member').write_bytes(b'source preserved')
 target=d/'exists';target.mkdir();(target/'sentinel').write_bytes(b'destination conserved')
 result=rename(os.fsencode(source),os.fsencode(target),4)
 ck('actual publication refuses nonempty destination',result!=0 and source.exists() and (target/'sentinel').read_bytes()==b'destination conserved')
 target_empty=d/'existing_empty';target_empty.mkdir();original_inode=target_empty.stat().st_ino
 result=rename(os.fsencode(source),os.fsencode(target_empty),0 if mutant=='publication' else 4)
 ck('actual publication refuses empty existing destination',result!=0 and source.exists() and target_empty.stat().st_ino==original_inode)
 (target_empty/'OBSERVATION.txt').write_text('Originally empty existing directory remained the same inode under exclusive rename4.\n')
 empty=d/'absent';ck('actual private absent publication',rename(os.fsencode(source),os.fsencode(empty),4)==0 and (empty/'member').read_bytes()==b'source preserved')
 return {'all4096_permission_values_checked':True,'physical_symlink_and_empty_directory_checks':True,'actual_private_rename4_only':True,'dated_private_mode_observations':mode_observations,'toys_RAM_only':True,'duplicate_source_guard_witness_only':True}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--mutant',default='none',choices=['none','types','path','modes','queue','duplicate_capture','publication']);args=parser.parse_args()
 # Each child has an isolated private test directory when invoked as a mutant.
 if args.mutant!='none':
  # The tests that fail early never create shared fixtures. Publication uses own separate folder.
  if args.mutant=='publication':
   global F
   F=F/'publication_mutant_private';F.mkdir(exist_ok=False)
 details=contract_controls(args.mutant)
 inspection=inspect_inputs() if args.mutant=='none' else None
 result={'schema':'PR45_NEW_SOURCE_ADVERSARY_OWN_CONTROLS_v1','status':'PASS_INDEPENDENT_SOURCE_CONTRACT_CONTROLS_ONLY','child_pid':os.getpid(),'argv':sys.argv,'cwd':str(Path.cwd()),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':len(checks),'assertion_labels':checks,'controls':details,'input_inspection':inspection,'production_import_compile_or_execution':False,'ROOT_approval':None,'future_runtime_PASS':False,'new_mathematical_discovery':0}
 print(json.dumps(result,indent=2,allow_nan=False))
if __name__=='__main__':main()
