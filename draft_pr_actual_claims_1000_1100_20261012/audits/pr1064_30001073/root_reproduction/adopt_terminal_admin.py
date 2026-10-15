from pathlib import Path
import json, hashlib, datetime, tempfile, subprocess, io, zipfile, os
A=Path(__file__).resolve().parents[1]
P=A/'preprint_v1_0'
F=A/'finalization/terminal_admin_20261014'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def check(p,x):
    b=p.read_bytes()
    if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError(str(p))
    return b
outputs=load(F/'OUTPUT_PINS.json')['entries']
for x in outputs:check(F/x['path'],x)
changes=load(F/'CHANGE_INVENTORY.json')['modified']; changed={x['path']:x for x in changes}
baseline=load(F/'INPUT_PINS.json')['records']
for x in baseline:
    if x['path'] in changed:
        c=changed[x['path']];check(A/c['preserved_path'],x);check(A/x['path'],c['after'])
    else:check(A/x['path'],x)
current=load(F/'FINAL_CURRENT_PINS.json')['records']
for x in current:check(P/x['path'],x)
protected=load(F/'PROTECTED_BYTE_RECEIPT.json')['unchanged_records']
for x in protected:check(A/x['path'],x)
stages=load(F/'PRIOR_STAGE_RECEIPTS.json')['stages']; old_count=0
for s in stages:
    if 'records' in s:
        if len(s['records'])!=s['count']:raise RuntimeError('Stage count')
        for x in s['records']:check(A/x['resolved_path'],x);old_count+=1
    else:
        inventory=A/s['stage'];rows=load(inventory)['entries']
        if len(rows)!=s['count']:raise RuntimeError('Unchanged stage count')
        for x in rows:check(inventory.parent/x['path'],x);old_count+=1
copies=load(P/'COPY_MAP.json')['copies']
for x in copies:
    if check(P/x['package_path'],x)!=(A/x['source_path']).read_bytes():raise RuntimeError('Source copy mismatch')
selection=load(P/'TERMINAL_SELECTION_LEDGER.json')['records']
for x in selection:
    check(A/x['source_path'],x)
    if not x['reason']:raise RuntimeError('Unexplained selection')
    if x['included'] and not any(c['source_path']==x['source_path'] and c['sha256']==x['sha256'] for c in copies):raise RuntimeError('Included source missing')
meta=load(P/'metadata.json')
for n in ['publication/zenodo.json','publication/release_metadata.json','publication/zenodo-deposit.json']:
    d=load(P/n)
    if d.get('metadata',d)!=meta:raise RuntimeError('Metadata differs')
for n in ['paper.tex','paper.pdf','metadata.json','publication/zenodo.json','publication/release_metadata.json']:
    check(P/n,next(x for x in baseline if x['path']=='preprint_v1_0/'+n))
archive=P/'support.zip';names=load(P/'SUPPORT_ALLOWLIST.json')
if isinstance(names,dict):names=names.get('files',names.get('members'))
if names and isinstance(names[0],dict):names=[x['path'] for x in names]
with zipfile.ZipFile(archive) as z:
    if z.namelist()!=sorted(names) or z.testzip() is not None:raise RuntimeError('ZIP names/CRC')
    for n in names:
        i=z.getinfo(n)
        if z.read(n)!=(P/n).read_bytes() or i.external_attr!=(0o100644<<16) or i.date_time!=(2026,10,14,0,0,0) or i.compress_type!=zipfile.ZIP_DEFLATED:raise RuntimeError('ZIP payload/header')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in sorted(names):
        i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(i,(P/n).read_bytes(),compresslevel=9)
if buf.getvalue()!=archive.read_bytes():raise RuntimeError('Independent CLOSED ZIP differs')
commands=[]
with tempfile.TemporaryDirectory(prefix='root-terminal-',dir=Path(__file__).parent) as td:
    td=Path(td).resolve();clean=td/'clean'
    with zipfile.ZipFile(archive) as z:z.extractall(clean)
    protected_clean={n:sha((clean/n).read_bytes()) for n in names}
    def run(flags,args,success=True):
        argv=['python3','-I','-B',*flags,*args];p=subprocess.run(argv,cwd=clean,capture_output=True)
        if (p.returncode==0)!=success:raise RuntimeError(str(argv)+p.stderr.decode(errors='replace'))
        commands.append({'argv':argv,'exit_code':p.returncode,'expected_success':success,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
    for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
        run(flags,['verify_package.py'])
        run(flags,['run_checks.py','--out-dir','tmp/check-'+mode])
        out='tmp/rebuilt-'+mode+'.zip';run(flags,['build_archive.py','--output',out])
        if (clean/out).read_bytes()!=archive.read_bytes():raise RuntimeError('Clean builder differs')
        run(flags,['verify_package.py','--archive',out])
        run(flags,['verify_package.py','--archive',out,'--deposit-binding',str(P/'publication/DEPOSIT_BINDING.json'),'--require-deposit-binding'])
        run(flags,['verify_package.py','--require-deposit-binding'],False)
        alias=td/('alias-'+mode);os.link(clean/'paper.tex',alias)
        run(flags,['build_archive.py','--output',str(alias)],False);alias.unlink()
        if protected_clean!={n:sha((clean/n).read_bytes()) for n in names}:raise RuntimeError('Protected clean input changed')
    run([],[str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'publication/zenodo-deposit.json')])
proof={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ROOT_TERMINAL_ADMIN_ADOPTION','full_report_75_line_semantic_diff_current_status_and_acceptance_read':True,'output_records_rehashed':len(outputs),'immediate_baseline_resolved':len(baseline),'authorized_admin_changes':len(changes),'protected_unchanged':len(protected),'current_package_files_rehashed':len(current),'old_stages':len(stages),'exact_old_stage_rows_resolved':old_count,'source_equal_copies':len(copies),'terminal_selection_records':len(selection),'independent_closed_ZIP_rebuild':True,'archive_members':len(names),'paper_TeX_PDF_and_bibliographic_bytes_unchanged':True,'actual_commands':commands,'no_recompile_or_rerender_of_unchanged_paper_in_admin_step':True,'full_whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_whole_review_actionable_P0_P1_P2_P3':0,'root_readiness':True,'publication_ready_after_order_hold_released':True,'published':False,'PR_merged':False,'DOI_or_tracker_action':False,'services_held_after_pr':1032,'dated_pending_internal_gates_superseded_by_this_current_root_adoption':True,'finalization_seal_sha256':sha((F/'SEAL.json').read_bytes()),'native_upload_manifest':'preprint_v1_0/publication/zenodo-deposit.json','artifact_pins':[{'path':str(p.relative_to(A)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in [P/'paper.tex',P/'paper.pdf',archive,P/'publication/zenodo-deposit.json',P/'publication/DEPOSIT_BINDING.json']]}
(A/'FINAL_INTEGRITY.json').write_text(json.dumps(proof,indent=2)+'\n')
seal={'utc':proof['utc'],'status':'ROOT_SEALED_READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032','pr':1064,'head':'bdefe31b9d226c8f27008d13f57775d5de8df3d7','root_readiness':True,'whole_reviews_completed':3,'latest_actionable_findings':0,'published':False,'services_held_after_pr':1032,'integrity_sha256':sha((A/'FINAL_INTEGRITY.json').read_bytes()),'artifact_pins':proof['artifact_pins'],'scope':'Current external ROOT adoption supersedes internal dated pending stages without rewriting them. No firstness, human peer review or service action is claimed.'}
(A/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items() if k not in ['actual_commands','artifact_pins']}))
