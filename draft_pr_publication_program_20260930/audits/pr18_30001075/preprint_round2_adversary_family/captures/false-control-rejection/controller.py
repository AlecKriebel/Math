#!/usr/bin/env python3
"""Independent archive and process audit. Writes exclusively in reviewer directory."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, stat, subprocess, sys, time, zipfile
if sys.flags.optimize: raise RuntimeError('Audit requires nonoptimized execution')
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT.parent/'preprint_v1'
PRODUCTION=ROOT.parent/'root_final_package_20261003/zenodo-deposit.json'
PINS={
 'paper.tex':(24824,'2522ac0138de5e21067af8c16e6749b3a9d3cd01f12bdb929cca87cb6baeabb6'),
 'common_tangent_nullness.pdf':(92307,'80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327'),
 'common_tangents_null_locus_v1.zip':(182613,'1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5'),
 'ARCHIVE_MANIFEST.json':(None,'595bf1903377f68b6836f345bdfa252d6e65342c4d5cce0c67f02fc9f2b333b2'),
 'ZENODO_UPLOAD_MANIFEST.json':(None,'5d45d5b3ba4137ddfa19efd2b2a8c63055cb308942b8cc9a6c01019d4f0ed119'),
 'source/CANDIDATE.md':(20728,'8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12')}
def sha(x): return hashlib.sha256(x).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def recfile(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def gate(v,msg):
 if not v:raise RuntimeError(msg)
checks={}
for name,(size,h) in PINS.items():
 r=recfile(PACKAGE/name);gate(r['sha256']==h and (size is None or r['bytes']==size),'pin mismatch '+name);checks[name]=r
production=recfile(PRODUCTION)
gate(production['sha256']=='fc0d603caee348ebf8442119b28733349779f53d155681a9f1342f67b9ea291a','production pin')
meta=json.loads((PACKAGE/'zenodo_metadata.json').read_bytes())
deposit=json.loads(PRODUCTION.read_bytes())
gate(deposit['metadata']==meta['metadata'],'metadata equality')
gate(deposit['files']==[{'path':'../preprint_v1/common_tangent_nullness.pdf'},{'path':'../preprint_v1/common_tangents_null_locus_v1.zip'}],'production file domain')
manifest=json.loads((PACKAGE/'ARCHIVE_MANIFEST.json').read_bytes())
ziprecs=[]
pristine=ROOT/'reproduction/pristine';pristine.mkdir(parents=True,exist_ok=False)
with zipfile.ZipFile(PACKAGE/'common_tangents_null_locus_v1.zip') as z:
 names=z.namelist();domain=sorted(manifest['payload_domain']+['ARCHIVE_MANIFEST.json'])
 gate(names==domain and len(names)==len(set(names)),'archive exact ordered unique domain')
 for i in z.infolist():
  gate(i.filename and not i.filename.startswith('/') and '..' not in Path(i.filename).parts,'archive safe path')
  gate(i.create_system==3 and i.external_attr>>16==0o100644 and i.date_time==(2026,10,3,0,0,0) and i.compress_type==zipfile.ZIP_STORED,'archive metadata '+i.filename)
  b=z.read(i.filename);gate(b==(PACKAGE/i.filename).read_bytes(),'archive/current byte agreement '+i.filename)
  if i.filename!='ARCHIVE_MANIFEST.json':
   gate(len(b)==manifest['entries'][i.filename]['bytes'] and sha(b)==manifest['entries'][i.filename]['sha256'],'entry hash/size '+i.filename)
  dest=pristine/i.filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
  ziprecs.append({'name':i.filename,'bytes':len(b),'sha256':sha(b),'full_mode':oct(i.external_attr>>16),'timestamp':i.date_time,'compression':i.compress_type})
(ROOT/'ARCHIVE_AUDIT.json').write_text(json.dumps({'UTC':stamp(),'actual_pid':os.getpid(),'python':sys.version,'optimization':sys.flags.optimize,'input_pins':checks,'production_manifest':production,'production_metadata_equal':True,'exact_two_files':True,'all_archive_entries_checked':ziprecs,'no_extra_or_private_members':True},indent=2)+'\n')
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','PYTHONHASHSEED':'0','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONIOENCODING':'utf-8'}
runs=[]
def run(label,case,filename='verify.py',extra=(),optimized=False,expected=0):
 f=ROOT/'captures'/label;f.mkdir(parents=True,exist_ok=False)
 target=case/filename;src=target.read_bytes();(f/'source.py').write_bytes(src);(f/'controller.py').write_bytes(Path(__file__).read_bytes())
 argv=[sys.executable]+(['-O'] if optimized else [])+['-B',str(target)]+list(extra)
 inputs={str(p.relative_to(case)):recfile(p) for p in sorted(case.rglob('*')) if p.is_file()}
 record={'label':label,'UTC_prelaunch':stamp(),'controller_pid':os.getpid(),'argv':argv,'cwd':str(case),'environment':env,'python':sys.version,'controller_optimization':sys.flags.optimize,'source_sha256':sha(src),'inputs':inputs,'expected_exit':expected}
 (f/'PRELAUNCH.json').write_text(json.dumps(record,indent=2)+'\n')
 t=time.perf_counter()
 with (f/'stdout.txt').open('wb') as out,(f/'stderr.txt').open('wb') as err:
  child=subprocess.Popen(argv,cwd=case,env=env,stdout=out,stderr=err)
  record['child_pid']=child.pid;record['UTC_launch_return']=stamp();(f/'LAUNCH.json').write_text(json.dumps(record,indent=2)+'\n')
  record['returncode']=child.wait()
 record['runtime_seconds']=time.perf_counter()-t;record['UTC_end']=stamp();record['source_unchanged']=target.read_bytes()==src
 for stream in ('stdout.txt','stderr.txt'):record[stream]=recfile(f/stream)
 record['expected_outcome']=(record['returncode']==0 if expected==0 else record['returncode']!=0)
 (f/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n');runs.append(record)
 gate(record['expected_outcome'] and record['source_unchanged'],'unexpected captured outcome '+label)
 return record

def case(label):
 p=ROOT/'reproduction'/label;shutil.copytree(pristine,p);return p
# Identical archive inputs are untouched by verification; reproduce before timestamp changes.
p=case('same_input_build')
run('same-input-build-1',p,'build_archive.py')
b1=(p/'common_tangents_null_locus_v1.zip').read_bytes();gate(sha(b1)==PINS['common_tangents_null_locus_v1.zip'][1],'same input build 1 byte identity')
run('same-input-build-2',p,'build_archive.py')
b2=(p/'common_tangents_null_locus_v1.zip').read_bytes();gate(b2==b1,'same input repeat identity')
run('positive',case('positive'))
run('optimized-rejection',case('optimized'),optimized=True,expected=1)
run('false-control-rejection',case('false'),extra=['--negative-control'],expected=1)
p=case('stale_source');(p/'paper.tex').write_bytes((p/'paper.tex').read_bytes()+b'\n% independent stale-source injection\n');run('stale-source-rejection',p,'build_archive.py',expected=1)
p=case('stale_candidate');(p/'source/CANDIDATE.md').write_bytes((p/'source/CANDIDATE.md').read_bytes()+b'\nindependent stale candidate\n');run('stale-candidate-rejection',p,expected=1)
p=case('stale_verifier');(p/'verify.py').write_bytes((p/'verify.py').read_bytes()+b'\n# independent stale-code injection\n');run('stale-verifier-rejection',p,'build_archive.py',expected=1)
p=case('stale_pdf');(p/'common_tangent_nullness.pdf').write_bytes((p/'common_tangent_nullness.pdf').read_bytes()+b'\n% independent stale-PDF injection\n');run('stale-pdf-rejection',p,'build_archive.py',expected=1)
p=case('stale_pdf_binding');b=json.loads((p/'PDF_BINDING.json').read_bytes());b['paper_sha256']='0'*64;(p/'PDF_BINDING.json').write_text(json.dumps(b));run('stale-pdf-binding-rejection',p,'build_archive.py',expected=1)
p=case('formal_fault');s=(p/'verify.py').read_text();needle='scale(mul(av[1],av[2]),-1)';gate(s.count(needle)==1,'formal fault target');(p/'verify.py').write_text(s.replace(needle,'scale(mul(av[1],av[2]),1)'));run('formal-sign-fault-rejection',p,expected=1)
# Independently exercising the supplied capture mechanism in a copied package.
p=case('portable_capture');run('portable-controller-positive',p,'run_capture.py',['independent-positive','verify']);
inner=json.loads((p/'captures/independent-positive/CAPTURE.json').read_bytes());gate(inner['child_pid']!=inner['controller_pid'] and inner['returncode']==0 and inner['outcome_as_expected'] and inner['source_unchanged'],'portable capture fields')
run('portable-controller-negative',p,'run_capture.py',['independent-negative','negative']);
inner=json.loads((p/'captures/independent-negative/CAPTURE.json').read_bytes());gate(inner['returncode']!=0 and inner['outcome_as_expected'],'portable negative fields')
(ROOT/'PROCESS_AUDIT.json').write_text(json.dumps({'UTC':stamp(),'actual_pid':os.getpid(),'same_input_zip_byte_identical':True,'same_input_repeat_byte_identical':True,'run_count':len(runs),'runs':runs,'scope':'Finite controls and packaging audit only; no continuum or priority certification.'},indent=2)+'\n')
print(json.dumps({'status':'PASS_INDEPENDENT_PACKAGE_CONTROLS','runs':[(r['label'],r['returncode'],r['child_pid'],r['runtime_seconds']) for r in runs],'same_input_zip_sha256':sha(b1)},indent=2))
