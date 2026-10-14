import datetime, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'sealed_at':now,'phase':'independent_source_scope_before_other_reports',
        'incoming_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8','target_id':30001234,
        'original_attempts_used':1,'original_attempt_limit':5,'new_proof_search_turns':0,
        'other_family_reports_read':False,'root_disposition_read':False,'closure_comment_read':False,
        'source_scope_completion_estimate_percent':95,'novel_complete_resolution_estimate_percent':0,
        'members':[pin(ROOT/name) for name in ['SOURCE_SCOPE_CHECKPOINT.md','ACQUISITION_RECEIPTS.json','TARGET_RENDER_RECEIPT.json','acquire.py']],
        'inspected_pixels':[pin(ROOT/'private'/name) for name in ['p937.png','scope-24.png','scope-25.png','owrscope-37.png','owrscope-38.png','owrscope-39.png']]}
(ROOT/'SOURCE_SCOPE_CHECKPOINT.json').write_text(json.dumps(record,indent=2)+'\n')
(ROOT/'RESEARCH_LOG.md').write_text('# Independent PR117 disposition audit log\n\n'
    '- 2026-10-06T18:57Z: Began independent exact-target/primary-source audit. Completion estimate 10%; no new proof-search turn.\n'
    '- 2026-10-06T18:59Z: Downloaded official 2009/2013 PDFs; full relevant 240 dpi pixels inspected. Acquisition and render process receipts saved. Completion estimate 55%.\n'
    f'- {now}: Sealed source-scope checkpoint before sibling/root reports. Same augmented LP, singleton-fiber quantifier, ideal and generator system after permutation; ambient c=0 removes extra equality. Source-scope completion 95%; overall audit completion 65%; novel complete target resolution estimate 0%.\n')
print(json.dumps({'checkpoint':pin(ROOT/'SOURCE_SCOPE_CHECKPOINT.json'),'source_scope':pin(ROOT/'SOURCE_SCOPE_CHECKPOINT.md')}))
