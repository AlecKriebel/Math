from pathlib import Path
import contextlib,datetime,hashlib,io,json,subprocess,tempfile,zipfile
A=Path(__file__).resolve().parents[1];B=A.parents[1];R=A/'finalization/terminal_admin_after_whole03_20261016';P=A/'preprint_v1_0'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p,n=None):
    b=p.read_bytes();return {'path':n or p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
literal_key_labels=[]
def pointer(d,p):
    original=d
    try:
        for k in p.split('/')[1:]:
            k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
        return d
    except (KeyError,IndexError,ValueError):
        # The local stage enumerator concatenates literal dictionary keys;
        # keys that are filenames may contain slashes. Its labels are not
        # RFC6901-escaped pointers. Match the actual original key sequence,
        # require a unique object, and retain an escaped locator separately.
        found=[]
        def walk(x,parts=()):
            if '/'+('/'.join(map(str,parts)))==p:found.append((parts,x))
            if isinstance(x,dict):
                for k,v in x.items():walk(v,parts+(k,))
            elif isinstance(x,list):
                for k,v in enumerate(x):walk(v,parts+(k,))
        walk(original);need(len(found)==1,'ambiguous literal-key historical traversal label')
        parts,x=found[0];literal_key_labels.append({'captured_local_label':p,'actual_RFC6901_pointer':'/'+('/'.join(str(k).replace('~','~0').replace('/','~1') for k in parts))})
        return x
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',{'bytes':s['output_pins_bytes'],'sha256':s['output_pins_sha256']});outputs=load(R/'OUTPUT_PINS.json')['files']
for r in outputs:check(R/r['path'],r)
baseline=load(R/'BASELINE_INPUT_PINS.json')['files'];changes=load(R/'CHANGE_INVENTORY.json')['files'];before={r['path']:r for r in changes}
for r in baseline:check(A/before[r['path']]['before_custody'] if r['path'] in before else A/r['path'],r)
current=load(R/'CURRENT_CANDIDATE_PINS.json')['files']
for r in current:check(P/r['path'],r)
copies=load(R/'COPY_EQUALITY_RECHECK.json')['files']
for r in copies:
    source=B/r['source_relative_program'] if 'source_relative_program' in r else A/r.get('source_snapshot_relative_audit',r['source_relative_audit'])
    check(source,r);check(P/r['copy'],r)
history=load(R/'HISTORICAL_STAGE_RESOLUTION.json');cache={}
for stage in history['stages']:
    if 'stage_bytes' not in stage:continue
    p=A/before[stage['stage']]['before_custody'] if stage['stage'] in before else A/stage['stage'];check(p,stage['stage_bytes']);cache[stage['stage']]=load(p)
bmap={r['path']:r for r in baseline}
for r in history['rows']:
    old=bmap[r['captured_locator']] if r['stage']=='post-whole03 terminal baseline' else pointer(cache[r['stage']],r['json_pointer'])
    need(old.get('bytes',old.get('size'))==r['bytes'] and old['sha256']==r['sha256'],'old live row identity')
    p=Path(r['resolved_exact_path']);check(p if p.is_absolute() else A/p,r)
retired=load(R/'HISTORICAL_RETIRED_SCRATCH_ROWS.json')['rows']
for r in retired:
    old=pointer(cache[r['stage']],r['json_pointer']);need(old['bytes']==r['bytes'] and old['sha256']==r['sha256'],'retired source row')
    check(A/r['final_cleanup_manifest'],r['final_cleanup_manifest_identity']);check(A/r['actual_cleanup_receipt'],r['actual_cleanup_receipt_identity'])
    rows=load(A/r['final_cleanup_manifest'])['files'];need(any(x['path']==r['captured_locator'] and x['bytes']==r['bytes'] and x['sha256']==r['sha256'] for x in rows),'retired final cleanup row')
    for witness in r['retained_actual_stdout_exact_witnesses']:
        obj=load(A/witness['source']);rows=obj['commands'] if isinstance(obj,dict) else obj;data=rows[witness['record_index']][witness['field']].encode();need(len(data)==witness['bytes'] and sha(data)==witness['sha256'],'exact retained stdout witness')
need(len(history['rows'])==6378 and len(retired)==38 and len(baseline)==543 and len(changes)==6 and len(copies)==142,'complete counts')
archive=P/'pr1085_support_v1_0.zip';names=sorted((P/'PAYLOAD_MEMBERS.txt').read_text().splitlines()+['SUPPORT_MANIFEST.json']);buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in names:
        i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,(P/n).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
need(buf.getvalue()==archive.read_bytes() and len(names)==175,'independent CLOSED archive')
commands=[];cleanup=[]
def run(argv,cwd,ok=True,error=None):
    p=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True);commands.append({'argv':[str(x) for x in argv],'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')});need((p.returncode==0)==ok,'actual outcome '+str(argv)+' '+p.stderr.decode(errors='replace'));need(error is None or error.encode() in p.stderr,'wrong rejection');return p
@contextlib.contextmanager
def scratch():
    with tempfile.TemporaryDirectory(prefix='root1085-terminal-',dir=A/'root_reproduction') as tmp:
        try:yield Path(tmp)
        finally:
            for p in Path(tmp).rglob('*'):
                if p.is_file():cleanup.append(pin(p,p.relative_to(tmp).as_posix()))
            (A/'root_reproduction/TERMINAL_AFTER_WHOLE03_SCRATCH_IDENTITIES.json').write_text(json.dumps(cleanup,indent=2)+'\n')
