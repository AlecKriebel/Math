"""Explicit accepted whole02 terminal guard; no assertions or external dependencies."""
import hashlib,json
def require(ok,message):
    if not ok:raise ValueError(message)
def verify_terminal(root):
    def get(name):return (root/name).read_bytes()
    def check(row):
        data=get(row['path']);require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'protected reviewed payload changed: '+row['path'])
    state=json.loads(get('CURRENT_REVIEW_STATE.json'));accepted=json.loads(get('support/FINAL_ACCEPTANCE.json'))
    require(state['stage']=='TERMINAL_ACCEPTED_WHOLE02_ADMINISTRATION' and state['publication_ready'] is True and state['all_issues_resolved'] is True and state['published'] is False and state['fresh_whole_package_reviews']==2,'terminal ready state required')
    require(accepted['publication_ready'] is True and accepted['published'] is False and accepted['fresh_whole_package_reviews']==2 and accepted['actionable_issues']==[],'terminal acceptance differs')
    check(accepted['root_adoption_pin'])
    adoption=json.loads(get('support/history/ROOT_WHOLE_PACKAGE_REVIEW_02.json'))
    require(adoption['status']=='ADOPT_ZERO_ACTIONABLE_WHOLE02_PENDING_TERMINAL_ADMIN_SEAL' and adoption['root_entire_report_and_verdict_read'] is True and adoption['root_independent_derivation_and_source_interface_read'] is True and adoption['mathematics_accepted_unchanged'] is True and adoption['fresh_whole_package_reviews']==2,'root full exact whole02 adoption required')
    prefix='support/history/reviews/package_02/'
    verdict=json.loads(get(prefix+'VERDICT.json'))
    require(verdict['verdict']=='ACCEPT_SCOPED_WHOLE_PACKAGE' and verdict['finding_counts']=={'P0':0,'P1':0,'P2':0,'P3':0} and verdict['required_corrections']==[] and verdict['historical_P3_01_exact_implementation_verified'] is True,'terminal whole02 must have zero actionable P0-P3')
    for name,field in [('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('OUTPUT_PINS.json','output_pins_sha256'),('REVIEW_SEAL.json','review_seal_sha256')]:
        require(hashlib.sha256(get(prefix+name)).hexdigest()==adoption[field],'root-adopted whole02 record differs: '+name)
    seal=json.loads(get(prefix+'REVIEW_SEAL.json'))
    require(seal['terminal_verdict']=='ACCEPT_SCOPED_WHOLE_PACKAGE' and all(seal[n]==0 for n in ['P0','P1','P2','P3']),'terminal review seal not zero')
    for name,field in [('INPUT_PINS.json','input_manifest_sha256'),('OUTPUT_PINS.json','output_manifest_sha256'),('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('FROZEN_DERIVATION.md','frozen_derivation_sha256')]:
        require(hashlib.sha256(get(prefix+name)).hexdigest()==seal[field],'terminal review seal hash mismatch: '+name)
    for row in accepted['protected_package_inputs']:check(row)
    for row in accepted['protected_external_inputs']:
        if (root/row['path']).exists():check(row)
    originals=json.loads(get('support/history/SUBMITTED_PINS.json'))['files'];require(len(originals)==8,'original eight required')
    for row in originals:check({'path':'support/history/'+row['snapshot_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    mapping=json.loads(get('support/COPY_MAP.json'))['copies'];require(len(mapping)==accepted['copy_count'],'terminal copy coverage changed')
    for row in mapping:check({'path':row['package_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    metadata=json.loads(get('.zenodo.json'))
    require(metadata==json.loads(get('metadata.json'))['metadata'],'bibliographic metadata equality changed')
    require(hashlib.sha256(json.dumps(metadata,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==accepted['metadata_object_sha256'],'protected bibliographic metadata object changed')
    if (root/'zenodo-deposit.json').exists():require(json.loads(get('zenodo-deposit.json'))['metadata']==metadata,'external bibliographic metadata differs')
    allow=json.loads(get('SUPPORT_ALLOWLIST.json'))['members'];pins=json.loads(get('TERMINAL_INPUT_PINS.json'))
    rows=[]
    for name in sorted(allow):
        if name in {'SUPPORT_MANIFEST.json','TERMINAL_INPUT_PINS.json'}:continue
        data=get(name);rows.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    require(pins['schema']=='pr1052-terminal-input-pins-v1' and pins['self_excluded'] is True and pins['files']==rows,'terminal input pin mismatch')
