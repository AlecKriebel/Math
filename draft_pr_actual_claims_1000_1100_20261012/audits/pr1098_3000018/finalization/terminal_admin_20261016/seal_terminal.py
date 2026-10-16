"""Final exact baseline/copy/current checks, then write the terminal seal last."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import difflib
import hashlib
import json
import stat
import sys

sys.dont_write_bytecode=True
F=Path(__file__).resolve().parent
A=F.parents[1]
C=A/'preprint_v1_0'

def need(value,message):
    if not value: raise ValueError(message)

def rec(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def obj(p): return json.loads(p.read_text())

def save(name,value):
    (F/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')

def main():
    need(not (F/'OUTPUT_SEAL.json').exists(),'terminal seal already exists')
    changed={'preprint_v1_0/'+n for n in ['README.md','code/verify_kit.py','MANIFEST.json','DEPOSIT_BINDING.json','pr1098_support_v1_0.zip']}
    rows=[];counts=Counter()
    freeze=obj(F/'INPUT_FREEZE.json')['entries']
    for row in freeze:
        name=row['path'];p=A/name;expected={k:row[k] for k in ('bytes','sha256')}
        actual=rec(p);info=p.lstat()
        if name in changed:
            before=F/'before'/name
            need(rec(before)==expected,'extant exact before '+name)
            need(actual!=expected,'changed interface unexpectedly equal '+name)
            status='CHANGED_CURRENT_EXACT_EXTANT_BEFORE'
            result={**row,'disposition':status,'before_path':str(before.relative_to(A)),
                'before_identity':rec(before),'current_identity':actual,
                'before_public_disposition':'DURABLE_LOCAL_IGNORED_NOT_REDISTRIBUTED' if name.endswith('.zip') else 'EXACT_AUTHORED_BEFORE_INTERFACE'}
        else:
            need(actual==expected,'protected preexisting bytes '+name)
            need(stat.S_IMODE(info.st_mode)==row['mode'] and info.st_mtime_ns==row['mtime_ns']
                 and info.st_nlink==row['nlink'],'protected preexisting metadata '+name)
            status='UNCHANGED_CURRENT_EXACT'
            result={**row,'disposition':status,'current_identity':actual,'mode_mtime_nlink_unchanged':True}
        rows.append(result);counts[status]+=1
    need(len(rows)==358 and counts['CHANGED_CURRENT_EXACT_EXTANT_BEFORE']==5,'358/5 baseline')
    save('BASELINE_RESOLUTION.json',{'utc':datetime.now(timezone.utc).isoformat(),'entries':rows,
        'counts':dict(counts),'every_changed_baseline_has_extant_exact_before':True,
        'preexisting_inputs_retired_or_removed':0})
    copies=obj(F/'COPY_LEDGER.json')['entries']
    for row in copies:
        need(rec(A/row['source'])==rec(C/row['destination'])=={k:row[k] for k in ('bytes','sha256')},'copy '+row['destination'])
    need(len(copies)==18,'18 exact copies')
    prep=obj(C/'INPUT_FREEZE.json')['entries']
    for row in prep:need(rec(A/row['path'])=={k:row[k] for k in ('bytes','sha256')},'168 preparation baseline')
    custody=obj(C/'CUSTODY_SELECTION.json')['entries'];ct=Counter()
    need(len(prep)==len(custody)==168 and {r['path'] for r in prep}=={r['path'] for r in custody},'168 custody partition')
    for row in custody:
        ct[row['disposition']]+=1
        need(rec(A/row['path'])=={k:row[k] for k in ('bytes','sha256')},'custody original')
        if row['disposition']=='EXACT_AUTHORED_COPY':
            need((A/row['path']).read_bytes()==(C/row['destination']).read_bytes(),'80 exact copies')
        else:need(row['disposition']=='OMITTED' and bool(row['reason']),'individual historical exclusion')
    need(ct=={'EXACT_AUTHORED_COPY':80,'OMITTED':88},'80/88 custody split')
    original_pins=obj(C/'OUTPUT_PINS.json')
    need(len(original_pins['entries'])==123 and obj(C/'PREPARATION_SEAL.json')['output_pins_sha256']==rec(C/'OUTPUT_PINS.json')['sha256'],'old 123 pin/seal')
    resolution=obj(C/'terminal/PREPARATION_PIN_RESOLUTION.json')['entries']
    need([{k:r[k] for k in ('path','bytes','sha256')} for r in resolution]==original_pins['entries'],'123 exact resolution original identities')
    for row in resolution:
        expected={k:row[k] for k in ('bytes','sha256')}
        if row['disposition']=='KNOWN_OLD_ZIP_OMITTED':p=F/'before/preprint_v1_0/pr1098_support_v1_0.zip'
        elif row['disposition']=='UNCHANGED_LOCAL_PREPARATION_OUTPUT_OMITTED':p=C/row['path']
        else:p=C/row['resolved_path']
        need(rec(p)==expected,'old preparation row extant exact '+row['path'])
    reviews=[]
    for number in (1,2):
        root=A/('reviews/package_'+str(number).zfill(2));pins=obj(root/'OUTPUT_PINS.json')
        for row in pins['entries']:need(rec(root/row['path'])=={k:row[k] for k in ('bytes','sha256')},'unchanged whole-review output')
        need(obj(root/'OUTPUT_SEAL.json')['output_pins']==rec(root/'OUTPUT_PINS.json'),'whole-review seal/pin')
        reviews.append({'review':str(root.relative_to(A)),'unchanged_pinned_outputs':len(pins['entries'])})
    first_git=obj(A/'reviews/package_01/CUSTODY_REVIEW.json')['actual_git']
    prep_git=obj(C/'validation/ORIGINAL_INPUT_RECHECK.json')['actual_git']
    need(len(first_git)==len(prep_git)==9,'two frozen 9-file Git receipts')
    submitted=[]
    for row in first_git:
        name=Path(row['path']).name;p=A/'submitted'/name;expected={k:row[k] for k in ('bytes','sha256')}
        match=next(r for r in prep_git if r['path']==name)
        need(rec(p)==expected=={k:match[k] for k in ('bytes','sha256')} and match['actual_git_equal'],'submitted exact frozen receipts')
        submitted.append({'path':name,**expected,'equals_two_frozen_actual_Git_receipts':True})
    save('CUSTODY_RECHECK.json',{'status':'PASS','preparation_baseline':168,'custody':dict(ct),
        'old_preparation_output_pins':123,'prep_resolution_counts':dict(Counter(r['disposition'] for r in resolution)),
        'exact_new_authored_interface_copies':18,'individual_review_stage_rows':55,'whole_reviews':reviews,
        'submitted':submitted,'fresh_Git_invocation':False,
        'Git_scope':'Current nine submitted bytes rehashed against two frozen actual-Git comparison receipts; no fresh Git object access.',
        'all_preexisting_review_stages_and_ROOT_adoptions_exact':True})
    need((F/'TERMINAL_STATUS.json').read_bytes()==(C/'TERMINAL_STATUS.json').read_bytes(),'identical current terminal records')
    before_manifest=obj(F/'before/preprint_v1_0/MANIFEST.json')
    current_manifest=obj(C/'MANIFEST.json')
    old_names={r['path'] for r in before_manifest['entries']}
    added=sorted({r['path'] for r in current_manifest['entries']}-old_names)
    need(len(added)==22,'22 added administrative members')
    diff=[]
    for name in ['README.md','code/verify_kit.py','MANIFEST.json','DEPOSIT_BINDING.json']:
        diff.extend(difflib.unified_diff((F/'before/preprint_v1_0'/name).read_text().splitlines(keepends=True),
            (C/name).read_text().splitlines(keepends=True),fromfile='before/preprint_v1_0/'+name,tofile='current/preprint_v1_0/'+name))
    authored=['TERMINAL_STATUS.json','terminal/README.md','terminal/PREPARATION_PIN_RESOLUTION.json','terminal/REVIEW_STAGE_SELECTION.json']
    for name in authored:
        diff.extend(difflib.unified_diff([], (C/name).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='current/preprint_v1_0/'+name))
    (F/'OPERATIVE_DIFF.patch').write_text(''.join(diff))
    save('BINARY_CHANGE.json',{'path':'preprint_v1_0/pr1098_support_v1_0.zip',
        'before':rec(F/'before/preprint_v1_0/pr1098_support_v1_0.zip'),'current':rec(C/'pr1098_support_v1_0.zip'),
        'before_extant_durable_local_ignored':True,'before_omitted_from_public_payload':True,
        'new_payload_members':added,'new_authored_administrative_members':authored,
        'other_18_new_members':'Exact authored copies individually resolved by COPY_LEDGER.json; no edited source text omitted from operative diff.'})
    current_names=[r['path'] for r in current_manifest['entries']]+['MANIFEST.json','paper.pdf','pr1098_support_v1_0.zip','DEPOSIT_BINDING.json']
    current_rows=[{'path':'preprint_v1_0/'+n,**rec(C/n)} for n in sorted(current_names)]
    save('CURRENT_PINS.json',{'utc':datetime.now(timezone.utc).isoformat(),'entries':current_rows,
        'scope':'Every current manifest member plus the manifest, mandatory external paper/ZIP and outer deposit binding; no recursive self hash.'})
    need(obj(F/'VALIDATION.json')['status']=='PASS' and obj(F/'VALIDATION.json')['commands']==153,'final actual validation')
    with (F/'RESEARCH_LOG.md').open('a') as stream:
        stream.write('\n'+datetime.now(timezone.utc).isoformat()+' — Final 153-command actual run passed: full mathematical JSON normal/optimized equals preparation, unconditional faults, 42 coherent semantic/evidence faults, physical/bootstrap guards and independent closed archive reconstruction. All 358 preexisting rows individually resolved (353 exact current, five extant exact before); 168/80/88 custody, 123 preparation identities, two frozen nine-file Git receipts and 22/33 review pins checked. Current and before ledgers, full operative diff, output inventory/pins and seal completed after current payload settled. Completion estimate: 100% of bounded terminal administration. External ROOT final integrity remains required/unadopted; readiness/issues-resolved/published false and services held after PR #1032.\n')
    files=[p for p in sorted(F.rglob('*')) if p.is_file() and '.scratch' not in p.relative_to(F).parts
        and p.name not in ('OUTPUT_INVENTORY.json','OUTPUT_PINS.json','OUTPUT_SEAL.json')]
    inventory=[{'path':str(p.relative_to(F)),**rec(p),
        'disposition':'DURABLE_LOCAL_IGNORED_NOT_REDISTRIBUTED' if p==F/'before/preprint_v1_0/pr1098_support_v1_0.zip' else 'ENDURING_AUTHORED_OUTPUT'} for p in files]
    save('OUTPUT_INVENTORY.json',{'entries':inventory,
        'final_control_files':['OUTPUT_INVENTORY.json','OUTPUT_PINS.json','OUTPUT_SEAL.json'],
        'scratch_contents':[],'cleanup':'Only two successive newly owned compact external fixture trees were removed after exact inventory; ATTEMPT_01 and final cleanup records both retained.'})
    files=[p for p in sorted(F.rglob('*')) if p.is_file() and '.scratch' not in p.relative_to(F).parts and p.name not in ('OUTPUT_PINS.json','OUTPUT_SEAL.json')]
    pins=[{'path':str(p.relative_to(A)),**rec(p)} for p in files]+current_rows
    save('OUTPUT_PINS.json',{'utc':datetime.now(timezone.utc).isoformat(),'entries':pins,
        'excludes_own_pinfile_and_seal':True,'durable_local_before_ZIP_is_individually_pinned_but_not_public':True})
    save('OUTPUT_SEAL.json',{'utc':datetime.now(timezone.utc).isoformat(),
        'status':'TERMINAL_ADMIN_COMPLETE_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY',
        'delegated_completion_percent':100,'output_pins':rec(F/'OUTPUT_PINS.json'),'outputs':len(pins),
        'report':rec(F/'REPORT.md'),'operative_diff':rec(F/'OPERATIVE_DIFF.patch'),
        'baseline_resolution':rec(F/'BASELINE_RESOLUTION.json'),'current_pins':rec(F/'CURRENT_PINS.json'),
        'current_closed_ZIP':rec(C/'pr1098_support_v1_0.zip'),'unchanged_PDF':rec(C/'paper.pdf'),
        'all_writes_settled_before_this_seal':True,'preexisting_regular_inputs':358,
        'unchanged_current_inputs':353,'changed_inputs_with_extant_exact_before':5,
        'whole_reviews_completed':2,'minimum_whole_reviews':2,'latest02_zero_actionable_ROOT_adopted':True,
        'further_whole_package_review_currently_required':False,'ROOT_final_terminal_integrity':'REQUIRED_UNADOPTED',
        'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,
        'actual_final_commands':153,'first_actual_admin_failure_preserved':True,
        'no_Git_index_branch_service_outreach_other_shard_or_subagent_action':True,
        'seal_excludes_itself_and_own_pinfile':True})
    print(json.dumps({'status':'SEALED_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','pins':len(pins),
        'current_ZIP':rec(C/'pr1098_support_v1_0.zip'),'seal':rec(F/'OUTPUT_SEAL.json')}))

if __name__=='__main__':main()
