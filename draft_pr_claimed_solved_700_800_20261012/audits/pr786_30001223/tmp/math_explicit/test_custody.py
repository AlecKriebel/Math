"""Actual normal/O flat-custody and immutable-input controls on owned copies."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,tempfile
def need(x,m):
 if not x:raise ValueError(m)
def main():
 a=argparse.ArgumentParser()
 for n in ('packet','input-root','scratch'):a.add_argument('--'+n,type=Path,required=True)
 a.add_argument('--pin',required=True);a.add_argument('--checker-pin',required=True);x=a.parse_args();cases=[]
 def invoke(packet,inputs,opt,pin=None):
  cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(x.packet/'verify_custody.py'),'--root',str(packet),'--input-root',str(inputs),'--expected-manifest-sha256',pin or x.pin,'--expected-checker-sha256',x.checker_pin]
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=8);return r.returncode,json.loads(r.stdout)
 with tempfile.TemporaryDirectory(dir=x.scratch,prefix='explicit-custody-') as tmp:
  w=Path(tmp);inputs=w/'intake';inputs.mkdir();b=json.loads((x.packet/'INPUTS.json').read_bytes())
  for n in b['files']:
   p=inputs/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((x.input_root/n).read_bytes())
  for opt in (False,True):
   rc,v=invoke(x.packet,x.input_root,opt);need(rc==0 and v['result']=='PASS','baseline');cases.append({'case':'baseline','optimized':opt,'result':'PASS'})
   for case in ('changed_report','missing_report','extra_file','extra_directory','fifo','symlink','directory','checker_change','manifest_rewrite','wrong_pin'):
    packet=w/'packet';shutil.copytree(x.packet,packet);p=packet/'REPORT.md'
    if case=='changed_report':p.write_bytes(p.read_bytes()+b'changed')
    elif case=='missing_report':p.unlink()
    elif case=='extra_file':(packet/'EXTRA.txt').write_text('extra')
    elif case=='extra_directory':(packet/'extra').mkdir()
    elif case=='fifo':p.unlink();os.mkfifo(p)
    elif case=='symlink':p.unlink();p.symlink_to(x.packet/'REPORT.md')
    elif case=='directory':p.unlink();p.mkdir()
    elif case=='checker_change':(packet/'verify_custody.py').write_text('print("untrusted")')
    elif case=='manifest_rewrite':(packet/'MANIFEST.json').write_text('{}')
    rc,v=invoke(packet,inputs,opt,'0'*64 if case=='wrong_pin' else None);need(rc!=0 and v['result']=='FAIL','tamper accepted:'+case);cases.append({'case':case,'optimized':opt,'result':'REJECTED'});shutil.rmtree(packet)
   for n in ('SELECTED_PUBLIC_RECORD.json','ROOT_SOURCE_IDENTITY.json','original/unsolved_math_prioritization/attempts/30001223/author/proof.md'):
    p=inputs/n;saved=p.read_bytes();p.write_bytes(saved+b'changed');rc,v=invoke(x.packet,inputs,opt);need(rc!=0 and v['result']=='FAIL','input mutation');p.write_bytes(saved);cases.append({'case':'input:'+n,'optimized':opt,'result':'REJECTED'})
   p=inputs/'original/extra.txt';p.write_text('extra');rc,v=invoke(x.packet,inputs,opt);need(rc!=0 and v['result']=='FAIL','original extra');p.unlink();cases.append({'case':'original_extra','optimized':opt,'result':'REJECTED'})
 print(json.dumps({'result':'PASS','case_count':len(cases),'cases':cases,'scope':'Actual ordinary/optimized byte-custody tampering; stable output allows final-seal retest without recursive hashing.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
