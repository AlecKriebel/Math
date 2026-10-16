#!/usr/bin/env python3
"""Actual, focused static-filesystem controls in one disposable own extraction."""
from pathlib import Path
import binascii,datetime,hashlib,json,os,shutil,subprocess,sys,zipfile,zlib
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0';TMP=HERE/'scratch'
def require(c,m):
 if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def cli(script,*args,optimized=False):return [sys.executable,'-I','-B',*(['-O'] if optimized else []),str(script),*map(str,args)]
def main():
 require(not TMP.exists(),'scratch already exists; inspect before resumption');TMP.mkdir()
 clean=TMP/'clean';clean.mkdir();alias=TMP/'CLEAN'
 require(alias.is_dir() and alias.samefile(clean),'actual case-insensitive identity not available')
 archive=(PACKAGE/'support.zip').read_bytes();allow=load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members']
 with zipfile.ZipFile(PACKAGE/'support.zip') as z:
  require(z.namelist()==allow and z.testzip() is None,'canonical ZIP member/CRC failure')
  for info in z.infolist():
   require(not Path(info.filename).is_absolute() and '..' not in Path(info.filename).parts,'unsafe canonical member')
  z.extractall(clean)
 originals={n:(clean/n).read_bytes() for n in allow}
 canonical_baseline={p.relative_to(PACKAGE).as_posix():sha(p.read_bytes()) for p in PACKAGE.rglob('*') if p.is_file() and not {'tmp','__pycache__'}.intersection(p.relative_to(PACKAGE).parts)}
 def unchanged():
  require(all((clean/n).read_bytes()==b for n,b in originals.items()),'extracted protected member changed')
  require(all(sha((PACKAGE/n).read_bytes())==s for n,s in canonical_baseline.items()),'canonical package bytes changed during validation')
 rows=[]
 def run(name,argv,expected=True,cwd=clean,message=None):
  started=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
  row={'name':name,'started_utc':started,'argv':argv,'cwd':str(cwd),'expected_success':expected,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
  rows.append(row)
  with (HERE/'EXECUTIONS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  require((r.returncode==0)==expected,'unexpected result '+name)
  if expected:require(not r.stderr,'successful command stderr '+name)
  if message:require(message in r.stderr,'wrong rejection '+name)
  return row
 case_records=[];guard_records=[];binding_records=[];allowed_records=[]
 # Four standard-library README commands in both modes; no PDF command invoked.
 for optimized in [False,True]:
  mode='optimized' if optimized else 'normal'
  run(mode+' README verify',cli(clean/'verify_package.py',optimized=optimized))
  run(mode+' README finite diagnostics',cli(clean/'run_checks.py','--out-dir','tmp/'+mode+'-recheck',optimized=optimized))
  run(mode+' README build',cli(clean/'build_archive.py','--output','tmp/'+mode+'-rebuilt.zip',optimized=optimized))
  run(mode+' README verify rebuilt',cli(clean/'verify_package.py','--archive','tmp/'+mode+'-rebuilt.zip',optimized=optimized))
  require((clean/'tmp'/ (mode+'-rebuilt.zip')).read_bytes()==archive,'README rebuilt bytes differ')
 unchanged()
 for optimized in [False,True]:
  mode='optimized' if optimized else 'normal'
  for scriptroot,outroot,direction in [(clean,alias,'canonical-script_alias-output'),(alias,clean,'alias-script_canonical-output')]:
   require(scriptroot.samefile(outroot),'script/output roots not physically identical')
   require(scriptroot.resolve()!=outroot.resolve(),'resolve spellings unexpectedly equal')
   for stem,parts in [('fresh',['blocked.zip']),('missing-one',['absent-one','blocked.zip']),('missing-two',['absent-two','deeper','blocked.zip'])]:
    output=outroot.joinpath(*parts);created=outroot/parts[0];require(not created.exists(),'case target already exists')
    row=run(mode+' '+direction+' '+stem,cli(scriptroot/'build_archive.py','--output',output,optimized=optimized),False,message='inside package output must be support.zip or under tmp/')
    require(not created.exists(),'rejection created absent file/directory')
    case_records.append({'mode':mode,'direction':direction,'shape':stem,'output':str(output),'script_root':str(scriptroot),'output_root':str(outroot),'samefile':scriptroot.samefile(outroot),'script_root_stat':[scriptroot.stat().st_dev,scriptroot.stat().st_ino],'output_root_stat':[outroot.stat().st_dev,outroot.stat().st_ino],'resolved_spellings_differ':scriptroot.resolve()!=outroot.resolve(),'returncode':row['returncode'],'no_created_descendant':True})
   # Matching canonical controls, even for the alias-spelled script root.
   for parts in [('control.zip',),('control-absent','next','control.zip')]:
    output=scriptroot.joinpath(*parts);require(not output.exists(),'canonical control exists')
    row=run(mode+' '+direction+' canonical control '+str(parts),cli(scriptroot/'build_archive.py','--output',output,optimized=optimized),False,message='inside package output must be support.zip or under tmp/')
    require(not (scriptroot/parts[0]).exists(),'canonical rejection created output')
    case_records.append({'mode':mode,'direction':direction,'shape':'canonical-control/'+str(parts),'output':str(output),'returncode':row['returncode'],'no_created_descendant':True})
   for target,label in [(clean/'support.zip','canonical-support'),(clean/'tmp'/mode/direction/'new'/'rebuilt.zip','canonical-tmp-missing-descendants'),(TMP/(mode+'-'+direction+'-external.zip'),'external')]:
    row=run(mode+' '+direction+' allowed '+label,cli(scriptroot/'build_archive.py','--output',target,optimized=optimized))
    require(target.read_bytes()==archive,'allowed ZIP differs '+label);allowed_records.append({'mode':mode,'direction':direction,'kind':label,'output':str(target),'returncode':row['returncode'],'bytes':len(archive),'sha256':sha(archive)})
    if label=='external':target.unlink()
   # Existing tmp identity alias remains intentionally mutable.
   tmpalias=outroot/'TMP'/mode/direction/'alias-tmp.zip';require((outroot/'TMP').samefile(clean/'tmp'),'tmp alias identity absent')
   run(mode+' '+direction+' allowed existing tmp case alias',cli(scriptroot/'build_archive.py','--output',tmpalias,optimized=optimized));require(tmpalias.read_bytes()==archive,'tmp alias ZIP differs')
   allowed_records.append({'mode':mode,'direction':direction,'kind':'existing-tmp-case-alias','samefile_tmp':True,'output':str(tmpalias),'sha256':sha(archive)})
 unchanged()
 # External/excluded current binding and dated stage seal receive the same guard.
 for name in ['publication/DEPOSIT_BINDING.json','TERMINAL_OUTPUT_PINS.json','publication/zenodo-deposit.json']:
  target=clean/name;target.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(PACKAGE/name,target)
 sentinels=['paper.tex','paper.pdf','metadata.json','build_archive.py','verify_package.py','REPAIR_STATUS_CASE_ALIAS01.json','SUPPORT_MANIFEST.json','publication/DEPOSIT_BINDING.json','TERMINAL_OUTPUT_PINS.json','publication/zenodo-deposit.json']
 for optimized in [False,True]:
  mode='optimized' if optimized else 'normal'
  for name in sentinels:
   target=clean/name;before=target.read_bytes()
   for kind in ['direct','symlink','hardlink','directory-symlink']:
    if kind=='direct':out=target
    elif kind=='symlink':out=TMP/'protected-symlink.zip';out.symlink_to(target)
    elif kind=='hardlink':out=TMP/'protected-hardlink.zip';os.link(target,out)
    else:
     link=TMP/'protected-directory';link.symlink_to(target.parent,target_is_directory=True);out=link/target.name
    row=run(mode+' protected '+kind+' '+name,cli(clean/'build_archive.py','--output',out,optimized=optimized),False,message='cannot overwrite protected package input')
    require(target.read_bytes()==before,'protected sentinel changed')
    guard_records.append({'mode':mode,'protected':name,'alias_kind':kind,'returncode':row['returncode'],'bytes_unchanged':True})
    if kind in ['symlink','hardlink']:out.unlink()
    elif kind=='directory-symlink':link.unlink()
  row=run(mode+' strict valid required binding',cli(clean/'verify_package.py','--require-deposit-binding',optimized=optimized));binding_records.append({'mode':mode,'kind':'required-present','returncode':row['returncode']})
  row=run(mode+' strict required missing binding',cli(clean/'verify_package.py','--deposit-binding','tmp/absent-binding.json','--require-deposit-binding',optimized=optimized),False,message='required deposit binding absent');binding_records.append({'mode':mode,'kind':'required-missing','returncode':row['returncode']})
  for kind,obj in [('missing-fields',{'schema_version':1}),('wrong-ZIP',dict(load(PACKAGE/'publication/DEPOSIT_BINDING.json'),support_archive={'path':'support.zip','bytes':0,'sha256':'0'*64})),('extra-field',dict(load(PACKAGE/'publication/DEPOSIT_BINDING.json'),unexpected=True))]:
   binding=clean/'tmp'/('invalid-'+kind+'.json');write(binding,obj)
   row=run(mode+' strict malformed binding '+kind,cli(clean/'verify_package.py','--deposit-binding',binding,optimized=optimized),False);binding_records.append({'mode':mode,'kind':kind,'returncode':row['returncode']})
 unchanged()
 # New current repair gate must reject coherent (rehash-adjusted) false states.
 gate='REPAIR_STATUS_CASE_ALIAS01.json'
 for optimized in [False,True]:
  mode='optimized' if optimized else 'normal'
  for field,value in [('whole_package_reviews_completed',4),('new_complete_whole04_required',False),('root_repair_adoption_required',False),('publication_ready',True),('ascending_publication_hold_after_pr',1033)]:
   altered=json.loads(originals[gate]);altered[field]=value;write(clean/gate,altered)
   manifest=json.loads(originals['SUPPORT_MANIFEST.json'])
   for r in manifest['entries']:
    if r['path']==gate:r.update(bytes=(clean/gate).stat().st_size,sha256=sha((clean/gate).read_bytes()))
   write(clean/'SUPPORT_MANIFEST.json',manifest)
   # Exclude the archive in this test: the current stage guard must itself fail.
   (clean/'support.zip').unlink(missing_ok=True)
   run(mode+' coherent current gate fault '+field,cli(clean/'verify_package.py',optimized=optimized),False)
   (clean/gate).write_bytes(originals[gate]);(clean/'SUPPORT_MANIFEST.json').write_bytes(originals['SUPPORT_MANIFEST.json'])
   # Descriptor requires an archive; recreate from the known exact byte string.
   (clean/'support.zip').write_bytes(archive)
 unchanged()
 independent=TMP/'independent.zip'
 with zipfile.ZipFile(independent,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
  for name in sorted(originals):
   info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=(0o100644<<16);info.compress_type=8;info.internal_attr=0
   z.writestr(info,originals[name],compress_type=8,compresslevel=9)
 require(independent.read_bytes()==archive,'closed independent ZIP bytes differ')
 headers=[]
 with zipfile.ZipFile(independent) as z:
  require(z.namelist()==allow and z.testzip() is None,'independent member set or CRC failed')
  for info in z.infolist():
   b=z.read(info);require(b==originals[info.filename],'independent member bytes differ');require(info.CRC==(binascii.crc32(b)&0xffffffff),'CRC differs')
   require(info.date_time==(2026,10,14,0,0,0) and info.create_system==3 and info.external_attr==0o100644<<16 and info.compress_type==8 and info.internal_attr==0 and not info.flag_bits&1,'ZIP header policy differs')
   if info.filename!='paper.pdf':b.decode('utf-8')
   headers.append({'name':info.filename,'bytes':info.file_size,'compressed_bytes':info.compress_size,'CRC32':info.CRC,'date_time':info.date_time,'create_system':info.create_system,'external_attr':info.external_attr,'internal_attr':info.internal_attr,'compress_type':info.compress_type,'flag_bits':info.flag_bits})
 independent.unlink()
 tool=AUDIT.parents[2]/'zenodo_deposit_tool/zenodo.py';require(tool.is_file(),'native repository tool missing')
 tool_before=sha(tool.read_bytes());row=run('native repository LOCAL check',cli(tool,'check',PACKAGE/'publication/zenodo-deposit.json'),cwd=PACKAGE);native=json.loads(row['stdout'])
 require(native['files']==[{'name':'paper.pdf','size':(PACKAGE/'paper.pdf').stat().st_size,'sha256':sha((PACKAGE/'paper.pdf').read_bytes())},{'name':'support.zip','size':len(archive),'sha256':sha(archive)}],'native asset identities differ')
 require(tool_before==sha(tool.read_bytes()),'native tool changed')
 write(HERE/'REPOSITORY_LOCAL_CHECK.json',{'scope':'Actual native LOCAL check only, no service/client/token/draft/deposit/DOI operation. Tool read-only. Entire native manifest unchanged; metadata exact.','tool':str(tool),'tool_sha256':tool_before,'native_manifest_sha256':sha((PACKAGE/'publication/zenodo-deposit.json').read_bytes()),'result':native})
 unchanged()
 write(HERE/'CASE_ALIAS_CONTROLS.json',{'pass':True,'static_filesystem_only':True,'real_case_alias_identity':True,'records':case_records,'allowed_outputs':allowed_records})
 write(HERE/'GUARD_CONTROLS.json',{'pass':True,'preserved_protected_file_controls':guard_records,'strict_binding_controls':binding_records,'coherent_current_status_faults_rejected':10,'all_protected_extraction_and_canonical_bytes_unchanged':True})
 write(HERE/'ZIP_VERIFICATION.json',{'pass':True,'independent_closed_archive_equal':True,'canonical_bytes':len(archive),'canonical_sha256':sha(archive),'members':len(headers),'headers_CRC32_and_UTF8_checked':True,'environment':{'python':sys.version,'zlib':zlib.ZLIB_VERSION},'headers':headers})
 write(HERE/'REPRODUCTION_RECEIPTS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'actual_commands':len(rows),'successes':sum(r['returncode']==0 for r in rows),'expected_rejections':sum(r['returncode']!=0 for r in rows),'README_four_stdlib_commands_both_modes':True,'case_controls':len(case_records),'allowed_control_outputs':len(allowed_records),'input_alias_controls':len(guard_records),'strict_binding_controls':len(binding_records),'coherent_current_gate_faults':10,'native_LOCAL_check':True,'no_compilation_rendering_or_marker':True,'samefile_case_alias_both_script_root_directions':True,'fresh_missing_descendants_and_canonical_controls':True,'no_hostile_concurrent_filesystem_claim':True,'all_protected_bytes_unchanged':True,'scratch_removed_after_commands_settled':True})
 shutil.rmtree(TMP)
 print(json.dumps({'pass':True,'commands':len(rows),'case_controls':len(case_records),'allowed':len(allowed_records),'protected_alias_controls':len(guard_records),'members':len(headers)},indent=2))
if __name__=='__main__':
 try:main()
 except OSError as e:
  with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — Actual validation OS failure: '+repr(e)+'. Planned or incomplete tests are not counted as executed.\n')
  raise
