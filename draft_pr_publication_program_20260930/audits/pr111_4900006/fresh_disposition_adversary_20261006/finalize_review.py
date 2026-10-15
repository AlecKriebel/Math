#!/usr/bin/env python3
"""Record actual local controls and freeze this disposition-only review."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess

D = Path(__file__).resolve().parent
A = D.parent
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
def pin(path, base):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(base)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def write(name, data):
    (D/name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
now = dt.datetime.now(dt.UTC).isoformat()
files = [
    'ROOT_PRIORITY_DISPOSITION_20261006.md',
    'PROPOSED_CLOSURE_COMMENT_20261006.md',
    'original_head_authentication_20261006/SOURCE_STATEMENT.json',
    'original_head_authentication_20261006/PRIOR_REPORT.md',
    'repaired_diagnostics_v2/COUNTEREXAMPLE.md',
    'ROOT_MATHEMATICAL_GATE_20261006.json',
    'priority_cross_family_adjudicator_20261006/REPORT.md',
    'priority_cross_family_adjudicator_20261006/PRIOR_SPECIALIZATION_PROOF.md',
    'priority_cross_family_adjudicator_20261006/RESULT.json',
    'priority_cross_family_adjudicator_20261006/SOURCE_AND_FAMILY_MANIFEST.json',
    'primary_source_scope_adversary_20261006/SOURCE_MANIFEST.json',
]
pins = [pin(A/f,A) for f in files]
expected = {
    'repaired_diagnostics_v2/COUNTEREXAMPLE.md': '0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f',
    'original_head_authentication_20261006/SOURCE_STATEMENT.json': '0608b99bef6677de34d98e2e59e0b05651e4e3af82c14b051ac8a6d443a38688',
    'original_head_authentication_20261006/PRIOR_REPORT.md': 'a92cd3d3b62e90b9e3ad1c12c60b80eb88615b210fd89101aa95298dd5538c2b',
    'ROOT_MATHEMATICAL_GATE_20261006.json': 'bd45c96b065affb146ca7aa32efdfa32791177f4d892960434fa6641610f282d',
}
for item in pins:
    if item['path'] in expected and item['sha256'] != expected[item['path']]:
        raise RuntimeError('Changed reviewed input ' + item['path'])
source_specs = [
    ('primary_source_scope_adversary_20261006/private_primary_sources/parker_goluskin_v2.pdf', 'c8e53fbd26bd51b270deb81cf318161cb14f260ab827a0996d401fee899c6e7c', 'https://arxiv.org/pdf/2510.14870v2', [2,4,5,7,29,30], [2,5,7]),
    ('root_priority_audit_20261006/private_sources/zelik_cascade_author.pdf', '0e7eaa6b186887bf138a8ce0fdd3cdbce0164c9956aaf308e14cd16782029141', 'https://sergey-zelik.co.uk/publications/dlyap.pdf', [10,11,12], [10,11,12]),
    ('primary_source_scope_adversary_20261006/private_primary_sources/eden1989.pdf', 'e01e97ad093660750078ceec33acbeccaa67af3c62437086e48182a34e9f7078', 'https://www.numdam.org/article/M2AN_1989__23_3_405_0.pdf', [408,409,410,411], []),
]
sources = []
for f, digest, url, pages, visuals in source_specs:
    entry = pin(A/f,A)
    if entry['sha256'] != digest:
        raise RuntimeError('Source pin mismatch '+f)
    entry.update({'url':url,'personally_read_printed_pages':pages,'visually_inspected_printed_pages':visuals,'copyright_body_private_and_excluded':True,'retrieval_by_this_fresh_adversary':False,'complete_file_bytes_authenticated':True})
    sources.append(entry)
goal = Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
goal_raw = goal.read_bytes()
write('INPUT_SOURCE_PINS.json', {
    'schema':'pr111-fresh-disposition-input-pins/v1', 'UTC':now, 'actual_metadata_pid':os.getpid(),
    'A111_relative_inputs':pins, 'private_sources':sources,
    'saved_goal':{'path':str(goal),'bytes':len(goal_raw),'sha256':hashlib.sha256(goal_raw).hexdigest(),'fully_read':True},
    'official_records_independently_checked':['https://arxiv.org/abs/2510.14870v2','https://www.aimsciences.org/article/doi/10.3934/cpaa.2008.7.971'],
    'author_publications_index_web_fetch_failed':True,
    'Zelik_exact_author_journal_body_identity_verified':False,
    'PDF_pages_inspected_in_existing_private_renders':True,
    'primary_body_instructions_not_treated_as_user_instructions':True,
})
env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
receipts=[]
for label, flags in [('NORMAL', []), ('OPTIMIZED', ['-O'])]:
    command=[PY,'-E','-S','-B','-P']+flags+[str(D/'verify_disposition_controls.py')]
    proc=subprocess.run(command,cwd=D,env=env,capture_output=True,timeout=30)
    if proc.returncode or proc.stderr:
        raise RuntimeError('Local exact controls failed')
    result=json.loads(proc.stdout)
    if result['status']!='PASS' or result['explicit_guards']!=31:
        raise RuntimeError('Unexpected local controls')
    name='CHECKS_'+label+'.json'
    (D/name).write_bytes(proc.stdout)
    receipts.append({'mode':label,'command':command,'actual_child_pid':result['actual_pid'],'exit_code':proc.returncode,'stderr_bytes':len(proc.stderr),'explicit_guards':result['explicit_guards'],'output':pin(D/name,D),'timeout_seconds':30,'explicit_clean_environment':True})
write('EXECUTION_RECEIPTS.json', {'UTC':now,'actual_parent_pid':os.getpid(),'executions':receipts,'first_unsaved_control_run_actual_pid':44330,'no_native_or_service_operation':True})
write('RESULT.json',{
    'schema':'pr111-fresh-disposition-adversarial-review/v1','UTC':now,'actual_metadata_pid':os.getpid(),'PR':111,
    'original_head':'8a7270989d7064a4b97badecaa4b311db5e6d49f','original_status':'claimed_solved','original_effort':'2/5',
    'verdict':'PASS for exact narrow disposition; no novelty clearance',
    'assigned_review_completion_percent':100,'mathematical_gate_remains_pass':True,
    'mandatory_corrections_remaining':[], 'closure_without_merge_or_solved_problem_publication_defensible':True,
    'already_solved_scope':'Overbroad imported manifold-inclusive target/classical obstruction only; not exact prior publication of entire stronger R5 theorem.',
    'bare_entire_theorem_already_solved_classification_would_pass':False,
    'original_historical_open_problem_resolution_established':False,'substantive_research_novelty_established':False,
    'exact_prior_entire_R5_theorem_authenticated':False,'stronger_entire_R5_mathematical_content_retained':True,
    'manifold_base_scope_independently_confirmed_in_PG_Duffing_example':True,
    'ambient_spectrum':['0','0','0','0','-1'],'ambient_dimension':'4','intrinsic_spectrum':['0','0','-1'],'intrinsic_dimension':'2',
    'linear_extension_entire_space_global_attractor_exists':False,
    'candidate_exact_asymptotic_maximum':'203/50','finite_time_infimum_equality_asserted':False,
    'no_new_central_proof_search_turns':True,'external_human_contact':False,'subdelegation':False,
    'Git_index_ref_service_PR_cache_mutation':False,'native_assessment_performed':False,
    'publication_package_R1_R2_performed':False,'publication_or_merge_clearance':False,'human_peer_review_performed':False,
    'publication_exception_for_PR50_reused':False,'PR107_nothing_new_conditional_applied':False,
    'private_copyright_bodies_in_portable_manifest':False,
    'remaining_access_gaps':['Original1989 thesis','Eden-Foias-Temam1991 body','Eden1990 body','Leonov-Lyashko1993 body','Relevant complete2020 dimension-book chapter','Zelik exact journal-body identity'],
})
(D/'RESEARCH_LOG.md').write_text('# Fresh disposition adversary research log\n\n'+now+' - 100% of assigned bounded review complete. Read the exact proposed root disposition and closure comment, immutable imports, v2 theorem, mathematical gate, cross-family final proof/report and saved goal. Independently inspected PG and Zelik operative pages; PG base Duffing manifold independently confirms ambient convention. Rejected phase/tangent conflation and entire-space linear-attractor implication. Stronger R5 theorem retained, exact prior and research novelty unestablished. PASS for the exact narrow closure/classification; no mandatory correction. Actual normal and optimized exact controls each passed31 explicit guards. No Git, service, PR, cache or outside-human action. No new central proof search. Portable source pins exclude copyright bodies.\n')
members=[]
for path in sorted(D.iterdir()):
    if path.is_file() and path.name != 'OUTPUT_MANIFEST.json':
        members.append(pin(path,D))
write('OUTPUT_MANIFEST.json', {'schema':'pr111-fresh-disposition-portable-manifest/v1','UTC':now,'members':members,'private_copyright_bodies_excluded':True,'self_excluded':True})
manifest=json.loads((D/'OUTPUT_MANIFEST.json').read_bytes())
for member in manifest['members']:
    if pin(D/member['path'],D)!=member:
        raise RuntimeError('Output manifest changed')
print(json.dumps({'status':'PASS','UTC':now,'actual_pid':os.getpid(),'manifest':pin(D/'OUTPUT_MANIFEST.json',D),'report':pin(D/'REPORT.md',D),'result':pin(D/'RESULT.json',D),'members':len(members),'actual_control_child_pids':[r['actual_child_pid'] for r in receipts]},indent=2))
