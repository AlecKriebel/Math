"""One external root closure of the final clean third review, no owned writes."""
from pathlib import Path
import json
from root_submission_gate import A, AUTHOR_NAMES, Capture, inventory, load, pin, sha, utc

N = A / 'preprint_review_03'
assert not (A / 'ROOT_PREPRINT_REVIEW03_SEAL.json').exists()
assert not (A / 'ROOT_PREPRINT_REVIEW03_VERIFICATION.json').exists()
assert not (A / 'ROOT_FINAL_CLOSED_EVIDENCE.json').exists()
expected = {
    'FINAL_NAMESPACE_MANIFEST.json': (54693, '4f0f1b3943e609bf8c4ab7ff731a21eec21f21337b02572a5fcdd1ae8a5d90eb'),
    'FULL_PREPRINT_REVIEW.md': (24806, '3fa1a440aaba0296ed480d79f33b71ef65614729a41177b91b5f82803c651c24'),
    'READING_LEDGER.md': (10245, 'a60793ed06c574a1d127762f1190149b15cbc1cbcf1e1be351d5e856ba64c8be'),
    'VERDICT.json': (734, '73ef3f78efedced91f8ceda4a2c73893ce47a75c105ed266784860150867726e'),
    'verify_review.py': (6551, 'c14925e4ebb0310cd5df2f1848239be94860f7cb4e63da5852e769535fabdc1e'),
    'audit_relations.py': (9164, '0fd3f6a537f5463710d79af66ff4984fea29a5383b0cfe9281d1eadf0bd84f7a'),
    'RESEARCH_LOG.md': (2208, '8d5f37da85a517b966c2a0f1c81c28d11acef379320c7a2ba6889eea566eb0a1')}
for name, (size, digest) in expected.items():
    assert pin(N / name) == dict(bytes=size, sha256=digest, mode=0o644)
namespace = inventory(N)
assert len(namespace['files']) == 265 and len(namespace['directories']) == 16
manifest = load(N / 'FINAL_NAMESPACE_MANIFEST.json')
assert manifest['scope'] == 'Every file and directory; only own manifest bytes excluded'
assert manifest['not_self_sealed'] and manifest['external_root_rehearsal_required']
actual = {name: dict(type='directory', mode=oct(mode))
          for name, mode in namespace['directories'].items()}
actual.update({name: dict(type='file', size=entry['bytes'], mode=oct(entry['mode']), sha256=entry['sha256'])
               for name, entry in namespace['files'].items()})
actual['FINAL_NAMESPACE_MANIFEST.json'] = dict(type='file', mode='0o644', own_bytes_excluded=True)
assert actual == manifest['entries']
verdict = load(N / 'VERDICT.json')
assert verdict['scientific_verdict'] == 'CLEAN_NO_MANDATORY_CHANGES'
assert verdict['mandatory_findings'] == verdict['actionable_author_repairs'] == []
inputs = {name: dict(bytes=entry['size'], sha256=entry['sha256'], mode=int(entry['mode'], 8))
          for name, entry in load(N / 'candidate_inputs.json')['inputs'].items()}
assert set(inputs) == set(AUTHOR_NAMES) and len(inputs) == 8
assert inputs == load(A / 'preprint/REVIEW_PACKET_MANIFEST.json')['author_inputs']
assert {name: pin(A / 'preprint' / name) for name in inputs} == inputs
for name, entry in inputs.items():
    assert pin(N / 'candidate' / name) == entry

closed_names = ('honda_lifting', 'intrinsic_invariants', 'semilinear_modules',
                'priority_supersingular_mechanism', 'priority_audit',
                'preprint_review_01', 'preprint_review_02', 'preprint_review_03')
closed = {name: inventory(A / name) for name in closed_names}
math = load(A / 'ROOT_MATHEMATICAL_ACCEPTANCE.json')
for family in closed_names[:3]:
    assert closed[family]['files'] == math['families'][family]['whole_current_namespace']
