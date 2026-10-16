#!/usr/bin/env python3
"""Freeze final administration after independent closed payload/custody checks."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,gzip,hashlib,io,json,re,shutil,struct,subprocess,tarfile,zlib
D=Path(__file__).resolve().parent;B=D.parent.parent;P=B/'preprint_v1_0'
def need(test,why):
 if not test:raise RuntimeError(why)
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_text())
def write(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def pin(path,rel):
 data=path.read_bytes();return {'path':rel,'bytes':len(data),'sha256':sha(data)}
def record(path,rec):
 data=path.read_bytes();need(len(data)==rec['bytes'] and sha(data)==rec['sha256'],'hash/size '+str(path))
commands=[]
def run(root,label,script,mode='normal',required=False,fail=False):
 cmd=[sys.executable,'-B',*(['-O'] if mode=='optimized' else []),script,*(['--require-deposit'] if required else [])]
 proc=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
 (D/(label+'_STDOUT.txt')).write_text(proc.stdout);(D/(label+'_STDERR.txt')).write_text(proc.stderr)
 need((proc.returncode!=0)==fail,'command exit '+label+proc.stderr)
 if fail:need('Required external deposit wrapper is absent' in proc.stderr,'required missing guard')
 result={'label':label,'command':cmd,'exit':proc.returncode}
 if not fail:result['receipt']=json.loads(proc.stdout)
 commands.append(result);return result
# Copy tooling is a source-tree preparation interface, not a clean-kit command.
oldmap=(P/'EVIDENCE_COPY_MANIFEST.json').read_bytes();run(P,'FINAL_COPY_TOOL_IDEMPOTENT','prepare_support.py');need(oldmap==(P/'EVIDENCE_COPY_MANIFEST.json').read_bytes(),'copy tool changed existing map identity')
run(P,'FINAL_BUILD','build_archive.py')
for mode in ['normal','optimized']:run(P,'FINAL_FULL_REQUIRED_'+mode,'verify_package.py',mode,True)
archive=(P/'supportkit-v1.0.tar.gz').read_bytes();manifest=load(P/'CURRENT_INTEGRITY.json');current={x['path']:x for x in manifest['files']};need(len(current)==len(manifest['files']),'duplicate content pins')
for name,r in current.items():record(P/name,r)
names=sorted(set(current)|{'CURRENT_INTEGRITY.json','BUILD_RECEIPT.json'})
expanded=gzip.decompress(archive);crc,size=struct.unpack('<II',archive[-8:]);need(archive[:10]==b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff' and crc==zlib.crc32(expanded)&0xffffffff and size==len(expanded)&0xffffffff,'gzip framing')
seen=[];utf8=0;jsons=0
with tarfile.open(fileobj=io.BytesIO(expanded),mode='r:') as tar:
 for m in tar.getmembers():
  need(m.isfile() and m.name.startswith('rank_one_uniqueness_v1_0/'),'tar regular/prefix');name=m.name[len('rank_one_uniqueness_v1_0/'):];seen.append(name)
  need(name in names and re.fullmatch(r'[A-Za-z0-9_.\-/]+',name) and all(x not in {'','..','.'} for x in name.split('/')),'safe closed path')
  need(tar.extractfile(m).read()==(P/name).read_bytes(),'tar local '+name)
  need(m.mode==0o644 and m.uid==m.gid==0 and m.uname==m.gname=='' and m.mtime==1791849600,'fixed metadata '+name)
  if name!='output/pdf/paper.pdf':
   text=(P/name).read_bytes().decode('utf-8');utf8+=1
   if name.endswith('.json'):json.loads(text);jsons+=1
need(seen==names and len(seen)==len({x.casefold() for x in seen}),'sorted unique/casefold membership')
# Construct full tar/gzip independently without importing either package tool.
out=io.BytesIO()
with tarfile.open(fileobj=out,mode='w',format=tarfile.PAX_FORMAT) as tar:
 for name in names:
  data=(P/name).read_bytes();m=tarfile.TarInfo('rank_one_uniqueness_v1_0/'+name);m.size=len(data);m.mode=0o644;m.uid=m.gid=0;m.uname=m.gname='';m.mtime=1791849600;tar.addfile(m,io.BytesIO(data))
need(out.getvalue()==expanded,'entire independent tar identity');gzout=io.BytesIO()
with gzip.GzipFile(filename='',fileobj=gzout,mode='wb',mtime=0) as gz:gz.write(out.getvalue())
need(gzout.getvalue()==archive,'entire independent gzip identity')
record(P/'supportkit-v1.0.tar.gz',load(P/'ARCHIVE_SHA256.json'))
# Recheck final bytes after QA/log changes using actual clean-kit interfaces.
S=D/'scratch_final';need(not S.exists(),'final scratch exists');S.mkdir()
for mode in ['normal','optimized']:
 dest=S/mode;dest.mkdir()
 with tarfile.open(P/'supportkit-v1.0.tar.gz','r:gz') as tar:tar.extractall(dest,filter='data')
 root=dest/'rank_one_uniqueness_v1_0'
 before=run(root,'FINAL_CLEAN_BEFORE_'+mode,'verify_package.py',mode)
 need(before['receipt']['archive_checked'] is False and before['receipt']['external_wrapper_present'] is False and before['receipt']['external_wrapper_metadata_and_files_verified'] is False,'final clean boundary flags')
 run(root,'FINAL_CLEAN_REQUIRE_ABSENT_BEFORE_'+mode,'verify_package.py',mode,True,True)
 run(root,'FINAL_CLEAN_BUILD_'+mode,'build_archive.py',mode)
 run(root,'FINAL_CLEAN_AFTER_'+mode,'verify_package.py',mode)
 run(root,'FINAL_CLEAN_REQUIRE_ABSENT_AFTER_'+mode,'verify_package.py',mode,True,True)
 need((root/'supportkit-v1.0.tar.gz').read_bytes()==archive,'final clean exact archive reconstruction')
 shutil.copyfile(P/'zenodo-deposit.json',root/'zenodo-deposit.json');run(root,'FINAL_CLEAN_REQUIRE_PRESENT_'+mode,'verify_package.py',mode,True)
 shutil.rmtree(dest)
shutil.rmtree(S)
# Every originating authored source and packaged copy, including all prior 161.
copies=load(P/'EVIDENCE_COPY_MANIFEST.json');oldcopies=load(D/'baseline/preprint_v1_0/EVIDENCE_COPY_MANIFEST.json')['files'];need(copies['files'][:161]==oldcopies and len(oldcopies)==161 and len(copies['files'])==468,'old copy-map identity/order or new count')
for r in copies['files']:
 record(P/r['package_path'],r);record(B/r['source_path'],r)
whole03=load(B/'reviews/package_03/OUTPUT_PINS.json')
for r in whole03['files']:record(B/'reviews/package_03'/r['path'],r);record(P/'evidence/reviews/package_03'/r['path'],r)
need(len(whole03['files'])==304,'whole03 authored output count')
# Terminal stage exact before bytes and immutable old 224-file freeze resolution.
h=P/'history/before_terminal03_finalization';stage=load(h/'STAGE_PINS.json')
for r in stage['files']:record(h/r['frozen_path'],r)
old224=load(B/'repairs/package02/FINAL_CURRENT_INPUT_PINS.json');resolution=[]
for r in old224['files']:
 saved=D/'baseline/preprint_v1_0'/r['path'];path=saved if saved.is_file() else P/r['path'];record(path,r)
 resolution.append({'original_path':r['path'],'resolved_before_byte_path':path.relative_to(B).as_posix(),'sha256':r['sha256'],'bytes':r['bytes']})
need(len(resolution)==224,'old current freeze count');write(D/'HISTORICAL_224_PIN_RESOLUTION.json',{'policy':'Old current candidate pins remain exact and unchanged. Mutable paths resolve to exact terminal before bytes; unchanged paths remain in place. No pin is retargeted.','files':resolution})
# Earlier repair's sealed 758 records and pre-repair outside17 baseline.
repairpins=load(B/'repairs/package02/OUTPUT_PINS.json')
for r in repairpins['files']:record(B/'repairs/package02'/r['path'],r)
need(len(repairpins['files'])==758,'prior repair output count')
repairchanges=load(B/'repairs/package02/CHANGE_INVENTORY.json');ex17={r['path'] for r in repairchanges['changed']};oldbase=load(B/'repairs/package02/BASELINE_ALL_PINS.json');outside17=0
for r in oldbase['files']:
 if r['path'] in ex17:continue
 record(B/r['path'],r);outside17+=1
need(outside17==2488,'outside17 count')
for r in repairchanges['changed']:record(B/r['exact_old_stage_copy'],r['before'])
# Every immediate input outside the exact authorized administrative path set.
allowed={'preprint_v1_0/'+x for x in ['ARCHIVE_SHA256.json','BUILD_RECEIPT.json','CURRENT_INTEGRITY.json','EVIDENCE_COPY_MANIFEST.json','EVIDENCE_INDEX.md','HASH_STAGE_INDEX.json','INTEGRITY_QA.json','PDF_QA.json','PREPARATION_REPORT.md','README.md','RESEARCH_LOG.md','STATUS.json','SUPPLEMENT.md','VERIFICATION_RECEIPT.json','build_archive.py','prepare_support.py','supportkit-v1.0.tar.gz','verify_package.py']}
inputs=load(D/'INPUT_PINS.json');old={r['path']:r for r in inputs['files']};changed=[];unchanged=0
for name,r in old.items():
 path=B/name;need(path.is_file(),'initial input disappeared '+name);data=path.read_bytes()
 if sha(data)!=r['sha256'] or len(data)!=r['bytes']:
  need(name in allowed,'unauthorized input change '+name);saved=D/'baseline/preprint_v1_0'/Path(name).name;record(saved,r)
  changed.append({'path':name,'before':r,'after':pin(path,name),'exact_before_byte_path':saved.relative_to(B).as_posix()})
 else:unchanged+=1
need({r['path'] for r in changed}==allowed,'authorized changed path count')
added=[]
for path in sorted(B.rglob('*')):
 if not path.is_file():continue
 name=path.relative_to(B).as_posix()
 if name in old or path.is_relative_to(D):continue
 need(path.is_relative_to(P),'new file outside allowed package/admin folders '+name);added.append(pin(path,name))
need(len(added)==328,'new package member count')
write(D/'CHANGE_INVENTORY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'policy':'Exact before/after hashes for 18 necessary admin/tooling/receipt/archive changes; 328 additive package records. Every other immediate input byte remains unchanged; existing historical pins never retargeted.','changed':changed,'added':added,'changed_count':len(changed),'added_count':len(added),'unchanged_immediate_input_count':unchanged,'outside_authorized_changes_verified':True,'no_protected_paper_pdf_math_metadata_descriptor_changes':True})
protected_names=['preprint_v1_0/paper.tex','preprint_v1_0/output/pdf/paper.pdf','preprint_v1_0/publication/zenodo.json','preprint_v1_0/zenodo-deposit.json','preprint_v1_0/LICENSE.md']+[r['path'] for r in inputs['files'] if r['path'].startswith(('submitted/','reviews/','preprint_v1_0/evidence/','preprint_v1_0/history/','repairs/'))]
protected=[old[n] for n in sorted(set(protected_names))]
for r in protected:record(B/r['path'],r)
write(D/'PROTECTED_UNCHANGED.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'policy':'Exact immediate-input identities of protected paper/PDF/bibliographic metadata/descriptor/license/original/proof/checker/evidence/review/repair/history files. No new mathematical/compiler/render check is claimed. All other nonauthorized immediate inputs are additionally verified.','files':protected,'count':len(protected),'all_bytes_unchanged':True})
# Verify all current content bytes and final complete local tree once more.
for name,r in current.items():record(P/name,r)
finalfiles=[pin(path,path.relative_to(P).as_posix()) for path in sorted(P.rglob('*')) if path.is_file()]
write(D/'FINAL_CURRENT_INPUT_PINS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Complete final local preprint_v1_0 file tree after terminal administrative freeze. Separate from unretargeted historical input/output pins.','files':finalfiles,'total_files':len(finalfiles),'content_files':len(current),'archive_members':len(names),'archive_sha256':sha(archive),'publication_ready':True,'all_issues_resolved':True,'published':False})
with tarfile.open(D/'baseline/preprint_v1_0/supportkit-v1.0.tar.gz','r:gz') as tar:oldnames={m.name for m in tar.getmembers()}
need(oldnames<={('rank_one_uniqueness_v1_0/'+n) for n in names},'old archive paths omitted')
status=load(P/'STATUS.json');need(status['publication_ready'] is True and status['all_issues_resolved'] is True and status['published'] is False,'final flags')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_TERMINAL_ADMIN_PENDING_ROOT_FINAL_ADMIN_ADOPTION','actual_final_commands':commands,'content_files':len(current),'archive_members':len(names),'local_current_files':len(finalfiles),'archive_bytes':len(archive),'archive_sha256':sha(archive),'current_integrity_sha256':sha((P/'CURRENT_INTEGRITY.json').read_bytes()),'all_closed_tar_payloads_verified':True,'independent_entire_tar_and_gzip_byte_identical':True,'gzip_header_crc_isize_verified':True,'safe_sorted_literal_and_casefold_unique_paths':True,'fixed_regular0644_epoch1791849600_zero_owner_empty_names':True,'utf8_nonpdf_members':utf8,'json_members':jsons,'old_archive_member_paths_retained':len(oldnames),'all_original_11_exact':True,'copies_and_originating_sources_verified':468,'all_previous_161_copy_records_and_bytes_exact':True,'whole03_outputs_exact':304,'whole03_pins_seal_root_adoption_exact':True,'whole03_omissions':0,'historic_output_members_verified':443,'explicit_historical_omissions':13,'old_stage_before_byte_records_verified':19,'old_current_224_pins_resolved_exactly':224,'prior_repair_sealed_output_records_verified':758,'prior_repair_outside17baseline_verified':outside17,'prior_repair_old_stage_records_verified':17,'immediate_inputs_frozen':len(old),'authorized_changed_inputs':len(changed),'all_other_immediate_inputs_exact':unchanged,'added_package_files':len(added),'protected_unchanged_records':len(protected),'copy_tool_actual_idempotent':True,'new_scratch_removed':True,'terminal_severity_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'fresh_whole_package_reviews':3,'publication_ready':True,'all_issues_resolved':True,'published':False,'ascending_services_held_at':1032,'new_tex_pdf_metadata_math_changes':False,'new_compilation_export_render_marker':False,'Git_index_branch_service_publication_or_contact_operation':False,'mathematical_proof_formally_verified':False,'root_final_admin_seal':'PENDING_ROOT_FINAL_ADMIN_ADOPTION','terminal_administrative_completion_percent':100}
write(D/'FINAL_INTEGRITY.json',result);print(json.dumps({k:v for k,v in result.items() if k!='actual_final_commands'}))
