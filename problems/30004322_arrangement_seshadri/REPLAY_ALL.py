from pathlib import Path
import subprocess,sys,json,hashlib
p=Path(__file__).resolve().parent
entries=0; total=0; sourcecount=0
for i in range(1,6):
 out=subprocess.check_output([sys.executable,str(p/f'check_turn_{i}.py')],cwd=p)
 assert out==(p/f'TURN_{i}_CHECKS.json').read_bytes(),i
 total+=json.loads(out)['assertions']
for name in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json']:
 for e in json.loads((p/name).read_text())['files']:
  b=(p/e['path']).read_bytes(); assert hashlib.sha256(b).hexdigest()==e['sha256']; assert len(b)==e['bytes'];entries+=1
if (p/'sources').is_dir():
 for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_FINAL.json']:
  for e in json.loads((p/name).read_text())['files']:
   b=(p/e['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==e['sha256'];sourcecount+=1
print(json.dumps({'assertions':total,'manifest_entries':entries,'source_files_checked':sourcecount,'all_receipts_byte_exact':True},sort_keys=True))
