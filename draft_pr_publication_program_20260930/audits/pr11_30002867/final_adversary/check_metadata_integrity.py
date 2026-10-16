#!/usr/bin/env python3
"""Verify the frozen repaired metadata separately from immutable originals."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
CANDIDATE=AUDIT/'reviewed_candidate'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    frozen=json.loads((AUDIT/'candidate_freeze.json').read_text())
    checked=[]
    for e in frozen['files']:
        p=CANDIDATE/e['path']
        assert sha(p)==e['sha256'] and p.stat().st_size==e['size'], p
        checked.append(e)
    for line in (CANDIDATE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert sha(CANDIDATE/name)==digest, name
    assert len(checked)==15
    repairs=json.loads((AUDIT/'repair_manifest.json').read_text())
    for e in repairs['changes']:
        assert sha(AUDIT/'source_snapshot'/e['file'])==e['before_sha256']
        assert sha(CANDIDATE/e['file'])==e['corrected_sha256']
    changed={e['file'] for e in repairs['changes']}|set(repairs['new_files'])
    historical=[]
    for p in (AUDIT/'source_snapshot').rglob('*'):
        if p.is_file():
            name=p.relative_to(AUDIT/'source_snapshot').as_posix()
            if name not in changed:
                assert p.read_bytes()==(CANDIDATE/name).read_bytes(), name
                historical.append(name)
    readiness=json.loads((CANDIDATE/'readiness.json').read_text())
    current=sha(CANDIDATE/'CANDIDATE.md')
    original=sha(AUDIT/'source_snapshot/CANDIDATE.md')
    assert current==frozen['proof_sha256']==readiness['proof_sha256']==readiness['reviewed_proof_sha256']
    assert original==readiness['original_reviewed_proof_sha256']
    oldreview=json.loads((CANDIDATE/'independent_review/review_summary.json').read_text())
    assert oldreview['reviewed_sha256']==original
    assert readiness['new_paper'] is False and readiness['zenodo_deposit'] is False and readiness['tracker_row'] is False
    assert readiness['status']=='already_solved_by_equivalent_methods_pending_fresh_acceptance'
    assert readiness['acceptance_review']=='pending_fresh_complete_adversary'
    assert 'source provenance, not asserted as current' in (CANDIDATE/'SOURCE_AUDIT.md').read_text()
    assert 'Original review hashes identify the historical proof' in (CANDIDATE/'README.md').read_text()
    priority=[]
    priority_frozen=json.loads((AUDIT/'priority_artifact_manifest.json').read_text())
    for e in priority_frozen['files']:
        p=AUDIT/e['path']
        assert sha(p)==e['sha256'] and p.stat().st_size==e['size'], p
        priority.append(e)
    assert len(priority)==21
    path=AUDIT/'priority/exact_question'
    for line in (path/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert sha(path/name)==digest, name
    equivalent=json.loads((AUDIT/'priority/equivalent_methods/verdict.json').read_text())
    assert equivalent['disposition']=='already_solved'
    assert equivalent['search']['absence_of_earlier_identical_formula_proved'] is False
    assert equivalent['search']['named_historical_answer_to_2015_problem_asserted'] is False
    assert equivalent['exact_target']['original_locator'].endswith('p.1183')
    exact=json.loads((AUDIT/'priority/exact_question/VERDICT.json').read_text())
    assert exact['candidate_matches_literal_target'] is True
    assert exact['earlier_sufficient_methods'].startswith('ESTABLISHED_DERIVED_COMPOSITION')
    assert exact['composition_not_attributed_as_explicit_earlier_response'] is True
    manifest={'checked_at':datetime.now(timezone.utc).isoformat(),'status':'PASS',
              'reviewed_proof_sha256':current,'original_proof_sha256':original,
              'candidate_frozen_files':checked,'priority_hashes':priority,
              'historical_files_unchanged':historical,
              'repair_manifest_consistent':True,'current_paper_deposit_tracker_flags':False,
              'historical_source_open_status_preserved_only_as_provenance':True,
              'original_reviews_not_misattributed_to_new_proof':True}
    (HERE/'metadata_integrity_results.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('PASS current 15-file freeze, original/repaired hashes, historical fields, priority manifests and disposition')

if __name__=='__main__':
    main()
