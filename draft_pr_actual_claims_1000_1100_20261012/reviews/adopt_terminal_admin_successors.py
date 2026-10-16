from pathlib import Path
import datetime,hashlib,json,sys,io,zipfile,tempfile,subprocess,collections
BASE=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
pr=int(sys.argv[1]);require(pr in [1080,1085],'scope');A=BASE/'audits'/('pr1080_11000150' if pr==1080 else 'pr1085_20000488');P=A/'preprint_v1_0';W=A/'finalization/terminal_admin_20261016';K=P/'verification_kit' if pr==1080 else P
seal=load(W/'SEAL.json');pinpath=W/'OUTPUT_PINS.json'
if pr==1080:check(pinpath,seal['output_pins'])
else:require(sha(pinpath.read_bytes())==seal['output_pins_sha256'],'seal')
outputs=load(pinpath)['files']
for row in outputs:check(W/row['path'],row)
account=load(W/('CHANGE_ACCOUNTING.json' if pr==1080 else 'CHANGE_INVENTORY.json'));changes={r['path']:r for r in account['changes']};baseline=load(W/('IMMEDIATE_INPUT_PINS.json' if pr==1080 else 'BASELINE_INPUT_PINS.json'))['files']
for row in baseline:
    c=changes.get(row['path']);check(A/(c['source_snapshot' if pr==1080 else 'before_snapshot'] if c else row['path']),row)
    if c:check(A/row['path'],c['after'])
