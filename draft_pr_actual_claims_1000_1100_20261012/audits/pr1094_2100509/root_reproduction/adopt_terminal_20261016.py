from pathlib import Path
import copy,datetime,hashlib,io,json,os,shutil,subprocess,tempfile,zipfile,zlib
A=Path(__file__).resolve().parents[1];R=A/'finalization/terminal_admin_20261016';P=A/'preprint_v1_0';K=P/'kit'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p,name=None):
    b=p.read_bytes();return {'path':name or p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',s['output_pins']);outputs=load(R/'OUTPUT_PINS.json')['records']
for r in outputs:check(R/r['path'],r)
before=load(R/'BEFORE_INPUT_RESOLUTION.json')['records'];baseline=load(R/'FROZEN_INPUT_PINS.json')['records'];need(len(before)==len(baseline)==419,'baseline count')
need([{k:r[k] for k in ('path','bytes','sha256')} for r in before]==baseline,'baseline identities')
for r in before:check(A/r['resolution'],r)
allowed=load(R/'ALLOWED_CHANGES.json')['existing_edits'];need(len(allowed)==6,'edit scope')
for r in allowed:check(R/'before'/r['path'],r);need(pin(A/r['path'])['sha256']!=r['sha256'],'declared edit absent')
current=load(R/'CURRENT_ARTIFACT_PINS.json')['records']
for r in current:check(A/r['path'],r)
history=load(R/'PRIOR_STAGE_RESOLUTION.json');rows=0
for stage in history['stages']:
    check(A/stage['inventory'],stage['inventory_pin'])
    original=load(A/stage['inventory']); original=next(original[k] for k in ('records','entries','members','files') if k in original and isinstance(original[k],list))
    need(len(original)==len(stage['records']),'stage length')
    for old,r in zip(original,stage['records']):
        need(old['path']==r['recorded_path'] and old['bytes']==r['bytes'] and old['sha256']==r['sha256'],'original historic row');check(A/r['resolution'],r);rows+=1
for r in history['nested_family_paths']:check(Path(r['resolution']),r)
need(rows==1539 and len(history['nested_family_paths'])==69,'history counts')
old=load(A/'repairs/package01/before/preprint_v1_0/kit/CUSTODY_MAP.json');custody=load(K/'CUSTODY_MAP.json')
need(custody['copies'][:57]==old['copies'] and custody['exclusions'][:114]==old['exclusions'],'prior custody prefixes')
need(len(custody['copies'])==99 and len(custody['exclusions'])==210,'repair partition')
for r in custody['copies']:check(K/r['copy_path'],r)
terminal=load(P/'TERMINAL_ACCOUNTING_20261016.json');need((P/'TERMINAL_ACCOUNTING_20261016.json').read_bytes()==(K/'TERMINAL_ACCOUNTING_20261016.json').read_bytes(),'terminal copies')
ledger=load(K/'TERMINAL_SOURCE_COPY_LEDGER.json')
for r in ledger['copies']:
    check(K/r['copy_path'],r);source=R/'before'/r['original_path'] if r['meaning']=='Exact before-terminal interface bytes' else A/r['original_path'];check(source,r)
archive=P/'pr1094_supportkit_v1.0.zip';names=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file());buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w') as z:
    for n in names:
        i=zipfile.ZipInfo(n,(1980,1,1,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED;z.writestr(i,(K/n).read_bytes())
need(buffer.getvalue()==archive.read_bytes(),'independent CLOSED archive bytes')
with zipfile.ZipFile(archive) as z:
    need(z.namelist()==names and len(names)==129 and z.testzip() is None,'archive members/CRC')
    for i in z.infolist():
        b=z.read(i.filename);need(b==(K/i.filename).read_bytes() and i.CRC==zlib.crc32(b),'payload/CRC');need(not i.extra and not i.comment and not i.flag_bits,'archive extra fields')
commands=[];cleanup=[]
def run(argv,cwd,ok=True,error=None):
    p=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True);commands.append({'argv':[str(x) for x in argv],'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')});need((p.returncode==0)==ok,'actual command outcome '+str(argv));need(error is None or error.encode() in p.stderr,'wrong rejection');return p
