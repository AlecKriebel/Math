#!/usr/bin/env python3
"""Finite source-first seal only; no mathematical/native/foreign code execution."""
import datetime, hashlib, json, stat
from pathlib import Path
Q=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23409879/reviews/scope-sol')
S=Q.parent.parent/'sources'
def need(x,label):
    if not x: raise ValueError(label)
def row(p,root):
    a=p.lstat(); need(stat.S_ISREG(a.st_mode) and not p.is_symlink(),'regular finite file')
    b=p.read_bytes(); z=p.lstat(); need((a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'stable bytes')
    return dict(path=p.relative_to(root).as_posix(),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(a.st_mode)))
def inventory(root):
    files=[]; dirs=[]
    for p in sorted(root.rglob('*')):
        a=p.lstat(); need(not p.is_symlink(),'no symlink')
        if stat.S_ISREG(a.st_mode): files.append(row(p,root))
        elif stat.S_ISDIR(a.st_mode): dirs.append(dict(path=p.relative_to(root).as_posix(),mode=oct(stat.S_IMODE(a.st_mode))))
        else: raise ValueError('special finite entry')
    return files,dirs
def write(name,data):
    p=Q/name
    with p.open('x') as f: json.dump(data,f,indent=2,ensure_ascii=False); f.write('\n')
    return row(p,Q)
custody=json.loads((Q/'SOURCE_CUSTODY.json').read_text())
source_files,source_dirs=inventory(S)
need(source_files==custody['files'] and source_dirs==custody['directories'] and (len(source_files),len(source_dirs))==(77,10),'all source77bytes/modes10dirs unchanged at gate')
files,dirs=inventory(Q)
need(not {'INITIAL_MANIFEST.json','INITIAL_SEAL.json'}&{r['path'] for r in files},'initial seal exclusively new')
need({r['path'] for r in dirs}=={'source-pdf-pages'} and len([r for r in files if r['path'].startswith('source-pdf-pages/')])==6,'all6 fresh source image files included')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest=write('INITIAL_MANIFEST.json',dict(schema='whole-source-first-owned-payload-manifest-v1',UTC=now,payload_files=files,directories=dirs,exact_excluded_terminal_controls=['INITIAL_MANIFEST.json','INITIAL_SEAL.json'],no_future_carveouts=True))
seal=write('INITIAL_SEAL.json',dict(schema='source-first-scientific-initial-seal-v1',UTC=now,status='SOURCE_ONLY_INITIAL_HAND_RESULTS_FROZEN_BEFORE_SUPPORT_PRIMARY_AND_CURRENT_OPINION',
    record='23409879',row=174,manifest=manifest,INITIAL=row(Q/'INITIAL.json',Q),hand_results=row(Q/'INITIAL_HAND_RESULTS.md',Q),
    finite_extent=dict(regular_files=len(files)+2,child_directories=len(dirs),files=sorted([r['path'] for r in files]+['INITIAL_MANIFEST.json','INITIAL_SEAL.json']),directories=dirs),
    all77source_bytes_modes10dirs_unchanged=True,all393TeX_and6PDFpages_text_and_fresh_pixels_personally_read=True,
    source_first_opaque_native_metadata_and_rights_read=True,informed_prior_related_geometry_copy_and_production_exposure_disclosed=True,
    support_program_README_audit_results_and_foreign_proof_bodies_opened=False,current174root_peer_or_other_family_findings_opened=False,
    scientific_verdict=None,follow_up=None,source_gate_percent=100,full_scientific_review_percent_estimate=40,
    root_handoff_readiness_pins_extent_status_only=True,publication_action_authority=False,self_hash_excluded=True))
actual,actual_dirs=inventory(Q)
need(len(actual)==len(files)+2 and actual_dirs==dirs,'exact source-first finite closure')
print(json.dumps(dict(seal=seal,manifest=manifest,regular_files=len(actual),child_directories=len(actual_dirs),source77_unchanged=True),indent=2))
