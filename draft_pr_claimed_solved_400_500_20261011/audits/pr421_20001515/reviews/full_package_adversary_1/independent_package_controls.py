"""Read-only candidate audit; mutations limited to owned disposable copies."""
from pathlib import Path
import ast, datetime, hashlib, json, os, shutil, subprocess, sys, zipfile

HERE=Path(__file__).resolve().parent
CASE=HERE.parent.parent
TMP=HERE/'tmp'; TMP.mkdir(exist_ok=True)
ENV=dict(os.environ,TMPDIR=str(TMP))
ROOT=HERE/'clean extraction with spaces'/'verification'

# Recreate the reviewed public archive, making this audit script rerunnable
# after disposal of its previous fixtures.
if ROOT.exists(): shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)
with zipfile.ZipFile(CASE/'publication/aim_5_2_verification.zip') as archive:
    names=archive.namelist()
    if len(names)!=len(set(names)): raise RuntimeError('duplicate archive name')
    for name in names:
        path=Path(name)
        if path.is_absolute() or '..' in path.parts or str(path)!=name:
            raise RuntimeError('unsafe archive name')
    archive.extractall(ROOT)
for opt in [False,True]:
    run=subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+
                       [str(ROOT/'verify_bundle.py')],cwd=HERE,env=ENV,
                       text=True,capture_output=True,timeout=120)
    if run.returncode or run.stderr: raise RuntimeError('full driver failed: '+run.stderr)
    mode='optimized' if opt else 'normal'
    (HERE/('driver_'+mode+'.stdout.json')).write_text(run.stdout)
    (HERE/('driver_'+mode+'.stderr.txt')).write_text(run.stderr)

def need(x,msg):
    if not x: raise RuntimeError(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def command(root,opt=False):
    return subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+
                          [str(root/'verify_bundle.py'),'--baseline-only'],
                          cwd=HERE,env=ENV,text=True,capture_output=True,timeout=90)

def rehash(root,name):
    for mf in ['MANIFEST.json','PUBLIC_OUTPUT_WHITELIST.json']:
        doc=json.loads((root/mf).read_text())
        for row in doc['files']:
            if row['path']==name:
                row['sha256']=sha(root/name);row['bytes']=(root/name).stat().st_size
        (root/mf).write_text(json.dumps(doc,indent=2)+'\n')
    doc=json.loads((root/'PUBLIC_OUTPUT_WHITELIST.json').read_text())
    for row in doc['files']:
        if row['path']=='MANIFEST.json':
            row['sha256']=sha(root/'MANIFEST.json');row['bytes']=(root/'MANIFEST.json').stat().st_size
    (root/'PUBLIC_OUTPUT_WHITELIST.json').write_text(json.dumps(doc,indent=2)+'\n')

def mutate(root,mode):
    if mode=='extra_file': (root/'foreign.txt').write_text('private fixture')
    elif mode=='extra_empty_directory': (root/'private_fixture').mkdir()
    elif mode=='missing_baseline': (root/'packet/checks.json').unlink()
    elif mode=='symlink_packet':
        p=root/'packet/ATTEMPT_1.md'; backup=root.parent/(root.name+' target proof');backup.write_bytes(p.read_bytes());p.unlink();p.symlink_to(backup)
    elif mode=='duplicate_manifest_key':
        p=root/'MANIFEST.json';t=p.read_text();p.write_text(t.replace('{','{"schema_version":1,',1))
    elif mode=='rehash_tampered_proof':
        p=root/'packet/ATTEMPT_1.md';p.write_bytes(p.read_bytes()+b'\n');rehash(root,'packet/ATTEMPT_1.md')
    elif mode=='rehash_tampered_saved_success':
        p=root/'packet/checks.json';d=json.loads(p.read_text());d['Z_link']['vertices']=15;p.write_text(json.dumps(d));rehash(root,'packet/checks.json')
    else: raise ValueError(mode)

