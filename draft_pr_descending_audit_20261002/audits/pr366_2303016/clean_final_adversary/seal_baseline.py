from pathlib import Path
import hashlib,json,datetime
root=Path(__file__).resolve().parent
names=['PRIMARY_SOURCE_RECEIPTS.json','source_receipt.py','INDEPENDENT_MATH_BASELINE.md']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'independent source and mathematical mechanism sealed before author proof/code/history or sibling/root analytical findings','files':{n:{'size':(root/n).stat().st_size,'sha256':hashlib.sha256((root/n).read_bytes()).hexdigest()} for n in names}}
(root/'INDEPENDENT_BASELINE_SEAL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
