"""Actual clean-extraction runtime commands and coherently rehashed semantic faults."""
import copy,hashlib,io,json,os,shutil,struct,subprocess,sys,tempfile,zipfile,zlib
from datetime import datetime,timezone
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';Z='PR1071_preprint_v1_0_support.zip'
def now():return datetime.now(timezone.utc).isoformat()
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def read(p):return json.loads(p.read_text())
def h(b):return hashlib.sha256(b).hexdigest()
def pin(p,n):return {'path':str(n),'bytes':p.stat().st_size,'sha256':h(p.read_bytes())}
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
need(not (D/'CONTROL_RECEIPTS.json').exists(),'Controls already settled')
commands=[];faults=[];products=[];scratch=Path(tempfile.mkdtemp(prefix='pr1071-history-order01-',dir='/private/tmp'))
write(D/'OWNED_SCRATCH.json',{'utc':now(),'path':str(scratch),'scope':'Only newly created scratch for this bounded repair; no shared/preexisting path touched.'})
root=scratch/'CleanPackage';root.mkdir()
with zipfile.ZipFile(P/Z) as z:z.extractall(root)
original={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
manifest=read(root/'PACKAGE_MANIFEST.json');need(len(original)==199 and len(manifest['members'])==198,'Archive counts')
data=(P/Z).read_bytes();names=sorted(original);memberrows=[]
with zipfile.ZipFile(P/Z) as z:
 need(z.namelist()==names and z.testzip() is None,'Closed ZIP names/order/CRC')
 for info in z.infolist():
  payload=original[info.filename];crc=zlib.crc32(payload)&0xffffffff
  need(z.read(info.filename)==payload==(P/info.filename).read_bytes(),'Exact archived bytes')
  need(info.date_time==(2026,10,14,0,0,0) and info.create_system==3 and info.external_attr==0o100644<<16 and info.compress_type==0 and info.CRC==crc,'ZIP central attributes')
  sig,version,flag,compression,tm,dt,c,csize,size,nlen,xlen=struct.unpack_from('<IHHHHHIIIHH',data,info.header_offset)
  need(sig==0x04034b50 and flag==compression==tm==xlen==0 and c==crc and size==csize==len(payload),'ZIP local header')
  start=info.header_offset+30;need(data[start:start+nlen].decode()==info.filename and data[start+nlen:start+nlen+size]==payload,'ZIP local name/payload')
  memberrows.append({'path':info.filename,'bytes':len(payload),'sha256':h(payload),'CRC32':crc,'local_and_central_checked':True})
need(data[-22:-18]==b'PK\x05\x06' and struct.unpack_from('<H',data,len(data)-2)[0]==0,'EOCD')
buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
 for name in names:
  i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,original[name])
need(buffer.getvalue()==data,'Independent closed reconstruction')
write(D/'INDEPENDENT_CLOSED_ZIP.json',{'utc':now(),'status':'PASS','archive':pin(P/Z,Z),'members':memberrows,'closed_reconstruction_byte_equal':True,'member_count':len(names)})
def run(py,opt,label,args,success=True,cwd=root):
 argv=[py,'-B',*(['-O'] if opt else []),*map(str,args)];p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 row={'utc':now(),'label':label,'argv':argv,'cwd':str(cwd),'returncode':p.returncode,'expected_success':success,'stdout':p.stdout,'stderr':p.stderr};commands.append(row)
 # Retain actual receipts immediately, including a failing command if a later check aborts.
 write(D/'COMMANDS_IN_PROGRESS.json',commands)
 need((p.returncode==0)==success,'Unexpected command outcome '+label+': '+p.stderr)
 return p
def restore(touched):
 for name in set(touched)|{'INPUT_COPY_MAP.json','PACKAGE_MANIFEST.json'}:(root/name).write_bytes(original[name])
