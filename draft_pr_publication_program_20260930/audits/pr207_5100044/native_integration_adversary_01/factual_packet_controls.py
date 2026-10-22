"""Read-only independent checks of the exact documentary finalization packet.

This checks files and Root's pinned event attestations, without making a remote
service call or re-reviewing the frozen mathematical result.
"""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).absolute().parent
A = HERE.parent
C = A.parents[2]
F = A / 'finalized_current_01'
N = A / 'native_revision_preparation_01'
S = A / 'publication_package_v1'
PREFIX = 'payload/unsolved_math_prioritization/attempts/5100044/'


def check(ok, message):
    if ok is not True:
        raise RuntimeError(message)


def pin(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def read(path, wanted=None, readonly=False):
    check(path.resolve() == path and path.is_file() and (not readonly or path.stat().st_mode & 0o777 == 0o444), 'Canonical pinned source ' + str(path))
    raw = path.read_bytes()
    if wanted is not None:
        check(pin(raw) == wanted, 'Input byte pin ' + str(path))
    return raw


def delta(a, b, path=()):
    if type(a) is dict and type(b) is dict:
        for key in set(a) | set(b):
            if key not in a or key not in b:
                yield path + (key,)
            else:
                yield from delta(a[key], b[key], path + (key,))
    elif type(a) is not type(b) or a != b:
        yield path


def run():
    check(sys.flags.ignore_environment == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode is True and sys.flags.safe_path is True and not sys.flags.optimize, 'Ordinary isolated Python required')
    checks = []
    def passed(name):
        checks.append(dict(control=name, result='PASS'))
    rules = json.loads(read(A / 'factual_finalization_preparation_01/FACTUAL_FINALIZATION_RULES.json', dict(bytes=2647, sha256='9028ea071ee69bfcbf6c37fd4f7ec91c72cebd744ce7f5f8aa7e4316efde863e')))
    read(F / 'FINALIZATION_SEAL.json', dict(bytes=569, sha256='40aca2dfdf1d57beffdab11c25274c004e25fe70e63a6888a5d057fb9cff0a1a'))
    final = json.loads(read(F / 'FINALIZATION_MANIFEST.json', dict(bytes=5121, sha256='4bec7494322ab85caab606f6ba7db1f69adc213bf70d07624319a8fb168a3b7a')))
    for name, identity in final['files'].items():
        read(F / name, identity, readonly=True)
    check(len(final['files']) == final['file_count'] == 26 and sum(x['bytes'] for x in final['files'].values()) == final['total_bytes'] == 159564, 'Final exact file/byte totals')
    passed('26_finalized_packet_files_canonical_0444_and_exact_pins')
    original = json.loads(read(N / 'PROPOSAL_MANIFEST.json', dict(bytes=7230, sha256='f9f5b31b2e049731964686da9e6abe48ac34f0f217ceb0a4e0c9dae91c55a780')))
    for name, identity in original['files'].items():
        read(N / name, identity)
    read(N / 'SEAL.json', rules['frozen_proposal_seal'])
    passed('complete_frozen_native_proposal_remains_byteexact')
    package = json.loads(read(S / 'PACKAGE_SEAL.json', rules['frozen_package_seal']))
    science = json.loads(read(S / 'PACKAGE_MANIFEST.json', package['scientific_manifest']))
    for row in science['files']:
        read(S / row['path'], {k: row[k] for k in ('bytes', 'sha256')})
    check(science['file_count'] == len(science['files']) == 45 and science['total_bytes'] == sum(x['bytes'] for x in science['files']) == 310204, 'Frozen science totals')
    for filename, key in [('focal_inversion_area.tex', 'TeX'), ('focal_inversion_area.pdf', 'PDF'), ('verification_package.zip', 'ZIP'), ('METADATA.json', 'metadata'), ('zenodo-deposit.json', 'deposit_manifest')]:
        read(S / filename, package[key])
    passed('frozen_science_45_files_and_exact_TeX_PDF_ZIP_metadata_seals_unchanged')
    custody = json.loads(read(A / 'native_integration_preparation_01/CUSTODY_INVENTORY.json', dict(bytes=6874, sha256='6923e78c3306a40bba66cdbe1a7b901b811a7d3ef51a07824ca3d81ed62d8e40')))
    for name, identity in custody.items():
        read(A / 'submitted_snapshot' / name, {k: identity[k] for k in ('bytes', 'sha256')})
    check(len(custody) == 20 and sum(x['bytes'] for x in custody.values()) == 61131, 'Original archive totals')
    passed('20_original_archive_files_61131_bytes_unchanged')
    changed = []
    unchanged = []
    json_changes = {}
    allowed_top = {
        'MANIFEST.json': {'created_utc', 'role', 'files'},
        'PUBLICATION_MANIFEST.json': {'PDF', 'Root_publication_gate', 'Root_publication_receipt', 'Root_tracker_receipt', 'finalized_utc', 'manifest', 'manuscript', 'package_seal', 'publication_doi', 'publication_doi_status', 'publication_ready', 'publication_record_url', 'schema', 'verification_ZIP', 'whole_package_review'},
        'independent_review/reviewed_hashes.json': {'created_utc', 'files', 'role', 'schema', 'whole_package_review'},
        'metadata.json': {'Root_publication_gate', 'Root_publication_receipt', 'Root_tracker_receipt', 'finalized_utc', 'package_seal', 'publication_doi', 'publication_doi_status', 'publication_ready', 'publication_record_url', 'schema', 'whole_package_review'},
        'source_manifest.json': {'publication_doi'},
    }
    for name in final['files']:
        if not name.startswith(PREFIX):
            continue
        short = name.removeprefix(PREFIX)
        old, new = read(N / name), read(F / name)
        (changed if old != new else unchanged).append(short)
        if old != new and short.endswith('.json'):
            paths = sorted(delta(json.loads(old), json.loads(new)))
            check(short in allowed_top and all(path[0] in allowed_top[short] for path in paths), 'Forbidden current JSON assertion change')
            json_changes[short] = [list(x) for x in paths]
    check(len(changed) == 12 and len(unchanged) == 10, 'Exact changed/unchanged partition')
    expected_unchanged = {'current_execution_receipt.json', 'independent_review/SOURCE_NOTES.md', 'independent_review/author_rerun_verification.json', 'independent_review/independent_check.py', 'independent_review/independent_output.json', 'prior_imported_report.json', 'requirements.txt', 'source_record.json', 'verification.json', 'verify.py'}
    check(set(unchanged) == expected_unchanged, 'Code/run/sourcecontract/history identity')
    passed('22_native_files_exact12_documentary_changes_and10_immutable_files')
    old_proof, new_proof = [(base / (PREFIX + 'PROOF.md')).read_bytes() for base in (N, F)]
    def analytic(raw):
        return raw[raw.index(b'## 1. Target, edition and normalization'):raw.rindex(b"Stachel's canonical theorem")]
    check(analytic(old_proof) == analytic(new_proof), 'Analytic proof body changed')
    def credit(raw):
        start = raw.rindex(b"Stachel's canonical theorem")
        finish = raw.index(b'No theorem or method novelty is claimed.', start) + len(b'No theorem or method novelty is claimed.')
        return raw[start:finish]
    check(credit(old_proof) == credit(new_proof), 'Mathematical credit/novelty changed')
    old_sources, new_sources = [(base / (PREFIX + 'SOURCES.md')).read_bytes() for base in (N, F)]
    check(old_sources[:old_sources.index(b'The scoped mathematics')] == new_sources[:new_sources.index(b'The scoped mathematics')], 'Source/attribution body changed')
    old_log, new_log = [(base / (PREFIX + 'RESEARCH_LOG.md')).read_bytes() for base in (N, F)]
    check(new_log.startswith(old_log), 'Earlier research log rewritten')
    passed('proof_analytic_body_credit_source_attribution_and_prior_log_byteexact')
    current = F / PREFIX
    for filename in ['MANIFEST.json', 'independent_review/reviewed_hashes.json']:
        obj = json.loads(read(current / filename))
        for path, identity in obj['files'].items():
            read(current / path, identity)
    publication = json.loads(read(current / 'PUBLICATION_MANIFEST.json'))
    read(current / publication['manifest']['path'], {k: publication['manifest'][k] for k in ('bytes', 'sha256')})
    for filename in ['PUBLICATION_MANIFEST.json', 'metadata.json']:
        obj = json.loads(read(current / filename))
        for value in obj.values():
            if type(value) is dict and 'repository_path' in value and 'sha256' in value:
                read(C / value['repository_path'], {k: value[k] for k in ('bytes', 'sha256')})
        known_key = 'known_result_doi' if filename == 'PUBLICATION_MANIFEST.json' else 'known_theorem_doi'
        check(obj['publication_doi'] == '10.5281/zenodo.23428090' and obj[known_key] == '10.5281/zenodo.23093706' and obj['publication_ready'] is True, 'DOI identity/readiness')
    passed('current_dependent_inventories_and_repository_asset_event_pins_consistent')
    pub = json.loads(read(A / 'ROOT_ACTUAL_PUBLICATION_01.json', dict(bytes=3517, sha256='b185725e145968fa2cbee89df27a6280378ef5d50da4319cd62ce236a346ce9b')))
    tracker = json.loads(read(A / 'ROOT_ACTUAL_TRACKER_01.json', dict(bytes=2311, sha256='4be14f01cb6dad4dcdfa1cf7f7512a1dcd29bdf1de1ff4f8510d6402d4254f70')))
    check(pub['evidence_scope'] == tracker['evidence_scope'] == 'ACTUAL_ROOT_RECEIPT' and pub['accepted'] is True and tracker['accepted'] is True, 'Actual Root event attestations')
    check(pub['doi'] == tracker['doi'] == publication['publication_doi'] and pub['published'] is True and pub['all_four_files_verified'] is True and pub['exact_intended_metadata_verified'] is True and tracker['native_readback_verified'] is True and tracker['range'] == "'Math Puzzles'!A134:D134", 'Actual Root event identity/readback')
    check(pub['goal_complete'] is False and tracker['goal_complete'] is False and pub['fully_completed_count'] == tracker['fully_completed_count'] == 49 and pub['published_count'] == tracker['published_count'] == 34, 'Publication/tracker do not imply case completion')
    passed('documentary_facts_match_exact_Root_event_attestations_without_service_calls')
    final_pr = json.loads(read(F / 'FINAL_PR_METADATA.json'))
    check(final_pr['preserved_ledger_status'] == 'claimed_solved' and final_pr['preserved_ledger_effort'] == '1/5' and final_pr['actual_model_or_effort_verified'] is None and final_pr['author_work_turns_verified'] is None and final_pr['advance_or_merge_authorized_by_this_file'] is False, 'PR current aliases/authority boundary')
    passed('PR_metadata_preserves_literal_ledger_and_unverified_effort_authority_boundary')
    return dict(schema='pr207-independent-factual-packet-controls-v1', evidence_scope='READ_ONLY_FROZEN_FILES_AND_ROOT_ATTESTATIONS', live_service_independent_verification_performed=False, actual_events_created=False,
                checks=checks, check_count=len(checks), changed_native_files=changed, unchanged_native_files=unchanged, JSON_changed_paths=json_changes,
                finalized_manifest_pin=dict(bytes=5121, sha256='4bec7494322ab85caab606f6ba7db1f69adc213bf70d07624319a8fb168a3b7a'))


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
