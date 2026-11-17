"""Distinct V2 reader: actual Fano root directory row; preserved V1 failure unchanged."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P / 'verification'
now = datetime.now(timezone.utc).isoformat()

def info(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(),
            'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

def external(path):
    return {'path': str(path), **info(path)}

def new(path, obj):
    with path.open('x') as stream:
        json.dump(obj, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())

def authenticate(name, counts, pins, exclusions):
    root = V / name
    for leaf, digest in pins.items():
        assert info(root / leaf)['SHA256'] == digest, (name, leaf)
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    rows = manifest.get('entries', manifest.get('payload_files'))
    assert isinstance(rows, list)
    actual_files, actual_dirs = {}, {'.': root}
    for folder, dirs, files in os.walk(root, followlinks=False):
        for leaf in dirs:
            path = Path(folder) / leaf
            assert stat.S_ISDIR(path.lstat().st_mode)
            actual_dirs[str(path.relative_to(root))] = path
        for leaf in files:
            path = Path(folder) / leaf
            assert stat.S_ISREG(path.lstat().st_mode)
            actual_files[str(path.relative_to(root))] = path
    assert (len(actual_files), len(actual_dirs) - 1) == counts
    if 'root_mode' in manifest:
        root_mode = manifest['root_mode']
    else:
        assert manifest['schema'] == 'finite-private-fano-editorial-manifest-v1'
        root_rows = [row for row in rows if row.get('kind') == 'directory' and row['path'] == '.']
        assert len(root_rows) == 1
        root_mode = root_rows[0]['mode']
    assert int(root_mode, 8) == stat.S_IMODE(root.stat().st_mode)
    file_rows = [row for row in rows if row.get('kind', 'file') == 'file']
    assert len({row['path'] for row in file_rows}) == len(file_rows)
    assert {row['path'] for row in file_rows} | exclusions == set(actual_files)
    for row in rows:
        namepath = Path(row['path'])
        assert not namepath.is_absolute() and '..' not in namepath.parts
        if row.get('kind') == 'directory':
            path = actual_dirs[row['path']]
            assert row.get('empty', not any(path.iterdir())) == (not any(path.iterdir()))
        else:
            path = actual_files[row['path']]
            actual = info(path)
            if 'SHA256' in row:
                assert (actual['bytes'], actual['SHA256']) == (row['bytes'], row['SHA256'])
            else:
                assert row['path'] in exclusions and row['path'] in pins
                assert isinstance(row['content_hash_exclusion'], str)
            if 'empty' in row:
                assert row['empty'] == (actual['bytes'] == 0)
            if 'hidden' in row:
                assert row['hidden'] == any(p.startswith('.') for p in namepath.parts)
        assert stat.S_IMODE(path.lstat().st_mode) == int(row['mode'], 8)
    for leaf, mode in manifest.get('terminal_modes', {}).items():
        assert stat.S_IMODE((root / leaf).stat().st_mode) == int(mode, 8)
    return {'path': str(root.relative_to(P)), 'files': counts[0],
            'child_directories': counts[1],
            'external_controls': {leaf: info(root / leaf) for leaf in pins}}

checkpoint = authenticate('checkpoint-fanoPASS146-twoINITIALs-20261117', (54, 0), {
    'FINAL.json': 'b3c58560565ee1e8db2de4fae2b5ecc35dcf3d9f6139d67068fb6d50e4bb46a9',
    'MANIFEST.json': '718e5e281dac725f472b0cb526cff89210e23684e56500ab0966f5a019506968',
    'REPORT.md': 'c65a3ee50fc7070456421413b9117dbe95487b4f054b1193e4c2b0b0d450690d',
    'FINAL_CHECKS.json': '891b5b46e8eccd0bbb58237032271bd57ab996e99ae87ac0da844cd30e6b6b26'
}, {'MANIFEST.json', 'FINAL.json'})
source = authenticate('gram-thompson-d4-production-prepare-v3-sol-20261117', (14, 0), {
    'FINAL.json': '9aa6c07efcbb920c860e9d5865dfd615829e8da0aac5531f6c2de5f534a23642',
    'MANIFEST.json': '29f3fc34d825d03098148f0b3b2d8e16284451b3b83536dad553a7f014fc7fc4',
    'SEAL.json': 'e219bd8dae98662e7f45397a07c49988e4de75fae1618a70677229bcd1131492'
}, {'MANIFEST.json', 'SEAL.json'})
audit = authenticate('gram-thompson-d4-production-v3-static-audit-sol-20261117', (10, 0), {
    'FINAL.json': 'd95fc1b6a101f2aa4443a18badc36fd33422e41a3c393409a51e4107cd26442c',
    'MANIFEST.json': 'd616e509ac8ed5678e03769d0390c84af05d4949038aaeaf6e98c9283d2a0e69'
}, {'MANIFEST.json', 'FINAL.json'})
editorial = authenticate('fano-rank-two-editorial-sol-20261117', (18, 1), {
    'FINAL.json': 'dfc5927e3bef7a8856f6aff3e8754fbb9f79726a84214b14117b85b09c2ef9c4',
    'MANIFEST.json': '6ba6ab0d4275301250d175a5f92062a1455533e64d3294753967be150772ee29'
}, {'MANIFEST.json'})
C = V / checkpoint['path'].split('/')[-1]
checks = json.loads((C / 'FINAL_CHECKS.json').read_text())
assert checks['commit'] == '164a569600dd415f65d7d377541d1485fc43a904'
assert checks['parent'] == '436ec422f9ae291a365b9ff2814cb88bc15db8f3'
assert checks['tree'] == '74821f3c2c13ea3fc6f52d9b04f8d0f0250ae171'
assert checks['changed_paths'] == 274 and checks['durable_closures'] == 88 and checks['key_files'] == 251
assert checks['all159siblings_docs_exact'] and checks['whole_native_and_public_guards_equal']
runs = json.loads((C / 'RUNS.json').read_text())
assert len(runs) == 6 and all(row['exit_code'] == 0 for row in runs)
cp_out = V / 'root-checkpoint-164a56-adoption-20261117.json'
source_out = V / 'root-gram-thompson-d4-v3-source-adoption-20261117.json'
page_out = V / 'root-fano-rank-two-editorial-adoption-20261117.json'
new(cp_out, {'UTC': now, 'status': 'ACCEPTED_SCOPED_CHECKPOINT',
             'commit': checks['commit'], 'parent': checks['parent'], 'tree': checks['tree'],
             'packet': checkpoint, 'all54_payloads_individual_modes_terminal_controls_exact': True,
             'root_full_actual_REPORT_FINAL_FINAL_CHECKS_and_six_RUNS_read': True,
             'all_six_runs_exit0': True, 'changed_paths': 274,
             'durable_closures': 88, 'key_files': 251,
             'all159siblings_docs_nativeM_W_and_public_unchanged_in_checkpoint': True,
             'two193_original_INITIALs_opaque_checkpointed': True,
             'scientific_reviewed': 146, 'native_reviewed_at_checkpoint_snapshot': 145,
             'programme_complete': False})
N = V / source['path'].split('/')[-1]
A = V / audit['path'].split('/')[-1]
helper_pin, plan_pin = external(N / 'release_overlay.py'), external(N / 'PLAN.json')
assert helper_pin['SHA256'] == 'db93c08a28775a06c3925e60dac8d2732724c71ec62d2752083a56e1bf65c038'
assert plan_pin['SHA256'] == 'f01b666bfd446e7ea10c1a8694bacd2d2046af1800c77ead0ecb25b620492137'
resolution = {
    'classification': 'ALL_ACTUAL_FINDINGS_RESOLVED_FOR_EXACT_ARTIFACT',
    'all_actual_criteria_accepted': True,
    'root_personally_read_complete_artifact_and_audit': True,
    'rationale': 'Root read the actual whole1709line source,231line PLAN, complete31/20line diffs, complete V3 static REPORT/FINDINGS/FINAL and producer REPORT/FINAL/SEAL. The bounded static audit and actual source resolve stream finally capture, journal parent sync, last prelaunch expiry and inherited blocked SIGALRM. No concrete remaining source defect found within the ordinary stated invocation/storage limits; all active modes remain unexecuted and require distinct fresh phase gates.',
    'actual_criteria_summary': 'Exact15path13A2M overlay;803/387/133/134 to816/390/136/137; all58741 raw untargeted native records,58756successor, exact six TREE ancestors/unchanged extension, foreign staging and whole untargeted HEAD preserved; separate current nonce/time/actual audit/root bindings; private ignored0700/0600 capture, one ordinary commit/push/deploy with stop/no retry; bounded15GETs. No hard-real-time/SIGKILL/fsync-failure/UI certificate.',
    'audit_FINAL': external(A / 'FINAL.json'),
    'audit_manifest': external(A / 'MANIFEST.json'),
    'helper': helper_pin, 'PLAN': plan_pin}
new(source_out, {'UTC': now, 'status': 'ACCEPTED_V3_STATIC_SOURCE_ONLY',
                 'source_packet': source, 'audit_packet': audit,
                 'authenticated_files': 24, 'child_directories': 0,
                 'helper': helper_pin, 'PLAN': plan_pin,
                 'root_resolution': resolution,
                 'root_actual_source_read_ranges': [[1,260],[261,540],[541,820],[821,1100],[1101,1380],[1381,1709]],
                 'all_helper_modes_import_AST_compile_help_test_executions': 0,
                 'prior_V1_V2_UNFIT_history_unchanged': True,
                 'publication_or_future_action_authority': False,
                 'AA': None, 'follow_up': None})
new(page_out, {'UTC': now, 'status': 'ACCEPTED_PRIVATE_EDITORIAL_ONLY',
               'packet': editorial, 'authenticated_files': 18, 'child_directories': 1,
               'root_entire_actual_HTML_MODEL_Bib_native_assets_REPORT_FINAL_and_independent_copy_review_read': True,
               'full_native_abstract_exact_dates_version_credit_AI_status_and_global_claim_preserved': True,
               'unchanged_native_PDF_ZIP_and_shared_CSS': True,
               'follow_up': None, 'AA': None, 'actual_canonical': None,
               'publication_certificate': False, 'future_action_authority': False,
               'legacy_scout': {'record': 23411227, 'genuine_candidate_found': False,
                                'physical_docs_filenames': 257, 'physical_eligible_text_files': 86,
                                'fixed_docs_trees': ['6ccfd5ab446400dc7fb3933dcc2e374cb415fa90','e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'],
                                'each_tree_leaf_paths': 254, 'each_tree_eligible_text_files': 115,
                                'evidence': 'Read-only parent/child scout tool transcripts; no separately captured raw command streams. Exact IDs/title and distinctive Fano terms absent in these finite collections, unrelated rank-two Jacobian hit rejected. No all-history/live/worldwide or archive-content absence claim.'}})

qpath = P / 'reconciliation/current-native-queue-20261117-pass146-fano.json'
queue = json.loads((P / 'reconciliation/current-native-queue-20261117-pass145-pentagon.json').read_text())
changes = {172: (23411227, 'Reviewed — preparing page'), 193: (23204810, 'In review — full manuscript')}
found = []
for row in queue['queue']:
    key = row['current_native_sheet_row']
    if key in changes:
        record, status_value = changes[key]
        assert row['record_id'] == record
        row['native_status'] = status_value
        found.append(key)
assert sorted(found) == [172,193] and len(queue['queue']) == 203
assert len({row['record_id'] for row in queue['queue']}) == 203
receipt = 'verification/sheet-fano-pass146-sperner-review-20261117/FINAL_READBACK.json'
final = json.loads((P / receipt).read_text())
assert final['reviewed'] == 146 and final['remaining'] == 57 and final['untargeted_whole_CellData_preserved'] == 263
queue.update(UTC=now, note='Native146; exact5value-only cells at172/193 read back. All247statuscells freshly read; only W172:AD172 and W193:AD193 identities freshly checked. Other203 identity reconciliation inherited, not falsely fresh reread.',
             source_final_native_readback=receipt,
             source_latest_native_status_snapshot='verification/sheet-fano-pass146-sperner-review-20261117/AFTER_CELLS.packed.json',
             latest_fresh_native_identity_range="'Full List'!W172:AD172 and W193:AD193",
             all203_identities_freshly_read_this_step=False)
new(qpath, queue)
progress_path = P / 'PROGRESS.json'
progress = json.loads(progress_path.read_text())
progress.update(updated_utc=now, current_status_UTC=now,
    root_scientific_dispositions=146, native_tracker_reviewed_count=146,
    root_scientific_percent=146/203*100, reviewed_or_deferred_percent=146/203*100,
    pending_other_eligible_works=57, scientific_reviews_remaining=57,
    native_sheet_preparing_count=5, native_sheet_deployed_pending_count=10,
    root172_native_transition_pending=False, root193_review_percent=35,
    current_native_queue=str(qpath.relative_to(P)),
    authoritative_current_native_queue=str(qpath.relative_to(P)),
    native_tracker_latest_readback=receipt,
    latest_math_checkpoint=checks['commit'], last_scoped_Math_checkpoint=checks['commit'],
    latest_checkpoint_commit=checks['commit'],
    latest_checkpoint_postverify=str((C/'POST_TREE_AUDIT.json').relative_to(P)),
    latest_math_checkpoint_root_adoption=str(cp_out.relative_to(P)),
    latest_math_checkpoint_root_adoption_SHA256=info(cp_out)['SHA256'],
    current_v3_source_adoption=str(source_out.relative_to(P)),
    current_fano_private_editorial_adoption=str(page_out.relative_to(P)),
    note='Native/scientific146/203:138PASS8defer57remaining (71.921182%).123verified+10deployed-awaitingactualUI+5preparing+6inreview+49queued+2holds+8defer. Fano full original PASS recorded AB172/AD172; optional one native SymPy failure retained without retry/checker positives. Sperner193 sourcefirst two INITIALs checkpointed, complete root original reading done, dependency/final review pending. All5targetnativecells/263untargetedcells/8metadata exact. Website remains4cc09d6/public803/387. V3source24file private static adoption accepted; ALLmodes unexecuted, no future authority. Programme active/incomplete.')
with progress_path.open('w') as stream:
    json.dump(progress, stream, indent=2)
    stream.write('\n')
    stream.flush()
    os.fsync(stream.fileno())
with (P / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n' + now + ' — Verified/adopted checkpoint164a5696 (274P-onlypaths;88closures251keys;159siblings/docs/nativeM/W unchanged), sourceV3/static24 and Fano editorial18/1 by fresh96file finite authentication. Full actual source1709/PLAN231/diffs/staticreports personally read, no active release invocation. Native exact5cells172/193 readback146/20371.921182%;138PASS8defer57remain, AAblank;263untargetedwholecells and8metadata exact. Sourcefirst193 families remain immutable, original body mechanics reused openly byroot with no peer findings exposure. No followup, formal/human/UI/publication certificate.\n')
    stream.flush()
    os.fsync(stream.fileno())
print(json.dumps({'authenticated_files': 96, 'child_directories': 1,
                  'checkpoint_adoption': external(cp_out),
                  'source_adoption': external(source_out),
                  'page_adoption': external(page_out), 'queue': external(qpath),
                  'native_and_scientific_reviewed': 146, 'remaining': 57}))