for number in (1, 2):
    seal = load(A / f'ROOT_PREPRINT_REVIEW0{number}_SEAL.json')['namespace_inventory']
    family = closed[f'preprint_review_0{number}']
    assert family['files'] == {name: dict(bytes=entry['bytes'], sha256=entry['sha256'], mode=int(entry['mode'], 8))
                               for name, entry in seal['files'].items()}
    assert family['directories'] == {'.': int(seal['root_mode'], 8),
                                     **{name: int(mode, 8) for name, mode in seal['directories'].items()}}
# Preserve the entire current namespaces; also check the earlier scientific
# manifests. The earlier private runtime snapshots are not retroactively
# claimed to have been intellectually reread.
mechanism_manifest = load(A / 'priority_supersingular_mechanism/MANIFEST.json')
priority_manifest = load(A / 'priority_audit/DRAFT_AUDIT_MANIFEST.json')
for family, frozen in [('priority_supersingular_mechanism', mechanism_manifest),
                       ('priority_audit', priority_manifest)]:
    for entry in frozen.get('payloads', frozen.get('entries')):
        path = entry.get('path', entry.get('relative_path'))
        current = closed[family]['files'][path]
        assert current['bytes'] == entry.get('bytes', entry.get('size'))
        assert current['sha256'] == entry['sha256']
        if 'mode' in entry:
            mode = entry['mode']
            assert current['mode'] == (int(mode, 8) if isinstance(mode, str) else mode)

source = load(A / 'ROOT_PREPRINT03_SOURCE_GATE.json')['source_only_freeze']
first = load(A / 'ROOT_PREPRINT03_FIRST_ASSESSMENT_GATE.json')['freeze']
for entry in (source, first):
    assert pin(A / entry['path']) == dict(bytes=entry['bytes'], sha256=entry['sha256'], mode=int(entry['mode'], 8))
receipt_summary = []
for path in sorted((N / 'receipts').glob('*.json')):
    record = load(path)
    for kind in ('stdout', 'stderr'):
        entry = record[kind]
        assert pin(path.with_suffix('.' + kind)) == dict(bytes=entry['size'], sha256=entry['sha256'], mode=int(entry['mode'], 8))
    receipt_summary.append(dict(name=path.name, command=record['command'], cwd=record['cwd'],
                                started_utc=record['started_utc'], ended_utc=record['ended_utc'],
                                exit_code=record['exit_code'], stdout=record['stdout'], stderr=record['stderr']))