def coherent_refresh():
 # Refresh internal copy pins too, so evidence mutations test semantics rather than stale hashes.
 c=read(root/'INPUT_COPY_MAP.json')
 for r in c['copies']:
  b=(root/r['package_copy']).read_bytes();r['bytes']=len(b);r['sha256']=h(b)
 write(root/'INPUT_COPY_MAP.json',c)
 m=read(root/'PACKAGE_MANIFEST.json')
 for r in m['members']:
  b=(root/r['path']).read_bytes();r['bytes']=len(b);r['sha256']=h(b)
 write(root/'PACKAGE_MANIFEST.json',m)
cases=[]
def field(name,path,key,value):cases.append((name,path,lambda v,k=key,x=value:v.__setitem__(k,x)))
S='HISTORY_ORDER_REPAIR_STATUS.json';Q='HISTORY_ORDER_QUALIFICATION.json'
for name,key,value in [('review_count','fresh_whole_package_reviews_completed',3),('minimum','minimum_fresh_reviews_required',1),('whole05_required','new_complete_whole_review_required',4),('pretend_whole05_done','new_complete_whole_review_completed',True),('readiness','publication_ready',True),('resolved','issues_resolved',True),('published','published',True),('hold','services_held_after_pr',0),('remove_root_repair','root_repair_adoption_required',False),('remove_root_terminal','root_terminal_adoption_required',False),('finding_erasure','latest_complete_review_findings',{'P0':0,'P1':0,'P2':0,'P3':0})]:field(name,S,key,value)
for name,key,value in [('false_global_order','additional1558_global_order_preserved',True),('false_first2788','original2788_global_values_and_order_preserved',False),('deny_multiset','additional1558_exact_row_multiset_preserved',False),('deny_per_stage','additional1558_per_stage_values_and_order_preserved',False),('wrong_mismatch','mismatched_global_additional_positions',0),('wrong_start','first_mismatch_additional_zero_based',0),('wrong_global_start','first_mismatch_global_zero_based',30),('wrong_references','historical_references',2788),('same_projection','after_projected_rows_sha256','ba6d22e917d183340ab20140260c2a71ab7045c616108f8c21a9d1e751e75d42')]:field(name,Q,key,value)
cases.append(('conceal_false_history',Q,lambda v:v['historical_false_claim'].__setitem__('truth_for_global_order',True)))
cases.append(('claim_old_record_rewritten',Q,lambda v:v['historical_false_claim'].__setitem__('preserved_as_dated_history',False)))
cases.append(('erase_two_block_permutation',Q,lambda v:v.__setitem__('after_groups',copy.deepcopy(v['before_groups']))))
cases.append(('wrong_per_stage_digest',Q,lambda v:v['per_stage'][1].__setitem__('before_and_after_projected_rows_sha256','0'*64)))
cases.append(('wrong_source_pin',Q,lambda v:v['source_records'][0].__setitem__('sha256','0'*64)))
cases.append(('wrong_first_difference',Q,lambda v:v['first_difference']['before'].__setitem__('stage','CURRENT_AUDIT_PINS.json')))
field('erase_whole04_finding','custody/reviews/package_04/VERDICT.json','finding_counts',{'P0':0,'P1':0,'P2':0,'P3':0})
field('erase_root_whole05','custody/ROOT_WHOLE_PACKAGE_REVIEW_04.json','new_complete_whole05_required',False)
field('root_readiness','custody/ROOT_WHOLE_PACKAGE_REVIEW_04.json','publication_ready',True)
field('root_output_binding','custody/ROOT_WHOLE_PACKAGE_REVIEW_04.json','output_pins_sha256','0'*64)
cases.append(('coherent_qual_and_counterexample_false_order',Q,lambda v:v.__setitem__('additional1558_global_order_preserved',True)))
tool=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
for version in ['3.11','3.14']:
 py='/opt/homebrew/bin/python'+version
 for opt in [False,True]:
  tag='py'+version.replace('.','')+('_optimized' if opt else '_normal')
  run(py,opt,tag+'_default_verify',['scripts/verify_package.py'])
  run(py,opt,tag+'_strict_external_binding',['scripts/verify_package.py','--require-bindings','--bindings',P/'UPLOAD_BINDINGS.json','--archive',P/Z])
  out=scratch/(tag+'-checker');run(py,opt,tag+'_unchanged_actual_checker',['scripts/check.py','--out',out])
  products.extend(pin(p,p.relative_to(scratch)) for p in sorted(out.rglob('*')) if p.is_file())
  archive=scratch/(tag+'-rebuilt.zip');run(py,opt,tag+'_documented_rebuild',['scripts/build_archive.py','--out',archive]);need(archive.read_bytes()==data,'Actual rebuilt ZIP equality');products.append(pin(archive,archive.relative_to(scratch)))
  local=run(py,opt,tag+'_native_LOCAL_only',[tool,'check',A/'publication/zenodo-deposit.json'],cwd=scratch)
  summary=json.loads(local.stdout);need(summary['files']==[{'name':'paper.pdf','size':93113,'sha256':'33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b'},{'name':Z,'size':len(data),'sha256':h(data)}],'Native exact asset identities')
  run(py,opt,tag+'_required_missing_binding',['scripts/verify_package.py','--require-bindings','--bindings',scratch/'missing-binding.json'],False)
  bad=read(P/'UPLOAD_BINDINGS.json');bad['archive']['sha256']='0'*64;badpath=scratch/(tag+'-bad-binding.json');write(badpath,bad);run(py,opt,tag+'_corrupt_present_binding',['scripts/verify_package.py','--bindings',badpath,'--archive',P/Z],False)
  for name,path,mutate in cases:
   v=read(root/path);mutate(v);write(root/path,v)
   if name=='coherent_qual_and_counterexample_false_order':
    p=root/'custody/reviews/package_04/HISTORICAL_ORDER_COUNTEREXAMPLE.json';c=read(p);c['actual_additional_global_order_preserved']=True;c['mismatched_positions']=0;write(p,c)
   coherent_refresh();r=run(py,opt,tag+'_semantic_'+name,['scripts/verify_package.py'],False)
   need('Member mismatch:' not in r.stderr and 'Custody copy mismatch:' not in r.stderr,'Semantic fault rejected only by stale checksum')
   faults.append({'runtime':version,'optimized':opt,'case':name,'rejected':True,'outer_manifest_and_copy_hashes_coherent':True,'stderr_sha256':h(r.stderr.encode())});restore([path]+(['custody/reviews/package_04/HISTORICAL_ORDER_COUNTEREXAMPLE.json'] if name=='coherent_qual_and_counterexample_false_order' else []))
  run(py,opt,tag+'_final_clean_verify',['scripts/verify_package.py'])
  need({str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}==original,'Clean extraction bytes changed')
write(D/'CONTROL_RECEIPTS.json',{'utc':now(),'status':'PASS','records':commands,'actual_commands':len(commands)})
write(D/'SEMANTIC_CONTROLS.json',{'utc':now(),'status':'PASS','records':faults,'actual_rejections':len(faults),'cases_per_runtime_mode':len(cases)})
write(D/'SCRATCH_PRODUCT_PINS.json',{'utc':now(),'records':products,'scratch':str(scratch),'retained':True})
summary={'utc':now(),'status':'PASS','actual_commands':len(commands),'expected_successes':sum(r['expected_success'] for r in commands),'expected_rejections':sum(not r['expected_success'] for r in commands),'semantic_rejections':len(faults),'runtime_modes':4,'clean_members':len(original),'actual_external_checker_normal_and_optimized':True,'actual_native_LOCAL_only':True,'four_rebuilds_byte_exact':True,'no_PDF_compile_or_render':True,'scratch':str(scratch)}
write(D/'CONTROL_SUMMARY.json',summary);print(json.dumps(summary))
