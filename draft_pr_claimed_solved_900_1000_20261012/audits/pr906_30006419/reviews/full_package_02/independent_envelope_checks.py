#!/usr/bin/env python3
"""Read-only closed-archive authentication and disposable independent negative controls."""
from pathlib import Path, PurePosixPath
import hashlib,importlib.util,json,os,shutil,socket,stat,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
AUDIT=BASE.parent.parent
PUB=AUDIT/'publication'
EXTRACT=BASE/'tmp/extracted'
PIN='e96eb05184d4e3e468bebd09bd828eef341867a7ff709346b4375c58faed557b'
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(x,msg):
 if not x: raise RuntimeError(msg)
def invoke(p,anchor=PIN,mode=(),pdf=None):
 cmd=[sys.executable,'-I','-B',*mode,str(p/'verify_package.py'),'--integrity-only','--expected-manifest',anchor]
 if pdf: cmd+=['--pdf',str(pdf)]
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
 return subprocess.run(cmd,cwd='/tmp',env=env,text=True,capture_output=True,timeout=15)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','cases':[]}
with zipfile.ZipFile(PUB/'harmonic-sphere-source-verification-v1.0.zip') as z:
 infos=z.infolist(); names=[x.filename for x in infos]
 require(len(names)==117 and len(set(names))==117,'archive membership/duplicates')
 require(z.testzip() is None,'CRC mismatch')
 m=json.loads(z.read('PACKAGE_MANIFEST.json'))
 require(sha(z.read('PACKAGE_MANIFEST.json'))==PIN,'external anchor')
 require(set(names)==set(m['files'])|{'PACKAGE_MANIFEST.json'},'ZIP closed inventory')
 for item in infos:
  p=PurePosixPath(item.filename);mode=item.external_attr>>16
  require(not p.is_absolute() and p.as_posix()==item.filename and '..' not in p.parts and '\\' not in item.filename,'ZIP unsafe path')
  require(stat.S_ISREG(mode),'ZIP nonregular mode')
  b=z.read(item)
  require((EXTRACT/item.filename).read_bytes()==b,'extract different')
  if item.filename!='PACKAGE_MANIFEST.json':
   r=m['files'][item.filename];require(len(b)==r['bytes'] and sha(b)==r['sha256'],'member mismatch')
 require(z.read('note.pdf')==(PUB/'output/pdf/note.pdf').read_bytes(),'separate PDF differs')
 require(z.read('note.tex')==(PUB/'note.tex').read_bytes(),'separate TeX differs')
 receipt['archive']={'members':len(infos),'payload_files':len(m['files']),'all_regular':True,'crc_and_hashes':True,'pdf_equal':True,'tex_equal':True}
original=AUDIT/'original/unsolved_math_prioritization/attempts/30006419'
originals=list(original.rglob('*')); originals=[p for p in originals if p.is_file()]
require(len(originals)==30,'original file count')
for p in originals:require(p.read_bytes()==(EXTRACT/'original_packet'/p.relative_to(original)).read_bytes(),'original bytes differ')
receipt['original_30_unchanged']=True
with tempfile.TemporaryDirectory(prefix='p906i-',dir='/tmp') as td:
 temp=Path(td)
 for mode in [(),('-O',),('-OO',)]:
  label=' '.join(mode) or 'normal'
  for name in ['pristine','bytes bool','pr bool','negative bytes','invalid digest','unsafe path','extra empty directory','missing verifier','listed FIFO','unlisted socket','listed symlink','resign note external old pin','resign original proof new pin','wrong separate PDF','changed ordinary payload internal no anchor']:
   root=temp/'package';shutil.copytree(EXTRACT,root);anchor=PIN;pdf=None;sock=None
   manifest=root/'PACKAGE_MANIFEST.json';v=json.loads(manifest.read_text());rewrite=False
   if name=='bytes bool': v['files']['README.md']['bytes']=True;rewrite=True
   elif name=='pr bool':v['pr']=True;rewrite=True
   elif name=='negative bytes':v['files']['README.md']['bytes']=-1;rewrite=True
   elif name=='invalid digest':v['files']['README.md']['sha256']='X'*64;rewrite=True
   elif name=='unsafe path':v['files']['../outside']={'bytes':1,'sha256':'0'*64};rewrite=True
   elif name=='extra empty directory':(root/'empty').mkdir()
   elif name=='missing verifier':(root/'verify_package.py').unlink()
   elif name=='listed FIFO':(root/'README.md').unlink();os.mkfifo(root/'README.md')
   elif name=='unlisted socket':sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);sock.bind(str(root/'socket'))
   elif name=='listed symlink':(root/'README.md').unlink();(root/'README.md').symlink_to(EXTRACT/'README.md')
   elif name=='wrong separate PDF':pdf=temp/'other.pdf';pdf.write_bytes(b'%PDF fake')
   elif name in ['resign note external old pin','resign original proof new pin','changed ordinary payload internal no anchor']:
    q={'resign note external old pin':'note.tex','resign original proof new pin':'original_packet/author/PROOF.md','changed ordinary payload internal no anchor':'README.md'}[name]
    p=root/q;p.write_bytes(p.read_bytes()+b'\nChanged content.\n');v['files'][q]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())};rewrite=True
   if rewrite:
    manifest.write_text(json.dumps(v,indent=2)+'\n')
    if name!='resign note external old pin':anchor=sha(manifest.read_bytes())
   if name=='changed ordinary payload internal no anchor':
    # Explicit trust-boundary positive: a newly supplied valid replacement anchor
    # can authenticate ordinary replacement payloads, and does not certify math.
    command=[sys.executable,'-I','-B',*mode,str(root/'verify_package.py'),'--integrity-only']
    p=subprocess.run(command,cwd='/tmp',capture_output=True,text=True,timeout=15)
    require(p.returncode==0 and json.loads(p.stdout)['external_anchor_checked'] is False,'self-consistency boundary')
    receipt['cases'].append({'mode':label,'case':name,'accepted_as_self_consistent_only':True})
   else:
    p=invoke(root,anchor,mode,pdf)
    good=p.returncode==0 if name=='pristine' else p.returncode!=0
    require(good,'unexpected envelope case '+label+' '+name)
    receipt['cases'].append({'mode':label,'case':name,'accepted':p.returncode==0,'guard':p.stderr.strip().splitlines()[-1] if p.stderr else None})
   if sock:sock.close()
   shutil.rmtree(root)
# Independent comparator edge probes in the runtime executing this harness.
spec=importlib.util.spec_from_file_location('v',EXTRACT/'verify_package.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
receipt['comparator']=[]
for x,y,ok in [(True,1.0,False),(1,True,False),(False,0,False),(float('nan'),0.0,False),(float('inf'),0.0,False),(1.0000000001,1.0,True),(1.01,1.0,False),(1,1.0,True)]:
 try:module.equivalent(x,y);accepted=True
 except RuntimeError:accepted=False
 require(accepted==ok,'comparator edge')
 receipt['comparator'].append({'actual':str(x),'expected':str(y),'accepted':accepted})
(BASE/'ENVELOPE_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['cases','comparator']},indent=2))
