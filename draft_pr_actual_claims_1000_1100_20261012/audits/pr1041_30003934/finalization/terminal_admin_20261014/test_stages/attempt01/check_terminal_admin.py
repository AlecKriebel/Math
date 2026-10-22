#!/usr/bin/env python3
"""Actual package interfaces and targeted terminal guards; no mathematical rerun."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,gzip,hashlib,io,json,re,shutil,struct,subprocess,tarfile,zlib
D=Path(__file__).resolve().parent;B=D.parent.parent;P=B/'preprint_v1_0';S=D/'scratch'
def sha(data):return hashlib.sha256(data).hexdigest()
def need(test,why):
 if not test:raise RuntimeError(why)
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def load(path):return json.loads(path.read_text())
def run(root,label,script,args=(),expected=0,target=None):
 command=[sys.executable,'-B',*args,script]
 proc=subprocess.run(command,cwd=root,capture_output=True,text=True)
 (D/(label+'_STDOUT.txt')).write_text(proc.stdout);(D/(label+'_STDERR.txt')).write_text(proc.stderr)
 need((proc.returncode==0)==(expected==0),'unexpected exit '+label+': '+proc.stderr)
 if target:need(target in proc.stderr,'wrong guard '+label+': '+proc.stderr)
 result={'label':label,'command':command,'exit':proc.returncode,'expected_exit_zero':expected==0,'expected_guard':target}
 if proc.returncode==0:result['receipt']=json.loads(proc.stdout)
 return result
def tarbytes(root,names):
 # Independent closed PAX/gzip construction; never invokes the supplied builder.
 stream=io.BytesIO()
 with tarfile.open(fileobj=stream,mode='w',format=tarfile.PAX_FORMAT) as tar:
  for name in sorted(names):
   data=(root/name).read_bytes();entry=tarfile.TarInfo('rank_one_uniqueness_v1_0/'+name)
   entry.size=len(data);entry.mtime=1791849600;entry.uid=entry.gid=0;entry.uname=entry.gname='';entry.mode=0o644
   tar.addfile(entry,io.BytesIO(data))
 expanded=stream.getvalue();out=io.BytesIO()
 with gzip.GzipFile(filename='',fileobj=out,mode='wb',mtime=0) as gz:gz.write(expanded)
 return expanded,out.getvalue()
def closed(root):
 integrity=load(root/'CURRENT_INTEGRITY.json');records=integrity['files'];current={x['path']:x for x in records}
 need(len(current)==len(records),'duplicate manifest')
 for name,record in current.items():
  data=(root/name).read_bytes();need(len(data)==record['bytes'] and sha(data)==record['sha256'],'current pin '+name)
 names=sorted(set(current)|{'BUILD_RECEIPT.json','CURRENT_INTEGRITY.json'})
 data=(root/'supportkit-v1.0.tar.gz').read_bytes();need(data[:10]==b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff','gzip canonical header')
 expanded=gzip.decompress(data);crc,size=struct.unpack('<II',data[-8:]);need(crc==zlib.crc32(expanded)&0xffffffff and size==len(expanded)&0xffffffff,'gzip footer')
 textcount=0;jsoncount=0
 with tarfile.open(fileobj=io.BytesIO(expanded),mode='r:') as tar:
  members=tar.getmembers();got=[]
  for m in members:
   need(m.isfile() and m.name.startswith('rank_one_uniqueness_v1_0/'),'regular prefix')
   name=m.name[len('rank_one_uniqueness_v1_0/'):];got.append(name)
   need(re.fullmatch(r'[A-Za-z0-9_.\-/]+',name) and all(x not in {'','..','.'} for x in name.split('/')),'safe path')
   need(name in names and tar.extractfile(m).read()==(root/name).read_bytes(),'closed local bytes '+name)
   need(m.mode==0o644 and m.uid==m.gid==0 and m.uname==m.gname=='' and m.mtime==1791849600,'metadata '+name)
   if name!='output/pdf/paper.pdf':
    text=(root/name).read_bytes().decode('utf-8');textcount+=1
    if name.endswith('.json'):json.loads(text);jsoncount+=1
   need(name not in {'zenodo-deposit.json','ARCHIVE_SHA256.json','VERIFICATION_RECEIPT.json','supportkit-v1.0.tar.gz'},'external receipt/wrapper')
  need(got==names and len(got)==len(set(got))==len({x.casefold() for x in got}),'membership/order/casefold')
 rebuilt_tar,rebuilt_gz=tarbytes(root,names);need(rebuilt_tar==expanded and rebuilt_gz==data,'entire independent tar/gzip reconstruction')
 side=load(root/'ARCHIVE_SHA256.json');need(sha(data)==side['sha256'] and len(data)==side['bytes'],'archive sidecar')
 return {'content_files':len(current),'archive_members':len(names),'utf8_nonpdf_members':textcount,'json_members':jsoncount,'archive_sha256':sha(data),'archive_bytes':len(data),'independent_entire_tar_and_gzip_byte_identical':True,'all_regular_sorted_safe_casefold_unique_fixed_metadata':True,'gzip_header_crc_isize_verified':True}
def refresh_outer(root):
 # Fault setup refreshes every outer manifest/receipt/archive hash without
 # invoking the terminal gate, to isolate the verifier's protected guard.
 manifest=load(root/'CURRENT_INTEGRITY.json')
 manifest['files']=[{'path':r['path'],'bytes':len((root/r['path']).read_bytes()),'sha256':sha((root/r['path']).read_bytes())} for r in manifest['files'] if (root/r['path']).is_file()]
 write(root/'CURRENT_INTEGRITY.json',manifest);receipt=load(root/'BUILD_RECEIPT.json');status=load(root/'STATUS.json')
 receipt.update({'status':'PREPARED_CANDIDATE_'+status['new_whole_package_review'],'publication_ready':status['publication_ready'],'all_issues_resolved':status['all_issues_resolved'],'content_files':len(manifest['files']),'current_integrity_sha256':sha((root/'CURRENT_INTEGRITY.json').read_bytes())});write(root/'BUILD_RECEIPT.json',receipt)
 names=[r['path'] for r in manifest['files']]+['CURRENT_INTEGRITY.json','BUILD_RECEIPT.json'];expanded,compressed=tarbytes(root,names);(root/'supportkit-v1.0.tar.gz').write_bytes(compressed)
 side=load(root/'ARCHIVE_SHA256.json');side.update({'bytes':len(compressed),'sha256':sha(compressed),'current_integrity_sha256':sha((root/'CURRENT_INTEGRITY.json').read_bytes()),'build_receipt_sha256':sha((root/'BUILD_RECEIPT.json').read_bytes()),'archive_members':len(names),'publication_ready':status['publication_ready'],'all_issues_resolved':status['all_issues_resolved']});write(root/'ARCHIVE_SHA256.json',side)
def fresh(name):
 root=S/name
 if root.exists():shutil.rmtree(root)
 shutil.copytree(P,root,ignore=shutil.ignore_patterns('tmp','__pycache__'));return root
if S.exists():raise RuntimeError('scratch already exists')
S.mkdir();commands=[];faults=[]
# Build actual local final candidate after the last authored index edit.
for mode,args in [('normal',()),('optimized',('-O',))]:
 commands.append(run(P,'FULL_BUILD_'+mode,'build_archive.py',args))
 commands.append(run(P,'FULL_REQUIRED_'+mode,'verify_package.py',(*args,'--require-deposit')))
final_closed=closed(P)
for mode,args in [('normal',()),('optimized',('-O',))]:
 root=S/('clean_'+mode);root.mkdir()
 with tarfile.open(P/'supportkit-v1.0.tar.gz','r:gz') as tar:
  tar.extractall(root,filter='data')
 root=root/'rank_one_uniqueness_v1_0'
 before=run(root,'CLEAN_BEFORE_'+mode,'verify_package.py',args);commands.append(before)
 need(before['receipt']['archive_checked'] is False and before['receipt']['external_wrapper_present'] is False and before['receipt']['external_wrapper_metadata_and_files_verified'] is False,'honest clean boundary')
 commands.append(run(root,'CLEAN_REQUIRED_ABSENT_BEFORE_'+mode,'verify_package.py',(*args,'--require-deposit'),1,'Required external deposit wrapper is absent'))
 commands.append(run(root,'CLEAN_BUILD_'+mode,'build_archive.py',args));commands.append(run(root,'CLEAN_AFTER_'+mode,'verify_package.py',args))
 need((root/'supportkit-v1.0.tar.gz').read_bytes()==(P/'supportkit-v1.0.tar.gz').read_bytes(),'clean rebuild identity')
 commands.append(run(root,'CLEAN_REQUIRED_ABSENT_AFTER_'+mode,'verify_package.py',(*args,'--require-deposit'),1,'Required external deposit wrapper is absent'))
 shutil.copyfile(P/'zenodo-deposit.json',root/'zenodo-deposit.json')
 commands.append(run(root,'CLEAN_REQUIRED_PRESENT_'+mode,'verify_package.py',(*args,'--require-deposit')))
 closed(root);shutil.rmtree(root.parent)
# One full local verify-build-verify per mode on disposable exact copies.
for mode,args in [('normal',()),('optimized',('-O',))]:
 root=fresh('full_'+mode)
 commands.append(run(root,'FULL_SEQUENCE_BEFORE_'+mode,'verify_package.py',(*args,'--require-deposit')))
 commands.append(run(root,'FULL_SEQUENCE_BUILD_'+mode,'build_archive.py',args))
 commands.append(run(root,'FULL_SEQUENCE_AFTER_'+mode,'verify_package.py',(*args,'--require-deposit')))
 need((root/'supportkit-v1.0.tar.gz').read_bytes()==(P/'supportkit-v1.0.tar.gz').read_bytes(),'full sequence rebuild identity');shutil.rmtree(root)
def edit(root,name,fn):
 path=root/name;j=load(path);fn(j);write(path,j)
def byte_edit(root,name):
 path=root/name;path.write_bytes(path.read_bytes()+b'\n')
probes=[
 ('nonzero_status',lambda r:edit(r,'STATUS.json',lambda j:j['terminal_severity_counts'].update(P2=1)),'Terminal zero severity counts: status'),
 ('bool_zero_status',lambda r:edit(r,'STATUS.json',lambda j:j['terminal_severity_counts'].update(P0=False)),'Terminal zero severity counts: status'),
 ('missing_severity',lambda r:edit(r,'STATUS.json',lambda j:j['terminal_severity_counts'].pop('P3')),'Terminal zero severity counts: status'),
 ('pending_promoted',lambda r:edit(r,'STATUS.json',lambda j:j.update(new_whole_package_review='PENDING_NEW_WHOLE_04')),'Pending review improperly promoted'),
 ('unknown_terminal',lambda r:edit(r,'STATUS.json',lambda j:j.update(new_whole_package_review='FINAL_SELF_DECLARED')),'Unrecognized terminal review status'),
 ('one_review',lambda r:edit(r,'STATUS.json',lambda j:j.update(fresh_whole_package_reviews=1)),'Fresh whole-review count'),
 ('bool_review_count',lambda r:edit(r,'STATUS.json',lambda j:j.update(fresh_whole_package_reviews=True)),'Fresh whole-review count'),
 ('minimum_one',lambda r:edit(r,'STATUS.json',lambda j:j.update(minimum_fresh_whole_package_reviews=1)),'Fresh whole-review count'),
 ('one_readiness_false',lambda r:edit(r,'STATUS.json',lambda j:j.update(all_issues_resolved=False)),'Terminal readiness flags'),
 ('published_true',lambda r:edit(r,'STATUS.json',lambda j:j.update(published=True)),'Unpublished held-service state'),
 ('service_advance',lambda r:edit(r,'STATUS.json',lambda j:j.update(ascending_services_held_at=1033)),'Unpublished held-service state'),
 ('third_nonzero',lambda r:edit(r,'STATUS.json',lambda j:j['third_whole_package_review']['severity_counts'].update(P3=1)),'Terminal zero severity counts: third review status'),
 ('third_locator',lambda r:edit(r,'STATUS.json',lambda j:j['third_whole_package_review'].update(verdict_path='evidence/reviews/package_02/VERDICT.json')),'Terminal status/adoption binding'),
 ('verdict_nonzero',lambda r:edit(r,'evidence/reviews/package_03/VERDICT.json',lambda j:j['severity_counts'].update(P2=1)),'Terminal accepted/protected identity: evidence/reviews/package_03/VERDICT.json'),
 ('root_adoption_changed',lambda r:edit(r,'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_03.json',lambda j:j.update(root_entire_report_and_verdict_read=False)),'Terminal accepted/protected identity: evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_03.json'),
 ('seal_changed',lambda r:edit(r,'evidence/reviews/package_03/SEAL.json',lambda j:j.update(terminal=False)),'Terminal accepted/protected identity: evidence/reviews/package_03/SEAL.json'),
 ('report_changed',lambda r:byte_edit(r,'evidence/reviews/package_03/REPORT.md'),'Terminal accepted/protected identity: evidence/reviews/package_03/REPORT.md'),
 ('output_pins_changed',lambda r:edit(r,'evidence/reviews/package_03/OUTPUT_PINS.json',lambda j:j.update(readiness_promoted=True)),'Terminal accepted/protected identity: evidence/reviews/package_03/OUTPUT_PINS.json'),
 ('paper_changed',lambda r:byte_edit(r,'paper.tex'),'Terminal accepted/protected identity: paper.tex'),
 ('pdf_changed',lambda r:byte_edit(r,'output/pdf/paper.pdf'),'Terminal accepted/protected identity: output/pdf/paper.pdf'),
 ('bare_metadata_changed',lambda r:edit(r,'publication/zenodo.json',lambda j:j.update(title=j['title']+' altered')),'Terminal accepted/protected identity: publication/zenodo.json'),
 ('history_p2_relabel',lambda r:edit(r,'REVIEW_HISTORY.json',lambda j:j['events'][2]['severity_counts'].update(P2=0)),'Terminal accepted/protected identity: REVIEW_HISTORY.json'),
 ('exclusion_added',lambda r:edit(r,'HISTORIC_EXCLUSIONS.json',lambda j:j['files'].append(dict(j['files'][0]))),'Terminal accepted/protected identity: HISTORIC_EXCLUSIONS.json'),
]
for name,mutate,target in probes:
 root=fresh('fault');mutate(root)
 for mode,args in [('normal',()),('optimized',('-O',))]:
  before={x:sha((root/x).read_bytes()) for x in ['CURRENT_INTEGRITY.json','BUILD_RECEIPT.json','ARCHIVE_SHA256.json','supportkit-v1.0.tar.gz']}
  result=run(root,'GUARD_BUILD_'+name+'_'+mode,'build_archive.py',args,1,target);result['builder_rejects_before_writing']=all(sha((root/x).read_bytes())==h for x,h in before.items());need(result['builder_rejects_before_writing'],'builder partially wrote on rejection');faults.append(result)
 refresh_outer(root)
 for mode,args in [('normal',()),('optimized',('-O',))]:
  for interface,extra in [('default',()),('required',('--require-deposit',))]:
   result=run(root,'GUARD_VERIFY_'+name+'_'+mode+'_'+interface,'verify_package.py',(*args,*extra),1,target);result['all_outer_manifest_archive_receipt_hashes_refreshed']=True;faults.append(result)
 shutil.rmtree(root)
# Preserve strict present-wrapper behavior in both verification modes after outer refresh.
wrappers=[('wrapper_metadata',lambda j:j['metadata'].update(title='altered'),'External wrapper metadata mismatch'),('wrapper_filename',lambda j:j['files'][0].update(name='wrong.pdf'),'External wrapper file binding mismatch'),('wrapper_missing_attachment',lambda j:j['files'].pop(),'External wrapper file binding mismatch'),('wrapper_type',lambda j:j.update(files={}),'External wrapper file binding mismatch')]
for name,mutate,target in wrappers:
 root=fresh('wrapper');edit(root,'zenodo-deposit.json',mutate);refresh_outer(root)
 for mode,args in [('normal',()),('optimized',('-O',))]:
  for interface,extra in [('default',()),('required',('--require-deposit',))]:faults.append(run(root,'STRICT_'+name+'_'+mode+'_'+interface,'verify_package.py',(*args,*extra),1,target))
 shutil.rmtree(root)
shutil.rmtree(S)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Terminal administration only; actual documented normal/optimized interfaces, targeted new guards, strict external-wrapper regressions, independent complete archive reconstruction. No compiler, rendering, mathematical checker or curve-program run.','closed_archive':final_closed,'actual_commands':commands,'faults':faults,'terminal_guard_families':len(probes),'terminal_guard_failures':len(probes)*6,'strict_wrapper_regression_failures':len(wrappers)*4,'all_faults_rejected_by_expected_explicit_guard':True,'scratch_removed_before_final_seal':True}
write(D/'ADMIN_CHECKS.json',result)
print(json.dumps({'commands':len(commands),'terminal_guard_failures':len(probes)*6,'strict_wrapper_failures':len(wrappers)*4,'closed_archive':final_closed}))
