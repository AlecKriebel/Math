"""Own complete package audit. All writes confined to this review folder."""
from pathlib import Path
import subprocess,json,hashlib,sys,zipfile,io,stat,zlib,ast,os,shutil,datetime
OWN=Path(__file__).resolve().parent;AUDIT=OWN.parents[1];CAND=AUDIT/'preprint_v1_0';REPO=AUDIT.parents[2]
SCRATCH=OWN/'scratch';SCRATCH.mkdir(exist_ok=True)
records=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,s):
 if not v:raise ValueError(s)
def save(n,o):(OWN/n).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def cmd(args,ok=True):
 r=subprocess.run([str(a) for a in args],capture_output=True,cwd=OWN)
 row={'argv':[str(a) for a in args],'returncode':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)}
 if len(r.stdout)<3000:row['stdout']=r.stdout.decode(errors='replace')
 if r.returncode and len(r.stderr)<2000:row['stderr']=r.stderr.decode(errors='replace')
 records.append(row)
 need((r.returncode==0)==ok,'command outcome: '+str(args)+' '+r.stderr.decode(errors='replace'))
 return r
# Independently authenticate every prior custody decision and exact original.
freeze=json.loads((CAND/'INPUT_FREEZE.json').read_text());select=json.loads((CAND/'CUSTODY_SELECTION.json').read_text())
entries=freeze['entries'];choices=select['entries'];need(len(entries)==168 and len(choices)==168,'baseline count')
need({r['path'] for r in entries}=={r['path'] for r in choices},'partition coverage')
by={r['path']:r for r in entries};details=[]
for r in choices:
 source=AUDIT/r['path'];need(rec(source)=={'bytes':r['bytes'],'sha256':r['sha256']},'unchanged prior bytes')
 need(all(r[k]==by[r['path']][k] for k in ('bytes','sha256')),'choice identity')
 if r['disposition']=='EXACT_AUTHORED_COPY':
  need((CAND/r['destination']).read_bytes()==source.read_bytes(),'history exact copy');need('/sources/' not in r['path'] and not r['path'].endswith('.py'),'third-party or executable included')
 else:need(r['disposition']=='OMITTED' and r['reason'],'explicit exclusion reason')
 details.append({'path':r['path'],'disposition':r['disposition'],'bytes_equal':True,'copy_equal':r['disposition']=='EXACT_AUTHORED_COPY','exclusion_reason':r.get('reason')})
git=[]
for p in sorted((AUDIT/'submitted').iterdir()):
 gitpath='unsolved_math_prioritization/attempts/3000018/'+p.name
 r=cmd(['git','show','f37a3ff66595fcf75bb18bf859be8594c3662242:'+gitpath])
 need(r.stdout==p.read_bytes(),'actual git submitted equality');git.append({'path':gitpath,**rec(p)})
