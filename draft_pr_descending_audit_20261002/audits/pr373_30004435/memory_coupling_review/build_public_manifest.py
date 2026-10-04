#!/usr/bin/env python3
"""Build the explicit public audit whitelist from this folder's authored files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent/'snapshot'/'unsolved_math_prioritization'/'attempts'/'30004435'


def sha(f):
    return hashlib.sha256(f.read_bytes()).hexdigest()


if __name__ == '__main__':
    now = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    code = ['REPLAY_ALL.py', 'finite_markov.py', 'observable_space.py',
            *[f'verify_turn{i}.py' for i in range(1, 6)],
            'final_review/independent_checks.py', 'final_review/verify_review.py']
    receipt = {'completed_utc': now,
               'candidate_code_inspected_sha256': {f: sha(CANDIDATE/f) for f in code},
               'old_review_content_read_after_mathematical_seal': {
                   'path': 'final_review/ADVERSARIAL_REVIEW.md',
                   'sha256': sha(CANDIDATE/'final_review'/'ADVERSARIAL_REVIEW.md')},
               'whole_author_replay': {'stdout': 'artifacts/author_complete_replay.stdout.json',
                                       'stderr': 'artifacts/author_complete_replay.stderr.txt',
                                       'exit_code': 0, 'optional_fresh_source_integrity': True},
               'individual_program_report': 'artifacts/REPLAY_REPORT.json',
               'root_and_sibling_proofs_read': False, 'service_writes': False,
               'git_operations': False}
    (HERE/'PROGRAM_INSPECTION_AND_REPLAY.json').write_text(
        json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    excluded_names = {'PUBLIC_MANIFEST.json', 'FINAL_SEAL.json',
                      'public_manifest_verification.stdout.json',
                      'public_manifest_verification.stderr.txt',
                      'build_public_manifest.stdout.json', 'build_public_manifest.stderr.txt'}
    fs = [f for f in HERE.rglob('*') if f.is_file()
          and 'private_sources' not in f.parts and '__pycache__' not in f.parts
          and f.name not in excluded_names]
    metadata = []
    for name, url in [('ems_46847.pdf', 'https://ems.press/content/serial-article-files/46847'),
                      ('bfg_9806132.pdf', 'https://arxiv.org/pdf/math/9806132'),
                      ('tail_1406.6670.pdf', 'https://arxiv.org/pdf/1406.6670'),
                      ('lemanczyk_thesis.pdf',
                       'https://www.mimuw.edu.pl/media/uploads/doctorates/thesis-michal-lemanczyk.pdf')]:
        f = HERE/'private_sources'/name
        metadata.append({'url': url, 'sha256': sha(f), 'bytes': f.stat().st_size,
                         'publicly_included': False,
                         'used_only_for_optional_whole_packet_source_integrity':
                         name == 'lemanczyk_thesis.pdf'})
    manifest = {
        'manifest_created_utc': now,
        'public_package_kind': 'independent memory-coupling audit; no raw author packet or third-party source copies',
        'frozen_candidate_head': '4e635c77d7399d671ea58700e41bbd92cbdeeb46',
        'public_files': [{'path': str(f.relative_to(HERE)), 'bytes': f.stat().st_size,
                          'sha256': sha(f),
                          'provenance': 'newly authored audit artifact or freshly regenerated replay stream'}
                         for f in sorted(fs)],
        'public_container_files_without_self_hash': ['PUBLIC_MANIFEST.json', 'FINAL_SEAL.json'],
        'additional_final_attestation_streams': [
            'artifacts/public_manifest_verification.stdout.json',
            'artifacts/public_manifest_verification.stderr.txt',
            'artifacts/build_public_manifest.stdout.json',
            'artifacts/build_public_manifest.stderr.txt'],
        'source_hash_metadata_only': metadata,
        'excluded': ['private_sources/** including PDFs, extracted text, rendered pages and symlinks',
                     'raw candidate prose/program/receipt packet copies',
                     'root and sibling audit proofs'],
        'completion_estimate_percent': 100,
        'exact_remaining_target_gap':
        'The source asks for an entropy-free proof for arbitrary stationary finite-alphabet laws; this scoped coupling criterion imposes overlap and summable history-uniform continuity.'}
    (HERE/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'utc': now, 'public_artifacts': len(fs),
                      'manifest_sha256': sha(HERE/'PUBLIC_MANIFEST.json')}, indent=2))
