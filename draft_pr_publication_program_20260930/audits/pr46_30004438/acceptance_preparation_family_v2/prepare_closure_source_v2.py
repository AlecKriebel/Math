"""Own text-only adaptation of the read standalone V1 closer for ROOT's V2 use."""
from pathlib import Path
import difflib, json, os
H=Path(__file__).resolve().parent;V=H.parent/'acceptance_preparation_family'
def replace(s,a,b):
    assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    original=(V/'close_source.py').read_text();s=original
    s=replace(s,'This handwritten administrative closer imports no proposed production source.','This handwritten V2 administrative closer imports no proposed production source.\nRejected V1 and the actually completed adverse review remain preserved history.')
    s=replace(s,"CONTROL_SOURCE = 'e38fe4d3962be61e44c170d2ba5179150469a48f7cb0407129076d4a55edd82f'\nOPERATOR_SOURCE = '7ae924cd41a044e15fe6b208079921279917cb0e46a9c7f77d9962bc4c00a337'", "V1_SHA = 'd97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab'")
    s=replace(s,"    parser.add_argument('--expected-source-report-sha256', required=True)","    parser.add_argument('--expected-source-report-sha256', required=True)\n    parser.add_argument('--expected-controls-sha256', required=True)")
    s=replace(s,"    need(not (H / NAME).exists() and not (H / NAME).is_symlink(), 'Already closed')", "    need(re.fullmatch('[0-9a-f]{64}', args.expected_controls_sha256), 'Explicit completed controls SHA256 required')\n    need(not (H / NAME).exists() and not (H / NAME).is_symlink(), 'Already closed')")
    s=replace(s,"    candidate, cdirs = closed(C, 'MANIFEST.json', 946, CURRENT)",'''    rejected, unused_dirs = closed(A/'acceptance_preparation_family', NAME, 166, V1_SHA)
    need(same(rejected, parse(read(H/'EXPECTED_REJECTED_V1_MANIFEST.json'))), 'Entire rejected V1 source differs')
    repair = parse(read(H/'SOURCE_REPAIR_BINDINGS.json'))
    need(repair['status']=='COMPLETED_REJECTED_V1_ADVERSE_BINDINGS'
      and repair['closed_adverse_binding_completed'] is True
      and repair['superseded_v1_manifest_sha256']==V1_SHA
      and repair['future_acceptance_approved'] is False
      and repair['production_imported_compiled_executed'] is False, 'Completed actual adverse bindings required')
    for row in repair['complete_first_party_refs']:
        relative(row['path']);read(R/row['path'],row,row['full_mode'])
    ap=R/repair['closed_adverse_manifest']['path']
    need(ap.parent==A/'acceptance_source_adversary_family', 'Exact rejected adverse family')
    am=parse(read(ap,repair['closed_adverse_manifest'],0o444))
    closed(ap.parent,ap.name,am['files_count'],repair['closed_adverse_manifest']['sha256'])
    need(same(am,parse(read(H/'EXPECTED_REJECTED_V1_ADVERSE_MANIFEST.json'))), 'Entire closed adverse manifest differs')
    av=parse(read(R/repair['closed_adverse_verdict']['path'],repair['closed_adverse_verdict'],0o444))
    need(same(av,parse(read(H/'EXPECTED_REJECTED_V1_ADVERSE_VERDICT.json')))
      and av['mandatory_corrections'] and 'S1' in json.dumps(av['mandatory_corrections'])
      and av['production_imported_compiled_executed'] is False
      and av['future_acceptance_approved'] is False, 'Actual final adverse verdict differs')
    ar=parse(read(R/repair['root_complete_adverse_inspection']['path'],repair['root_complete_adverse_inspection']))
    need(same(ar,parse(read(H/'EXPECTED_ROOT_REJECTED_V1_INSPECTION.json')))
      and same(ar['complete_VERDICT_object'],av), 'Entire genuine ROOT adverse read differs')
    candidate, cdirs = closed(C, 'MANIFEST.json', 946, CURRENT)''')
    a=s.index("    exits = {'AUTHORING_ACTUAL_CAPTURE'");b=s.index('    for name in PRODUCTION:',a)
    s=s[:a]+'''    actuals=sorted(H.glob('*_ACTUAL_CAPTURE/CAPTURE.json'))
    need(len(actuals)>=5, 'Complete own authoring/repair/binding/closure-source/controls captures required')
    captures={p.parent.name:capture(p.parent,parse(read(p))['exit_code']) for p in actuals}
    selected=status['private_controls_capture']
    need(selected in captures, 'Exact successful private controls capture required')
    control=captures[selected]
    need(control['exit_code']==0 and control['status']=='PASS'
      and control['prelaunch']['source_sha256']==sha(read(H/'independent_controls_v2.py'))
      and control['prelaunch']['operator_sha256']==sha(read(H/'capture_owned_operation.py')),
      'Completed successful current V2 controls source/operator identity differs')
    raw_result=read(H/'OWN_CONTROL_RESULTS.json')
    need(sha(raw_result)==args.expected_controls_sha256, 'Complete actual V2 controls pin differs')
    result=parse(raw_result)
    need(result['schema']=='pr46-acceptance-source-v2-private-controls/v1'
      and result['status']=='PASS_PRIVATE_SOURCE_ONLY_S1_REPAIR_CONTROLS'
      and type(result['assertions']) is int and result['assertions']>50
      and len(result['checks'])==result['assertions']
      and all(z['passed'] is True for z in result['checks'])
      and result['actual_pid']==control['pid']
      and result['new_S1_boundary_rejection_before_mutation'] is True
      and result['no_whole_program_exclusion'] is True
      and result['unrelated_paths_preserved'] is True
      and result['owned_log_full_prefix_append_mode_verified'] is True
      and result['production_imported_compiled_executed'] is False
      and result['future_acceptance_approved'] is False
      and same(result['native13_before'],result['native13_after']),
      'Complete actual handwritten V2 source-only control evidence differs')
    need(dt.datetime.fromisoformat(control['started_utc'])<=
      dt.datetime.fromisoformat(result['utc'])<=dt.datetime.fromisoformat(control['finished_utc']),
      'Actual V2 control chronology differs')
    failure=result['private_V1_failure_reproduction']
    need(failure['actual_model_pid']==control['pid'] and failure['reproduced_S1'] is True
      and failure['production_executed'] is False
      and failure['logical_path']=='draft_pr_publication_program_20260930/RESEARCH_LOG.md',
      'Actual private V1 failure reproduction differs')
    ownership=parse(read(H/'OWNERSHIP_WRITE_INVENTORY.json'))
    need(ownership['additional_owned_tracked_body_paths']==['draft_pr_publication_program_20260930/RESEARCH_LOG.md']
      and ownership['complete_program_exclusion'] is False
      and ownership['canonical_overlay_payload_count']==955
      and ownership['accepted_payload_count']==957, 'Exact narrow S1 ownership scope differs')
    post=parse(read(H/'ROOT_POST_CONTRACT.json'))
    need(len(post['required_ROOT_complete_keyset'])==22
      and len(set(post['required_ROOT_complete_keyset']))==22
      and post['required_completed_values']['owned_operational_log_appends_exact'] is True,
      'Exact revised complete ROOT post contract differs')
''' +s[b:]
    s=replace(s,"'source_report_sha256':args.expected_source_report_sha256,", "'source_report_sha256':args.expected_source_report_sha256,\n      'actual_controls_sha256':args.expected_controls_sha256,")
    put(H/'close_source.py',s.encode())
    verifier=(V/'verify_closed_source.py').read_text().replace('ROOT-only future read-only post-exit inspection;','V2 ROOT-only future read-only post-exit inspection;')
    put(H/'verify_closed_source.py',verifier.encode())
    put(H/'V2_CLOSURE_SOURCE_ADAPTATION.patch',''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='read_closed_v1/close_source.py',tofile='root_only_v2/close_source.py')).encode())
    print(json.dumps({'status':'AUTHORED_V2_ROOT_ONLY_CLOSURE_SOURCE','actual_pid':os.getpid(),'closer_launched':False,'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
