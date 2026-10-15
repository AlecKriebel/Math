"""Adopt frozen clean whole review02; preserve the reviewed mathematical bytes."""
import datetime
import hashlib
import json
from pathlib import Path
import re
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


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def replace(path, old, new):
    text = path.read_text()
    require(text.count(old) == 1, 'Administrative anchor differs: ' + str(path))
    path.write_text(text.replace(old, new))


def main():
    require(not (HERE / 'FINAL_SEAL.json').exists(), 'Final package already frozen')
    review = HERE / 'reviews/package_02'
    verdict = json.loads((review / 'VERDICT.json').read_text())
    require(verdict['status'] == 'CLEAN' and verdict['issues'] == [] and
            all(x == 0 for x in verdict['actionable_counts'].values()), 'Clean full review required')
    archive = PUB / 'teichmuller_original_ball_paths_source_audits_v1.zip'
    require(sha(archive) == verdict['reviewed_archive']['sha256'], 'Reviewed archive changed')
    frozen = {n: sha(PUB / n) for n in ('research_note.tex', 'research_note.pdf', 'metadata.json')}
    rows = json.loads((review / 'OUTPUT_PINS.json').read_text())['files']
    rows += [{'path': 'OUTPUT_PINS.json', 'bytes': (review / 'OUTPUT_PINS.json').stat().st_size,
              'sha256': sha(review / 'OUTPUT_PINS.json')}]
    copied = []
    for row in rows:
        rel = Path(row['path'])
        require(not rel.is_absolute() and '..' not in rel.parts and
                not any(x in rel.parts for x in ('raw', 'rawprivate', 'extracted', 'render', 'tmp', '__pycache__')),
                'Private/unsafe review path')
        require(rel.suffix not in {'.pdf', '.png', '.txt', '.zip', '.pyc'}, 'Third-party/duplicate review body')
        source = review / rel
        require(source.stat().st_size == row['bytes'] and sha(source) == row['sha256'], 'Frozen review output differs')
        target = EVIDENCE / 'package_02' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied.append({'path': target.relative_to(PUB).as_posix(),
                       'audit_source_path': source.relative_to(HERE).as_posix(),
                       'bytes': target.stat().st_size, 'sha256': sha(target)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(EVIDENCE / 'PACKAGE_REVIEW_02_COPY.json', {'utc': now, 'unchanged_authored_review_copies': True,
        'files': copied, 'raw_source_bodies_renders_extractions_caches_excluded': True,
        'historical_pins_keep_original_input_stage_meanings': True})
    manifest = json.loads((EVIDENCE / 'AUDIT_COPY_MANIFEST.json').read_text())
    manifest['utc'] = now
    manifest['terminal_package_02_authored_records'] = len(copied)
    manifest['files'] += copied
    save(EVIDENCE / 'AUDIT_COPY_MANIFEST.json', manifest)
    state = json.loads((EVIDENCE / 'CURRENT_REVIEW_STATE.json').read_text())
    require([r['family'] for r in state['fresh_package_reviews']] == ['package_01', 'package_02'], 'Review history differs')
    state['utc'] = now
    state['fresh_package_reviews'][0]['repair_verification_by_new_independent_reviewer'] = 'VERIFIED_BY_PACKAGE_02'
    state['fresh_package_reviews'][1] = {'family': 'package_02', 'status': 'CLEAN',
        'actionable_issue_count': 0, 'verdict': 'evidence/package_02/VERDICT.json',
        'reviewed_archive_sha256': verdict['reviewed_archive']['sha256'], 'whole_scoped_theorem_and_package_verified': True}
    state.update({'preprint_ready_for_immutable_publication': True, 'all_actionable_issues_resolved': True,
        'published': False, 'pending_issues': [],
        'next_gate': 'authorized production publication after preceding PR1032 priority disposition, preserving ascending order'})
    save(EVIDENCE / 'CURRENT_REVIEW_STATE.json', state)
    save(EVIDENCE / 'FINAL_ACCEPTANCE.json', {'utc': now, 'pr': 1033, 'original_head': verdict['original_head'],
        'scope': verdict['scope'], 'mathematical_gap': None, 'eligible_framing': 'EXPOSITORY_COROLLARY_ONLY',
        'substantive_geometry_Lenzhen_Rafi_prior': True, 'priority_and_generic_lemma_firstness_unestablished': True,
        'fresh_whole_package_reviews': 2, 'terminal_review_status': 'CLEAN', 'actionable_issues': [],
        'PKG01_private_raw_preservation_and_distribution_omission_verified': True,
        'reviewed_mathematical_source_PDF_metadata_unchanged': frozen, 'preprint_ready': True,
        'published': False, 'extensive_AI_use': True, 'unrefereed': True, 'conventional_human_peer_review': False})
    replace(PUB / 'README.md',
        'that history. A NEW independent whole-package review 02 and any resulting\nrepair loops remain pending before immutable publication.',
        'that history. A NEW independent whole-package review 02 rederived the entire\n'
        'theorem and verified the source, repair and full package with zero actionable\n'
        'issues. [The clean review](evidence/package_02/FULL_REVIEW.md) and\n'
        '[final acceptance](evidence/FINAL_ACCEPTANCE.json) record readiness for\n'
        'immutable publication. Publication remains pending in the ascending PR workflow.')
    replace(PUB / 'SUPPLEMENT.md',
        'explains those old references. A NEW independent whole-package adversarial\nreview 02 and any resulting repair loops remain pending before immutable publication.',
        'explains those old references. A NEW independent whole-package review 02\n'
        'verified the complete theorem, source interfaces, all three paper pages,\n'
        'the repair and entire package with zero actionable issues.\n'
        '[Final acceptance](evidence/FINAL_ACCEPTANCE.json) records readiness for\n'
        'immutable publication; publication remains pending in ascending PR order.')
    replace(EVIDENCE / 'INDEX.md',
        'No earlier PASS or acceptance constitutes current zero-issue package clearance;\nthe PKG-01 repair is applied and a NEW independent full package review 02 remains pending.',
        'Earlier PASS and acceptance records retain their input-stage meanings.\n'
        '[NEW second full package review](package_02/FULL_REVIEW.md),\n'
        '[clean verdict](package_02/VERDICT.json) and\n'
        '[unchanged terminal copy pins](PACKAGE_REVIEW_02_COPY.json) independently\n'
        'verify the entire theorem, primary interfaces, all three pages and full\n'
        'package. PKG-01 is resolved and zero actionable issues remain.\n'
        '[Final acceptance](FINAL_ACCEPTANCE.json) advances readiness. After that\n'
        'review only its unchanged authored records and administrative navigation/\n'
        'acceptance were appended; reviewed TeX, PDF and metadata stay unchanged.\n'
        'Publication remains pending after preceding PR1032 priority disposition.')
    require(all(sha(PUB / n) == digest for n, digest in frozen.items()), 'Mathematical/metadata bytes changed')
    subprocess.run([sys.executable, '-B', str(HERE / 'build_package.py')], check=True)
    records = json.loads((PUB / 'PACKAGE_MANIFEST.json').read_text())['files']
    for row in records:
        path = PUB / row['path']
        require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'Final inventory differs')
    for row in manifest['files']:
        require((PUB / row['path']).read_bytes() == (HERE / row['audit_source_path']).read_bytes(), 'Authored copy differs')
    links = []
    for name in ('README.md', 'SUPPLEMENT.md', 'evidence/INDEX.md'):
        path = PUB / name
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if not link.startswith(('http:', 'https:', '#')):
                require((path.parent / link.split('#')[0]).exists(), 'Missing final navigation link')
                links.append(link)
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        require(zipped.testzip() is None and len(names) == len(records) + 1 and names == sorted(names), 'ZIP inventory/CRC/order')
        require(len(set(names)) == len(names) == len({n.casefold() for n in names}), 'Duplicate ZIP paths')
        for info in zipped.infolist():
            name = info.filename
            require(name.isascii() and name.startswith('teichmuller_original_ball_paths_v1/') and
                    '..' not in Path(name).parts and '\\' not in name and info.external_attr >> 16 == 0o100644,
                    'Unsafe final ZIP path')
            require(zipped.read(name) == (PUB / name.removeprefix('teichmuller_original_ball_paths_v1/')).read_bytes(),
                    'Final archived bytes differ')
    wrapper = json.loads((PUB / 'zenodo-deposit.json').read_text())
    require(wrapper['metadata'] == json.loads((PUB / 'metadata.json').read_text()), 'Metadata wrapper differs')
    integrity = {'utc': now, 'status': 'PASS', 'archive_entries': len(names), 'manifest_records': len(records),
        'archive_bytes': archive.stat().st_size, 'archive_sha256': sha(archive), 'terminal_authored_review_copies': len(copied),
        'all_authored_copies': len(manifest['files']), 'relative_links_verified': len(links),
        'safe_names_CRC_exact_bytes_metadata_pass': True, 'reviewed_math_PDF_metadata_unchanged': frozen}
    save(HERE / 'FINAL_PACKAGE_INTEGRITY.json', integrity)
    save(HERE / 'FINAL_SEAL.json', {'utc': now, 'immutable_ready': True, 'published': False,
        'fresh_whole_package_reviews': 2, 'actionable_issues': [], 'mathematical_payload': frozen,
        'archive_sha256': sha(archive), 'archive_entries': len(names),
        'postreview_changes': 'unchanged terminal review records and administrative acceptance/navigation only',
        'publication_order_hold': 'preceding PR1032 priority disposition pending'})
    print(json.dumps(integrity))


if __name__ == '__main__':
    main()
