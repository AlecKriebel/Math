#!/usr/bin/env python3
"""Independent guard and trust-boundary challenges; no package mutation."""
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'tmp/extracted'
PIN='c30902d2269b62a3c37bfe4caf9ae0b4abcc50599a39e9996ab7eab1eb4ffde3'
receipts=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def resign(r):
 p=r/'PACKAGE_MANIFEST.json';d=json.loads(p.read_text())
 for n in d['files']:
  f=r/n
  if f.is_file() and not f.is_symlink():d['files'][n]={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}
 p.write_text(json.dumps(d,indent=2)+'\n');return sha(p.read_bytes())
def edit(r,name):
 f=r/name;f.write_bytes(f.read_bytes()+b'\n')
def drop(r,name): (r/name).unlink()
def symlink(r,name):
 f=r/name;f.unlink();f.symlink_to('README.md' if '/' not in name else ROOT/'tmp/extracted/README.md')
def fifo(r,name):
 f=r/name;f.unlink();os.mkfifo(f)
def invalid_path(r):
 p=r/'PACKAGE_MANIFEST.json';d=json.loads(p.read_text());d['files']['../outside']={'bytes':0,'sha256':sha(b'')};p.write_text(json.dumps(d))
cases=[('note bytes',lambda r:edit(r,'note.tex'),False),('missing payload',lambda r:drop(r,'note.pdf'),False),('extra file',lambda r:(r/'extra.txt').write_text('extra'),False),('extra empty directory',lambda r:(r/'empty').mkdir(),False),('file symlink',lambda r:symlink(r,'note.tex'),False),('FIFO payload',lambda r:fifo(r,'note.tex'),False),('directory symlink',lambda r:(r/'linked').symlink_to(ROOT,target_is_directory=True),False),('manifest symlink',lambda r:symlink(r,'PACKAGE_MANIFEST.json'),False),('changed manifest',lambda r:edit(r,'PACKAGE_MANIFEST.json'),False),('resigned changed note trusted pin',lambda r:(edit(r,'note.tex'),resign(r)),False),('resigned changed original proof new outer pin',lambda r:(edit(r,'original_packet/author/PROOF.md'),resign(r)),True),('resigned unsafe path new outer pin',invalid_path,True),('resigned wrong scope new outer pin',lambda r:wrong_scope(r),True)]
def wrong_scope(r):
 p=r/'PACKAGE_MANIFEST.json';d=json.loads(p.read_text());d['problem_id']='30006420';p.write_text(json.dumps(d))
for optimization in ['', '-O']:
 for name,mutate,use_new_anchor in cases:
  with tempfile.TemporaryDirectory(dir=ROOT/'tmp',prefix='guard-') as td:
   r=Path(td)/'packet';shutil.copytree(PACKAGE,r);mutate(r)
   anchor=sha((r/'PACKAGE_MANIFEST.json').read_bytes()) if use_new_anchor else PIN
   args=[sys.executable,'-I','-B']+([optimization] if optimization else [])+[str(r/'verify_package.py'),'--integrity-only','--expected-manifest',anchor]
   out=subprocess.run(args,capture_output=True,text=True,timeout=20)
   rejected=out.returncode!=0
   if not rejected:raise RuntimeError('Unexpected acceptance: '+name)
   receipts.append({'mode':optimization or 'normal','case':name,'rejected':rejected,'returncode':out.returncode,'reason':out.stderr.strip().splitlines()[-1]})
 # Importing the unchanged authentic module tests the comparator directly.
 spec=importlib.util.spec_from_file_location('trusted',PACKAGE/'verify_package.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 for name,actual,expected in [('bool as float',True,1.0),('float as bool',1.0,True),('NaN',float('nan'),0.0),('infinity',float('inf'),0.0),('extra dict key',{'a':1,'b':2},{'a':1}),('wrong exact int type',1.0,1)]:
  try:module.equivalent(actual,expected)
  except RuntimeError as e:receipts.append({'mode':'normal direct import; repeated during '+(optimization or 'normal')+' CLI suite','case':name,'rejected':True,'reason':str(e),'actual_python_optimization':sys.flags.optimize})
  else:raise RuntimeError('Comparator accepted '+name)
# Deliberately caller-resigned arbitrary authored note: a new supplied anchor does authenticate that new envelope,
# which is not the genuine freeze. Fixed original pins constrain original material, not all new authored content.
with tempfile.TemporaryDirectory(dir=ROOT/'tmp',prefix='trust-') as td:
 r=Path(td)/'packet';shutil.copytree(PACKAGE,r);edit(r,'note.tex');new_pin=resign(r)
 out=subprocess.run([sys.executable,'-I','-B',str(r/'verify_package.py'),'--integrity-only','--expected-manifest',new_pin],capture_output=True,text=True,timeout=20)
 if out.returncode:raise RuntimeError(out.stderr)
 trust={'caller_resigned_new_authored_note_with_new_anchor_accepted':True,'genuine_freeze_rejects_it':True,'interpretation':'Expected external trust boundary; a replacement caller-supplied anchor is not the genuine frozen anchor.'}
result={'status':'PASS','guard_rejections':len(receipts),'receipts':receipts,'trust_boundary':trust,'outer_modes':['normal','-O'],'math_scope':'Integrity/comparator guards, not analytic theorem certification.'}
(ROOT/'guard_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','guard_rejections':len(receipts),'trust_boundary':trust},indent=2))
