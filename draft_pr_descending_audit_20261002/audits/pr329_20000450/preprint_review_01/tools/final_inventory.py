#!/usr/bin/env python3
"""Computed final inventory for an external audit; intentionally not a seal."""
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess

R=Path(__file__).resolve().parents[1]
output=R/'COMPLETE_INVENTORY.json'
assert not output.exists(),'Refuse to overwrite a held inventory'
capture='evidence/closing/complete_inventory_01'
excluded={'COMPLETE_INVENTORY.json'}|{capture+s for s in ['.argv.json','.stdout','.stderr','.native-time.txt']}
def sha(body):return hashlib.sha256(body).hexdigest()
def load(path):return json.loads(path.read_bytes())

# Every prior frozen body/mode, including exact old log prefixes.
early=[]
for name in ['ROOT_PREPRINT01_SOURCE_GATE.json','ROOT_PREPRINT01_FIRST_CANDIDATE_GATE.json']:
    gate=load(R/'evidence/stage_integrity'/name)
    for rec in gate['payloads']:
        p=R/rec['path'];body=p.read_bytes()
        assert stat.S_IMODE(p.stat().st_mode)==rec['mode_decimal'],rec['path']+' mode'
        if rec['path']=='RESEARCH_LOG.md':assert len(body)>=rec['bytes'] and sha(body[:rec['bytes']])==rec['sha256'],'Old log prefix changed'
        else:assert len(body)==rec['bytes'] and sha(body)==rec['sha256'],rec['path']+' body changed'
    for rel,mode in gate['directory_modes'].items():assert stat.S_IMODE((R/rel).stat().st_mode)==mode,rel+' directory mode'
    early.append(dict(external_inventory=name,payloads=len(gate['payloads']),all_prior_bodies_modes_exact=True,log_append_only=True))

# Final report discharges every genuine first-assessment row without inventing IDs.
pattern=r'^\| ([A-Z][0-9]{2}) \|'
old=set(re.findall(pattern,(R/'FIRST_CANDIDATE_ASSESSMENT.md').read_text(),re.M))
current=set(re.findall(pattern,(R/'FULL_PREPRINT_REVIEW.md').read_text(),re.M))
assert old==current and len(old)==47,(old-current,current-old)
pins=load(R/'evidence/candidate_full/exact_full_input_pins.json')
for pin in pins:
    p=Path(pin['copy']);body=p.read_bytes()
    assert len(body)==pin['bytes'] and sha(body)==pin['sha256'],pin['name']
    assert Path(pin['source']).read_bytes()==body,'Released source changed '+pin['name']
