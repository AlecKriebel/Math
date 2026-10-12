import datetime, hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return {'path':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
manifest=json.loads((root/'EVIDENCE_MANIFEST.json').read_text())
for item in manifest['public_authored_files']+manifest['private_reading_inputs']:
    p=root/item['path'];b=p.read_bytes()
    assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
for record in manifest['actual_child_process_records']:
    directory=(root/record['record_path']).parent
    for which in ['stdout','stderr']:
        b=(directory/(which+'.bin')).read_bytes()
        assert len(b)==record[which]['bytes']
        assert hashlib.sha256(b).hexdigest()==record[which]['sha256']
verdict=json.loads((root/'VERDICT.json').read_text())
assert verdict['candidate_bytes']==11679
assert verdict['definitive_novelty_clearance'] is False
assert verdict['automatic_block_from_search_nonexhaustiveness'] is False
assert verdict['exact_prior_affirmative_result_identified'] is False
assert verdict['candidate_correctness_assessed_by_this_family'] is False
assert (root/'.gitignore').read_text().splitlines()==['private/','process_evidence/','__pycache__/']
files=['REPORT.md','VERDICT.json','LITERATURE_LEDGER.md','RESEARCH_LOG.md','EVIDENCE_MANIFEST.json','FIRST_SOURCE_ONLY.md','FIRST_SOURCE_ONLY_PIN.json','FIRST_PRIORITY.md','FIRST_PRIORITY_PIN.json','CANDIDATE_AUTH.json','AUTHOR_SOURCES_AUTH.json','PRIMARY_INPUT_MANIFEST.json','capture.py','write_manifest.py','final_artifact_check.py']
result={'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit_completion_best_guess_percent':100,'completion_scope':'Assigned bounded primary-literature audit complete; exact novelty, present-day openness and correctness are not certified. Specific source gaps remain.','all_manifest_file_and_process_byte_pins_verified':True,'independence_pins_unchanged':True,'artifact_pins':[pin(root/f) for f in files],'process_record':'process_evidence/final_artifact_check/result.json'}
(root/'FINAL_ARTIFACT_PINS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'finished_utc':result['finished_utc'],'audit_completion_best_guess_percent':100,'all_manifest_file_and_process_byte_pins_verified':True,'independence_pins_unchanged':True,'report_bytes':(root/'REPORT.md').stat().st_size,'manifest_bytes':(root/'EVIDENCE_MANIFEST.json').stat().st_size,'final_artifact_pins_path':str(root/'FINAL_ARTIFACT_PINS.json')}))
