#!/usr/bin/env python3
"""Complete root-reviewable custody verification for this bounded successor."""
import collections, difflib, hashlib, io, json, sys, zipfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent; A=W.parents[1]; D=A/'preprint_v1_0'; K=D/'verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def row(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def require(test,msg):
    if not test:raise RuntimeError(msg)
def matches(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def main():
    require(not (W/'SEAL.json').exists(),'Cannot rewrite sealed administrative stage')
    immediate=obj(W/'IMMEDIATE_INPUT_PINS.json')['files']; before={r['original_path']:r for r in obj(W/'BEFORE_COPIES.json')['files']}
    current={p.relative_to(A).as_posix():p for p in A.rglob('*') if p.is_file() and not p.is_relative_to(W)}
    protected=[]; changed=[]
    for r in immediate:
        name=r['path'];require(name in current,'Missing baseline file '+name)
        if matches(current[name],r):protected.append(r)
        else:
            require(name in before and matches(A/before[name]['source_snapshot'],r),'Unauthorized change or missing before '+name)
            changed.append({'path':name,'before':r,'after':row(current[name],A),'source_snapshot':before[name]['source_snapshot']})
    require(set(before)=={r['path'] for r in changed},'Before/changed set differs')
    require(len(immediate)==536 and len(changed)==9 and len(protected)==527,'Unexpected preservation counts')
    new=sorted(set(current)-{r['path'] for r in immediate})
    require(len(current)==584 and len(new)==48,'Unexpected new/current count')
    dump(W/'CHANGE_ACCOUNTING.json',{'baseline_count':len(immediate),'changed_count':len(changed),'unchanged_count':len(protected),'new_count':len(new),'current_count':len(current),'changes':changed,'new_files':[row(current[n],A) for n in new]})
    dump(W/'PROTECTED_INPUT_PINS.json',{'scope':'Every unchanged immediate input, including all historical statuses/seals, all paper/native metadata, all finite-checker and writer-guard programs.','files':protected})
    dump(W/'CURRENT_INPUT_PINS.json',{'scope':'Complete current audit outside this administrative workspace; captured stage only, not an instruction to rewrite old inventories.','files':[row(current[n],A) for n in sorted(current)]})
    prior_output_counts={}
    for stage in ['reviews/package_01','repairs/package01','repairs/package01_metadata_date02','reviews/package_02']:
        inventory=obj(A/stage/'OUTPUT_PINS.json')['files']
        for r in inventory:require(matches(A/stage/r['path'],r),'Previously sealed authored output changed '+stage+'/'+r['path'])
        prior_output_counts[stage]=len(inventory)
    for name in ['metadata.json','deposit_metadata.json','research_metadata.json','preprint.pdf','preprint.tex','CURRENT_STATUS_REPAIR01.json','verification_kit/metadata.json','verification_kit/research_metadata.json','verification_kit/run_checks.py','verification_kit/build_archive.py','verification_kit/fault_checks.py','verification_kit/output_guard_checks.py','verification_kit/METADATA_DATE02_ADMIN_STAGE.json']:
        pin=next(r for r in immediate if r['path']=='preprint_v1_0/'+name);require(matches(D/name,pin),'Protected core changed '+name)
    require((D/'metadata.json').read_bytes()==(K/'metadata.json').read_bytes() and obj(D/'deposit_metadata.json')['metadata']==obj(D/'metadata.json'),'Native metadata equality')
    require(obj(D/'deposit_metadata.json')['files']==[{'path':'preprint.pdf','name':'preprint.pdf'},{'path':'verification_kit.zip','name':'verification_kit.zip'}],'Attachment list')
    copies=obj(K/'REPAIR01_STAGE_COPIES.json')['files']; previous=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json')['files']; appended=obj(W/'NEW_COPY_ROWS.json')['files']
    require(len(copies)==145 and copies[:100]==previous and copies[100:]==appended and len(appended)==45,'Exact old-copy prefix/append')
    for r in copies:require(matches(A/r['source_snapshot'],r) and matches(K/r['destination'],r),'Exact stage source/copy '+r['destination'])
    history=obj(K/'REPAIR01_HISTORY_RESOLUTION.json'); oldhistory=obj(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json')
    require(history['references'][:2312]==oldhistory['references'] and len(history['references'])==4628,'Old history prefix/total')
    reloc=obj(K/'TERMINAL_HISTORY_RELOCATIONS.json')['rows']; require(len(reloc)==2 and {r['reference_index'] for r in reloc}=={1050,1455},'Relocation indices')
    relocation={r['reference_index']:r for r in reloc}; groups=collections.defaultdict(list)
    for i,r in enumerate(history['references']):
        groups[r['stage']].append(r)
        if r['disposition']=='exact_captured_stage_or_canonical_copy':
            target=r['destination']
            if i in relocation:
                require(relocation[i]['historical_reference']==r,'Historical relocation record differs');target=relocation[i]['current_exact_destination']
            require(matches(K/target,r),'Historical exact bytes differ '+str(i))
        else:require(r['disposition']=='omitted' and bool(r['reason']),'Unexplained individual omission')
    prefixes={'immediate-before-repair01':'','preparation-input194':'','preparation-output90':'preprint_v1_0/','whole01-input289':'','whole01-output17':'reviews/package_01/','metadata-date02-immediate404':'','repair01-current360':'','repair01-protected298':'','repair01-output42':'repairs/package01/','repair01-immediate309':''}
    specs={r['stage']:r for r in obj(W/'APPENDED_HISTORY_SPECIFICATION.json')['inventories']}
    require(set(groups)==set(prefixes)|set(specs),'History stage set differs')
    countdict={}
    for stage,refs in groups.items():
        s=specs.get(stage); inventory=s['inventory'] if s else refs[0]['inventory'];key=s['key'] if s else 'files';prefix=s['prefix'] if s else prefixes[stage]
        original=obj(A/inventory)[key]
        require([(prefix+r['path'],r['bytes'],r['sha256']) for r in original]==[(r['original_path'],r['bytes'],r['sha256']) for r in refs] and len(refs)==history['inventory_counts'][stage],'Complete ordered original inventory differs '+stage)
        countdict[stage]=dict(collections.Counter(r['disposition'] for r in refs))
    names=obj(K/'ALLOWLIST.json')['members'];require(len(names)==225 and len(obj(K/'MANIFEST.json')['files'])==224,'Payload count')
    require(sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file())==names,'Allowlist filesystem')
    for r in obj(K/'MANIFEST.json')['files']:require(matches(K/r['path'],r),'Current payload pin')
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
        for n in names:
            info=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED;z.writestr(info,(K/n).read_bytes())
    require(buf.getvalue()==(D/'verification_kit.zip').read_bytes(),'Independent CLOSED ZIP mismatch')
    require(obj(W/'REPRODUCTION_SUMMARY.json')['status']=='PASS' and obj(W/'REPRODUCTION_SUMMARY.json')['canonical_inputs_unchanged_during_reproduction']==584,'Reproduction snapshot')
    receipts=[json.loads(x) for x in (W/'REPRODUCTION_RECEIPTS.jsonl').read_text().splitlines()]
    require(len(receipts)==33 and all(r['returncode']==0 if r['expected']==0 else r['returncode']!=0 for r in receipts),'Actual commands failed/count')
    runresults=[json.loads(r['stdout']) for r in receipts if r['label']=='full finite adapters'];require(len(runresults)==2 and runresults[0]==runresults[1],'Full normal/-O result JSON')
    guards=[json.loads(r['stdout']) for r in receipts if r['label']=='complete existing output-alias suite']; require(len(guards)==2 and all(g['status']=='PASS' and g['protected_file_count']==231 and g['rejection_count']==480 for g in guards),'Guard counts')
    stage=obj(K/'TERMINAL_ADMIN_STAGE.json');require((K/'TERMINAL_ADMIN_STAGE.json').read_bytes()==(D/'TERMINAL_ADMIN_STAGE.json').read_bytes() and stage['whole_reviews_completed']==2 and stage['minimum_whole_reviews']==2 and stage['latest_review_actionable_P0_P1_P2_P3']==0 and stage['root_integrity_adoption_required'] and not any(stage[k] for k in ['publication_ready','issues_resolved','published','root_integrity_adopted']) and stage['services_held_at']==1032,'Terminal stage')
    patch=[]
    for r in changed:
        name=r['path']
        if name.endswith(('/ALLOWLIST.json','/MANIFEST.json','/REPAIR01_STAGE_COPIES.json','/REPAIR01_HISTORY_RESOLUTION.json','.zip')):continue
        patch.extend(difflib.unified_diff((A/r['source_snapshot']).read_text().splitlines(keepends=True),(A/name).read_text().splitlines(keepends=True),fromfile='before/'+name,tofile='after/'+name))
    for name in ['preprint_v1_0/TERMINAL_ADMIN_STAGE.json','preprint_v1_0/verification_kit/TERMINAL_ADMIN_STAGE.json','preprint_v1_0/verification_kit/TERMINAL_HISTORY_RELOCATIONS.json']:
        patch.extend(difflib.unified_diff([], (A/name).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/'+name))
    (W/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(patch))
    dump(W/'FINAL_VERIFICATION.json',{'status':'PASS_TERMINAL_ADMIN_PENDING_ROOT_INTEGRITY_ADOPTION','baseline_files':536,'changed_files':9,'protected_files':527,'new_files':48,'current_files':584,'before_snapshots':9,'delivered_new_exact_copies':45,'all_stage_copies':145,'original_stage_copy_prefix_unchanged':100,'original_history_prefix_unchanged':2312,'appended_history_rows':2316,'all_history_rows':4628,'historical_exact_relocations':2,'history_counts':countdict,'prior_sealed_output_counts':prior_output_counts,'archive':row(D/'verification_kit.zip',D),'archive_members':225,'manifest_hashed_payloads':224,'pdf':row(D/'preprint.pdf',D),'tex':row(D/'preprint.tex',D),'all_native_metadata_and_paper_bytes_unchanged':True,'finite_checker_and_writer_guard_bytes_unchanged':True,'actual_clean_commands':33,'guard_invocations':2,'guard_rejections_per_invocation':480,'guard_total_rejections':960,'terminal_semantic_cases_each_mode':7,'independent_closed_zip_byte_exact':True,'actual_local_native_check_passed':True,'normal_optimized_full_finite_json_equal':True,'no_new_compile_render_view_or_marker':True,'whole_reviews_completed':2,'minimum_whole_reviews':2,'latest_review_actionable_P0_P1_P2_P3':0,'root_integrity_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'administrative_completion_percent':100,'mathematical_research_completion_best_guess_percent':60})
    case=obj(W/'CASE_ALIAS_OUTPUT_FINDING.json')
    require(case['status']=='REPRODUCED_P3_CASE_ALIAS_OUTPUT_BOUNDARY' and case['canonical_candidate_unchanged'] and not case['root_integrity_adoption_eligible'] and len(case['normal_and_optimized_results'])==2,'New regression finding missing')
    require({r['optimized'] for r in case['normal_and_optimized_results']}=={False,True} and all(r['physical_directory_samefile'] and r['lexical_alias_outside_root'] and r['destination_initially_absent'] and r['returncode']==0 and r['accepted_and_created_physically_inside_kit'] and r['all_preexisting_disposable_kit_bytes_unchanged'] for r in case['normal_and_optimized_results']),'Case regression receipts differ')
    final=obj(W/'FINAL_VERIFICATION.json')
    final.update(status='PASS_BOUNDED_ADMIN_CUSTODY_NEW_P3_CASE_ALIAS_REPAIR_REQUIRED',root_integrity_adoption_eligible=False,new_unresolved_findings=[{'id':'TERMINAL-P3-CASE-INSENSITIVE-OUTPUT-BOUNDARY','priority':'P3','receipt':'CASE_ALIAS_OUTPUT_FINDING.json'}],new_complete_review_required=True,required_next_complete_review='NEW whole03 after bounded physical-output-containment repair',additional_actual_case_regression_commands=2,total_actual_final_standard_and_case_commands=35,delivered_terminal_record_is_dated_pre_new_finding_checkpoint=True)
    dump(W/'FINAL_VERIFICATION.json',final)
    print(json.dumps(obj(W/'FINAL_VERIFICATION.json'),indent=2))
if __name__=='__main__':main()