with scratch() as T:
    C=T/'kit';C.mkdir()
    with zipfile.ZipFile(archive) as z:z.extractall(C)
    saved={p.relative_to(C).as_posix():p.read_bytes() for p in C.rglob('*') if p.is_file()};math=[]
    for opt in (False,True):
        py=['python3','-B']+(['-O'] if opt else [])
        run(py+[P/'verify_package.py','--require-deposit'],T);run(py+[C/'verify_package.py'],T)
        p=run(py+[C/'check_math.py'],T);math.append(json.loads(p.stdout))
        for fault in ('normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign'):run(py+[C/'check_math.py','--mutation',fault],T,False)
        rebuilt=T/('rebuilt'+str(opt)+'.zip');run(py+[C/'build_archive.py','--output',rebuilt],T);need(rebuilt.read_bytes()==archive.read_bytes(),'actual deterministic archive')
        status=C/'CURRENT_TERMINAL_ACCOUNTING_20261016.json';v=load(status);v['whole_reviews_completed']=2;status.write_text(json.dumps(v));m=load(C/'SUPPORT_MANIFEST.json')
        def update(x):
            if isinstance(x,dict):
                if x.get('path')==status.name:x.update({k:pin(status,status.name)[k] for k in ('bytes','sha256')})
                else:
                    for y in x.values():update(y)
            elif isinstance(x,list):
                for y in x:update(y)
        update(m);(C/'SUPPORT_MANIFEST.json').write_text(json.dumps(m));run(py+[C/'verify_package.py'],T,False,'current terminal review count')
        for n,b in saved.items():
            if (C/n).read_bytes()!=b:(C/n).write_bytes(b)
        alias=C.with_name('KIT');need(alias.samefile(C),'actual physical alias premise');run(py+[C/'build_archive.py','--output',alias/'absent1'/'absent2'/'bad.zip'],T,False);need(not (C/'absent1').exists(),'protected ancestor created')
    need(math[0]==math[1],'complete current math JSON normal/optimized')
    run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',P/'zenodo-deposit.json'],Path('/Users/alec/Documents/Math'))
for r in current:check(P/r['path'],r)
for r in outputs:check(R/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_POST_WHOLE03_TERMINAL_ADMIN_FINAL_INTEGRITY','ROOT_full_REPORT_complete_operative_verifier_README_new_accounting_copy_map_and_retired_derivative_scope_read':True,'counts':{'baseline':len(baseline),'changes':len(changes),'protected':len(baseline)-len(changes),'outputs':len(outputs),'candidate':len(current),'source_copy_pairs':len(copies),'retained_live_history':len(history['rows']),'intentionally_retired_scratch_occurrences':len(retired),'stages':len(history['stages']),'archive_members':len(names)},'root_actual_commands':commands,'root_complete_normal_optimized_math_JSON_equal':True,'independent_CLOSED_ZIP_byte_equal_current_environment':True,'retired_derivative_qualification':'38 occurrences/19 distinct own scratch locators individually equal recorded final cleanup rows and bound actual cleanup receipt. Exact stdout witnesses checked where present; no extant-body, re-creation, omitted-program replay or full source read claim.','local_traversal_label_scope':'Historical local json_pointer fields were produced by the disclosed literal-key walker; slash-containing filename keys and the baseline labels are local traversal labels, not RFC6901 interfaces. ROOT independently resolves each to an actual unique source object, verifies the complete size/hash identity, and records escaped equivalents where needed. No runtime/public package API depends on these labels.','literal_key_label_escaped_equivalents':literal_key_labels,'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_whole_review':3,'actionable_issues':0,'mathematics_PDF_TeX_path_guards_native_metadata_unchanged':True,'new_compile_render_or_marker':False,'priority_novelty_independent_discovery_worldwide_openness':'UNKNOWN','current_assets':[pin(P/'paper.pdf'),pin(archive),pin(P/'SUPPORT_MANIFEST.json'),pin(P/'zenodo-deposit.json')],'published':False,'services_held_after_pr':1032}
adoption=A/'ROOT_TERMINAL_AFTER_WHOLE03_REVIEW_20261016.json';need(not adoption.exists(),'prior adoption exists');adoption.write_text(json.dumps(record,indent=2)+'\n')
integrity=A/'CURRENT_FINAL_INTEGRITY_20261016.json';seal=A/'CURRENT_FINAL_SEAL_20261016.json';need(not integrity.exists() and not seal.exists(),'new current authority exists')
integrity.write_text(json.dumps({'utc':record['utc'],'scope':'All current regular audit files before these new current integrity/seal files; both excluded to avoid cycles.','records':[pin(p) for p in sorted(A.rglob('*')) if p.is_file() and not p.is_symlink()]},indent=2)+'\n')
seal.write_text(json.dumps({'utc':record['utc'],'pr':1085,'status':'ROOT_CURRENT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','whole_reviews_completed':3,'minimum_whole_reviews':2,'actionable_issues':0,'publication_ready':True,'all_issues_resolved':True,'published':False,'services_held_after_pr':1032,'priority_novelty_worldwide_openness':'UNKNOWN','current_assets':record['current_assets'],'root_terminal_adoption':pin(adoption),'current_final_integrity':pin(integrity),'terminal_outputs':pin(R/'OUTPUT_PINS.json'),'terminal_seal':pin(R/'SEAL.json'),'dated_internal_pending_fields':'Exact captured terminal administration; this new external seal supplies ROOT final integrity adoption.'},indent=2)+'\n')
print(json.dumps({'status':'ROOT_CURRENT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','counts':record['counts'],'commands':len(commands),'external_actions':0}))
