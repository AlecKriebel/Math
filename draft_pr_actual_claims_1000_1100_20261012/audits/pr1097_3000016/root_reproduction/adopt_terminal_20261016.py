from pathlib import Path
import collections,datetime,hashlib,io,json,subprocess,tempfile,zipfile,zlib
A=Path(__file__).resolve().parents[1];R=A/'finalization/terminal_admin_20261016';P=A/'preprint_v1_0';K=P/'kit';L=K/'provenance/terminal_admin_20261016'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p,n=None):
    b=p.read_bytes();return {'path':n or p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'FINAL_SEAL.json');check(R/'OUTPUT_PINS.json',s['output_inventory']);outputs=load(R/'OUTPUT_PINS.json')['entries']
for r in outputs:check(R/r['path'],r)
baseline=load(R/'INPUT_FREEZE.json')['entries'];resolved=load(R/'INPUT_PRESERVATION.json')['entries'];need(len(baseline)==len(resolved)==683,'baseline count')
need([{k:r[k] for k in ('path','bytes','sha256')} for r in resolved]==baseline,'baseline identities')
for r in resolved:check(A/r['resolved_path'],r)
before=load(R/'BEFORE_BYTES.json')['entries'];need(len(before)==7,'minimal edits')
for r in before:check(A/r['before_path'],r);need(pin(A/r['path'])['sha256']!=r['sha256'],'declared edit absent')
current=load(R/'CURRENT_CANDIDATE_PINS.json')['entries']
for r in current:check(A/r['path'],r)
stages=load(L/'STAGE_RESOLUTION.json')['entries'];cache={};ostates=collections.Counter();pstates=collections.Counter()
for r in stages:
    inv=r['inventory'];cache.setdefault(inv,load(A/inv));old=cache[inv][r['array']][r['row_zero_based']]
    need(old.get('bytes',old.get('size'))==r['bytes'] and old['sha256']==r['sha256'],'historic row identity')
    need(r['captured_locator'] in [old.get(k) for k in ('path','file','snapshot_path','repository_path','before_path')],'historic row locator')
    for role,base,counts in [('original_audit_resolution',A,ostates),('portable_resolution',K,pstates)]:
        d=r[role];counts[d['state']]+=1
        if d['state']=='INDIVIDUAL_OMISSION':need(bool(d['reason']),'individual omission lacks reason')
        else:
            p=Path(d['path']);check(p if p.is_absolute() else base/p,r)
need(len(stages)==4025 and ostates=={'EXACT_CURRENT_OR_CAPTURED_BEFORE_BYTES':3992,'EXACT_EXTERNAL_READ_ONLY_INPUT':2,'INDIVIDUAL_OMISSION':31} and pstates=={'EXACT_DISTRIBUTED_BYTES':3001,'INDIVIDUAL_OMISSION':1024},'stage counts')
copies=load(L/'COPIES.json')['entries']
for r in copies:check(A/r['source_path'],r);check(K/r['copy_path'],r)
tcustody=load(L/'CUSTODY.json')['entries'];bmap={r['path']:r for r in baseline};need(len(tcustody)==683,'terminal custody count')
for r in tcustody:
    b=bmap[r['captured_path']];need(b['bytes']==r['bytes'] and b['sha256']==r['sha256'],'terminal custody identity')
    if r['decision']=='EXACT_DISTRIBUTED_BYTES':check(K/r['copy_path'],r)
    else:need(r['decision']=='EXCLUDED' and bool(r.get('reason')),'custody omission reason')
need((P/'TERMINAL_ADMIN.json').read_bytes()==(K/'TERMINAL_ADMIN.json').read_bytes(),'terminal identical copies')
archive=P/'pr1097_support_v1_0.zip';names=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file());buf=io.BytesIO()
with zipfile.ZipFile(buf,'w') as z:
    for n in names:
        i=zipfile.ZipInfo(n,(1980,1,1,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED;z.writestr(i,(K/n).read_bytes())
need(buf.getvalue()==archive.read_bytes(),'independent CLOSED archive bytes')
with zipfile.ZipFile(archive) as z:
    need(z.namelist()==names and len(names)==198 and not z.comment and z.testzip() is None,'closed archive inventory')
    for i in z.infolist():
        b=z.read(i.filename);need(b==(K/i.filename).read_bytes() and i.CRC==zlib.crc32(b),'archive payload/CRC');need(not i.extra and not i.comment and not i.flag_bits,'archive header extras')
commands=[];cleanup=[]
def run(argv,cwd,ok=True,error=None):
    p=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True);commands.append({'argv':[str(x) for x in argv],'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')});need((p.returncode==0)==ok,'actual command outcome '+str(argv));need(error is None or error.encode() in p.stderr,'wrong rejection');return p
