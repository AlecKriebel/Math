from pathlib import Path
import subprocess,json,hashlib,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/shared/math-11000151')
out=Path(__file__).parent
m=json.loads((root/'FINAL_AUTHOR_MANIFEST.json').read_text())
for f in m['files']:
 p=root/f['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
reports=[]
for n in range(1,5):
 b=subprocess.check_output([sys.executable,str(root/f'check_turn_{n}.py')]);assert json.loads(b)==json.loads((root/f'TURN_{n}_CHECKS.json').read_text());reports.append(json.loads(b))
b=subprocess.check_output([sys.executable,str(root/'verify_turn_4_cpp.py')]);assert json.loads(b)==json.loads((root/'TURN_4_CPP_CHECKS.json').read_text())
print(json.dumps({'status':'PASS','author_manifest_sha256':hashlib.sha256((root/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest(),'bound_files':len(m['files']),'python_replays':reports,'cpp_replay':json.loads(b)},indent=2))
