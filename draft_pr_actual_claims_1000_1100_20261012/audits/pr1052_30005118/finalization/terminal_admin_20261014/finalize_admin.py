"""Bounded PR1052 terminal administration; no proof/metadata/compiler/service edits."""
import ast,datetime,difflib,hashlib,io,json,shutil,subprocess,sys,time,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PUB=AUDIT/'preprint_v1_0'
REVIEW=AUDIT/'reviews/package_02'
ARCHIVE=PUB/'pr1052_support_v1_0.zip'
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
MUTABLE=['README.md','RESEARCH_LOG.md','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','verify_support.py','support/COPY_MAP.json','support/HISTORY.md','pr1052_support_v1_0.zip','pr1052_support_v1_0.zip.sha256','zenodo-deposit.json']
PROTECTED=['paper.tex','paper.pdf','paper.pdf.sha256','.zenodo.json','metadata.json','run_checks.py','test_integrity.py','build_pdf.py','build_support.py','verification/check_claim.py','OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json']
RUNS=[]
def require(ok,why):
    if not ok:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p,root=AUDIT):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def copy(p,q):
    require(not q.exists(),'refuse overwrite '+str(q));q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());require(p.read_bytes()==q.read_bytes(),'copy mismatch')
def inventory():return [rec(p) for p in sorted(AUDIT.rglob('*')) if p.is_file() and 'finalization' not in p.relative_to(AUDIT).parts]
def checkpoint(n,s):
    with (HERE/'RESEARCH_LOG.md').open('a') as out:out.write(f'\n{datetime.datetime.now(datetime.timezone.utc).isoformat()}: {n}% of bounded terminal administration. {s}\n')
def run(name,cmd,cwd,good=True):
    start=time.perf_counter();r=subprocess.run(cmd,cwd=cwd,capture_output=True)
    (HERE/(name+'.stdout')).write_bytes(r.stdout);(HERE/(name+'.stderr')).write_bytes(r.stderr)
    RUNS.append({'name':name,'command':cmd,'cwd':str(cwd.relative_to(AUDIT)),'exit_code':r.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'expected':'success' if good else 'rejection'})
    save(HERE/'RUNTIME_RECEIPTS.json',{'processes':RUNS});require((r.returncode==0)==good,'unexpected process '+name+': '+r.stderr.decode());return r
