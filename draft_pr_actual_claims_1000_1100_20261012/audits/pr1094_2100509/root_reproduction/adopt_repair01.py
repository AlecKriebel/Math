from pathlib import Path
import datetime, hashlib, json, os, subprocess, tempfile, zipfile, io
A=Path(__file__).resolve().parents[1]; P=A/'preprint_v1_0'; K=P/'kit'; R=A/'repairs/package01'
def load(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v: raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes(); require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'SEAL.json'); require(sha((R/'OUTPUT_PINS.json').read_bytes())==seal['output_pins_sha256'],'seal')
for row in load(R/'OUTPUT_PINS.json')['records']: check(R/row['path'],row)
changed={r['path']:r for r in load(R/'INPUT_PRESERVATION.json')['allowed_changes']}
baseline=load(R/'FROZEN_INPUT_PINS.json')['records']
for row in baseline:
    c=changed.get(row['path']); check(R/c['exact_before_path'] if c else A/row['path'],row)
    if c: check(A/row['path'],c['after'])
current=load(R/'CURRENT_ARTIFACT_PINS.json')['records']
for row in current: check(A/row['path'],row)
history=load(R/'PRIOR_STAGE_RESOLUTION.json')['stages']; n_history=0
for stage in history:
    require(sha((A/stage['inventory']).read_bytes())==stage['inventory_sha256'],'historical inventory')
    require(len(stage['records'])==stage['count'],'historical count')
    for row in stage['records']: check(A/row['resolution'],row); n_history+=1
custody=load(K/'CUSTODY_MAP.json'); origins=[]
for row in custody['copies']:
    src=changed.get(row['original_path']); source=R/src['exact_before_path'] if src else A/row['original_path']
    check(source,row); check(K/row['copy_path'],row); origins.append(row['original_path'])
for row in custody['exclusions']:
    src=changed.get(row['path']); check(R/src['exact_before_path'] if src else A/row['path'],row); origins.append(row['path'])
require(len(origins)==len(set(origins))==len(baseline)==custody['exact_partition_count'],'partition')
manifest=load(K/'MANIFEST.json')['records']; expected=sorted(['MANIFEST.json']+[r['path'] for r in manifest])
for row in manifest: check(K/row['path'],row)
archive=P/'pr1094_supportkit_v1.0.zip'
with zipfile.ZipFile(archive) as z:
    require(z.namelist()==expected and z.testzip() is None,'closed ZIP inventory/CRC')
    for info in z.infolist():
        require(info.date_time==(1980,1,1,0,0,0) and info.compress_type==zipfile.ZIP_STORED and info.create_system==3 and info.external_attr==0o100644<<16,'ZIP header')
        require(z.read(info.filename)==(K/info.filename).read_bytes(),'ZIP member')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
    for name in expected:
        info=zipfile.ZipInfo(name,(1980,1,1,0,0,0)); info.create_system=3; info.external_attr=0o100644<<16
        z.writestr(info,(K/name).read_bytes())
require(buf.getvalue()==archive.read_bytes(),'independent CLOSED ZIP bytes')
meta=load(K/'metadata.json'); require(meta==load(K/'.zenodo.json')==load(K/'metadata_api.json')['metadata']==load(P/'zenodo-deposit.json')['metadata'],'metadata equality')
commands=[]
def run(argv,cwd,success=True):
    p=subprocess.run(argv,cwd=cwd,capture_output=True); require((p.returncode==0)==success,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'))
    commands.append({'argv':[str(a) for a in argv],'expected_success':success,'exit_code':p.returncode,'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode(errors='replace')}); return p
with tempfile.TemporaryDirectory(prefix='root1094-repair-',dir='/private/tmp') as td:
    td=Path(td); kit=td/'kit'
    with zipfile.ZipFile(archive) as z: z.extractall(kit)
    require((td/'KIT').samefile(kit),'case alias premise')
    snapshot={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()}
    link=td/'lexical'; os.symlink(kit,link)
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal'; py=['python3','-B']+(['-O'] if optimized else [])
        run(py+['scripts/verify_kit.py'],kit)
        p=run(py+['scripts/run_checks.py','--out',f'../checks-{mode}.json'],kit)
        require(load(td/f'checks-{mode}.json')==load(K/'NEW_CONTROLS_RESULT.json'),'math JSON')
        run(py+['scripts/build_support.py','--out',f'../support-{mode}.zip'],kit)
        require((td/f'support-{mode}.zip').read_bytes()==archive.read_bytes(),'clean ZIP bytes')
        run(py+[str(K/'scripts/verify_kit.py'),'--require-binding'],K)
        run(py+['scripts/verify_kit.py','--binding',str(td/'missing-binding.json')],kit,False)
        for writer,flag,suffix in [('build_support.py','--out','.zip'),('run_checks.py','--out','.json'),('build_pdf.py','--out-dir','')]:
            for kind,target in [('case',td/'KIT'/'absent'/'nested'/f'{writer}{mode}{suffix}'),('lexical',link/'..'/f'{writer}{mode}{suffix}')]:
                run(py+['scripts/'+writer,flag,str(target)],kit,False)
                require(not target.exists() and not (td/'absent').exists() and not (kit/'absent').exists(),'forbidden output')
        require(snapshot=={p.relative_to(kit).as_posix():p.read_bytes() for p in kit.rglob('*') if p.is_file()},'protected extraction changed')
uploader=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
p=run(['python3','-B',str(uploader),'check',str(P/'zenodo-deposit.json')],P)
for row in load(R/'OUTPUT_PINS.json')['records']: check(R/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_BOUNDED_REPAIR01_PENDING_NEW_COMPLETE_WHOLE02','full_report_and_complete_code_prose_diff_read':True,'counts_rehashed':{'outputs':32,'baseline':len(baseline),'allowed_changes':len(changed),'protected_unchanged':len(baseline)-len(changed),'current':len(current),'historical_rows':n_history,'copies':len(custody['copies']),'exclusions':len(custody['exclusions']),'closed_zip_members':len(expected)},'independent_actual_commands':commands,'closed_zip_rebuilt_byte_equal':True,'paper_PDF_native_metadata_unchanged_verified':True,'no_new_compile_render':True,'whole_reviews_completed':1,'minimum_whole_reviews':2,'new_complete_whole02_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032,'repair_output_pins_sha256':seal['output_pins_sha256']}
(A/'ROOT_REPAIR_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ADOPT_BOUNDED_REPAIR01','counts':record['counts_rehashed'],'actual_commands':len(commands),'ready':False}))
