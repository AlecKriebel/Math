"""One administrative finalization; no scientific program or production action."""
import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'papers/23411227/reviews/root-continuation-20261117'
now = datetime.now(timezone.utc).isoformat()

def info(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': format(stat.S_IMODE(path.stat().st_mode), '04o')}

def save_new(path, obj):
    with path.open('x') as out:
        json.dump(obj, out, indent=2)
        out.write('\n')
        out.flush()
        os.fsync(out.fileno())

specs = [
    ('verification/fano-root-evidence-custody-sol-20261117', 19, 0,
     '54f431130ea63d81b816f0fd77f3f4b6bb773cebada297e8417b44451e1e54e6',
     'bfd4cc3df84158a3796aee782eb56c182d52d35c8568ecc5967082c4fc722111'),
    ('papers/23411227/reviews/mw-input-challenge-sol-20261117', 23, 1,
     'f46a581c24e857ef48483e18b87665c0d7b9d5691c4e9406d759e6866301059e',
     '65f748b01ffa0aef02ce6eaa68a132675f0f1cd02ab9c352dabd0cd83e6de918')
]
checked = []
for relative, files, dirs, final_sha, manifest_sha in specs:
    root = P / relative
    assert info(root / 'FINAL.json')['SHA256'] == final_sha
    assert info(root / 'MANIFEST.json')['SHA256'] == manifest_sha
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    raw = manifest['payload_files']
    rows = raw.items() if isinstance(raw, dict) else ((row['path'], row) for row in raw)
    expected = {'FINAL.json', 'MANIFEST.json'}
    for name, declared in rows:
        namepath = Path(name)
        assert not namepath.is_absolute() and '..' not in namepath.parts
        path = root / name
        assert path.is_file() and not path.is_symlink()
        actual = info(path)
        assert actual['bytes'] == declared['bytes']
        assert actual['SHA256'] == declared['SHA256']
        assert int(actual['mode'], 8) == int(declared['mode'], 8)
        expected.add(name)
    actual_files, actual_dirs = set(), []
    for folder, childdirs, names in os.walk(root, followlinks=False):
        for child in childdirs:
            childpath = Path(folder) / child
            assert not childpath.is_symlink()
            actual_dirs.append(str(childpath.relative_to(root)))
        for name in names:
            path = Path(folder) / name
            assert stat.S_ISREG(path.lstat().st_mode)
            actual_files.add(str(path.relative_to(root)))
    assert actual_files == expected and len(actual_files) == files
    assert len(actual_dirs) == dirs
    checked.append({'path': relative, 'files': files, 'child_directories': dirs,
                    'FINAL': info(root / 'FINAL.json'),
                    'MANIFEST': info(root / 'MANIFEST.json')})

review = R / 'ROOT_REVIEW.md'
review_info = info(review)
assert review_info['SHA256'] == '4753c243b4b3a88c122e1480a3ef2995a266def28fe17fc83fce5956f70f58d3'
adoption = P / 'verification/root-fano-final-evidence-adoption-20261117.json'
clearance = P / 'verification/root-clearance-23411227-20261117.json'
ledger = R / 'FINAL_READING_LEDGER.json'
assert not any(path.exists() for path in (adoption, clearance, ledger))
save_new(adoption, {
    'UTC': now, 'status': 'ACCEPTED_FIXED_CUSTODY_AND_BOUNDED_MW_INPUT',
    'root_actual_complete_REPORT_FINAL_read': True,
    'root_complete_MW_exact_derivations_read_and_checked': True,
    'fresh_finite_authentication': checked,
    'authenticated_packet_files': 42, 'child_directories': 1,
    'underlying_fixed_custody': {'files': 334, 'child_directories': 29},
    'native_failure_preserved': {'attempts': 1, 'exit': 1, 'positive_children': 0},
    'scientific_execution_or_publication_certificate': False
})
save_new(ledger, {
    'UTC': now, 'root_review_percent': 100,
    'source_first_checkpoint_immutable': '436ec422f9ae291a365b9ff2814cb88bc15db8f3',
    'original_TeX_lines': 388, 'original_fresh_text_pages': 5,
    'original_fresh_raster_pages_viewed': 5,
    'primary_text_page_ledger': 'PRIMARY_READING_CHECKPOINT_65.json',
    'primary_raster_pages_personally_viewed': {
        'OWR': [29], 'MW': [10, 11, 12, 17, 18, 19], 'WZ': [1, 3, 7],
        'HL': [21, 28, 33, 34], 'BLXZ': [2, 5, 25], 'HLYTD': [18, 19]},
    'primary_raster_pages_viewed_total': 19,
    'both_current_full_REPORT_FINAL_and_detailed_derivations_read': True,
    'focused_MW_REPORT_FINAL_EXACT_SMOOTH_INPUT_read': True,
    'original_exposure_and_focused_summary_timing_not_rewritten': True,
    'root_native_support_lines_read': 630, 'root_native_code_lines_read': 286,
    'outer_portable_698_full_read_or_run': False,
    'root_scientific_executions': 0,
    'root_report': review_info, 'auxiliary_replay_success_claim': False
})
save_new(clearance, {
    'UTC': now, 'record_id': '23411227', 'sheet_row': 172,
    'status': 'PASS_ORIGINAL_FULL_QUANTIFIED_THEOREM',
    'scientific_review_completion_percent': 100,
    'full_original_manuscript_read': True,
    'root_source_first_and_primary_checkpoints': True,
    'independent_families': ['adversarial-sol', 'scope-sol'],
    'focused_additional_input': 'mw-input-challenge-sol-20261117',
    'central_defect_or_unsupported_inference': None,
    'native_API_and_printed_version': '1.0.0',
    'declared_publication_date': '2026-10-16',
    'review': str(review.relative_to(P)), 'review_info': review_info,
    'finite_custody_receipt': str(adoption.relative_to(P)),
    'finite_custody_info': info(adoption),
    'scope': 'Exact smooth Fano fivefold, unique GLOBAL Han-Li minimizer among ALL valuations, irrational weight ratio and rational-rank-two value group, singular canonical first center Z times F1, unchanged second underlying variety',
    'boundaries': ['Established named geometry/PDE inputs accepted, not formally reproved',
                   'Rational rank two, ordered rank one',
                   'No general product-minimizer theorem or dimension-three assertion',
                   'No exclusive priority, current-open-status or human refereeing claim'],
    'native_reproduction_limit': 'One scope native attempt exited1 at missing SymPy import, empty stdout, no positive checker children; no retry/install/alternate campaign. Exact written proof assessed independently.',
    'root_scientific_executions': 0, 'adversarial_scientific_executions': 0,
    'rights': 'Native CC-BY-4.0; no separate native MIT split inferred',
    'follow_up': None, 'prepare_factual_private_page_authorized': True,
    'publication_or_AA_or_redirect_certificate': False,
    'native_sheet_transition_pending': True,
    'scientific_dispositions': 146, 'scientific_passes': 138,
    'deferred': 8, 'scientific_remaining': 57,
    'programme_percent': 100 * 146 / 203, 'goal_complete': False
})
progress_path = P / 'PROGRESS.json'
progress = json.loads(progress_path.read_text())
progress.update({
    'updated_utc': now, 'root_scientific_dispositions': 146,
    'root_scientific_percent': 100 * 146 / 203,
    'root172_scientific_review_percent': 100,
    'root_clearance_23411227': str(clearance.relative_to(P)),
    'root172_native_transition_pending': True,
    'native_tracker_reviewed_count': 145,
    'scientific_reviews_remaining': 57,
    'note': 'Scientific146/203:138PASS8defer57remain; native145 pending exact row172 transition. Fano full original claim passed with accepted explicit geometry/PDE inputs; optional native replay failed at missingSymPy, no checker positives/retry. Website remains4cc09d6;10deployed await actualUI,4nativepreparing. V1/V2 production source UNFIT frozen;V3 inert source/static review only. Two row193 source-first INITIALs sealed, math withheld pending checkpoint. Goal active/incomplete.'
})
with progress_path.open('w') as out:
    json.dump(progress, out, indent=2)
    out.write('\n')
    out.flush()
    os.fsync(out.fileno())
with (R / 'RESEARCH_LOG.md').open('a') as out:
    out.write('\n' + now + ' — Full original Fano claim PASS100%; actual global theorem, exact irrationality, special real grading, bounded weak product soliton and absolute uniqueness checked. Both full current families and focused MW smooth-case derivations read;42file finite custody/MW packets freshly authenticated, underlying334/29 fixed. Primary pixels personally viewed19, scientific executions0, native auxiliary one exit1 retained with no child positives/retry. Scientific146/20371.921182%, native145 until separate mutation/readback. No publication/UI/AA certificate or followup.\n')
    out.flush()
    os.fsync(out.fileno())
print(json.dumps({'status': 'FULL_ORIGINAL_SCIENTIFIC_PASS_NATIVE_PENDING',
                  'review': review_info, 'clearance': info(clearance),
                  'adoption': info(adoption), 'ledger': info(ledger)}))
