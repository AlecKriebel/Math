from pathlib import Path
import json,hashlib,subprocess,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/shared/sirsn_9700034')
n=0
for path in p.glob('*MANIFEST.json'):
 for f in json.loads(path.read_text()).get('files',[]):
  if 'path' not in f:continue
  assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256'];n+=1
r=[]
for i in range(1,6):
 b=subprocess.check_output([sys.executable,str(p/f'check_turn_{i}.py')]);assert b==(p/f'TURN_{i}_CHECKS.json').read_bytes();r.append(json.loads(b))
print(json.dumps({'status':'PASS','author_manifest_sha256':hashlib.sha256((p/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest(),'public_bindings':n,'receipts':r},indent=2))
