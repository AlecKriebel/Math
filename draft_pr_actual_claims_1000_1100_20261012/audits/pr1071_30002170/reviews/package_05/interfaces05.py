import sys,os,json,hashlib,zipfile,copy,shutil
from pathlib import Path
sys.dont_write_bytecode=True
from run05 import R,P,S,A,PYTHONS,run,sha,put
C=S/'MixedPackage05'
if C.exists():
 for p in C.rglob('*'):
  if p.is_file() and not p.is_symlink():
   if p.read_bytes()!=(P/p.relative_to(C)).read_bytes():raise RuntimeError('Interrupted clean extraction differs')
else:
 C.mkdir();zipfile.ZipFile(P/'PR1071_preprint_v1_0_support.zip').extractall(C)
alias=C.with_name(C.name.swapcase())
if not alias.samefile(C):raise RuntimeError('Physical case alias unavailable')
sentinel=S/'sentinel05';sentinel.write_bytes(b'OWNED REVIEW05 SENTINEL\n');sentinelhash=sha(sentinel)
hard=S/'hard05'
if not hard.exists():os.link(sentinel,hard)
linked=S/'linked05'
if not linked.is_symlink():linked.symlink_to(sentinel)
dangling=S/'dangling05'
if not dangling.is_symlink():dangling.symlink_to(S/'absent05')
directory=S/'existing05';directory.mkdir(exist_ok=True)
parent=S/'syparent05'
if not parent.is_symlink():parent.symlink_to(S,target_is_directory=True)
cases={'existing-file':sentinel,'existing-dir':directory,'hardlink':hard,'symlink':linked,'dangling':dangling,'symlink-parent':parent/'never05','inside':C/'never05','case-alias':alias/'never05','missing-inside':C/'absent/never05','missing-case-alias':alias/'absent/never05','parent-traversal':S/'absent/../never05','missing-outside':S/'missing05/never05'}
def reject(label,argv,reason=None):
 p=run(label,argv,cwd=S,expected=1)
 if reason is not None and reason.encode()not in p.stderr:raise RuntimeError('Wrong rejection '+label)
 return p
