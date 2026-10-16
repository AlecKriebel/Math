from pathlib import Path
import datetime,hashlib,json,subprocess,tempfile,zipfile,io
B=Path(__file__).resolve().parents[1];A=B/'audits/pr1080_11000150';P=A/'preprint_v1_0';K=P/'verification_kit';R=A/'repairs/case_alias01'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',seal['output_inventory']);outputs=load(R/'OUTPUT_PINS.json')['files']
for row in outputs:check(R/row['path'],row)
changes={r['path']:r for r in load(R/'CHANGE_ACCOUNTING.json')['changes']};baseline=load(R/'IMMEDIATE_INPUT_PINS.json')['files']
for row in baseline:
    c=changes.get(row['path']);check(A/(c['source_snapshot'] if c else row['path']),row)
    if c:check(A/row['path'],c['after'])
current=load(R/'CURRENT_INPUT_PINS.json')['files']
for row in current:check(A/row['path'],row)
commands=[]
def run(argv,cwd,success=True):
    p=subprocess.run(argv,cwd=cwd,capture_output=True);need((p.returncode==0)==success,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'));commands.append({'argv':[str(x) for x in argv],'expected_success':success,'exit_code':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')});return p
r=run(['python3','-B',str(R/'verify_repair.py'),'--check'],R);need(json.loads(r.stdout)==load(R/'FINAL_VERIFICATION.json'),'sealed read-only reconciliation')
archive=P/'verification_kit.zip';names=load(K/'ALLOWLIST.json')['members']
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
    for name in names:
        info=zipfile.ZipInfo('verification_kit/'+name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,(K/name).read_bytes())
need(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP bytes')
with tempfile.TemporaryDirectory(prefix='root1080-case-repair-',dir='/private/tmp') as td:
    td=Path(td)
    with zipfile.ZipFile(archive) as z:z.extractall(td)
    kit=td/'verification_kit';alias=td/'VERIFICATION_KIT';need(alias.samefile(kit),'actual case premise');snapshot={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()};results=[]
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';py=['python3','-B','-I']+(['-O'] if optimized else [])
        run(py+['verify.py'],kit);r=run(py+['run_checks.py'],kit);results.append(json.loads(r.stdout));run(py+['fault_checks.py'],kit)
        out=td/f'archive-{mode}.zip';run(py+['build_archive.py','--output',str(out)],kit);need(out.read_bytes()==archive.read_bytes(),'actual clean rebuild')
        run(py+['verify.py','--require-binding','--binding',str(P/'EXTERNAL_BINDING.json'),'--pdf',str(P/'preprint.pdf'),'--archive',str(archive)],kit)
        for script_root,target_root in [(kit,alias),(alias,kit)]:
            target=target_root/'missing'/'deeper'/f'forbidden-{mode}.zip';r=run(py+[str(script_root/'build_archive.py'),'--output',str(target)],kit,False);need(b'outside' in r.stderr and not (kit/'missing').exists(),'alias reject before mkdir')
        need(snapshot=={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()},'protected extraction changed')
    need(results[0]==results[1],'full math JSON differs')
run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(P/'deposit_metadata.json')],P)
for row in outputs:check(R/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_BOUNDED_CASE_ALIAS_REPAIR_PENDING_NEW_COMPLETE_WHOLE03','full_report_operative_code_prose_diff_and_complete_read_only_reconciliation_source_read':True,'counts_rehashed':{'outputs':len(outputs),'baseline':len(baseline),'changes':len(changes),'unchanged':len(baseline)-len(changes),'current_audit':len(current),'source_copy_pairs':157,'historical_rows':4641,'historical_relocations':9,'individual_changed_pin_resolutions':75,'closed_zip_members':len(names)},'root_actual_commands':commands,'read_only_complete_sealed_reconciliation_passed':True,'independent_CLOSED_zip_byte_equal':True,'old_failed_fault_wrapper_cause':'UNKNOWN; initial erasing-fault escape preserved. Later direct fault and final suite rejected correctly, and ROOT fresh entire fault suite passed in BOTH modes; do not infer environmental cause or erase old failure. NEWwhole03 must evaluate residual concern.','paper_TeX_math_native_metadata_unchanged':True,'new_compile_render':False,'whole_reviews_completed':2,'minimum_whole_reviews':2,'new_complete_whole03_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_CASE_ALIAS_REPAIR_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':'PASS_BOUNDED_CASE_REPAIR_ROOT_ADOPTION','counts':record['counts_rehashed'],'actual_commands':len(commands),'ready':False}))
