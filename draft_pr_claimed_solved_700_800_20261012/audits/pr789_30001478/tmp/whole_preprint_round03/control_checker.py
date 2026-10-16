"""Own-checker rejection controls on owned copies; output is outside the copied packet."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(v,m):
 if not v:raise ValueError(m)
def seal(p):
 mf=json.loads((p/'MANIFEST.json').read_text())
 mf['files']=[{'path':q.relative_to(p).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q)}for q in sorted(p.rglob('*'))if q.is_file()and q.name!='MANIFEST.json']
 (p/'MANIFEST.json').write_text(json.dumps(mf,indent=2)+'\n');return sha(p/'MANIFEST.json')
def main():
 ap=argparse.ArgumentParser()
 for n in ('packet-root','expected-manifest-sha256','expected-checker-sha256','source-root','release-root','primary-root','scratch','output'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();packet=Path(a.packet_root).absolute();source=Path(a.source_root).absolute();release=Path(a.release_root).absolute();primary=Path(a.primary_root).absolute();scratch=Path(a.scratch).absolute();scratch.mkdir(parents=True,exist_ok=False)
 need(sha(packet/'MANIFEST.json')==a.expected_manifest_sha256 and sha(packet/'verify_review.py')==a.expected_checker_sha256,'bootstrap pins')
 results=[]
 def invoke(label,p=packet,s=source,r=release,bank=None,mf=None,cp=None,opt=False,positive=False):
  cmd=[sys.executable,'-I','-B']+(['-O']if opt else[])+[str(p/'verify_review.py'),'--packet-root',str(p),'--expected-manifest-sha256',mf or a.expected_manifest_sha256,'--expected-checker-sha256',cp or a.expected_checker_sha256,'--source-root',str(s),'--release-root',str(r),'--replay']
  if bank is not None:cmd+=['--primary-root',str(bank)]
  proc=subprocess.run(cmd,capture_output=True,text=True,cwd='/',timeout=30)
  observed=proc.returncode==0
  need(observed==positive,label+' unexpected: '+proc.stdout+proc.stderr)
  out=json.loads(proc.stdout);need(out['result']==('PASS'if positive else'FAIL'),label+' result')
  results.append({'name':label,'expected':'PASS'if positive else'REJECT','returncode':proc.returncode,'result':out})
 for opt in (False,True):
  invoke('baseline_'+str(opt),opt=opt,positive=True)
  invoke('primary_'+str(opt),bank=primary,opt=opt,positive=True)
 for name in ('wrong_manifest','wrong_checker','extra','missing','edit','empty','symlink','hardlink','fifo','root_alias','self_alias','duplicate_key','traversal','promote_priority','false_counts','wrong_math'):
  base=scratch/name;base.mkdir();p=base/'packet with spaces';shutil.copytree(packet,p);kw={}
  q=p/'REPORT.md'
  if name=='wrong_manifest':kw['mf']='0'*64
  elif name=='wrong_checker':kw['cp']='0'*64
  elif name=='extra':(p/'EXTRA').write_text('extra')
  elif name=='missing':q.unlink()
  elif name=='edit':q.write_text('edit')
  elif name=='empty':(p/'empty').mkdir()
  elif name in ('symlink','hardlink','fifo'):
   donor=base/'donor';shutil.copyfile(q,donor);q.unlink()
   if name=='symlink':q.symlink_to(donor)
   elif name=='hardlink':os.link(donor,q)
   else:os.mkfifo(q)
  elif name=='root_alias':
   alias=base/'root-link';alias.symlink_to(p,target_is_directory=True);p=alias
  elif name=='self_alias':
   q=p/'verify_review.py';donor=base/'checker.py';q.rename(donor);q.symlink_to(donor)
  elif name=='duplicate_key':
   q=p/'MANIFEST.json';q.write_text(q.read_text().replace('{','{"schema":"duplicate",',1));kw['mf']=sha(q)
  elif name=='traversal':
   q=p/'MANIFEST.json';d=json.loads(q.read_text());d['files'][0]['path']='../escape';q.write_text(json.dumps(d));kw['mf']=sha(q)
  elif name in ('promote_priority','false_counts'):
   q=p/'VERDICT.json';d=json.loads(q.read_text())
   if name=='promote_priority':d['firstness_certified']=True
   else:d['severity_counts']['high']=1
   q.write_text(json.dumps(d));kw['mf']=seal(p)
  else:
   q=p/'MATH_RESULTS.json';d=json.loads(q.read_text());d['result']='FALSE';q.write_text(json.dumps(d));kw['mf']=seal(p)
  invoke(name,p=p,**kw)
 # Every input mutation uses copied inputs, never frozen inputs.
 for name in ('changed_source','source_ancestor_alias','changed_release','changed_primary'):
  base=scratch/name;base.mkdir();kw={}
  if name in ('changed_source','source_ancestor_alias'):
   s=base/'source';shutil.copytree(source,s)
   if name=='changed_source':(s/'LICENSE.txt').write_text('changed')
   else:
    alias=base/'link';alias.symlink_to(base,target_is_directory=True);s=alias/'source'
   kw['s']=s
  elif name=='changed_release':
   r=base/'release';r.mkdir()
   for row in json.loads((packet/'INPUT_VERIFICATION.json').read_text())['release_files']:
    dest=r/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(release/row['path'],dest)
   (r/'output/pdf/paper.pdf').write_bytes(b'%PDF-changed');kw['r']=r
  else:
   bank=base/'primary';shutil.copytree(primary,bank);(bank/'owr.pdf').write_bytes(b'%PDF-changed');kw['bank']=bank
  invoke(name,**kw)
 summary={'result':'PASS','positive_controls':4,'negative_controls':20,'controls':results,'scope':'Static custody/scope/replay controls on disposable copies; no candidate, source, or frozen report mutations.'}
 Path(a.output).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'result':'PASS','positive_controls':4,'negative_controls':20}))
if __name__=='__main__':main()
