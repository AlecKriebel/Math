"""Bind the final external ROOT clearance to the unchanged reviewed v1.1 kit."""
from pathlib import Path
import hashlib
import json

D = Path(__file__).resolve().parent.parent
R = Path(__file__).resolve().parent
A = D / 'audits/pr1032_30001739'


def read(path):
    return json.loads(path.read_text())


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    seal_path = A / 'CURRENT_FINAL_SEAL_20261016.json'
    seal = read(seal_path)
    require(seal['publication_ready'] is True, 'Final ROOT clearance required')
    count = seal['whole_reviews_completed']
    require(count >= 2 and seal['actionable_issues'] == 0,
            'Two complete reviews and zero remaining issues required')
    require(seal['Luo_Zha_overlap'] == 'UNKNOWN', 'Preserve unknown source comparison')
    manifest = A / 'publication/zenodo-deposit-v1_1.json'
    native = read(manifest)
    require(set(native) == {'metadata', 'files'} and len(native['files']) == 2,
            'Exact native manifest shape required')
    expected = [
        (106606, '1144eb3999212084bef013e7984bfc54bf43a9f931d959b63ba2743d814cf0a9'),
        (394529, '1f1a66d7e67b1434e4c17af96c9461b1d2f6bd7f4197de4ef88f95aad8105dc1'),
    ]
    files = []
    for item, target in zip(native['files'], expected):
        require(set(item) <= {'path', 'name'} and 'path' in item, 'Native file shape')
        path = (manifest.parent / item['path']).resolve()
        value = identity(path)
        require((value['bytes'], value['sha256']) == target, 'Reviewed asset changed')
        files.append({'path': str(path.relative_to(D)),
                      'name': item.get('name', path.name), **value})
    row = next(v for v in read(D / 'CLAIM_REGISTRY.json')['records'] if v['pr'] == 1032)
    require(row['head_oid'] == '810d52306312623ecfe01ecbc5f5f0dd360972c3',
            'Exact audited head required')
    metadata = native['metadata']
    url = 'https://github.com/AlecKriebel/Math/pull/1032'
    limits = ('Luo-Zha DOI10.1007/s11464-025-0256-0 full body unavailable and '
              'uninspected; exact, transformed, dual, twist, kernel and unitary '
              'overlap comparisons remain UNKNOWN. The result may overlap or '
              'be superseded. No novelty, firstness, worldwide current openness '
              'or separate kernel-generation disproof is asserted.')
    notes = (metadata['title'] + '. Accepted scope: ' + row['asserted_result'] +
             ' Limits: ' + limits + ' Prior theorem dependencies are credited. '
             'Extensive AI use; unrefereed; ' + str(count) +
             ' complete independent AI package reviews, latest zero actionable '
             'issues; no external human peer review or formal certification. '
             'Proof and verification: ' + url)
    config = {
        'pr': 1032, 'problem_id': str(row['problem_id']), 'head': row['head_oid'],
        'audit_folder': str(A.relative_to(D)),
        'manifest': str(manifest.relative_to(D)), 'manifest_identity': identity(manifest),
        'metadata_sha256': hashlib.sha256(json.dumps(metadata, sort_keys=True,
                                                     separators=(',', ':')).encode()).hexdigest(),
        'final_seal': str(seal_path.relative_to(D)),
        'final_seal_identity': identity(seal_path), 'fresh_complete_reviews': count,
        'files': files, 'title': metadata['title'], 'accepted_scope': row['asserted_result'],
        'limitations': limits,
        'tracker_original_problem': 'Catalogue problem 30001739; original formulation/proof provenance: ' + url,
        'tracker_notes': notes, 'pr_title': 'Accept 30001739: ' + metadata['title'],
        'historical_scope': 'Old priority refusals and preparation holds remain dated history. '
                            'The user accepted UNKNOWN/nonblocking source comparison; '
                            'the current external ROOT seal governs readiness.',
    }
    require(len(config['pr_title']) <= 256, 'PR title limit')
    target = R / 'PR1032_SERVICE_CONFIG.json'
    require(not target.exists(), 'Do not replace an existing operational service configuration')
    target.write_text(json.dumps(config, indent=2) + '\n')
    print(json.dumps({'status': 'FINAL_ROOT_CLEARANCE_AND_REVIEWED_BYTES_BOUND',
                      'pr': 1032, 'fresh_complete_reviews': count, 'files': files}))


if __name__ == '__main__':
    main()
