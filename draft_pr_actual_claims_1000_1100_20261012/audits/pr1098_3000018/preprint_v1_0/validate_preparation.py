"""Actual clean-copy README execution and negative-path preparation evidence."""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import hashlib,json,os,shutil,subprocess,tempfile,zipfile,datetime
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
REPO=AUDIT.parents[2]
VALID=ROOT/'validation'
VALID.mkdir(exist_ok=True)
records=[]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    (VALID/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def run(args,expect=0):
    r=subprocess.run(args,capture_output=True,text=True)
    row={'argv':list(map(str,args)),'exit_code':r.returncode,
         'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),
         'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()}
    records.append(row)
    require((r.returncode==0) if expect==0 else (r.returncode!=0),
            'unexpected command result: '+str(args)+'\n'+r.stdout+'\n'+r.stderr)
    return r
def inventory(root):
    return {str(p.relative_to(root)):sha(p) for p in root.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts}
freeze=json.loads((ROOT/'INPUT_FREEZE.json').read_text())
for row in freeze['entries']:
    p=AUDIT/row['path']
    require(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],
            'prior baseline mismatch: '+str(p))
auth=[]
for p in sorted((AUDIT/'submitted').iterdir()):
    data=subprocess.check_output(['git','show','f37a3ff66595fcf75bb18bf859be8594c3662242:unsolved_math_prioritization/attempts/3000018/'+p.name],cwd=REPO)
    require(data==p.read_bytes(),'actual Git original mismatch')
    auth.append({'path':p.name,'bytes':len(data),'sha256':sha(p),'actual_git_equal':True})
selection=json.loads((ROOT/'CUSTODY_SELECTION.json').read_text())['entries']
require(len(selection)==len(freeze['entries']) and {r['path'] for r in selection}=={r['path'] for r in freeze['entries']},'complete custody partition')
for row in selection:
    if row['disposition']=='EXACT_AUTHORED_COPY':
        require((ROOT/row['destination']).read_bytes()==(AUDIT/row['path']).read_bytes(),'exact history copy')
save('ORIGINAL_INPUT_RECHECK.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'prior_inputs_unchanged':len(freeze['entries']),'actual_git':auth,'exact_copies':sum(r['disposition']=='EXACT_AUTHORED_COPY' for r in selection),
 'exclusions':sum(r['disposition']=='OMITTED' for r in selection)})
