#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,stat,datetime,shutil
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]
PKG=OUT/'frozen/preprint_v1_0'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,row):assert p.is_file() and not p.is_symlink() and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],str(p)
def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2)+'\n')
allpins={r['path']:r for r in json.loads((OUT/'INPUT_PINS.json').read_text())['files']}
protected=json.loads((PKG/'INPUT_PINS.json').read_text())['files']
for r in protected:
 # Byte identity is assessed against the pre-inspection live audit and its pinned evidence copy.
 check(BASE/r['path'],r)
 assert allpins[r['path']]['sha256']==r['sha256']
outputs=json.loads((PKG/'OUTPUT_PINS.json').read_text())['files']
for r in outputs:check(PKG/r['path'],r)
copies=json.loads((PKG/'EVIDENCE_COPY_MAP.json').read_text())['copies']
for r in copies:
 check(PKG/r['package_path'],r);check(BASE/r['source_audit_relative'],r)
 assert allpins[r['source_audit_relative']]['sha256']==r['sha256']
orig=json.loads((OUT/'frozen/root_records/ROOT_MATH_ACCEPTANCE.json').read_text())['original_files']
for r in orig:
 check(OUT/'frozen'/r['snapshot_path'],r)
 check(PKG/'evidence'/r['snapshot_path'],r)
 assert allpins[r['snapshot_path']]['sha256']==r['sha256']
 # exact earlier frozen Git-object copies as byte evidence, without running Git.
 gp=BASE/'reviews/package_01/frozen/git_objects'/Path(r['snapshot_path']).name
 check(gp,r)
allow=json.loads((PKG/'ALLOWLIST.json').read_text())['members'];manifest=json.loads((PKG/'MANIFEST.json').read_text())
assert allow==sorted(set(allow))
assert len(allow)==142 and manifest['members']==allow+['MANIFEST.json']
assert [r['path'] for r in manifest['entries']]==allow
for r in manifest['entries']:check(PKG/r['path'],r)
archive=PKG/'pr1047_supportkit_v1.0.zip'
ziprows=[]
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert z.namelist()==sorted(allow+['MANIFEST.json'])
 assert len(z.infolist())==143
 for i in z.infolist():
  p=PurePosixPath(i.filename)
  assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
  assert stat.S_ISREG(i.external_attr>>16)
  assert i.date_time==(2026,10,14,0,0,0) and i.compress_type==zipfile.ZIP_STORED
  data=z.read(i);assert data==(PKG/i.filename).read_bytes()
  ziprows.append({'path':i.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc':i.CRC})
 extracted=OUT/'clean_extraction';extracted.mkdir(exist_ok=False);z.extractall(extracted)
assert not any(p.endswith('.pdf') or '/raw/' in p or p.startswith('tmp/') or p.endswith('.png') or p.endswith('.zip') or p=='zenodo-deposit.json' for p in allow)
meta=json.loads((PKG/'zenodo_metadata.json').read_text());assert set(meta)=={'metadata'}
m=meta['metadata'];assert m==json.loads((PKG/'.zenodo.json').read_text())==json.loads((PKG/'zenodo-deposit.json').read_text())['metadata']
assert [r['path'] for r in json.loads((PKG/'zenodo-deposit.json').read_text())['files']]==['paper/matroid_rank_obstruction.pdf','pr1047_supportkit_v1.0.zip']
assert m['creators']==[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X','affiliation':'Independent researcher'}]
assert m['version']=='1.0' and m['license']=='cc-by-4.0' and m['publication_date']=='2026-10-14'
# Read every authored text member into deterministic inspection receipts; content review is separately recorded.
readrows=[]
for name in allow:
 data=(PKG/name).read_bytes();text=data.decode('utf-8');readrows.append({'path':name,'bytes':len(data),'lines':len(text.splitlines()),'sha256':hashlib.sha256(data).hexdigest()})
save('PACKAGE_BYTE_CHECKS.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','frozen_input_inventory':len(allpins),'protected_inputs':len(protected),'preparation_outputs':len(outputs),'copies':len(copies),'exact_originals':len(orig),'prior_frozen_git_object_byte_copies':len(orig),'git_reexecuted':False,'manifest_content_entries':len(allow),'zip_members':len(ziprows),'all_crc_payloads_modes_timestamps_pass':True,'metadata_normalized_equal':True,'archive_sha256':digest(archive),'tex_sha256':digest(PKG/'paper/matroid_rank_obstruction.tex'),'pdf_sha256':digest(PKG/'paper/matroid_rank_obstruction.pdf')})
save('ZIP_MEMBERS.json',ziprows);save('TEXT_MEMBER_READ_RECEIPTS.json',readrows)
print(json.dumps(json.loads((OUT/'PACKAGE_BYTE_CHECKS.json').read_text()),indent=2))
