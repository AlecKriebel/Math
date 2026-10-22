from pathlib import Path
import shutil,subprocess,json,hashlib,datetime,sys
home=Path(__file__).resolve().parent
pkg=home/'extracted/congestion-fragmentation-verification'
specs=[('probability',pkg/'probability_controls.py','/Users/alec/Documents/Math/.venv/bin/python',pkg/'expected-independent-controls.json','INDEPENDENT_CONTROLS.json'),('flow',pkg/'reviews/flow_adversary_01/independent_flow_controls.py','/Users/alec/Documents/Math/.venv/bin/python',pkg/'reviews/flow_adversary_01/INDEPENDENT_FLOW_CONTROLS.json','INDEPENDENT_FLOW_CONTROLS.json'),('priority',pkg/'reviews/priority_scope_adversary_01/scope_priority_controls.py','/opt/homebrew/bin/python3',pkg/'reviews/priority_scope_adversary_01/SCOPE_PRIORITY_CONTROLS.json','SCOPE_PRIORITY_CONTROLS.json')]
rows=[]
for name,script,python,expected,outname in specs:
 work=home/('optional_'+name); work.mkdir(exist_ok=False); target=work/script.name; shutil.copyfile(script,target)
 r=subprocess.run([python,'-B',str(target)],cwd=work,capture_output=True,timeout=180)
 (work/'stdout.txt').write_bytes(r.stdout); (work/'stderr.txt').write_bytes(r.stderr)
 produced=work/outname
 row={'name':name,'python':python,'exit_code':r.returncode,'source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'produced':produced.exists()}
 if produced.exists():
  row.update(actual_sha256=hashlib.sha256(produced.read_bytes()).hexdigest(),expected_sha256=hashlib.sha256(expected.read_bytes()).hexdigest(),byte_identical=produced.read_bytes()==expected.read_bytes(),json_equal=json.loads(produced.read_bytes())==json.loads(expected.read_bytes()))
 rows.append(row)
 print(json.dumps(row),flush=True)
(home/'OPTIONAL_REPRODUCTION.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows},indent=2)+'\n')
