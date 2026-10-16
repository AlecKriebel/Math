#!/usr/bin/env python3
"""Full bounded successor custody; --check replays the terminal seal read-only."""
import collections, hashlib, io, json, sys, zipfile, zlib
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent; A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def obj(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def need(x,m):
    if not x:raise RuntimeError(m)
def matches(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def pointer(v,p):
    for t in p.split('/')[1:]:
        t=t.replace('~1','/').replace('~0','~');v=v[int(t)] if isinstance(v,list) else v[t]
    return v
def main():
    check='--check' in sys.argv;need(check or not (W/'SEAL.json').exists(),'Cannot rewrite a sealed successor')
    before=obj(W/'BEFORE_COPIES.json')['files'];byname={r['original_path']:r for r in before};frozen=obj(W/'IMMEDIATE_INPUT_PINS.json')['files']
    current={p.relative_to(A).as_posix():p for p in A.rglob('*') if p.is_file() and not p.is_symlink() and not p.is_relative_to(W)}
    changed=[];protected=[]
    for r in frozen:
        n=r['path'];need(n in current,'Missing frozen input '+n)
        if matches(current[n],r):protected.append(r)
        else:
            need(n in byname and matches(A/byname[n]['source_snapshot'],r),'Unauthorized mutation '+n)
            changed.append({'path':n,'before':r,'after':row(current[n],A),'source_snapshot':byname[n]['source_snapshot']})
    new=sorted(set(current)-{r['path'] for r in frozen})
    need(len(frozen)==721 and len(changed)==8 and len(protected)==713 and len(new)==29 and len(current)==750,'Complete baseline/change/new count')
    need(set(byname)=={r['path'] for r in changed},'Before snapshots do not equal changed set')
    for r in before:need(matches(A/r['source_snapshot'],r),'Exact before bytes '+r['original_path'])
    # Prefixes and complete old stage/source copy resolutions.
    oldcopies=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json')['files'];copies=obj(K/'REPAIR01_STAGE_COPIES.json')['files'];addedcopies=obj(W/'NEW_COPY_ROWS.json')['files']
    need(len(oldcopies)==157 and copies[:157]==oldcopies and copies[157:]==addedcopies and len(copies)==181,'157-copy exact prefix and 24 append')
    for r in copies:need(matches(A/r['source_snapshot'],r) and matches(K/r['destination'],r),'Exact source/delivery copy '+r['destination'])
    oldhistory=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json');history=obj(K/'REPAIR01_HISTORY_RESOLUTION.json');refs=history['references'];added=obj(W/'APPENDED_HISTORY_ROWS.json')['references']
    need(len(oldhistory['references'])==4641 and refs[:4641]==oldhistory['references'] and refs[4641:]==added and len(refs)==4666,'4641-history exact prefix and 25 append')
    need(collections.Counter(r['disposition'] for r in refs[:4641])=={'exact_captured_stage_or_canonical_copy':3207,'omitted':1434},'3207 exact/1434 individually omitted old rows')
    terminal=obj(K/'TERMINAL_HISTORY_RELOCATIONS.json')['rows'];case=obj(K/'CASE_ALIAS_HISTORY_RELOCATIONS.json')['rows'];need(len(terminal)==2 and len(case)==7,'Nine old relocations preserved')
    reloc={r['reference_index']:r for r in terminal+case};need(len(reloc)==9,'Relocation indices')
    for i,r in reloc.items():need(refs[i]==r['historical_reference'],'Full old relocation row identity')
    groups=collections.defaultdict(list)
    for i,r in enumerate(refs):
        groups[r['stage']].append(r)
        if r['disposition']=='exact_captured_stage_or_canonical_copy':need(matches(K/(reloc[i]['current_exact_destination'] if i in reloc else r['destination']),r),'History resolution '+str(i))
        else:need(r['disposition']=='omitted' and bool(r['reason']),'Individual omission '+str(i))
    prefixes={'immediate-before-repair01':'','preparation-input194':'','preparation-output90':'preprint_v1_0/','whole01-input289':'','whole01-output17':'reviews/package_01/','metadata-date02-immediate404':'','repair01-current360':'','repair01-protected298':'','repair01-output42':'repairs/package01/','repair01-immediate309':''}
    specs={r['stage']:r for r in obj(A/'finalization/terminal_admin_20261016/APPENDED_HISTORY_SPECIFICATION.json')['inventories']}
    special={'case-alias01-changed-before':(A/'repairs/case_alias01/BEFORE_COPIES.json','files','original_path'), 'case-alias01-selected-evidence':(A/'repairs/case_alias01/SELECTED_CASE_INPUTS.json','files','path'), 'archive-wording01-changed-before':(W/'BEFORE_COPIES.json','files','original_path'),'archive-wording01-selected-evidence':(W/'SELECTED_WHOLE03_INPUTS.json','files','path')}
    need(set(groups)==set(prefixes)|set(specs)|set(special),'Complete stage set')
    for stage,rs in groups.items():
        if stage in special:
            p,key,pathkey=special[stage];tuples=[(r[pathkey],r['bytes'],r['sha256']) for r in obj(p)[key]]
        else:
            spec=specs.get(stage);inventory=spec['inventory'] if spec else rs[0]['inventory'];key=spec['key'] if spec else 'files';prefix=spec['prefix'] if spec else prefixes[stage]
            tuples=[(prefix+r['path'],r['bytes'],r['sha256']) for r in obj(A/inventory)[key]]
        need(tuples==[(r['original_path'],r['bytes'],r['sha256']) for r in rs] and len(rs)==history['inventory_counts'][stage],'Complete ordered stage '+stage)
    # Preserve and re-resolve all 75 earlier structured pointers using their original before interfaces.
    oldcase=obj(A/'repairs/case_alias01/BEFORE_COPIES.json')['files'];oldby={r['original_path']:r for r in oldcase}
    older=obj(A/'repairs/case_alias01/INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json')['references'];need(len(older)==75,'75 old structured resolutions')
    def validate_resolution(r,source):
        need(pointer(obj(source),r['json_pointer'])==r['original_pin'],'Structured old pointer '+r['source_inventory']+r['json_pointer'])
        need(matches(A/r['exact_local_before'],r['original_pin']),'Exact local old-pointer bytes')
        if r['delivered_before'] is not None:need(matches(K/r['delivered_before'],r['original_pin']),'Exact delivered old-pointer bytes')
    for r in older:
        n=r['source_inventory'];source=A/(oldby[n]['source_snapshot'] if n in oldby else byname[n]['source_snapshot'] if n in byname else n);validate_resolution(r,source)
    resolutions=obj(W/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json')['references'];need(len(resolutions)==42,'42 new before resolutions')
    for r in resolutions:validate_resolution(r,A/r['source_snapshot'])
    need(obj(K/'ARCHIVE_WORDING01_OLD_PIN_RESOLUTIONS.json')==obj(W/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json'),'Delivered structured map differs')
    need(obj(K/'ARCHIVE_WORDING01_BEFORE_MAP.json')['files']==[{**r,'delivered_before':None if r['original_path'].endswith('.zip') else 'archive_wording01_history/before/'+r['original_path'],'reason':'Old ZIP deliberately not newly packed; retained exact locally only.' if r['original_path'].endswith('.zip') else 'Exact immediate before bytes.'} for r in before],'Explicit before map')
    omissions=obj(K/'ARCHIVE_WORDING01_SOURCE_BODY_OMISSIONS.json')['files'];need(len(omissions)==8 and all(r['disposition']=='omitted' and r['reason'] for r in omissions),'Eight individual new source body omissions')
    for r in omissions:need(matches(Path(r['original_path']),r),'Original source body no mutation')
    status=obj(K/'CURRENT_ARCHIVE_WORDING_REPAIR01.json');need((K/'CURRENT_ARCHIVE_WORDING_REPAIR01.json').read_bytes()==(D/'CURRENT_ARCHIVE_WORDING_REPAIR01.json').read_bytes(),'Outer/kit current status')
    need(status['whole_reviews_completed']==3 and status['minimum_whole_reviews']==2 and status['latest_complete_review']=='whole03' and status['latest_review_actionable_counts']=={'P0':0,'P1':0,'P2':0,'P3':1} and status['latest_complete_review_zero_findings'] is False and status['root_whole03_adopted'] is True,'Three completed/latest one P3')
    need(status['new_complete_review_required'] is True and status['required_next_review']=='NEW complete whole04' and all(status[k] is False for k in ['root_repair_adopted','root_integrity_adopted','publication_ready','issues_resolved','published']) and status['services_held_at']==1032,'Current mandatory ROOT/whole04/readiness boundary')
    native=obj(D/'metadata.json');upload=obj(D/'deposit_metadata.json');need((D/'metadata.json').read_bytes()==(K/'metadata.json').read_bytes() and upload=={'metadata':native,'files':[{'path':'preprint.pdf','name':'preprint.pdf'},{'path':'verification_kit.zip','name':'verification_kit.zip'}]},'Exact native schema and attachments')
    binding=obj(D/'EXTERNAL_BINDING.json');need(matches(D/binding['current_archive_wording_status']['filename'],binding['current_archive_wording_status']),'Current outer status explicitly bound')
    need(binding['manifest_sha256']==sha(K/'MANIFEST.json') and matches(D/binding['archive']['filename'],binding['archive']),'Manifest/archive external binding')
    names=obj(K/'ALLOWLIST.json')['members'];need(len(names)==267 and names==sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()),'Closed allowlist')
    manifest=obj(K/'MANIFEST.json');need([r['path'] for r in manifest['files']]==[n for n in names if n!='MANIFEST.json'],'266 manifest payloads')
    for r in manifest['files']:need(matches(K/r['path'],r),'Pinned payload '+r['path'])
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=0) as z:
        for n in names:
            i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=0;z.writestr(i,(K/n).read_bytes())
    need(buf.getvalue()==(D/'verification_kit.zip').read_bytes(),'Independently reconstructed closed ZIP')
    with zipfile.ZipFile(D/'verification_kit.zip') as z:
        need(z.namelist()==['verification_kit/'+n for n in names] and not z.comment and z.testzip() is None,'ZIP inventory/order/CRC')
        for i,n in zip(z.infolist(),names):
            b=(K/n).read_bytes();need(z.read(i)==b and i.CRC==(zlib.crc32(b)&0xffffffff) and i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==0 and not i.extra and not i.comment and i.flag_bits==0,'ZIP payload/header '+n)
        archives=[n for n in names if n.endswith('.zip')];need(len(archives)==3 and all(not n.startswith('archive_wording01_history/') for n in archives),'Exactly three retained historical ZIPs; no new duplicate ZIP')
        need((K/archives[1]).read_bytes()==(K/archives[2]).read_bytes(),'Retained duplicate archives exact')
    summary=obj(W/'REPRODUCTION_SUMMARY.json');need(summary['status']=='PASS' and summary['canonical_files_unchanged']==750 and summary['physical_case_rejections']==12 and summary['independent_semantic_commands']==42,'Actual clean guards and interfaces')
    actual=[json.loads(s) for s in (W/'ACTUAL_COMMAND_RECEIPTS.jsonl').read_text().splitlines()];need(len(actual)==summary['actual_driver_commands'] and all((r['returncode']==0)==r['expected_success'] for r in actual),'Actual command receipts')
    need((W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json').read_bytes()==(W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json').read_bytes(),'Full normal/-O mathematical equality')
    for suffix in ['','_O']:need(obj(W/('FULL_MATHEMATICAL_OUTPUT_COMPARISON'+suffix+'.json'))==obj(A/('reviews/package_03/FULL_MATHEMATICAL_OUTPUT_COMPARISON'+suffix+'.json')),'Adopted whole03 full mathematics')
    result={'status':'PASS_BOUNDED_WORDING_REPAIR_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE04','baseline_files':721,'changed_files':8,'protected_files':713,'new_canonical_files':29,'current_canonical_files':750,'exact_before_files':8,'old_copy_prefix':157,'new_copies':24,'current_copies':181,'old_history_prefix':4641,'old_exact_references':3207,'old_individual_omissions':1434,'new_history_rows':25,'current_history_rows':4666,'history_dispositions':dict(collections.Counter(r['disposition'] for r in refs)),'old_relocations':9,'preserved_old_structured_pointers':75,'new_structured_before_resolutions':42,'new_individual_source_body_omissions_separate_from_old_rows':8,'retained_historical_archives':3,'newly_selected_duplicate_archives':0,'members':267,'manifest_payloads':266,'archive':row(D/'verification_kit.zip',D),'pdf':row(D/'preprint.pdf',D),'tex':row(D/'preprint.tex',D),'paper_native_metadata_all_checkers_pathguards_dated_history_unchanged':True,'independent_closed_zip_byte_equal':True,**summary,'repair_completion_best_guess_percent':100,'mathematical_research_completion_best_guess_percent':60,'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_review_one_P3':True,'required_next_review':'NEW complete whole04','root_repair_adoption_required':True,'root_integrity_adoption_required':True}
    result['status']='PASS_BOUNDED_WORDING_REPAIR_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE04'
    if check:
        need(obj(W/'FINAL_VERIFICATION.json')==result,'Sealed verification result differs')
        inventory=obj(W/'OUTPUT_PINS.json')
        for r in inventory['files']:need(matches(W/r['path'],r),'Sealed repair artifact '+r['path'])
        need(matches(W/'OUTPUT_PINS.json',obj(W/'SEAL.json')['output_inventory']),'Separate seal binding')
    else:
        dump(W/'CHANGE_ACCOUNTING.json',{'baseline_count':721,'changed_count':8,'unchanged_count':713,'new_count':29,'current_count':750,'changes':changed,'new_files':[row(current[n],A) for n in new]});dump(W/'PROTECTED_INPUT_PINS.json',{'files':protected});dump(W/'CURRENT_INPUT_PINS.json',{'files':[row(current[n],A) for n in sorted(current)]});dump(W/'FINAL_VERIFICATION.json',result)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
