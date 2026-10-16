from pathlib import Path
import hashlib,json,zipfile,difflib
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent.parent
P=BASE/'publication_package_v2'
O=Path(__file__).resolve().parent
h=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def req(x,msg):
 if not x:raise RuntimeError(msg)
seal=json.loads((P/'PACKAGE_SEAL.json').read_bytes())
allfiles={str(x.relative_to(P)):x for x in P.rglob('*') if x.is_file()}
expected=seal['package_files_excluding_this_seal']
req(set(allfiles)==set(expected)|{'PACKAGE_SEAL.json'},'outer path mismatch')
for n,v in expected.items():req(not (P/n).is_symlink() and h((P/n).read_bytes())==v,'outer hash mismatch '+n)
m=P/'materials';man=json.loads((m/'MANIFEST.json').read_bytes())['files']
req({str(x.relative_to(m)) for x in m.rglob('*') if x.is_file()}==set(man)|{'MANIFEST.json'},'material paths')
for n,v in man.items():req(h((m/n).read_bytes())==v,'material hash '+n)
with zipfile.ZipFile(P/'verification-package.zip') as z:
 names=z.namelist();req(len(names)==len(set(names)),'duplicate zip name')
 req(set(names)==set(man)|{'MANIFEST.json'},'zip paths')
 req(z.testzip() is None,'bad zip CRC')
 for n in names:req(z.read(n)==(m/n).read_bytes(),'zip bytes '+n)
 req(all(not n.startswith('/') and '..' not in Path(n).parts for n in names),'unsafe zip path')
req((P/'original_pedal_flag.tex').read_bytes()==(m/'original_pedal_flag.tex').read_bytes(),'tex duplicate')
req(json.loads((P/'zenodo-deposit.json').read_bytes())['metadata']==json.loads((m/'metadata.json').read_bytes()),'metadata duplicate')
port=json.loads((m/'PORTABILITY_PROVENANCE.json').read_bytes())
for n,v in port.items():
 old=(m/v['original_path']).read_bytes();new=(m/'verification'/n).read_bytes()
 req(h(old)==v['original'] and h(new)==v['portable'],'port hash '+n)
 req(''.join(l for l in old.decode().splitlines(keepends=True) if l not in v['only_removed_lines']).encode()==new,'port diff '+n)
summary={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','outer_files_including_seal':len(allfiles),'outer_pins_excluding_seal':len(expected),'material_pins_excluding_self':len(man),'zip_entries':len(names),'package_seal':h((P/'PACKAGE_SEAL.json').read_bytes()),'pdf':h((P/'original_pedal_flag.pdf').read_bytes()),'tex':h((P/'original_pedal_flag.tex').read_bytes()),'all_paths_and_hashes_exact':True,'zip_crc_and_bytes':True,'metadata_tex_duplicates':True,'portability_differences_exactly_declared':True,'all_files_read':list(sorted(allfiles))}
(O/'PACKAGE_INTEGRITY_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='all_files_read'},indent=2))