def checkrow(p,r):require(p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'pin mismatch '+str(p))
def check_inputs():
    require(AUDIT.name=='pr1052_30005118','only PR1052')
    root=json.loads((AUDIT/'ROOT_WHOLE_PACKAGE_REVIEW_02.json').read_text());v=json.loads((REVIEW/'VERDICT.json').read_text())
    require(root['status']=='ADOPT_ZERO_ACTIONABLE_WHOLE02_PENDING_TERMINAL_ADMIN_SEAL' and root['root_entire_report_and_verdict_read'] and root['root_independent_derivation_and_source_interface_read'] and root['mathematics_accepted_unchanged'] and root['fresh_whole_package_reviews']==2,'root full acceptance required')
    require(v['verdict']=='ACCEPT_SCOPED_WHOLE_PACKAGE' and v['finding_counts']=={'P0':0,'P1':0,'P2':0,'P3':0} and v['required_corrections']==[] and v['historical_P3_01_exact_implementation_verified'],'terminal findings or repair unresolved')
    require(sha(ARCHIVE)==v['support_zip_sha256'] and sha(PUB/'paper.pdf')==v['paper_pdf_sha256'],'reviewed archive/PDF changed')
    for name,key in [('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('OUTPUT_PINS.json','output_pins_sha256'),('REVIEW_SEAL.json','review_seal_sha256')]:require(sha(REVIEW/name)==root[key],'root accepted record mismatch '+name)
    rows=json.loads((REVIEW/'OUTPUT_PINS.json').read_text())['files'];require(len(rows)==29,'review output count')
    for r in rows:checkrow(REVIEW/r['path'],r)
    seal=json.loads((REVIEW/'REVIEW_SEAL.json').read_text())
    for name,key in [('INPUT_PINS.json','input_manifest_sha256'),('OUTPUT_PINS.json','output_manifest_sha256'),('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('FROZEN_DERIVATION.md','frozen_derivation_sha256')]:require(sha(REVIEW/name)==seal[key],'seal differs')
    oldmap=json.loads((PUB/'support/COPY_MAP.json').read_text());require(len(oldmap['copies'])==99,'old copy count')
    for r in oldmap['copies']:checkrow(PUB/r['package_path'],r);require((PUB/r['package_path']).read_bytes()==(AUDIT/r.get('source_snapshot',r['original_path'])).read_bytes(),'old copy/source mismatch')
    original=json.loads((AUDIT/'SUBMITTED_PINS.json').read_text());require(len(original['files'])==8,'original count')
    for r in original['files']:checkrow(AUDIT/r['snapshot_path'],r)
    require(len(json.loads((PUB/'OUTPUT_PINS.json').read_text())['files'])==91 and len(json.loads((PUB/'CURRENT_OUTPUT_PINS.json').read_text())['files'])==134,'historical preparation pin counts')
    repair=json.loads((AUDIT/'repairs/package01/OUTPUT_PINS.json').read_text())['files'];require(len(repair)==30,'repair output count')
    for r in repair:checkrow(AUDIT/'repairs/package01'/r['path'],r)
    metadata=json.loads((PUB/'.zenodo.json').read_text());require(json.loads((PUB/'metadata.json').read_text())['metadata']==metadata and json.loads((PUB/'zenodo-deposit.json').read_text())['metadata']==metadata,'three metadata objects differ')
    return rows,oldmap,metadata
def freeze():
    require(not (HERE/'INPUT_PINS.json').exists(),'do not reapply administration')
    rows,oldmap,metadata=check_inputs();before=inventory()
    save(HERE/'INPUT_PINS.json',{'utc':UTC,'files':before,'self_excluded':True,'scope':'Every immediate pre-existing regular audit file including private/source/repair/review custody, excluding only this new finalization effort. Hash references do not promise distribution.'})
    save(HERE/'FROZEN_BASELINE.json',{'utc':UTC,'protected':[rec(PUB/n) for n in PROTECTED],'reviewed_archive':rec(ARCHIVE),'old_99_copy_records':oldmap['copies'],'metadata_object':metadata,'root_adoption':rec(AUDIT/'ROOT_WHOLE_PACKAGE_REVIEW_02.json'),'allowed_existing_mutations':['preprint_v1_0/'+n for n in MUTABLE],'external_descriptor_change_boundary':'Only ZIP delivery size/digest; bibliographic metadata object and PDF binding unchanged; archive is external to its descriptor.'})
    (HERE/'.gitignore').write_text('frozen_before/\nscratch/\n')
    history=PUB/'support/history/before_terminal_admin_20261014'
    for n in MUTABLE+['OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json']:
        p=PUB/n;copy(p,HERE/'frozen_before/preprint_v1_0'/n)
        if n not in {'pr1052_support_v1_0.zip','pr1052_support_v1_0.zip.sha256','OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json'}:copy(p,history/n)
    save(history/'HISTORY.json',{'utc':UTC,'scope':'Exact repaired pending whole02 stage before terminal administration; old readiness flags and descriptors keep this dated input meaning','archive':rec(ARCHIVE),'duplicate_old_ZIP_PDF_not_distributed':True,'original_91_and_repaired_134_pin_files_unchanged':True,'external_frozen_binary_and_pin_custody':'finalization/terminal_admin_20261014/frozen_before/preprint_v1_0'})
    (HERE/'RESEARCH_LOG.md').write_text('# PR1052 terminal administrative research log\n');checkpoint(15,'Exact root full whole02 acceptance, all 29 outputs/seal, all 99 copies, original eight, three metadata objects and 30 repair outputs verified. Full immediate baseline frozen before mutations; mutable before bytes and unchanged 91/134 stage pin files preserved.')
    return rows,oldmap,metadata,before
def append_review(rows,oldmap):
    copies=[];omitted=[]
    rows=rows+[rec(REVIEW/'OUTPUT_PINS.json',REVIEW),rec(REVIEW/'REVIEW_SEAL.json',REVIEW)]
    for r in rows:
        p=REVIEW/r['path'];parts=PurePosixPath(r['path']);require(not parts.is_absolute() and '..' not in parts.parts,'unsafe review path')
        if len(parts.parts)!=1 or p.suffix not in {'.json','.md','.py'} or '.stdout.' in p.name or '.stderr.' in p.name:
            omitted.append({**r,'source_audit_relative':p.relative_to(AUDIT).as_posix(),'distribution':'OMITTED','reason':'Control file, full textual verifier diff, or raw process stdout/stderr is omitted from appended public evidence. Its exact original hash remains in the unchanged complete output seal; authored result/execution receipts retain the historical scope.'});continue
        q=PUB/'support/history/reviews/package_02'/p.name;copy(p,q)
        copies.append({'original_path':p.relative_to(AUDIT).as_posix(),'package_path':q.relative_to(PUB).as_posix(),'bytes':r['bytes'],'sha256':r['sha256']})
    p=AUDIT/'ROOT_WHOLE_PACKAGE_REVIEW_02.json';q=PUB/'support/history'/p.name;copy(p,q);r=rec(q,PUB);copies.append({'original_path':p.name,'package_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256']})
    save(PUB/'support/TERMINAL_COPY_MAP.json',{'utc':UTC,'unchanged_authored_review_root_copies':copies,'individual_omitted_sealed_outputs':omitted,'complete_seals_unchanged_and_historical_referents_not_retargeted':True,'private_raw_render_extracted_env_duplicate_archives_not_copied':True})
    save(PUB/'support/TERMINAL_SOURCE_EXCLUSION_LEDGER.json',{'utc':UTC,'individual_omitted_sealed_outputs':omitted,'policy':'Only safe top-level authored whole02 records, complete OUTPUT_PINS/REVIEW_SEAL and root adoption appended. Ignored compiler/raster/clean extraction/private primary body trees remain excluded, represented by their unchanged authored receipts. Process outputs and diff/control files are individually omitted. Pins identify historical referents, not inclusion promises.','omitted_tree_categories':['private source bodies','full extracts','page renders','environments','raw process/scratch trees','duplicate ZIP/PDF baselines']})
    updated=json.loads(json.dumps(oldmap));updated['copies']+=copies;updated['terminal_append_utc']=UTC;save(PUB/'support/COPY_MAP.json',updated)
    return copies,omitted
GUARD='''"""Explicit accepted whole02 terminal guard; no assertions or external dependencies."""
import hashlib,json
def require(ok,message):
    if not ok:raise ValueError(message)
def verify_terminal(root):
    def get(name):return (root/name).read_bytes()
    def check(row):
        data=get(row['path']);require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'protected reviewed payload changed: '+row['path'])
    state=json.loads(get('CURRENT_REVIEW_STATE.json'));accepted=json.loads(get('support/FINAL_ACCEPTANCE.json'))
    require(state['stage']=='TERMINAL_ACCEPTED_WHOLE02_ADMINISTRATION' and state['publication_ready'] is True and state['all_issues_resolved'] is True and state['published'] is False and state['fresh_whole_package_reviews']==2,'terminal ready state required')
    require(accepted['publication_ready'] is True and accepted['published'] is False and accepted['fresh_whole_package_reviews']==2 and accepted['actionable_issues']==[],'terminal acceptance differs')
    check(accepted['root_adoption_pin'])
    adoption=json.loads(get('support/history/ROOT_WHOLE_PACKAGE_REVIEW_02.json'))
    require(adoption['status']=='ADOPT_ZERO_ACTIONABLE_WHOLE02_PENDING_TERMINAL_ADMIN_SEAL' and adoption['root_entire_report_and_verdict_read'] is True and adoption['root_independent_derivation_and_source_interface_read'] is True and adoption['mathematics_accepted_unchanged'] is True and adoption['fresh_whole_package_reviews']==2,'root full exact whole02 adoption required')
    prefix='support/history/reviews/package_02/'
    verdict=json.loads(get(prefix+'VERDICT.json'))
    require(verdict['verdict']=='ACCEPT_SCOPED_WHOLE_PACKAGE' and verdict['finding_counts']=={'P0':0,'P1':0,'P2':0,'P3':0} and verdict['required_corrections']==[] and verdict['historical_P3_01_exact_implementation_verified'] is True,'terminal whole02 must have zero actionable P0-P3')
    for name,field in [('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('OUTPUT_PINS.json','output_pins_sha256'),('REVIEW_SEAL.json','review_seal_sha256')]:
        require(hashlib.sha256(get(prefix+name)).hexdigest()==adoption[field],'root-adopted whole02 record differs: '+name)
    seal=json.loads(get(prefix+'REVIEW_SEAL.json'))
    require(seal['terminal_verdict']=='ACCEPT_SCOPED_WHOLE_PACKAGE' and all(seal[n]==0 for n in ['P0','P1','P2','P3']),'terminal review seal not zero')
    for name,field in [('INPUT_PINS.json','input_manifest_sha256'),('OUTPUT_PINS.json','output_manifest_sha256'),('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('FROZEN_DERIVATION.md','frozen_derivation_sha256')]:
        require(hashlib.sha256(get(prefix+name)).hexdigest()==seal[field],'terminal review seal hash mismatch: '+name)
    for row in accepted['protected_package_inputs']:check(row)
    for row in accepted['protected_external_inputs']:
        if (root/row['path']).exists():check(row)
    originals=json.loads(get('support/history/SUBMITTED_PINS.json'))['files'];require(len(originals)==8,'original eight required')
    for row in originals:check({'path':'support/history/'+row['snapshot_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    mapping=json.loads(get('support/COPY_MAP.json'))['copies'];require(len(mapping)==accepted['copy_count'],'terminal copy coverage changed')
    for row in mapping:check({'path':row['package_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    metadata=json.loads(get('.zenodo.json'))
    require(metadata==json.loads(get('metadata.json'))['metadata'],'bibliographic metadata equality changed')
    require(hashlib.sha256(json.dumps(metadata,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==accepted['metadata_object_sha256'],'protected bibliographic metadata object changed')
    if (root/'zenodo-deposit.json').exists():require(json.loads(get('zenodo-deposit.json'))['metadata']==metadata,'external bibliographic metadata differs')
    allow=json.loads(get('SUPPORT_ALLOWLIST.json'))['members'];pins=json.loads(get('TERMINAL_INPUT_PINS.json'))
    rows=[]
    for name in sorted(allow):
        if name in {'SUPPORT_MANIFEST.json','TERMINAL_INPUT_PINS.json'}:continue
        data=get(name);rows.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    require(pins['schema']=='pr1052-terminal-input-pins-v1' and pins['self_excluded'] is True and pins['files']==rows,'terminal input pin mismatch')
'''
def administer(copies,metadata):
    objectsha=hashlib.sha256(json.dumps(metadata,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    save(PUB/'CURRENT_REVIEW_STATE.json',{'utc':UTC,'stage':'TERMINAL_ACCEPTED_WHOLE02_ADMINISTRATION','publication_ready':True,'all_issues_resolved':True,'published':False,'fresh_whole_package_reviews':2,'actionable_issue_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'historical_whole01_verdict':'P3-01 retained unchanged; corrected repair verified by full whole02','metadata_json_remains_exact_dated_pending_repair_snapshot':True,'root_final_administrative_verification_pending':True,'services_hold':'BLOCKED BY PRECEDING PR1032 PRIORITY CURSOR','acceptance':'support/FINAL_ACCEPTANCE.json'})
    save(PUB/'support/FINAL_ACCEPTANCE.json',{'utc':UTC,'pr':1052,'fresh_whole_package_reviews':2,'publication_ready':True,'all_issues_resolved':True,'published':False,'actionable_issues':[],'root_adoption_pin':rec(PUB/'support/history/ROOT_WHOLE_PACKAGE_REVIEW_02.json',PUB),'protected_package_inputs':[rec(PUB/n,PUB) for n in PROTECTED],'metadata_object_sha256':objectsha,'copy_count':99+len(copies),'first_whole_P3_history_not_relabelled_clean':True,'dated_notes_P3_repair_verified_by_full_whole02':True,'bibliographic_metadata_three_objects_unchanged':True,'root_final_administrative_verification_pending':True,'services_hold':'BLOCKED BY PRECEDING PR1032 PRIORITY CURSOR','novelty_exact_priority':'UNKNOWN','human_peer_review':False,'formal_certification':False})
    text=(PUB/'README.md').read_text();start=text.index('The draft upload metadata is identical');end=text.index('\n\nThe unchanged first review',start)
    text=text[:start]+"The bibliographic upload metadata remains identical in `.zenodo.json`, `metadata.json`'s `metadata` object and external `zenodo-deposit.json`. Their exact repaired dated notes are unchanged. The `metadata.json` false readiness/pending whole02 fields describe its frozen 2026-10-14 repair snapshot and are retained as historical input values. Current operational readiness is separately recorded in `CURRENT_REVIEW_STATE.json`: true, all issues resolved, published false. The root has adopted the complete new whole02 report/verdict/derivation/source-interface reconstruction with zero actionable P0–P3 findings. The first whole review's P3-01 remains unchanged history; its precise repair was verified by whole02. Two comprehensive reviews now meet the minimum. Parent root final administrative verification/adoption is pending; publication services remain blocked at preceding PR1032. The external descriptor preserves the exact bibliographic metadata and PDF binding; only its ZIP delivery size/digest advances to this administrative archive. It remains external to avoid a self-reference and is fully checked whenever present."+text[end:]
    text+='\nTerminal administrative append, 14 October 2026: unchanged safe whole02 records, complete OUTPUT_PINS/REVIEW_SEAL and root adoption are copied under `support/history/`. `support/TERMINAL_COPY_MAP.json` and `support/TERMINAL_SOURCE_EXCLUSION_LEDGER.json` describe every copied/omitted sealed output. All 99 prior copy entries and bytes remain exact. Original 91 preparation pins, repaired 134 current pins and all 30 repair outputs retain their historical bytes; `support/TERMINAL_HISTORICAL_PIN_RESOLUTION.json` resolves every old hash to its exact unchanged or preserved before bytes. `TERMINAL_INPUT_PINS.json` separately freezes current allowlisted inputs except itself/generated manifest; the manifest hashes these pins without a self-cycle. All paper/PDF/source/checker and metadata bytes remain unchanged. The prior actual compilation and four-page review apply to the same PDF; no new compiler/render/marker is needed for administrative verification.\n';(PUB/'README.md').write_text(text)
    with (PUB/'support/HISTORY.md').open('a') as out:out.write('\n## Terminal administration, 14 October 2026\n\nThe earlier preparation and repaired pending paragraphs above retain their exact dated meanings. Two complete whole-package reviews are now finished; first-review P3-01 is immutable history, and the second complete review independently verified its exact repair and the full package with zero actionable P0–P3. Current readiness is true, all issues resolved, published false, recorded in ../../CURRENT_REVIEW_STATE.json and ../FINAL_ACCEPTANCE.json. Parent final administrative adoption is pending, and services are blocked at preceding PR1032. Only unchanged safe authored whole02/root records and administration were appended. The paper/PDF, all bibliographic metadata, original eight, old checker/source/report bodies, all 99 earlier copies, both old pin stages and 30 repair outputs are unchanged. Before-terminal administration and new historical pin resolutions explicitly preserve every old byte target; no old pin or verdict was retargeted or relabelled clean.\n')
    with (PUB/'RESEARCH_LOG.md').open('a') as out:out.write(f'\n{UTC}: 65% of bounded terminal administration. Full whole02 root adoption is recorded separately; first P3 history and dated notes remain exact. Ready true/published false in distinct CURRENT_REVIEW_STATE, parent final verification pending, services held at preceding PR1032. Paper/PDF/metadata/checkers and prior pin stages/copies unchanged; external descriptor changes only ZIP delivery binding.\n')
    (PUB/'terminal_stage.py').write_text(GUARD)
    verifier=PUB/'verify_support.py';source=verifier.read_text();anchor="    verify_metadata()\n    mapping = json.loads((ROOT/'support/COPY_MAP.json').read_text())['copies']"
    require(source.count(anchor)==1,'verifier anchor differs')
    loader="""    verify_metadata()  # Exact immutable dated repair metadata remains checked.
    import importlib.util
    spec = importlib.util.spec_from_file_location('pr1052_terminal_stage', ROOT/'terminal_stage.py')
    terminal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(terminal)
    terminal.verify_terminal(ROOT)
    mapping = json.loads((ROOT/'support/COPY_MAP.json').read_text())['copies']"""
    verifier.write_text(source.replace(anchor,loader))
def history_pins(before):
    table={r['path']:r for r in before};mutable={'preprint_v1_0/'+n for n in MUTABLE};rows=[]
    oldloc=json.loads((PUB/'support/history/preparation_01/OUTPUT_PIN_LOCATIONS.json').read_text())['files']
    for stage,records in [('original_preparation91',oldloc),('repaired_pending134',json.loads((PUB/'CURRENT_OUTPUT_PINS.json').read_text())['files'])]:
        require(len(records)==(91 if stage=='original_preparation91' else 134),'historical stage count')
        for r in records:
            logical=r['path'];existing=(AUDIT/r['before_bytes_path_relative_to_audit']) if stage=='original_preparation91' else PUB/logical
            expected={'bytes':r['bytes'],'sha256':r['sha256']}
            if existing.relative_to(AUDIT).as_posix() in mutable:
                # These paths will advance after this ledger is authored, so
                # bind their exact frozen before bytes even if current bytes
                # still match at this instant.
                resolved=HERE/'frozen_before'/existing.relative_to(AUDIT);checkrow(resolved,r)
                public=PUB/'support/history/before_terminal_admin_20261014'/existing.relative_to(PUB)
                if public.exists() and public.stat().st_size==r['bytes'] and sha(public)==r['sha256']:resolved=public
            elif existing.exists() and existing.stat().st_size==r['bytes'] and sha(existing)==r['sha256']:
                resolved=existing
            else:
                require(existing.relative_to(AUDIT).as_posix() in mutable,'historical target lacks authorized before bytes')
                resolved=HERE/'frozen_before'/existing.relative_to(AUDIT);checkrow(resolved,r)
                public=PUB/'support/history/before_terminal_admin_20261014'/existing.relative_to(PUB)
                if public.exists() and public.stat().st_size==r['bytes'] and sha(public)==r['sha256']:resolved=public
            checkrow(resolved,r)
            rows.append({'stage':stage,'historical_path':logical,**expected,'resolved_before_bytes_audit_relative':resolved.relative_to(AUDIT).as_posix(),'available_in_distributed_archive':resolved.is_relative_to(PUB) and resolved.name not in {'OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json','pr1052_support_v1_0.zip','pr1052_support_v1_0.zip.sha256'},'old_hash_target_not_reinterpreted':True})
    save(PUB/'support/TERMINAL_HISTORICAL_PIN_RESOLUTION.json',{'utc':UTC,'files':rows,'original_pin_files_unchanged':True,'91_and_134_all_exact_before_byte_resolutions':True,'old30_repair_outputs_unchanged':'repairs/package01/OUTPUT_PINS.json and entire source tree remain protected baseline'})
    return rows
def generate():
    allow=json.loads((PUB/'SUPPORT_ALLOWLIST.json').read_text());added=[p.relative_to(PUB).as_posix() for p in PUB.rglob('*') if p.is_file() and ('before_terminal_admin_20261014' in p.parts or 'package_02' in p.parts or p.name in {'CURRENT_REVIEW_STATE.json','terminal_stage.py','TERMINAL_COPY_MAP.json','TERMINAL_SOURCE_EXCLUSION_LEDGER.json','TERMINAL_HISTORICAL_PIN_RESOLUTION.json','FINAL_ACCEPTANCE.json','ROOT_WHOLE_PACKAGE_REVIEW_02.json'})]
    allow['members']=sorted(set(allow['members']+added+['TERMINAL_INPUT_PINS.json']));allow['terminal_append_utc']=UTC;save(PUB/'SUPPORT_ALLOWLIST.json',allow)
    save(PUB/'TERMINAL_INPUT_PINS.json',{'schema':'pr1052-terminal-input-pins-v1','utc':UTC,'self_excluded':True,'files':[rec(PUB/n,PUB) for n in allow['members'] if n not in {'SUPPORT_MANIFEST.json','TERMINAL_INPUT_PINS.json'}],'scope':'Current explicit payload except own pins/generated manifest; old 91/134 pin files remain exact separate history.'})
    manifest=json.loads((PUB/'SUPPORT_MANIFEST.json').read_text());manifest['members']=allow['members'];manifest['entries']=[rec(PUB/n,PUB) for n in allow['members'] if n!='SUPPORT_MANIFEST.json'];manifest['terminal_administration_utc']=UTC;manifest['publication_ready']=True;manifest['published']=False;manifest['services_hold']='preceding PR1032 priority cursor';save(PUB/'SUPPORT_MANIFEST.json',manifest)
    run('CURRENT_BUILD',[sys.executable,'-I','-B','build_support.py'],PUB)
    descriptor=json.loads((PUB/'zenodo-deposit.json').read_text());require(descriptor['files'][0]['filename']=='paper.pdf' and descriptor['files'][1]['filename']==ARCHIVE.name,'delivery names')
    descriptor['files'][1]['bytes']=ARCHIVE.stat().st_size;descriptor['files'][1]['sha256']=sha(ARCHIVE);save(PUB/'zenodo-deposit.json',descriptor)
def archive_verify():
    allow=json.loads((PUB/'SUPPORT_ALLOWLIST.json').read_text())['members'];manifest=json.loads((PUB/'SUPPORT_MANIFEST.json').read_text());require(manifest['members']==sorted(allow),'manifest coverage')
    for r in manifest['entries']:checkrow(PUB/r['path'],r)
    names=sorted(allow);read=[];independent=io.BytesIO()
    with zipfile.ZipFile(ARCHIVE) as z,zipfile.ZipFile(independent,'w',compression=zipfile.ZIP_STORED) as rebuilt:
        require(z.namelist()==names and len(names)==len({n.casefold() for n in names}) and z.testzip() is None,'ZIP membership/CRC')
        for info in z.infolist():
            n=info.filename;p=PurePosixPath(n);require(n.isascii() and not p.is_absolute() and '..' not in p.parts and '\\' not in n and info.external_attr>>16==0o100644 and info.date_time==(2026,10,14,0,0,0) and info.compress_type==zipfile.ZIP_STORED,'ZIP safe headers')
            require(not any(x.lower() in {'raw','private','private_raw','render','rendered','__pycache__','.venv','scratch','clean_extraction'} for x in p.parts) and not n.endswith(('.zip','.png','.pyc')) and (not n.endswith('.pdf') or n=='paper.pdf'),'body exclusion')
            data=(PUB/n).read_bytes();require(z.read(n)==data,'ZIP current payload differs')
            if n!='paper.pdf':
                s=data.decode('utf-8')
                if n.endswith('.json'):json.loads(s)
                if n.endswith('.py'):ast.parse(s)
            zi=zipfile.ZipInfo(n,(2026,10,14,0,0,0));zi.create_system=3;zi.external_attr=0o100644<<16;zi.compress_type=zipfile.ZIP_STORED;rebuilt.writestr(zi,data);read.append(rec(PUB/n,PUB))
    require(independent.getvalue()==ARCHIVE.read_bytes(),'closed independent reconstruction differs')
    save(HERE/'ARCHIVE_MEMBER_READ_RECEIPTS.json',{'files':read,'all_CRC_header_member_disk_bytes_checked':True,'UTF8_JSON_Python_read':True,'only_existing_authored_paper_PDF_binary':True,'closed_independent_rebuild_byte_exact':True})
    return len(names),len(manifest['entries'])
def extraction():
    root=HERE/'scratch';require(not root.exists(),'scratch already exists');root.mkdir()
    with zipfile.ZipFile(ARCHIVE) as z:z.extractall(root)
    return root
def reproduction():
    root=extraction()
    run('README_VERIFY',[sys.executable,'-I','-B','verify_support.py'],root)
    run('README_CHECKS',[sys.executable,'-I','-B','run_checks.py','--output','_runs/fresh.json'],root)
    run('README_INTEGRITY',[sys.executable,'-I','-B','test_integrity.py','--output','_runs/integrity.json'],root)
    run('README_BUILD',[sys.executable,'-I','-B','build_support.py','--output','_runs/rebuilt.zip'],root)
    require((root/'_runs/rebuilt.zip').read_bytes()==ARCHIVE.read_bytes(),'documented closed rebuild differs')
    run('README_ARCHIVE_VERIFY',[sys.executable,'-I','-B','verify_support.py','--archive','_runs/rebuilt.zip'],root)
    for optimized in [False,True]:
        flags=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
        run('WRAPPED_VERIFY_'+str(int(optimized)),flags+['verify_support.py','--archive',ARCHIVE.name],PUB)
        run('EXTRACTED_VERIFY_'+str(int(optimized)),flags+['verify_support.py','--archive','_runs/rebuilt.zip'],root)
        run('EXTRACTED_BUILD_'+str(int(optimized)),flags+['build_support.py','--output','_runs/rebuilt.zip'],root)
        require((root/'_runs/rebuilt.zip').read_bytes()==ARCHIVE.read_bytes(),'normal/optimized rebuild differs')
    fresh=json.loads((root/'_runs/fresh.json').read_text());old=json.loads((PUB/'verification/FRESH_RUN.json').read_text());require(fresh['all_checks_passed'] and len(fresh['runs'])==5,'fresh checker executions')
    require([(r['family'],r['optimization'],r['source_sha256'],r['results']) for r in fresh['runs']]==[(r['family'],r['optimization'],r['source_sha256'],r['results']) for r in old['runs']],'full family results differ')
    save(HERE/'DOCUMENTED_FRESH_RESULTS.json',fresh);save(HERE/'DOCUMENTED_INTEGRITY_RESULTS.json',json.loads((root/'_runs/integrity.json').read_text()));shutil.rmtree(root)
    return {'five_documented_support_commands_actual_exit_zero':True,'fresh_five_checker_results_exact_substantive_projection':True,'strict_actual_descriptor_metadata_PDF_ZIP_bindings_normal_optimized':True,'normal_optimized_extracted_verify_build_byte_identical':True,'compile_not_repeated':'Paper/PDF unchanged; prior preparation/full-review compilation and four-page receipts are inherited exactly; no compile/render/marker in administration.'}
def controls():
    results=[]
    for name in ['ready_false','nonzero_whole02','wrong_report','wrong_seal','changed_paper','changed_metadata','changed_original','input_pin','wrong_delivery_binding']:
        root=extraction()
        if name=='ready_false':p=root/'CURRENT_REVIEW_STATE.json';d=json.loads(p.read_text());d['publication_ready']=False;save(p,d);expected='terminal ready state required'
        elif name=='nonzero_whole02':p=root/'support/history/reviews/package_02/VERDICT.json';d=json.loads(p.read_text());d['finding_counts']['P3']=1;save(p,d);expected='terminal whole02 must have zero actionable'
        elif name in {'wrong_report','wrong_seal'}:
            p=root/'support/history/reviews/package_02'/('REPORT.md' if name=='wrong_report' else 'REVIEW_SEAL.json');p.write_bytes(p.read_bytes()+b'\n ');expected='root-adopted whole02 record differs'
        elif name in {'changed_paper','changed_metadata','changed_original'}:
            original=json.loads((root/'support/history/SUBMITTED_PINS.json').read_text())['files'][0]['snapshot_path']
            p=root/('paper.tex' if name=='changed_paper' else '.zenodo.json' if name=='changed_metadata' else 'support/history/'+original);p.write_bytes(p.read_bytes()+b'\n ');expected='protected reviewed payload changed'
        elif name=='input_pin':p=root/'LICENSE.txt';p.write_bytes(p.read_bytes()+b'\nScratch mutation.\n');expected='terminal input pin mismatch'
        else:
            copy(PUB/'zenodo-deposit.json',root/'zenodo-deposit.json');copy(ARCHIVE,root/ARCHIVE.name);copy(Path(str(ARCHIVE)+'.sha256'),root/(ARCHIVE.name+'.sha256'));p=root/'zenodo-deposit.json';d=json.loads(p.read_text());d['files'][1]['sha256']='0'*64;save(p,d);expected='upload file binding mismatch'
        mapping=json.loads((root/'support/COPY_MAP.json').read_text())
        for r in mapping['copies']:
            if r['package_path']==p.relative_to(root).as_posix():r['bytes']=p.stat().st_size;r['sha256']=sha(p)
        save(root/'support/COPY_MAP.json',mapping)
        allow=json.loads((root/'SUPPORT_ALLOWLIST.json').read_text())['members']
        if name!='input_pin':
            pins=json.loads((root/'TERMINAL_INPUT_PINS.json').read_text());pins['files']=[rec(root/n,root) for n in sorted(allow) if n not in {'SUPPORT_MANIFEST.json','TERMINAL_INPUT_PINS.json'}];save(root/'TERMINAL_INPUT_PINS.json',pins)
        manifest=json.loads((root/'SUPPORT_MANIFEST.json').read_text());manifest['entries']=[rec(root/n,root) for n in sorted(allow) if n!='SUPPORT_MANIFEST.json'];save(root/'SUPPORT_MANIFEST.json',manifest)
        for optimized in [False,True]:
            flags=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
            r=run('FAULT_VERIFY_'+name+'_'+str(int(optimized)),flags+['verify_support.py'],root,False);require(expected in r.stderr.decode(),'control missed intended verifier guard '+name)
            if name!='wrong_delivery_binding':
                r=run('FAULT_BUILD_'+name+'_'+str(int(optimized)),flags+['build_support.py','--output','_runs/fault.zip'],root,False);require(expected in r.stderr.decode(),'control missed intended builder guard '+name)
                require(not (root/'_runs/fault.zip').exists(),'failed semantic builder created archive')
        results.append({'control':name,'intended_guard':expected,'normal_optimized_verifier_rejection':True,'normal_optimized_builder_rejection':name!='wrong_delivery_binding','outer_manifest_copy_map_and_pins_coherently_refreshed':name!='input_pin','builder_produces_no_archive_on_rejection':name!='wrong_delivery_binding'});shutil.rmtree(root)
    return results
def final_verify(before,oldmap,metadata,resolutions):
    mutable={'preprint_v1_0/'+n for n in MUTABLE}
    for r in before:
        if r['path'] not in mutable:checkrow(AUDIT/r['path'],r)
    current=json.loads((PUB/'support/COPY_MAP.json').read_text())['copies'];require(current[:99]==oldmap['copies'],'old copy rows altered')
    for r in current:checkrow(PUB/r['package_path'],r);require((PUB/r['package_path']).read_bytes()==(AUDIT/r.get('source_snapshot',r['original_path'])).read_bytes(),'copied source differs')
    for r in resolutions:checkrow(AUDIT/r['resolved_before_bytes_audit_relative'],r)
    require(json.loads((PUB/'.zenodo.json').read_text())==metadata and json.loads((PUB/'metadata.json').read_text())['metadata']==metadata and json.loads((PUB/'zenodo-deposit.json').read_text())['metadata']==metadata,'metadata objects changed')
    oldd=json.loads((HERE/'frozen_before/preprint_v1_0/zenodo-deposit.json').read_text());newd=json.loads((PUB/'zenodo-deposit.json').read_text());require(oldd['metadata']==newd['metadata'] and oldd['files'][0]==newd['files'][0] and oldd['files'][1]['filename']==newd['files'][1]['filename'],'descriptor beyond ZIP binding altered')
    return len(current)
def finish(before,copies,omitted,resolutions,members,payloads,repro,faults):
    after=inventory();b={r['path']:r for r in before};a={r['path']:r for r in after};require(set(b)<=set(a),'old input removed')
    changed=[{'path':n,'before':b[n],'after':a[n]} for n in sorted(b) if b[n]!=a[n]];require({r['path'] for r in changed}<={'preprint_v1_0/'+n for n in MUTABLE},'unwhitelisted change')
    added=[r for r in after if r['path'] not in b];require(all(r['path'].startswith('preprint_v1_0/') for r in added),'out-of-scope append')
    save(HERE/'CHANGE_INVENTORY.json',{'utc':UTC,'allowed_existing_mutations':['preprint_v1_0/'+n for n in MUTABLE],'changed_existing_files':changed,'appended_files':added,'all_math_PDF_metadata_checker_original_report_old_pins_copy_records_protected':True,'external_descriptor_only_ZIP_file_binding_changed':True})
    diffs=[]
    for r in changed:
        p=AUDIT/r['path'];q=HERE/'frozen_before'/r['path']
        if p.suffix!='.zip':diffs.extend(difflib.unified_diff(q.read_text().splitlines(True),p.read_text().splitlines(True),fromfile='before/'+r['path'],tofile='after/'+r['path']))
    for r in added:
        p=AUDIT/r['path'];diffs.extend(difflib.unified_diff([],p.read_text().splitlines(True),fromfile='/dev/null',tofile='added/'+r['path']))
    (HERE/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(diffs))
    save(HERE/'REPRODUCTION_AND_FAULT_RECEIPTS.json',{'utc':UTC,'reproduction':repro,'targeted_semantic_controls':faults,'actual_processes':RUNS,'one_scratch_tree_at_a_time_removed_after_receipts':True})
    save(HERE/'FINAL_INTEGRITY.json',{'utc':UTC,'pr':1052,'status':'PASS_PENDING_PARENT_ROOT_ADOPTION','archive':rec(ARCHIVE),'sidecar':rec(Path(str(ARCHIVE)+'.sha256')),'external_delivery_descriptor':rec(PUB/'zenodo-deposit.json'),'members':members,'hashed_payloads':payloads,'old_99_copy_records_exact':True,'terminal_copy_count':len(copies),'individual_omissions':len(omitted),'original91_repaired134_exact_resolutions':len(resolutions),'all30_repair_outputs_unchanged':True,'whole01_P3_history_unchanged_not_relabelled':True,'protected':[rec(PUB/n) for n in PROTECTED],'every_CRC_member_safe_header_disk_byte_and_UTF8_body_checked':True,'independent_closed_archive_byte_exact':True,'documented_clean_rebuild_byte_exact':True,'normal_optimized_terminal_guards':True,'bibliographic_metadata_all_three_objects_exact_unchanged':True,'compiler_render_marker':False,'services_hold':'preceding PR1032 priority cursor'})
    save(HERE/'FINAL_SEAL.json',{'utc':UTC,'pr':1052,'status':'PROPOSED_TERMINAL_SEAL_PENDING_PARENT_ROOT_ADOPTION','publication_ready':True,'all_issues_resolved':True,'published':False,'fresh_whole_package_reviews':2,'actionable_issues':[],'archive':rec(ARCHIVE),'descriptor':rec(PUB/'zenodo-deposit.json'),'protected':[rec(PUB/n) for n in PROTECTED],'integrity':rec(HERE/'FINAL_INTEGRITY.json'),'root_final_administrative_adoption_required':True,'services_hold':'BLOCKED BY PRECEDING PR1032 PRIORITY CURSOR','postreview_scope':'Unchanged authored whole02/root records and terminal administration only; descriptor ZIP binding updated without bibliographic metadata change.'})
    checkpoint(95,'All pre-existing nonwhitelisted bytes, all old/source copies, 91+134 historical byte resolutions and 30 repair outputs rechecked unchanged. Documented support commands and strict wrapped/extracted normal/-O verification passed; targeted semantic controls hit intended guards after coherent scratch refresh. Independent closed archive rebuild byte-exact. Parent final administrative adoption remains; no compiler/render/marker, Git/services or outreach.')
    (HERE/'FINALIZATION_REPORT.md').write_text(f'''# PR1052 terminal administrative finalization

PASS, pending parent root administrative verification/adoption. Root had fully read and adopted complete whole02 report, verdict, independent frozen derivation and source-interface reconstruction with zero actionable P0–P3. Two complete reviews meet the minimum; the first review/root P3-01 observation remains exact historical evidence and is not relabelled clean. Whole02 independently verified the precise dated repair and the full package.

Final archive `{ARCHIVE.relative_to(AUDIT)}`: {ARCHIVE.stat().st_size} bytes, SHA-256 `{sha(ARCHIVE)}`, {members} members / {payloads} manifest-hashed payloads. Sorted stored ZIP, fixed 14 October timestamp, regular0644, all CRC/header/name/current-member bytes checked. The CLOSED archive was independently reconstructed without importing the package builder/verifier and matched every byte. Current payload remains one unchanged authored paper PDF plus UTF8 authored support; JSON/Python bodies were parsed. Raw/source/private/full extracts/renders/environments/process trees and duplicate ZIP/PDF baselines remain excluded.

Readiness and all issues resolved are true; published is false. Services remain **BLOCKED at preceding PR1032 priority cursor**. Parent final administrative adoption is pending. Proposed FINAL_SEAL/FINAL_INTEGRITY are external to the ZIP and avoid a self-reference. The separate CURRENT_REVIEW_STATE records current readiness. The unchanged metadata.json false/pending fields retain their exact dated repair-stage meanings; no bibliographic metadata was rewritten to advance administration.

All {len(before)} immediate pre-existing audit files are hash-frozen in INPUT_PINS. Protected paper.tex/PDF, all three exact bibliographic metadata objects with dated notes, original eight files, mathematical/source/checker code/reports, all 99 previous copied record entries/bytes, original91/repaired134 pin manifests and all30 repair outputs remain unchanged. Mutable before bytes are in ignored frozen_before; safe before administration is in support/history/before_terminal_admin_20261014. New terminal historical resolution verifies all225 old hashes against exact current or preserved before bytes; old pin fields/stages were not retargeted. Existing source_snapshot records continue resolving through their original repair custody.

{len(copies)} unchanged safe authored whole02/output-pin/seal/root records were copied; {len(omitted)} sealed control/diff/process outputs were individually omitted with exact hash/reason. Complete original output pins and REVIEW_SEAL are copied unchanged and still identify omitted/private historical referents honestly. The copy map prefix of99 entries remains exact, and every current copy equals its original_path/source_snapshot bytes.

Only necessary current administrative state/acceptance/history/README/copy inventory, verifier loading of an explicit accepted-zero whole02 guard, and noncircular current pins/manifest/ZIP bindings changed. The builder itself and all checkers remain unchanged; it already delegates strict payload checks to the verifier. New terminal input pins exclude only themselves/generated manifest. All three bibliographic metadata objects, .zenodo.json and metadata.json whole-file bytes remain exact. External zenodo-deposit.json changes only the current ZIP delivery size/hash; its metadata value, PDF binding and filenames stay exact. COMPLETE_CODE_PROSE_DIFF.patch supplies every changed/appended text diff; CHANGE_INVENTORY lists all byte hashes including binary ZIP.

Actual clean extraction ran all five documented support commands, reproduced the five family/mode results under the declared exact/substantive comparison, rejected21 integrity controls, rebuilt the exact ZIP, and verified it. Strict actual descriptor-present verification binds the current unchanged PDF and new ZIP normally and under -O; extracted descriptor absence is separately valid. Normal/optimized extracted verifier and builder pass. {len(faults)} new targeted controls reject normally and under -O after coherent outer manifest/copy-map/pin refresh where applicable; failed semantic builders produce no archive. One small own scratch tree was used at a time and removed after receipts. Exact argv/timing/streams/results are in the reproduction receipts. The primary historical checker remains ordinary-assertion mode; its runner explicitly invokes it normally and retains other declared optimized scopes.

No compilation, render or operation marker was performed. Prior actual standalone compilation and four-page review bind the same preserved source/PDF and are inherited explicitly. This effort is administration/reproduction, not a new mathematical/source review or novelty finding. No Git/index/branch/remote, upload/DOI/release/PR/GWS/tracker/service or outreach action occurred; only PR1052 was touched. Completion estimate95%, remaining5% is parent root final verification/adoption.
''')
    outputs=[rec(p,HERE) for p in sorted(HERE.rglob('*')) if p.is_file() and 'frozen_before' not in p.relative_to(HERE).parts and 'scratch' not in p.relative_to(HERE).parts and p.name!='OUTPUT_PINS.json']
    save(HERE/'OUTPUT_PINS.json',{'utc':UTC,'self_excluded':True,'files':outputs,'current_audit_payload_files':after,'frozen_before_bound_by_INPUT_PINS_and_historical_resolution':True,'no_scratch_left':True,'proposed_root_adoption_pending':True,'no_late_writes_after_seal':True})
    print(json.dumps({'pr':1052,'archive':rec(ARCHIVE),'members':members,'payloads':payloads,'before_files':len(before),'changed_existing':len(changed),'appended':len(added),'terminal_copies':len(copies),'omissions':len(omitted),'history_resolutions':len(resolutions),'controls':len(faults),'processes':len(RUNS),'status':'PASS_PENDING_PARENT_ROOT_ADOPTION'}))
def main():
    if (HERE/'INPUT_PINS.json').exists():
        require(not (HERE/'OUTPUT_PINS.json').exists(),'final administration already sealed')
        before=json.loads((HERE/'INPUT_PINS.json').read_text())['files'];base=json.loads((HERE/'FROZEN_BASELINE.json').read_text());metadata=base['metadata_object'];oldmap={'copies':base['old_99_copy_records']}
        mapping=json.loads((PUB/'support/TERMINAL_COPY_MAP.json').read_text());copies,omitted=mapping['unchanged_authored_review_root_copies'],mapping['individual_omitted_sealed_outputs']
        resolutions=history_pins(before)
        accepted=json.loads((PUB/'support/FINAL_ACCEPTANCE.json').read_text());external={'paper.pdf.sha256','OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json'}
        rows=accepted['protected_package_inputs'];accepted['protected_package_inputs']=[r for r in rows if r['path'] not in external];accepted['protected_external_inputs']=accepted.get('protected_external_inputs',[])+[r for r in rows if r['path'] in external];save(PUB/'support/FINAL_ACCEPTANCE.json',accepted)
        (PUB/'terminal_stage.py').write_text(GUARD)
        checkpoint(70,'First clean extraction exposed that three protected external sidecars (PDF SHA and original91/repaired134 pin manifests) are intentionally outside the established archive. Corrected only new guard/acceptance administration to distinguish those explicit external protected inputs: checked whenever present, globally frozen/rehashed unchanged, and not required in a clean extraction. Paper/source/metadata and original verifier controls unchanged. First admin attempt records preserved locally.')
        checkpoint(80,'Completed reproduction and all nine semantic controls passed before final historical resolution recheck found a mutable-path locator that was authored before regeneration. Corrected only the new terminal resolution ledger to point mutable paths directly to exact preserved before bytes, irrespective of interim current equality. Old91/repaired134 manifests and every historical byte remain unchanged. Rebuilding current bindings and rerunning documented checks for this final corrected ledger.')
    else:
        rows,oldmap,metadata,before=freeze();copies,omitted=append_review(rows,oldmap);administer(copies,metadata);resolutions=history_pins(before)
        accepted=json.loads((PUB/'support/FINAL_ACCEPTANCE.json').read_text());external={'paper.pdf.sha256','OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json'};rows=accepted['protected_package_inputs'];accepted['protected_package_inputs']=[r for r in rows if r['path'] not in external];accepted['protected_external_inputs']=[r for r in rows if r['path'] in external];save(PUB/'support/FINAL_ACCEPTANCE.json',accepted)
    generate();members,payloads=archive_verify();checkpoint(65,'Safe unchanged terminal records and root adoption appended; current state/guards and distinct pins bind ready administration while old metadata/pin stages retain exact meanings. Every archive member and independent closed reconstruction pass. Starting actual documented reproduction and targeted guards.')
    repro=reproduction();faults=controls();final_verify(before,oldmap,metadata,resolutions);finish(before,copies,omitted,resolutions,members,payloads,repro,faults)
if __name__=='__main__':main()
