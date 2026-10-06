import datetime, hashlib, json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parent
PYTHON='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
ENV={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,message):
    if not ok: raise ValueError(message)
def pin(p):
    b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
require(not (ROOT/'OUTPUT_MANIFEST.json').exists(),'final seal already exists; refusing overwrite')
argv=[PYTHON,'-E','-S','-B','-P',str(ROOT/'verify_inputs.py')]
start=utc(); p=subprocess.run(argv,cwd=ROOT,env=ENV,capture_output=True,check=False); stop=utc()
(ROOT/'input_validation.stdout.json').write_bytes(p.stdout)
(ROOT/'input_validation.stderr.json').write_bytes(p.stderr)
(ROOT/'FINAL_VALIDATION_RECEIPT.json').write_text(json.dumps({'argv':argv,'cwd':str(ROOT),
    'environment':ENV,'started_at':start,'finished_at':stop,'exit_code':p.returncode,
    'stdout':pin(ROOT/'input_validation.stdout.json'),'stderr':pin(ROOT/'input_validation.stderr.json')},indent=2)+'\n')
require(p.returncode==0,'final input validation failed; full diagnostic preserved')
integrity=json.loads(p.stdout)
require(integrity['status']=='pass','input verification not PASS')
(ROOT/'INPUT_INTEGRITY.json').write_text(json.dumps(integrity,indent=2)+'\n')
diagnostics={'captured_at':utc(),'tool_level_events':[{
    'kind':'read_only_file_probe','exit_code':1,
    'detail':'No AGENTS.md at nested checkout root; no source of mathematical evidence. Repository-root policy was read.',
    'expected_audit_guard_failure':False},{
    'kind':'web_open','url':'https://msp.org/ant/2013/7-4/p06.xhtml',
    'detail':'Web tool reported unsupported application/xhtml+xml. Official PDF acquisition succeeded.',
    'expected_audit_guard_failure':False},{
    'kind':'web_open','url':'https://doi.org/10.2140/ant.2013.7.917',
    'detail':'Web tool reported inaccessible landing URL. Official PDF cover/first page establishes published year.',
    'expected_audit_guard_failure':False}],
    'process_level_mutant_failures':'Sixteen expected exit-2 diagnostics retained in CHECK_PROCESS_RECEIPTS.json and output files.',
    'unexpected_validation_process_failures':0}
(ROOT/'DIAGNOSTIC_EVENTS.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
checks=json.loads((ROOT/'CHECK_RESULTS.json').read_text())
checkpoint=json.loads((ROOT/'SOURCE_SCOPE_CHECKPOINT.json').read_text())
require(checks['normal_and_optimized_identical'] and checks['unexpected_failure_processes']==0,'verification result mismatch')
now=utc()
with (ROOT/'RESEARCH_LOG.md').open('a') as f:
    f.write('- 2026-10-06T19:03:39.209995+00:00: Normal/-O exact checks agree; 5,005 active bases, 15 vertices, two optimal endpoints, 495 rational controls; eight mutants each rejected in both modes. Audit completion 85%; novel target-resolution estimate 0%.\n')
    f.write(f'- {now}: Complete human goal read; exact priority chronology and materiality challenged. Original 20 members, full source, ledger1/5 and early checkpoint pins rechecked unchanged. Final disposition PASS, no blocking correction to proposed closure comment. Audit completion 100%; novel complete target-resolution estimate 0%. No external mutation performed.\n')
result={'schema':'independent-pr117-priority-disposition-adversary/v1','sealed_at':now,
    'verdict':'PASS_PROPOSED_ALREADY_SOLVED_DISPOSITION','mathematical_verdict':'PASS_COMPLETE_COUNTEREXAMPLE',
    'priority_verdict':'EXACT_PUBLISHED_PRIOR_BY_2013','recommended_target_assessment':'already_solved',
    'recommended_pr_action':'close_without_merging','new_solution_publication_supported':False,
    'no_substantive_new_full_target_resolution_established':True,
    'full_face_exposition_and_code_value':'useful elementary explanation and reproducibility of already published counterexample',
    'reasonable_repair':'additive attribution/status clarification and explicit-exception diagnostics; does not restore novelty',
    'incoming_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8','target':30001234,
    'original_budget':'1/5','new_proof_search_turns':0,'original_20_members_unchanged':True,
    'independence':{'source_scope_sealed_before_root_or_other_family_reports':True,
                    'other_family_reports_read':False,'source_scope_checkpoint':pin(ROOT/'SOURCE_SCOPE_CHECKPOINT.json')},
    'authoritative_goal':integrity['authoritative_goal'],
    'primary_urls':['https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf','https://ems.press/content/serial-article-files/46224'],
    'primary_printed_pages':{'takagi2013':[937,939,940],'owr2009':[1137,1138,1139]},
    'primary_takagi_pdf_bytes':1075287,'primary_takagi_pdf_sha256':'6ada6b6669124acda5bb4b0bd25a98d07b39808c07e7d41c1f0ae1ba49e085e5',
    'bridge_permutation_zero_based':[0,3,1,4,5,2],
    'normal_and_optimized_pass':True,'active_bases_examined':5005,'feasible_vertices':15,
    'optimal_vertices':2,'rational_segment_controls':495,'expected_mutant_exit2_processes':16,
    'unexpected_validation_process_failures':0,'mandatory_findings':['counterexample mathematics valid',
      'exact prior answers original minimal monomial-free condition','no publication route under human novelty standard',
      'preserve original immutable artifacts and ledger','coordinate/sign/ambient bridge accurate; no blocking comment correction'],
    'exact_remaining_gaps':['earliest discovery date not established by this independent audit',
      'prior printing/priority of full-face exposition not exhaustively established; does not affect original negative-answer priority',
      'integration authentication and any authorized native/PR action remain root responsibilities'],
    'performed_actions':{'git_index_or_main_mutation':False,'native_assessment':False,'pr_comment':False,
                         'pr_close':False,'merge':False,'publication':False,'external_contact':False},
    'completion_estimate_percent':100,'novel_complete_target_resolution_estimate_percent':0,
    'report':pin(ROOT/'REPORT.md'),'check_results':pin(ROOT/'CHECK_RESULTS.json'),
    'copyrighted_source_body_public':False}
(ROOT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
public=[p for p in sorted(ROOT.iterdir()) if p.is_file() and p.name!='OUTPUT_MANIFEST.json']
require(all(p.suffix not in ('.pdf','.png','.txt') for p in public),'private copyrighted body included in public members')
manifest={'schema':'exact-public-member-manifest/v1','sealed_at':now,'folder':str(ROOT),
    'members':[pin(p) for p in public],'member_count':len(public),
    'excluded_directories':['private/'],'manifest_self_pin':'provided externally in final delivery to avoid circular digest',
    'private_pdf_text_render_bodies_excluded':True}
(ROOT/'OUTPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'REPORT.md':pin(ROOT/'REPORT.md'),'RESULT.json':pin(ROOT/'RESULT.json'),
    'OUTPUT_MANIFEST.json':pin(ROOT/'OUTPUT_MANIFEST.json'),'public_member_count_excluding_manifest':len(public)},indent=2))
