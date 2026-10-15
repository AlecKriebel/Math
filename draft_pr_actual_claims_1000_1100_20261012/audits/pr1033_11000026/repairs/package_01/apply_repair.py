"""Apply PKG-01 once, preserving all frozen authored and private review bytes.

Run with PYTHONDONTWRITEBYTECODE=1 python3 -B. This deliberately does not
execute prepare_package.main(), conduct a new review, or contact services.
"""
import datetime
import hashlib
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'publication'
REPAIR = Path(__file__).resolve().parent
RAW = 'evidence/metric_01/sources/farb_printed_24_25.txt'


def pin(path):
    return {'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    assert not (PUB / 'evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json').exists()
    before = json.loads((REPAIR / 'BASELINE_FILE_PINS.json').read_text())
    baseline = {row['path']: row for row in before['files']}
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    old = json.loads((PUB / 'evidence/AUDIT_COPY_MANIFEST.json').read_text())
    raw_row = next(row for row in old['files'] if row['path'] == RAW)
    private = ROOT / raw_row['audit_source_path']
    assert pin(private) == pin(PUB / RAW) == {k: raw_row[k] for k in ('bytes', 'sha256')}
    (PUB / RAW).unlink()

    # Keep all 39 prior valid copies in their existing order, without rewriting
    # the files themselves. Append only authored records from the old review.
    copied = [row for row in old['files'] if row['path'] != RAW]
    select = runpy.run_path(str(ROOT / 'prepare_package.py'))['is_authored_review_record']
    directory = ROOT / 'reviews/package_01'
    appended = []
    for source in sorted(directory.rglob('*')):
        if not source.is_file() or not select(source, directory):
            continue
        relative = source.relative_to(directory)
        target = PUB / 'evidence/package_01' / relative
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        row = {'path': target.relative_to(PUB).as_posix(),
               'audit_source_path': source.relative_to(ROOT).as_posix(), **pin(target)}
        copied.append(row)
        appended.append(row)
    assert len(appended) == 15
    save(PUB / 'evidence/AUDIT_COPY_MANIFEST.json', {
        'utc': now, 'copied_authored_bytes_unchanged': True,
        'third_party_raw_bodies_omitted': True,
        'historical_manifests_describe_their_input_stages': True,
        'repair_id': 'PKG-01', 'retained_prior_authored_records': 39,
        'appended_package_01_authored_records': 15,
        'stage_mapping': 'evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json',
        'files': copied})

    stage = {
        'utc': now, 'repair_id': 'PKG-01',
        'scope': 'Remove only the distributed raw Farb extract; preserve mathematical and frozen review bytes',
        'historical_stage': {
            'review_family': 'package_01', 'status': 'ISSUES_FOUND',
            'actionable_counts': {'P0': 0, 'P1': 0, 'P2': 1, 'P3': 0},
            'reviewed_archive': baseline['publication/teichmuller_original_ball_paths_source_audits_v1.zip'],
            'reviewed_package_manifest': baseline['publication/PACKAGE_MANIFEST.json'],
            'reviewed_authored_copy_manifest': baseline['publication/evidence/AUDIT_COPY_MANIFEST.json'],
            'reviewed_controls_preserved_privately_under': 'repairs/package_01/before/',
            'review_input_pins_copied_unchanged': [
                'evidence/package_01/INPUT_PINS_INITIAL.json',
                'evidence/package_01/INPUT_PINS_FINAL.json'],
            'historical_output_pins_copied_unchanged': 'evidence/package_01/OUTPUT_PINS.json',
            'old_pin_meaning': 'Hashes of the earlier candidate or private inspected bodies, never claims about changed current files',
            'old_reviewed_archive_body_not_redistributed': True},
        'intentionally_omitted_raw_body': {
            **raw_row,
            'private_original_preserved': True,
            'current_distribution': 'Absent from publication/evidence and the rebuilt archive',
            'root_historical_output_pin': 'evidence/ROOT_MATH_ACCEPTANCE.json: authored_output_pins path reviews/metric_01/sources/farb_printed_24_25.txt',
            'source_identity_locator_record_retained': 'evidence/metric_01/sources/SOURCE_PINS.json',
            'other_historical_references': [
                'evidence/package_01/ACTIONABLE_ISSUES.json',
                'evidence/package_01/FULL_REVIEW.md',
                'evidence/package_01/HISTORICAL_PIN_RECONCILIATION.json',
                'evidence/package_01/PACKAGE_VERIFICATION.json',
                'evidence/package_01/PRIVATE_SOURCE_PINS.json'],
            'reference_semantics': 'Historical locators and exact byte identities; raw bodies are private provenance and not portable included dependencies'},
        'private_work_excluded': [
            'raw/rawprivate/raw_private bodies', 'extracted candidate trees',
            'render/renders/candidate_render images and text', 'cache/.cache/__pycache__',
            '.venv/tmp', 'source text/HTML/PDF/image bodies and archives'],
        'current_stage': {
            'package_01_actionable_repair_applied': True,
            'new_independent_review_family': 'package_02', 'new_review_status': 'PENDING',
            'immutable_publication_clearance': False,
            'copy_pins': 'evidence/AUDIT_COPY_MANIFEST.json',
            'current_inventory': 'PACKAGE_MANIFEST.json'},
        'appended_authored_records': appended}
    save(PUB / 'evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json', stage)

    state = json.loads((PUB / 'evidence/CURRENT_REVIEW_STATE.json').read_text())
    state.update({
        'utc': now,
        'fresh_package_reviews': [
            {'family': 'package_01', 'status': 'ISSUES_FOUND',
             'verdict': 'evidence/package_01/VERDICT.json',
             'reviewed_archive_sha256': stage['historical_stage']['reviewed_archive']['sha256'],
             'actionable_issues': ['PKG-01'], 'required_repair_applied': True,
             'repair_verification_by_new_independent_reviewer': 'PENDING'},
            {'family': 'package_02', 'status': 'PENDING',
             'scope': 'NEW independent whole-package adversarial review of the repaired candidate'}],
        'prior_review_actionable_repairs_applied': True,
        'repair_id': 'PKG-01',
        'repair_stage_mapping': 'evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json',
        'all_actionable_issues_resolved': False,
        'preprint_ready_for_immutable_publication': False, 'published': False,
        'next_gate': 'NEW independent whole-package review 02'})
    save(PUB / 'evidence/CURRENT_REVIEW_STATE.json', state)

    readme = PUB / 'README.md'
    old_text = ('peer review or journal acceptance. A NEW independent whole-package review\n'
                'and any resulting repair loops remain pending before immutable publication.\n')
    new_text = ('peer review or journal acceptance. Whole-package review 01 found one raw-source\n'
                'packaging issue (PKG-01); its required omission and archive repair are applied.\n'
                'The unchanged [review 01 report](evidence/package_01/FULL_REVIEW.md) and\n'
                '[repair stage mapping](evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json) retain\n'
                'that history. A NEW independent whole-package review 02 and any resulting\n'
                'repair loops remain pending before immutable publication.\n')
    assert readme.read_text().count(old_text) == 1
    readme.write_text(readme.read_text().replace(old_text, new_text))

    supplement = PUB / 'SUPPLEMENT.md'
    old_text = ('The supporting package remains subject to a NEW whole-package adversarial\n'
                'review and repair loop before immutable publication.\n')
    new_text = ('The raw Farb text extraction identified by whole-package review 01 is omitted\n'
                'from the repaired distribution; its private source and historical pins remain\n'
                'unchanged. The [repair stage mapping](evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json)\n'
                'explains those old references. A NEW independent whole-package adversarial\n'
                'review 02 and any resulting repair loops remain pending before immutable publication.\n')
    assert supplement.read_text().count(old_text) == 1
    supplement.write_text(supplement.read_text().replace(old_text, new_text))

    index = PUB / 'evidence/INDEX.md'
    text = index.read_text()
    anchor = '- [Unchanged authored-copy pins](AUDIT_COPY_MANIFEST.json),\n'
    addition = ('- [Whole-package review 01](package_01/FULL_REVIEW.md),\n'
                '  [verdict](package_01/VERDICT.json), [actionable finding](package_01/ACTIONABLE_ISSUES.json),\n'
                '  [independent derivation](package_01/INDEPENDENT_DERIVATION.md),\n'
                '  [package verification](package_01/PACKAGE_VERIFICATION.json),\n'
                '  [historical pin reconciliation](package_01/HISTORICAL_PIN_RECONCILIATION.json),\n'
                '  [input pins](package_01/INPUT_PINS_FINAL.json), [output pins](package_01/OUTPUT_PINS.json),\n'
                '  [source manifest](package_01/SOURCE_MANIFEST.json),\n'
                '  [source retrievals](package_01/SOURCE_RETRIEVALS.json),\n'
                '  [source locators](package_01/SOURCE_VISUAL_LOCATORS.json),\n'
                '  [private-body identities](package_01/PRIVATE_SOURCE_PINS.json),\n'
                '  [review log](package_01/RESEARCH_LOG.md). These are unchanged authored\n'
                '  records of the earlier candidate, whose one P2 issue required the raw\n'
                '  Farb extraction to be omitted. The [repair stage mapping](PACKAGE_01_REPAIR_STAGE_MAPPING.json)\n'
                '  records that intentional omission and the old hashes; raw bodies, candidate\n'
                '  extractions and page renders stay outside the distribution.\n')
    assert text.count(anchor) == 1
    text = text.replace(anchor, addition + anchor)
    text = text.replace('a NEW full package review remains pending.\n',
                        'the PKG-01 repair is applied and a NEW independent full package review 02 remains pending.\n')
    index.write_text(text)
    runpy.run_path(str(ROOT / 'build_package.py'), run_name='__main__')
    print(json.dumps({'repair_id': 'PKG-01', 'utc': now,
                      'retained_authored': 39, 'appended_authored': 15,
                      'raw_body_absent': not (PUB / RAW).exists(),
                      'new_independent_review': 'package_02 PENDING'}))


if __name__ == '__main__':
    main()
