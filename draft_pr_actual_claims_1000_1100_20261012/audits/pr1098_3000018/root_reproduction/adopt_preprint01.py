from pathlib import Path
import datetime,hashlib,json,os,subprocess,tempfile,zipfile,io,shutil
A=Path(__file__).resolve().parents[1];P=A/'preprint_v1_0';REPO=A.parents[2]
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(P/'PREPARATION_SEAL.json');require(sha((P/'OUTPUT_PINS.json').read_bytes())==seal['output_pins_sha256'],'preparation seal')
outputs=load(P/'OUTPUT_PINS.json')['entries']
for row in outputs:check(P/row['path'],row)
baseline=load(P/'INPUT_FREEZE.json')['entries']
for row in baseline:check(A/row['path'],row)
submitted=load(A/'SUBMITTED_PINS.json')
for row in submitted['files']:
    check(A/row['snapshot_path'],row);blob=subprocess.check_output(['git','cat-file','blob',submitted['head_oid']+':'+row['repository_path']],cwd=REPO);require(blob==(A/row['snapshot_path']).read_bytes(),'exact submitted Git blob')
custody=load(P/'CUSTODY_SELECTION.json')['entries'];require({r['path'] for r in custody}=={r['path'] for r in baseline} and len(custody)==len(baseline),'individual custody partition');copies=0
for row in custody:
    check(A/row['path'],row)
    if row['disposition']=='EXACT_AUTHORED_COPY':check(P/row['destination'],row);copies+=1
    else:require(row['disposition']=='OMITTED' and row['reason'],'omission reason')
manifest=load(P/'MANIFEST.json')['entries'];names=sorted([r['path'] for r in manifest]+['MANIFEST.json']);archive=P/'pr1098_support_v1_0.zip'
for row in manifest:check(P/row['path'],row)
require('paper.pdf' not in names and archive.name not in names and len(names)==102,'noncircular external assets')
with zipfile.ZipFile(archive) as z:
    require(z.namelist()==names and z.testzip() is None,'closed ZIP inventory CRC')
    for info in z.infolist():
        require(info.date_time==(2026,10,16,0,0,0) and info.compress_type==zipfile.ZIP_STORED and info.create_system==3 and info.external_attr==0o100644<<16 and not info.extra and not info.comment,'ZIP header')
        require(z.read(info.filename)==(P/info.filename).read_bytes(),'ZIP payload')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
    for name in names:
        info=zipfile.ZipInfo(name,(2026,10,16,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,(P/name).read_bytes())
require(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP')
native=load(P/'publication/zenodo-deposit.json');require(native['metadata']==load(P/'metadata.json')==load(P/'zenodo-api.json')['metadata'],'exact native object')
binding=load(P/'DEPOSIT_BINDING.json')
for name,row in binding['artifacts'].items():check(P/name,row)
require(sha((P/'metadata.json').read_bytes())==binding['metadata_sha256'],'metadata binding')
commands=[]
def run(argv,cwd,success=True):
    p=subprocess.run(argv,cwd=cwd,capture_output=True);require((p.returncode==0)==success,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'));commands.append({'argv':[str(x) for x in argv],'expected_success':success,'exit_code':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')});return p
with tempfile.TemporaryDirectory(prefix='root1098-preprint-',dir='/private/tmp') as td:
    td=Path(td);kit=td/'kit'
    with zipfile.ZipFile(archive) as z:z.extractall(kit)
    shutil.copyfile(P/'paper.pdf',kit/'paper.pdf');shutil.copyfile(archive,kit/archive.name)
    alias=td/'KIT';require(alias.samefile(kit),'physical case premise');snapshot={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()};results=[]
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';py=['python3','-B']+(['-O'] if optimized else [])
        run(py+['code/verify_kit.py'],kit)
        result=run(py+['code/run_checks.py'],kit);results.append(json.loads(result.stdout));require(results[-1]==load(P/'validation/NEW_CONTROLS_normal.json')==load(P/'validation/NEW_CONTROLS_optimized.json'),'full current diagnostics JSON')
        run(py+['code/run_checks.py','--invalid'],kit,False)
        target=td/f'rebuilt-{mode}.zip';run(py+['code/rebuild_archive.py','--output',str(target)],kit);require(target.read_bytes()==archive.read_bytes(),'supported clean archive bytes')
        for script,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
            for parent in [alias,alias/'code']:
                forbidden=parent/f'forbidden-{mode}-{script}';r=run(py+['code/'+script,flag,str(forbidden)],kit,False);require(b'inside physical protected root' in r.stderr and not forbidden.exists(),'physical guard before writer/compiler')
        require(snapshot=={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()},'protected extraction changed')
    require(results[0]==results[1],'normal/optimized diagnostics differ')
    out=td/'pdf-build';r=run(['python3','-B','code/build_pdf.py','--out-dir',str(out)],kit);require((out/'paper.pdf').read_bytes()==(P/'paper.pdf').read_bytes(),'root actual supported compile differs')
    pdf_rebuilt={'actual_supported_compile':True,'normal_mode':True,'PDF_byte_equal':True,'log_sha256':sha((out/'paper.log').read_bytes()),'scope':'Actual supported clean compilation. Other runtime versions not promised identical; all seven canonical pages viewed separately.'}
    saved=kit/'ARTIFACT_BINDINGS.json';raw=saved.read_bytes();saved.unlink()
    run(['python3','-B','code/verify_kit.py'],kit,False);saved.write_bytes(raw)
    require(snapshot=={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()},'restored extraction differs')
run(['python3','-B',str(REPO/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'publication/zenodo-deposit.json')],P)
images=[]
for i in range(1,8):
    path=A/'root_reproduction'/f'preprint_page-{i}.png';raw=path.read_bytes();images.append({'page':i,'path':str(path.relative_to(A)),'bytes':len(raw),'sha256':sha(raw),'actually_viewed':True,'issues':[]})
for row in outputs:check(P/row['path'],row)
for row in baseline:check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_ATTRIBUTED_PREPRINT_PREPARATION_PENDING_TWO_NEW_COMPLETE_WHOLE_REVIEWS','full_paper_preparation_report_all_seven_support_modules_metadata_README_and_source_notes_read':True,'prior_root_math_and_priority_adoptions_preserved':True,'mandatory_HLW_bank_and_Stockmeyer_Meyer_Gramlich_CRT_credits_globally_incorporated':True,'exact_result_realization_method_priority_worldwide_openness':'UNKNOWN','counts_rehashed':{'outputs':len(outputs),'prior_inputs':len(baseline),'actual_submitted_Git_blobs':len(submitted['files']),'exact_authored_copies':copies,'individual_exclusions':len(custody)-copies,'closed_zip_members':len(names)},'independent_CLOSED_zip_byte_equal':True,'independent_actual_commands':commands,'actual_root_PDF_compile':pdf_rebuilt,'all_actual_canonical_page_views':images,'whole_reviews_completed':0,'minimum_whole_reviews':2,'new_complete_whole01_and_new_complete_whole02_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_PREPRINT_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
# These new root-only renders have not entered another input freeze. Preserve
# their exact identities above, then remove only these disposable derivatives.
for row in images:(A/row['path']).unlink()
print(json.dumps({'status':'PASS_COMPLETE_PREPRINT_ROOT_ADOPTION','counts':record['counts_rehashed'],'actual_commands':len(commands),'pages_actually_viewed':7,'ready':False}))
