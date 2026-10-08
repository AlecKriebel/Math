"""Reproduce hostile-input and nonroot/read-only controls on a pinned bundle."""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('bundle',type=pathlib.Path)
parser.add_argument('--manifest-sha256',required=True)
args=parser.parse_args()
bundle=args.bundle.resolve()

def run(args,expected=0,cwd=None):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
 if p.returncode != expected: raise RuntimeError((args,p.returncode,p.stdout,p.stderr))
 return p.stdout

pin=args.manifest_sha256
run([sys.executable,'-B',str(bundle/'verify.py'),str(bundle),'--manifest-sha256',pin])
normal=run([sys.executable,'-B',str(bundle/'audit.py')])
opt=run([sys.executable,'-O','-B',str(bundle/'audit.py')])
if normal!=opt:raise RuntimeError('optimized mismatch')
controls=[]
for data in ['{"p":0,"q":1}','{"p":6,"q":2}','{"p":1,"q":0}','{"p":1,"q":-2}',
 '{"p":true,"q":1}','{"p":1.0,"q":1}','{"p":"1","q":1}',
 '{"p":1,"q":1,"solved":true}','{"p":1,"p":2,"q":1}','{"p":NaN,"q":1}',
 '[1,1]','{"p":100001,"q":1}','{"p":1}', '{']:
 for mode in [[],['-O']]:
  run([sys.executable,*mode,'-B',str(bundle/'audit.py'),'--slope-json',data],2)
 controls.append(data)

verifier=bundle/'verify.py'
for mode in [[],['-O']]:run([sys.executable,*mode,'-B',str(verifier),str(bundle),'--manifest-sha256',pin])
mutations=[]
with tempfile.TemporaryDirectory(prefix='su2-controls-') as td:
 td=pathlib.Path(td)
 for case in ['modified_file','missing_file','extra_file','symlink_file','wrong_pin','malformed_manifest','duplicate_key','traversal','wrong_bytes','duplicate_entry','manifest_symlink']:
  root=td/case;shutil.copytree(bundle,root);usepin=pin
  if case=='modified_file':(root/'REPORT.md').write_text((root/'REPORT.md').read_text()+'\nchange\n')
  if case=='missing_file':(root/'README.md').unlink()
  if case=='extra_file':(root/'EXTRA.txt').write_text('unexpected')
  if case=='symlink_file':
   (root/'README.md').unlink();(root/'README.md').symlink_to(bundle/'README.md')
  if case=='wrong_pin':usepin='0'*64
  if case=='malformed_manifest':(root/'MANIFEST.json').write_text('{')
  if case=='duplicate_key':(root/'MANIFEST.json').write_text('{"format":"su2-surgery-audit-v1","format":"su2-surgery-audit-v1","files":[]}')
  if case in ['traversal','wrong_bytes','duplicate_entry']:
   d=json.loads((root/'MANIFEST.json').read_text())
   if case=='traversal':d['files'][0]['name']='../REPORT.md'
   if case=='wrong_bytes':d['files'][0]['bytes']=True
   if case=='duplicate_entry':d['files'].append(d['files'][0])
   (root/'MANIFEST.json').write_text(json.dumps(d))
  if case in ['malformed_manifest','duplicate_key','traversal','wrong_bytes','duplicate_entry']:
   usepin=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()
  if case=='manifest_symlink':
   (root/'MANIFEST.json').unlink();(root/'MANIFEST.json').symlink_to(bundle/'MANIFEST.json')
  for mode in [[],['-O']]:run([sys.executable,*mode,'-B',str(verifier),str(root),'--manifest-sha256',usepin],2)
  mutations.append(case)
 readonly=td/'readonly';shutil.copytree(bundle,readonly)
 for p in readonly.iterdir():p.chmod(0o444)
 readonly.chmod(0o555)
 try:
  if os.geteuid()==0:raise RuntimeError('nonroot test requires nonroot execution')
  for mode in [[],['-O']]:
   run([sys.executable,*mode,'-B',str(readonly/'audit.py')],cwd=readonly)
   run([sys.executable,*mode,'-B',str(readonly/'verify.py'),'.','--manifest-sha256',pin],cwd=readonly)
 finally:
  readonly.chmod(0o755)
  for p in readonly.iterdir():p.chmod(0o644)
result={'status':'passed','normal_optimized_outputs_identical':True,'math_result':json.loads(normal),
 'slope_hostile_cases':len(controls),'slope_hostile_modes':['normal','optimized'],
 'integrity_hostile_cases':mutations,'integrity_hostile_modes':['normal','optimized'],
 'read_only_nonroot':{'uid':os.geteuid(),'directory_mode':'0555','file_mode':'0444','modes':['normal','optimized'],'passed':True},
 'security_scope':'hash/schema/path controls on fixed artifact bundle; no external theorem verification; not a race-safe hostile-filesystem sandbox',
 'control_note':'Malformed-schema controls use intentionally recomputed test pins to reach parser branches; tamper controls keep the original trusted pin.'}
print(json.dumps(result,indent=2))
