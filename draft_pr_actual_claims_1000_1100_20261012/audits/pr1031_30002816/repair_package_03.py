"""Fix only PK03A diagnostic literals; preserve frozen mathematical evidence."""
import ast
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB = HERE / 'publication'
EVIDENCE = PUB / 'evidence'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    if (EVIDENCE / 'REPAIR_RECORD_03.json').exists():
        raise RuntimeError('Round 03 already applied; do not reset its stage')
    review = HERE / 'reviews/package_03'
    verdict = json.loads((review / 'VERDICT.json').read_text())
    if verdict['status'] != 'REPAIR_REQUIRED' or {x['id'] for x in verdict['actionable_issues']} != {'PK03A'}:
        raise RuntimeError('Frozen verdict differs')
    archive = PUB / 'grassmann_calibrations_source_verification_v1.zip'
    if sha(archive) != verdict['candidate_archive']['sha256']:
        raise RuntimeError('Reviewed candidate differs')
    protected = [PUB / n for n in ('research_note.tex', 'research_note.pdf', 'metadata.json')]
    protected += [p for directory in ('checks', 'expected')
                  for p in (PUB / directory).rglob('*') if p.is_file()]
    before = {p.relative_to(PUB).as_posix(): sha(p) for p in protected}
    copied = []
    for source in sorted(review.rglob('*')):
        if not source.is_file():
            continue
        relative = source.relative_to(review)
        if any(p in relative.parts for p in ('raw', 'extracted', 'render', '__pycache__', 'tmp')):
            continue
        if source.suffix in {'.pdf', '.png', '.zip', '.pyc'}:
            continue
        target = EVIDENCE / 'package_review_03' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied.append({'path': target.relative_to(PUB).as_posix(), 'bytes': target.stat().st_size, 'sha256': sha(target)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(EVIDENCE / 'PACKAGE_REVIEW_03_COPY.json', {
        'utc': now, 'all_copied_bytes_unchanged': True,
        'excluded': 'raw third-party bodies, own page renders, extracted input archive and caches',
        'historical_manifests_describe_original_review_inputs': True, 'files': copied})
    runner = PUB / 'run_checks.py'
    old = runner.read_text()
    replacements = {
        'References must be exactly48unique executed cases': 'References must contain exactly 48 unique executed cases',
        'Exactly15actualcertificatefaultfamilies required': 'Exactly 15 actual certificate fault families required',
    }
    new = old
    for previous, repaired in replacements.items():
        if new.count(previous) != 1:
            raise RuntimeError('Diagnostic repair anchor differs')
        new = new.replace(previous, repaired)
    old_ast = ast.parse(old)
    for node in ast.walk(old_ast):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in replacements:
            node.value = replacements[node.value]
    if ast.dump(old_ast, include_attributes=False) != ast.dump(ast.parse(new), include_attributes=False):
        raise RuntimeError('AST changed beyond the two diagnostic literals')
    old_runner_sha = sha(runner)
    runner.write_text(new)
    readme = PUB / 'README.md'
    text = readme.read_text()
    anchor = 'independent whole-package review is required.'
    if text.count(anchor) != 1:
        raise RuntimeError('README stage anchor differs')
    text = text.replace('A NEW third\nindependent whole-package review is required.',
                        'The third NEW review verified the complete mathematics and found only\n'
                        'spacing in two current runner diagnostics. Those strings are corrected;\n'
                        'the runner algorithm, mathematical source, PDF, arithmetic validator,\n'
                        'certificates, reference streams and metadata are unchanged. A NEW fourth\n'
                        'independent whole-package review is required.')
    readme.write_text(text)
    index = EVIDENCE / 'INDEX.md'
    text = index.read_text()
    anchor = 'bytes are unchanged by round 02; a NEW third package review is pending.'
    if text.count(anchor) != 1:
        raise RuntimeError('Index stage anchor differs')
    index.write_text(text.replace(anchor, 'bytes were unchanged by round 02.\n\n'
        '[Third fresh package review](package_review_03/REVIEW.md),\n'
        '[verdict](package_review_03/VERDICT.json),\n'
        '[unchanged copy pins](PACKAGE_REVIEW_03_COPY.json) and\n'
        '[diagnostic spacing repair](REPAIR_RECORD_03.json) record the next stage.\n'
        'Only two exception-message literals changed in the current runner;\n'
        'AST equality after those literal replacements verifies unchanged logic.\n'
        'Original/historical files, mathematical source/PDF, arithmetic, certificates,\n'
        'reference streams and metadata remain unchanged. A NEW fourth full\n'
        'independent package review is pending.'))
    state = json.loads((EVIDENCE / 'CURRENT_REVIEW_STATE.json').read_text())
    state['utc'] = now
    state['fresh_package_reviews'].append({'round': 3, 'status': 'REPAIR_REQUIRED',
        'actionable_P3_issues': 1, 'root_repairs': 'REPAIR_RECORD_03.json',
        'input_archive_sha256': verdict['candidate_archive']['sha256']})
    state['next_gate'] = 'NEW independent whole-package review 04'
    save(EVIDENCE / 'CURRENT_REVIEW_STATE.json', state)
    save(EVIDENCE / 'REPAIR_RECORD_03.json', {
        'utc': now, 'issues_applied': ['PK03A'], 'diagnostic_replacements': replacements,
        'runner_before_sha256': old_runner_sha, 'runner_after_sha256': sha(runner),
        'AST_unchanged_except_two_diagnostic_literals': True,
        'mathematical_source_pdf_arithmetic_certificates_references_metadata_unchanged': before,
        'original_and_historical_bytes_unchanged': True, 'new_independent_recheck_pending': True})
    if any(sha(PUB / p) != h for p, h in before.items()):
        raise RuntimeError('Protected mathematical/reference/metadata bytes changed')
    print(json.dumps({'applied': ['PK03A'], 'copied_review_records': len(copied),
                      'runner_algorithm_unchanged': True, 'runner_after_sha256': sha(runner)}))


if __name__ == '__main__':
    main()
