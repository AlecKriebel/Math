from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/shared/math-2302055/research')
m=json.loads((p/'FINAL_AUTHOR_MANIFEST.json').read_text())
for f in m['files']:assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256']
r=[]
for i in range(1,6):
 b=subprocess.check_output([sys.executable,str(p/f'verify_turn{i}.py')]);assert b==(p/f'TURN_{i}_CHECKS.json').read_bytes();r.append(json.loads(b))
print(json.dumps({'status':'PASS','author_manifest_sha256':hashlib.sha256((p/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest(),'bound_files':len(m['files']),'receipts':r},indent=2))
