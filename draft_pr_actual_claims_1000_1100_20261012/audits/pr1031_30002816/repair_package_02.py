"""Apply frozen PK02A and preserve the second independent review unchanged."""
import datetime
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB = HERE / 'publication'
EVIDENCE = PUB / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    if (EVIDENCE / 'REPAIR_RECORD_02.json').exists():
        raise RuntimeError('Round 02 already applied; preserve its stage record')
    review = HERE / 'reviews/package_02'
    verdict = json.loads((review / 'VERDICT.json').read_text())
    if verdict['status'] != 'REPAIR_REQUIRED' or {x['id'] for x in verdict['actionable_issues']} != {'PK02A'}:
        raise RuntimeError('Frozen verdict differs')
    archive = PUB / verdict['candidate']['archive']
    if sha(archive) != verdict['candidate']['sha256']:
        raise RuntimeError('Reviewed candidate differs')
    frozen = [PUB / n for n in ('research_note.tex', 'research_note.pdf', 'run_checks.py', 'metadata.json')]
    frozen += [p for p in (PUB / 'checks').rglob('*') if p.is_file()]
    before = {p.relative_to(PUB).as_posix(): sha(p) for p in frozen}
    copied = []
    for source in sorted(review.rglob('*')):
        if not source.is_file():
            continue
        relative = source.relative_to(review)
        if any(p in relative.parts for p in ('raw', 'extracted', 'render', '__pycache__')):
            continue
        if source.suffix in {'.pdf', '.png', '.zip', '.pyc'}:
            continue
        target = EVIDENCE / 'package_review_02' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied.append({'path': target.relative_to(PUB).as_posix(), 'bytes': target.stat().st_size, 'sha256': sha(target)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(EVIDENCE / 'PACKAGE_REVIEW_02_COPY.json', {
        'utc': now, 'all_copied_bytes_unchanged': True,
        'excluded': 'raw third-party bodies, own PDF renders, duplicate extracted candidate and caches',
        'historical_manifests_describe_original_review_inputs': True, 'files': copied})
    supplement = PUB / 'SUPPLEMENT.md'
    text = supplement.read_text()
    if text.count('G(3,6)result') != 1:
        raise RuntimeError('Spacing repair anchor differs')
    supplement.write_text(text.replace('G(3,6)result', 'G(3,6) result'))
    readme = PUB / 'README.md'
    text = readme.read_text()
    old = 'Both have been applied; a NEW second independent review is required.'
    if text.count(old) != 1:
        raise RuntimeError('README stage anchor differs')
    readme.write_text(text.replace(old, 'The second NEW review again verified the complete mathematics and found one\nremaining P3 spacing defect. That defect has been corrected. A NEW third\nindependent whole-package review is required.'))
    index = EVIDENCE / 'INDEX.md'
    text = index.read_text()
    old = 'prose have been repaired. A NEW second package review remains pending.'
    if text.count(old) != 1:
        raise RuntimeError('Index stage anchor differs')
    index.write_text(text.replace(old, 'prose were repaired after that review.\n\n[Second fresh package review](package_review_02/REVIEW.md),\n[verdict](package_review_02/VERDICT.json),\n[unchanged copy pins](PACKAGE_REVIEW_02_COPY.json) and\n[remaining spacing repair](REPAIR_RECORD_02.json) record the next stage.\nThat review verified the mathematics and found one P3 spacing defect.\nIt has been corrected. Mathematical source, PDF, arithmetic and metadata\nbytes are unchanged by round 02; a NEW third package review is pending.'))
    state = json.loads((EVIDENCE / 'CURRENT_REVIEW_STATE.json').read_text())
    state['utc'] = now
    state['fresh_package_reviews'].append({
        'round': 2, 'status': 'REPAIR_REQUIRED', 'actionable_P3_issues': 1,
        'root_repairs': 'REPAIR_RECORD_02.json', 'input_archive_sha256': verdict['candidate']['sha256']})
    state['next_gate'] = 'NEW independent whole-package review 03'
    save(EVIDENCE / 'CURRENT_REVIEW_STATE.json', state)
    save(EVIDENCE / 'REPAIR_RECORD_02.json', {
        'utc': now, 'issues_applied': ['PK02A'],
        'PK02A': 'Inserted the missing space in G(3,6) result in current supplement.',
        'mathematical_source_pdf_checkers_metadata_unchanged': before,
        'historical_and_original_bytes_unchanged': True, 'independent_recheck_pending': True})
    if any(sha(PUB / p) != h for p, h in before.items()):
        raise RuntimeError('Protected mathematical or metadata bytes changed')
    boundary_hits = []
    for name in ('README.md', 'SUPPLEMENT.md', 'evidence/INDEX.md'):
        for line, text in enumerate((PUB / name).read_text().splitlines(), 1):
            if '](' in text or 'http' in text:
                continue
            for match in re.finditer(r'\)[A-Za-z]', text):
                boundary_hits.append({'path': name, 'line': line, 'match': match.group(0), 'text': text})
    save(HERE / 'REPAIRED_PROSE_SCAN_02.json', {'utc': now, 'closing_parenthesis_word_hits': boundary_hits})
    print(json.dumps({'repairs_applied': ['PK02A'], 'unchanged_review_files_copied': len(copied),
                      'protected_bytes_unchanged': True, 'closing_parenthesis_word_hits': boundary_hits}))


if __name__ == '__main__':
    main()
