from pathlib import Path
import os,sys,json,hashlib,subprocess,zipfile,shutil,struct,zlib,datetime
O=Path(__file__).resolve().parent; A=O.parent.parent; P=A/'preprint_v1_0'; S=O/'scratch'; S.mkdir(exist_ok=True); K=S/'kit';K.mkdir(exist_ok=True)
R=[]
def req(c,m):
 if not c:raise RuntimeError(m)
def h(b):return hashlib.sha256(b).hexdigest()
def execute(name,args,cwd=K,ok=True,env=None):
 q=subprocess.run(args,cwd=cwd,capture_output=True,text=True,env=env)
 r={'name':name,'argv':list(map(str,args)),'cwd':str(cwd),'returncode':q.returncode,'expected_success':ok,'stdout':q.stdout,'stderr':q.stderr};R.append(r)
 (O/'EXECUTION_RECEIPTS.json').write_text(json.dumps(R,indent=2)+'\n')
 req((q.returncode==0)==ok,name+' return code');return q
with zipfile.ZipFile(P/'support.zip') as z:
 z.extractall(K)
 allow=json.loads((P/'SUPPORT_ALLOWLIST.json').read_text())['members'];infos=z.infolist();req([i.filename for i in infos]==allow,'sorted exact payload')
 details=[]
 for i in infos:
  b=z.read(i);req(b==(P/i.filename).read_bytes(),'payload '+i.filename)
  req(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.internal_attr==0 and i.compress_type==8 and i.flag_bits==0 and i.extra==b'' and i.comment==b'','headers '+i.filename)
  req(zlib.crc32(b)&0xffffffff==i.CRC,'CRC '+i.filename)
  details.append({'path':i.filename,'bytes':len(b),'sha256':h(b),'crc32':i.CRC,'header_offset':i.header_offset})
 req(z.comment==b'','archive comment')
 (O/'CLOSED_ZIP.json').write_text(json.dumps({'members':details,'count':len(details),'archive_bytes':(P/'support.zip').stat().st_size,'sha256':h((P/'support.zip').read_bytes()),'all_payload_and_headers_verified':True},indent=2)+'\n')
