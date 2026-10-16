#!/usr/bin/env python3
"""Copy only pinned, authored evidence into the local review package."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
records=[]
def copy(source, target, group):
    src=AUDIT/source; dst=ROOT/target
    dst.parent.mkdir(parents=True,exist_ok=True)
    data=src.read_bytes();dst.write_bytes(data)
    records.append(dict(source_path=source,package_path=target,group=group,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),copy_policy='byte-identical authored record; private attachments excluded'))
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
manifest=dict(policy='Only authored prose, source receipts/metadata, exact-check code and receipts, and pins. No raw/rawprivate third-party bodies, extracts, images, caches, or citation-discovery response dump.',original_head='ad138ddd5bd1a51c0f225f03342c0c058873f790',original_files=11,files=records)
(ROOT/'EVIDENCE_COPY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(copied_authored_records=len(records),original_files=11,all_copies_byte_identical=True,private_sources_copied=False)))
