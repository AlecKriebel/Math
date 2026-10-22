"""Initial authored evidence assembly; preserve every original stage byte."""
import hashlib
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / 'publication'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    for name in ('checks', 'expected', 'evidence'):
        (PUB / name).mkdir(parents=True, exist_ok=True)
    programs = {
        'exact_checks': ROOT / 'submitted/current/exact_checks.py',
        'independent_exact_check': ROOT / 'reviews/proximity_01/independent_exact_check.py',
        'independent_ring_value_checks': ROOT / 'reviews/ring_hull_01/independent_ring_value_checks.py',
    }
    for name, source in programs.items():
        shutil.copyfile(source, PUB / 'checks' / (name + '.py'))
    original_contract = json.loads((ROOT / 'submitted/FINITE_CONTRACT.json').read_text())
    # Inspect the original schema rather than infer expected values from replay.
    write_json(PUB / 'expected/ORIGINAL_FINITE_CONTRACT.json', original_contract)
    proximity = json.loads((ROOT / 'reviews/proximity_01/CHECK_RUNS.json').read_text())
    independent_output = proximity['runs'][0]['parsed']
    write_json(PUB / 'expected/independent_exact_check.json', independent_output)
    for mode, label in ((0, 'normal'), (1, 'O'), (2, 'OO')):
        shutil.copyfile(ROOT / 'reviews/ring_hull_01' / ('independent_' + label + '.stdout'),
                        PUB / 'expected' / ('independent_ring_value_checks_mode' + str(mode) + '.stdout'))
    mutation_rows = json.loads((ROOT / 'reviews/proximity_01/SOURCE_MUTATIONS.json').read_text())['runs']
    unique = {}
    for row in mutation_rows:
        if row['mode'] != 'normal':
            continue
        reason = row['expected_last_error'].removeprefix('RuntimeError: ')
        unique[row['name']] = {'before': row['replace']['old'],
                               'after': row['replace']['new'], 'reason': reason,
                               'mutant_sha256': row['mutant_sha256']}
    if len(unique) != 5:
        raise RuntimeError('five independently validated mutation families required')
    source = programs['independent_exact_check'].read_text()
    for row in unique.values():
        if source.count(row['before']) != 1:
            raise RuntimeError('mutation anchor not unique')
        actual = hashlib.sha256(source.replace(row['before'], row['after'], 1).encode()).hexdigest()
        if actual != row['mutant_sha256']:
            raise RuntimeError('independent mutation pin differs')
    write_json(PUB / 'checks/SOURCE_MUTATIONS.json', unique)

    for source, name in ((ROOT / 'submitted', 'submitted'),
                         (ROOT / 'reviews/proximity_01', 'proximity_review_01'),
                         (ROOT / 'reviews/ring_hull_01', 'ring_hull_review_01'),
                         (ROOT / 'reviews/priority_01', 'priority_review_01')):
        for path in sorted(source.rglob('*')):
            if not path.is_file() or 'sources' in path.relative_to(source).parts:
                continue
            target = PUB / 'evidence' / name / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    for name in ('SUBMITTED_PINS.json', 'ROOT_MATH_AUDIT.md', 'ROOT_PRIORITY_ADOPTION.json'):
        shutil.copyfile(ROOT / name, PUB / 'evidence' / name)
    write_json(PUB / 'evidence/CURRENT_REVIEW_STATE.json', {
        'math': 'two independent families and root deductions passed',
        'priority': 'bounded audit, classical-lineage corrections adopted',
        'fresh_package_reviews': [], 'preprint_ready_for_immutable_publication': False,
        'all_actionable_issues_resolved': False, 'published': False})


if __name__ == '__main__':
    main()
