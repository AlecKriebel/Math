"""Disposable reviewer checker controls; never modifies sealed inputs. Output/scratch must be outside all sealed inputs."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,subprocess,shutil,os,sys
ap=argparse.ArgumentParser()
for name in ['packet','source','package','scratch','output','expected-manifest-sha256','expected-checker-sha256']:ap.add_argument('--'+name,required=True)
a=ap.parse_args();W=Path(a.packet).absolute();S=Path(a.source).absolute();P=Path(a.package).absolute();D=Path(a.scratch).absolute();O=Path(a.output).absolute()
for protected in [W,S,P]:
 if D==protected or protected in D.parents or O==protected or protected in O.parents:raise ValueError('controls must write outside every sealed input')
D.mkdir(exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def seal(p):
 rows=[dict(path=x.relative_to(p).as_posix(),bytes=x.stat().st_size,sha256=sha(x.read_bytes()))for x in sorted(p.rglob('*'))if x.is_file()and x.name!='MANIFEST.json']
 b=(json.dumps({'schema':'pr789-whole-preprint-round04/v1','files':rows},indent=2)+'\n').encode();(p/'MANIFEST.json').write_bytes(b);return sha(b)
mf=a.expected_manifest_sha256;cp=a.expected_checker_sha256;results=[]
def run(name,root=W,expected=True,source=S,package=P,pin=mf,checkerpin=cp,opt=False,replay=False,entry=None):
 cmd=[sys.executable,'-I','-B']+(['-O']if opt else[])+[str(entry or root/'verify_review.py'),'--packet',str(root),'--source',str(source),'--package',str(package),'--expected-manifest-sha256',pin,'--expected-checker-sha256',checkerpin]+(['--replay']if replay else[])
 p=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=60);ok=p.returncode==0
 if ok!=expected:raise ValueError(name+' unexpected '+p.stdout+p.stderr)
 results.append({'name':name,'expected':'PASS'if expected else'REJECT','returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr})
run('normal',replay=True);run('optimized',opt=True,replay=True)
for name in ['wrong_manifest_pin','wrong_checker_pin','changed_report','extra_file','empty_directory','missing_report','report_symlink','report_hardlink','report_fifo','self_symlink','root_symlink','ancestor_symlink','duplicate_JSON_key','nonfinite_JSON','unsafe_path','duplicate_row','rehashed_firstness','rehashed_head','rehashed_result','rehashed_high_severity','source_extra','source_tamper','source_ancestor_symlink','wrong_bound_PDF']:
 root=D/name;shutil.copytree(W,root);pin=mf;checkerpin=cp;source=S;package=P;entry=None
 if name=='wrong_manifest_pin':pin='0'*64
 elif name=='wrong_checker_pin':checkerpin='0'*64
 elif name=='changed_report':(root/'REPORT.md').write_text('changed')
 elif name=='extra_file':(root/'EXTRA').write_text('extra')
 elif name=='empty_directory':(root/'empty').mkdir()
 elif name=='missing_report':(root/'REPORT.md').unlink()
 elif name.startswith('report_'):
  f=root/'REPORT.md';f.unlink();donor=D/(name+'_donor');donor.write_text('donor')
  if name=='report_symlink':f.symlink_to(donor)
  elif name=='report_hardlink':os.link(donor,f)
  else:os.mkfifo(f)
 elif name=='self_symlink':f=root/'verify_review.py';f.unlink();f.symlink_to(W/'verify_review.py')
 elif name in ['root_symlink','ancestor_symlink']:
  alias=D/(name+'_alias');alias.symlink_to(root if name=='root_symlink'else D,target_is_directory=True);root=alias if name=='root_symlink'else alias/name
 elif name in ['duplicate_JSON_key','nonfinite_JSON','unsafe_path','duplicate_row']:
  p=root/'MANIFEST.json';m=json.loads(p.read_bytes())
  if name=='duplicate_JSON_key':b=b'{"schema":"x","schema":"y","files":[]}'
  elif name=='nonfinite_JSON':b=b'{"schema":"pr789-whole-preprint-round04/v1","files":NaN}'
  else:
   if name=='unsafe_path':m['files'][0]['path']='../escape'
   else:m['files'].append(m['files'][0])
   b=json.dumps(m).encode()
  p.write_bytes(b);pin=sha(b)
 elif name in ['rehashed_firstness','rehashed_head','rehashed_result','rehashed_high_severity']:
  p=root/'VERDICT.json';m=json.loads(p.read_bytes())
  if name=='rehashed_firstness':m['firstness_certified']=True
  elif name=='rehashed_head':m['reviewed_head']='0'*40
  elif name=='rehashed_result':m['result']='FAIL'
  else:m['severity_counts']['high']=1
  p.write_text(json.dumps(m));pin=seal(root)
 elif name.startswith('source_'):
  source=D/(name+'_source');shutil.copytree(S,source)
  if name=='source_extra':(source/'EXTRA').write_text('x')
  elif name=='source_tamper':(source/'main.tex').write_text('changed')
  else:alias=D/'source_ancestor_alias';alias.symlink_to(D,target_is_directory=True);source=alias/source.name
 elif name=='wrong_bound_PDF':
  package=D/'bad_package';shutil.copytree(P/'output',package/'output');shutil.copyfile(P/'main.tex',package/'main.tex');(package/'output/pdf/paper.pdf').write_bytes(b'%PDF-altered')
 run(name,root=root,expected=False,source=source,package=package,pin=pin,checkerpin=checkerpin,entry=entry)
result={'result':'PASS','utc':datetime.now(timezone.utc).isoformat(),'positive_controls':2,'negative_controls':len(results)-2,'controls':results,'expensive_candidate_core_repeated':False}
O.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'result':'PASS','positive':2,'negative':len(results)-2}))
