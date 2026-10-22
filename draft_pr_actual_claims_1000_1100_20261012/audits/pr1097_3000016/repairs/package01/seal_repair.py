#!/usr/bin/env python3
"""Hash and seal settled bounded-repair artifacts without touching prior stages."""
import sys
sys.dont_write_bytecode=True
import datetime
import hashlib
import json
from pathlib import Path

F=Path(__file__).resolve().parent
A=F.parent.parent
P=A/'preprint_v1_0'

def need(q,m):
    if not q:raise ValueError(m)

def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def load(p):return json.loads(p.read_text())

def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')

def main():
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    need(not (F/'SEAL.json').exists(),'terminal seal already exists')
    baseline=load(F/'INPUT_PINS.json')['entries']
    before={r['path']:r for r in load(F/'BEFORE_BYTES.json')['entries']}
    validation=load(F/'VALIDATION.json')
    commands=load(F/'COMMAND_RECEIPTS.json')
    need(validation['status']==commands['status']=='PASS','validation not terminal PASS')
    need(len(commands['entries'])==validation['command_count']==99,'command count')
    need(sum(not r['expected_success'] for r in commands['entries'])==82,'rejection count')
    rows=[]
    for r in baseline:
        want={'bytes':r['bytes'],'sha256':r['sha256']}
        current=pin(A/r['path'])
        if current==want:
            row={'captured_path':r['path'],'status':'UNCHANGED_AT_CAPTURED_PATH',**want}
        else:
            need(r['path'] in before,'unpermitted late edit')
            b=before[r['path']]
            need(pin(A/b['before_path'])==want,'changed before bytes missing')
            row={'captured_path':r['path'],'status':'PERMITTED_CURRENT_CHANGE_EXACT_BEFORE_RETAINED',
                 'before_path':b['before_path'],'before':want,'current':current}
        rows.append(row)
    need(sum(r['status']=='UNCHANGED_AT_CAPTURED_PATH' for r in rows)==325,'preservation count')
    write(F/'BASELINE_PRESERVATION.json',{'utc':utc,'baseline_count':len(rows),
        'unchanged_at_captured_path':325,'permitted_existing_changes_with_exact_before':7,'entries':rows})
    current=[]
    for p in sorted(P.rglob('*')):
        if p.is_file() and not p.is_symlink():current.append({'path':str(p.relative_to(P)),**pin(p)})
    write(F/'CURRENT_CANDIDATE_PINS.json',{'utc':utc,'root':str(P),
          'scope':'Every current regular candidate file at bounded-repair handoff; prior output inventories retain captured-stage meanings',
          'entries':current})
    need(pin(P/'paper.pdf')==validation['paper'],'paper drift after validation')
    need(pin(P/'pr1097_support_v1_0.zip')==validation['archive'],'archive drift after validation')
    for r in load(P/'kit/provenance/repair01/COPIES.json')['entries']:
        need(pin(A/r['source_path'])==pin(P/'kit'/r['copy_path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'late exact copy drift')
    entries=[]
    paths=sorted(set([p for p in F.rglob('*') if p.is_file() and not p.is_symlink()]+[p for p in P.rglob('*') if p.is_file() and not p.is_symlink()]))
    for p in paths:
        if p in [F/'OUTPUT_PINS.json',F/'SEAL.json']:continue
        entries.append({'path':str(p.relative_to(A)),**pin(p)})
    write(F/'OUTPUT_PINS.json',{'utc':utc,'root':str(A),
        'scope':'Every bounded-repair regular record including exact before bytes, and every current candidate regular file; excludes this inventory and its separate SEAL',
        'entries':entries})
    for r in entries:need(pin(A/r['path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'output seal race')
    seal={'utc':utc,'status':'BOUNDED_REPAIR01_COMPLETE_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE02',
        'pr':1097,'head':'ad7b0eeef847da65afe1b691705cfa6e832e8201','problem_id':3000016,
        'output_inventory':{'path':'repairs/package01/OUTPUT_PINS.json',**pin(F/'OUTPUT_PINS.json')},
        'output_records_bound':len(entries),'current_candidate_files_bound':len(current),
        'prior_regular_inputs_hash_frozen':len(baseline),'unchanged_existing_inputs':325,
        'permitted_existing_changes_exact_before_bytes_retained':7,
        'supplementary_exact_source_copies':48,'original165_capture_83copy_82exclusion_decisions':'UNCHANGED',
        'prior_pin_rows_resolved_or_individually_omitted':1127,
        'validation':{'commands':99,'expected_rejections':82,'physical_case_normalization_alias_rejections':28,
                      'both_writers_both_Python_modes':True,'compiler_child_invoked_by_rejections':False,
                      'new_compilation_or_rendering':False,'actual_native_uploader_local_check':'PASS'},
        'paper':pin(P/'paper.pdf'),'support_archive':pin(P/'pr1097_support_v1_0.zip'),
        'shared_guard':pin(P/'kit/scripts/common.py'),
        'mathematics_TeX_PDF_checker_and_bibliographic_metadata':'UNCHANGED',
        'priority':'UNKNOWN','new_complete_whole_reviews_completed':1,'minimum_complete_whole_reviews_required':2,
        'addressed_finding':'P3_CASE_ALIAS_PROTECTED_OUTPUT_BYPASS','new_complete_whole02_required':True,
        'publication_ready':False,'published':False,'ordered_service_hold_pr':1032,
        'Git_index_branch_service_outreach_action':False,'delegated_repair_completion_percent':100}
    write(F/'SEAL.json',seal)
    print(json.dumps(seal,indent=2))

if __name__=='__main__':main()
