"""Whole03 owned extraction, actual CLI reproduction, alias and coherent-fault controls."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile,shutil,os,datetime
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;P=AUDIT/'preprint_v1_0';TMP=HERE/'tmp';C=TMP/'clean'
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
records=[]
def run(name,args,expected=0,cwd=C,flags=(),env=None):
 argv=[sys.executable,'-I','-B',*flags,*args]
 s=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env=env)
 r={'name':name,'argv':argv,'cwd':str(cwd),'returncode':s.returncode,'stdout':s.stdout,'stderr':s.stderr,'expected_success':expected==0}
 records.append(r)
 with (HERE/'EXECUTIONS.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 need((s.returncode==0)==(expected==0),'unexpected outcome '+name)
 return s
def refresh_manifest():
 m=json.loads((C/'SUPPORT_MANIFEST.json').read_text())
 for x in m['entries']:
  b=(C/x['path']).read_bytes();x.update(bytes=len(b),sha256=sha(b))
 (C/'SUPPORT_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
def baseline_now():return {p.relative_to(C).as_posix():p.read_bytes() for p in C.rglob('*') if p.is_file() and 'tmp' not in p.relative_to(C).parts}
def restore(base):
 for name,b in base.items():
  p=C/name
  if p.is_symlink():p.unlink()
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def unchanged(base):need(all((C/n).read_bytes()==b for n,b in base.items()),'payload changed')
TMP.mkdir(exist_ok=True);need(not C.exists(),'scratch already exists');C.mkdir()
with zipfile.ZipFile(P/'support.zip') as z:z.extractall(C)
base=baseline_now()
for mode in [(),('-O',)]:
 tag='optimized' if mode else 'normal'
 run(tag+'_clean_verify',['verify_package.py'],flags=mode)
 run(tag+'_checks',['run_checks.py','--out-dir','tmp/recheck_'+tag],flags=mode)
 run(tag+'_archive',['build_archive.py','--output','tmp/rebuilt.zip'],flags=mode)
 run(tag+'_archive_verify',['verify_package.py','--archive','tmp/rebuilt.zip'],flags=mode)
 run(tag+'_binding_actual',['verify_package.py','--archive','tmp/rebuilt.zip','--deposit-binding',str(P/'publication/DEPOSIT_BINDING.json'),'--require-deposit-binding'],flags=mode)
 run(tag+'_binding_absent',['verify_package.py','--require-deposit-binding'],expected=1,flags=mode)
 unchanged(base)
run('real_Tectonic_clean_compile',['build_pdf.py','--out-dir','tmp/recompiled'])
b=(C/'tmp/recompiled/paper.pdf').read_bytes();need(b.startswith(b'%PDF-'),'compile missing')
info=subprocess.check_output(['pdfinfo',str(C/'tmp/recompiled/paper.pdf')],text=True)
need('Pages:           5' in info,'compiled page count')
compile_record={'compiler':'real Tectonic','bytes':len(b),'sha256':sha(b),'canonical_byte_identical':b==(P/'paper.pdf').read_bytes(),'pdfinfo':info,'builtin_compiler_success':True}
unchanged(base)
for src in P.rglob('*'):
 if src.is_file() and 'tmp' not in src.relative_to(P).parts:
  name=src.relative_to(P);target=C/name
  if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
base=baseline_now();protected=[n for n in sorted(base) if n!='support.zip'];need(len(protected)==157,'protected set count')
for mode in [(),('-O',)]:
 tag='optimized' if mode else 'normal'
 for name in protected:
  alias=C/'tmp/hardlinked.zip';os.link(C/name,alias)
  result=run(tag+'_hardlink_'+name,['build_archive.py','--output','tmp/hardlinked.zip'],expected=1,flags=mode)
  need('cannot overwrite protected package input' in result.stderr,'not alias guard')
  need(alias.read_bytes()==base[name],'alias target changed');alias.unlink();unchanged(base)
 for name in ['paper.pdf','paper.tex','SUPPORT_MANIFEST.json','CURRENT_OUTPUT_PINS_WHOLE03.json','publication/DEPOSIT_BINDING.json']:
  alias=C/'tmp/linked.zip';alias.symlink_to(C/name)
  result=run(tag+'_symlink_'+name,['build_archive.py','--output','tmp/linked.zip'],expected=1,flags=mode)
  need('cannot overwrite protected package input' in result.stderr,'not symlink guard');alias.unlink();unchanged(base)
  result=run(tag+'_lexical_'+name,['build_archive.py','--output',name],expected=1,flags=mode)
  need('cannot overwrite protected package input' in result.stderr,'not lexical guard');unchanged(base)
 run(tag+'_canonical_archive_allowed',['build_archive.py','--output','support.zip'],flags=mode);unchanged(base)
 run(tag+'_strict_present_binding',['verify_package.py','--require-deposit-binding'],flags=mode)
 # Coherent outer hashes still cannot bypass semantic invariants.
 for name,key,value in [('STATUS.json','whole_package_reviews_completed',1),('CURRENT_STATUS.json','publication_ready',True),('CURRENT_STATUS_WHOLE03.json','issues_updated',True),('CURRENT_STATUS_WHOLE03.json','whole_package_reviews_completed',3),('CURRENT_STATUS_WHOLE03.json','ascending_publication_hold_after_pr',0)]:
  d=json.loads((C/name).read_text());d[key]=value;(C/name).write_text(json.dumps(d,indent=2)+'\n');refresh_manifest()
  run(tag+'_coherent_stage_'+name+'_'+key,['verify_package.py'],expected=1,flags=mode);restore(base)
 for name in ['SUPPORT_MANIFEST.json','SUPPORT_ALLOWLIST.json']:
  target=C/name;stash=C/'tmp/linktarget';stash.write_bytes(target.read_bytes());target.unlink();target.symlink_to(stash)
  result=run(tag+'_manifest_symlink_'+name,['verify_package.py'],expected=1,flags=mode)
  need('missing/symlink member' in result.stderr,'preflight skipped');target.unlink();stash.unlink();restore(base)
 for binding_case in ['wrong_hash','missing_field']:
  name='publication/DEPOSIT_BINDING.json';d=json.loads((C/name).read_text())
  if binding_case=='wrong_hash':d['paper_pdf']['sha256']='0'*64
  else:del d['support_archive']
  (C/name).write_text(json.dumps(d,indent=2)+'\n');run(tag+'_binding_'+binding_case,['verify_package.py'],expected=1,flags=mode);restore(base)
 # PDF alias guard must precede compiler discovery and writes.
 for alias_kind in ['dot','hardlink','file_symlink','directory_symlink']:
  out='.'
  if alias_kind=='hardlink':
   out='tmp/pdfhard';(C/out).mkdir(exist_ok=True);os.link(C/'paper.pdf',C/out/'paper.pdf')
  elif alias_kind=='file_symlink':
   out='tmp/pdfsym';(C/out).mkdir(exist_ok=True);(C/out/'paper.pdf').symlink_to(C/'paper.pdf')
  elif alias_kind=='directory_symlink':
   out='tmp/pdfdir';(C/out).symlink_to(C,target_is_directory=True)
  result=run(tag+'_pdf_alias_'+alias_kind,['build_pdf.py','--out-dir',out],expected=1,flags=mode)
  need('aliases canonical paper.pdf' in result.stderr,'PDF alias not rejected');unchanged(base)
  if alias_kind in ['hardlink','file_symlink']:(C/out/'paper.pdf').unlink();(C/out).rmdir()
  elif alias_kind=='directory_symlink':(C/out).unlink()
 # Delete the repaired archive guard in scratch to prove the control exposes its failure.
 source=(C/'build_archive.py').read_text();source=source.replace("v.require(not alias,'cannot overwrite protected package input '+protected.relative_to(root).as_posix())","pass")
 (C/'build_archive.py').write_text(source);refresh_manifest();alias=C/'tmp/oldbug.zip';os.link(C/'publication/DEPOSIT_BINDING.json',alias)
 run(tag+'_old_bug_reintroduced',['build_archive.py','--output','tmp/oldbug.zip'],flags=mode)
 need((C/'publication/DEPOSIT_BINDING.json').read_bytes()!=base['publication/DEPOSIT_BINDING.json'],'old defect control failed');alias.unlink();restore(base);unchanged(base)
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_commands':len(records),'clean_five_commands_passed':True,'protected_inputs':len(protected),'hardlink_rejections':2*len(protected),'compiler':compile_record,'all_original_extracted_bytes_unchanged':True,'canonical_inputs_not_modified':True,'static_local_filesystem_scope':True}
(HERE/'REPRODUCTION_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
# Preserve only the compiled authored PDF outside disposable scratch for root checks.
shutil.copyfile(C/'tmp/recompiled/paper.pdf',HERE/'private/clean_compiled.pdf')
shutil.rmtree(C)
print(json.dumps(receipt,indent=2))
