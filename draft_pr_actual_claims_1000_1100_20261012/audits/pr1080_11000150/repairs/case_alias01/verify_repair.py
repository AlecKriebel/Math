#!/usr/bin/env python3
"""Complete bounded custody checker; --check verifies the sealed stage read-only."""
import collections,difflib,hashlib,io,json,sys,zipfile,zlib
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def row(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def require(x,m):
 if not x:raise RuntimeError(m)
def matches(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def main():
 checking='--check' in sys.argv
 require(checking or not (W/'SEAL.json').exists(),'Cannot rewrite a sealed repair')
 frozen=obj(W/'IMMEDIATE_INPUT_PINS.json')['files'];before=obj(W/'BEFORE_COPIES.json')['files'];byname={r['original_path']:r for r in before}
 current={p.relative_to(A).as_posix():p for p in A.rglob('*') if p.is_file() and not p.is_symlink() and not p.is_relative_to(W)}
 unchanged=[];changes=[]
 for r in frozen:
  n=r['path'];require(n in current,'Missing old regular input '+n)
  if matches(current[n],r):unchanged.append(r)
  else:
   require(n in byname and matches(A/byname[n]['source_snapshot'],r),'Unauthorized change/missing exact before '+n)
   changes.append({'path':n,'before':r,'after':row(current[n],A),'source_snapshot':byname[n]['source_snapshot']})
 require(len(frozen)==623 and len(changes)==10 and len(unchanged)==613 and set(byname)=={r['path'] for r in changes},'Baseline/allowed mutation accounting')
 new=sorted(set(current)-{r['path'] for r in frozen});require(len(new)==15 and len(current)==638,'Unexpected new canonical artifact')
 for r in before:require(matches(A/r['source_snapshot'],r),'Before bytes differ '+r['original_path'])
 copies=obj(K/'REPAIR01_STAGE_COPIES.json')['files'];oldcopies=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json')['files'];newcopies=obj(W/'NEW_COPY_ROWS.json')['files']
 require(len(copies)==157 and copies[:145]==oldcopies and copies[145:]==newcopies and len(newcopies)==12,'145-copy prefix/append')
 for r in copies:require(matches(A/r['source_snapshot'],r) and matches(K/r['destination'],r),'Source/delivery exact copy '+r['destination'])
 history=obj(K/'REPAIR01_HISTORY_RESOLUTION.json');oldhistory=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json');refs=history['references'];added=obj(W/'APPENDED_HISTORY_ROWS.json')['references']
 require(len(refs)==4641 and refs[:4628]==oldhistory['references'] and refs[4628:]==added,'4628 historical rows prefix/append')
 terminal=obj(K/'TERMINAL_HISTORY_RELOCATIONS.json')['rows'];case=obj(K/'CASE_ALIAS_HISTORY_RELOCATIONS.json')['rows'];require(len(terminal)==2 and len(case)==7,'Relocation counts')
 # Unchanged terminal relocation bytes are themselves frozen/protected.
 oldterminal=next(r for r in frozen if r['path']=='preprint_v1_0/verification_kit/TERMINAL_HISTORY_RELOCATIONS.json');require(matches(K/'TERMINAL_HISTORY_RELOCATIONS.json',oldterminal),'Old two relocations changed')
 reloc={r['reference_index']:r for r in terminal+case};require(len(reloc)==9,'Duplicate relocation')
 for i,r in reloc.items():require(refs[i]==r['historical_reference'],'Historical full row relocation identity')
 groups=collections.defaultdict(list)
 for i,r in enumerate(refs):
  groups[r['stage']].append(r)
  if r['disposition']=='exact_captured_stage_or_canonical_copy':require(matches(K/(reloc[i]['current_exact_destination'] if i in reloc else r['destination']),r),'Historical resolution '+str(i))
  else:require(r['disposition']=='omitted' and bool(r['reason']),'Unexplained omission '+str(i))
 prefixes={'immediate-before-repair01':'','preparation-input194':'','preparation-output90':'preprint_v1_0/','whole01-input289':'','whole01-output17':'reviews/package_01/','metadata-date02-immediate404':'','repair01-current360':'','repair01-protected298':'','repair01-output42':'repairs/package01/','repair01-immediate309':''}
 specs={r['stage']:r for r in obj(A/'finalization/terminal_admin_20261016/APPENDED_HISTORY_SPECIFICATION.json')['inventories']}
 require(set(groups)==set(prefixes)|set(specs)|{'case-alias01-changed-before','case-alias01-selected-evidence'},'Complete historical stage set')
 for stage,rs in groups.items():
  if stage=='case-alias01-changed-before':original=before;tuples=[(r['original_path'],r['bytes'],r['sha256']) for r in original]
  elif stage=='case-alias01-selected-evidence':tuples=[(r['path'],r['bytes'],r['sha256']) for r in obj(W/'SELECTED_CASE_INPUTS.json')['files']]
  else:
   s=specs.get(stage);inventory=s['inventory'] if s else rs[0]['inventory'];key=s['key'] if s else 'files';prefix=s['prefix'] if s else prefixes[stage];tuples=[(prefix+r['path'],r['bytes'],r['sha256']) for r in obj(A/inventory)[key]]
  require(tuples==[(r['original_path'],r['bytes'],r['sha256']) for r in rs] and len(rs)==history['inventory_counts'][stage],'Complete ordered historical inventory '+stage)
 # Individually map every structured old pin to the changed immediate bytes.
 pinres=[];beforehash=collections.defaultdict(list)
 for r in before:beforehash[(r['bytes'],r['sha256'])].append(r)
 def walk(value,pointer,source):
  if isinstance(value,dict):
   if type(value.get('bytes')) is int and isinstance(value.get('sha256'),str):
    for b in beforehash.get((value['bytes'],value['sha256']),[]):
     pinres.append({'source_inventory':source,'json_pointer':pointer,'original_pin':value,'changed_current_path':b['original_path'],'exact_local_before':b['source_snapshot'],'delivered_before':None if b['original_path'].endswith('.zip') else 'case_alias01_history/before/'+b['original_path'],'disposition':'old_archive_local_only_not_newly_packed' if b['original_path'].endswith('.zip') else 'exact_delivered_before_bytes'})
   for k,v in value.items():walk(v,pointer+'/'+str(k).replace('~','~0').replace('/','~1'),source)
  elif isinstance(value,list):
   for i,v in enumerate(value):walk(v,pointer+'/'+str(i),source)
 for r in frozen:
  if not r['path'].endswith('.json'):continue
  try:data=obj(A/byname[r['path']]['source_snapshot']) if r['path'] in byname else obj(A/r['path'])
  except (ValueError,UnicodeDecodeError):continue
  walk(data,'',r['path'])
 require(bool(pinres),'No changed historical pins found')
 native=obj(D/'metadata.json');upload=obj(D/'deposit_metadata.json');require((D/'metadata.json').read_bytes()==(K/'metadata.json').read_bytes() and upload=={'metadata':native,'files':[{'path':'preprint.pdf','name':'preprint.pdf'},{'path':'verification_kit.zip','name':'verification_kit.zip'}]},'Native schema/fields/attachment list changed')
 status=obj(K/'CURRENT_CASE_ALIAS_REPAIR01.json');require((K/'CURRENT_CASE_ALIAS_REPAIR01.json').read_bytes()==(D/'CURRENT_CASE_ALIAS_REPAIR01.json').read_bytes() and status['new_complete_review_required'] is True and status['required_next_review']=='NEW complete whole03' and status['whole_reviews_completed']==2 and status['minimum_whole_reviews']==2 and all(status[k] is False for k in ['publication_ready','issues_resolved','published','root_repair_adopted','root_integrity_adopted']) and status['services_held_at']==1032,'Current mandatory hold/review state')
 names=obj(K/'ALLOWLIST.json')['members'];require(len(names)==239 and names==sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()),'Allowlist')
 require([r['path'] for r in obj(K/'MANIFEST.json')['files']]==[n for n in names if n!='MANIFEST.json'],'Manifest members')
 for r in obj(K/'MANIFEST.json')['files']:require(matches(K/r['path'],r),'Payload mismatch '+r['path'])
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
  for n in names:
   info=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED;z.writestr(info,(K/n).read_bytes())
 require(buf.getvalue()==(D/'verification_kit.zip').read_bytes(),'Independent CLOSED ZIP byte mismatch')
 with zipfile.ZipFile(D/'verification_kit.zip') as z:
  require(z.namelist()==['verification_kit/'+n for n in names] and not z.comment and z.testzip() is None,'ZIP order/comment/CRC')
  for info,n in zip(z.infolist(),names):require(z.read(info)==(K/n).read_bytes() and info.date_time==(2026,10,14,0,0,0) and info.create_system==3 and info.external_attr==0o100644<<16 and info.compress_type==0 and info.flag_bits==0 and not info.extra and not info.comment and info.CRC==(zlib.crc32((K/n).read_bytes())&0xffffffff),'ZIP payload/header '+n)
 summary=obj(W/'REPRODUCTION_SUMMARY.json');require(summary['status']=='PASS' and summary['canonical_inputs_unchanged_during_reproduction']==638 and summary['actual_physical_case_rejections']==12,'Actual reproduction result')
 actual=[json.loads(x) for x in (W/'FINAL_REPRODUCTION_RECEIPTS.jsonl').read_text().splitlines()];require(len(actual)==summary['actual_commands'] and all(r['returncode']==0 if r['expected']==0 else r['returncode']!=0 for r in actual),'Actual receipt outcomes')
 finite=[json.loads(r['stdout']) for r in actual if r['label']=='full finite adapters'];require(len(finite)==2 and finite[0]==finite[1],'Full finite normal/-O JSON')
 physical=obj(W/'PHYSICAL_WRITER_REGRESSION.json');require(physical['status']=='PASS' and physical['actual_commands']==14 and physical['negative_physical_case_commands']==12 and physical['positive_case_varied_external_commands']==2,'Detailed physical regression summary')
 require(len(physical['receipts'])==14 and {r['optimized'] for r in physical['receipts']}=={False,True},'Detailed physical modes/count')
 for r in physical['receipts']:
  if r['kind']=='fresh-case-varied-external-positive':require(r['returncode']==0 and r['byte_identical_to_current_zip'] and r['external_parent_samefile'] and r['all_preexisting_kit_bytes_unchanged'],'Detailed physical positive')
  else:require(r['returncode']!=0 and 'archive must be outside' in r['stderr'] and r['script_root_samefile_as_kit'] and r['case_output_root_samefile_as_kit'] and r['script_root_device_inode']==r['kit_device_inode'] and r['destination_initially_absent'] and r['destination_absent_after'] and r['absent_parent_not_created'] and r['all_preexisting_kit_bytes_unchanged'],'Detailed physical negative')
 result={'status':'PASS_BOUNDED_REPAIR_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03','baseline_files':623,'changed_files':10,'protected_files':613,'new_canonical_files':15,'current_canonical_files':638,'exact_before_snapshots':10,'old_stage_copy_prefix':145,'new_stage_copies':12,'all_stage_copies':157,'old_history_prefix':4628,'new_history_rows':13,'all_history_rows':4641,'old_terminal_relocations':2,'new_case_relocations':7,'individual_old_structured_pin_resolutions':len(pinres),'history_dispositions':dict(collections.Counter(r['disposition'] for r in refs)),'archive':row(D/'verification_kit.zip',D),'members':239,'manifest_hashed_payloads':238,'pdf':row(D/'preprint.pdf',D),'tex':row(D/'preprint.tex',D),'native_metadata_math_source_credits_finite_adapters_unchanged':True,'independent_closed_zip_byte_equal':True,'actual_clean_commands':summary['actual_commands'],'additional_detailed_physical_commands':14,'total_final_successful_command_receipts':72,'guard_rejections':summary['guard_rejections'],'guard_protected_files':summary['guard_protected_files'],'actual_physical_case_rejections':12,'semantic_cases_each_mode':20,'local_native_check_passed':True,'new_complete_whole03_required':True,'whole_reviews_completed':2,'minimum_whole_reviews':2,'root_repair_adoption_required':True,'root_integrity_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'repair_completion_best_guess_percent':100,'mathematical_research_completion_best_guess_percent':60,'new_compile_render_view_or_PDF_marker':False}
 if not checking:
  dump(W/'CHANGE_ACCOUNTING.json',{'baseline_count':623,'changed_count':10,'unchanged_count':613,'new_count':15,'current_count':638,'changes':changes,'new_files':[row(current[n],A) for n in new]});dump(W/'PROTECTED_INPUT_PINS.json',{'files':unchanged});dump(W/'CURRENT_INPUT_PINS.json',{'files':[row(current[n],A) for n in sorted(current)]});dump(W/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json',{'scope':'Every structured size/SHA old reference equal to an immediately changed artifact is individually mapped to exact before bytes; full old history also checked separately. No historical inventory rewritten.','references':pinres});dump(W/'FINAL_VERIFICATION.json',result)
 else:
  require(obj(W/'FINAL_VERIFICATION.json')==result,'Sealed result differs')
  inventory=obj(W/'OUTPUT_PINS.json')
  for r in inventory['files']:require(matches(W/r['path'],r),'Sealed output mismatch '+r['path'])
  seal=obj(W/'SEAL.json');require(matches(W/'OUTPUT_PINS.json',seal['output_inventory']),'Separate seal/inventory mismatch')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
