"""Create local input receipts, independent seal, and safe authored manifest."""
import datetime, hashlib, json, pathlib

BASE = pathlib.Path(__file__).resolve().parent
STAMP = datetime.datetime.now(datetime.timezone.utc).isoformat()
FROZEN = BASE.parent / 'submitted/unsolved_math_prioritization/attempts/30006020'
input_pins = []
for name in ['CANDIDATE.md', 'TARGET.json', 'source_manifest.json']:
    path = FROZEN / name
    input_pins.append({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size})
(BASE / 'FROZEN_INPUT_PINS.json').write_text(json.dumps({'read_scope': 'Only these frozen submitted artifacts were read; no root or sibling review content.', 'files': input_pins}, indent=2) + '\n')

seal = {
    'sealed_at_utc': STAMP,
    'identity': 'priority_novelty_challenge_01',
    'proof_gate': 'Assumed separately passed; not a fresh proof acceptance.',
    'result': 'novelty_not_falsified_by_bounded_primary_audit',
    'already_solved_evidence_found': False,
    'first_priority_certified': False,
    'original_concrete_scope_covered_if_proof_sound': True,
    'theorem_A_assessment': 'Short new articulation/corollary of old uniform geometry and weighted permutation model.',
    'potential_new_delta': 'Geometric all-rate mesoscopic PPP and fixed joint window moments, including original example.',
    'main_unresolved_lead': 'Announced Delecroix-Liu Small components work; complete public text not located.',
    'independent_of_root_and_sibling_reviews': True,
    'writes_confined_to': str(BASE),
    'external_communications': 'None; public literature reads only.',
    'git_index_ref_or_provider_writes': 'None',
    'private_payload_directory': 'private/ (ignored by local .gitignore)',
    'bounded_audit_completion_estimate_percent': 100,
}
(BASE / 'INDEPENDENT_SEAL.json').write_text(json.dumps(seal, indent=2) + '\n')
log = BASE / 'RESEARCH_LOG.md'
with log.open('a') as f:
    f.write('\n' + STAMP + ' — Sealed bounded priority challenge. Completion estimate: 100% of the requested adversarial audit; first-priority certification remains unresolved, as explicitly recorded. Strongest verified result: no checked same ensemble earlier mesoscopic theorem, with substantial old-proof overlap. Exact remaining gap: announced Small components work and broader assembly theorem assumptions. No root/sibling review read; no Git/index/ref mutation, outreach, manuscript, depositor/tracker, or provider write.\n')

files = []
for path in sorted(BASE.iterdir()):
    if path.is_file() and path.name != 'SAFE_AUTHORED_MANIFEST.json':
        files.append({'path': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size})
manifest = {'created_at_utc': STAMP, 'scope': str(BASE), 'policy': 'Only authored report, analysis, operational scripts, and safe provenance metadata. Excludes complete external reading, raw payloads, rendered pages, and Python bytecode.', 'excluded_directories': ['private/', '__pycache__/'], 'files': files}
(BASE / 'SAFE_AUTHORED_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'sealed_at_utc': STAMP, 'safe_authored_files': len(files), 'report_sha256': hashlib.sha256((BASE / 'REPORT.md').read_bytes()).hexdigest(), 'verdict': seal['result']}, indent=2))