capture = Capture('review03_external_root_closure')
runtimes = ('/opt/homebrew/bin/python3',
            '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
for index, runtime in enumerate(runtimes):
    result = capture.run(f'independent_{index}', [runtime, '-B', N / 'independent_controls.py'], cwd=N)
    assert not result.stderr and result.stdout == (N / 'receipts/independent-py314.stdout').read_bytes()
    assert json.loads(result.stdout)['checks'] == 3278
mutations = load(N / 'mutation_summary.json')['mutations']
assert len(mutations) == 8
for index, row in enumerate(mutations):
    record = load(N / 'receipts' / (row['receipt'] + '.json'))
    command = record['command']
    assert command[0] in runtimes and command[1] == '-B'
    assert Path(command[2]).resolve().is_relative_to(N)
    result = capture.run('direct_negative_' + str(index), command, cwd=record['cwd'], ok=(1,))
    assert result.returncode == record['exit_code'] == 1 and result.stdout == b''
    assert result.stderr == (N / 'receipts' / (row['receipt'] + '.stderr')).read_bytes()
    assert b'Traceback' in result.stderr and b'manifest' not in result.stderr.lower()

full_results = []
for index, runtime in enumerate(runtimes):
    for mode, flags, expected_replays in [('public', [], 4), ('full', ['--full'], 26)]:
        result = capture.run(f'verifier_{index}_{mode}', [runtime, '-B', N / 'verify_review.py', *flags], cwd=N)
        assert not result.stderr
        parsed = json.loads(result.stdout)
        assert parsed['integrity'] == 'PASS' and parsed['mode'] == mode
        assert parsed['scientific_verdict'] == 'CLEAN_NO_MANDATORY_CHANGES'
        assert parsed['mandatory_findings'] == [] and parsed['scientific_clearance']
        assert parsed['namespace_unchanged'] and not parsed['external_source_paths_read']
        assert parsed['relations']['author_inputs'] == 8 and parsed['relations']['zip_members'] == 33
        assert len(parsed['actual_fresh_replays']) == expected_replays
        assert all(event['exit_code'] in (0, 1) for event in parsed['actual_fresh_replays'])
        if mode == 'full':
            assert sum(event['exit_code'] == 1 for event in parsed['actual_fresh_replays']) == 8
        full_results.append(dict(runtime=runtime, mode=mode, complete_output_pin=capture.entries[-1]['streams']['stdout'],
                                 native_replay_count=expected_replays, whole_output_parsed_and_all_relations_verified=True))
assert {name: inventory(A / name) for name in closed_names} == closed
assert {name: pin(A / 'preprint' / name) for name in inputs} == inputs
assert {name: pin(N / name) for name in expected} == {
    name: dict(bytes=size, sha256=digest, mode=0o644) for name, (size, digest) in expected.items()}
time = utc()
seal = dict(utc=time, status='NEW_THIRD_CLEAN_FULL_PREPRINT_REVIEW_EXTERNALLY_CLOSED',
            reviewer='/root/pr344_preprint_03', namespace_inventory=namespace,
            manifest=pin(N / 'FINAL_NAMESPACE_MANIFEST.json'), scientific_verdict='CLEAN_NO_MANDATORY_CHANGES',
            mandatory_findings=[], no_owned_namespace_write=True,
            native_capture_directory=str(capture.directory), not_a_self_process_receipt=True)
(A / 'ROOT_PREPRINT_REVIEW03_SEAL.json').write_text(json.dumps(seal, indent=2) + '\n')
verification = dict(utc=utc(), status='REVIEW_COMPLETE_NO_UNRESOLVED_MANDATORY_FINDINGS',
                    mandatory_findings=0, main_theorem_valid=True, classical_mechanism_valid=True,
                    generic_helper_valid=True, closed_namespace_unchanged=True,
                    whole_verifier_output_compared=True, source_first_and_premath_gates_preserved=True,
                    sealed_author_inputs=inputs, all_required_source_scopes_read=True,
                    full_packet_bytes_and_metadata_verified=True,
                    root_independent_controls_reproduced=True, root_negative_controls_reproduced=True,
                    actual_independent_native_runs=2, actual_direct_negative_runs=8,
                    actual_public_full_verifier_runs=4, verifier_results=full_results,
                    historical_native_receipts=receipt_summary,
                    review_seal_sha256=sha((A / 'ROOT_PREPRINT_REVIEW03_SEAL.json').read_bytes()),
                    namespace_manifest_sha256=pin(N / 'FINAL_NAMESPACE_MANIFEST.json')['sha256'],
                    root_complete_read_scope=['Full final report, actual ledger, verdict, research log, four scientific/verification programs, complete independent positive output and all eight complete negative tracebacks, exact source/input inventories and native receipt relations.',
                                              'Root independently verified operative primary sources in the preceding mathematical and priority audits; no claim to reread every raw original in full.'],
                    native_capture_directory=str(capture.directory), program=pin(Path(__file__)),
                    publication_clearance=False, math_percent=100, priority_percent=100, workflow_percent=60)
(A / 'ROOT_PREPRINT_REVIEW03_VERIFICATION.json').write_text(json.dumps(verification, indent=2) + '\n')
evidence = dict(utc=utc(), status='ALL_EIGHT_CLOSED_NAMESPACES_PINNED_AFTER_CLEAN_REVIEW03',
                namespaces=closed, all_namespaces_unchanged_through_actual_root_replay=True,
                historical_first_second_adverse_verdicts_preserved=True,
                no_claim_to_full_intellectual_reading_of_all_raw_primary_bodies=True)
(A / 'ROOT_FINAL_CLOSED_EVIDENCE.json').write_text(json.dumps(evidence, indent=2) + '\n')
print(json.dumps({key: value for key, value in verification.items()
                  if key not in ('historical_native_receipts', 'sealed_author_inputs')}, indent=2))
