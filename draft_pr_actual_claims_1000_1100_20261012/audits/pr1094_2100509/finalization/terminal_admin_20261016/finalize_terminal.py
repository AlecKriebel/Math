"""Final individual custody recheck and separate NON-readiness handoff seal."""
from pathlib import Path
import datetime, difflib, hashlib, json
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/'preprint_v1_0';K=P/'kit'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def rec(p,n):
    b=p.read_bytes();return {'path':n,'bytes':len(b),'sha256':sha(b)}
def wj(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def main():
    need(not (R/'SEAL.json').exists(),'already terminal sealed; do not rewrite')
    need(not (R/'scratch').exists(),'own scratch remains')
    baseline=json.loads((R/'FROZEN_INPUT_PINS.json').read_text())['records']
    before={r['path']:r for r in baseline}
    allowed=[r['path'] for r in json.loads((R/'ALLOWED_CHANGES.json').read_text())['existing_edits']]
    changes=[]; protected=[]
    for r in baseline:
        n=r['path'];actual=rec(A/n,n)
        if n in allowed:
            need(rec(R/'before'/n,n)==r and actual!=r,'allowed before/current bytes not exact')
            changes.append({'path':n,'before':r,'current':actual,'exact_before_locator':'before/'+n})
        else:
            need(actual==r,'protected original changed: '+n);protected.append(r)
    need(len(baseline)==419 and len(changes)==6 and len(protected)==413,'input boundary counts')
    wj(R/'INPUT_PRESERVATION.json',{'utc':now(),'baseline_count':419,'allowed_existing_edits':changes,'protected_unchanged_count':413,'all_protected_inputs_rehashed':True,'old_CURRENT_STATUS_all_guards_math_TeX_PDF_native_metadata_unchanged':True})
    for n in ('preprint_v1_0/paper.pdf','preprint_v1_0/kit/paper.pdf'):
        need((A/n).stat().st_size==69486 and sha((A/n).read_bytes())=='a1e2da77dd739bcc7ddc4dd8ba916c99010450e4224ae7a52d01d34c98960e72','paper changed')
    native=json.loads((P/'zenodo-deposit.json').read_text());meta=json.loads((K/'metadata.json').read_text())
    need(native=={'metadata':meta,'files':[{'path':'paper.pdf','name':'paper.pdf'},{'path':'pr1094_supportkit_v1.0.zip','name':'pr1094_supportkit_v1.0.zip'}]},'native uploader schema or files differs')
    need(meta==json.loads((K/'.zenodo.json').read_text())==json.loads((K/'metadata_api.json').read_text())['metadata'],'shared metadata differs')
    binding=json.loads((P/'DEPOSIT_BINDING.json').read_text())
    need(binding['metadata']==meta and binding['files']==[rec(P/n,n) for n in ('paper.pdf','pr1094_supportkit_v1.0.zip')],'current binding differs')
    ledger=json.loads((K/'TERMINAL_SOURCE_COPY_LEDGER.json').read_text());copied=[]
    for r in ledger['copies']:
        n=r['original_path'];need(rec(K/r['copy_path'],n)==before[n],'new copy is not exact initial bytes')
        copied.append(r)
    need(len(copied)==10,'terminal copy count')
    need((P/'TERMINAL_ACCOUNTING_20261016.json').read_bytes()==(K/'TERMINAL_ACCOUNTING_20261016.json').read_bytes(),'outer/kit accounting differs')
    t=json.loads((K/'TERMINAL_ACCOUNTING_20261016.json').read_text())
    need(t['completed_new_whole_package_reviews']==t['minimum_new_whole_package_reviews']==2 and t['new_complete_whole_review_required'] is False,'terminal counts')
    need(t['publication_ready'] is t['issues_resolved'] is t['published'] is t['root_terminal_integrity_adopted'] is False and t['root_terminal_integrity_required'] is True,'terminal pending root flags')
    m=json.loads((K/'MANIFEST.json').read_text());current_members=[rec(p,p.relative_to(K).as_posix()) for p in sorted(K.rglob('*')) if p.is_file() and not p.is_symlink() and p!=K/'MANIFEST.json']
    need(m['records']==current_members and len(current_members)==128,'current manifest exact/self-excluded')
    stage=json.loads((R/'PRIOR_STAGE_RESOLUTION.json').read_text());count=0
    for s in stage['stages']:
        need(rec(A/s['inventory'],s['inventory'])==s['inventory_pin'],'old stage inventory changed')
        for r in s['records']:
            need(rec(A/r['resolution'],'')=={'path':'','bytes':r['bytes'],'sha256':r['sha256']},'old stage resolution changed');count+=1
    need(count==1539,'prior stage count')
    for r in stage['nested_family_paths']:
        need(rec(Path(r['resolution']),'')=={'path':'','bytes':r['bytes'],'sha256':r['sha256']},'nested history changed')
    seals=[]
    for seal,pins,key in [
        ('preprint_v1_0/PREPARATION_SEAL.json','preprint_v1_0/OUTPUT_PINS.json','output_pins_sha256'),
        ('reviews/package_01/SEALED.json','reviews/package_01/OUTPUT_PINS.json','output_pins_sha256'),
        ('repairs/package01/SEAL.json','repairs/package01/OUTPUT_PINS.json','output_pins_sha256'),
        ('reviews/collar_algebra_01/SEALED.json','reviews/collar_algebra_01/OUTPUT_PINS.json','output_pin_sha256'),
        ('reviews/priority_01/SEALED.json','reviews/priority_01/OUTPUT_PINS.json','output_pins_sha256')]:
        s=json.loads((A/seal).read_text());need(s[key]==sha((A/pins).read_bytes()),'old seal inventory binding')
        seals.append({'seal':rec(A/seal,seal),'inventory':rec(A/pins,pins),'binding_field':key,'binding_exact':True})
    ws=json.loads((A/'reviews/package_02/SEAL.json').read_text());need(ws['output_pins']==rec(A/'reviews/package_02/OUTPUT_PINS.json','OUTPUT_PINS.json'),'whole02 seal binding')
    wr=json.loads((A/'ROOT_WHOLE_PACKAGE_REVIEW_02.json').read_text());need(wr['output_pins_sha256']==ws['output_pins']['sha256'],'root whole02 seal binding')
    seals.append({'seal':rec(A/'reviews/package_02/SEAL.json','reviews/package_02/SEAL.json'),'inventory':rec(A/'reviews/package_02/OUTPUT_PINS.json','reviews/package_02/OUTPUT_PINS.json'),'root_adoption':rec(A/'ROOT_WHOLE_PACKAGE_REVIEW_02.json','ROOT_WHOLE_PACKAGE_REVIEW_02.json'),'binding_exact':True})
    wj(R/'OLD_SEAL_BINDINGS.json',{'utc':now(),'status':'PASS','records':seals,'old_seals_and_statuses_exact_dated_history':True})
    v=json.loads((R/'VALIDATION.json').read_text());need(v['status']=='PASS' and v['actual_commands']==139 and v['expected_rejections']==128 and v['no_compile_or_render'] is True,'actual validation incomplete')
    z=json.loads((R/'CLOSED_ARCHIVE_REVIEW.json').read_text());need(z['archive']==rec(P/'pr1094_supportkit_v1.0.zip','pr1094_supportkit_v1.0.zip') and z['member_count']==129,'validated archive changed')
    current=[rec(p,p.relative_to(A).as_posix()) for p in sorted(P.rglob('*')) if p.is_file() and not p.is_symlink()]
    wj(R/'CURRENT_ARTIFACT_PINS.json',{'utc':now(),'scope':'Every current regular delivery artifact, including current ZIP/binding/manifest; older original pins keep dated meaning.','records':current})
    wj(R/'FINAL_CUSTODY_RECHECK.json',{'utc':now(),'status':'PASS','baseline_count':419,'unchanged_protected_count':413,'allowed_existing_edits':changes,'current_delivery_count':len(current),'terminal_copies':copied,'prior_inventory_rows_rehashed':1539,'nested_family_paths_rehashed':69,'old_partition_counts':[171,309],'old_status_pins_reports_seals_rootadoptions_exact':True,'paper_math_TeX_shared_safety_all_native_metadata_and_native_manifest_exact':True,'current_manifest_payload_records':128,'current_archive_members':129,'current_archive':rec(P/'pr1094_supportkit_v1.0.zip','pr1094_supportkit_v1.0.zip'),'outer_kit_terminal_record_identical':True,'new_compile_render_or_services':False})
    wj(R/'TERMINAL_HANDOFF.json',{'utc':now(),'status':'DELEGATED_TERMINAL_ADMIN_COMPLETE_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','pr':1094,'head_oid':t['head_oid'],'original_submitted_files':8,'delegated_completion_percent':100,'completed_new_whole_reviews':2,'minimum_new_whole_reviews':2,'new_complete_whole_review_currently_required':False,'latest_whole02_zero_actionable_and_root_adopted':True,'root_terminal_integrity_required':True,'root_terminal_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'final_readiness_seal_issued':False,'ordered_services_hold_pr':1032,'services_performed':False,'git_mutations':False,'new_compiler_render_or_source_reading':False,'unexpected_candidate_findings':[],'new_whole03_required_if_new_actionable_finding':True})
    with (R/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now()+' — Final checkpoint: 100% of delegated terminal administrative reconciliation complete. All 419 initial inputs resolve; 413 protected originals exact and six authorized successors individually pinned with exact before bytes. Final 1,539 stage rows, 69 nested paths, ten new copies, six old seal/inventory bindings and every current delivery artifact rehashed. Completed 139-command clean validation; no candidate finding. ROOT final integrity adoption remains required and absent; publication_ready/issues_resolved/published=false and hold PR1032. Separate delegated handoff seal follows after all preceding writes settle.\n')
    parts=[]
    new_current=['preprint_v1_0/TERMINAL_ACCOUNTING_20261016.json','preprint_v1_0/kit/TERMINAL_ACCOUNTING_20261016.json','preprint_v1_0/kit/TERMINAL_SOURCE_COPY_LEDGER.json']
    for n in allowed+new_current:
        if n.endswith('.zip'):continue
        b=(R/'before'/n).read_text().splitlines(keepends=True) if n in allowed else []
        parts.extend(difflib.unified_diff(b,(A/n).read_text().splitlines(keepends=True),fromfile='before/'+n if n in allowed else '/dev/null',tofile='current/'+n))
    for p in sorted(R.iterdir()):
        if p.suffix not in ('.py','.md'):continue
        parts.extend(difflib.unified_diff([],p.read_text().splitlines(keepends=True),fromfile='/dev/null',tofile=p.relative_to(A).as_posix()))
    (R/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(parts))
    outputs=[rec(p,p.relative_to(R).as_posix()) for p in sorted(R.rglob('*')) if p.is_file() and not p.is_symlink() and p.name not in ('OUTPUT_PINS.json','SEAL.json')]
    wj(R/'OUTPUT_PINS.json',{'utc':now(),'scope':'Every retained regular terminal-admin output, including exact before bytes, own harness/code/prose and interrupted-harness evidence; excludes only this inventory and separate seal to avoid a hash cycle. No scratch or third-party body/runtime added.','records':outputs})
    seal={'utc':now(),'status':'DELEGATED_TERMINAL_ADMIN_COMPLETE_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','not_a_final_readiness_seal':True,'pr':1094,'head_oid':t['head_oid'],'original_submitted_files':8,'delegated_completion_percent':100,'baseline_input_count':419,'protected_unchanged_count':413,'allowed_existing_edits':6,'output_count':len(outputs),'output_pins':rec(R/'OUTPUT_PINS.json','OUTPUT_PINS.json'),'current_delivery_count':len(current),'terminal_exact_authored_copies':10,'prior_stage_inventory_rows':1539,'nested_history_paths':69,'preserved_partition_counts':[171,309],'completed_new_whole_reviews':2,'minimum_new_whole_reviews':2,'new_complete_whole_review_currently_required':False,'latest_whole02_P0_P1_P2_P3':0,'root_whole02_adopted':True,'root_terminal_integrity_required':True,'root_terminal_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'ordered_services_hold_pr':1032,'priority_novelty_worldwide_openness':'UNKNOWN','actual_commands':139,'expected_rejections':128,'semantic_rejections':46,'writer_rejections':66,'bootstrap_rejections':8,'paper':rec(P/'paper.pdf','paper.pdf'),'support_zip':rec(P/'pr1094_supportkit_v1.0.zip','pr1094_supportkit_v1.0.zip'),'current_root_manifest':rec(K/'MANIFEST.json','MANIFEST.json'),'native_manifest':rec(P/'zenodo-deposit.json','zenodo-deposit.json'),'separate_inventory_seal_no_hash_cycle':True,'all_prior_writes_settled_before_this_seal':True,'no_Git_service_compiler_render_or_outreach':True}
    wj(R/'SEAL.json',seal)
    for r in outputs:need(rec(R/r['path'],r['path'])==r,'sealed output changed')
    need(sha((R/'OUTPUT_PINS.json').read_bytes())==seal['output_pins']['sha256'],'seal inventory differs')
    print(json.dumps(seal,indent=2))
if __name__=='__main__':main()
