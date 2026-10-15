#!/usr/bin/env python3
"""Read-only final recheck of inputs; write only this review's authored outputs."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

R = Path(__file__).resolve().parent
W = R.parent
K = W / 'preprint_package_v03'
C = W / 'scoped_candidate/attempts/30000170'
PIN_K = '197df0ea3d83b19c29e0fcd3548fc309db2c8844e5096b1434c8b82e526d85e2'
PIN_C = 'c2ea92f1638dfafbd2d17e3600c0ef1951f866cf4eaeaa4f71fd6c0ea4d713b3'
UTC = datetime.now(timezone.utc).isoformat()

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def write_json(name, value):
    (R / name).write_text(json.dumps(value, indent=2) + '\n')

def recheck(root, manifest_name, pin, key):
    path = root / manifest_name
    assert digest(path) == pin
    manifest = json.loads(path.read_bytes())
    names = set()
    rows = []
    for row in manifest[key]:
        rel = row['path']
        assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
        assert rel not in names
        names.add(rel)
        target = root / rel
        assert not target.is_symlink()
        content = target.read_bytes()
        assert len(content) == row['bytes']
        assert sha256(content).hexdigest() == row['sha256']
        rows.append({'path':rel, 'bytes':len(content), 'sha256':sha256(content).hexdigest()})
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    assert actual == names | {manifest_name}
    return manifest, rows

km, krows = recheck(K, 'PACKAGE_MANIFEST.json', PIN_K, 'files')
cm, crows = recheck(C, 'CANDIDATE_MANIFEST.json', PIN_C, 'payload')
assert all((K / row['path']).stat().st_mode & 0o222 == 0 for row in krows)
external = []
for row in cm['root_decision_and_review_pins']:
    path = Path(row['path'])
    assert path.stat().st_size == row['bytes'] and digest(path) == row['sha256']
    external.append(row)
write_json('FINAL_INPUT_RECHECK.json', {
    'UTC':UTC, 'status':'PASS',
    'package_root':str(K), 'package_manifest_sha256':PIN_K,
    'package_files':len(krows), 'package_total_bytes':sum(x['bytes'] for x in krows),
    'package_exact_file_inventory':True, 'package_selected_bodies_read_only':True,
    'candidate_root':str(C), 'candidate_manifest_sha256':PIN_C,
    'candidate_payload_files':len(crows), 'candidate_total_bytes':sum(x['bytes'] for x in crows),
    'candidate_exact_file_inventory':True, 'external_candidate_pins_matched':len(external),
    'package_selected_bodies':krows, 'candidate_selected_bodies':crows,
    'external_candidate_pins':external,
    'input_mutations':[],
})
write_json('VERDICT.json', {
    'schema':'pr263-whole-preprint-independent-review02-v1', 'UTC':UTC,
    'reviewer':'NEW second whole-preprint adversary',
    'original_PR_head':'c4eff3253932a504f8e558c8b5f5b1b5e155de0f',
    'package_manifest_sha256':PIN_K, 'candidate_manifest_sha256':PIN_C,
    'verdict':'NO_MATERIAL_DEFECT_FOUND',
    'direct_credited_unrefereed_note_recommendation':'GO',
    'required_material_repairs':[],
    'claims_independently_reviewed':[
        'Theorem1: monic/full coefficient set prox-regularity fails for each fixed SPD metric',
        'Theorem1: arbitrarily close unstable inputs with distinct attained GLOBAL nearest stable coefficient polynomials',
        'Theorem1: whole-epigraph set prox-regularity fails for each fixed joint SPD metric, including mixed coefficient/height metrics',
        'Remark2: exact closed stability chart and edge cases; real monic orthant contrast',
        'Proposition3: Euclidean monic function prox-regularity relative to every finite limiting subgradient; v0-dependent constants and strict support',
    ],
    'preceding_D1_delivery_repair_verified':True,
    'candidate_current_claim_alignment':'PASS at the stated semantic read extents',
    'all_package_archive_hashes_and_duplicate_bindings':'PASS',
    'supplied_verifier_stdout_files_byte_exact':True,
    'hash_checker':'PASS exact object; no supplied expected stdout file exists',
    'independent_controls':'PASS', 'PDF_all_six_pages_visual_review':'PASS',
    'primary_sources':'Bounded actual extents in PRIMARY_READ_EXTENTS.json; no unread-body absence inference',
    'source_priority_or_present_openness_clearance':'HOLD / not asserted',
    'no_explicit_nearest_pair_claimed':True,
    'remaining_limits':[
        'Named unread/inaccessible primary bodies and OCR/visual limits',
        'No firstness, exhaustive-priority or present-openness conclusion',
        'No all-degree or real-only general theorem',
        'Primary PRT2000 global projection equivalence used, not independently reproved',
        'Finite numerical controls are not interval-certified or universal proofs',
        'AI adversarial review is not human peer review or formal proof-assistant certification',
    ],
    'assigned_review_completion_percent':100,
    'publication_authorization_or_provider_action':False,
    'external_contacts_or_outreach':False,
    'shared_or_primary_Git_mutations':False,
    'authored_report':'WHOLE_PREPRINT_REVIEW.md',
    'independent_derivations':'COLD_ANALYTIC_CHECKS.md',
})
log = R / 'RESEARCH_LOG.md'
marker = 'Checkpoint 3, final exact-version review completion estimate 100%'
assert marker not in log.read_text()
with log.open('a') as out:
    out.write(f'\n- {UTC} — {marker} of this assigned adversarial review, not of exhaustive priority research. Full report and independent analytic derivations completed. Final recheck reconfirms all21 package-selected bodies(287,853 bytes), exact22-file inventory, frozen manifest pin and read-only modes; all23 candidate payloads(136,023 bytes), exact24-file inventory and11 external pins remain byte-identical. Verdict: NO MATERIAL DEFECT FOUND; GO for the carefully credited direct unrefereed note at this exact version. Required material repairs: none. Firstness/exhaustive priority/current openness remain unclaimed. Authored checkpoint selection excludes private reading extracts, all PDF renders and copied archive members. No input/Git/provider/contact/publication mutations.\n')

names = [
    'WHOLE_PREPRINT_REVIEW.md', 'COLD_ANALYTIC_CHECKS.md', 'RESEARCH_LOG.md',
    'VERDICT.json', 'FINAL_INPUT_RECHECK.json', 'PACKAGE_CHECKS.json',
    'CANDIDATE_AND_REPAIR_CHECKS.json', 'INDEPENDENT_CONTROLS.json',
    'PRIMARY_READ_EXTENTS.json', 'PDF_LINKS.json', 'SECOND_RUNTIME_REPLAY.json',
    'SOURCE_BINDING_CHECKS.json', 'audit_package.py', 'independent_symbolic_controls.py',
    'source_binding_check.py', 'finalize_review.py', 'verify_exact.py.stdout',
    'verify_function_boundary.py.stdout', 'check_archive_hashes.py.stdout',
]
actual_root = {p.name for p in R.iterdir() if p.is_file()}
assert actual_root == set(names)
rows = [{'path':name, 'bytes':(R/name).stat().st_size, 'sha256':digest(R/name)} for name in names]
write_json('REVIEW_MANIFEST.json', {
    'schema':'pr263-whole-preprint-review02-authored-checkpoint-v1', 'UTC':UTC,
    'review_root':str(R), 'package_manifest_sha256':PIN_K, 'candidate_manifest_sha256':PIN_C,
    'selected_authored_outputs':rows,
    'selected_authored_output_count':len(rows),
    'selected_authored_total_bytes':sum(x['bytes'] for x in rows),
    'manifest_self_excluded':True,
    'excluded_private_or_copy_directories':[
        {'path':'private_reading_text', 'reason':'Third-party body extracts and manuscript extraction; private inspection copies'},
        {'path':'private_reading_visuals', 'reason':'All manuscript and primary-source PDF renders; private visual inspection copies'},
        {'path':'independent_archive_extraction', 'reason':'Copies of delivered ZIP members, independently checked but not newly authored review outputs'},
    ],
    'primary_corpus':'Existing private corpus originals stay outside this authored review selection',
    'all_remaining_root_files_selected':True,
    'verdict':'NO_MATERIAL_DEFECT_FOUND / GO for scoped direct credited note',
    'priority_clearance':'No firstness/current-openness/exhaustive-priority certification',
    'assigned_review_completion_percent':100,
})
print(json.dumps({'status':'PASS', 'UTC':UTC, 'selected_authored_outputs':len(rows),
                  'review_manifest_sha256':digest(R/'REVIEW_MANIFEST.json'),
                  'report_sha256':digest(R/'WHOLE_PREPRINT_REVIEW.md'),
                  'analytic_checks_sha256':digest(R/'COLD_ANALYTIC_CHECKS.md'),
                  'verdict_sha256':digest(R/'VERDICT.json')}, indent=2))
