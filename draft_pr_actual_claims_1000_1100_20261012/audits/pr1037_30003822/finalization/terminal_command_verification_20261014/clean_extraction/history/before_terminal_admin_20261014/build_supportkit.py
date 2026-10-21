#!/usr/bin/env python3
"""Rebuild a local, deterministic current supportkit; no network or Git calls."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'pr1037_supportkit_v1.0.zip'
GENERATED={'MANIFEST.json','ARCHIVE_PIN.json',ARCHIVE.name,'zenodo-deposit.json'}
EXCLUDED={'render','raw','rawprivate','extractedcache','__pycache__','.venv','tmp','cache'}
def digest(data):return hashlib.sha256(data).hexdigest()
def included(p):
    rel=p.relative_to(ROOT)
    return p.is_file() and not any(x in EXCLUDED for x in rel.parts) and str(rel) not in GENERATED and p.suffix not in {'.zip','.pyc','.log','.aux','.out'}
files=sorted((p for p in ROOT.rglob('*') if included(p)),key=lambda p:p.relative_to(ROOT).as_posix())
# Noncircular manifest hashes payload members, while being a ZIP member itself.
manifest={'edition_date':'2026-10-13','version':'1.0','package_type':'credited proof exposition and authored support evidence','review_state':'PENDING_NEW_WHOLE_02; publication_ready=false; all_issues_resolved=false; no publication approval','hash_algorithm':'SHA-256','self_reference_policy':'MANIFEST.json is a member without its own payload hash; ARCHIVE_PIN.json externally pins manifest and archive and is excluded from the ZIP. zenodo-deposit.json externally lists the PDF and ZIP with identical metadata and is excluded to avoid an archive self-reference. ZIPs, raw/private/render/extracted caches, environments and compiler intermediates are excluded.','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files]}
manifest_path=ROOT/'MANIFEST.json';manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
all_files=sorted(files+[manifest_path],key=lambda p:p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ARCHIVE,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
    for p in all_files:
        name=p.relative_to(ROOT).as_posix();info=zipfile.ZipInfo(name,(2026,10,13,0,0,0))
        info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None
    assert z.namelist()==[p.relative_to(ROOT).as_posix() for p in all_files]
    for p in all_files:assert z.read(p.relative_to(ROOT).as_posix())==p.read_bytes()
archive_data=ARCHIVE.read_bytes();manifest_data=manifest_path.read_bytes()
pin={'snapshot_date':'2026-10-13','archive':ARCHIVE.name,'bytes':len(archive_data),'sha256':digest(archive_data),'manifest':'MANIFEST.json','manifest_bytes':len(manifest_data),'manifest_sha256':digest(manifest_data),'payload_members':len(files),'archive_members':len(all_files),'zip_policy':'Sorted relative POSIX paths; timestamp 2026-10-13 00:00:00 for every member; Unix regular-file mode 0644; DEFLATE level 9; no archive pin or nested archives. Deterministic for unchanged inputs and the same ZIP implementation.','round_trip_all_bytes_verified':True}
(ROOT/'ARCHIVE_PIN.json').write_text(json.dumps(pin,indent=2)+'\n')
print(json.dumps(pin,indent=2))