archive=R/'evidence/candidate_full/archive'
manifest=load(archive/'MANIFEST.json')
for rel,expected in manifest['files'].items():
    p=archive/rel;body=p.read_bytes()
    assert dict(bytes=len(body),sha256=sha(body),mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')==expected,'Original archive changed '+rel

# Index actual process records, retaining pointers to complete raw streams.
receipts=[]
for p in sorted(R.rglob('*.argv.json')):
    rel=str(p.relative_to(R))
    if rel in excluded:continue
    stem=str(p)[:-len('.argv.json')]
    times=Path(stem+'.native-time.txt')
    out=Path(stem+'.stdout');err=Path(stem+'.stderr')
    assert times.is_file() and out.is_file() and err.is_file(),str(p)
    match=re.fullmatch(r'START ([^\n]+)\nEND ([^\n]+)\nEXIT (-?\d+)\n',times.read_text())
    assert match,str(times)
    receipts.append(dict(kind='main actual process receipt',argv_record=rel,native_clock=str(times.relative_to(R)),stdout=str(out.relative_to(R)),stderr=str(err.relative_to(R)),start_native_utc=match[1],end_native_utc=match[2],exit=int(match[3])))
for p in sorted((R/'families/exact_geometry/runs').glob('*/record.json')):
    rec=load(p)
    assert rec['start_native_date']['exit']==rec['end_native_date']['exit']==0
    out=p.parent/'stdout.bin';err=p.parent/'stderr.bin'
    assert len(out.read_bytes())==rec['stdout_bytes'] and len(err.read_bytes())==rec['stderr_bytes']
    receipts.append(dict(kind='geometry family actual process receipt',record=str(p.relative_to(R)),stdout=str(out.relative_to(R)),stderr=str(err.relative_to(R)),start_native_date=rec['start_native_date'],end_native_date=rec['end_native_date'],exit=rec['exit']))
for p in sorted((R/'families/primary_inputs/native').glob('*/run.json')):
    rec=load(p)
    assert (p.parent/rec['stdout']).is_file() and (p.parent/rec['stderr']).is_file() and (p.parent/rec['http_headers']).is_file()
    receipts.append(dict(kind='primary family actual retrieval process receipt',record=str(p.relative_to(R)),stdout=str((p.parent/rec['stdout']).relative_to(R)),stderr=str((p.parent/rec['stderr']).relative_to(R)),headers=str((p.parent/rec['http_headers']).relative_to(R)),start_actual_utc=rec['start_utc'],end_actual_utc=rec['end_utc'],exit=rec['exit_code']))
for p in sorted((R/'evidence/guard_controls').glob('*_actual_receipt/record.json')):
    rec=load(p)
    assert len((p.parent/'stdout.bin').read_bytes())==rec['stdout_bytes'] and len((p.parent/'stderr.bin').read_bytes())==rec['stderr_bytes']
    receipts.append(dict(kind='fresh expected-failure guard actual child receipt',record=str(p.relative_to(R)),stdout=str((p.parent/'stdout.bin').relative_to(R)),stderr=str((p.parent/'stderr.bin').relative_to(R)),native_start=str((p.parent/'native_start.txt').relative_to(R)),native_end=str((p.parent/'native_end.txt').relative_to(R)),exit=rec['exit']))

files=[];dirs=[]
for p in sorted(R.rglob('*')):
    rel=str(p.relative_to(R))
    assert not p.is_symlink(),'Unexpected final symlink '+rel
    mode=f'{stat.S_IMODE(p.stat().st_mode):04o}'
    if p.is_dir():dirs.append(dict(path=rel,mode=mode))
    elif p.is_file() and rel not in excluded:
        body=p.read_bytes();files.append(dict(path=rel,bytes=len(body),sha256=sha(body),mode=mode))
groups={}
for f in files:groups.setdefault((f['bytes'],f['sha256']),[]).append(f['path'])
duplicates=[dict(bytes=k[0],sha256=k[1],paths=v) for k,v in sorted(groups.items()) if len(v)>1]
clock=subprocess.check_output(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ']).decode().strip()
inventory=dict(status='COMPLETE_UNSEALED_HOLD_FOR_PARENT_EXTERNAL_AUDIT',actual_inventory_capture_utc=clock,review_goal_percent=100,
    publication_clearance=False,self_sealed=False,scope='Complete current qualified eight-input paper/archive/metadata review; no mathematical gap identified, one source-attribution wording correction, one subordinate historical failure-record limit.',
    exact_release_pins=pins,prior_freeze_integrity=early,body_claim_ids=sorted(old),body_claim_count=len(old),
    payload_file_count=len(files),directory_count=len(dirs),payloads=files,directory_modes=dirs,
    actual_native_receipt_count=len(receipts),actual_native_receipts=receipts,
    identical_body_groups=duplicates,
    exclusions_sorted=sorted(excluded),exclusion_reason='Self-reference and live closing capture cannot be recursively hash-bound here. Parent must externally inventory these five final files plus all listed payloads. This computed inventory is not a seal or retrieval evidence.',
    evidence_limits=dict(primary_exploratory_failure='Historical actual tool stdout/stderr/exit1 retained; no contemporaneous native UTC bounds or saved old program body. Current corrected program and separate main/root native replays are reproducible.',ordinary_read_path_failures='Historical tool outputs exist; native later failure replays are explicitly later, not invented old clocks.',status_snippet_exposure='After genuine source-only/first-candidate freezes and explicit full release; no other-project verdict files opened or results used.',family_freezes='Primary source-first but no pre-candidate written family freeze; geometry candidate-first before source intake with no family freeze. Main genuine freezes remain authoritative.'))
output.write_text(json.dumps(inventory,indent=2)+'\n')
assert all((R/f['path']).read_bytes() and sha((R/f['path']).read_bytes())==f['sha256'] if f['bytes'] else (R/f['path']).read_bytes()==b'' for f in files),'Payload changed during capture'
print(json.dumps(dict(status=inventory['status'],capture_utc=clock,covered_payload_files=len(files),covered_directories=len(dirs),actual_receipt_records=len(receipts),body_claims=len(old),inventory_sha256=sha(output.read_bytes()),inventory_bytes=output.stat().st_size,external_closing_files=sorted(excluded),source_and_first_candidate_body_mode_integrity=True,log_append_only=True,publication_clearance=False),indent=2))
