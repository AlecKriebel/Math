#!/usr/bin/env python3
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;A=R.parents[1];S=R/'ignored_scratch';S.mkdir(exist_ok=True)
os.environ['TMPDIR']=str(S/'tmp');os.environ['PYTHONDONTWRITEBYTECODE']='1'
import copy,datetime,hashlib,json,shutil,stat,subprocess,zipfile,importlib.util
ENV=dict(os.environ);ENV.pop('PYTHONOPTIMIZE',None)
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def cp(s,d):d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,d)
def invoke(p,flags=(),args=()):
 r=subprocess.run([sys.executable,'-B',*flags,str(p),*args],cwd=S,env=ENV,text=True,capture_output=True,timeout=240)
 return {'flags':list(flags),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def load(p):
 sp=importlib.util.spec_from_file_location('r3_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m

def archive():
 p=A/'publication';b=json.loads((p/'BUILD_RECEIPT.json').read_text());anchors=b['verification_anchors'];zpath=p/b['verification_zip']['path'];dest=S/'archive';dest.mkdir(exist_ok=True)
 with zipfile.ZipFile(zpath) as z:
  names=z.namelist();need(len(names)==199 and len(set(names))==199,'ZIP count/duplicate');need(len(set(n.casefold()for n in names))==199,'ZIP case collision')
  for i in z.infolist():
   pp=Path(i.filename);need(not pp.is_absolute() and '..'not in pp.parts and '\\'not in i.filename and str(pp)==i.filename,'ZIP path');need(not stat.S_ISLNK(i.external_attr>>16),'ZIP symlink')
   q=dest/i.filename;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(z.read(i))
  need(z.testzip()is None,'ZIP CRC');need(all(z.read(n)==(p/'verification'/n).read_bytes()for n in names),'actual ZIP/staging bytes')
 args=[x for k,v in anchors.items()for x in['--expected-'+k+'-sha256',v]]
 results=[invoke(dest/'verify.py',f,args)for f in [[],['-O'],['-OO']]]
 need(all(x['returncode']==0 for x in results),'actual extracted verifier')
 controls=[]
 # Corrupt real extracted bytes, then also repair outer manifest: frozen nested seal must defeat it.
 target=dest/'reviews/source_question_family/SOURCE_ONLY_RECONSTRUCTION.md';old=target.read_bytes();manifest=dest/'MANIFEST.json';oldm=manifest.read_bytes();target.write_bytes(old+b'\nR3 FAULT\n')
 bad=invoke(dest/'verify.py',[],args);need(bad['returncode']!=0,'real payload fault accepted');controls.append({'case':'real_member_bytes','returncode':bad['returncode'],'error':bad['stderr'][-900:]})
 obj=json.loads(oldm)
 for e in obj['files']:
  if e['path']==target.relative_to(dest).as_posix():e['bytes']=target.stat().st_size;e['sha256']=sha(target)
 save(manifest,obj);reanchored=list(args);reanchored[1]=sha(manifest);bad=invoke(dest/'verify.py',['-OO'],reanchored);need(bad['returncode']!=0,'coupled outer payload fault accepted');controls.append({'case':'real_payload_outer_manifest_reanchored','returncode':bad['returncode'],'error':bad['stderr'][-900:]})
 target.write_bytes(old);manifest.write_bytes(oldm)
 v=load(dest/'verify.py');paths=[]
 for raw in ['../escape','/absolute','a//b','a/./b','a/../b','a\\b','']:
  try:v.safe(raw)
  except ValueError:paths.append(raw)
  else:raise RuntimeError('unsafe accepted '+raw)
 link=dest/'probe_link';link.symlink_to(dest/'verify.py')
 try:
  try:v.member(dest,'probe_link')
  except ValueError:paths.append('symlink')
  else:raise RuntimeError('symlink accepted')
 finally:link.unlink()
 # Outside three anchors each independently incorrect.
 for j,k in enumerate(['manifest','context','snapshot']):
  badargs=list(args);badargs[2*j+1]='0'*64;r=invoke(dest/'verify.py',[],badargs);need(r['returncode']!=0,'outside anchor not used');controls.append({'case':'outside_'+k,'returncode':r['returncode']})
 save(R/'ARCHIVE_CHECKS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'zip_sha256':sha(zpath),'zip_bytes':zpath.stat().st_size,'members':len(names),'three_outside_anchors':anchors,'normal_O_OO':results,'real_corruption_controls':controls,'path_rejections':paths,'nested_registry_count':len(json.loads((A/'CURRENT_PR1268_CONTEXT.json').read_text())['authored_freezes'])})
 return dest

def original():
 snap=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());out=[]
 for e in snap['files']:
  data=(A/'submitted'/Path(e['path']).name).read_bytes();cur=(A/'current_edition'/Path(e['path']).name).read_bytes();need(data==cur,'historical preservation');blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();need(blob==e['blob'],'blob pin')
  r=subprocess.run(['git','show',snap['head']+':'+e['path']],cwd='/Users/alec/Documents/Math',capture_output=True);need(r.returncode==0 and r.stdout==data,'exact Git snapshot');out.append({'path':e['path'],'blob':blob,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 save(R/'ORIGINAL_GIT_CHECKS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_original_and_preserved_current':out,'read_only_git':True})

def workers():
 p=S/'deployed/program/audits/pr1268_10900050/publication'
 for n in ['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py','zenodo-deposit.json']:cp(A/'publication'/n,p/n)
 c=p.parents[2]/'publication_coordinators'
 for n in ['pr1268.py','verify_pr1268_merge.py']:cp(A.parents[1]/'publication_coordinators'/n,c/n)
 results=[invoke(p/'workflow_regression.py',f,['--worker'])for f in [[],['-O'],['-OO']]]
 need(all(x['returncode']==0 for x in results),'deployed workflow regression')
 save(R/'CURRENT_WORKFLOW_REPLAY.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_path':str(A/'publication/workflow_regression.py'),'copied_exact':True,'runs':results,'scope':'Actual deployed bodies copied; existing synthetic regression rerun. Not an independently designed test or actual service/Git integration.'})
 return p
if __name__=='__main__':
 archive();original();workers();print(json.dumps({'archive':'PASS','original10current10_git':'PASS','deployed_workflow_3modes':'PASS'}))
