"""Reviewer-owned negative controls, entirely on disposable copies."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).absolute().parent;T=R.parent;S=T/'preprint/source';W=T/'whole_preprint_round03_scratch/package-controls'
PIN='50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de'
PY='/opt/homebrew/bin/python3'
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd):return subprocess.run([PY,'-I','-B']+cmd,cwd='/',text=True,capture_output=True,timeout=30)
def main():
 W.mkdir(parents=True,exist_ok=False);rows=[]
 def case(name,prepare,build=False):
  base=W/name;base.mkdir();source=base/'source';shutil.copytree(S,source)
  pdf=base/'input.pdf';shutil.copyfile(T/'preprint/output/pdf/paper.pdf',pdf)
  target=base/'output';pin=PIN;source,pdf,target,pin=prepare(base,source,pdf,target,pin)
  cmd=([str(source/'build_package.py'),'--source',str(source),'--expected-manifest-sha256',pin,'--pdf',str(pdf),'--output-dir',str(target)]
       if build else [str(source/'verify_source.py'),'--expected-manifest-sha256',pin,'--pdf',str(pdf)])
  before=pdf.read_bytes();p=run(cmd)
  need(p.returncode!=0,'accepted '+name)
  need(pdf.read_bytes()==before,'input PDF changed '+name)
  rows.append({'name':name,'expected':'REJECT','returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'input_pdf_unchanged':True})
 def mutate(kind):
  def f(base,s,p,o,pin):
   q=s/'LICENSE.txt'
   if kind=='extra':(s/'unexpected').write_text('extra')
   elif kind=='empty':(s/'empty').mkdir()
   elif kind=='missing':q.unlink()
   elif kind=='edit':q.write_text('edit')
   elif kind=='symlink':q.unlink();q.symlink_to(S/'LICENSE.txt')
   elif kind=='fifo':q.unlink();os.mkfifo(q)
   elif kind=='wrongpin':pin='0'*64
   elif kind=='badpdf':p.write_bytes(b'%PDF-invalid')
   elif kind=='rootlink':
    link=base/'source-link';link.symlink_to(s,target_is_directory=True);s=link
   elif kind in ('duplicatekey','traversal','boolsize'):
    mf=s/'MANIFEST.json';v=json.loads(mf.read_text())
    if kind=='duplicatekey':raw=mf.read_text().replace('{','{"schema":"duplicate",',1)
    else:
     if kind=='traversal':v['files'][0]['path']='../escape'
     else:v['files'][0]['bytes']=True
     raw=json.dumps(v)
    mf.write_text(raw);pin=sha(mf)
   return s,p,o,pin
  return f
 for name in ('extra','empty','missing','edit','symlink','fifo','wrongpin','badpdf','rootlink','duplicatekey','traversal','boolsize'):case('verify_'+name,mutate(name))
 def build_mutate(kind):
  def f(base,s,p,o,pin):
   if kind=='inside_source':o=s/'release'
   elif kind=='output_ancestor_symlink':
    real=base/'real';real.mkdir();link=base/'link';link.symlink_to(real,target_is_directory=True);o=link/'out'
   elif kind=='output_file_symlink':
    o.mkdir();(o/'main.tex').symlink_to(s/'main.tex')
   elif kind=='output_file_hardlink':
    o.mkdir();donor=base/'donor';donor.write_bytes(b'keep');os.link(donor,o/'main.tex')
   elif kind=='output_pdf_is_input':
    (o/'output/pdf').mkdir(parents=True);dest=o/'output/pdf/paper.pdf';p.rename(dest);p=dest
   elif kind=='output_aliases_source':
    o.mkdir();os.link(s/'main.tex',o/'main.tex')
   elif kind=='output_fifo':
    o.mkdir();os.mkfifo(o/'main.tex')
   return s,p,o,pin
  return f
 for name in ('inside_source','output_ancestor_symlink','output_file_symlink','output_file_hardlink','output_pdf_is_input','output_aliases_source','output_fifo'):case('build_'+name,build_mutate(name),True)
 out={'result':'PASS','negative_control_count':len(rows),'controls':rows,'limits':'Static malformed-path and alias tests, not a race-free filesystem sandbox.'}
 (R/'PACKAGE_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'result':'PASS','negative_control_count':len(rows)}))
if __name__=='__main__':main()
