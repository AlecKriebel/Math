"""Actual bounded unmodified-wrapper, semantic, path and LOCAL native checks."""
import copy, hashlib, json, os, shutil, subprocess, sys, zipfile
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
from admin import D,A,P,ZIP,read,write,pin,basic,need,log
S=D/'private';S.mkdir(exist_ok=True);C=S/'MixedTerminal05'
PY={'py311':'/opt/homebrew/bin/python3.11','py314':'/opt/homebrew/bin/python3.14'}
def run(label,argv,cwd=S,expected=0,reason=None):
 start=datetime.now(timezone.utc).isoformat();p=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True)
 out=D/(label+'.stdout');err=D/(label+'.stderr');out.write_bytes(p.stdout);err.write_bytes(p.stderr)
 row={'utc':start,'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'exit':p.returncode,'expected_exit':expected,'stdout':basic(out,out.relative_to(D)),'stderr':basic(err,err.relative_to(D))}
 with (D/'COMMANDS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 need(p.returncode==expected,'Unexpected command exit '+label)
 if reason:need(reason.encode() in p.stderr,'Wrong rejection '+label)
 return p
def modes():
 for tag,py in PY.items():
  for mode,flags in [('normal',[]),('optimized',['-O'])]:yield tag+'-'+mode,[py,'-B',*flags]
def remove_duplicate(p,canonical):
 r=pin(p,p.relative_to(D));need(p.read_bytes()==canonical.read_bytes(),'Duplicate not equal')
 with (D/'OWNED_DUPLICATE_CLEANUP.jsonl').open('a') as f:f.write(json.dumps({**r,'canonical':str(canonical.relative_to(A)),'canonical_identity':basic(canonical,canonical.name),'full_bytes_equal':True,'only_this_new_owned_unsealed_duplicate_removed':True})+'\n')
 p.unlink()
def pack(root,path):
 m=read(root/'PACKAGE_MANIFEST.json')
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
  for n in sorted([r['path'] for r in m['members']]+['PACKAGE_MANIFEST.json']):
   i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(root/n).read_bytes())
def main():
 need(not C.exists(),'Fresh controls only');C.mkdir();zipfile.ZipFile(P/ZIP).extractall(C)
 wrapper_results={}
 for label,base in modes():
  run(label+'-runtime',base+['-c','import sys,json;print(json.dumps({"version":sys.version,"float_info":list(sys.float_info),"optimized":not __debug__}))'])
  for kind,root in [('canonical',P),('clean',C)]:
   prefix=label+'-'+kind;run(prefix+'-verify',base+[root/'scripts/verify_package.py'])
   run(prefix+'-strict',base+[root/'scripts/verify_package.py','--require-bindings','--bindings',P/'UPLOAD_BINDINGS.json','--archive',P/ZIP])
   output=S/(prefix+'-check');run(prefix+'-check',base+[root/'scripts/check.py','--out',output]);wrapper_results[prefix]=read(output/'CHECK_RECEIPT.json')
   archive=S/(prefix+'.zip');run(prefix+'-archive',base+[root/'scripts/build_archive.py','--out',archive]);need(archive.read_bytes()==(P/ZIP).read_bytes(),'Actual builder bytes')
   if prefix=='py314-optimized-clean':retained_archive=basic(archive,archive.relative_to(D))
   else:remove_duplicate(archive,P/ZIP)
 for tag in PY:
  results=[]
  for mode in ['normal','optimized']:
   for kind in ['canonical','clean']:
    prefix=tag+'-'+mode+'-'+kind;out=S/(prefix+'-check')
    for inner in ['normal','optimized']:
     result=read(out/inner/'FINITE_CHECKS.json');results.append({k:v for k,v in result.items() if k!='utc'})
  need(all(x==results[0] for x in results),'Complete same-runtime nonUTC JSON differs')
 write(D/'FULL_JSON_RUNTIME_COMPARISON.json',{'status':'PASS','installed_versions':['3.11.8','3.14.6'],'canonical_and_clean':True,'outer_modes':['normal','optimized'],'inner_modes':['normal','optimized'],'full_non_utc_JSON_per_runtime_exact_equal':True,'cross_runtime_exact_equality_claimed':False,'finite_binary64_acceptance_envelopes_not_interval_error_bounds':True,'receipts':wrapper_results,'actual_retained_builder_output':retained_archive})
 sentinel=S/'sentinel';sentinel.write_bytes(b'OWNED TERMINAL05 SENTINEL\n');sentinelpin=basic(sentinel,'sentinel')
 hard=S/'hard';os.link(sentinel,hard);link=S/'linked';link.symlink_to(sentinel);dangling=S/'dangling';dangling.symlink_to(S/'absent');directory=S/'existing';directory.mkdir();parent=S/'syparent';parent.symlink_to(S,target_is_directory=True)
 alias=C.with_name(C.name.swapcase());need(alias.samefile(C),'Physical case alias unavailable')
 cases={'existing-file':sentinel,'existing-dir':directory,'hardlink':hard,'symlink':link,'dangling':dangling,'symlink-parent':parent/'never','inside':C/'never','case-alias':alias/'never','missing-inside':C/'absent/never','missing-case-alias':alias/'absent/never','parent-traversal':S/'absent/../never','missing-outside':S/'missing/never'}
 for label,base in modes():
  for script in ['check.py','build_pdf.py','build_archive.py']:
   for name,path in cases.items():run(label+'-'+script+'-'+name,base+[C/'scripts'/script,'--out',path],expected=1)
   run(label+'-'+script+'-reverse-case',base+[alias/'scripts'/script,'--out',C/'reverse-never'],expected=1,reason='outside all frozen package descendants')
  run(label+'-required-absent',base+[C/'scripts/verify_package.py','--require-bindings'],expected=1,reason='Required bindings are absent')
  bad=S/(label+'-bad-binding.json');b=read(P/'UPLOAD_BINDINGS.json');b['pdf']['sha256']='0'*64;write(bad,b)
  run(label+'-corrupt-present',base+[C/'scripts/verify_package.py','--bindings',bad,'--archive',P/ZIP],expected=1,reason='Upload PDF binding mismatch')
  run(label+'-missing-archive',base+[C/'scripts/verify_package.py','--bindings',P/'UPLOAD_BINDINGS.json','--archive',S/'absent-archive'],expected=1,reason='Present bindings require')
  need(basic(sentinel,'sentinel')==sentinelpin,'Sentinel changed')
 # Coherent faults update every active copy-map pin, all manifest pins, the
 # complete closed ZIP and strict external binding before invoking the actual CLI.
 faults=[]
 specifications=[
 ('TERMINAL_AFTER_WHOLE05_STATUS.json',{'publication_ready':True,'issues_resolved':True,'published':True,'services_held_after_pr':1071,'fresh_whole_package_reviews_completed':4,'minimum_fresh_reviews_required':1,'new_complete_whole_review_currently_required':True,'terminal_administration_complete':False,'root_final_integrity_required':False,'root_final_integrity_adopted':True,'latest_complete_review_findings':{'P0':0,'P1':0,'P2':0,'P3':1},'root_review_adoption':'custody/ROOT_WHOLE_PACKAGE_REVIEW_04.json'}),
 ('custody/reviews/package_05/VERDICT.json',{'full_review_complete':False,'repair_only':True,'whole_reviews_completed':4,'findings':[{'id':'fake'}]}),
 ('custody/ROOT_WHOLE_PACKAGE_REVIEW_05.json',{'status':'fake','new_complete_whole_review_currently_required':True,'root_final_integrity_adopted':True}),
 ('HISTORY_ORDER_QUALIFICATION.json',{'additional1558_global_order_preserved':True,'additional1558_exact_row_multiset_preserved':False,'mismatched_global_additional_positions':0}),
 ('custody/reviews/package_05/SOURCE_READ_LEDGER.json',{'worldwide_current_open':'VERIFIED_OPEN'})]
 originalmap=(C/'INPUT_COPY_MAP.json').read_bytes();originalmanifest=(C/'PACKAGE_MANIFEST.json').read_bytes()
 for filename,mutations in specifications:
  target=C/filename;original=target.read_bytes();document=json.loads(original)
  for field,value in mutations.items():
   fault=copy.deepcopy(document);fault[field]=value;write(target,fault)
   copy_map=json.loads(originalmap)
   for row in copy_map['copies']:
    q=C/row['package_copy'];row['bytes']=q.stat().st_size;row['sha256']=hashlib.sha256(q.read_bytes()).hexdigest()
   write(C/'INPUT_COPY_MAP.json',copy_map)
   m=json.loads(originalmanifest)
   for row in m['members']:row.update(basic(C/row['path'],row['path']))
   write(C/'PACKAGE_MANIFEST.json',m);archive=S/'coherent-fault.zip';pack(C,archive)
   b=read(P/'UPLOAD_BINDINGS.json');b['archive']['bytes']=archive.stat().st_size;b['archive']['sha256']=hashlib.sha256(archive.read_bytes()).hexdigest();b['manifest_sha256']=hashlib.sha256((C/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest();binding=S/'coherent-binding.json';write(binding,b)
   z=zipfile.ZipFile(archive);need(z.testzip() is None and all(z.read(n)==(C/n).read_bytes() for n in z.namelist()),'Closed fault ZIP mismatch')
   for label,base in modes():
    p=run('coherent-'+str(len(faults))+'-'+label,base+[C/'scripts/verify_package.py','--require-bindings','--bindings',binding,'--archive',archive],expected=1)
    need(not any(t in p.stderr for t in [b'Member mismatch:',b'Custody copy mismatch:',b'Upload PDF binding mismatch.',b'Upload ZIP binding mismatch.']),'Stale-checksum-only rejection')
   faults.append({'file':filename,'field':field,'all_four_modes_rejected':True,'all_active_copy_map_and_manifest_pins_refreshed':True,'closed_archive':basic(archive,archive.relative_to(D)),'strict_bindings_refreshed':True,'reason':'Semantic/sealed authored evidence guards, after coherent current-member rehash and closed repack.'})
   with (D/'OWNED_FAULT_ARCHIVE_RETIREMENT.jsonl').open('a') as f:f.write(json.dumps({**basic(archive,archive.relative_to(D)),'fault_index':len(faults)-1,'only_new_owned_unsealed_fixture_retired':True})+'\n')
   archive.unlink();target.write_bytes(original);(C/'INPUT_COPY_MAP.json').write_bytes(originalmap);(C/'PACKAGE_MANIFEST.json').write_bytes(originalmanifest)
 # Bootstrap manifest and member and ancestor guards, before JSON policy parsing.
 for name in ['PACKAGE_MANIFEST.json','paper.tex']:
  target=C/name;original=target.read_bytes();target.unlink();target.symlink_to(sentinel)
  for label,base in modes():run('bootstrap-'+name+'-'+label,base+[C/'scripts/verify_package.py'],expected=1,reason='Symlink member/ancestor')
  target.unlink();target.write_bytes(original)
 custody=C/'custody';hidden=C/'owned-custody-backup';custody.rename(hidden);custody.symlink_to(hidden,target_is_directory=True)
 for label,base in modes():run('ancestor-bootstrap-'+label,base+[C/'scripts/verify_package.py'],expected=1,reason='Symlink member/ancestor')
 custody.unlink();hidden.rename(custody)
 native=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py');nativepin=basic(native,str(native))
 for label,base in modes():
  p=run(label+'-native-LOCAL',base+[native,'check',A/'publication/zenodo-deposit.json']);data=json.loads(p.stdout);need(data['environment']=='production' and [r['name'] for r in data['files']]==['paper.pdf',ZIP],'Native check file selection drift')
  run(label+'-historical-wrapper-not-native',base+[native,'check',P/'deposit.json'],expected=1)
  run(label+'-final-clean-verify',base+[C/'scripts/verify_package.py'])
 write(D/'SEMANTIC_CONTROLS.json',{'status':'PASS','cases':faults,'fault_count':len(faults),'runtime_modes':4,'all_active_copy_and_manifest_pins_rehashed_and_closed_archive_repacked_before_semantic_verification':True})
 write(D/'INTERFACE_CONTROLS.json',{'status':'PASS','canonical_clean_actual_unmodified_wrappers':True,'writers':3,'path_cases_each':13,'runtime_modes':4,'sentinel':sentinelpin,'sentinel_unchanged':basic(sentinel,'sentinel')==sentinelpin,'default_absent_strict_present_required_missing_corrupt_present_missing_archive_cases':True,'bootstrap_manifest_member_ancestor_before_JSON':True,'native_checker_source':nativepin,'native_semantic_source_scope':'load_manifest, run check dispatch, main parser; check returns before local_state, token_for, client or network. Actual four LOCAL checks only.','no_compile_render_of_unchanged_paper':True})
 log('Actual unmodified canonical+clean verification/check/archive wrappers passed in both installed runtimes and normal/O modes, full same-runtime nonUTC JSON equal. All156 physical-path writer rejections, coherent semantic/evidence faults with all active pins and closed ZIP refreshed, strict binding/bootstrap controls and four actual LOCAL-only native checks completed.',80)
 print(json.dumps({'status':'PASS','semantic_cases':len(faults),'actual_wrapper_suites':8,'path_rejections':156}))
if __name__=='__main__':main()