with tempfile.TemporaryDirectory(prefix='pr1097-root-terminal-',dir='/private/tmp') as tmp:
    T=Path(tmp);C=T/'kit';C.mkdir()
    with zipfile.ZipFile(archive) as z:z.extractall(C)
    saved={p.relative_to(C).as_posix():p.read_bytes() for p in C.rglob('*') if p.is_file()}
    def restore():
        for n,b in saved.items():
            if (C/n).read_bytes()!=b:(C/n).write_bytes(b)
    def refresh():
        d=load(C/'MANIFEST.json')
        for r in d['entries']:r.update(pin(C/r['path'],r['path']))
        (C/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n')
    for opt in (False,True):
        py=['python3','-B']+(['-O'] if opt else [])
        run(py+['scripts/verify.py','--require-binding'],K);run(py+['scripts/verify.py'],C)
        p=run(py+['scripts/run_checks.py'],C);need(json.loads(p.stdout)==load(K/'EXPECTED_RESULTS.json'),'complete math JSON')
        run(py+['scripts/run_checks.py','--inject-failure'],C,False,'deliberate unconditional failure control')
        out=T/('rebuilt'+str(opt)+'.zip');run(py+['scripts/build_support.py','--out',out],C);need(out.read_bytes()==archive.read_bytes(),'actual closed archive build')
        for key,value in [('complete_whole_package_reviews_completed',1),('publication_ready',True),('external_ROOT_final_integrity_adopted',True)]:
            restore();v=load(C/'TERMINAL_ADMIN.json');v[key]=value;(C/'TERMINAL_ADMIN.json').write_text(json.dumps(v));refresh();run(py+['scripts/verify.py'],C,False,'terminal semantic mismatch: '+key)
        restore();alias=C.with_name('KIT');need(alias.samefile(C),'actual physical alias premise')
        run(py+[C/'scripts/build_support.py','--out',alias/'fresh.zip'],T,False,'aliases a protected root');need(not (C/'fresh.zip').exists(),'protected output created')
    run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',P/'zenodo-deposit.json'],Path('/Users/alec/Documents/Math'))
    for p in T.rglob('*'):
        if p.is_file():cleanup.append(pin(p,p.relative_to(T).as_posix()))
for r in current:check(A/r['path'],r)
for r in outputs:check(R/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_TERMINAL_ADMIN_ROOT_FINAL_INTEGRITY','ROOT_full_REPORT_complete_operative_diff_new_terminal_record_selection_and_omission_qualification_read':True,'counts':{'baseline_inputs':683,'allowed_edits':7,'protected_unchanged':676,'terminal_outputs':len(outputs),'delivery_files':len(current),'history_rows':len(stages),'exact_new_copy_pairs':len(copies),'terminal_custody_decisions':len(tcustody),'archive_members':len(names)},'original_history_resolution_states':dict(ostates),'portable_history_resolution_states':dict(pstates),'old_165_and_332_partitions_and1127_rows_18_original_image_omissions_preserved':True,'current_asset_pins':[pin(P/'paper.pdf'),pin(archive),pin(K/'MANIFEST.json'),pin(P/'zenodo-deposit.json')],'actual_root_command_receipts':commands,'own_external_scratch_individual_hashes_before_cleanup':cleanup,'external_scratch_reason':'Unmodified supplied guard protects entire original audit root. All enduring work is in this dedicated audit folder; disposable external path was necessary for actual unchanged documented output commands.','mathematics_PDF_TeX_checker_path_guards_native_metadata_unchanged':True,'new_compile_render_or_marker':False,'whole_reviews_completed':2,'minimum_whole_reviews':2,'latest_whole_review_actionable_issues':0,'priority_result_gadget_method_independent_discovery_worldwide_openness':'UNKNOWN','initial_empty_optimized_output':'Uncompleted preserved attempt; completed optimized rerun is adopted.','services_held_after_pr':1032,'published':False}
adoption=A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json';need(not adoption.exists(),'prior adoption must not be overwritten');adoption.write_text(json.dumps(record,indent=2)+'\n')
integrity=A/'FINAL_INTEGRITY.json';seal=A/'FINAL_SEAL.json';need(not integrity.exists() and not seal.exists(),'prior final authority must not be overwritten')
integrity.write_text(json.dumps({'utc':record['utc'],'scope':'All current audit regular files before this external final integrity/seal; both excluded to avoid cycle.','records':[pin(p) for p in sorted(A.rglob('*')) if p.is_file() and not p.is_symlink()]},indent=2)+'\n')
seal.write_text(json.dumps({'utc':record['utc'],'pr':1097,'head':'ad7b0eeef847da65afe1b691705cfa6e832e8201','status':'ROOT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','root_full_terminal_report_operative_code_prose_and_final_package_independently_adopted':True,'whole_reviews_completed':2,'minimum_whole_reviews':2,'actionable_issues':0,'publication_ready':True,'all_issues_resolved':True,'published':False,'services_held_after_pr':1032,'priority_novelty_independent_discovery_worldwide_openness':'UNKNOWN','dated_internal_pending_fields':'Exact captured administration history; this external current seal supplies ROOT final integrity adoption.','current_assets':record['current_asset_pins'],'root_terminal_adoption':pin(adoption),'final_integrity':pin(integrity),'terminal_output_pins':pin(R/'OUTPUT_PINS.json'),'terminal_seal':pin(R/'FINAL_SEAL.json')},indent=2)+'\n')
print(json.dumps({'status':'ROOT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','root_commands':len(commands),'counts':record['counts'],'external_actions':0}))
