from pathlib import Path
import hashlib,json,subprocess,datetime
root=Path(__file__).resolve().parent
checks=[]
for path,expected in json.loads((root/'INPUT_HASHES.json').read_text()).items():
    actual=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    assert actual==expected,(path,actual,expected)
    checks.append({'type':'frozen_input','file':path,'sha256':actual,'pass':True})
for item in json.loads((root/'PRIMARY_RETRIEVAL.json').read_text()):
    if 'sha256' not in item:continue
    path=root/item['file']
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual==item['sha256'],(str(path),actual,item['sha256'])
    checks.append({'type':'private_primary_pin','file':item['file'],'sha256':actual,'pass':True})
for script,receipt in [('check_rare_event_obstruction.py','RARE_EVENT_CONTROL_RECEIPT.json'),('check_inward_funnel.py','INWARD_FUNNEL_CONTROL_RECEIPT.json')]:
    run=subprocess.run(['python3',str(root/'adversary'/script)],capture_output=True,text=True,check=True)
    generated=json.loads(run.stdout)
    saved=json.loads((root/'adversary'/receipt).read_text())
    assert generated['status']=='PASS'
    assert all(saved.get(key)==value for key,value in generated.items())
    checks.append({'type':'independent_adversary_replay','script':script,'pass':True,'receipt_extra_keys':sorted(set(saved)-set(generated))})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'checks':checks},indent=2))
