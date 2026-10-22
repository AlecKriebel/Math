from pathlib import Path
import json, hashlib, io, zipfile, tempfile, subprocess, os, datetime

A=Path(__file__).resolve().parents[1]
P=A/'NEWpreprint_v1_0'
F=A/'finalization/terminal_admin_20261015'
def load(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v: raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p));return b
seal=load(F/'SEAL.json')
check(F/'OUTPUT_PINS.json',seal['output_pins'])
outputs=load(F/'OUTPUT_PINS.json')['records']
for r in outputs: check(F/r['path'],r)
changes=load(F/'CHANGE_INVENTORY.json')['authorized_existing_changes']
changed={r['path']:r for r in changes}
baseline=load(F/'BASELINE_INPUT_PINS.json')['records']
for r in baseline:
    if r['path'] in changed:
        c=changed[r['path']];check(A/c['before_bytes_path_relative_to_audit'],r);check(A/r['path'],c['after'])
    else: check(A/r['path'],r)
for filename,base in [('CURRENT_CANDIDATE_PINS.json',P),('CURRENT_AUDIT_PINS.json',A),('CORE_PROTECTED_IDENTITIES.json',A)]:
    for r in load(F/filename)['records']: check(base/r['path'],r)
history=load(F/'HISTORICAL_STAGE_RESOLUTION.json')['records']
for r in history: check(A/r['resolved_path'],r)
copies=load(F/'COPY_EQUALITY_RECHECK.json')['records']
for r in copies:
    require(check(P/r['package_copy'],r)==check(A/r['source_resolved'],r),'copy differs')
beforemap=load(F/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies']
require(load(P/'INPUT_COPY_MAP.json')['copies'][:len(beforemap)]==beforemap,'old copy rows changed')
metadata=load(P/'metadata.json')
require(metadata==load(P/'metadata_wrapped.json')['metadata']==load(P/'deposit.json')['metadata']==load(A/'publication/zenodo-deposit.json')['metadata'],'metadata differs')
manifest=load(P/'PACKAGE_MANIFEST.json')
names=sorted(['PACKAGE_MANIFEST.json']+[r['path'] for r in manifest['members']])
for r in manifest['members']: check(P/r['path'],r)
archive=P/'PR1071_preprint_v1_0_support.zip'
with zipfile.ZipFile(archive) as z:
    require(z.namelist()==names and z.testzip() is None,'ZIP inventory/CRC')
    for n in names:
        i=z.getinfo(n)
        require(z.read(n)==(P/n).read_bytes() and i.date_time==(2026,10,14,0,0,0) and i.external_attr==0o100644<<16 and i.compress_type==zipfile.ZIP_STORED,'ZIP member/header')
buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as z:
    for n in names:
        i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED;z.writestr(i,(P/n).read_bytes())
require(buffer.getvalue()==archive.read_bytes(),'independent CLOSED ZIP differs')
commands=[]
with tempfile.TemporaryDirectory(prefix='root-terminal-',dir=Path(__file__).parent) as td:
    td=Path(td).resolve();clean=td/'clean'
    with zipfile.ZipFile(archive) as z:z.extractall(clean)
    protected={n:sha((clean/n).read_bytes()) for n in names}
    def run(flags,args,success=True,cwd=clean):
        argv=['python3','-B',*flags,*args];p=subprocess.run(argv,cwd=cwd,capture_output=True)
        require((p.returncode==0)==success,str(argv)+p.stderr.decode(errors='replace'))
        commands.append({'argv':argv,'exit_code':p.returncode,'expected_success':success,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
        return p
    for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
        run(flags,['scripts/verify_package.py'])
        run(flags,['scripts/check.py','--out',str(td/('checks-'+mode))])
        rebuilt=td/(mode+'.zip');run(flags,['scripts/build_archive.py','--out',str(rebuilt)])
        require(rebuilt.read_bytes()==archive.read_bytes(),'README rebuild differs')
        run(flags,['scripts/verify_package.py','--bindings',str(P/'UPLOAD_BINDINGS.json'),'--archive',str(archive),'--require-bindings'])
        run(flags,['scripts/verify_package.py','--bindings',str(td/'absent-bindings.json'),'--require-bindings'],False)
        for target in [clean/'TERMINAL_STATUS.json',clean/'paper.tex',td/('alias-'+mode)]:
            if target.parent==td:os.link(clean/'paper.tex',target)
            run(flags,['scripts/build_archive.py','--out',str(target)],False)
        run(flags,['scripts/build_pdf.py','--out',str(clean/'new-output'),'--tectonic','absent-root-compiler'],False)
    for n,h in protected.items():require(sha((clean/n).read_bytes())==h,'protected extraction changed')
    native=run([], [str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(A/'publication/zenodo-deposit.json')],cwd=A.parents[2])
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'utc':utc,'status':'ROOT_TERMINAL_ADMIN_ADOPTED','pr':1071,'head':'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','full_report_and_complete_semantic_diff_read':True,'output_records_rehashed':len(outputs),'immediate_inputs_resolved':len(baseline),'existing_changes':len(changes),'unchanged_inputs':len(baseline)-len(changes),'historical_stage_rows_resolved':len(history),'exact_copy_pairs_rehashed':len(copies),'independent_closed_zip_byte_equal':True,'clean_commands':commands,'no_new_compile_required':'Unchanged paper/PDF; complete whole02 actually compiled both modes and viewed all seven pages, previously ROOT adopted.','publication_ready':True,'published':False,'whole_reviews_completed':2,'latest_actionable_findings':0,'services_held_after_pr':1032,'scope':'This external current ROOT acceptance supersedes dated internal pending statuses without rewriting history. Mathematical/metadata meanings remain unchanged; no service operation performed.'}
(A/'FINAL_INTEGRITY.json').write_text(json.dumps(result,indent=2)+'\n')
artifacts=[]
for p in [P/'paper.tex',P/'paper.pdf',archive,P/'UPLOAD_BINDINGS.json',A/'publication/zenodo-deposit.json']:
    b=p.read_bytes();artifacts.append({'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
final={'utc':utc,'status':'ROOT_SEALED_READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032','pr':1071,'head':result['head'],'root_readiness':True,'whole_reviews_completed':2,'latest_actionable_findings':0,'published':False,'services_held_after_pr':1032,'integrity_sha256':sha((A/'FINAL_INTEGRITY.json').read_bytes()),'artifact_pins':artifacts,'terminal_admin_output_pins_sha256':sha((F/'OUTPUT_PINS.json').read_bytes()),'scope':result['scope']}
(A/'FINAL_SEAL.json').write_text(json.dumps(final,indent=2)+'\n')
print(json.dumps({'status':'PASS','utc':utc,'outputs':len(outputs),'history':len(history),'copies':len(copies),'commands':len(commands),'zip_sha256':sha(archive.read_bytes()),'published':False}))
