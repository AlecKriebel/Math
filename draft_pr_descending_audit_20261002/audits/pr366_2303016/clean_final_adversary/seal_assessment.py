from pathlib import Path
import datetime,json,hashlib
R=Path(__file__).resolve().parent
names=['INDEPENDENT_BASELINE_SEAL.json','ORIGINAL_MATHEMATICAL_ASSESSMENT.md','FROZEN_PACKET_RECEIPT.json','ADVERSARIAL_CONTROLS.json','audit_frozen_packet.py','adversarial_controls.py']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'original mathematical assessment sealed before reading sibling/root analytical findings','original_head':'f4039c9c093b10e651ee7fd2e6379073b84238c7','verdict':'PASS direct credited proof; limited sharpness; no novelty','files':{n:{'bytes':(R/n).stat().st_size,'sha256':hashlib.sha256((R/n).read_bytes()).hexdigest()} for n in names}}
(R/'ORIGINAL_ASSESSMENT_SEAL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
