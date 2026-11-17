"""One metadata-only v2 terminal seal. Reads/writes exclusively this owned lane.
Preserves original functions.exec sealing failure and every preexisting payload/source/stream.
No builder import/execution, subprocess, Git, network, source/native/public reads or mutation.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, os, re, stat
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mink-riesz-k3-stage-sol-20261117')
BASE=OWN/'baseline-public'; CAND=OWN/'candidate-public'
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(rows):
 d={}
 for k,v in rows:
  assert k not in d
  d[k]=v
 return d
def readj(name): return json.loads((OWN/name).read_bytes(),object_pairs_hook=pairs)
def pin(path):
 assert path.is_relative_to(OWN) and path.resolve().is_relative_to(OWN) and stat.S_ISREG(path.lstat().st_mode) and not path.is_symlink()
 b=path.read_bytes(); return {'bytes':len(b),'SHA256':sha(b),'mode':format(stat.S_IMODE(path.stat().st_mode),'04o')}
def checkpath(r,root=False):
 assert type(r) is str and r and '\x00' not in r and '\\' not in r
 if r=='.' and root: return
 assert not r.startswith('/') and all(x not in ('','.','..') for x in r.split('/')) and PurePosixPath(r).as_posix()==r
def validate(s):
 assert set(s)=={'root','files','directories','regular_files','child_directories'}
 assert type(s['root']) is str and Path(s['root']).is_absolute() and '.' in s['directories']
 fs,ds=s['files'],s['directories']; assert type(fs) is dict and type(ds) is dict and not set(fs)&set(ds)
 parents=set()
 for r,x in fs.items():
  checkpath(r); assert set(x)=={'bytes','SHA256','mode'} and type(x['bytes']) is int and x['bytes']>=0
  assert re.fullmatch('[0-9a-f]{64}',x['SHA256']) and re.fullmatch('0[0-7]{3}',x['mode'])
  parents.add(PurePosixPath(r).parent.as_posix())
 for r,x in ds.items():
  checkpath(r,True); assert set(x)=={'mode','empty'} and type(x['empty']) is bool and re.fullmatch('0[0-7]{3}',x['mode'])
  if r!='.': parents.add(PurePosixPath(r).parent.as_posix())
 assert parents<=set(ds) and all(x['empty']==(r not in parents) for r,x in ds.items())
 assert type(s['regular_files']) is int and s['regular_files']==len(fs)
 assert type(s['child_directories']) is int and s['child_directories']==len(ds)-1
def census(root):
 assert root.is_relative_to(OWN) and root.resolve().is_relative_to(OWN) and root.is_dir() and not root.is_symlink()
 fs,ds={},{}
 for base,dirs,files in os.walk(root,followlinks=False):
  base=Path(base); assert all(not (base/n).is_symlink() for n in dirs+files)
  ds[base.relative_to(root).as_posix()]={'mode':format(stat.S_IMODE(base.stat().st_mode),'04o'),'empty':not dirs and not files}
  for n in files: fs[(base/n).relative_to(root).as_posix()]=pin(base/n)
 s={'root':str(root),'files':fs,'directories':ds,'regular_files':len(fs),'child_directories':len(ds)-1}; validate(s); return s
def write(name,data):
 assert '/' not in name and name not in ('.','..')
 with (OWN/name).open('xb') as f: f.write(data)
def writej(name,data): write(name,(json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
def hidden(r): return r!='.' and any(x.startswith('.') for x in r.split('/'))
assert OWN.is_dir() and not OWN.is_symlink() and OWN.resolve()==OWN
assert not (OWN/'OWNED_MANIFEST.json').exists() and not (OWN/'FINAL.json').exists()
started=utc(); before=census(OWN)
writej('SEAL_V2_GUARDS_BEFORE.json',{'schema':'terminal-seal-v2-whole-preexisting-owned-custody-v1','snapshot':before})
try:
 original=readj('SEAL_ATTEMPT_V1.input-metadata.json'); assert original['schema']=='captured-first-terminal-seal-data-v1'
 prior=original['snapshot']; validate(prior); assert prior['regular_files']==1616 and prior['child_directories']==770 and prior['root']==str(OWN)
 assert all(before['files'][r]==x for r,x in prior['files'].items())
 assert before['directories']==prior['directories']
 assert pin(OWN/'build_private.py')=={'bytes':36119,'SHA256':'571d593b18f9d74584a18787f4b8da9118fcd1de8d71e500ca8a87a5745acc56','mode':'0644'}
 assert (OWN/'BUILD.stdout.txt').read_bytes()==(OWN/'BUILD.stderr.txt').read_bytes()==b''
 build=readj('BUILD_EXECUTION.json'); result=readj('BUILD_RESULT.json')
 assert build['exit_code']==0 and build['invocations']==1 and build['error'] is None and result['invocations']==1
 assert result['status']=='PRIVATE_STAGE_COMPLETE_AWAITING_ROOT_AND_INDEPENDENT_AUDIT' and result['counts']==[803,387,133,134]
 guards=readj('GUARDS_BEFORE.json'); assert (OWN/'GUARDS_BEFORE.json').read_bytes()==(OWN/'GUARDS_AFTER.json').read_bytes()
 assert pin(OWN/'GUARDS_BEFORE.json')=={'bytes':330664,'SHA256':'467c495655dbf942b21208679e02819f9504f1911bad565edd9f4fbee8c4a902','mode':'0644'}
 base,can=census(BASE),census(CAND); saved_base,saved_can=readj('BASELINE_MANIFEST.json'),readj('CANDIDATE_MANIFEST.json')
 for x in (saved_base,saved_can,guards['public']): validate(x)
 assert base==saved_base and can==saved_can
 assert base['files']==guards['public']['files'] and base['directories']==guards['public']['directories']
 target=readj('TARGETS.json'); adds=target['additions_public_relative']; mods=target['modifications_public_relative']; newdirs=target['new_directories_public_relative']
 assert len(adds)==len(set(adds))==13 and len(mods)==2 and set(mods)=={'research/index.html','research/sitemap.xml'} and len(newdirs)==6
 assert set(can['files'])-set(base['files'])==set(adds) and set(base['files'])<=set(can['files'])
 assert {r for r,x in base['files'].items() if can['files'][r]!=x}==set(mods)
 assert all(can['files'][r]['mode']==x['mode'] for r,x in base['files'].items())
 assert all(can['files'][r]==x for r,x in base['files'].items() if r not in mods)
 assert all(can['files'][r]['mode']=='0644' for r in adds)
 assert all(can['directories'][r]==x for r,x in base['directories'].items())
 assert set(can['directories'])-set(base['directories'])==set(newdirs)
 assert all(can['directories'][r]=={'mode':'0755','empty':False} for r in newdirs)
 assert (base['regular_files'],base['child_directories'],can['regular_files'],can['child_directories'])==(790,381,803,387)
 modes=dict(Counter(x['mode'] for x in base['files'].values())); assert modes=={'0644':764,'0600':24,'0666':2}
 assert readj('MODE_DIAGNOSIS.json')['baseline_per_copy_old_mode_counts']==modes
 assert (OWN/'SEAL_ATTEMPT_V1.stdout.txt').read_bytes()==b'' and b'Error: filepin' in (OWN/'SEAL_ATTEMPT_V1.stderr.txt').read_bytes()
 assert readj('SEAL_FAILURE.json')['builder_exit_remains']==0
 disposition=readj('ROOT_METADATA_DISPOSITION.json'); assert disposition['builder_or_payload_or_source_repair_authorized'] is False
 writej('SEAL_ATTEMPT_V1.execution.json',{'schema':'retained-first-terminal-seal-tool-failure-v1','mechanism':'functions.exec JavaScript orchestration','tool_result':'Script failed','mapped_failure_status':1,'native_process_exit_code':None,'code_recorded_after_failure':True,'source':pin(OWN/'SEAL_ATTEMPT_V1.js'),'stdout':pin(OWN/'SEAL_ATTEMPT_V1.stdout.txt'),'stderr':pin(OWN/'SEAL_ATTEMPT_V1.stderr.txt'),'terminal_created':False,'builder_or_payload_changed':False,'old_failure_remains_failure':True})
 writej('SEAL_V2_EXECUTION.json',{'schema':'single-passive-terminal-metadata-v2-receipt-v1','UTC_start':started,'data_checks_end_UTC':utc(),'invocations':1,'exit_code_at_normal_completion':0,'external_tool_exit_observation_required_at_handoff':True,'scope':'Owned data/mode validation and terminal seal only','old_builder_exit':0,'old_functions_seal_failure_status':1,'all_original_1616_files_and770dirs_exact':True,'baseline_mode_counts':modes,'only13newpayloads_require0644':True,'all_old_file_directory_modes_exact':True,'no_builder_execution_or_payload_repair':True})
 report='The fresh builder remains one successful exit0 with empty streams. Its original435line code, all1616pre-seal files and770directory modes/topology are unchanged. The first functions.exec administrative sealing attempt remains a literal failurestatus1 (no native process exitcode): Error:filepin, caused solely by demanding0644 for every copied old file. Actual authenticated baseline modes are764files0644,24files0600 and2files0666 per copy. These modes were correctly preserved; there is no payload defect. Original code/error/input metadata/diagnosis are retained.\n\nUnder explicit root metadata-only disposition, this distinct saved/full-read v2 sealer validates complete actual per-file modes, requires only13newpayloads0644, preserves all old file/dir modes, and reads/writes exclusively this owned lane. No builder rerun/import/help/AST/compile/source repair, no candidate/input/guard/oldresult overwrite, and no Git/network/W/science/publication action occurred. Literal history is builder0, firstmetadataseal1, separatepassivemetadata0 at normal completion, corroborated by external tool return.\n\nPrivate candidate803/387/133index/134XML and13A2M/15paths/6dirs remain exactly the successful build. Staging100%, follow_up null. Root reading and independent audit remain pending; no future action authority.\n'
 write('SEAL_V2_REPORT.md',report.encode())
finally:
 after=census(OWN)
 stable=all(after['files'].get(r)==x for r,x in before['files'].items()) and after['directories']==before['directories']
 allowed={'SEAL_V2_GUARDS_BEFORE.json','SEAL_ATTEMPT_V1.execution.json','SEAL_V2_EXECUTION.json','SEAL_V2_REPORT.md'}
 assert set(after['files'])-set(before['files'])<=allowed
 writej('SEAL_V2_GUARDS_AFTER.json',{'schema':'terminal-seal-v2-preexisting-owned-closing-custody-v1','protected_preexisting_snapshot':before,'unchanged':stable,'new_created_files_at_capture':sorted(set(after['files'])-set(before['files'])),'actual_after_snapshot':after})
 assert stable,'Actual preexisting payload/source/stream/result changed'
full=census(OWN)
assert all(x['mode']=='0644' for r,x in full['files'].items() if not r.startswith(('baseline-public/','candidate-public/')))
files=[dict(path=r,**x,hidden=hidden(r),empty=x['bytes']==0) for r,x in sorted(full['files'].items())]
dirs=[dict(path=r,**x,hidden=hidden(r)) for r,x in sorted(full['directories'].items())]
count=len(files)+2; now=utc()
manifest={'schema':'finite-mink-riesz-k3-private-stage-manifest-v1','UTC':now,'root':str(OWN),'root_mode':'0755','regular_files':count,'child_directories':770,'payload_files':files,'directories':dirs,'file_mode_counts':dict(Counter(x['mode'] for x in files)),'hidden_files':sum(x['hidden'] for x in files),'hidden_directories':sum(x['hidden'] for x in dirs),'empty_payload_files':[x['path'] for x in files if x['empty']],'empty_directories':[x['path'] for x in dirs if x['empty']],'symlinks':0,'special_objects':0,'exact_already_created_terminal_recursive_hash_exclusions':[str(OWN/'OWNED_MANIFEST.json'),str(OWN/'FINAL.json')],'terminal_modes':{'OWNED_MANIFEST.json':'0644','FINAL.json':'0644'},'other_exclusions':[],'all_hidden_ignored_empty_bytes_modes_topology_included':True,'no_future_subtree_or_basename_exclusions':True,'external_terminal_pins_required':True}
assert full['child_directories']==770 and full['directories']['.']['mode']=='0755'
writej('OWNED_MANIFEST.json',manifest)
top={r:x for r,x in full['files'].items() if '/' not in r}
final={'schema':'private-mink-riesz-k3-stage-FINAL-v1','UTC':now,'status':'PRIVATE_STAGE_FROZEN_AWAITING_ROOT_AND_INDEPENDENT_AUDIT','completion_percent_staging_only':100,'follow_up':None,'candidate_counts_files_childdirs_index_XML':[803,387,133,134],'baseline_counts':[790,381,130,131],'projection':'13A2M/15Gitpaths/6newdirs','targets':target,'source_files_childdirs':[133,34],'private_files_childdirs':[378,25],'accepted_BODY_MAIN_abstracts_Bibs_seven_assets_exact':True,'HEAD_spans':[8,7,7],'all_old130HTML_concat_visible_rawJSON_typed_and131raw_fullparsedXML_prefix_and_wholebuffer_reversal_exact':True,'untouched_old_files':788,'all381old_directory_modes_sharedCSS_and17DSStore_exact':True,'W_baseline_HEAD':'217d41c0a9344aed9caacee7aed31d4f23b77e47','W_baseline_tree':'cb7ae0adb22dc34b9c36b9d1e8efcf94f89f44e3','W_raw_index_SHA256':'25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7','M_native_main':'a4ce3c37dad209339e490d18dcced6c48cf912d2','M_native_index_SHA256':'91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11','build_source_private_root_native_public_guards':pin(OWN/'GUARDS_BEFORE.json'),'build_guards_byte_identical':True,'builder':pin(OWN/'build_private.py'),'builder_lines':435,'literal_history':{'builder_exit':0,'first_functions_seal_failure_status':1,'first_seal_native_process_exit_code':None,'separate_v2_passive_exit_at_normal_completion':0,'external_tool_exit_observation_required':True,'first_seal_failure_not_retroactively_passed':True,'no_builder_retry_repair_import_AST_compile_help':True},'metadata_v2_scope':'Owned data only; all original1616files/770dirs unchanged, exact inherited modes from authenticated baseline,13newpayloads0644 only','old_baseline_file_modes':modes,'all_original_payloads_sources_streams_and_results_unchanged':True,'own_regular_files':count,'own_child_directories':770,'directory_rows_including_root':len(dirs),'root_mode':'0755','payload_file_mode_counts':manifest['file_mode_counts'],'terminal_modes':manifest['terminal_modes'],'hidden_files':manifest['hidden_files'],'empty_files':manifest['empty_payload_files'],'manifest':pin(OWN/'OWNED_MANIFEST.json'),'artifacts':top,'W_Git_network_source_science_Sheet_deploy_redirect_or_outreach_mutation':False,'publication_or_futureaction_authority':False,'new_science_copy_render_live_actualUI_certificate':False,'AA':None,'actual_publication_date':None,'terminal_external_pins_required':True,'frozen':True}
writej('FINAL.json',final)
closed=census(OWN)
assert closed['regular_files']==count and closed['directories']==full['directories'] and set(closed['files'])==set(full['files'])|{'OWNED_MANIFEST.json','FINAL.json'}
assert all(closed['files'][r]==x for r,x in full['files'].items())
assert closed['files']['OWNED_MANIFEST.json']['mode']==closed['files']['FINAL.json']['mode']=='0644'