for tag,py in PYTHONS.items():
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  prefix=tag+'-'+mode;base=[py,'-B',*flags]
  run(prefix+'-all-math-adversaries',base+[R/'guard05.py',prefix],cwd=R)
  run(prefix+'-clean-verify',base+[C/'scripts/verify_package.py'],cwd=S)
  archive=S/(prefix+'-clean-retry.zip')
  run(prefix+'-clean-archive',base+[C/'scripts/build_archive.py','--out',archive],cwd=S)
  if sha(archive)!=sha(P/'PR1071_preprint_v1_0_support.zip'):raise RuntimeError('Clean rebuild differs')
  with (R/'OWNED_STREAMING_CLEANUP.jsonl').open('a') as f:f.write(json.dumps({'path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'mode':archive.stat().st_mode&511,'exact_identity_to_canonical_archive':True,'remove_only_this_own_new_unsealed_duplicate':True})+'\n')
  archive.unlink()
  for script in ['check.py','build_pdf.py','build_archive.py']:
   for label,path in cases.items():reject(prefix+'-'+script+'-'+label,base+[C/'scripts'/script,'--out',path])
   # Reverse physical spelling: wrapper's own ROOT comes from the case alias.
   reject(prefix+'-'+script+'-reverse-case',base+[alias/'scripts'/script,'--out',C/'reverse-never05'],'outside all frozen package descendants')
  reject(prefix+'-required-absent',base+[C/'scripts/verify_package.py','--require-bindings'],'Required bindings are absent')
  run(prefix+'-clean-strict',base+[C/'scripts/verify_package.py','--require-bindings','--bindings',P/'UPLOAD_BINDINGS.json','--archive',P/'PR1071_preprint_v1_0_support.zip'],cwd=S)
  bad=S/(prefix+'-bad-binding.json');b=json.loads((P/'UPLOAD_BINDINGS.json').read_text());b['pdf']['sha256']='0'*64;bad.write_text(json.dumps(b))
  reject(prefix+'-corrupt-binding',base+[C/'scripts/verify_package.py','--bindings',bad,'--archive',P/'PR1071_preprint_v1_0_support.zip'],'Upload PDF binding mismatch')
  reject(prefix+'-missing-archive',base+[C/'scripts/verify_package.py','--bindings',P/'UPLOAD_BINDINGS.json','--archive',S/'absent-archive05'],'Present bindings require')
  if sha(sentinel)!=sentinelhash:raise RuntimeError('Sentinel changed')
# Coherent semantic corruptions rehash the active allowlist member. These are
# actual unmodified verifier CLI calls on our extraction, not stale-hash tests.
manifest=C/'PACKAGE_MANIFEST.json';manbytes=manifest.read_bytes()
semantic=[]
for filename,mutations in [
 ('HISTORY_ORDER_REPAIR_STATUS.json',{'publication_ready':True,'issues_resolved':True,'published':True,'services_held_after_pr':1071,'fresh_whole_package_reviews_completed':5,'minimum_fresh_reviews_required':1,'new_complete_whole_review_completed':True,'root_terminal_adoption_required':False,'root_repair_adoption_required':False,'latest_complete_review_findings':{'P0':0,'P1':0,'P2':0,'P3':0}}),
 ('HISTORY_ORDER_QUALIFICATION.json',{'additional1558_global_order_preserved':True,'additional1558_exact_row_multiset_preserved':False,'mismatched_global_additional_positions':0,'before_projected_rows_sha256':'0'*64}),
 ('PORTABILITY_SOURCE_EVIDENCE.json',{'finding':'wrong'}),
 ('CASE_ALIAS_SOURCE_EVIDENCE.json',{'root_status':'wrong'})]:
 target=C/filename;original=target.read_bytes();d=json.loads(original)
 for key,value in mutations.items():
  bad=copy.deepcopy(d);bad[key]=value;target.write_text(json.dumps(bad));m=json.loads(manbytes)
  for row in m['members']:
   if row['path']==filename:row['bytes']=target.stat().st_size;row['sha256']=sha(target)
  manifest.write_text(json.dumps(m))
  for tag,py in PYTHONS.items():
   for mode,flags in [('normal',[]),('optimized',['-O'])]:
    label='coherent-'+filename+'-'+key+'-'+tag+'-'+mode
    p=reject(label,[py,'-B',*flags,C/'scripts/verify_package.py'])
    if b'Member mismatch:'in p.stderr:raise RuntimeError('Stale-hash-only rejection')
  semantic.append({'file':filename,'field':key,'all_four_modes_rejected_after_member_rehash':True})
  target.write_bytes(original);manifest.write_bytes(manbytes)
# Bootstrap guard must run before JSON parsing, even for the self-excluded manifest.
for relative in ['PACKAGE_MANIFEST.json','paper.tex']:
 target=C/relative;old=target.read_bytes();target.unlink();target.symlink_to(sentinel)
 for tag,py in PYTHONS.items():
  for mode,flags in [('normal',[]),('optimized',['-O'])]:reject('bootstrap-'+relative+'-'+tag+'-'+mode,[py,'-B',*flags,C/'scripts/verify_package.py'],'Symlink member/ancestor')
 target.unlink();target.write_bytes(old)
custody=C/'custody';hidden=C/'owned-custody-backup05';custody.rename(hidden);custody.symlink_to(hidden,target_is_directory=True)
for tag,py in PYTHONS.items():
 for mode,flags in [('normal',[]),('optimized',['-O'])]:reject('ancestor-bootstrap-'+tag+'-'+mode,[py,'-B',*flags,C/'scripts/verify_package.py'],'Symlink member/ancestor')
custody.unlink();hidden.rename(custody)
run('clean-final-verify',[PYTHONS['py314'],'-B',C/'scripts/verify_package.py'],cwd=S)
put('INTERFACE_CONTROLS.json',{'status':'PASS','clean_extraction':str(C),'unmodified_original_wrappers_and_ROOT':True,'sentinel_sha256':sentinelhash,'sentinel_unchanged':sha(sentinel)==sentinelhash,'path_cases_per_writer_runtime_mode':len(cases)+1,'writers':3,'runtime_modes':4,'coherent_semantic_cases':semantic,'bootstrap_manifest_member_ancestor_guards':True})
