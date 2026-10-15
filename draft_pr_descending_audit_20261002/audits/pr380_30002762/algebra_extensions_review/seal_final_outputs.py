from pathlib import Path
import datetime
import hashlib
import json

A = Path(__file__).resolve().parent
R = A.parent
HEAD = '9946a67cf8a1f7e3130d2a12de902db05875283a'
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
preseal = json.loads((A / 'PRECOMPARISON_SEAL.json').read_text())
for entry in preseal['files']:
    b = (A / entry['path']).read_bytes()
    assert hashlib.sha256(b).hexdigest() == entry['sha256'] and len(b) == entry['bytes']
inspection_names = ['TURN_1.md', 'TURN_2.md', 'TURN_3.md',
                    'check_turn_1.py', 'check_turn_2.py', 'check_turn_3.py',
                    'check_turn_4.py', 'check_turn_5.py', 'REPLAY_ALL.py',
                    'verify_publication.py', 'review/independent_check.py',
                    'review/REVIEW.md', 'FINAL_RESULT.md',
                    'FINAL_REVIEW_REQUEST.md', 'README_PUBLICATION.md']
target = R / 'snapshot' / 'problems' / '30002762_conjugation_norms'
inspection = {'recorded_utc': utc, 'head': HEAD,
              'inspection_order': ['primary EMS source and metadata/source index',
                                   'independent proof and fresh controls',
                                   'immutable precomparison seal',
                                   'complete Turns1–3 proof texts and all replay code',
                                   'private complete portable replay',
                                   'earlier review and final summaries',
                                   'rechecked all44 Git/snapshot/private bindings and scoped replays'],
              'files_fully_read': [{'path': str(f),
                                    'bytes': (target / f).stat().st_size,
                                    'sha256': hashlib.sha256((target / f).read_bytes()).hexdigest()}
                                   for f in inspection_names],
              'scope_limit': 'Turns4–5 mathematical proof texts not audited by this family; their replay code was fully inspected and executed as part of full portable replay.'}
(A / 'INSPECTION_RECEIPT.json').write_text(json.dumps(inspection, indent=2) + '\n')
log = f'''# Post-seal checkpoint log\n\n- 2026-10-03T03:34:52.354934+00:00: Independent reconstruction and 71,921 fresh exact controls sealed. Scoped completion estimate 55%; exact remaining gap was candidate comparison and full replay. The earlier RESEARCH_LOG.md remains immutable inside that seal.\n- 2026-10-03T03:35–03:36Z: Complete candidate Turns1–3 proofs and all replay code inspected. No mandatory algebraic repair found. First private replay preparation failed before execution with a shell temporary-file "no space left on device" error. Disk availability was checked; no other family's files were deleted by this agent. Parent reported a scoped removal of its own ignored/untracked prior-audit temporary copies.\n- 2026-10-03T03:36:16.832483+00:00: Successful private full portable replay started. It reproduced 345,888 author assertions with62 manifest entries and0 optional source bindings; the old checker reproduced47,964 and the wrapper passed. Scoped completion estimate85%. Remaining gap: final exact-copy and scoped-output binding checks and report/seal.\n- {utc}: All44 exact Git/snapshot/private bindings rechecked; the precomparison seal remained unchanged; separately executed scoped checkers gave7,418/149,704/12,002 byte-exact assertions. Report and clean list completed. Scoped completion estimate100%. Strongest verified result: the exact metabelian bound, ambient virtually metabelian mechanism, and split abelian extension inheritance in Turns1–3. Original discovery completion is not estimated by this family; the original finite-presentation existence question remains unresolved. No novelty, whole-PR merge-readiness, queue/service disposition, or sixth author-search claim.\n'''
(A / 'CHECKPOINT_LOG.md').write_text(log)
files = []
for p in sorted(A.rglob('*')):
    if not p.is_file() or p.name == 'FINAL_OUTPUT_MANIFEST.json' or '__pycache__' in p.parts:
        continue
    b = p.read_bytes()
    files.append({'path': str(p.relative_to(A)), 'bytes': len(b),
                  'sha256': hashlib.sha256(b).hexdigest(),
                  'private_ignored': p.relative_to(A).parts[0] in ('private_sources', 'private_runs')})
manifest = {'sealed_utc': utc, 'head': HEAD,
            'snapshot_manifest_sha256': hashlib.sha256((R / 'snapshot_manifest.json').read_bytes()).hexdigest(),
            'precomparison_seal_sha256': hashlib.sha256((A / 'PRECOMPARISON_SEAL.json').read_bytes()).hexdigest(),
            'scope': 'PR380 Turns1–3 algebra and extensions; no service disposition',
            'file_count': len(files), 'files': files}
(A / 'FINAL_OUTPUT_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'head': HEAD, 'file_count': len(files),
                  'precomparison_seal_still_exact': True,
                  'final_output_manifest_sha256': hashlib.sha256((A / 'FINAL_OUTPUT_MANIFEST.json').read_bytes()).hexdigest()}, indent=2))
