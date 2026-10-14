#!/usr/bin/env python3
"""Copy only pinned, authored evidence into the local review package."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
records=[]
previous=json.loads((ROOT/'EVIDENCE_COPY_MANIFEST.json').read_text())
previous_records={(r['source_path'],r['package_path']):r for r in previous['files']}
def copy(source, target, group):
    src=AUDIT/source; dst=ROOT/target
    dst.parent.mkdir(parents=True,exist_ok=True)
    data=src.read_bytes();dst.write_bytes(data)
    rec=dict(source_path=source,package_path=target,group=group,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),copy_policy='byte-identical authored record; private attachments excluded')
    old=previous_records.get((source,target))
    if old is not None:
        if any(old[k]!=rec[k] for k in ['source_path','package_path','group','bytes','sha256']):raise RuntimeError('Existing copied record identity changed: '+source)
        rec=old
    records.append(rec)
pins=json.loads((AUDIT/'SUBMITTED_PINS.json').read_text())
for rec in pins['files']:
    src=rec['snapshot_path'];data=(AUDIT/src).read_bytes()
    if hashlib.sha256(data).hexdigest()!=rec['sha256'] or len(data)!=rec['bytes']:raise RuntimeError('original snapshot mismatch: '+src)
    copy(src,'evidence/original/'+src,'frozen_original_11')
for filename in ['SUBMITTED_PINS.json','ROOT_MATH_AUDIT.md','ROOT_MATH_ACCEPTANCE.json','ROOT_PRIORITY_ADOPTION.json']:
    copy(filename,'evidence/root/'+filename,'root_acceptance_snapshot')
for family in ['game_certificate_01','flow_source_01','priority_01']:
    base=AUDIT/'reviews'/family
    pins=json.loads((base/'OUTPUT_PINS.json').read_text())
    entries=pins.get('files',pins.get('entries',[]))
    for rec in entries:
        name=rec.get('path',rec.get('file'))
        src=base/name;data=src.read_bytes()
        if hashlib.sha256(data).hexdigest()!=rec['sha256'] or len(data)!=rec['bytes']:raise RuntimeError('fresh frozen output mismatch: '+str(src))
    # Enumerate approved authored files, not a broad directory copy. API discovery
    # response dumps are excluded along with every private source body/image/text.
    names=[p.name for p in base.iterdir() if p.is_file() and p.suffix in {'.md','.json','.py'}]
    names += [str(p.relative_to(base)) for p in (base/'sources').glob('*.json') if p.name in {'CATALOGUE.json','RETRIEVALS.json'}]
    if (base/'sources/.gitignore').exists():names+=['sources/.gitignore']
    for name in sorted(set(names)):
        if name=='CITATION_DISCOVERY.json':continue
        source='reviews/'+family+'/'+name
        copy(source,'evidence/'+source,'fresh_'+family)
base=AUDIT/'reviews/package_01'
pins=json.loads((base/'OUTPUT_PINS.json').read_text())
for rec in pins['files']:
    data=(base/rec['path']).read_bytes()
    if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:raise RuntimeError('frozen package_01 output mismatch: '+rec['path'])
for name in sorted([rec['path'] for rec in pins['files']]+['OUTPUT_PINS.json']):
    if '/' in name or name.lower()=='fullsource.txt':raise RuntimeError('unexpected terminal review member')
    copy('reviews/package_01/'+name,'evidence/reviews/package_01/'+name,'frozen_package_01')
copy('ROOT_PREPRINT_REVIEW_01.json','evidence/root/ROOT_PREPRINT_REVIEW_01.json','root_release_wording_snapshot')
base=AUDIT/'reviews/package_02'
pins=json.loads((base/'OUTPUT_PINS.json').read_text())
if len(pins['files'])!=64:raise RuntimeError('whole02 sealed output count')
for rec in pins['files']:
    data=(base/rec['path']).read_bytes()
    if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:raise RuntimeError('frozen whole02 mismatch')
for name in sorted([rec['path'] for rec in pins['files']]+['OUTPUT_PINS.json']):
    if '/' in name or name.lower()=='fullsource.txt':raise RuntimeError('unexpected terminal whole02 member')
    copy('reviews/package_02/'+name,'evidence/reviews/package_02/'+name,'frozen_package_02')
copy('ROOT_WHOLE_PACKAGE_REVIEW_02.json','evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json','root_whole_package_02_adoption')
base=AUDIT/'reviews/package_03'
pins=json.loads((base/'OUTPUT_PINS.json').read_text())
if len(pins['files'])!=304:raise RuntimeError('whole03 sealed output count')
for rec in pins['files']:
    data=(base/rec['path']).read_bytes()
    if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:raise RuntimeError('frozen whole03 mismatch: '+rec['path'])
for name in sorted([rec['path'] for rec in pins['files']]+['OUTPUT_PINS.json','SEAL.json']):
    if '/' in name or name.lower()=='fullsource.txt' or Path(name).suffix.lower() not in {'.txt','.md','.json','.py',''}:raise RuntimeError('unexpected terminal whole03 member')
    copy('reviews/package_03/'+name,'evidence/reviews/package_03/'+name,'frozen_package_03')
copy('ROOT_WHOLE_PACKAGE_REVIEW_03.json','evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_03.json','root_whole_package_03_adoption')
manifest=dict(previous)
manifest['files']=records
(ROOT/'EVIDENCE_COPY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(copied_authored_records=len(records),original_files=11,all_copies_byte_identical=True,private_sources_copied=False)))
