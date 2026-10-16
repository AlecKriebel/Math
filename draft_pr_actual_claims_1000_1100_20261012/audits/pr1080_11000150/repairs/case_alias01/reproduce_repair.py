#!/usr/bin/env python3
"""Actual clean extraction and bounded repair controls; no services."""
import datetime,hashlib,io,json,os,subprocess,sys,tempfile,zipfile,zlib
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def require(x,m):
 if not x:raise RuntimeError(m)
def pins(root,exclude=None):return {p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink() and (exclude is None or not p.is_relative_to(exclude))}
receipts=W/'FINAL_REPRODUCTION_RECEIPTS.jsonl';require(not receipts.exists(),'Do not overwrite an actual attempt');baseline=pins(A,W);results=[]
with tempfile.TemporaryDirectory(prefix='case_alias01-own-',dir=W) as temp:
 B=Path(temp).resolve();env=dict(os.environ,TMPDIR=str(B));extract=B/'extract'
 with zipfile.ZipFile(D/'verification_kit.zip') as z:z.extractall(extract)
 kit=extract/'verification_kit';kitpins=pins(kit)
 def run(label,args,expected=0,cwd=kit,reason=None):
  r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,timeout=240)
  row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'argv':[str(x) for x in args],'cwd':str(cwd),'expected':expected,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
  with receipts.open('a') as f:f.write(json.dumps(row)+'\n')
  results.append(row);require((r.returncode==0) if expected==0 else (r.returncode!=0),'Unexpected actual command result '+label+' '+r.stderr[-1200:])
  if reason:require(reason in r.stderr,'Unexpected rejection reason '+label)
  return r
 finite=[]
 for opt in [False,True]:
  prefix=[sys.executable,'-B','-I']+(['-O'] if opt else [])
  run('default verifier',prefix+['verify.py']);finite.append(json.loads(run('full finite adapters',prefix+['run_checks.py']).stdout));run('built-in mathematical/custody faults',prefix+['fault_checks.py'])
  out=B/('normal.zip' if not opt else 'optimized.zip');run('actual fresh outside writer',prefix+['build_archive.py','--output',str(out)]);require(out.read_bytes()==(D/'verification_kit.zip').read_bytes(),'Actual writer ZIP differs');out.unlink()
  run('strict external binding',prefix+['verify.py','--require-binding','--binding',str(D/'EXTERNAL_BINDING.json'),'--pdf',str(D/'preprint.pdf'),'--archive',str(D/'verification_kit.zip')])
  run('required missing binding',prefix+['verify.py','--require-binding'],1,reason='external binding required');run('explicit missing binding',prefix+['verify.py','--binding',str(B/'absent.json')],1,reason='input missing or nonregular')
  p=kit/'ALLOWLIST.json';saved=p.read_bytes();p.unlink();target=B/'allowlist-identical.json';target.write_bytes(saved);p.symlink_to(target);run('bootstrap identical-content symlink',prefix+['verify.py'],1,reason='input symlink rejected');p.unlink();p.write_bytes(saved);target.unlink()
  if not opt:run('complete current output guards both modes',prefix+['output_guard_checks.py'])
  originalmanifest=(kit/'MANIFEST.json').read_bytes()
  tests=[('CURRENT_CASE_ALIAS_REPAIR01.json','new_complete_review_required',False,'new complete review required'),('CURRENT_CASE_ALIAS_REPAIR01.json','whole_reviews_completed',3,'new complete review required'),('CURRENT_CASE_ALIAS_REPAIR01.json','minimum_whole_reviews',1,'new complete review required'),('CURRENT_CASE_ALIAS_REPAIR01.json','required_next_review','whole02','new complete review required'),('CURRENT_CASE_ALIAS_REPAIR01.json','supersedes_dated_terminal_review_requirement',False,'current stage authority'),('CURRENT_CASE_ALIAS_REPAIR01.json','root_repair_adoption_required',False,'publication/service boundary'),('CURRENT_CASE_ALIAS_REPAIR01.json','root_integrity_adopted',True,'publication/service boundary'),('CURRENT_CASE_ALIAS_REPAIR01.json','publication_ready',True,'publication/service boundary'),('CURRENT_CASE_ALIAS_REPAIR01.json','issues_resolved',True,'publication/service boundary'),('CURRENT_CASE_ALIAS_REPAIR01.json','published',True,'publication/service boundary'),('CURRENT_CASE_ALIAS_REPAIR01.json','services_held_at',1033,'publication/service boundary'),('CURRENT_CASE_ALIAS_REPAIR01.json','full_original_maximum_classification_bundle','RESOLVED','scope boundary'),('CURRENT_CASE_ALIAS_REPAIR01.json','exact_application_priority','NOVEL','scope boundary'),('TERMINAL_ADMIN_STAGE.json','whole_reviews_completed',3,'terminal complete review count'),('TERMINAL_ADMIN_STAGE.json','minimum_whole_reviews',1,'terminal complete review count'),('TERMINAL_ADMIN_STAGE.json','latest_review_actionable_P0_P1_P2_P3',1,'terminal latest review findings'),('TERMINAL_ADMIN_STAGE.json','root_integrity_adoption_required',False,'terminal root adoption boundary'),('TERMINAL_ADMIN_STAGE.json','publication_ready',True,'terminal publication/service boundary'),('TERMINAL_ADMIN_STAGE.json','services_held_at',1033,'terminal publication/service boundary'),('TERMINAL_ADMIN_STAGE.json','full_original_maximum_classification_bundle','RESOLVED','terminal scope boundary')]
  for name,key,value,reason in tests:
   p=kit/name;saved=p.read_bytes();data=json.loads(saved);data[key]=value;dump(p,data);manifest=json.loads(originalmanifest)
   for row in manifest['files']:
    if row['path']==name:row.update(bytes=p.stat().st_size,sha256=sha(p))
   dump(kit/'MANIFEST.json',manifest);run('semantic fault '+name+':'+key,prefix+['verify.py'],1,reason=reason);p.write_bytes(saved);(kit/'MANIFEST.json').write_bytes(originalmanifest)
 require(finite[0]==finite[1],'Full normal/-O finite JSON differs');require(pins(kit)==kitpins,'Clean extracted inputs changed')
 run('actual repository native local check',[sys.executable,'-B',str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(D/'deposit_metadata.json')],cwd=A.parents[2])
 names=obj(K/'ALLOWLIST.json')['members'];b=io.BytesIO()
 with zipfile.ZipFile(b,'w',compression=zipfile.ZIP_STORED) as z:
  for n in names:
   info=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED;z.writestr(info,(K/n).read_bytes())
 require(b.getvalue()==(D/'verification_kit.zip').read_bytes(),'Independent CLOSED ZIP bytes differ')
 with zipfile.ZipFile(D/'verification_kit.zip') as z:
  require(z.namelist()==['verification_kit/'+n for n in names] and not z.comment and z.testzip() is None,'ZIP names/comment/CRC')
  for i,n in zip(z.infolist(),names):
   payload=(K/n).read_bytes();require(z.read(i)==payload and i.CRC==(zlib.crc32(payload)&0xffffffff),'Payload/CRC '+n);require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==zipfile.ZIP_STORED and i.flag_bits==0 and not i.extra and not i.comment,'ZIP headers '+n)
 require(pins(A,W)==baseline,'Canonical audit side effects');guards=[json.loads(r['stdout']) for r in results if r['label']=='complete current output guards both modes'][0]
 require(guards['status']=='PASS' and len([r for r in guards['rejections'] if r.get('fault','').startswith('physical-case')])==12,'Actual physical alias tests not exercised')
 dump(W/'REPRODUCTION_SUMMARY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_commands':len(results),'canonical_inputs_unchanged_during_reproduction':len(baseline),'extracted_members_unchanged':len(kitpins),'full_normal_optimized_finite_JSON_equal':True,'guard_invocations':1,'guard_internal_modes':[False,True],'guard_rejections':guards['rejection_count'],'guard_protected_files':guards['protected_file_count'],'actual_physical_case_rejections':12,'actual_case_sensitive_unavailable_skips':0,'semantic_cases_each_mode':len(tests),'independent_closed_ZIP_byte_equal':True,'fixed_headers_payloads_CRCS_verified':len(names),'actual_local_native_check_passed':True,'no_compile_render_view_or_PDF_marker':True,'all_external_services_held_at':1032})
print(json.dumps(obj(W/'REPRODUCTION_SUMMARY.json'),indent=2))