if pr==1080:
    current=load(W/'CURRENT_INPUT_PINS.json')['files']
    for row in current:check(A/row['path'],row)
    copies=load(K/'REPAIR01_STAGE_COPIES.json')['files'];oldcopies=load(W/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json')['files'];require(copies[:100]==oldcopies and len(copies)==145,'old copy prefix')
    for row in copies:check(A/row['source_snapshot'],row);check(K/row['destination'],row)
    history=load(K/'REPAIR01_HISTORY_RESOLUTION.json')['references'];oldhistory=load(W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json')['references'];require(history[:2312]==oldhistory and len(history)==4628,'history prefix')
    relocations={r['reference_index']:r for r in load(K/'TERMINAL_HISTORY_RELOCATIONS.json')['rows']};states=collections.Counter()
    for i,row in enumerate(history):
        states[row['disposition']]+=1
        if row['disposition']=='exact_captured_stage_or_canonical_copy':
            destination=row['destination']
            if i in relocations:require(relocations[i]['historical_reference']==row,'historical relocation');destination=relocations[i]['current_exact_destination']
            check(K/destination,row)
        else:require(row['disposition']=='omitted' and row['reason'],'unexplained historical omission')
    names=load(K/'ALLOWLIST.json')['members'];archive=P/'verification_kit.zip';prefix='verification_kit/';stamp=(2026,10,14,0,0,0);compression=zipfile.ZIP_STORED;manifest=load(K/'MANIFEST.json')['files']
else:
    current=load(W/'CURRENT_CANDIDATE_PINS.json')['files']
    for row in current:check(P/row['path'],row)
    for row in load(W/'CURRENT_AUDIT_PINS.json')['files']:check(A/row['path'],row)
    for row in load(W/'CORE_PROTECTED_IDENTITIES.json')['files']:check(P/row['path'],row)
    copies=load(W/'COPY_EQUALITY_RECHECK.json')['files']
    for row in copies:check(A/row['source'],row);check(P/row['copy'],row)
    history=load(W/'HISTORICAL_STAGE_RESOLUTION.json')['rows'];states=collections.Counter()
    for row in history:check(A/row['resolved_exact_path'],row);states['exact_captured_bytes']+=1
    for row in load(W/'HISTORICAL_SEAL_BINDINGS.json')['seals']:
        parent=(A/row['seal']).parent;require(sha((parent/'OUTPUT_PINS.json').read_bytes())==row['output_pins_sha256'],'historical output seal')
    names=(P/'PAYLOAD_MEMBERS.txt').read_text().splitlines();archive=P/'pr1085_support_v1_0.zip';prefix='';stamp=(2026,10,14,0,0,0);compression=zipfile.ZIP_DEFLATED;manifest=load(P/'SUPPORT_MANIFEST.json')['files'];names=sorted(names+['SUPPORT_MANIFEST.json'])
for row in manifest:check(K/row['path'],row)
with zipfile.ZipFile(archive) as z:
    require(z.namelist()==[prefix+n for n in names] and z.testzip() is None,'ZIP inventory CRC')
    for info,name in zip(z.infolist(),names):
        require(info.date_time==stamp and info.compress_type==compression and info.create_system==3 and info.external_attr==0o100644<<16 and not info.extra and not info.comment,'ZIP header')
        require(z.read(info.filename)==(K/name).read_bytes(),'ZIP payload')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=compression,compresslevel=9 if pr==1085 else None) as z:
    for name in names:
        info=zipfile.ZipInfo(prefix+name,stamp);info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=compression;z.writestr(info,(K/name).read_bytes(),compress_type=compression,compresslevel=9 if pr==1085 else None)
require(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP bytes')
commands=[]
def run(argv,cwd,success=True):
    p=subprocess.run(argv,cwd=cwd,capture_output=True);require((p.returncode==0)==success,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'));commands.append({'argv':[str(x) for x in argv],'exit_code':p.returncode,'expected_success':success,'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode(errors='replace')});return p
with tempfile.TemporaryDirectory(prefix=f'root{pr}-admin-',dir='/private/tmp') as td:
    td=Path(td)
    with zipfile.ZipFile(archive) as z:z.extractall(td/'extract')
    kit=td/'extract'/'verification_kit' if pr==1080 else td/'extract';snapshot={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()};results=[]
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';py=['python3','-B']+(['-I'] if pr==1080 else [])+(['-O'] if optimized else [])
        run(py+['verify.py' if pr==1080 else 'verify_package.py'],kit)
        p=run(py+['run_checks.py' if pr==1080 else 'check_math.py'],kit);results.append(json.loads(p.stdout))
        target=td/f'archive-{mode}.zip';run(py+['build_archive.py','--output',str(target)],kit);require(target.read_bytes()==archive.read_bytes(),'actual clean archive rebuild')
        if pr==1080:args=['verify.py','--require-binding','--binding',str(P/'EXTERNAL_BINDING.json'),'--pdf',str(P/'preprint.pdf'),'--archive',str(archive)]
        else:args=[str(P/'verify_package.py'),'--require-deposit']
        run(py+args,kit)
        if pr==1080:
            alias=kit.parent/'VERIFICATION_KIT';require(alias.samefile(kit),'case premise');out=alias/f'case-{mode}.zip';run(py+['build_archive.py','--output',str(out)],kit);require(out.read_bytes()==archive.read_bytes(),'actual case finding');out.unlink()
        require(snapshot=={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()},'protected extraction changed')
    require(results[0]==results[1],'complete math JSON differs')
native=P/('deposit_metadata.json' if pr==1080 else 'zenodo-deposit.json');run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(native)],P)
for row in outputs:check(W/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_BOUNDED_TERMINAL_ADMIN_WITH_NEW_P3_HOLD_PENDING_REPAIR_AND_NEW_COMPLETE_WHOLE03','full_report_complete_code_prose_diff_read':True,'counts_rehashed':{'outputs':len(outputs),'baseline':len(baseline),'allowed_changes':len(changes),'protected_unchanged':len(baseline)-len(changes),'current':len(current),'copies':len(copies),'historical_rows':len(history),'closed_zip_members':len(names)},'historical_states':dict(states),'independent_actual_commands':commands,'independent_closed_zip_byte_equal':True,'mathematics_PDF_native_metadata_unchanged':True,'new_compile_render':False,'new_unresolved_P3':'Physical case alias bypasses intended outside-kit output boundary; actual archive writers normal/-O, no existing overwrite. Case-scope ROOT adoption additionally confirms1085.','new_bounded_shared_guard_repair_required':True,'new_complete_whole03_required':True,'whole_reviews_completed':2,'minimum_whole_reviews':2,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ADMIN_ADOPTED_WITH_NEW_P3_HOLD','pr':pr,'counts':record['counts_rehashed'],'actual_commands':len(commands),'ready':False}))
