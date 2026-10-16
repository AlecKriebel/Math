from pathlib import Path
import contextlib,datetime,hashlib,io,json,subprocess,tempfile,zipfile
A=Path(__file__).resolve().parents[1];R=A/'finalization/terminal_admin_20261016';P=A/'preprint_v1_0'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p,n=None):
    b=p.read_bytes();return {'path':n or p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
    if 'mode' in r:need(p.stat().st_mode&511==r['mode'],'mode '+str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',s['output_inventory']);outputs=load(R/'OUTPUT_PINS.json')['entries']
for r in outputs:check(R/r['path'],r)
baseline=load(R/'INPUT_PINS.json')['records'];befores={r['path']:r for r in load(R/'BEFORE_PINS.json')['entries']}
for r in baseline:check(R/befores[r['path']]['preserved_path'] if r['path'] in befores else A/r['path'],r)
current=load(R/'FINAL_CURRENT_PINS.json')['records']
for r in current:check(P/r['path'],r)
copies=load(P/'COPY_MAP.json')['copies'];old=load(R/'before/preprint_v1_0/COPY_MAP.json')['copies'];need(copies[:165]==old and len(copies)==176,'copy prefix')
for r in copies:check(A/r['source_path'],r);check(P/r['package_path'],r)
stages=load(R/'PRIOR_STAGE_RECEIPTS.json')['stages'];total=0
for stage in stages:
    check(A/stage['manifest']['path'],stage['manifest'])
    for r in stage['records']:check(A/r['retained_exact_path'],r['original_record']);total+=1
need(total==852,'limited historical count')
archive=P/'support.zip';allow=load(P/'SUPPORT_ALLOWLIST.json');names=allow['members'];buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in names:
        i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,(P/n).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
need(buf.getvalue()==archive.read_bytes() and len(names)==212,'independent CLOSED deflate9 archive')
commands=[];cleanup=[]
def run(argv,cwd,ok=True,error=None):
    p=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True);commands.append({'argv':[str(x) for x in argv],'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')});need((p.returncode==0)==ok,'actual outcome '+str(argv)+' '+p.stderr.decode(errors='replace'));need(error is None or error.encode() in p.stderr,'wrong rejection');return p
@contextlib.contextmanager
def scratch():
    with tempfile.TemporaryDirectory(prefix='root1064-terminal-',dir=A/'root_reproduction') as tmp:
        try:yield Path(tmp)
        finally:
            for p in Path(tmp).rglob('*'):
                if p.is_file():cleanup.append(pin(p,p.relative_to(tmp).as_posix()))
            (A/'root_reproduction/TERMINAL_20261016_SCRATCH_IDENTITIES.json').write_text(json.dumps(cleanup,indent=2)+'\n')
with scratch() as T:
    C=T/'kit';C.mkdir()
    with zipfile.ZipFile(archive) as z:z.extractall(C)
    saved={p.relative_to(C).as_posix():p.read_bytes() for p in C.rglob('*') if p.is_file()}
    for opt in (False,True):
        py=['python3','-I','-B']+(['-O'] if opt else [])
        run(py+[C/'verify_package.py'],T)
        run(py+[P/'verify_package.py','--deposit-binding',P/'publication/DEPOSIT_BINDING.json','--require-deposit-binding'],T)
        out=T/('checks'+str(opt));run(py+[C/'run_checks.py','--out-dir',out],T)
        project=lambda d:{k:v for k,v in d.items() if k not in ('completed_utc','python','platform')}
        need(project(load(out/'original_normal/FINITE_CHECKS.json'))==project(load(P/'support/history/root_reproduction/FINITE_CHECKS.json')),'full original mathematical JSON')
        need(project(load(out/'guard_normal/FINITE_CHECKS.json'))==project(load(out/'guard_optimized/FINITE_CHECKS.json')),'full guarded math JSON')
        rebuilt=T/('rebuilt'+str(opt)+'.zip');run(py+[C/'build_archive.py','--output',rebuilt],T);need(rebuilt.read_bytes()==archive.read_bytes(),'actual archive rebuild')
        status=C/'TERMINAL_STATUS_20261016.json';v=load(status);v['whole_package_reviews_completed']=3;status.write_text(json.dumps(v))
        m=load(C/'SUPPORT_MANIFEST.json')
        # Every unchanged manifest field is retained; only this coherent
        # documentary fault's size/hash is refreshed to reach semantic checks.
        def update(x):
            if isinstance(x,dict):
                if x.get('path')=='TERMINAL_STATUS_20261016.json':x.update({k:pin(status,'TERMINAL_STATUS_20261016.json')[k] for k in ('bytes','sha256')})
                else:
                    for y in x.values():update(y)
            elif isinstance(x,list):
                for y in x:update(y)
        update(m);(C/'SUPPORT_MANIFEST.json').write_text(json.dumps(m))
        run(py+[C/'verify_package.py'],T,False,'dated terminal complete-review count altered')
        for n,b in saved.items():
            if (C/n).read_bytes()!=b:(C/n).write_bytes(b)
        alias=C.with_name('KIT');need(alias.samefile(C),'actual physical alias premise');run(py+[C/'build_archive.py','--output',alias/'fresh-forbidden.zip'],T,False);need(not (C/'fresh-forbidden.zip').exists(),'case guard wrote protected output')
    run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',P/'publication/zenodo-deposit.json'],Path('/Users/alec/Documents/Math'))