for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
 pre=[sys.executable,'-I','-B',*flags]
 execute(mode+'_clean_verify',pre+['verify_package.py'])
 execute(mode+'_checks',pre+['run_checks.py','--out-dir','tmp/check-'+mode])
 execute(mode+'_build',pre+['build_archive.py','--output','tmp/rebuilt-'+mode+'.zip'])
 req((K/('tmp/rebuilt-'+mode+'.zip')).read_bytes()==(P/'support.zip').read_bytes(),'byte identical ZIP')
 execute(mode+'_archive_verify',pre+['verify_package.py','--archive','tmp/rebuilt-'+mode+'.zip'])
 execute(mode+'_binding_absent_required',pre+['verify_package.py','--require-deposit-binding'],ok=False)
 binding=K/'publication/DEPOSIT_BINDING.json';binding.write_bytes((P/'publication/DEPOSIT_BINDING.json').read_bytes())
 execute(mode+'_present_binding',pre+['verify_package.py','--archive','tmp/rebuilt-'+mode+'.zip','--require-deposit-binding'])
 good=binding.read_bytes();binding.write_text('{}');execute(mode+'_corrupt_binding',pre+['verify_package.py','--archive','tmp/rebuilt-'+mode+'.zip'],ok=False);binding.write_bytes(good)
 bad=json.loads(good);bad['paper_pdf']['bytes']+=1;binding.write_text(json.dumps(bad));execute(mode+'_wrong_binding',pre+['verify_package.py','--archive','tmp/rebuilt-'+mode+'.zip'],ok=False);binding.unlink()
 extra=K/'unlisted.txt';extra.write_text('extra');execute(mode+'_extra_file',pre+['verify_package.py'],ok=False);extra.unlink()
 source=K/'metadata.json';data=source.read_bytes();source.write_bytes(data+b' ');execute(mode+'_hash_corrupt',pre+['verify_package.py'],ok=False);source.write_bytes(data)
 for member in ['SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json']:
  source=K/member;data=source.read_bytes();save=S/('saved-'+member);source.rename(save);source.symlink_to(save)
  q=execute(mode+'_symlink_'+member,pre+['verify_package.py'],ok=False);req('symlink' in q.stderr and 'JSONDecodeError' not in q.stderr,'preparse manifest/allow guard');source.unlink();save.rename(source)
 # Fresh case aliases and absent descendants, static filesystem checks.
 req(K.samefile(S/'KIT'),'case insensitive fixture unavailable')
 for suffix in ['unlisted.zip','absent/deep/unlisted.zip']:
  dest=S/'KIT'/suffix
  execute(mode+'_case_reject_'+suffix,pre+['build_archive.py','--output',str(dest)],ok=False);req(not dest.exists() and not (K/'absent').exists(),'unlisted no effects')
 for suffix in ['tmp/case-allowed.zip','TMP/existing-case-allowed.zip']:
  dest=S/'KIT'/suffix;execute(mode+'_case_allowed_'+suffix,pre+['build_archive.py','--output',str(dest)]);req(dest.read_bytes()==(P/'support.zip').read_bytes(),'allowed current archive')
 external=S/('external-'+mode+'.zip');execute(mode+'_external_allowed',pre+['build_archive.py','--output',str(external)])
 execute(mode+'_support_regenerate',pre+['build_archive.py','--output','support.zip']);req((K/'support.zip').read_bytes()==(P/'support.zip').read_bytes(),'support regenerate')
 # Explicit direct, file link, hardlink, directory link and case aliases of every excluded/current input.
 binding.write_bytes(good)
 for member in ['paper.pdf','metadata.json','publication/DEPOSIT_BINDING.json']:
  protected=K/member;before=protected.read_bytes()
  for kind in ['direct','symlink','hardlink','directory','case']:
   alias=S/('protected-'+mode+'.zip');linkdir=S/'diralias'
   if kind=='direct':dest=protected
   elif kind=='symlink':alias.symlink_to(protected);dest=alias
   elif kind=='hardlink':os.link(protected,alias);dest=alias
   elif kind=='directory':linkdir.symlink_to(protected.parent,target_is_directory=True);dest=linkdir/protected.name
   else:dest=S/'KIT'/member
   q=execute(mode+'_protected_'+member+'_'+kind,pre+['build_archive.py','--output',str(dest)],ok=False)
   req('cannot overwrite protected package input' in q.stderr,'identity guard first')
   req(protected.read_bytes()==before,'protected no writes')
   if alias.exists() or alias.is_symlink():alias.unlink()
   if linkdir.is_symlink():linkdir.unlink()
 binding.unlink()
 # Every excluded local stage file individually protected; install exact current bytes then remove.
 excluded=json.loads((P/'EXCLUSION_LEDGER.json').read_text())['local_package_files']
 for member in excluded:
  if member in ['support.zip','publication/DEPOSIT_BINDING.json']:continue
  dest=K/member;dest.write_bytes((P/member).read_bytes());before=dest.read_bytes()
  q=execute(mode+'_excluded_protected_'+member,pre+['build_archive.py','--output',str(dest)],ok=False)
  req('cannot overwrite protected package input' in q.stderr and dest.read_bytes()==before,'excluded protection');dest.unlink()
 # PDF preflight, using a compiler sentinel executable to detect accidental invocation.
 bindir=S/'bin';bindir.mkdir(exist_ok=True);engine=bindir/'tectonic';marker=S/'compiler-called'
 engine.write_text('#!/bin/sh\necho called >> "'+str(marker)+'"\nexit 98\n');engine.chmod(0o755);env=dict(os.environ,PATH=str(bindir)+os.pathsep+os.environ.get('PATH',''))
 for kind in ['direct','directory','child-symlink','child-hardlink','case']:
  out=S/('pdf-'+mode+'-'+kind);linkdir=S/'pdf-diralias'
  if kind=='direct':out=K
  elif kind=='directory':linkdir.symlink_to(K,target_is_directory=True);out=linkdir
  elif kind=='case':out=S/'KIT'
  else:
   out.mkdir(exist_ok=True)
   if kind=='child-symlink':(out/'paper.pdf').symlink_to(K/'paper.pdf')
   else:os.link(K/'paper.pdf',out/'paper.pdf')
  q=execute(mode+'_pdf_alias_'+kind,pre+['build_pdf.py','--out-dir',str(out)],ok=False,env=env)
  req('aliases canonical' in q.stderr and not marker.exists(),'PDF preflight no compiler')
  if linkdir.is_symlink():linkdir.unlink()
 # Other root spelling direction: actual root KIT and lower output kit.
 K.rename(S/'KIT');K=S/'KIT'
 for suffix in ['new.zip','missing/nested/new.zip']:
  dest=S/'kit'/suffix;execute(mode+'_reverse_case_reject_'+suffix,pre+['build_archive.py','--output',str(dest)],cwd=K,ok=False);req(not dest.exists(),'reverse no write')
 K.rename(S/'kit');K=S/'kit'
 # Reset support.zip because extraction defaults exclude it, preserving clean no-binding behavior.
 (K/'support.zip').unlink()
