#!/usr/bin/env python3
"""Select explicit, public, changed PR110 audit evidence; never stage here."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parents[1]
C=A.parents[2]
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
def need(x,m):
    if not x: raise RuntimeError(m)
def can(x): return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def cp(f): return {'path':str(f.relative_to(C)),**hp(f.read_bytes())}
def ap(f): return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
def read(f): return json.loads(f.read_bytes())
def git(*args):
    r=subprocess.run([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=True)
    need(not r.stderr,'Unexpected Git diagnostic')
    return r.stdout
need(git('rev-parse','--abbrev-ref','HEAD').strip()==b'main','main only')
need(git('rev-parse','HEAD').strip()==b'e0a94b93520610553c001f265f210f959b591c2c','Exact authenticated parent')
need(not git('diff','--cached','--name-only','-z'),'Empty index')
selected=set(A.glob('ROOT*.json'))|{A/'RESEARCH_LOG.md'}|set((A/'publication_build_v1').glob('*.py'))
D=A/'native_post_assess_carryforward_v3_20261006'
manifest=D/'OUTPUT_MANIFEST.json'
selected|={D/x['path'] for x in read(manifest)['files']}|{manifest,D/'SEAL_RECEIPT.json',D/'ROOT_CARRYFORWARD_GATE.json'}
for folder in ('current_main_carryforward_input_20261006','root_actual_candidate_reproduction_v2_20261006','actual_operations/root_actual_linear_carryforward_20261006','actual_operations/root_actual_pr110_export_20261006'):
    selected|={f for f in (A/folder).rglob('*') if f.is_file()}
V=A/'actual_native_candidate_adversary_20261006'
for name in ('LINEAR_CARRYFORWARD_PREEXEC_OUTPUT_MANIFEST.json','ACTUAL_NATIVE_CANDIDATE_OUTPUT_MANIFEST.json'):
    m=V/name
    selected|={m}|{V/x['path'] for x in read(m)['files']}
selected|={f for f in (D/'workspaces/candidate_d9eb646c1dd70e89').iterdir() if f.is_file()}
selected|={A/'actual_action_commissions_20261006/export_ROOT_GATE.json',A/'actual_action_inputs_20261006/export_EXTRA.json',A/'root_actual_candidate_reproduction_20261006/FAILURE_NOTE.json'}
F=A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006'
selected|={F/n for n in ('EXECUTION_INPUTS.json','PREFLIGHT.json','PREFLIGHT_ROOT_AUTHENTICATED.json','ROOT_GIT_REPLAY_JOURNAL.json','TRANSPORT_INVENTORY.json')}
E=A/'actual_acceptance_actions_20261006/pr110_export_20261006'
selected|={E/n for n in ('RECEIPT.json','START.json','PRE_EXPORT.json','EXPORT_PROGRESS.json','PROCESS_LAUNCHES.json','PROCESS_JOURNAL.json')}
for folder,names in (
    ('native_post_assess_carryforward_v2_20261006',('post_assess_carryforward.py','OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','STOPPED_CONTINUATION_INVENTORY.json')),
    ('native_post_assess_continuation_v1_20261006',('post_assess_continuation.py','OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','SEED_INVENTORY.json'))):
    selected|={A/folder/n for n in names}
for f in selected:
    s=f.lstat();need(stat.S_ISREG(s.st_mode) and not f.is_symlink() and s.st_nlink==1,'Regular public body only: '+str(f))
    need(f.is_relative_to(A) and not f.is_relative_to(D/'workspaces/candidate_d9eb646c1dd70e89/offer'),'Audit scope; no duplicated offer')
tracked={x.decode() for x in git('ls-files','-z','--',str(A.relative_to(C))).split(b'\0') if x}
changed={x.decode() for x in git('diff','--name-only','--diff-filter=ACMRTUXB','-z').split(b'\0') if x}
kept=sorted((f for f in selected if str(f.relative_to(C)) not in tracked or str(f.relative_to(C)) in changed),key=lambda f:str(f))
pins=[cp(f) for f in kept]
report=A/'actual_action_inputs_20261006/ACCEPTANCE_CHECKPOINT_SELECTION.json'
extra=A/'actual_action_inputs_20261006/acceptance_commit_EXTRA.json'
need(not report.exists() and not extra.exists(),'Unique selection and decision inputs')
need(len(pins)+1<=256,'Bounded exact audit additions')
report.write_bytes(can({'schema':'pr110-root-public-acceptance-selection/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_selector_PID':os.getpid(),'parent':'e0a94b93520610553c001f265f210f959b591c2c','selected_public_count':len(selected),'new_or_changed_evidence_count':len(pins),'existing_unchanged_evidence_already_committed_count':len(selected)-len(pins),'body_pins':pins,'selection_program_pin':ap(Path(__file__).resolve()),'Git_staging_executed':False,'excluded':'Source caches, third-party PDFs, stopped/private candidate offer duplication and unrelated physical sparse absences remain unstaged.'}))
pins.append(cp(report))
er=E/'RECEIPT.json';exported=read(er)
need(exported['native_export_executed'] is True and exported['all_exported_full_bytes_checked'] is True and len(exported['exported_paths'])==84,'Actual reviewed export')
for row in exported['exported_paths']:
    need(hp((C/row['path']).read_bytes())==row['after'],'Export body drift')
need((C/exported['additional_actual_target_receipt']).read_bytes()==er.read_bytes(),'Installed full live acceptance receipt')
need(sum(len(x['path'])+1 for x in pins)+sum(len(x['path'])+1 for x in exported['exported_paths'])+len(exported['additional_actual_target_receipt'])+1<=65536,'Bounded complete add argv')
extra.write_bytes(can({'export_receipt_pin':ap(er),'commit_identity':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},'commit_message':'Accept PR110: verified and published focal antipedal invariant','additional_checkpoint_pins':pins}))
print(json.dumps({'actual_selector_PID':os.getpid(),'extra_pin':ap(extra),'selection_report_pin':ap(report),'additional_count':len(pins),'additional_bytes':sum(x['bytes'] for x in pins),'actual_staging_executed':False}))
