"""Append frozen clean review 04 and advance only acceptance/navigation records."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
PUB = HERE / 'publication'
EVIDENCE = PUB / 'evidence'


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def replace(path, old, new):
    text = path.read_text()
    require(text.count(old) == 1, 'Administrative text anchor differs: ' + str(path))
    path.write_text(text.replace(old, new))


def main():
    require(not (HERE / 'FINAL_SEAL.json').exists(), 'Final seal exists; never rewrite frozen files')
    review = HERE / 'reviews/package_04'
    verdict = json.loads((review / 'VERDICT.json').read_text())
    require(verdict['status'] == 'CLEAN' and verdict['actionable_issues'] == [] and
            all(v == 0 for v in verdict['severity_counts'].values()), 'Clean full review required')
    archive = PUB / 'grassmann_calibrations_source_verification_v1.zip'
    require(sha(archive) == verdict['candidate']['sha256'], 'Reviewed archive changed')
    frozen_paths = [PUB / n for n in ('research_note.tex', 'research_note.pdf', 'metadata.json', 'run_checks.py')]
    frozen_paths += [p for d in ('checks', 'expected') for p in (PUB / d).rglob('*') if p.is_file()]
    frozen = {p.relative_to(PUB).as_posix(): sha(p) for p in frozen_paths}
    records = json.loads((review / 'OUTPUT_PINS.json').read_text())['records']
    copied = []
    for record in records + [{'path': 'OUTPUT_PINS.json', 'bytes': (review / 'OUTPUT_PINS.json').stat().st_size,
                              'sha256': sha(review / 'OUTPUT_PINS.json')}]:
        relative = Path(record['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe review path')
        require(not any(x in relative.parts for x in ('raw', 'rawprivate', 'extracted', 'render', '__pycache__', 'tmp')),
                'Private review body in authored pins')
        require(relative.suffix not in {'.pdf', '.png', '.zip', '.pyc', '.txt'}, 'Raw/duplicate review body')
        source = review / relative
        require(source.stat().st_size == record['bytes'] and sha(source) == record['sha256'], 'Review output pin differs')
        target = EVIDENCE / 'package_review_04' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied.append({'path': target.relative_to(PUB).as_posix(), 'bytes': target.stat().st_size, 'sha256': sha(target)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(EVIDENCE / 'PACKAGE_REVIEW_04_COPY.json', {
        'utc': now, 'all_copied_bytes_unchanged': True, 'files': copied,
        'excluded': 'raw third-party bodies, page renders, extracted input copies and caches',
        'historical_manifests_describe_original_review_inputs': True})
    state = json.loads((EVIDENCE / 'CURRENT_REVIEW_STATE.json').read_text())
    require([r['round'] for r in state['fresh_package_reviews']] == [1, 2, 3], 'Prior review history differs')
    state['utc'] = now
    state['fresh_package_reviews'].append({'round': 4, 'status': 'CLEAN', 'actionable_issue_count': 0,
        'input_archive_sha256': verdict['candidate']['sha256'], 'complete_theorem_and_package_reviewed': True})
    state.update({'preprint_ready_for_immutable_publication': True, 'all_actionable_issues_resolved': True,
        'published': False, 'pending_issues': [], 'next_gate': 'owner final integrity, production publication and tracker'})
    save(EVIDENCE / 'CURRENT_REVIEW_STATE.json', state)
    save(EVIDENCE / 'FINAL_ACCEPTANCE.json', {
        'utc': now, 'pr': 1031, 'audited_head': verdict['candidate']['original_head'],
        'mathematics': 'root and distinct geometry and SOS/source families passed complete scoped deduction',
        'priority': 'bounded primary-body audit; all nine framing obligations adopted globally; no worldwide priority certification',
        'fresh_whole_package_reviews': 4, 'final_review': 'CLEAN', 'actionable_issues': [], 'preprint_ready': True,
        'scope': verdict['strongest_verified_result'], 'Fawzi_theorem_external_not_reproved': True,
        'AI_used_extensively': True, 'unrefereed': True, 'conventional_human_peer_review': False,
        'finite_checks_replace_universal_proof': False, 'reviewed_mathematical_payload_unchanged': frozen})
    replace(PUB / 'README.md', 'Version 1.0, 12 October 2026. Draft preprint; NEW whole-package review pending.',
            'Version 1.0, 12 October 2026. Unrefereed preprint; final full review clean.')
    replace(PUB / 'README.md',
        'Current immutable-publication readiness is false until a NEW fresh package\nreview and any required repair loops finish.',
        'The NEW fourth independent whole-package review found zero actionable issues.\n'
        '[Final acceptance](evidence/FINAL_ACCEPTANCE.json) and\n'
        '[current review state](evidence/CURRENT_REVIEW_STATE.json) record readiness\nfor immutable publication.')
    replace(PUB / 'README.md',
        'certificates, reference streams and metadata are unchanged. A NEW fourth\nindependent whole-package review is required.',
        'certificates, reference streams and metadata are unchanged. A NEW fourth\n'
        'independent reviewer rederived the entire theorem, checked primary bodies,\n'
        'all six PDF pages and the full package, and found zero actionable issues.\n'
        '[The clean review](evidence/package_review_04/FULL_REVIEW.md) and\n'
        '[verdict](evidence/package_review_04/VERDICT.json) are preserved unchanged.')
    replace(PUB / 'SUPPLEMENT.md',
        'failing calibration. NEW whole-package review remains required before immutable\npublication; the current state records that gate. AI reviews are not',
        'failing calibration. The NEW fourth full independent package review is clean\n'
        'with zero actionable issues. [Final acceptance](evidence/FINAL_ACCEPTANCE.json)\n'
        'and [current state](evidence/CURRENT_REVIEW_STATE.json) record readiness for\nimmutable publication. AI reviews are not')
    replace(EVIDENCE / 'INDEX.md',
        'complete; a NEW independent whole-package review is still pending, so this\ndraft has not passed the immutable-publication gate.',
        'complete. The NEW fourth independent whole-package review is clean with zero\n'
        'actionable issues; [final acceptance](FINAL_ACCEPTANCE.json) records the\nimmutable-publication gate.')
    replace(EVIDENCE / 'INDEX.md',
        'reference streams and metadata remain unchanged. A NEW fourth full\nindependent package review is pending.',
        'reference streams and metadata remain unchanged.\n\n'
        '[Fourth fresh whole-package review](package_review_04/FULL_REVIEW.md),\n'
        '[clean verdict](package_review_04/VERDICT.json) and\n'
        '[unchanged copy pins](PACKAGE_REVIEW_04_COPY.json) record the final stage.\n'
        'The full scoped theorem, source interfaces, verification, original files,\n'
        'metadata and all six paper pages passed with zero actionable issues.\n'
        'After this review only its unchanged authored evidence and administrative\n'
        'acceptance/navigation records were appended. The last reviewed mathematical\n'
        'source, PDF, validator, certificates, runner and metadata remain unchanged.\n'
        'Historical manifests keep their original stage meanings.')
    require(all(sha(PUB / p) == h for p, h in frozen.items()), 'Protected payload changed')
    subprocess.run([sys.executable, '-B', str(HERE / 'build_package.py')], check=True)
    manifest = json.loads((PUB / 'PACKAGE_MANIFEST.json').read_text())['files']
    for record in manifest:
        path = PUB / record['path']
        require(path.stat().st_size == record['bytes'] and sha(path) == record['sha256'], 'Final manifest differs')
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        require(zipped.testzip() is None and names == sorted(names) and len(names) == len(manifest) + 1,
                'Final archive inventory or CRC differs')
        require(len(set(names)) == len(names) == len({n.casefold() for n in names}), 'Duplicate archive paths')
        for info in zipped.infolist():
            name = info.filename
            require(name.isascii() and name.startswith('grassmann_calibrations_v1/') and
                    '..' not in Path(name).parts and '\\' not in name and
                    info.external_attr >> 16 == 0o100644, 'Unsafe archive member')
            path = PUB / name.removeprefix('grassmann_calibrations_v1/')
            require(zipped.read(name) == path.read_bytes(), 'Final archive bytes differ')
    wrapper = json.loads((PUB / 'zenodo-deposit.json').read_text())
    require(wrapper['metadata'] == json.loads((PUB / 'metadata.json').read_text()), 'Metadata wrapper differs')
    save(HERE / 'FINAL_PACKAGE_INTEGRITY.json', {'utc': now, 'status': 'PASS',
        'manifest_records': len(manifest), 'archive_entries': len(names), 'archive_sha256': sha(archive),
        'archive_bytes': archive.stat().st_size, 'unchanged_review04_copies': len(copied),
        'reviewed_mathematical_payload_unchanged': frozen, 'safe_names_CRC_exact_files': True,
        'metadata_wrapper_exact': True})
    save(HERE / 'FINAL_SEAL.json', {'utc': now, 'immutable_ready': True, 'no_actionable_concerns': True,
        'fresh_whole_package_reviews': 4, 'mathematical_payload': frozen, 'archive_sha256': sha(archive),
        'appended_final_review_files': len(copied), 'only_postreview_additions': 'unchanged terminal review and administrative acceptance/navigation'})
    print(json.dumps({'final_acceptance': True, 'review_files': len(copied), 'archive_sha256': sha(archive)}))


if __name__ == '__main__':
    main()
