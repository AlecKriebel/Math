#!/usr/bin/env python3
"""Independent actual clean-extraction checks; writes only this review directory."""
from pathlib import Path
import subprocess,sys,os,json,hashlib,tarfile,shutil,copy,datetime
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent;CANDIDATE=BASE/'preprint_v1_0';PRIVATE=HERE/'private'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
results=[]
def run(tag,args,cwd,expected=0):
 p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
 (HERE/(tag+'_STDOUT.txt')).write_text(p.stdout);(HERE/(tag+'_STDERR.txt')).write_text(p.stderr)
 r={'tag':tag,'command':args,'cwd':str(cwd.relative_to(HERE)) if HERE in cwd.parents else str(cwd),'returncode':p.returncode,'expected_returncode':expected,'matched':(p.returncode==0 if expected==0 else p.returncode!=0),'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()}
 results.append(r)
 if not r['matched']:raise RuntimeError('Unexpected status '+tag+': '+p.stderr)
 return p
# Local supplied kit copy preserves candidate and its receipts.
full=PRIVATE/'full';shutil.copytree(CANDIDATE,full,ignore=shutil.ignore_patterns('tmp','__pycache__'))
run('FULL_REQUIRE_BEFORE',[sys.executable,'verify_package.py','--require-deposit'],full)
run('FULL_BUILD',[sys.executable,'build_archive.py'],full)
run('FULL_REQUIRE_AFTER',[sys.executable,'verify_package.py','--require-deposit'],full)
original=(CANDIDATE/'supportkit-v1.0.tar.gz').read_bytes()
if (full/'supportkit-v1.0.tar.gz').read_bytes()!=original:raise RuntimeError('Full build not byte identical')
# Directly extracted distributed kit, no wrapper and no archive.
clean=PRIVATE/'clean';clean.mkdir()
with tarfile.open(CANDIDATE/'supportkit-v1.0.tar.gz','r:gz') as t:
 members=t.getmembers()
 for m in members:
  if not m.isfile() or '..' in Path(m.name).parts or Path(m.name).is_absolute():raise RuntimeError('Unsafe supplied tar')
 t.extractall(clean,filter='data')
kit=clean/'rank_one_uniqueness_v1_0'
run('CLEAN_VERIFY_BEFORE',[sys.executable,'verify_package.py'],kit)
run('CLEAN_REQUIRE_ABSENT',[sys.executable,'verify_package.py','--require-deposit'],kit,1)
run('CLEAN_BUILD',[sys.executable,'build_archive.py'],kit)
run('CLEAN_VERIFY_AFTER',[sys.executable,'verify_package.py'],kit)
run('CLEAN_OPTIMIZED',[sys.executable,'-O','verify_package.py'],kit)
run('CLEAN_REQUIRE_ABSENT_AFTER',[sys.executable,'verify_package.py','--require-deposit'],kit,1)
if (kit/'supportkit-v1.0.tar.gz').read_bytes()!=original:raise RuntimeError('Clean build not byte identical')
shutil.copy2(CANDIDATE/'zenodo-deposit.json',kit/'zenodo-deposit.json')
run('CLEAN_REQUIRE_PRESENT',[sys.executable,'verify_package.py','--require-deposit'],kit)
run('CLEAN_REQUIRE_PRESENT_OPTIMIZED',[sys.executable,'-O','verify_package.py','--require-deposit'],kit)
run('CLEAN_TEX_BUILD',['tectonic','--outdir','output/pdf','paper.tex'],PRIVATE/'tex_build' if False else kit)
# PDF rebuild is deliberately confined to the disposable kit and recorded separately.
run('REBUILT_PDFINFO',['pdfinfo','output/pdf/paper.pdf'],kit)
# Fault probes use the full baseline copy with pinned supplied PDF.
faultdir=PRIVATE/'fault';shutil.copytree(full,faultdir)
wrapper=faultdir/'zenodo-deposit.json';good=wrapper.read_bytes();obj=json.loads(good)
controls=[]
def probe(tag,change,restore):
 change()
 for mode in ['normal','optimized']:
  for required in [False,True]:
   args=[sys.executable]+(['-O'] if mode=='optimized' else [])+['verify_package.py']+(['--require-deposit'] if required else [])
   r=run('FAULT_'+tag+'_'+mode+'_'+('required' if required else 'default'),args,faultdir,1)
 controls.append({'fault':tag,'modes':4,'all_rejected':True})
 restore()
def wrapper_fault(tag,o):probe(tag,lambda:wrapper.write_text(json.dumps(o)),lambda:wrapper.write_bytes(good))
for tag,mut in [('title',lambda x:x['metadata'].update(title='incorrect')),('metadata_bool',lambda x:x['metadata'].update(publication_date=False)),('extra_field',lambda x:x.update(extra=1)),('metadata_missing',lambda x:x.pop('metadata')),('attachment_wrong_name',lambda x:x['files'][0].update(name='wrong.pdf')),('attachment_wrong_path',lambda x:x['files'][0].update(path='paper.tex')),('attachment_swapped',lambda x:x['files'].reverse()),('files_missing',lambda x:x['files'].pop()),('files_extra',lambda x:x['files'].append(x['files'][0])),('metadata_type',lambda x:x.update(metadata=[])),('files_type',lambda x:x.update(files={}))]:
 x=copy.deepcopy(obj);mut(x);wrapper_fault(tag,x)
probe('duplicate_wrapper_key',lambda:wrapper.write_text('{"metadata":{},"metadata":{},"files":[]}'),lambda:wrapper.write_bytes(good))
probe('wrapper_symlink',lambda:(wrapper.unlink(),wrapper.symlink_to(full/'zenodo-deposit.json')),lambda:(wrapper.unlink(),wrapper.write_bytes(good)))
probe('wrapper_directory',lambda:(wrapper.unlink(),wrapper.mkdir()),lambda:(wrapper.rmdir(),wrapper.write_bytes(good)))
for tag,rel in [('content_changed','paper.tex'),('archive_changed','supportkit-v1.0.tar.gz'),('historic_output_changed','evidence/reviews/package_01/VERDICT.json'),('original_changed','evidence/original/submitted/PROOF.md')]:
 p=faultdir/rel;b=p.read_bytes();probe(tag,lambda p=p,b=b:p.write_bytes(b+b'\n'),lambda p=p,b=b:p.write_bytes(b))
p=faultdir/'evidence/reviews/package_02/VERDICT.json';b=p.read_bytes();probe('historic_output_absent',lambda:p.unlink(),lambda:p.write_bytes(b))
p=faultdir/'unmanifested.md';probe('unmanifested_content',lambda:p.write_text('rogue\n'),lambda:p.unlink())
# Rehashed pending status may not promote readiness; challenge beyond simple byte pins.
p=faultdir/'STATUS.json';b=p.read_bytes();state=json.loads(b);state['publication_ready']=True;state['all_issues_resolved']=True
p.write_text(json.dumps(state,indent=2)+'\n');run('PREPARE_PENDING_FAULT',[sys.executable,'build_archive.py'],faultdir)
for mode in ['normal','optimized']:
 for required in [False,True]:run('FAULT_pending_promoted_'+mode+'_'+('required' if required else 'default'),[sys.executable]+(['-O'] if mode=='optimized' else [])+['verify_package.py']+(['--require-deposit'] if required else []),faultdir,1)
controls.append({'fault':'pending_promoted_after_rehash','modes':4,'all_rejected':True})
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':results,'controls':controls,'all_expected_statuses':all(r['matched'] for r in results),'original_archive_sha256':hashlib.sha256(original).hexdigest(),'archive_bytes':len(original),'archive_members':len(members),'clean_and_full_build_byte_identical':True,'clean_extracted_content_files':len(json.loads((full/'CURRENT_INTEGRITY.json').read_text())['files']),'normal_and_optimized_supported':True,'isolated_mode_excluded':'python -I suppresses local imports and is not a documented interface'}
(HERE/'PACKAGE_CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k not in ['runs','controls']},indent=2))
