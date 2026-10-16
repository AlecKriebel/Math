from pathlib import Path
import json, hashlib, datetime, io, zipfile, subprocess, tempfile
A=Path(__file__).resolve().parents[1]
P=A/'preprint_v1_0'
def load(p):return json.loads(p.read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def check(p,x):
    b=p.read_bytes()
    if len(b)!=x['bytes'] or digest(b)!=x['sha256']:raise RuntimeError(str(p))
    return b
outputs=load(P/'OUTPUT_PINS.json')['files']
inputs=load(P/'PREPARATION_INPUT_PINS.json')['files']
for x in outputs:check(P/x['path'],x)
for x in inputs:check(A/x['path'],x)
seal=load(P/'PREPARATION_SEAL.json')
if digest((P/'OUTPUT_PINS.json').read_bytes())!=seal['output_pins_sha256']:raise RuntimeError('Preparation seal')
copies=load(P/'COPY_MAP.json')['files']
for x in copies:
    if check(P/x['copy'],x)!=(A/x['source_relative_audit']).read_bytes():raise RuntimeError('Copy equality')
exclusions=load(P/'EXCLUSIONS.json')['files']
if {x['source_relative_audit'] for x in copies}&{x['path'] for x in exclusions}:raise RuntimeError('Copy/exclusion overlap')
if {x['source_relative_audit'] for x in copies}|{x['path'] for x in exclusions}!={x['path'] for x in inputs}:raise RuntimeError('Incomplete partition')
if any(not x['reason'] for x in exclusions):raise RuntimeError('Unexplained exclusion')
meta=load(P/'.zenodo.json')
if meta!=load(P/'metadata.json')['metadata'] or meta!=load(P/'zenodo-deposit.json')['metadata'] or meta!=load(P/'UPLOAD_BINDINGS.json')['metadata']:raise RuntimeError('Metadata equality')
manifest=load(P/'SUPPORT_MANIFEST.json')['files']
for x in manifest:check(P/x['path'],x)
archive=P/'pr1085_support_v1_0.zip';names=sorted([x['path'] for x in manifest]+['SUPPORT_MANIFEST.json'])
with zipfile.ZipFile(archive) as z:
    if z.namelist()!=names or z.testzip() is not None:raise RuntimeError('ZIP membership/CRC')
    for n in names:
        i=z.getinfo(n)
        if z.read(n)!=(P/n).read_bytes() or i.date_time!=(2026,10,14,0,0,0) or i.external_attr!=(0o100644<<16) or i.compress_type!=zipfile.ZIP_DEFLATED:raise RuntimeError('ZIP payload/header')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in names:
        i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(i,(P/n).read_bytes(),compresslevel=9)
if buf.getvalue()!=archive.read_bytes():raise RuntimeError('Independent closed ZIP rebuild')
visual=[]
for i in range(1,8):
    p=P/'render'/('page-'+str(i)+'.png')
    visual.append({'page':i,'path':str(p.relative_to(A)),'sha256':digest(p.read_bytes()),'actually_viewed_by_root':True})
commands=[]
with tempfile.TemporaryDirectory(prefix='root-preprint01-',dir=Path(__file__).parent) as td:
    td=Path(td).resolve();clean=td/'clean'
    with zipfile.ZipFile(archive) as z:z.extractall(clean)
    def run(flags,args,success=True):
        argv=['python3','-B',*flags,*args];p=subprocess.run(argv,cwd=clean,capture_output=True)
        if (p.returncode==0)!=success:raise RuntimeError(str(argv)+p.stderr.decode(errors='replace'))
        commands.append({'argv':argv,'exit_code':p.returncode,'expected_success':success,'stdout_sha256':digest(p.stdout),'stderr_sha256':digest(p.stderr)})
        return p
    math=[]
    for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
        run(flags,['verify_package.py'])
        result=run(flags,['check_math.py']);math.append(json.loads(result.stdout))
        rebuilt=td/('rebuilt-'+mode+'.zip');run(flags,['build_archive.py','--output',str(rebuilt)])
        if rebuilt.read_bytes()!=archive.read_bytes():raise RuntimeError('Clean builder differs')
        run(flags,['verify_package.py'])
        run(flags,['verify_package.py','--require-deposit'],False)
        for fault in ['normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign']:run(flags,['check_math.py','--mutation',fault],False)
        run(flags,[str(P/'verify_package.py'),'--require-deposit'])
    if math[0]!=math[1]:raise RuntimeError('Normal/optimized complete math results differ')
    run([],[str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'zenodo-deposit.json')])
    for n in names:
        if (clean/n).read_bytes()!=(P/n).read_bytes():raise RuntimeError('Clean input changed')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ACCEPT_PREPARED_CREDITED_EDITION_PENDING_TWO_NEW_COMPLETE_WHOLE_REVIEWS','complete_paper_preparation_report_README_and_all_six_current_code_files_read':True,'paper_math_and_source_credit_consistent_with_root_adoptions':True,'all_seven_current_pdf_pages_actually_viewed':visual,'preparation_outputs_rehashed':len(outputs),'all_prior_inputs_rehashed':len(inputs),'source_equal_copies':len(copies),'individual_exclusions':len(exclusions),'archive_members_independently_rehashed':len(names),'independent_CLOSED_archive_rebuild_byte_identical':True,'all_four_native_metadata_objects_equal':True,'actual_commands':commands,'new_full_reviews_completed':0,'minimum_new_full_reviews':2,'actionable_findings_by_root':[],'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_PREPRINT_REVIEW_01.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['actual_commands','all_seven_current_pdf_pages_actually_viewed']}))
