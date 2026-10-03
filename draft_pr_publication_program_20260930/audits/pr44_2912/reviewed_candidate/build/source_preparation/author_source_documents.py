#!/usr/bin/env python3
"""Own source authoring and full-byte input classification; no production execution."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat

FAMILY = Path(__file__).absolute().parent
AUDIT = FAMILY.parent
REPO = AUDIT.parents[2]
TEMPLATE = REPO / 'draft_pr_publication_program_20260930/audits/pr43_30004386/current_preparation_family'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(obj): return (json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode()
def raw(path):
    assert not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
    assert stat.S_ISREG(path.stat().st_mode)
    return path.read_bytes()
def row(path, root=AUDIT):
    body=raw(path)
    return {'path':path.relative_to(root).as_posix(),'bytes':len(body),'sha256':sha(body)}
def write(name, body):
    path=FAMILY/name
    assert not path.exists()
    path.write_bytes(body if type(body) is bytes else body.encode())

FLAGS = [
 'original18_science_helpers_results_metadata_and_complete19_path_diff_fully_read',
 'operative_primary_target_categories_and_relevant_proofs_fully_read',
 'both_realization_gaps_and_no_novelty_disposition_accepted',
 'whole_raw_SQL_and_prior_presence_actual_evidence_fully_read',
 'unchanged_author507_and_independent29933_actual_reproductions_fully_read',
 'both_closed_independent_families_fully_read',
 'first_party_closures_and_individual_foreign_exclusions_mechanically_checked',
 'standard_conditional_deductions_only_scoped_partial_accepted',
 'new_source_adversary_closed_clean_complete_report_personally_read',
]
family_data={}
for name, mf, expected in [
 ('duality_algebra_family','AUTHORSHIP_MANIFEST.json','83dcad444a56274472224bbb58dec268ded92ac2042ddabe8fee7851626acb81'),
 ('literal_realization_family','SELF_ONLY_CLOSURE.json','6e656761b9c7938aa8901157706dcf9587e627903ee0dbac1b20eaa2be0dea40')]:
    directory=AUDIT/name
    manifest=raw(directory/mf)
    assert sha(manifest)==expected
    value=json.loads(manifest)
    own=value['files'] if name=='duality_algebra_family' else value['authored_members']
    own_names={x['path'] for x in own}
    assert len(own_names)==(54 if name=='duality_algebra_family' else 13)
    all_names={p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}
    assert not any(p.is_symlink() for p in directory.rglob('*'))
    own_rows=[]; foreign_rows=[]
    for path in sorted(all_names):
        entry=row(directory/path, directory)
        if path in own_names:
            original=next(x for x in own if x['path']==path)
            assert entry['bytes']==original['bytes'] and entry['sha256']==original['sha256']
            assert stat.S_IMODE((directory/path).stat().st_mode)==0o444
            own_rows.append(entry)
        elif path!=mf:
            foreign_rows.append(entry)
    assert stat.S_IMODE((directory/mf).stat().st_mode)==0o444
    external=[]
    if name=='duality_algebra_family':
        assert {x['path'] for x in value['foreign_local_members_individually_excluded']} == {x['path'] for x in foreign_rows}
        for original in value['foreign_local_members_individually_excluded']:
            entry=next(x for x in foreign_rows if x['path']==original['path'])
            assert entry['bytes']==original['bytes'] and entry['sha256']==original['sha256']
        for original in value['external_parent_original_inputs']:
            path=Path(original['path'])
            entry=row(path)
            assert entry['bytes']==original['bytes'] and entry['sha256']==original['sha256']
            external.append(entry)
    else:
        foreign_manifest=json.loads(raw(directory/'FOREIGN_EVIDENCE_MANIFEST.json'))
        assert len(foreign_manifest['foreign_evidence'])==len(foreign_rows)==54
        assert {x['path'] for x in foreign_manifest['foreign_evidence']} == {x['path'] for x in foreign_rows}
        for original in foreign_manifest['foreign_evidence']:
            entry=next(x for x in foreign_rows if x['path']==original['path'])
            assert entry['bytes']==original['bytes'] and entry['sha256']==original['sha256']
    family_data[name]={'manifest':row(directory/mf,directory),'copied_members':own_rows,
                       'foreign_members':foreign_rows,'external_inputs':external,
                       'directories':[p.relative_to(directory).as_posix() for p in sorted(directory.rglob('*')) if p.is_dir()]}

aux_names=['snapshot_manifest_v2.json','original_diff_v2.patch','export_original_snapshot.py',
           'export_original_snapshot_v2.py','PRELAUNCH_EXPORT_SOURCE.py','PRELAUNCH_EXPORT_SOURCE_V2.py',
           'ORIGINAL_GIT_COMMANDS.json','ORIGINAL_GIT_COMMANDS_V2.json','capture_root_command.py']
for directory in ['original_git_commands','original_git_commands_v2',
                  'root_original_export_actual_capture','root_original_export_v2_actual_capture',
                  'root_original_branch_fetch_actual_capture','root_live_PR_metadata_actual_capture']:
    aux_names.extend(p.relative_to(AUDIT).as_posix() for p in sorted((AUDIT/directory).rglob('*')) if p.is_file())
auxiliary=[row(AUDIT/name) for name in sorted(set(aux_names))]
snapshot=json.loads(raw(AUDIT/'snapshot_manifest_v2.json'))
for item in snapshot['files']:
    entry=row(AUDIT/'source_snapshot_v2'/item['path'])
    assert entry['bytes']==item['size'] and entry['sha256']==item['sha256']
    assert raw(AUDIT/'source_snapshot'/item['path'])==raw(AUDIT/'source_snapshot_v2'/item['path'])
    assert stat.S_IMODE((AUDIT/'source_snapshot_v2'/item['path']).stat().st_mode)==0o444
source_read={p:row(AUDIT/'source_snapshot_v2'/p) for p in [x['path'] for x in snapshot['files']]}
assert raw(AUDIT/'source_snapshot_v2/verify_group_block.py')==raw(AUDIT/'source_snapshot_v2/review/submitted_verifier.py')
assert raw(AUDIT/'source_snapshot_v2/group_block_verification.json')==raw(AUDIT/'source_snapshot_v2/review/submitted_results.json')
assert raw(AUDIT/'source_snapshot_v2/OBSTRUCTION.md')==raw(AUDIT/'source_snapshot_v2/review/reviewed_obstruction.md')
write('STATIC_INPUT_BINDINGS.json',dump({'schema':'PR44_FIXED_CURRENT_SOURCE_INPUTS_v1',
 'status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING','snapshot_manifest':row(AUDIT/'snapshot_manifest_v2.json'),
 'families':family_data,'auxiliary':auxiliary,'original18':source_read,
 'template_source':row(TEMPLATE/'prepare_current_packet.py',REPO),
 'template_operator':row(TEMPLATE/'capture_root_builder_operation.py',REPO),
 'no_ROOT_mutable_logs_or_native_preimages_bound_as_timeless':True}))

prefix=raw(TEMPLATE/'prepare_current_packet.py').decode().split('def build(args, script, audit, repo, attempt):')[0]
prefix=prefix.replace('PR43','PR44').replace('86be0f85c7a37a5cad8d24abd16a32d8d1f27e62','c772dc5b851ec91da9d46d534577609e5d3ca389').replace('60292bed09f59236aa192cb17aa138f7b4750e1a','01358d66fc67d1c462bddf31c0d4ee5b120e6737')
start=prefix.index('FINAL_SOURCE ='); end=prefix.index('HEADER =')
prefix=prefix[:start]+"SCIENCE = '69a3ffb7b6c2ba3bf1a4df8d7d83960d66095db9d175d78cfe49e2324aac1a71'\nGATE = 'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'\nFLAGS = "+repr(FLAGS)+'\n'+prefix[end:]
start=prefix.index('IMMUTABLE ='); end=prefix.index('\n\ndef require',start)
immutable=['OBSTRUCTION.md','SOURCES.md','group_block_verification.json','source_manifest.json','source_record.json','turns.jsonl','verify_group_block.py','review/submitted_verifier.py','review/submitted_results.json','review/reviewed_obstruction.md','review/independent_checks.py','review/independent_results.json']
prefix=prefix[:start]+'IMMUTABLE = '+repr(immutable)+prefix[end:]
core=raw(FAMILY/'BUILDER_BODY.source.txt').decode()
tail=raw(TEMPLATE/'prepare_current_packet.py').decode().split('def main():\n')[1]
tail='def main():\n'+tail
tail=tail.replace('PR43','PR44').replace('pr43_30004386','pr44_2912').replace('root_pr43','root_pr44')
tail=tail.replace("'root-current-input-manifest']", "'root-current-input-manifest', 'root-evidence-bindings']")
tail=tail.replace('four genuine prerequisite', 'five genuine prerequisite')
write('prepare_current_packet.py',(prefix+core+'\n\n'+tail).encode())
operator=raw(TEMPLATE/'capture_root_builder_operation.py').decode().replace('PR43','PR44').replace('pr43_30004386','pr44_2912').replace('root_pr43','root_pr44')
operator=operator.replace("'root-current-input-manifest']", "'root-current-input-manifest', 'root-evidence-bindings']")
operator=operator.replace("'root_current_input_manifest']", "'root_current_input_manifest', 'root_evidence_bindings']")
operator=operator.replace('four real','five real')
write('capture_root_builder_operation.py',operator.encode())

qualification='''# Current PR44 science and provenance qualifications

PR44 / 2912 / KP-4.36 remains unsolved. The preserved mathematical note gives standard conditional deductions, no novel theorem, no full positive answer, and no same-full-2-type counterexample among actual smooth or locally flat PL 2-knot exteriors in S4. The full unmarked triple includes the group, its action on pi2, and the first k-invariant. Neither a chosen meridian nor boundary pair data are included in the source invariant.

The duality formula uses finite-support group-ring cohomology, relative boundary cohomology and the inversion converting right modules to left cover-homology modules. Its kernel depends on the meridional inclusion. A relative-degree-one map of pairs inducing pi1 and pi2 isomorphisms is sufficient; no such pair map or compatible boundary-sphere/meridian datum has been produced from the unmarked full 2-type. This route stops at realization.

The explicit amalgam calculation is for (G,<t>). The nonzero quotient is Z[G]^C/Z[G]^A, with each integral finite block Z^7/Z(1,...,1) of rank six. This quotient cannot be replaced by the augmentation lattice integrally. Geometric identification of t as the meridian of an actual source-category exterior is an additional condition. Normal generation, weight-one and a known abstract knot-group presentation do not establish that identification for an existing exterior or give two actual exteriors with equal full triples. The second route stops before geometric realization and comparison.

Lomonaco's known completeness theorem requires both third-cover homology groups zero. Infinite ends alone do not imply non-quasi-asphericity. Hillman's group is printed p.277; his locally flat surgery statements do not automatically certify the source's smooth/PL category. Jablonowski's inspected theorem has inequivalent first k-invariants and hence different full 2-types. Conway-Kasprowski's inspected theorems require boundary pi1 surjectivity, forcing a 2-knot group cyclic, hence Z. Their additional hypotheses are retained. These are credits and limitations, not project discoveries.

The 1983 Gonzalez-Acuna--Montesinos full proof was not read: only its indexed primary opening was accessible, while direct retrieval returned verification HTML. No standard algebraic deduction relies on its inaccessible construction. Source searches and arXiv version checks are dated and bounded; they do not prove exhaustive priority, current universal literature absence or the fact that the original problem remains open.

All original18 files are byte-exact archives. Original metadata, source-search dates, model/reasoning/deadline claims, historical PASS labels, 507 and 29,933 execution claims, and pending/completed-review sentences remain dated attributions. Current approval never transfers those labels. Genuine ROOT replays authenticate unchanged source/results now, not September30 execution. Current model, reasoning, deadline and verdict are explicitly null. Finite arithmetic checks do not prove duality, group cohomology, exterior realization or homotopy classification.

Original substantive turns remain two out of five; new substantive attempts and audit turns are zero. The failed V1 ROOT filename-guess export is preserved and qualified; V2 is operative, with the actual branch base 01358d66fc67d1c462bddf31c0d4ee5b120e6737. Immutable mathematical bodies and helper sources are untouched. New whole-current review is PENDING until a separate new adversary and ROOT complete it.

AI tools were used extensively. The work is unrefereed and has no claimed human peer review or formal certification. Acceptance, if completed, is a repository report of standard partial deductions with both exact gaps, not a paper, new DOI or tracker row. Foreign PDFs, extracted source text and page pixels remain individually hash-bound and excluded from authored copies and publication. Kirby's PDF expressly forbids reposting without permission; its PDF, text and renders are not included.

Dated native queue/inventory/state/history bindings in old evidence are historical bodies, never timeless current authority. ROOT must separately approve and check a fresh13 native manifest and actual current main HEAD before and after the administrative freeze. Global qualifications apply to every current presentation and metadata file; exact historical scientific/source bodies remain linked with these qualifications.
'''
write('SOURCE_PRECISION_QUALIFICATIONS.md',qualification)
write('CURRENT_OVERVIEW.md','''# PR44 / Kirby4.36: standard partial deductions, unsolved

The full problem is unresolved by this work. The unchanged obstruction note records a standard meridional restriction-kernel formula, a sufficient degree-one pair-map criterion and a nonzero integral kernel for the specified abstract group pair. Both realization gaps remain. No novelty is claimed.

Read SOURCE_PRECISION_QUALIFICATIONS.md and CURRENT_OBSTRUCTION_CONTEXT.md with OBSTRUCTION.md. Original18 files and old review/results/metadata are preserved in original_archive/. Actual ROOT evidence and two independent source/math families are separate. NEW whole-current review: PENDING. Original2/5; new0; audit0. Paper/new DOI/tracker: false.
''')
write('DRAFT_ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','''# DRAFT ROOT PR44 scoped partial acceptance

All ROOT reading and source safety are PENDING. Do not substitute this draft for ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md. Required completed first line: # ROOT PR44 scoped standard-partial acceptance. Required standalone marker: ROOT_SCOPE_ACCEPTED_STANDARD_PARTIAL_ONLY.
PR44 / 2912 / KP-4.36
Status: unsolved
Original turns: 2/5; new: 0; audit: 0
Full problem solved: false
Novelty: false
NEW whole-current review: PENDING
Paper/new DOI/tracker: false
''')
common={'created_utc':None,'reading_completed':False,'root_flags':dict.fromkeys(FLAGS,False),
 'reading_notes':None,'scope_certificate_sha256':None,'preparation_manifest_sha256':None,
 'source_qualification_sha256':None,'evidence_bindings_sha256':None,
 'family_manifest_sha256':{k:v['manifest']['sha256'] for k,v in family_data.items()},
 'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0}
write('DRAFT_ROOT_READ_LEDGER.json',dump(dict(common,schema='PR44_ROOT_PRIMARY_READ_LEDGER_v1')))
write('DRAFT_ROOT_SCIENCE_CARD.json',dump(dict(common,schema='PR44_ROOT_SCIENCE_CARD_v1',status='unsolved',
 partial_valid=False,full_problem_solved=False,novelty_claimed=False,turn_limit=5,
 paper_created=False,new_DOI_created=False,tracker_row_created=False,read_ledger_sha256=None,
 current_input_manifest_sha256=None,new_whole_current_gate='PENDING',current_model=None,
 current_reasoning_effort=None,current_deadline_utc=None,current_verdict=None)))
write('DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json',dump({'schema':'PR44_ROOT_FRESH13_INPUT_PREIMAGES_v1',
 'approved_by_root':False,'created_utc':None,'reason':None,'current_head':None,'files':[],
 'draft_has_no_native_preimages_or_current_HEAD':True}))
write('DRAFT_ROOT_EVIDENCE_BINDINGS.json',dump({'schema':'PR44_ROOT_EVIDENCE_BINDINGS_v1',
 'approved_by_root':False,'created_utc':None,'notes':None,'manifest':None,'proof_notes':None,'summary':None,
 'draft_does_not_approve_or_claim_future_ROOT_evidence':True}))
write('SOURCE_STATUS.json',dump({'schema':'PR44_SOURCE_ONLY_PREPARATION_STATUS_v1',
 'production_builder_executed':False,'production_operator_executed':False,
 'ROOT_reading_completed':False,'ROOT_prerequisites_authored':False,'source_adversary_passed':False,
 'whole_current_review_completed':False,'current_gate':'PENDING',
 'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,
 'paper_created':False,'new_DOI_created':False,'tracker_row_created':False}))
write('SOURCE_PREPARATION_RESEARCH_LOG.md',dt.datetime.now(dt.timezone.utc).isoformat()+
 ' — source-only authoring; source preparation70%, full discovery0%. Original18/helpers/results/metadata and both closed scoped family reports read. Future ROOT genuine evidence/read/fresh13 and new source/whole review remain pending. No production execution, native/Git/remote mutation or outreach.\n')
print(json.dumps({'status':'SOURCE_ONLY_DOCUMENTS_AUTHORED','original_files_read_and_bound':18,
 'families':{k:{'own':len(v['copied_members']),'foreign':len(v['foreign_members']),'external':len(v['external_inputs'])} for k,v in family_data.items()},
 'auxiliary_count':len(auxiliary),'production_execution':False},indent=2))
