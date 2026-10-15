#!/usr/bin/env python3
"""Independent custody/archive checks. Writes only inside package_01."""
from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, stat, datetime, subprocess, time

D=Path(__file__).resolve().parent
A=D.parent.parent
C=D/'frozen/candidate'
def require(ok, message):
    if not ok: raise RuntimeError(message)
def digest(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
checks={}
for name,base,key in [('INPUT_PINS.json',A,'files'),('OUTPUT_PINS.json',C,'files')]:
    rows=load(C/name)[key]
    for row in rows:
        b=(base/row['path']).read_bytes()
        require(len(b)==row['bytes'] and digest(b)==row['sha256'],name+' '+row['path'])
    checks[name]=len(rows)
copies=load(C/'EVIDENCE_COPY_MAP.json')['copies']
for row in copies:
    b=(C/row['package_path']).read_bytes()
    require(len(b)==row['bytes'] and digest(b)==row['sha256'],'copied bytes '+row['package_path'])
    require(b==(A/row['source_audit_relative']).read_bytes(),'copy provenance '+row['package_path'])
require(len(copies)==97 and sum(x['package_path'].startswith('evidence/submitted/') for x in copies)==9,'copies count including nine originals')
checks['exact_evidence_copies_including_nine_originals']=97
allow=load(C/'ALLOWLIST.json')['members']; man=load(C/'MANIFEST.json')
require(allow==sorted(set(allow)) and len(allow)==142,'allowlist')
require(man['members']==allow+['MANIFEST.json'],'manifest list appended self')
require([r['path'] for r in man['entries']]==allow,'manifest entries')
for row in man['entries']:
    b=(C/row['path']).read_bytes()
    require(len(b)==row['bytes'] and digest(b)==row['sha256'],'manifest hash')
require('MANIFEST.json' not in [x['path'] for x in man['entries']],'no self hash')
Z=C/'pr1047_supportkit_v1.0.zip'
E=D/'clean_extraction';E.mkdir(exist_ok=True)
with zipfile.ZipFile(Z) as z:
    require(z.testzip() is None,'CRC')
    names=z.namelist(); require(names==sorted(allow+['MANIFEST.json']) and len(names)==143,'archive member set/order/count')
    for info in z.infolist():
        p=PurePosixPath(info.filename)
        require(not p.is_absolute() and all(v not in ('','.','..') for v in p.parts) and '\\' not in info.filename,'unsafe path')
        require(stat.S_ISREG(info.external_attr>>16) and stat.S_IMODE(info.external_attr>>16)==0o644,'regular 0644')
        require(info.create_system==3 and info.compress_type==zipfile.ZIP_STORED and info.date_time==(2026,10,14,0,0,0),'deterministic info')
        b=z.read(info); require(b==(C/info.filename).read_bytes(),'archive byte match')
    require(not any(p.endswith('.pdf') or p.startswith('sources/') or '/sources/raw/' in p or 'zenodo-deposit' in p or '__pycache__' in p for p in names),'excluded artifact')
    z.extractall(E)
checks['archive']={'members':143,'manifest_entries':142,'safe':True,'crc':True,'regular_mode':'0644','stored':True,'fixed_timestamp':'2026-10-14T00:00:00','sorted':True,'byte_equal_all_members':True,'sha256':digest(Z.read_bytes())}
wrapper=load(C/'zenodo_metadata.json');bare=load(C/'.zenodo.json');external=load(C/'zenodo-deposit.json')
require(set(wrapper)=={'metadata'} and bare==wrapper['metadata']==external['metadata'],'all three metadata normalized same')
require(set(external)=={'metadata','files'} and external['files']==[{'path':'paper/matroid_rank_obstruction.pdf'},{'path':'pr1047_supportkit_v1.0.zip'}],'external files')
require('zenodo-deposit.json' not in names and not (E/'zenodo-deposit.json').exists(),'descriptor deliberately external')
checks['metadata']={'all_three_equal':True,'wrapper_bare_external_shapes_correct':True,'external_files_correct':True,'external_descriptor_absent_from_zip':True}
executions=[]
def run(label,cmd):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    p=subprocess.run(cmd,cwd=E,capture_output=True)
    (D/(label+'.stdout')).write_bytes(p.stdout);(D/(label+'.stderr')).write_bytes(p.stderr)
    row={'label':label,'command':cmd,'cwd':str(E),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit':p.returncode,'stdout_sha256':digest(p.stdout),'stderr_sha256':digest(p.stderr)}
    executions.append(row);print(json.dumps(row),flush=True);return p
require(run('verify',['python3','-I','-B','scripts/verify_package.py']).returncode==0,'clean verifier failed')
(E/'verification_output').mkdir(exist_ok=True)
require(run('checker',['python3','-I','-B','scripts/check_mathematics.py','--output-dir','verification_output']).returncode==0,'clean checker failed')
fresh=load(E/'verification_output/CHECKER_RESULTS.json');stored=load(C/'validation/fresh_finite/CHECKER_RESULTS.json');historical=load(C/'evidence/reviews/basis_family_01/CHECKER_RESULTS.json')
excluded=['started_utc','completed_utc','checker_sha256']
project=lambda x:{k:v for k,v in x.items() if k not in excluded}
require(project(fresh)==project(stored)==project(historical),'entire checker result metadata projection')
checks['checker']={'total_matroids':sum(r['matroids'] for r in fresh['exhaustive_results']),'full_projection_equal_to_both_recorded_final_runs':True,'projection_removed_only':excluded,'scope':{'all_matroids_n':'1..5','uniform_sqrt_n':'1..200','uniform_rational_m':'1..30','cube_m':'1..100','sqrt_direct_pairs_n':'0..8','rational_direct_pairs_m':'1..3'},'finite_only':True,'no_original_edition_executable_replay':True}
require(run('build',['python3','-I','-B','scripts/build_supportkit.py']).returncode==0,'clean builder failed')
require((E/'MANIFEST.json').read_bytes()==(C/'MANIFEST.json').read_bytes(),'rebuilt manifest')
require((E/Z.name).read_bytes()==Z.read_bytes(),'deterministic entire ZIP equality')
require(run('verify_after_build',['python3','-I','-B','scripts/verify_package.py']).returncode==0,'post-build verifier')
require(run('tectonic',['tectonic','--outdir','paper','paper/matroid_rank_obstruction.tex']).returncode==0,'README Tectonic build failed')
checks['clean_execution']={'README_verifier_checker_and_tectonic_executed':True,'builder_executed':True,'builder_exact_zip_equal':True,'generated_outputs_excluded_by_allowlist':True,'executions':executions}
(D/'PACKAGE_CHECKS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks},indent=2)+'\n')
print('ALL_CUSTODY_AND_REPLAY_CHECKS_COMPLETE',flush=True)
