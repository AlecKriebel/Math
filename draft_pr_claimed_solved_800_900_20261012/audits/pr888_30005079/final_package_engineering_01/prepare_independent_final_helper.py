from pathlib import Path
import datetime,hashlib,json
H=Path(__file__).absolute().parent;A=H.parent
source=A/'publication_tools_01/independent_zip_rebuild.py';raw=source.read_bytes()
manifest=json.loads((A/'publication_tools_01/SAFE_PAYLOAD_MANIFEST.json').read_bytes())
row=next(r for r in manifest['files'] if r['path']==source.name)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert pin(raw)=={k:row[k] for k in ('bytes','sha256')}
before='Independent manual ZIP reconstruction of the private engineering fixture; no final-paper or mathematical clearance.'
after='Independent manual ZIP reconstruction of the final candidate verification archive; auxiliary archive-byte evidence only, no mathematical, priority, whole-package or publication verdict.'
text=raw.decode();assert text.count(before)==1
updated=text.replace(before,after).encode();target=H/'independent_zip_rebuild_final.py'
with target.open('xb') as f:f.write(updated)
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_estimate_percent':60,'scope':'Recorded scope-label-only copy for actual final archive reconstruction; frozen original helper and receipt are unchanged.','original_helper':{'relative_path':'publication_tools_01/independent_zip_rebuild.py',**pin(raw)},'new_helper':{'relative_path':'independent_zip_rebuild_final.py',**pin(updated)},'exact_single_literal_change':{'before':before,'after':after},'behavioral_algorithm_changed':False,'new_receipt_written_in_new_final_engineering_directory':True}
(H/'INDEPENDENT_HELPER_SCOPE_DELTA.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
