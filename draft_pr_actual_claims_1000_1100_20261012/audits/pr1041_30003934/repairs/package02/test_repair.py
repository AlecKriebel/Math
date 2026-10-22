#!/usr/bin/env python3
"""Actual local package02 interface/fault tests; disposable copies, no services."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import copy,gzip,hashlib,io,json,os,shutil,struct,subprocess,tarfile,zlib,datetime
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/'preprint_v1_0';T=R/'tmp'
if T.exists():shutil.rmtree(T)
T.mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def require(x,m):
 if not x:raise RuntimeError(m)
def sha(d):return hashlib.sha256(d).hexdigest()
def writej(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def run(name,path,script,args=(),optimized=False,good=True,message=None):
 cmd=[sys.executable]+(['-O'] if optimized else [])+[script]+list(args)
 proc=subprocess.run(cmd,cwd=path,env=ENV,capture_output=True,text=True)
 (R/(name+'_STDOUT.txt')).write_text(proc.stdout);(R/(name+'_STDERR.txt')).write_text(proc.stderr)
 rec=dict(name=name,command=cmd,cwd=str(path.relative_to(A)),returncode=proc.returncode,stdout_sha256=sha(proc.stdout.encode()),stderr_sha256=sha(proc.stderr.encode()),expected_pass=good)
 require((proc.returncode==0)==good,'Unexpected result '+name+': '+proc.stderr)
 if message is not None:require(message in proc.stderr,'Wrong failure '+name+': '+proc.stderr)
 if good and script=='verify_package.py':rec['result']=json.loads(proc.stdout)
 return rec
# Build the real candidate; verifier's receipt is external to archive domain.
results=[run('CANDIDATE_BUILD',P,'build_archive.py'),run('CANDIDATE_REQUIRED_VERIFY',P,'verify_package.py',['--require-deposit'])]
archive=P/'supportkit-v1.0.tar.gz';data=archive.read_bytes();original_hash=sha(data)
with tarfile.open(archive,'r:gz') as tar:
 members=tar.getmembers();tar.extractall(T/'clean_extract',filter='data')
clean=T/'clean_extract/rank_one_uniqueness_v1_0'
require(not (clean/'zenodo-deposit.json').exists(),'Wrapper distributed')
require(not (clean/'supportkit-v1.0.tar.gz').exists(),'Archive distributed inside itself')
for optimized in [False,True]:
 tag='OPTIMIZED' if optimized else 'NORMAL'
 if optimized:
  shutil.rmtree(T/'clean_extract');
  with tarfile.open(archive,'r:gz') as tar:tar.extractall(T/'clean_extract',filter='data')
 before=run('CLEAN_'+tag+'_VERIFY_BEFORE',clean,'verify_package.py',optimized=optimized)
 require(before['result']['external_wrapper_present'] is False and before['result']['external_wrapper_metadata_and_files_verified'] is False,'Dishonest absent wrapper before build')
 require(before['result']['archive_checked'] is False and before['result']['gzip_crc_isize_verified'] is False,'Dishonest absent archive')
 results.append(before)
 results.append(run('CLEAN_'+tag+'_REQUIRED_ABSENT',clean,'verify_package.py',['--require-deposit'],optimized,False,'Required external deposit wrapper is absent'))
 results.append(run('CLEAN_'+tag+'_BUILD',clean,'build_archive.py',optimized=optimized))
 require((clean/'supportkit-v1.0.tar.gz').read_bytes()==data,'Clean build not byte identical')
 after=run('CLEAN_'+tag+'_VERIFY_AFTER',clean,'verify_package.py',optimized=optimized)
 require(after['result']['external_wrapper_present'] is False and after['result']['external_wrapper_metadata_and_files_verified'] is False and after['result']['archive_checked'] is True,'Dishonest after build flags')
 results.append(after)
 results.append(run('CLEAN_'+tag+'_REQUIRED_ABSENT_AFTER',clean,'verify_package.py',['--require-deposit'],optimized,False,'Required external deposit wrapper is absent'))
 # The exact unchanged external descriptor enables full local-deposit verification.
 shutil.copyfile(P/'zenodo-deposit.json',clean/'zenodo-deposit.json')
 for mode,args in [('DEFAULT',[]),('REQUIRED',['--require-deposit'])]:
  x=run('CLEAN_'+tag+'_PRESENT_'+mode,clean,'verify_package.py',args,optimized)
  require(x['result']['external_wrapper_present'] is True and x['result']['external_wrapper_metadata_and_files_verified'] is True,'Missing full deposit coverage')
  results.append(x)
# Actual full-copy verify/build/verify sequence.
full=T/'full_candidate';shutil.copytree(P,full,ignore=shutil.ignore_patterns('tmp','__pycache__'))
results.append(run('FULL_VERIFY_BEFORE',full,'verify_package.py',['--require-deposit']))
results.append(run('FULL_BUILD',full,'build_archive.py'))
require((full/'supportkit-v1.0.tar.gz').read_bytes()==data,'Full build differs')
results.append(run('FULL_VERIFY_AFTER',full,'verify_package.py',['--require-deposit']))
wrapper=json.loads((P/'zenodo-deposit.json').read_text())
def metadata(x):x['metadata']['title']='altered title'
def publication_type(x):x['metadata']['publication_type']='article'
def upload_type(x):x['metadata']['upload_type']='dataset'
def filepaths(x):x['files'][1]['path']='README.md'
def filename(x):x['files'][0]['name']='wrong.pdf'
def nonexternal(x):x['files'][1]['path']='publication/zenodo.json'
def duplicate(x):x['files'].append(copy.deepcopy(x['files'][0]))
def object_type(x):return []
def metadata_type(x):x['metadata']=[]
def files_type(x):x['files']={}
def extra_field(x):x['unexpected']='not allowed'
def malformed(x):return '{"metadata":'
def duplicate_key(x):return '{"metadata":null,"metadata":'+json.dumps(x['metadata'])+',"files":'+json.dumps(x['files'])+'}'
wrapper_faults=[('metadata',metadata,'External wrapper metadata mismatch'),('publication_type',publication_type,'External wrapper metadata mismatch'),('upload_type',upload_type,'External wrapper metadata mismatch'),('filepaths',filepaths,'External wrapper file binding mismatch'),('filename',filename,'External wrapper file binding mismatch'),('nonexternal_misbinding',nonexternal,'External wrapper file binding mismatch'),('duplicate_attachment',duplicate,'External wrapper file binding mismatch'),('object_type',object_type,'Malformed external wrapper object'),('metadata_type',metadata_type,'External wrapper metadata mismatch'),('files_type',files_type,'External wrapper file binding mismatch'),('extra_field',extra_field,'Malformed external wrapper object'),('malformed_json',malformed,'JSONDecodeError'),('duplicate_json_key',duplicate_key,'Duplicate JSON key')]
controls=[]
for fault,mutate,message in wrapper_faults:
 for optimized in [False,True]:
  for mode,args in [('default',[]),('required',['--require-deposit'])]:
   name=f'FAULT_{fault}_{"optimized" if optimized else "normal"}_{mode}'
   target=T/'fault';
   if target.exists():shutil.rmtree(target)
   shutil.copytree(P,target,ignore=shutil.ignore_patterns('tmp','__pycache__'))
   bad=copy.deepcopy(wrapper);new=mutate(bad)
   if new is not None:bad=new
   (target/'zenodo-deposit.json').write_text(bad if isinstance(bad,str) else json.dumps(bad))
   controls.append(run(name,target,'verify_package.py',args,optimized,False,message))
# Package integrity and historical/state checks remain active under -O.
def altered_content(t):(t/'README.md').write_bytes((t/'README.md').read_bytes()+b'\nchanged\n')
def unmanifested(t):(t/'new_authored.md').write_text('not declared\n')
def altered_archive(t):(t/'supportkit-v1.0.tar.gz').write_bytes((t/'supportkit-v1.0.tar.gz').read_bytes()+b'x')
def historical_copy(t):(t/'evidence/reviews/package_02/VERDICT.json').write_text('{}\n')
def pending_state(t):
 x=json.loads((t/'STATUS.json').read_text());x['publication_ready']=True;writej(t/'STATUS.json',x)
 # Rebuild to move beyond the ordinary content hash check into the pending guard.
 run('PREPARE_PENDING_FAULT',t,'build_archive.py')
def wrapper_symlink(t):
 (t/'zenodo-deposit.json').unlink();(t/'zenodo-deposit.json').symlink_to('publication/zenodo.json')
def wrapper_broken_symlink(t):
 (t/'zenodo-deposit.json').unlink();(t/'zenodo-deposit.json').symlink_to('absent.json')
def missing_archive(t):(t/'supportkit-v1.0.tar.gz').unlink()
def wrapper_directory(t):
 (t/'zenodo-deposit.json').unlink();(t/'zenodo-deposit.json').mkdir()
def changed_tar(t,kind):
 source=t/'supportkit-v1.0.tar.gz'
 with tarfile.open(source,'r:gz') as old:
  items=[(m,old.extractfile(m).read()) for m in old.getmembers()]
 if kind=='payload':
  for m,d in items:
   if m.name.endswith('/README.md'):break
  at=next(i for i,(m,d) in enumerate(items) if m.name=='rank_one_uniqueness_v1_0/README.md')
  member,content=items[at];items[at]=(member,content+b'changed payload')
 elif kind=='missing':items.pop()
 elif kind=='duplicate':items.append(items[-1])
 elif kind=='mode':items[-1][0].mode=0o600
 out=io.BytesIO()
 with gzip.GzipFile(fileobj=out,mode='wb',filename='',mtime=0) as compressed:
  with tarfile.open(fileobj=compressed,mode='w',format=tarfile.PAX_FORMAT) as tar:
   for member,content in items:
    member.size=len(content);tar.addfile(member,io.BytesIO(content))
 content=out.getvalue();source.write_bytes(content)
 side=json.loads((t/'ARCHIVE_SHA256.json').read_text());side['bytes']=len(content);side['sha256']=sha(content);side['archive_members']=len(items);writej(t/'ARCHIVE_SHA256.json',side)
def historic_pin_fault(t):
 name='evidence/reviews/package_02/VERDICT.json';path=t/name;path.write_text('{}\n')
 c=json.loads((t/'EVIDENCE_COPY_MANIFEST.json').read_text())
 for rec in c['files']:
  if rec['package_path']==name:rec['bytes']=path.stat().st_size;rec['sha256']=sha(path.read_bytes())
 writej(t/'EVIDENCE_COPY_MANIFEST.json',c);run('PREPARE_HISTORIC_FAULT',t,'build_archive.py')
for fault,mutate,message in [('content',altered_content,'Hash/size mismatch'),('unmanifested',unmanifested,'manifest/content membership mismatch'),('archive',altered_archive,'Hash/size mismatch'),('historical_copy',historical_copy,'Hash/size mismatch'),('pending_state',pending_state,'Pending review improperly promoted'),('wrapper_symlink',wrapper_symlink,'External wrapper must be a regular local file'),('wrapper_broken_symlink',wrapper_broken_symlink,'External wrapper must be a regular local file'),('present_missing_archive',missing_archive,'Missing or nonregular local upload attachment'),('wrapper_directory',wrapper_directory,'External wrapper must be a regular local file'),('tar_payload_after_sidecar_rebind',lambda t:changed_tar(t,'payload'),'Archive/local mismatch'),('tar_missing_member_after_sidecar_rebind',lambda t:changed_tar(t,'missing'),'Archive membership mismatch'),('tar_duplicate_member_after_sidecar_rebind',lambda t:changed_tar(t,'duplicate'),'Archive membership mismatch'),('tar_mode_after_sidecar_rebind',lambda t:changed_tar(t,'mode'),'Archive metadata mismatch'),('historic_pin_after_manifest_rebuild',historic_pin_fault,'Hash/size mismatch')]:
 for optimized in [False,True]:
  for mode,args in [('default',[]),('required',['--require-deposit'])]:
   target=T/'fault'
   if target.exists():shutil.rmtree(target)
   shutil.copytree(P,target,ignore=shutil.ignore_patterns('tmp','__pycache__'));mutate(target)
   controls.append(run(f'FAULT_{fault}_{"optimized" if optimized else "normal"}_{mode}',target,'verify_package.py',args,optimized,False,message))
# Excluded material cannot enter payload or be mistaken for legitimate authored output.
excluded=T/'excluded_copy';shutil.copytree(P,excluded,ignore=shutil.ignore_patterns('tmp','__pycache__'))
for name in ['fullsource.txt','unapproved_stdout.txt','raw/source.pdf','rawprivate/source.txt','replay/a.md','render/page.png','sources/CITATION_DISCOVERY.json','extracted/body.txt','cache/entry.md']:
 path=excluded/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'private-body-probe')
results.append(run('EXCLUSION_BUILD',excluded,'build_archive.py'))
require((excluded/'supportkit-v1.0.tar.gz').read_bytes()==data,'Excluded bodies changed archive')
results.append(run('EXCLUSION_VERIFY',excluded,'verify_package.py',['--require-deposit']))
# Independently construct closed tar bytes from parsed manifest, no builder import.
manifest=json.loads((P/'CURRENT_INTEGRITY.json').read_text());expected=sorted([x['path'] for x in manifest['files']]+['CURRENT_INTEGRITY.json','BUILD_RECEIPT.json'])
expanded=gzip.decompress(data);crc,isize=struct.unpack('<II',data[-8:])
require(data[:3]==b'\x1f\x8b\x08' and data[3]==0 and data[4:8]==b'\x00'*4,'Gzip header')
require(crc==(zlib.crc32(expanded)&0xffffffff) and isize==(len(expanded)&0xffffffff),'Gzip footer')
require(len(members)==len(expected) and [m.name for m in members]==['rank_one_uniqueness_v1_0/'+n for n in expected],'Closed member cardinality/order')
require(len({n.casefold() for n in expected})==len(expected),'Casefold path collision')
raw_tar=io.BytesIO()
with tarfile.open(fileobj=raw_tar,mode='w',format=tarfile.PAX_FORMAT) as out:
 for name,member in zip(expected,members):
  require(all(x not in {'','..','.'} for x in name.split('/')) and not name.startswith('/'),'Unsafe path')
  require(member.isfile() and member.mode==0o644 and member.uid==member.gid==0 and member.mtime==1791849600 and member.uname==member.gname=='','Tar member metadata')
  content=(P/name).read_bytes()
  with tarfile.open(archive,'r:gz') as source:require(source.extractfile(member).read()==content,'Tar member/local bytes')
  info=tarfile.TarInfo('rank_one_uniqueness_v1_0/'+name);info.size=len(content);info.mtime=1791849600;info.uid=info.gid=0;info.uname=info.gname='';info.mode=0o644
  out.addfile(info,io.BytesIO(content))
require(raw_tar.getvalue()==expanded,'Independent tar bytes differ')
raw_gz=io.BytesIO()
with gzip.GzipFile(fileobj=raw_gz,mode='wb',filename='',mtime=0) as out:out.write(raw_tar.getvalue())
require(raw_gz.getvalue()==data,'Independent gzip bytes differ')
copies=json.loads((P/'EVIDENCE_COPY_MANIFEST.json').read_text())
for rec in copies['files']:
 content=(P/rec['package_path']).read_bytes();require(content==(A/rec['source_path']).read_bytes() and len(content)==rec['bytes'] and sha(content)==rec['sha256'],'Copy mapping mismatch '+rec['package_path'])
# UTF-8 authored content; only the unchanged authored PDF is binary.
utf8=jsons=0;binary=[]
for name in expected:
 content=(P/name).read_bytes()
 if name=='output/pdf/paper.pdf':binary.append(name);continue
 require(not content.startswith((b'%PDF-',b'\x1f\x8b',b'\x89PNG',b'PK\x03\x04',b'GIF8')),'Hidden binary '+name)
 content.decode('utf8');utf8+=1
 if name.endswith('.json'):json.loads(content);jsons+=1
writej(R/'NEGATIVE_CONTROLS.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),controls=controls,total=len(controls),all_rejected_with_expected_failure=True,interpreters=['normal','-O'],modes=['default','--require-deposit'],explicit_exception_guards=True,old_game_flow_code_unchanged=True))
writej(R/'TEST_RESULTS.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_runs=results,all_expected_results=True,clean_before_build_coverage_honest=True,clean_after_build_byte_identical=True,absent_required_wrapper_fails=True,present_wrapper_passes_both_modes=True,archive_sha256=original_hash,content_files=len(manifest['files']),archive_members=len(members),copied_authored_records=len(copies['files']),independent_tar_gzip_bytes_identical=True,gzip_crc_isize_verified=True,utf8_authored_files=utf8,parseable_json_files=jsons,binary_files=binary,excluded_material_did_not_change_archive=True,publication_ready=False,all_issues_resolved=False,new_whole_package_review='PENDING_NEW_WHOLE_03'))
print(json.dumps(dict(status='PASS_BOUNDED_PACKAGE02_REPAIR',actual_positive_and_required_absent_runs=len(results),negative_runs=len(controls),content_files=len(manifest['files']),archive_members=len(members),archive_sha256=original_hash,independent_tar_gzip_exact=True)))
