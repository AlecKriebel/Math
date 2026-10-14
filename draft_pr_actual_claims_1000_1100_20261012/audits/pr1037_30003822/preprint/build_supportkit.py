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
def require(ok, message):
    if not ok: raise RuntimeError(message)
state=json.loads((ROOT/'CURRENT_REVIEW_STATE.json').read_text())
terminal=json.loads((ROOT/'evidence/whole_20261014/package_02/VERDICT.json').read_text())
adoption=json.loads((ROOT/'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json').read_text())
acceptance=json.loads((ROOT/'evidence/FINAL_ACCEPTANCE.json').read_text())
require(state['publication_ready'] is True and state['published'] is False and
        state['all_issues_resolved'] is True and state['fresh_whole_package_reviews']==2,
        'accepted terminal ready administration required')
require(terminal['status']=='PASS_ZERO_ACTIONABLE_P0_P3' and terminal['issues']==[] and
        terminal['issue_counts']=={'P0':0,'P1':0,'P2':0,'P3':0}, 'terminal actionable review findings')
require(adoption['root_entire_report_and_verdict_read'] and adoption['mathematics_accepted_unchanged'] and
        adoption['status']=='ADOPT_ZERO_ACTIONABLE_FINDINGS_PENDING_TERMINAL_ADMIN_SEAL',
        'root terminal exact-candidate acceptance required')
for name,field in (('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('OUTPUT_PIN.json','output_pins_sha256')):
    require(digest((ROOT/'evidence/whole_20261014/package_02'/name).read_bytes())==adoption[field],
            'root-adopted terminal review hash differs')
require(acceptance['fresh_whole_package_reviews']==2 and acceptance['publication_ready'] is True and
        acceptance['published'] is False and acceptance['actionable_issues']==[], 'terminal acceptance differs')
for row in acceptance['protected_mathematical_source_PDF_metadata']:
    p=ROOT/Path(row['path']).relative_to('preprint')
    if p.name=='zenodo-deposit.json' and not p.exists():
        continue  # Explicitly external sidecar; absent from a clean extracted kit.
    require(p.stat().st_size==row['bytes'] and digest(p.read_bytes())==row['sha256'],
            'protected reviewed paper/metadata differs')
metadata=json.loads((ROOT/'.zenodo.json').read_text())
require(json.loads((ROOT/'zenodo_metadata.json').read_text())=={'metadata':metadata}, 'metadata wrapper differs')
deposit=ROOT/'zenodo-deposit.json'
if deposit.exists():
    require(json.loads(deposit.read_text())=={'metadata':metadata,'files':[{'path':'paper/forest_transfer_catalan.pdf'},{'path':'pr1037_supportkit_v1.0.zip'}]}, 'external deposit metadata/file selection differs')
files=sorted((p for p in ROOT.rglob('*') if included(p)),key=lambda p:p.relative_to(ROOT).as_posix())
# Noncircular manifest hashes payload members, while being a ZIP member itself.
manifest={'edition_date':'2026-10-13','version':'1.0','package_type':'credited proof exposition and authored support evidence','review_state':'ACCEPTED_ZERO_ACTIONABLE_NEW_WHOLE_02; publication_ready=true; all_issues_resolved=true; published=false; root final administration verification pending; services blocked by preceding PR1032','hash_algorithm':'SHA-256','self_reference_policy':'MANIFEST.json is a member without its own payload hash; ARCHIVE_PIN.json externally pins manifest and archive and is excluded from the ZIP. zenodo-deposit.json externally lists the PDF and ZIP with identical metadata and is excluded to avoid an archive self-reference. ZIPs, raw/private/render/extracted caches, environments and compiler intermediates are excluded.','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files]}
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