# Actual supported compilation, no authoring operation: unchanged source read-only reproduction.
execute('actual_compile',[sys.executable,'-I','-B',str(P/'build_pdf.py'),'--out-dir',str(S/'compiled')],cwd=S)
execute('actual_pdfinfo',['pdfinfo',str(S/'compiled/paper.pdf')],cwd=S)
execute('actual_render',['pdftoppm','-r','95','-png',str(S/'compiled/paper.pdf'),str(S/'page')],cwd=S)
execute('native_manifest_local_check',[sys.executable,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(P/'publication/zenodo-deposit.json')],cwd=S)
# Read-only object authentication of all nine submitted files, no index/branch changes.
pins=json.loads((A/'SUBMITTED_PINS.json').read_text());auth=[]
for item in pins['files']:
 q=execute('git_blob_'+item['snapshot_path'],['git','cat-file','blob',pins['head_oid']+':'+item['repository_path']],cwd=A)
 b=q.stdout.encode();local=(A/item['snapshot_path']).read_bytes();req(b==local and h(b)==item['sha256'] and len(b)==item['bytes'],'nine original object authentication')
 auth.append(item)
(O/'ORIGINAL_NINE_AUTHENTICATION.json').write_text(json.dumps({'head_oid':pins['head_oid'],'all_nine_exact':True,'records':auth},indent=2)+'\n')
# Full-object metadata and selected-copy checks, independent of candidate verifier.
meta=json.loads((P/'metadata.json').read_text())
for member in ['publication/release_metadata.json','publication/zenodo.json','publication/zenodo-deposit.json']:req(json.loads((P/member).read_text())['metadata']==meta,'full metadata object '+member)
copies=json.loads((P/'COPY_MAP.json').read_text())['copies'];req(copies==json.loads((P/'SAFE_INPUT_PINS.json').read_text())['records'],'copy pin equality')
for row in copies:
 b=(P/row['package_path']).read_bytes();req(h(b)==row['sha256'] and len(b)==row['bytes'],'copied bytes '+row['package_path']);req(b==(A/row['source_path']).read_bytes(),'original copy identity '+row['source_path'])
prior=json.loads((A/'repairs/case_alias01/before/preprint_v1_0/COPY_MAP.json').read_text())['copies'];req(copies[:len(prior)]==prior and len(prior)==163 and len(copies)==165,'copy append only')
(O/'CURRENT_INTEGRITY.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'copied_records':len(copies),'old_ordered_copies_preserved':len(prior),'metadata_objects_exact':True,'all_commands_pass_expected':True,'actual_pdf_sha256':h((S/'compiled/paper.pdf').read_bytes()),'canonical_pdf_sha256':h((P/'paper.pdf').read_bytes()),'execution_count':len(R)},indent=2)+'\n')
print('PASS',len(R),'commands, 198 CLOSED ZIP members, 165 copies')