need(len(git)==9,'original files')
save('CUSTODY_REVIEW.json',{'prior_choices':details,'actual_git':git,'prior_count':168,'copies':sum(r['disposition']=='EXACT_AUTHORED_COPY' for r in choices),'exclusions':sum(r['disposition']=='OMITTED' for r in choices)})
# Independent closed archive/header/payload reconstruction with no candidate imports.
manifest=json.loads((CAND/'MANIFEST.json').read_text());payload={r['path']:(CAND/r['path']).read_bytes() for r in manifest['entries']}
for r in manifest['entries']:need(rec(CAND/r['path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'manifest bytes')
payload['MANIFEST.json']=(CAND/'MANIFEST.json').read_bytes();names=sorted(payload)
need(len(names)==102 and len(set(names))==102,'closed archive names')
need('paper.pdf' not in names and 'ARTIFACT_BINDINGS.json' in names,'external required PDF design')
raw=(CAND/'pr1098_support_v1_0.zip').read_bytes();headers=[]
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 need(z.namelist()==names and not z.comment and z.testzip() is None,'zip names CRC')
 for i in z.infolist():
  b=z.read(i.filename);need(b==payload[i.filename],'exact payload')
  need(i.compress_type==0 and i.date_time==(2026,10,16,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16),'exact ZIP header')
  need(i.CRC==zlib.crc32(b) and i.file_size==len(b) and i.compress_size==len(b) and not i.extra and not i.comment,'CRC and no variable fields')
  headers.append({'name':i.filename,'CRC':i.CRC,'bytes':len(b),'header_offset':i.header_offset})
buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as z:
 for n in names:
  i=zipfile.ZipInfo(n,(2026,10,16,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,payload[n])
need(buffer.getvalue()==raw,'independent closed ZIP equality')
bind=json.loads((CAND/'ARTIFACT_BINDINGS.json').read_text());need(bind=={'paper.pdf':rec(CAND/'paper.pdf')},'required exact PDF binding')
deposit=json.loads((CAND/'DEPOSIT_BINDING.json').read_text())
for n,r in deposit['artifacts'].items():need(rec(CAND/n)==r,'outer deposit binding')
need(deposit['metadata_sha256']==rec(CAND/'metadata.json')['sha256'],'metadata outer pin')
save('CLOSED_ARCHIVE_REVIEW.json',{'independent_closed_reconstruction_equal':True,'archive':rec(CAND/'pr1098_support_v1_0.zip'),'headers':headers,'external_PDF':rec(CAND/'paper.pdf'),'no_hash_cycle':True})
# Exact native metadata agreement, parse expected constant without executing it.
metadata=json.loads((CAND/'metadata.json').read_text());api=json.loads((CAND/'zenodo-api.json').read_text());native=json.loads((CAND/'publication/zenodo-deposit.json').read_text())
module=ast.parse((CAND/'code/metadata_constants.py').read_text());constant=ast.literal_eval(module.body[1].value)
need(metadata==api['metadata']==native['metadata']==constant,'metadata equality')
need(set(api)=={'metadata'} and set(native)=={'metadata','files'},'native schemas')
need(native['files']==[{'path':'../paper.pdf','name':'paper.pdf'},{'path':'../pr1098_support_v1_0.zip','name':'pr1098_support_v1_0.zip'}],'native upload selections')
need(metadata['license']=='cc-by-4.0' and metadata['creators'][0]['orcid']=='0009-0001-9320-500X','rights author')
cmd([sys.executable,'-B',REPO/'zenodo_deposit_tool/zenodo.py','check',CAND/'publication/zenodo-deposit.json'])
# One extraction in own compact scratch; original candidate unchanged.
kit=SCRATCH/'kit';kit.mkdir(exist_ok=True)
with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(kit)
for n in ('paper.pdf','pr1098_support_v1_0.zip'):shutil.copyfile(CAND/n,kit/n)
protected={str(p.relative_to(kit)):rec(p) for p in kit.rglob('*') if p.is_file()}
outputs=[]
for optimized in (False,True):
 base=[sys.executable]+(['-O'] if optimized else [])+['-B']
 cmd(base+[kit/'code/verify_kit.py'])
 r=cmd(base+[kit/'code/run_checks.py']);obj=json.loads(r.stdout);save('CANDIDATE_CONTROLS_'+('OPTIMIZED' if optimized else 'NORMAL')+'.json',obj);outputs.append(r.stdout)
 need(obj==json.loads((CAND/('validation/NEW_CONTROLS_'+('optimized' if optimized else 'normal')+'.json')).read_text()),'current full validation JSON')
 cmd(base+[kit/'code/run_checks.py','--invalid'],False)
 own=cmd(base+[OWN/'independent_checks.py']);save('INDEPENDENT_'+('OPTIMIZED' if optimized else 'NORMAL')+'.json',json.loads(own.stdout));cmd(base+[OWN/'independent_checks.py','--invalid'],False)
need(outputs[0]==outputs[1],'normal optimized complete equality')
# Canonical writers hard-code actual audit protection; our output scope is inside it.
# Keep that protection intact. For positive writer/ancestor tests only, set the runtime
# ORIGINAL constant to a disposable sibling root. No candidate bytes are edited.
original=SCRATCH/'original';original.mkdir(exist_ok=True)
def writer(base,name,flag,target,ok=False):
 harness="import sys,runpy;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import common;common.ORIGINAL=Path(sys.argv[2]);script=sys.argv[3];sys.argv=[script,*sys.argv[4:]];runpy.run_path(script,run_name='__main__')"
 return cmd(base+['-c',harness,str(kit/'code'),str(original),str(kit/'code'/name),flag,str(target)],ok)
writer_tests=[]
# Real positive archive and PDF script logic in both modes, canonical payload unchanged.
for optimized in (False,True):
 base=[sys.executable]+(['-O'] if optimized else [])+['-B']
 dest=SCRATCH/('rebuilt-'+str(optimized)+'.zip');writer(base,'rebuild_archive.py','--output',dest,True)
 need(dest.read_bytes()==raw,'writer exact ZIP')
 build=SCRATCH/('build-'+str(optimized));r=writer(base,'build_pdf.py','--out-dir',build,True)
 need((build/'paper.pdf').read_bytes()==(CAND/'paper.pdf').read_bytes(),'real PDF canonical equality')
 save('ACTUAL_PDF_'+('OPTIMIZED' if optimized else 'NORMAL')+'.json',{'result':json.loads(r.stdout),'canonical_exact':True,'log':(build/'paper.log').read_text(errors='replace'),'compiler':subprocess.check_output(['tectonic','--version'],text=True).strip(),'harness_scope':'unmodified script and payload; runtime ORIGINAL redirected to own disposable root for work-directory-only scope'})
 # Reject output paths before any compiler invocation: use own marker executable.
 bindir=SCRATCH/'fakebin';bindir.mkdir(exist_ok=True);fake=bindir/'tectonic';marker=SCRATCH/'compiler-must-not-run';fake.write_text('#!/bin/sh\n: > "'+str(marker)+'"\nexit 77\n');fake.chmod(0o700)
 oldpath=os.environ['PATH'];os.environ['PATH']=str(bindir)+os.pathsep+oldpath
 existing=SCRATCH/'existing';existing.write_bytes(b'keep');link=SCRATCH/'leaflink'
 if not link.is_symlink():link.symlink_to(existing)
 broken=SCRATCH/'broken'
 if not broken.is_symlink():broken.symlink_to(SCRATCH/'absent')
 ancestor=SCRATCH/'ancestor'
 if not ancestor.is_symlink():ancestor.symlink_to(kit,target_is_directory=True)
 hard=SCRATCH/'hardleaf'
 if not hard.exists():os.link(existing,hard)
 cases=[('existingfile',existing),('existingdirectory',build),('symlinkleaf',link),('brokensymlinkleaf',broken),('symlinkancestor',ancestor/'new'),('hardlinkleaf',hard),('raw-parent',str(SCRATCH/'kit')+'/../traversal'),('relative','relative-created'),('missingparent',SCRATCH/'missing'/'new'),('kitroot',kit/'forbidden'),('originalroot',original/'forbidden'),('PDFleaf',kit/'paper.pdf'),('PDFchild',kit/'paper.pdf'/'new')]
 for protectedroot in (kit,original):
  case=Path(str(protectedroot).upper())
  if case.exists() and os.path.samefile(case,protectedroot):cases.append(('physical-case-alias-'+protectedroot.name,case/'forbidden'))
 for name,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
  for label,target in cases:
   writer(base,name,flag,target)
   need(not marker.exists(),'compiler called on rejected destination')
   if label not in ('existingfile','existingdirectory','symlinkleaf','brokensymlinkleaf','hardlinkleaf','PDFleaf'):need(not Path(target).exists(),'rejected destination created')
   writer_tests.append({'optimized':optimized,'writer':name,'fault':label,'rejected_before_compiler':True})
 # Missing original parent too; explicit lexical/missing-parent guard rejection.
 original.rmdir()
 for name,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
  writer(base,name,flag,original/'new');need(not original.exists(),'missing original recreated');writer_tests.append({'optimized':optimized,'writer':name,'fault':'absent-original-root-parent','rejected_before_compiler':True})
 original.mkdir();hard.unlink()
 # Independent input faults: good fresh output, no output aliases masking them.
 for inputname in ['MANIFEST.json','paper.tex','ARTIFACT_BINDINGS.json']:
  p=kit/inputname;tmp=SCRATCH/('save-'+p.name);p.rename(tmp)
  for fault in ('symlink','hardlink','duplicateJSON' if p.suffix=='.json' else 'hardlink'):
   if fault=='symlink':p.symlink_to(tmp)
   elif fault=='hardlink':os.link(tmp,p)
   else:p.write_bytes(b'{"a":1,"a":2}')
   for name,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
    target=SCRATCH/('reject-'+name);writer(base,name,flag,target);need(not target.exists() and not marker.exists(),'input fault side effect');writer_tests.append({'optimized':optimized,'writer':name,'fault':inputname+'-'+fault,'rejected_before_compiler':True})
   cmd(base+[kit/'code/verify_kit.py'],False);p.unlink()
  tmp.rename(p)
 for inputname in ['ARTIFACT_BINDINGS.json','paper.pdf']:
  p=kit/inputname;tmp=SCRATCH/('save-'+p.name);p.rename(tmp);cmd(base+[kit/'code/verify_kit.py'],False);tmp.rename(p)
 for inputname in ['metadata.json','zenodo-api.json','publication/zenodo-deposit.json']:
  p=kit/inputname;old=p.read_bytes();obj=json.loads(old)
  if inputname=='metadata.json':obj['title']='damaged'
  else:obj['metadata']['title']='damaged'
  p.write_text(json.dumps(obj));cmd(base+[kit/'code/verify_kit.py'],False);p.write_bytes(old)
 os.environ['PATH']=oldpath
 cmd(base+[kit/'code/verify_kit.py'])
need(protected=={str(p.relative_to(kit)):rec(p) for p in kit.rglob('*') if p.is_file()},'extraction unchanged after tests')
save('ACTUAL_REPRODUCTION.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','commands':records,'command_count':len(records),'writer_tests':writer_tests,'writer_test_count':len(writer_tests),'complete_candidate_JSON_equal':True,'untouched_candidate_bytes':True,'actual_clean_readers':True,'writer_scope_note':'Review work is restricted inside protected actual audit. Positive archive/PDF and guard subprocesses execute exact unchanged scripts with ONLY runtime ORIGINAL redirected to a disposable own root. Actual canonical ROOT protection is retained. No output request targets actual canonical protected tree. This is explicitly distinct from unmodified documented external writer invocation.'})
print(json.dumps({'status':'PASS','commands':len(records),'writer_tests':len(writer_tests),'scratch_bytes':sum(p.stat().st_size for p in SCRATCH.rglob('*') if p.is_file())}))
