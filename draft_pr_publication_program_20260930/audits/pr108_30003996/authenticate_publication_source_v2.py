from pathlib import Path, PurePosixPath
import hashlib, json, datetime, os
A = Path(__file__).resolve().parent
S, V = A/'publication_package_v2', A/'publication_package_v1'
def require(c, m):
    if not c: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def body(p):
    require(p.is_file() and not p.is_symlink(), 'regular input')
    return p.read_bytes()
def pin(p):
    b=body(p); return {'path':str(p.relative_to(A)), 'bytes':len(b), 'sha256':sha(b)}
mb=body(S/'SOURCE_PREPARATION_MANIFEST.json'); m=json.loads(mb)
seal=json.loads(body(S/'SEAL.json')); seen=set()
require(sha(mb)==seal['manifest_sha256']=='d05467112fa2a3e71d90dcf9bba4074af87075653582fb2eb0b8e2931cb71d16','manifest SHA')
for row in m['files']:
    rel=row['relative_path']; p=PurePosixPath(rel)
    require(str(p)==rel and not p.is_absolute() and '..' not in p.parts and rel not in seen,'member path')
    seen.add(rel); b=body(S/rel)
    require(len(b)==row['bytes'] and sha(b)==row['sha256'],'member pin')
require(len(seen)==seal['payload_files']==36 and sum(r['bytes'] for r in m['files'])==186557,'totals')
require(seen|{'SOURCE_PREPARATION_MANIFEST.json','SHA256SUMS','SEAL.json'}=={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()},'extra files')
cs=body(S/'SHA256SUMS')
require(len(cs)==seal['checksums_bytes'] and sha(cs)==seal['checksums_sha256'],'checksums pin')
for line in cs.decode().splitlines():
    h,rel=line.split('  ',1); require(sha(body(S/rel))==h,'checksum member')
c=json.loads(body(S/'CORRECTION_LEDGER.json'))
for row in c['V1_manifest_rows']:
    b=body(V/row['relative_path']); require(len(b)==row['bytes'] and sha(b)==row['sha256'],'V1 unchanged')
for row in c['R1_bindings']:
    b=body(A/row['relative_to_audit']); require(len(b)==row['bytes'] and sha(b)==row['sha256'],'R1 binding')
for row in c['paper_and_metadata_historical_preserved_exact']:
    require(body(S/row['relative_path'])==body(V/row['relative_path']),'paper/meta/history unchanged')
old=json.loads(body(V/'example_full_cost_instance.json')); new=json.loads(body(S/'example_full_cost_instance.json'))
omit={'UTC','actual_operator_PID','verifier_sha256'}
require({k:v for k,v in old.items() if k not in omit}=={k:v for k,v in new.items() if k not in omit},'mathematical fixture continuity')
require(new['verifier_sha256']==sha(body(S/'verify_exact.py')) and old['verifier_sha256']==sha(body(V/'verify_exact.py')),'fixture verifier binding')
r=json.loads(body(S/'verification_results/actual_run_receipt.json'))
require(r['all_pass'] and r['intentional_controls_rejected']==12 and len(r['actual_subprocesses'])==18,'actual runner')
require(len(r['verification_reports'])==2 and len(r['historical_scratch_replays'])==4,'run modes')
for mode in r['verification_reports']:
    require(mode['total_checks']==2727845 and mode['formula_parameter_cases']==397 and mode['tree_formula_parameter_cases']==74997,'current counts')
    require(mode['verifier_sha256']==sha(body(S/'verify_exact.py')) and mode['paper_sha256']==m['paper_sha256'],'actual code/paper binding')
require(r['runner_sha256']==sha(body(S/'run_checks.py')),'runner hash')
failed=[x for x in r['actual_subprocesses'] if x['expected_exit']==1]
require(len(failed)==12 and all(x['actual_exit']==1 and x['expected_guard_present'] for x in failed),'intended failures')
require(all(x['actual_exit']==x['expected_exit'] for x in r['actual_subprocesses']),'all actual exits')
w=json.loads(body(S/'verification_results/runner_execution.json'))
require(w['exit']==0 and r['actual_operator_PID']==w['actual_runner_PID'],'actual wrapper PID')
for stream in ('stdout','stderr'):
    b=body(S/w[stream+'_relative_path']); require(len(b)==w[stream+'_bytes'] and sha(b)==w[stream+'_sha256'],'wrapper stream pin')
oldqa_path=A/'ROOT_PDF_BUILD_V1_QA_20261006.json'; oldqa=json.loads(body(oldqa_path))
tex=body(S/'root_dependent_spanning_trees.tex'); pdf=body(A/'publication_build_v1/root_dependent_spanning_trees.pdf')
require(sha(tex)==oldqa['source_after_export']['sha256']==m['paper_sha256']=='a0e7e6158267fbf9ca4cafbd5ccb4cfa4ac79a1e0aea61282c9ee09d7e8d11d5','TeX continuity')
require(sha(pdf)==oldqa['PDF']['sha256']=='f51acb267822dd082fdb28a14bc581b37fc3b3a75008647a3e04fa8a3d84fbf4','PDF continuity')
require(oldqa['all_actual_page_images_inspected_by_root'] and not oldqa['layout_concerns'],'original visual QA')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
qa=dict(oldqa); qa.update({'continuity_UTC':utc,'continuity_actual_operator_PID':os.getpid(),'current_source_revision':'publication_package_v2','current_source':pin(S/'root_dependent_spanning_trees.tex'),'original_V1_QA_receipt':pin(oldqa_path),'original_compilation_export_and_render_reused_without_rerun':True,'TeX_and_PDF_bytes_unchanged':True,'fresh_V2_whole_package_R2_pending':True,'publication_clearance':False,'scope':'Unchanged TeX/PDF continuity; original compiler/export/render and four-page inspection remain valid. No new compilation or new visual inspection claimed here.'})
(A/'ROOT_PDF_UNCHANGED_V2_CONTINUITY_20261006.json').write_text(json.dumps(qa,indent=2)+'\n')
auth={'schema':'pr108-root-corrected-source-V2-authentication/v1','UTC':utc,'actual_operator_PID':os.getpid(),'source_manifest_sha256':sha(mb),'source_manifested_files_verified':36,'all_byte_pins_match':True,'V1_source_unchanged':True,'TeX_metadata_historical_byteidentical':True,'fixture_mathematical_data_identical_to_V1':True,'only_fixture_differences':sorted(omit),'fixture_current_provenance_bound':True,'normal_optimized_checks_each':2727845,'actual_intended_failures':12,'actual_subprocesses':18,'historical_replays':4,'root_changed_code_diff_and_current_docs_read':True,'root_reexecution_pending_in_outer_assembly':True,'F01_repaired_at_source_level':True,'whole_package_R2_complete':False,'publication_clearance':False,'original_effort':'2/5; original structured ledger absent','new_central_proof_search_turns':0}
(A/'ROOT_PUBLICATION_SOURCE_V2_AUTHENTICATION_20261006.json').write_text(json.dumps(auth,indent=2)+'\n')
print(json.dumps(auth))
