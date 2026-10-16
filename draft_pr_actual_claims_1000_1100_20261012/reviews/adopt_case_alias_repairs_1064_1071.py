from pathlib import Path
import datetime,hashlib,json,sys,io,zipfile,tempfile,subprocess,collections
BASE=Path(__file__).resolve().parents[1];pr=int(sys.argv[1]);A=BASE/'audits'/('pr1064_30001073' if pr==1064 else 'pr1071_30002170');P=A/('preprint_v1_0' if pr==1064 else 'NEWpreprint_v1_0');R=A/'repairs/case_alias01'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(sha(b)==r['sha256'] and ('bytes' not in r or len(b)==r['bytes']),str(p))
seal=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',seal['output_pins']);outputs=load(R/'OUTPUT_PINS.json')['entries' if pr==1064 else 'records']
for row in outputs:check(R/row['path'],row)
changes={r['path']:r for r in load(R/'CHANGE_INVENTORY.json')['modified' if pr==1064 else 'authorized_existing_changes']};baseline=load(R/('INPUT_PINS.json' if pr==1064 else 'BASELINE_INPUT_PINS.json'))['records']
for row in baseline:
    c=changes.get(row['path']);check(A/(c['preserved_path' if pr==1064 else 'before_bytes_path_relative_to_audit'] if c else row['path']),row)
    if c:check(A/row['path'],c['after'])
current=load(R/('FINAL_CURRENT_PINS.json' if pr==1064 else 'CURRENT_CANDIDATE_PINS.json'))['records']
for row in current:check(P/row['path'],row)
states=collections.Counter()
if pr==1064:
    history=load(R/'PRIOR_PIN_RESOLUTIONS.json');n_history=0
    for stage in history['manifests']:
        check(A/stage['resolved_manifest_path'],stage['manifest'])
        for row in stage['records']:
            states[row['status']]+=1;n_history+=1
            if 'resolved_path' in row:check(A/row['resolved_path'],row)
            else:require(row['reason'],'individual unresolved reference reason')
    require(n_history==14818 and states['RESOLVED_EXACT_RETAINED_BYTES']==14813,'historical resolution counts')
    copies=load(P/'COPY_MAP.json')['copies'];oldcopies=load(R/'before/preprint_v1_0/COPY_MAP.json')['copies'];require(copies[:163]==oldcopies,'old copy prefix')
    for row in copies:check(A/row['source_path'],row);check(P/row['package_path'],row)
    manifest=load(P/'SUPPORT_MANIFEST.json')['entries'];names=load(P/'SUPPORT_ALLOWLIST.json')['members'];archive=P/'support.zip';compression=zipfile.ZIP_DEFLATED
else:
    for row in load(R/'CURRENT_AUDIT_PINS.json')['records']:check(A/row['path'],row)
    history=load(R/'HISTORICAL_STAGE_RESOLUTION.json');allhistory=history['records']+history['additional_terminal_rows'];n_history=len(allhistory)
    for row in allhistory:check(A/row['resolved_path'],row);states['EXACT_CURRENT_OR_BEFORE']+=1
    require(len(history['records'])==2788 and len(history['additional_terminal_rows'])==1558,'history counts')
    copies=load(R/'COPY_EQUALITY_RECHECK.json')['records'];oldcopies=load(R/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies'];require(load(P/'INPUT_COPY_MAP.json')['copies'][:116]==oldcopies,'old copy prefix')
    for row in copies:check(A/row['source_resolved'],row);check(P/row['package_copy'],row)
    manifest=load(P/'PACKAGE_MANIFEST.json')['members'];names=sorted([r['path'] for r in manifest]+['PACKAGE_MANIFEST.json']);archive=P/'PR1071_preprint_v1_0_support.zip';compression=zipfile.ZIP_STORED
for row in manifest:check(P/row['path'],row)
with zipfile.ZipFile(archive) as z:
    require(z.namelist()==names and z.testzip() is None,'closed ZIP inventory/CRC')
    for info,name in zip(z.infolist(),names):
        require(info.date_time==(2026,10,14,0,0,0) and info.compress_type==compression and info.create_system==3 and info.external_attr==0o100644<<16 and not info.extra and not info.comment,'ZIP header')
        require(z.read(info.filename)==(P/name).read_bytes(),'ZIP payload')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=compression,compresslevel=9 if pr==1064 else None) as z:
    for name in names:
        info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=compression;z.writestr(info,(P/name).read_bytes(),compress_type=compression,compresslevel=9 if pr==1064 else None)