controls=[]
for mode in ['extra_file','extra_empty_directory','missing_baseline','symlink_packet',
             'duplicate_manifest_key','rehash_tampered_proof','rehash_tampered_saved_success']:
    for opt in [False,True]:
        p=HERE/'owned control fixtures with spaces'/(mode+(' O' if opt else ' normal'))
        p.parent.mkdir(exist_ok=True)
        if p.exists(): shutil.rmtree(p)
        shutil.copytree(ROOT,p)
        mutate(p,mode); result=command(p,opt)
        need(result.returncode!=0 and not result.stdout,'integrity corruption produced successful stdout')
        need(result.stderr.startswith('VERIFICATION FAILED: '),'incidental failure')
        controls.append({'control':mode,'mode':'-O' if opt else 'normal','returncode':result.returncode,
                         'stdout_empty':True,'diagnostic':result.stderr.strip()})

# Independently verify baseline and negative-control reports from both full runs.
full=[]
for mode in ['normal','optimized']:
    d=json.loads((HERE/('driver_'+mode+'.stdout.json')).read_text())
    need(d['status']=='PASS' and d['integrity']['file_count']==24,'driver baseline inventory')
    need(len(d['baseline_runs'])==6,'all baseline modes')
    need(len(d['negative_controls']['mathematical_data'])==14,'all seven data controls both modes')
    need(len(d['negative_controls']['sha_tampering'])==3,'all three integrity controls')
    need(all(x['saved_outputs_deleted_before_run'] for x in d['baseline_runs']),'fresh baseline artifacts')
    need(all(x['result_files_absent'] and x['stdout_empty'] and x['exit_code']!=0
             for x in d['negative_controls']['mathematical_data']),'no stale success output')
    full.append({'mode':mode,'baseline_count':6,'data_rejections':14,'integrity_rejections':3,
                 'relocated_subruns':d['relocated_bundle']['clean_normal_and_O_program_runs']})

manifest=json.loads((CASE/'global_candidate/packet-update-manifest.json').read_text())
rows=manifest['entries'];need(len(rows)==53,'global update count')
candidate=json.loads((CASE/'PREPRINT_PACKAGE_CANDIDATE.json').read_text())
need({x['local_path']:x['sha256'] for x in rows}==candidate['candidate_files'],'global candidate mapping')
prefix='unsolved_math_prioritization/attempts/20001515/'
need(all(x['remote_path'].startswith(prefix) for x in rows),'other case path')
need(len({x['remote_path'] for x in rows})==53,'duplicate remote path')
need(all(sha(CASE/x['local_path'])==x['sha256'] for x in rows),'mapping data drift')

# Scan all delivered text and code. Potential matches are retained only by location,
# never token contents. Hash/ORCID evidence strings are not secrets.
scan=[]; bodies=[]
for family in ['source','verification']:
    with zipfile.ZipFile(CASE/'publication'/('aim_5_2_'+family+'.zip')) as z:
        for name in z.namelist():
            data=z.read(name)
            need(b'\x00' not in data,'unexpected binary foreign body')
            text=data.decode('utf-8')
            need(not any(s in name.split('/') for s in ['private','private_sources','private_cases','__pycache__','.venv']), 'private archive member')
            for marker in ['BEGIN PRIVATE KEY','BEGIN RSA PRIVATE KEY','Bearer ','ghp_','github_pat_','sk-proj-']:
                if marker in text: scan.append({'family':family,'path':name,'marker_kind':marker})
            bodies.append({'family':family,'path':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
need(not scan,'potential credential payload')

result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
        'additional_integrity_controls':controls,'full_driver_summary':full,
        'global_mapping_exact53':True,'all_remote_paths_selected_case':True,
        'archive_members_scanned':bodies,'credential_markers':scan,
        'scope':'Owned fixtures only; finite reproducibility/integrity does not prove global mathematics or priority.'}
(HERE/'INDEPENDENT_PACKAGE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
shutil.rmtree(HERE/'owned control fixtures with spaces')
shutil.rmtree(ROOT.parent)
print(json.dumps({'status':'PASS','additional_rejections':len(controls),'global_rows':len(rows),
                  'archive_text_members':len(bodies),'secret_marker_count':len(scan)}))
