#!/usr/bin/env python3
"""Read-only or authoring custody check for this exact terminal administrative stage."""
from pathlib import Path
import collections,hashlib,io,json,sys,zipfile,zlib
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def obj(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def need(x,m):
 if not x:raise RuntimeError(m)
def matches(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def pointer(v,p):
 for t in p.split('/')[1:]:
  t=t.replace('~1','/').replace('~0','~');v=v[int(t)] if isinstance(v,list) else v[t]
 return v
def main():
 check='--check' in sys.argv;need(check or not (W/'SEAL.json').exists(),'Never modify sealed terminal evidence')
 before=obj(W/'BEFORE_COPIES.json')['files'];by={r['original_path']:r for r in before};frozen=obj(W/'IMMEDIATE_INPUT_PINS.json')['files']
 current={p.relative_to(A).as_posix():p for p in A.rglob('*') if p.is_file() and not p.is_symlink() and not p.is_relative_to(W)}
 changes=[];protected=[]
 for r in frozen:
  n=r['path'];need(n in current,'Missing frozen input '+n)
  if matches(current[n],r):protected.append(r)
  else:
   need(n in by and matches(A/by[n]['source_snapshot'],r),'Unauthorized mutation '+n);changes.append({'path':n,'before':r,'after':row(current[n],A),'source_snapshot':by[n]['source_snapshot']})
 new=sorted(set(current)-{r['path'] for r in frozen});need(len(frozen)==865 and len(changes)==9 and len(protected)==856 and len(new)==33 and len(current)==898,'Complete baseline/change/new membership')
 need(set(by)=={r['path'] for r in changes},'Exact nine changed set')
 for r in before:need(matches(A/r['source_snapshot'],r),'Exact before '+r['original_path'])
 oldcopies=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json')['files'];copies=obj(K/'REPAIR01_STAGE_COPIES.json')['files'];addcopies=obj(W/'NEW_COPY_ROWS.json')['files']
 need(len(oldcopies)==181 and copies[:181]==oldcopies and copies[181:]==addcopies and len(copies)==207,'181-copy exact prefix/26 append')
 for r in copies:need(matches(A/r['source_snapshot'],r) and matches(K/r['destination'],r),'Exact copy pair '+r['destination'])
 oldhistory=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json');history=obj(K/'REPAIR01_HISTORY_RESOLUTION.json');refs=history['references'];added=obj(W/'APPENDED_HISTORY_ROWS.json')['references']
 need(len(oldhistory['references'])==4666 and refs[:4666]==oldhistory['references'] and refs[4666:]==added and len(refs)==4731,'4666-history exact prefix/65 append')
 need(collections.Counter(r['disposition'] for r in refs[:4666])=={'exact_captured_stage_or_canonical_copy':3231,'omitted':1435},'Old exact/individual omission accounting')
 reloc={}
 for name,count in [('TERMINAL_HISTORY_RELOCATIONS.json',2),('CASE_ALIAS_HISTORY_RELOCATIONS.json',7),('TERMINAL_AFTER_WHOLE04_HISTORY_RELOCATIONS.json',0)]:
  rows=obj(K/name)['rows'];need(len(rows)==count,'Relocation count '+name)
  for r in rows:
   i=r['reference_index'];need(i not in reloc and refs[i]==r['historical_reference'],'Full original relocation row');reloc[i]=r
 groups=collections.defaultdict(list)
 for i,r in enumerate(refs):
  groups[r['stage']].append(r)
  if r['disposition']=='exact_captured_stage_or_canonical_copy':need(matches(K/(reloc[i]['current_exact_destination'] if i in reloc else r['destination']),r),'History resolution '+str(i))
  else:need(r['disposition']=='omitted' and bool(r['reason']),'Individual omission '+str(i))
 prefixes={'immediate-before-repair01':'','preparation-input194':'','preparation-output90':'preprint_v1_0/','whole01-input289':'','whole01-output17':'reviews/package_01/','metadata-date02-immediate404':'','repair01-current360':'','repair01-protected298':'','repair01-output42':'repairs/package01/','repair01-immediate309':''}
 specs={r['stage']:r for r in obj(A/'finalization/terminal_admin_20261016/APPENDED_HISTORY_SPECIFICATION.json')['inventories']}
 special={'case-alias01-changed-before':(A/'repairs/case_alias01/BEFORE_COPIES.json','files','original_path',''),'case-alias01-selected-evidence':(A/'repairs/case_alias01/SELECTED_CASE_INPUTS.json','files','path',''),'archive-wording01-changed-before':(A/'repairs/archive_wording01/BEFORE_COPIES.json','files','original_path',''),'archive-wording01-selected-evidence':(A/'repairs/archive_wording01/SELECTED_WHOLE03_INPUTS.json','files','path',''),'terminal-after-whole04-changed-before':(W/'BEFORE_COPIES.json','files','original_path',''),'terminal-after-whole04-output52':(A/'newreviews/package_04/OUTPUT_PINS.json','files','path','newreviews/package_04/'),'terminal-after-whole04-extra-selected':(W/'SELECTED_EXTRA_INPUTS.json','files','path','')}
 need(set(groups)==set(prefixes)|set(specs)|set(special),'Complete inventory stage set')
 for stage,rs in groups.items():
  if stage in special:
   p,key,pathkey,prefix=special[stage];expected=[(prefix+r[pathkey],r['bytes'],r['sha256']) for r in obj(p)[key]]
  else:
   spec=specs.get(stage);inventory=spec['inventory'] if spec else rs[0]['inventory'];key=spec['key'] if spec else 'files';prefix=spec['prefix'] if spec else prefixes[stage];expected=[(prefix+r['path'],r['bytes'],r['sha256']) for r in obj(A/inventory)[key]]
  need(expected==[(r['original_path'],r['bytes'],r['sha256']) for r in rs] and len(rs)==history['inventory_counts'][stage],'Complete ordered inventory '+stage)
 # All old pointer chains resolved against original exact before snapshots, never live changed bytes.
 caseby={r['original_path']:r for r in obj(A/'repairs/case_alias01/BEFORE_COPIES.json')['files']};archiveby={r['original_path']:r for r in obj(A/'repairs/archive_wording01/BEFORE_COPIES.json')['files']}
 def validate(r,source):
  need(pointer(obj(source),r['json_pointer'])==r['original_pin'],'Original JSON pointer '+r['source_inventory']+r['json_pointer'])
  need(matches(A/r['exact_local_before'],r['original_pin']),'Local before pointer target')
  if r['delivered_before'] is not None:need(matches(K/r['delivered_before'],r['original_pin']),'Delivered before pointer target')
 old75=obj(A/'repairs/case_alias01/INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json')['references'];need(len(old75)==75,'75 old pointer chains')
 for r in old75:
  n=r['source_inventory'];p=A/(caseby[n]['source_snapshot'] if n in caseby else archiveby[n]['source_snapshot'] if n in archiveby else by[n]['source_snapshot'] if n in by else n);validate(r,p)
 old42=obj(A/'repairs/archive_wording01/INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json')['references'];need(len(old42)==42,'42 archive wording pointer chains')
 for r in old42:
  n=r['source_snapshot'];validate(r,A/(by[n]['source_snapshot'] if n in by else n))
 resolutions=obj(W/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json')['references'];need(len(resolutions)==65,'65 current before pointer chains')
 for r in resolutions:validate(r,A/r['source_snapshot'])
 need(obj(K/'TERMINAL_AFTER_WHOLE04_OLD_PIN_RESOLUTIONS.json')['references']==resolutions,'Delivered pointer map')
 need(obj(K/'TERMINAL_AFTER_WHOLE04_BEFORE_MAP.json')['files']==[{**r,'delivered_before':None if r['original_path'].endswith('.zip') else 'terminal_after_whole04_history/before/'+r['original_path'],'reason':'Old archive local only; other before bytes exact delivered.'} for r in before],'Exact before map')
 decisions=obj(K/'TERMINAL_AFTER_WHOLE04_OUTPUT_DECISIONS.json')['files'];original=obj(A/'newreviews/package_04/OUTPUT_PINS.json')['files']
 need([{k:r[k] for k in ['path','bytes','sha256']} for r in decisions]==original and len(decisions)==52,'Complete52 decisions exact order')
 selected=obj(W/'SELECTED_INPUTS.json')['files'];need(len(selected)==18,'18 selected authored evidence')
 for r in decisions:
  need(matches(A/r['original_path'],r),'Original whole04 sealed output')
  if r['disposition']=='omitted':need(bool(r['reason']),'Output individual omission')
  else:need(matches(K/r['destination'],r),'Selected whole04 exact output')
 for r in selected:need(matches(A/r['path'],r) and matches(K/('terminal_after_whole04_history/evidence/'+r['path']),r),'Selected authored evidence pin')
 for name,count in [('ARCHIVE_WORDING01_SOURCE_BODY_OMISSIONS.json',8),('TERMINAL_AFTER_WHOLE04_SOURCE_BODY_OMISSIONS.json',8)]:
  omissions=obj(K/name)['files'];need(len(omissions)==count and all(r['disposition']=='omitted' and r['reason'] for r in omissions),'Individual source body omissions')
  for r in omissions:need(matches(Path(r['original_path']),r),'Original source body unchanged')
 # Rehash every earlier separately inventoried authored output at its exact original location.
 inventories=[]
 for r in frozen:
  if r['path'].endswith('/OUTPUT_PINS.json') and r['path'].split('/')[0] in ['reviews','newreviews','repairs','finalization']:
   p=A/r['path'];v=obj(p);rows=v.get('files',v.get('public_safe_files',[]))
   for x in rows:need(matches(p.parent/x['path'],x),'Preserved sealed output '+r['path']+' '+x['path'])
   inventories.append({'path':r['path'],'rows':len(rows)})
 status=obj(K/'CURRENT_TERMINAL_AFTER_WHOLE04.json');need((D/'CURRENT_TERMINAL_AFTER_WHOLE04.json').read_bytes()==(K/'CURRENT_TERMINAL_AFTER_WHOLE04.json').read_bytes(),'Current status identical')
 need(status['whole_reviews_completed']==4 and status['minimum_whole_reviews']==2 and status['latest_complete_review']=='whole04' and status['latest_review_actionable_counts']=={'P0':0,'P1':0,'P2':0,'P3':0} and status['root_whole04_adopted'] is True and status['new_complete_review_required'] is False,'Current adopted zero review accounting')
 need(status['root_integrity_adoption_required'] is True and all(status[k] is False for k in ['root_integrity_adopted','publication_ready','issues_resolved','published']) and status['services_held_at']==1032,'Final external ROOT boundary')
 native=obj(D/'metadata.json');upload=obj(D/'deposit_metadata.json');need((D/'metadata.json').read_bytes()==(K/'metadata.json').read_bytes() and upload=={'metadata':native,'files':[{'path':'preprint.pdf','name':'preprint.pdf'},{'path':'verification_kit.zip','name':'verification_kit.zip'}]},'Exact native schema/attachments')
 b=obj(D/'EXTERNAL_BINDING.json');need(matches(D/b['current_terminal_after_whole04']['filename'],b['current_terminal_after_whole04']) and b['manifest_sha256']==sha(K/'MANIFEST.json') and matches(D/b['archive']['filename'],b['archive']),'Current external binding')
 names=obj(K/'ALLOWLIST.json')['members'];need(names==sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()) and len(names)==299,'Closed299 allowlist')
 manifest=obj(K/'MANIFEST.json')['files'];need([r['path'] for r in manifest]==[n for n in names if n!='MANIFEST.json'],'Complete manifest membership')
 for r in manifest:need(matches(K/r['path'],r),'Manifest payload '+r['path'])
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',compression=0) as z:
  for n in names:
   i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=0;z.writestr(i,(K/n).read_bytes())
 need(buf.getvalue()==(D/'verification_kit.zip').read_bytes(),'Independent closed ZIP byte equality')
 with zipfile.ZipFile(D/'verification_kit.zip') as z:
  need(z.namelist()==['verification_kit/'+n for n in names] and not z.comment and z.testzip() is None,'ZIP order/comment/CRC')
  for i,n in zip(z.infolist(),names):
   payload=(K/n).read_bytes();need(z.read(i)==payload and i.CRC==(zlib.crc32(payload)&0xffffffff) and i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==0 and not i.extra and not i.comment and i.flag_bits==0,'ZIP complete header/payload '+n)
 archives=[n for n in names if n.endswith('.zip')];need(len(archives)==3 and not any(n.startswith('terminal_after_whole04_history/') for n in archives),'Three retained historical ZIPs/no new archive')
 need((K/archives[1]).read_bytes()==(K/archives[2]).read_bytes(),'Two identical historical ZIPs')
 for suffix in ['','_O']:need(obj(W/('FULL_MATHEMATICAL_OUTPUT_COMPARISON'+suffix+'.json'))==obj(A/('newreviews/package_04/FULL_MATHEMATICAL_OUTPUT_COMPARISON'+suffix+'.json')),'Adopted whole04 full mathematical JSON')
 summary=obj(W/'REPRODUCTION_SUMMARY.json');need(summary['status']=='PASS' and summary['canonical_files_unchanged']==898 and summary['extracted_files_unchanged']==299,'Actual reproduction counts')
 receipts=[json.loads(s) for s in (W/'ACTUAL_COMMAND_RECEIPTS.jsonl').read_text().splitlines()];need(len(receipts)==summary['actual_commands'] and len(receipts)==31 and all((r['returncode']==0)==r['expected_success'] for r in receipts[:26]+receipts[27:]) and receipts[26]['returncode']!=0 and 'Errno 28' in receipts[26]['stderr'],'Actual30 completed expected commands and one explicit ENOSPC interruption')
 result={'status':'PASS_TERMINAL_ADMIN_AFTER_ADOPTED_WHOLE04_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','baseline_files':865,'changed_files':9,'protected_files':856,'new_canonical_files':33,'current_canonical_files':898,'exact_before_files':9,'old_copy_prefix':181,'new_copies':26,'current_copies':207,'old_history_prefix':4666,'new_history_rows':65,'current_history_rows':4731,'history_dispositions':dict(collections.Counter(r['disposition'] for r in refs)),'old_relocations':9,'new_relocations':0,'preserved_old_structured_pointers':117,'new_structured_before_resolutions':65,'selected_authored_evidence':18,'whole04_output_rows_individually_decided':52,'selected_whole04_output_rows':14,'new_individual_source_body_omissions':8,'previous_sealed_output_inventories':inventories,'retained_historical_archives':3,'newly_selected_archives':0,'members':len(names),'manifest_payloads':len(manifest),'archive':row(D/'verification_kit.zip',D),'pdf':row(D/'preprint.pdf',D),'tex':row(D/'preprint.tex',D),'independent_closed_zip_byte_equal':True,'whole_reviews_completed':4,'minimum_whole_reviews':2,'latest_complete_review':'whole04','latest_zero_actionable_findings':True,'root_whole04_adopted':True,'new_complete_review_currently_required':False,'root_final_integrity_required':True,'root_final_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'administrative_completion_best_guess_percent':100,'mathematical_research_completion_best_guess_percent':60,'reproduction':summary}
 if check:
  need(obj(W/'FINAL_VERIFICATION.json')==result,'Sealed result differs')
  for r in obj(W/'OUTPUT_PINS.json')['files']:need(matches(W/r['path'],r),'Terminal sealed output '+r['path'])
  need(matches(W/'OUTPUT_PINS.json',obj(W/'SEAL.json')['output_inventory']),'Terminal separate seal')
 else:
  dump(W/'CHANGE_ACCOUNTING.json',{'baseline_count':865,'changed_count':9,'unchanged_count':856,'new_count':33,'current_count':898,'changes':changes,'new_files':[row(current[n],A) for n in new]});dump(W/'PROTECTED_INPUT_PINS.json',{'files':protected});dump(W/'CURRENT_INPUT_PINS.json',{'files':[row(current[n],A) for n in sorted(current)]});dump(W/'FINAL_VERIFICATION.json',result)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
