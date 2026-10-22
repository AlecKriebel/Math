"""Check bounded audit metadata after the external strict-inventory bootstrap."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: isolated bootstrap required')
import json
from pathlib import Path

root = Path(__file__).resolve().parent
acceptance = json.loads((root / 'ACCEPTANCE.json').read_bytes())
replay = json.loads((root / 'INDEPENDENT_REPLAY.json').read_bytes())
corpus = json.loads((root / 'CORPUS_BINDINGS.json').read_bytes())
sources = json.loads((root / 'SOURCE_CHECKS.json').read_bytes())
if acceptance.get('problem_id') != 10300026 or acceptance.get('catalog_rank') != 844:
    raise SystemExit('REJECT: identity')
if acceptance.get('disposition') != 'ACCEPTED_SCOPED_AUDIT_NO_GENERAL_SOLUTION':
    raise SystemExit('REJECT: disposition')
if acceptance.get('full_solution') is not False or acceptance.get('new_mathematical_result_claimed') is not False:
    raise SystemExit('REJECT: unsupported success')
if acceptance.get('substantive_approaches') != 4 or acceptance.get('elementary_lemmas_reviewed') != 4:
    raise SystemExit('REJECT: accounting')
if acceptance.get('mathematical_patch_required') is not False or acceptance.get('author_v2_immutable') is not True:
    raise SystemExit('REJECT: preservation')
if replay.get('all_tests_pass') is not True or replay.get('test_count') != 45 or len(replay.get('tests', [])) != 45 or not all(x.get('pass') is True for x in replay['tests']):
    raise SystemExit('REJECT: recorded replay')
if corpus.get('statement_match') is not True or corpus.get('review_match') is not True or corpus.get('review_sha256') != 'd539a48fb43e8d346651b0e11607b0e6315c856cdaec3d0d156d348c4d77aca2':
    raise SystemExit('REJECT: corpus bindings')
if sources.get('all_six_original_pdf_hashes_match') is not True or sources.get('all_six_fresh_text_extractions_match') is not True:
    raise SystemExit('REJECT: source verification')
print(json.dumps({'problem_id': 10300026, 'audit_metadata': 'PASS', 'full_solution': False, 'mathematical_proof_checked_by_program': False}, sort_keys=True))
