from pathlib import Path
import datetime,hashlib,json,subprocess,tempfile,zipfile,io
A=Path(__file__).resolve().parents[1];B=A.parents[1];P=A/'preprint_v1_0';R=A/'repairs/case_alias01'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'SEAL.json');need(sha((R/'OUTPUT_PINS.json').read_bytes())==seal['output_pins_sha256'],'seal');outputs=load(R/'OUTPUT_PINS.json')['files']
for row in outputs:check(R/row['path'],row)
baseline=load(R/'BASELINE_INPUT_PINS.json')['files'];changes={r['path']:r for r in load(R/'CHANGE_INVENTORY.json')['files']}
for row in baseline:
    c=changes.get(row['path']);check(A/(c['before_custody'] if c else row['path']),row)
    if c:check(A/row['path'],c['after'])
current=load(R/'CURRENT_CANDIDATE_PINS.json')['files']
for row in current:check(P/row['path'],row)
for row in load(R/'CURRENT_AUDIT_PINS.json')['files']:check(A/row['path'],row)
for row in load(R/'CORE_PROTECTED_IDENTITIES.json')['files']:check(P/row['path'],row)
copies=load(R/'COPY_EQUALITY_RECHECK.json')['files']
for row in copies:check(B/row['source_relative_program'],row);check(P/row['copy'],row)
history=load(R/'HISTORICAL_STAGE_RESOLUTION.json')['rows']
for row in history:check(A/row['resolved_exact_path'],row)
manifest=load(P/'SUPPORT_MANIFEST.json')['files'];names=sorted([r['path'] for r in manifest]+['SUPPORT_MANIFEST.json']);archive=P/'pr1085_support_v1_0.zip'
for row in manifest:check(P/row['path'],row)
with zipfile.ZipFile(archive) as z:
    need(z.namelist()==names and z.testzip() is None,'ZIP inventory CRC')
    for info in z.infolist():
        need(info.date_time==(2026,10,14,0,0,0) and info.compress_type==zipfile.ZIP_DEFLATED and info.create_system==3 and info.external_attr==0o100644<<16 and not info.extra and not info.comment,'ZIP headers');need(z.read(info.filename)==(P/info.filename).read_bytes(),'payload')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in names:
        info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(P/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
need(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP')
commands=[]
def run(argv,cwd,success=True):
    p=subprocess.run(argv,cwd=cwd,capture_output=True);need((p.returncode==0)==success,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'));commands.append({'argv':[str(x) for x in argv],'expected_success':success,'exit_code':p.returncode,'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode(errors='replace')});return p
with tempfile.TemporaryDirectory(prefix='root1085-case-repair-',dir='/private/tmp') as td:
    td=Path(td);kit=td/'kit'
    with zipfile.ZipFile(archive) as z:z.extractall(kit)
    alias=td/'KIT';need(alias.samefile(kit),'samefile premise');snapshot={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()};results=[]
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';py=['python3','-B']+(['-O'] if optimized else [])
        run(py+['verify_package.py'],kit);p=run(py+['check_math.py'],kit);results.append(json.loads(p.stdout))
        target=td/f'archive-{mode}.zip';run(py+['build_archive.py','--output',str(target)],kit);need(target.read_bytes()==archive.read_bytes(),'clean supported rebuild')
        run(py+[str(P/'verify_package.py'),'--require-deposit'],P)
        for script,flag in [('verify_package.py','--output'),('check_math.py','--output'),('build_archive.py','--output'),('build_pdf.py','--out-dir')]:
            target=alias/'missing'/'deeper'/f'forbidden-{script}-{mode}';r=run(py+[script,flag,str(target)],kit,False);need(b'outside physical kit' in r.stderr and not (kit/'missing').exists(),'physical guard before creation/compiler')
        need(snapshot=={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()},'protected extraction changed')
    need(results[0]==results[1],'full math JSON differs')
run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(P/'zenodo-deposit.json')],P)
for row in outputs:check(R/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_BOUNDED_CASE_ALIAS_REPAIR_PENDING_NEW_COMPLETE_WHOLE03','full_report_complete_code_prose_diff_read':True,'counts_rehashed':{'outputs':len(outputs),'baseline':len(baseline),'changes':len(changes),'unchanged':len(baseline)-len(changes),'current_candidate':len(current),'exact_copies':len(copies),'historical_rows':len(history),'closed_zip_members':len(names)},'independent_actual_commands':commands,'independent_closed_zip_byte_equal':True,'paper_TeX_math_native_bibliographic_metadata_unchanged':True,'no_new_compile_render':True,'whole_reviews_completed':2,'minimum_whole_reviews':2,'new_complete_whole03_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_CASE_ALIAS_REPAIR_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':'PASS_BOUNDED_CASE_REPAIR_ROOT_ADOPTION','counts':record['counts_rehashed'],'actual_commands':len(commands),'ready':False}))
