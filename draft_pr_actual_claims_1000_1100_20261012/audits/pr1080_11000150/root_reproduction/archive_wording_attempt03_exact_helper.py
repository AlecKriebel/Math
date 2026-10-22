from pathlib import Path
import contextlib,datetime,hashlib,json,subprocess,tempfile,zipfile
A=Path(__file__).resolve().parents[1];R=A/'repairs/archive_wording01';P=A/'preprint_v1_0';K=P/'verification_kit';Q=A/'reviews/package_03'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',s['output_inventory']);outputs=load(R/'OUTPUT_PINS.json')['files']
for r in outputs:check(R/r['path'],r)
current=load(R/'CURRENT_INPUT_PINS.json')['files']
for r in current:check(A/r['path'],r)
commands=[];cleanup=[]
@contextlib.contextmanager
def owned_scratch():
    with tempfile.TemporaryDirectory(prefix='root1080-wording-',dir=A/'root_reproduction') as tmp:
        try:yield tmp
        finally:
            rows=[]
            for p in Path(tmp).rglob('*'):
                if p.is_file():rows.append({'path':p.relative_to(tmp).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
            (A/'root_reproduction/ARCHIVE_WORDING_SCRATCH_CLEANUP.json').write_text(json.dumps({'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'only_new_own_scratch':True,'records':rows},indent=2)+'\n')
def run(argv,cwd,ok=True,error=None):
    p=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True);commands.append({'argv':[str(x) for x in argv],'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')})
    (A/'root_reproduction/ARCHIVE_WORDING_ROOT_COMMANDS_ATTEMPT03.json').write_text(json.dumps(commands,indent=2)+'\n')
    need((p.returncode==0)==ok,'actual outcome '+str(argv)+' '+p.stderr.decode(errors='replace'));need(error is None or error.encode() in p.stderr,'wrong rejection');return p
with owned_scratch() as tmp:
    T=Path(tmp);C=T/'verification_kit'
    with zipfile.ZipFile(P/'verification_kit.zip') as z:z.extractall(T)
    for optimized in (False,True):
        py=['python3','-B','-I']+(['-O'] if optimized else [])
        run(py+[C/'verify.py'],T)
        run(py+[C/'verify.py','--require-binding','--binding',P/'EXTERNAL_BINDING.json','--pdf',P/'preprint.pdf','--archive',P/'verification_kit.zip'],T)
        run(py+[C/'fault_checks.py'],T)
        # The adopted capture harness changes only owned I/O locations. The
        # current supported adapters/program bytes and full computations remain.
        H=T/('full-math-'+str(optimized));H.mkdir();(H/'scratch').mkdir()
        code=(Q/'fullmath_capture03.py').read_text()
        code=code.replace('HERE=Path(__file__).resolve().parent','HERE=Path('+repr(str(H))+')')
        code=code.replace("BASE=HERE.parents[1];DELIVERY=BASE/'preprint_v1_0';SCRATCH=HERE/'scratch'",'BASE=Path('+repr(str(A))+');DELIVERY=BASE/\'preprint_v1_0\';SCRATCH=HERE/\'scratch\'')
        code=code.replace("KIT=SCRATCH/'clean_check/verification_kit';RECEIPTS=HERE/'RESUME02_COMMAND_RECEIPTS.jsonl'",'KIT=Path('+repr(str(C))+');RECEIPTS=HERE/\'RESUME02_COMMAND_RECEIPTS.jsonl\'')
        run(py+['-c',code],T)
        need(load(H/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json')==load(Q/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json'),'complete mathematical JSON differs')
        alias=C.with_name('VERIFICATION_KIT');need(alias.samefile(C),'actual physical alias premise')
        for invoke,target in [(C,alias/'absent1'/'absent2'/'bad.zip'),(alias,C/'absent1'/'absent2'/'bad.zip')]:
            run(py+[invoke/'build_archive.py','--output',target],T,False)
            need(not (C/'absent1').exists(),'guard made protected ancestor')
    run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',P/'deposit_metadata.json'],Path('/Users/alec/Documents/Math'))
    for p in T.rglob('*'):
        if p.is_file():cleanup.append({'path':p.relative_to(T).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
for r in current:check(A/r['path'],r)
for r in outputs:check(R/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_BOUNDED_ARCHIVE_WORDING_REPAIR_NEW_COMPLETE_WHOLE04_REQUIRED','full_REPORT_both_current_READMEs_new_status_complete_readonly_custody_verifier_and_capture_harness_read':True,'read_only_verify_repair_check_actual_PASS_before_appending_this_root_artifact':True,'captured_stage_replay_scope':'The sealed local repair checker enumerates its captured750 canonical files; ROOT executed --check before creating this helper/adoption. Future new review/adoption artifacts are outside that historical count; this checker is not a portable entry point. Current public verify/fault/archive programs remain unchanged.','sealed_stage_summary':load(R/'FINAL_VERIFICATION.json'),'output_files_rehashed':len(outputs),'current_canonical_pins_rehashed':len(current),'root_actual_commands':commands,'full_math_output_comparison':'Both modes: exact full adopted whole03 mathematical JSON; only established surface timestamp and priority historical frozen-input count excluded, tuple/list JSON-normalized. No omitted52-input custody-tail replay.','root_closed_archive_and_all_custody_replay':'Actual read-only sealed stage replay independently rebuilt CLOSED267-member ZIP and checked721/8/713,181copy pairs,4666history,75old+42new structured pointers,9relocations and8source-body omission identities.','own_derivatives_hashed_before_cleanup':cleanup,'all_checkers_pathguards_PDF_TeX_native_metadata_unchanged':True,'new_compile_render_or_marker':False,'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_whole03_actionable_P3':1,'NEW_complete_whole04_REQUIRED':True,'priority_novelty_worldwide_openness':'UNKNOWN','full_maximum_classification_bundle':'PARTIAL','publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'output_pins_sha256':s['output_inventory']['sha256']}
(A/'ROOT_ARCHIVE_WORDING_REPAIR_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'outputs':len(outputs),'commands':len(commands),'ready':False}))