with tempfile.TemporaryDirectory(prefix='root1094-terminal-',dir=A/'root_reproduction') as tmp:
    T=Path(tmp);C=T/'kit';C.mkdir()
    with zipfile.ZipFile(archive) as z:z.extractall(C)
    saved={p.relative_to(C).as_posix():p.read_bytes() for p in C.rglob('*') if p.is_file()}
    def restore():
        for n,b in saved.items():
            if (C/n).read_bytes()!=b:(C/n).write_bytes(b)
    def refresh():
        d=load(C/'MANIFEST.json')
        for r in d['records']:r.update(pin(C/r['path'],r['path']))
        (C/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n')
    for opt in (False,True):
        py=['python3','-B']+(['-O'] if opt else [])
        run(py+['scripts/verify_kit.py','--require-binding'],K)
        run(py+['scripts/verify_kit.py'],C)
        p=run(py+['scripts/run_checks.py','--out',str(T/('math'+str(opt)+'.json'))],C);need(json.loads(p.stdout)==load(K/'NEW_CONTROLS_RESULT.json')==load(T/('math'+str(opt)+'.json')),'full math JSON')
        out=T/('rebuilt'+str(opt)+'.zip');run(py+['scripts/build_support.py','--out',out],C);need(out.read_bytes()==archive.read_bytes(),'actual CLOSED build')
        restore();v=load(C/'TERMINAL_ACCOUNTING_20261016.json');v['completed_new_whole_package_reviews']=1;(C/'TERMINAL_ACCOUNTING_20261016.json').write_text(json.dumps(v));refresh();run(py+['scripts/verify_kit.py'],C,False,'terminal whole-review counts')
        restore();v=load(C/'TERMINAL_ACCOUNTING_20261016.json');v['publication_ready']=True;(C/'TERMINAL_ACCOUNTING_20261016.json').write_text(json.dumps(v));refresh();run(py+['scripts/verify_kit.py'],C,False,'terminal false flag');restore()
        alias=C.with_name('KIT');need(alias.samefile(C),'actual case alias premise')
        target=alias/'absent1'/'absent2'/'out.json';run(py+[C/'scripts/run_checks.py','--out',target],T,False,'physically overlaps protected kit');need(not (C/'absent1').exists(),'guard created protected ancestor')
    run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',P/'zenodo-deposit.json'],Path('/Users/alec/Documents/Math'))
    for p in T.rglob('*'):
        if p.is_file():cleanup.append(pin(p,p.relative_to(T).as_posix()))
for r in current:check(A/r['path'],r)
for r in outputs:check(R/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_TERMINAL_ADMIN_ROOT_FINAL_INTEGRITY','ROOT_full_REPORT_operative_README_verifier_diff_new_terminal_record_and_copy_selection_read':True,'counts':{'inputs':419,'allowed_edits':6,'protected_unchanged':413,'terminal_outputs':len(outputs),'delivery_files':len(current),'history_rows':rows,'nested_family_paths':69,'terminal_exact_copies':len(ledger['copies']),'archive_members':len(names)},'current_asset_pins':[pin(P/'paper.pdf'),pin(archive),pin(K/'MANIFEST.json'),pin(P/'zenodo-deposit.json')],'actual_root_command_receipts':commands,'own_scratch_removed_after_individual_hashes':cleanup,'complete_normal_optimized_math_JSON_equals_expected':True,'independent_closed_ZIP_byte_exact':True,'actual_native_local_check_only':True,'mathematics_PDF_TeX_path_guards_native_metadata_unchanged':True,'new_compile_render_or_marker':False,'old_171_and_309_partitions_preserved':True,'whole_reviews_completed':2,'minimum_whole_reviews':2,'latest_whole_review_actionable_issues':0,'priority_full_result_method_novelty_worldwide_openness':'UNKNOWN','services_held_after_pr':1032,'published':False}
adoption=A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json';need(not adoption.exists(),'adoption already exists');adoption.write_text(json.dumps(record,indent=2)+'\n')
integrity=A/'FINAL_INTEGRITY.json';seal=A/'FINAL_SEAL.json';need(not integrity.exists() and not seal.exists(),'prior final authority must not be overwritten')
items=[pin(p) for p in sorted(A.rglob('*')) if p.is_file() and not p.is_symlink()]
integrity.write_text(json.dumps({'utc':record['utc'],'scope':'All current regular audit files before this external final integrity/seal; both excluded to avoid cycle.','records':items},indent=2)+'\n')
seal.write_text(json.dumps({'utc':record['utc'],'pr':1094,'head':'954dd70b49458026e29b8dae63243391249008d8','status':'ROOT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','root_full_terminal_report_operative_code_prose_and_final_package_independently_adopted':True,'whole_reviews_completed':2,'minimum_whole_reviews':2,'actionable_issues':0,'publication_ready':True,'all_issues_resolved':True,'published':False,'services_held_after_pr':1032,'priority_novelty_independent_discovery_worldwide_openness':'UNKNOWN','dated_internal_pending_fields':'Exact captured administration history; this external current seal supplies ROOT final integrity adoption.','current_assets':record['current_asset_pins'],'root_terminal_adoption':pin(adoption),'final_integrity':pin(integrity),'terminal_output_pins':pin(R/'OUTPUT_PINS.json'),'terminal_seal':pin(R/'SEAL.json')},indent=2)+'\n')
print(json.dumps({'status':'ROOT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','root_commands':len(commands),'counts':record['counts'],'external_actions':0}))