scratch=Path(tempfile.mkdtemp(prefix='pr1098-clean-preparation-',dir='/private/tmp'))
try:
    kit=scratch/'kit';kit.mkdir()
    with zipfile.ZipFile(ROOT/'pr1098_support_v1_0.zip') as z:
        require(len(z.namelist())==len(set(z.namelist())),'unique archive names')
        for name in z.namelist():
            require(not name.startswith('/') and '..' not in Path(name).parts,'safe member names')
        z.extractall(kit)
    for name in ('paper.pdf','pr1098_support_v1_0.zip'):shutil.copyfile(ROOT/name,kit/name)
    protected=inventory(kit)
    outputs=[]
    for optimized in (False,True):
        cmd=[sys.executable]+(['-O'] if optimized else [])+['-B']
        verification=run(cmd+[str(kit/'code/verify_kit.py')])
        controls=run(cmd+[str(kit/'code/run_checks.py')])
        outputs.append(controls.stdout)
        save('CLEAN_CHECKS_'+('optimized' if optimized else 'normal')+'.json',json.loads(controls.stdout))
        run(cmd+[str(kit/'code/run_checks.py'),'--invalid'],1)
        archive=scratch/('new-'+str(optimized)+'.zip')
        run(cmd+[str(kit/'code/rebuild_archive.py'),'--output',str(archive)])
        require(archive.read_bytes()==(ROOT/'pr1098_support_v1_0.zip').read_bytes(),'closed ZIP exact reproduction')
        build=scratch/('pdf-'+str(optimized))
        result=run(cmd+[str(kit/'code/build_pdf.py'),'--out-dir',str(build)])
        require((build/'paper.pdf').read_bytes()==(ROOT/'paper.pdf').read_bytes(),'canonical PDF exact reproduction')
        save('REAL_PDF_BUILD_'+('optimized' if optimized else 'normal')+'.json',
             {'result':json.loads(result.stdout),'paper_log_sha256':sha(build/'paper.log'),
              'log':(build/'paper.log').read_text(errors='replace'),
              'canonical_bytes_equal':True,'compiler':subprocess.check_output(['tectonic','--version'],text=True).strip()})
    require(outputs[0]==outputs[1],'complete normal/optimized diagnostic JSON')
    fault_cases=[]
    # Existing outside leaves, including a hardlink to a protected input.
    existing=scratch/'existing';existing.write_bytes(b'untouched')
    existing_dir=scratch/'existing-dir';existing_dir.mkdir()
    leaf_link=scratch/'leaf-link';leaf_link.symlink_to(existing)
    broken=scratch/'broken-link';broken.symlink_to(scratch/'absent')
    aliasdir=scratch/'aliasdir';aliasdir.symlink_to(kit,target_is_directory=True)
    hard=scratch/'hard-output';os.link(existing,hard)
    casekit=Path(str(kit).upper())
    case_actual=os.path.samefile(casekit,kit) if casekit.exists() else False
    targets=[('existing-file',existing),('existing-directory',existing_dir),
             ('leaf-symlink',leaf_link),('broken-leaf',broken),
             ('symlink-ancestor',aliasdir/'created'),('parent-traversal',scratch/'kit'/'..'/'created'),
             ('relative',Path('relative-created')),('protected-kit',kit/'created'),
             ('protected-original',AUDIT/'must-not-create-from-preparation'),('hardlinked-leaf',hard)]
    if case_actual:targets.append(('physical-case-alias',casekit/'created'))
    for optimized in (False,True):
        cmd=[sys.executable]+(['-O'] if optimized else [])+['-B']
        for writer,flag in (('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')):
            for label,target in targets:
                run(cmd+[str(kit/'code'/writer),flag,str(target)],1)
                fault_cases.append({'optimized':optimized,'writer':writer,'fault':label,'rejected':True})
        # Introduce the source hardlink only for these separate input faults;
        # it must not mask a failure of the preceding output-path guards.
        input_partner=scratch/'tex-input-hardlink';os.link(kit/'paper.tex',input_partner)
        for writer,flag in (('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')):
            target=scratch/('hardinput-'+writer+str(optimized))
            run(cmd+[str(kit/'code'/writer),flag,str(target)],1)
            require(not target.exists(),'hardlinked input created output')
            fault_cases.append({'optimized':optimized,'writer':writer,'fault':'hardlinked-TeX-input','rejected':True})
        input_partner.unlink()
    hard.unlink()
    require(existing.read_bytes()==b'untouched','existing file overwritten')
    # Strict missing bindings and malformed native semantic metadata.
    for optimized in (False,True):
        cmd=[sys.executable]+(['-O'] if optimized else [])+['-B']
        path=kit/'ARTIFACT_BINDINGS.json';raw=path.read_bytes();path.unlink()
        run(cmd+[str(kit/'code/verify_kit.py')],1);path.write_bytes(raw)
        fault_cases.append({'optimized':optimized,'fault':'missing-required-PDF-binding','rejected':True})
        path=kit/'metadata.json';raw=path.read_bytes();obj=json.loads(raw);obj['title']='corrupted title';path.write_text(json.dumps(obj))
        run(cmd+[str(kit/'code/verify_kit.py')],1);path.write_bytes(raw)
        fault_cases.append({'optimized':optimized,'fault':'semantic-native-metadata','rejected':True})
        # Bootstrap manifest aliases are rejected before JSON parsing.
        manifest=kit/'MANIFEST.json';saved=scratch/('manifest-save-'+str(optimized));manifest.rename(saved)
        manifest.symlink_to(saved)
        for writer,flag in (('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')):
            target=scratch/('bootstrap-link-'+writer+str(optimized))
            run(cmd+[str(kit/'code'/writer),flag,str(target)],1)
            require(not target.exists(),'bootstrap link created output')
            fault_cases.append({'optimized':optimized,'writer':writer,'fault':'bootstrap-symlink','rejected':True})
        run(cmd+[str(kit/'code/verify_kit.py')],1)
        manifest.unlink();saved.rename(manifest)
        partner=scratch/('manifest-hard-'+str(optimized));os.link(manifest,partner)
        for writer,flag in (('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')):
            target=scratch/('bootstrap-hard-'+writer+str(optimized))
            run(cmd+[str(kit/'code'/writer),flag,str(target)],1)
            require(not target.exists(),'bootstrap hardlink created output')
            fault_cases.append({'optimized':optimized,'writer':writer,'fault':'bootstrap-hardlink','rejected':True})
        run(cmd+[str(kit/'code/verify_kit.py')],1);partner.unlink()
        path=kit/'MANIFEST.json';raw=path.read_bytes()
        path.write_bytes(b'{"entries":[],"entries":[]}')
        run(cmd+[str(kit/'code/verify_kit.py')],1);path.write_bytes(raw)
        fault_cases.append({'optimized':optimized,'fault':'duplicate-bootstrap-JSON-key','rejected':True})
        run(cmd+[str(kit/'code/verify_kit.py')])
    require(inventory(kit)==protected,'protected extraction bytes changed')
    for row in freeze['entries']:require(sha(AUDIT/row['path'])==row['sha256'],'old input changed after validation')
    native=run([sys.executable,'-B',str(REPO/'zenodo_deposit_tool/zenodo.py'),'check',str(ROOT/'publication/zenodo-deposit.json')])
    save('REPOSITORY_NATIVE_LOCAL_CHECK.json',{'stdout':native.stdout,'stderr':native.stderr,'exit_code':native.returncode,'network_action':False})
    save('CLEAN_REPRODUCTION.json',{'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'commands':records,'command_count':len(records),'fault_cases':fault_cases,
         'physical_case_alias_samefile':case_actual,'protected_extraction_files':len(protected),
         'protected_extraction_unchanged':True,'prior_inputs_unchanged':len(freeze['entries']),
         'normal_optimized_complete_JSON_equal':True,'real_PDF_both_modes_equal_canonical':True,
         'closed_ZIP_both_modes_equal_canonical':True})
    print(json.dumps({'status':'PASS','commands':len(records),'faults':len(fault_cases),'physical_case_alias_samefile':case_actual}))
finally:
    pins=[{'path':str(p.relative_to(scratch)),'bytes':p.stat().st_size,'sha256':sha(p)}
          for p in scratch.rglob('*') if p.is_file() and not p.is_symlink()]
    # Only this task's one disposable extraction/build tree is removed.
    shutil.rmtree(scratch)
    save('OWN_SCRATCH_CLEANUP.json',{'path':str(scratch),'removed':True,'regular_files':pins})
