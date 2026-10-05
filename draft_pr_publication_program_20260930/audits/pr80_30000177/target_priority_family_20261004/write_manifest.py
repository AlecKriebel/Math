import datetime, hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
def pin(path):
    b=path.read_bytes(); return {'path':str(path.relative_to(root)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
records=[]
for path in sorted((root/'process_evidence').glob('*/result.json')):
    record=json.loads(path.read_text())
    for which in ['stdout','stderr']:
        p=path.parent/(which+'.bin'); actual=pin(p)
        assert record[which]['bytes']==actual['bytes']
        assert record[which]['sha256']==actual['sha256']
    records.append({'record_path':str(path.relative_to(root)), **record})
for filename,pinfile in [('FIRST_SOURCE_ONLY.md','FIRST_SOURCE_ONLY_PIN.json'),('FIRST_PRIORITY.md','FIRST_PRIORITY_PIN.json')]:
    previous=json.loads((root/pinfile).read_text());actual=pin(root/filename)
    assert previous['bytes']==actual['bytes'] and previous['sha256']==actual['sha256']
auth=json.loads((root/'CANDIDATE_AUTH.json').read_text()); src=json.loads((root/'AUTHOR_SOURCES_AUTH.json').read_text())
assert json.loads((root/'FIRST_SOURCE_ONLY_PIN.json').read_text())['frozen_utc'] < json.loads((root/'FIRST_PRIORITY_PIN.json').read_text())['frozen_utc'] < auth['first_read_utc'] < src['first_read_utc']
private=[pin(p) for p in sorted((root/'private').rglob('*')) if p.is_file()]
public=[pin(p) for p in sorted(root.iterdir()) if p.is_file() and p.name not in ['EVIDENCE_MANIFEST.json','FINAL_ARTIFACT_PINS.json']]
data={
    'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Own dedicated folder only; no Git/index/queue/branch/PR/publication/outreach mutation.',
    'private_storage_policy':'.gitignore excludes private/,process_evidence/,__pycache__/; full copyrighted captures are not public authored findings.',
    'native_web_process_metadata':'No shell argv/cwd/PID/exit exposed by web tool; native request/response/timing captures are in private/. No fabricated subprocess fields.',
    'process_helper':'capture.py records real child subprocess argv,cwd,PID,start/end UTC,exit and exact full stdout/stderr with byte pins; helper propagates child exit.',
    'public_authored_files':public,
    'private_reading_inputs':private,
    'actual_child_process_records':records,
    'successful_downloaded_pdf_count':len([p for p in (root/'process_evidence').glob('download_*/stdout.bin') if p.read_bytes()[:5]==b'%PDF-']),
    'authenticated_copied_pdf_count':len(list((root/'private'/'primary').glob('*.pdf'))),
    'nonzero_child_labels':[pathlib.Path(r['record_path']).parent.name for r in records if r['exit_code']],
    'nonpdf_successful_request':'download_yuan2011_springer returned HTML subscription preview, not PDF; extract child1.',
    'independence_checks':{'unchanged_first_pins':True,'chronology_order_verified':True,'candidate_auth':auth,'author_sources_auth':src},
    'generation_process_record':'process_evidence/write_manifest/result.json',
    'final_verification_process_record':'process_evidence/final_artifact_check/result.json'
}
(root/'EVIDENCE_MANIFEST.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'process_records':len(records),'private_files':len(private),'public_files':len(public),'successful_downloaded_pdfs':data['successful_downloaded_pdf_count'],'copied_authenticated_pdfs':data['authenticated_copied_pdf_count'],'all_capture_byte_pins_checked':True,'unchanged_first_pins':True}))
