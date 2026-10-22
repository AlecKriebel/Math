"""Owned-copy audit controls; no sealed-packet mutation. Print stdout outside packet."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys

def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seal(p):
 rows=[{'path':f.name,'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(p.iterdir()) if f.name!='MANIFEST.json' and f.is_file()]
 (p/'MANIFEST.json').write_text(json.dumps({'schema':'whole-preprint-round01-closed/v1','files':rows},indent=2)+'\n');return sha(p/'MANIFEST.json')
def main():
 a=argparse.ArgumentParser()
 for n in ['packet-root','expected-manifest-sha256','expected-checker-sha256','scratch']:a.add_argument('--'+n,required=True)
 a.add_argument('--other-python');args=a.parse_args();P=Path(args.packet_root).absolute();D=Path(args.scratch).absolute();D.mkdir(parents=True,exist_ok=False);rows=[]
 def invoke(name,p,accept,exe=sys.executable,opt=False,mf=None,cp=None,entry=None):
  cmd=[exe,'-I','-B']+(['-O']if opt else[])+[str(entry or p/'verify_packet.py'),'--packet-root',str(p),'--expected-manifest-sha256',mf or args.expected_manifest_sha256,'--expected-checker-sha256',cp or args.expected_checker_sha256,'--replay']
  r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=60);ok=(r.returncode==0)==accept;need(ok,name+': '+r.stdout+r.stderr);rows.append({'name':name,'expected_accept':accept,'returncode':r.returncode,'pass':ok})
 relocated=D/'relocated packet with spaces';shutil.copytree(P,relocated)
 for label,exe in [('primary',sys.executable)]+([('secondary',args.other_python)]if args.other_python else[]):
  for opt in [False,True]:invoke(label+('_optimized'if opt else'_normal'),relocated,True,exe,opt)
 invoke('wrong_manifest_pin',P,False,mf='0'*64);invoke('wrong_checker_pin',P,False,cp='0'*64)
 for name in ['changed_report','extra_file','missing_file','empty_directory','file_symlink','file_hardlink','file_fifo','root_symlink','self_symlink','duplicate_json','nonfinite_json','unsafe_row','duplicate_row','unsupported_firstness_after_reseal']:
  p=D/name;shutil.copytree(P,p);mf=None;entry=None
  if name=='changed_report':(p/'REPORT.md').write_text('changed')
  elif name=='extra_file':(p/'extra').write_text('x')
  elif name=='missing_file':(p/'REPORT.md').unlink()
  elif name=='empty_directory':(p/'empty').mkdir()
  elif name in ['file_symlink','file_hardlink','file_fifo']:
   f=p/'REPORT.md';b=f.read_bytes();f.unlink();donor=D/(name+'_donor');donor.write_bytes(b)
   if name=='file_symlink':f.symlink_to(donor)
   elif name=='file_hardlink':os.link(donor,f)
   else:os.mkfifo(f)
  elif name=='root_symlink':q=D/'root_alias';q.symlink_to(p,target_is_directory=True);p=q
  elif name=='self_symlink':f=p/'verify_packet.py';f.unlink();f.symlink_to(P/'verify_packet.py')
  elif name=='unsupported_firstness_after_reseal':
   f=p/'VERDICT.json';v=json.loads(f.read_text());v['firstness_certified']=True;f.write_text(json.dumps(v));mf=seal(p)
  else:
   f=p/'MANIFEST.json';m=json.loads(f.read_text())
   if name=='duplicate_json':f.write_text('{"schema":"x","schema":"whole-preprint-round01-closed/v1","files":[]}')
   elif name=='nonfinite_json':f.write_text('{"schema":"whole-preprint-round01-closed/v1","files":NaN}')
   elif name=='unsafe_row':m['files'][0]['path']='../escape';f.write_text(json.dumps(m))
   else:m['files'].append(m['files'][0]);f.write_text(json.dumps(m))
   mf=sha(f)
  invoke(name,p,False,mf=mf,entry=entry)
 print(json.dumps({'result':'PASS','positive_controls':sum(r['expected_accept']for r in rows),'negative_controls':sum(not r['expected_accept']for r in rows),'controls':rows,'scope':'Static owned-copy custody and scope controls. Does not test a concurrent hostile filesystem or formally prove the mathematics.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