require(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP bytes')
commands=[]
def run(argv,cwd,success=True):
    p=subprocess.run(argv,cwd=cwd,capture_output=True);require((p.returncode==0)==success,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'));commands.append({'argv':[str(x) for x in argv],'exit_code':p.returncode,'expected_success':success,'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode(errors='replace')});return p
with tempfile.TemporaryDirectory(prefix=f'root{pr}-case-repair-',dir='/private/tmp') as td:
    td=Path(td);kit=td/'kit'
    with zipfile.ZipFile(archive) as z:z.extractall(kit)
    alias=td/'KIT';require(alias.samefile(kit),'case alias premise');snapshot={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()}
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';py=['python3','-B']+(['-I'] if pr==1064 else [])+(['-O'] if optimized else []);script='' if pr==1064 else 'scripts/'
        run(py+[script+'verify_package.py'],kit)
        if pr==1064:
            run(py+['run_checks.py','--out-dir',f'tmp/root-check-{mode}'],kit)
            output=td/f'external-{mode}.zip';run(py+['build_archive.py','--output',str(output)],kit);require(output.read_bytes()==archive.read_bytes(),'supported external ZIP')
            for target in [alias/f'forbidden-{mode}.zip',alias/'missing'/'nested'/f'forbidden-{mode}.zip']:
                run(py+['build_archive.py','--output',str(target)],kit,False);require(not target.exists() and not (kit/'missing').exists(),'forbidden descendant')
            allowed=alias/'tmp'/f'allowed-{mode}.zip';run(py+['build_archive.py','--output',str(allowed)],kit);require(allowed.read_bytes()==archive.read_bytes(),'intended tmp alias remains allowed')
            run(py+[str(P/'verify_package.py'),'--require-deposit-binding'],P)
        else:
            run(py+['scripts/check.py','--out',str(td/f'checks-{mode}')],kit)
            output=td/f'external-{mode}.zip';run(py+['scripts/build_archive.py','--out',str(output)],kit);require(output.read_bytes()==archive.read_bytes(),'supported external ZIP')
            for writer,flag in [('build_archive.py','--out'),('check.py','--out'),('build_pdf.py','--out')]:
                target=alias/f'forbidden-{writer}-{mode}';run(py+['scripts/'+writer,flag,str(target)],kit,False);require(not target.exists(),'forbidden output')
            run(py+[str(P/'scripts/verify_package.py'),'--require-bindings'],P)
        for name,data in snapshot.items():require((kit/name).read_bytes()==data,'protected extraction changed')
native=P/'publication/zenodo-deposit.json' if pr==1064 else A/'publication/zenodo-deposit.json';run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(native)],P)
for row in outputs:check(R/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_BOUNDED_CASE_ALIAS_REPAIR_PENDING_NEW_COMPLETE_WHOLE_REVIEW','full_report_operative_code_and_prose_diff_read_large_pin_arrays_rehashed':True,'counts_rehashed':{'outputs':len(outputs),'baseline':len(baseline),'changes':len(changes),'unchanged':len(baseline)-len(changes),'current':len(current),'historical_rows':n_history,'copies':len(copies),'closed_zip_members':len(names)},'historical_states':dict(states),'historical_exceptions':'1064:two copies of unsupported stale inventory digest andthree intentional invalidbindingfixture pointers, individuallydisclosed; no fabricated missingbytes ororiginalstage replay' if pr==1064 else 'All4346original/laterstage rows resolve exact, no oldstage rewrite','independent_actual_commands':commands,'independent_closed_zip_byte_equal':True,'paper_TeX_PDF_math_checker_bibliographic_bytes_unchanged':True,'no_new_compile_render':True,'prior_complete_whole_reviews':3 if pr==1064 else 2,'new_required_complete_whole_review':4 if pr==1064 else 3,'minimum_whole_reviews':2,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_CASE_ALIAS_REPAIR_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_BOUNDED_CASE_REPAIR_ADOPTED','pr':pr,'counts':record['counts_rehashed'],'actual_commands':len(commands),'ready':False}))
