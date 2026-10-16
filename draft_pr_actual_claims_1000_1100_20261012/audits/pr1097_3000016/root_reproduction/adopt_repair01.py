from pathlib import Path
import datetime, hashlib, json, subprocess, tempfile, zipfile, io, os, collections, shutil
A=Path(__file__).resolve().parents[1]; P=A/'preprint_v1_0'; K=P/'kit'; R=A/'repairs/package01'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',seal['output_inventory'])
outputs=load(R/'OUTPUT_PINS.json')['entries']
for row in outputs:check(A/row['path'],row)
changes={r['path']:r for r in load(R/'CURRENT_CHANGES.json')['changes']}
baseline=load(R/'INPUT_PINS.json')['entries']
for row in baseline:
    c=changes.get(row['path']);check(A/(c['before_path'] if c else row['path']),row)
    if c:check(A/row['path'],c['after'])
current=load(R/'CURRENT_CANDIDATE_PINS.json')['entries']
for row in current:check(P/row['path'],row)
history=load(K/'provenance/repair01/STAGE_RESOLUTION.json')['entries'];states=collections.Counter()
for row in history:
    for key,base in [('original_audit_resolution',A),('portable_resolution',K)]:
        resolution=row[key];states[(key,resolution['state'])]+=1
        if 'path' in resolution:check(base/resolution['path'],row)
        else:require(resolution['state']=='INDIVIDUAL_OMISSION' and resolution['reason'],'unexplained omission')
copies=load(K/'provenance/repair01/COPIES.json')['entries']
for row in copies:check(A/row['source_path'],row);check(K/row['copy_path'],row)
custody=load(K/'provenance/repair01/CUSTODY.json')['entries'];origins=[]
for row in custody:
    origins.append(row['captured_path']);c=changes.get(row['captured_path']);check(A/(c['before_path'] if c else row['captured_path']),row)
    if row['decision']=='EXACT_DISTRIBUTED_BYTES':check(K/row['copy_path'],row)
    else:require(row.get('reason'),'omission reason')
require(len(origins)==len(set(origins))==len(baseline),'custody partition')
manifest=load(K/'MANIFEST.json')['entries'];names=sorted(['MANIFEST.json']+[r['path'] for r in manifest]);archive=P/'pr1097_support_v1_0.zip'
for row in manifest:check(K/row['path'],row)
with zipfile.ZipFile(archive) as z:
    require(z.namelist()==names and z.testzip() is None,'ZIP inventory CRC')
    for info in z.infolist():
        require(info.date_time==(1980,1,1,0,0,0) and info.compress_type==zipfile.ZIP_STORED and info.create_system==3 and info.external_attr==0o100644<<16 and not info.extra and not info.comment,'ZIP header')
        require(z.read(info.filename)==(K/info.filename).read_bytes(),'ZIP payload')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
    for name in names:
        info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,(K/name).read_bytes())
require(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP')
meta=load(K/'metadata.json');require(meta==load(P/'.zenodo.json')==load(K/'zenodo-metadata.json')['metadata']==load(P/'zenodo-deposit.json')['metadata']==load(P/'DEPOSIT_BINDING.json')['metadata'],'native metadata exact')
commands=[]
def run(argv,cwd,success=True):
    p=subprocess.run(argv,cwd=cwd,capture_output=True);require((p.returncode==0)==success,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'))
    commands.append({'argv':[str(x) for x in argv],'expected_success':success,'exit_code':p.returncode,'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode(errors='replace')});return p
with tempfile.TemporaryDirectory(prefix='root1097-repair-',dir='/private/tmp') as td:
    td=Path(td);kit=td/'kit'
    with zipfile.ZipFile(archive) as z:z.extractall(kit)
    require((td/'KIT').samefile(kit),'actual case premise');snapshot={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()}
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';py=['python3','-B']+(['-O'] if optimized else [])
        run(py+['scripts/verify.py'],kit)
        result=run(py+['scripts/run_checks.py'],kit);require(json.loads(result.stdout)==load(K/'EXPECTED_RESULTS.json'),'full math JSON')
        run(py+['scripts/run_checks.py','--inject-failure'],kit,False)
        out=td/f'support-{mode}.zip';run(py+['scripts/build_support.py','--out',str(out)],kit);require(out.read_bytes()==archive.read_bytes(),'actual writer exact bytes')
        run(py+[str(K/'scripts/verify.py'),'--require-binding'],K)
        run(py+['scripts/verify.py','--binding',str(td/'missing.json')],kit,False)
        for script,flag,suffix in [('build_support.py','--out','.zip'),('rebuild_pdf.py','--out-dir','')]:
            for kind,parent in [('case',td/'KIT'),('nested-case',td/'KIT'/'scripts')]:
                target=parent/f'forbidden-{mode}{suffix}';result=run(py+['scripts/'+script,flag,str(target)],kit,False)
                require(b'aliases a protected root' in result.stderr,'guard reached before compiler/writer')
                require(not target.exists(),'forbidden output created')
        require(snapshot=={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()},'protected extraction mutation')
run(['python3','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(P/'zenodo-deposit.json')],P)
for row in outputs:check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_BOUNDED_REPAIR01_PENDING_NEW_COMPLETE_WHOLE02','full_report_complete_code_prose_diff_and_current_guard_read':True,'counts_rehashed':{'outputs':len(outputs),'baseline':len(baseline),'changes':len(changes),'unchanged':len(baseline)-len(changes),'current':len(current),'history':len(history),'supplemental_exact_copy_pairs':len(copies),'custody':len(custody),'closed_zip_members':len(names)},'historical_states':{'/'.join(k):v for k,v in states.items()},'historical_metadata_only_omissions':'18 prior source-page image identities explicitly omitted, no fabricated local bytes','independent_actual_commands':commands,'closed_zip_rebuilt_byte_equal':True,'paper_PDF_math_checker_bibliographic_metadata_unchanged_verified':True,'no_new_compile_render':True,'whole_reviews_completed':1,'minimum_whole_reviews':2,'new_complete_whole02_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032,'repair_output_pins_sha256':seal['output_inventory']['sha256']}
(A/'ROOT_REPAIR_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ADOPT_BOUNDED_REPAIR01','counts':record['counts_rehashed'],'actual_commands':len(commands),'ready':False}))
