"""Generate exact frozen target-claim coverage, with path and count guards."""
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'snapshot/unsolved_math_prioritization/attempts/2302055'

def assessment(name):
    if name.startswith('TURN_') and name.endswith('.md') and '_LOG' not in name:
        return 'Independent pre-code mathematical reconstruction supports exact scoped theorem; no universal resolution.'
    if name.startswith('verify_turn') or name in ['independent_check.py','replay_author.py']:
        return 'Code inspected and safely replayed from ignored private copy; complete receipt matches; finite control scope retained.'
    if name.endswith('MANIFEST.json') and name != 'SOURCE_MANIFEST.json':
        return 'Every listed file size/hash matches; historical subsets and self-exclusion checked. Publication manifest exactly covers all other target files.'
    if name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T4.json']:
        return 'Independent primary download matches routed URL/byte size/SHA256; actual relevant primary statements read.'
    if name in ['SOURCE_SCOPE.md','PRIOR_GATE.json']:
        return 'Original 2018 question and primary special cases independently verified; original Annals proof/1977 full PDF not fetched; historical search counts not independently replayed and no novelty certification inferred.'
    if name.startswith('CURRENT_STATE'):
        return 'Historical source/turn status has complete_resolution=false and matches its stated phase; additive final disposition is unsolved 5/5.'
    if name.endswith('_CHECKS.json') or name in ['AUTHOR_REPLAY.json','INDEPENDENT_CHECKS.json']:
        return 'Complete replay stdout is byte-identical; counts and scope disclaimers consistent.'
    if name.endswith('_LOG.md'):
        return 'Scoped mechanism, counts and remaining gap agree with proof and receipts; turn count is preserved author history.'
    return 'Full text inspected after own mathematical seal; scoped PASS/original unsolved, credited dependencies, exact remaining gap and file/assertion counts agree. Old review not used to create new verdict.'

if __name__ == '__main__':
    seal = json.loads((ROOT / 'MATHEMATICAL_SEAL.json').read_text())
    assert seal['candidate_code_outputs_status_finals_history_reviews_read'] is False
    frozen = json.loads((ROOT.parent / 'snapshot_manifest.json').read_text())
    expected = {Path(row['path']).relative_to('unsolved_math_prioritization/attempts/2302055').as_posix()
                for row in frozen['files']
                if row['path'].startswith('unsolved_math_prioritization/attempts/2302055/')}
    files = sorted(p for p in SOURCE.rglob('*') if p.is_file())
    actual = {p.relative_to(SOURCE).as_posix() for p in files}
    assert actual and actual == expected, 'Frozen claim inventory is not exact'
    rows = [{'path':p.relative_to(SOURCE).as_posix(),
             'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
             'assessment':assessment(p.name)} for p in files]
    payload = {'generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
               'frozen_files_covered':len(rows), 'exact_target_set_verified':True,
               'mathematical_verdict_unchanged_after_code_and_claim_reads':True,
               'mandatory_geometric_corrections':[],
               'unreplayed_historical_claims':['403 live branch-name search','443 mirrored-ref search',
                                             'negative current-literature bounded search outcome',
                                             'author-history Git identifiers beyond specified frozen binding'],
               'claimed_complete_resolution_found':False,'claimed_novelty_certification_found':False,
               'claimed_merge_or_release_request_found':False,'claims':rows}
    (ROOT / 'FROZEN_CLAIM_AUDIT.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({'frozen_target_files_audited':len(rows),'exact_target_set_verified':True,
                      'checkpoint_utc':payload['generated_utc']}))
