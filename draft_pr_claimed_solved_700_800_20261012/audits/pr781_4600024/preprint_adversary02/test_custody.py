"""Actual normal/optimized physical custody controls on owned copies; stable receipt."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile

def need(x,m):
 if not x:raise ValueError(m)
def main():
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--input-root',type=Path,required=True);a.add_argument('--scratch',type=Path,required=True);a.add_argument('--pin',required=True);a.add_argument('--checker-pin',required=True);x=a.parse_args();cases=[]
 def invoke(packet,inputs,opt,pin=None):
  cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(x.packet/'verify_custody.py'),'--root',str(packet),'--input-root',str(inputs),'--expected-manifest-sha256',pin or x.pin,'--expected-checker-sha256',x.checker_pin]
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=8);v=json.loads(r.stdout)
  return r.returncode,v
 with tempfile.TemporaryDirectory(dir=x.scratch,prefix='review-custody-') as temp:
  w=Path(temp);inputs=w/'inputs';inputs.mkdir();bindings=json.loads((x.packet/'INPUTS.json').read_bytes())
  for n in bindings['files']:
   p=inputs/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((x.input_root/n).read_bytes())
  for opt in (False,True):
   rc,v=invoke(x.packet,x.input_root,opt);need(rc==0 and v['result']=='PASS','positive baseline');cases.append({'case':'baseline','optimized':opt,'result':'PASS'})
   for case in ('changed_report','missing_report','extra_file','extra_directory','fifo_member','symlink_member','directory_member','changed_checker','rewritten_manifest','wrong_external_pin'):
    packet=w/'packet';shutil.copytree(x.packet,packet);p=packet/'REPORT.md'
    if case=='changed_report':p.write_bytes(p.read_bytes()+b'changed')
    elif case=='missing_report':p.unlink()
    elif case=='extra_file':(packet/'EXTRA.txt').write_text('unexpected')
    elif case=='extra_directory':(packet/'extra').mkdir()
    elif case=='fifo_member':p.unlink();os.mkfifo(p)
    elif case=='symlink_member':p.unlink();p.symlink_to(x.packet/'REPORT.md')
    elif case=='directory_member':p.unlink();p.mkdir()
    elif case=='changed_checker':(packet/'verify_custody.py').write_text('print("untrusted")\n')
    elif case=='rewritten_manifest':(packet/'MANIFEST.json').write_text('{}\n')
    rc,v=invoke(packet,inputs,opt,'0'*64 if case=='wrong_external_pin' else None)
    need(rc!=0 and v['result']=='FAIL','packet tamper accepted: '+case);cases.append({'case':case,'optimized':opt,'result':'REJECTED'});shutil.rmtree(packet)
   for n in ('output/pdf/paper.pdf','source/MANIFEST.json','source/audit/SELECTED_PUBLIC_RECORD.json','source/verify_bundle.py'):
    p=inputs/n;saved=p.read_bytes();p.write_bytes(saved+b'changed');rc,v=invoke(x.packet,inputs,opt);need(rc!=0 and v['result']=='FAIL','input tamper accepted');p.write_bytes(saved);cases.append({'case':'input_changed:'+n,'optimized':opt,'result':'REJECTED'})
   p=inputs/'source/UNEXPECTED.txt';p.write_text('unexpected');rc,v=invoke(x.packet,inputs,opt);need(rc!=0 and v['result']=='FAIL','source extra accepted');p.unlink();cases.append({'case':'source_extra','optimized':opt,'result':'REJECTED'})
 print(json.dumps({'result':'PASS','case_count':len(cases),'cases':cases,'scope':'Actual externally pinned checker, exact packet closure and reviewed-input tamper controls in normal and optimized modes. Output is pin-independent so the final sealed packet can be retested without circular hashing.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