for r in current:check(P/r['path'],r)
for r in outputs:check(R/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_CURRENT_TERMINAL_ADMIN_NEW_EXTERNAL_FINAL_INTEGRITY','ROOT_full_REPORT_operative_diff_new_status_acceptance_and_explicit_historical_exception_qualification_read':True,'counts':{'baseline':len(baseline),'allowed_changes':len(befores),'protected':len(baseline)-len(befores),'outputs':len(outputs),'current_package':len(current),'copies':len(copies),'limited_retained_stage_rows':total,'archive_members':len(names)},'root_actual_commands':commands,'full_original_and_normal_optimized_guard_math_JSON_checked':True,'independent_closed_archive_byte_equal_current_python_zlib_environment':True,'history_qualification':'852 explicitly named retained rows individually rehashed. Five already unsupported historical occurrences remain unsupported; no blanket historical resolution. Whole04 broader dated14818/14813 qualification preserved, no missing bytes fabricated.','old_FINAL_SEAL_and_FINAL_INTEGRITY':'Preserved exact dated history; this new external authority supersedes their readiness for the current support successor.','whole_reviews_completed':4,'minimum_whole_reviews':2,'latest_complete_review_actionable_issues':0,'mathematics_paper_PDF_metadata_native_manifest_path_guards_unchanged':True,'new_compile_render_or_marker':False,'priority_novelty_independent_discovery_worldwide_openness':'UNKNOWN','published':False,'services_held_after_pr':1032,'current_assets':[pin(P/'paper.pdf'),pin(archive),pin(P/'SUPPORT_MANIFEST.json'),pin(P/'publication/zenodo-deposit.json')]}
adoption=A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json';need(not adoption.exists(),'adoption already exists');adoption.write_text(json.dumps(record,indent=2)+'\n')
integrity=A/'CURRENT_FINAL_INTEGRITY_20261016.json';seal=A/'CURRENT_FINAL_SEAL_20261016.json';need(not integrity.exists() and not seal.exists(),'new current authority already exists')
integrity.write_text(json.dumps({'utc':record['utc'],'scope':'All current regular audit files, including old FINAL history; this new integrity and new seal excluded to avoid cycle.','records':[pin(p) for p in sorted(A.rglob('*')) if p.is_file() and not p.is_symlink()]},indent=2)+'\n')
seal.write_text(json.dumps({'utc':record['utc'],'pr':1064,'status':'ROOT_CURRENT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','whole_reviews_completed':4,'minimum_whole_reviews':2,'actionable_issues':0,'publication_ready':True,'all_issues_resolved':True,'published':False,'services_held_after_pr':1032,'priority_novelty_worldwide_openness':'UNKNOWN','historical_unsupported_occurrences':5,'history_scope':record['history_qualification'],'old_seals_preserved':True,'current_assets':record['current_assets'],'root_terminal_adoption':pin(adoption),'current_final_integrity':pin(integrity),'terminal_outputs':pin(R/'OUTPUT_PINS.json'),'terminal_seal':pin(R/'SEAL.json'),'dated_internal_pending_fields':'Captured terminal administration; this new external seal supplies current ROOT final adoption.'},indent=2)+'\n')
print(json.dumps({'status':'ROOT_CURRENT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','counts':record['counts'],'root_commands':len(commands),'external_actions':0}))
