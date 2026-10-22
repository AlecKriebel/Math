#!/usr/bin/env python3
"""Seal authored historical-audit artifacts; never includes source reading copies."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

p=Path(__file__).resolve().parent
now=datetime.now(timezone.utc).isoformat()
for name in ['COHERENT_RANK_CHECK.json','LRW_REFLECTION_CHECK.json']:
    data=json.loads((p/name).read_text())
    assert data['all_checks_passed'] is True
negative=json.loads((p/'LRW_REFLECTION_CHECK.json').read_text())['negative_control']
assert negative['disproves_no_extra_pile_assertion'] is True
assert (p/'history/LRW2001_ALL_JOINT_EQUIVALENCE_before_finite_prefix_count_repair.md').is_file()
report=p/'REPORT.md'
s=report.read_text()
start=s.index('UTC report: ')
end=s.index('. Scope completion:',start)
s=s[:start]+'UTC report: '+now+s[end:]
report.write_text(s)
status=dict(utc=now,scope_completion_percent=100,
            scope='Independent historical finite-pile/random-rank/Hammersley audit for PR246 /9700040',
            strongest_verified_conclusion='Published2001 off-diagonal no-jump determinant automatically evaluates every stationary joint survival probability via explicitly proved reflected-initial-row equivalence.',
            exact_remaining_gap='No claim that an older source literally displayed this stationary threshold formula as a resolution of Aldous2018, that the proposer accepted it, or that2001 is universally earliest. Parent promotion/synthesis is outside this family.',
            correction='Original no-extra-unrestricted-pile assertion preserved in history; current proof caps finite count at min(k,U), retains first-k autonomy, and includes an exact counterexample negative control.',
            independent_controls=dict(rank_max_n=8,rank_compatibility_equalities=255,
                                      LRW_raw_series_degree=7,LRW_max_k=5,LRW_pathwise_checks=11534),
            parent_reported_independent_review='Corrected bridge confirmed by another independently reconstructed family; not imported into this family own control counts.',
            no_external_outreach=True,no_provider_mutation=True,no_git_index_or_ref_changes=True)
(p/'FINAL_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
with (p/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n- {now}: Final checkpoint. Both independent exact controls replayed successfully; corrected LRW proof and original flawed history preserved. Source ledger and pins complete. Parent reports independent bridge confirmation; parent promotion remains separate. Completion estimate:100% of assigned historical family, with no worldwide-firstness or proposer-acceptance claim. Authored manifest sealed, excluding full third-party reading copies/text/images and provider data.\n')
items=[]
for f in sorted(p.rglob('*')):
    if not f.is_file() or 'private_reading' in f.relative_to(p).parts or f.name=='MANIFEST.json':
        continue
    b=f.read_bytes()
    items.append(dict(path=f.relative_to(p).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
manifest=dict(utc=now,scope='Authored artifacts only; includes superseded authored history clearly labeled as such.',
              excludes=['private_reading/**','third-party PDFs, full text, renders','provider payloads','MANIFEST.json (self-hash reported separately)'],
              files=items)
raw=(json.dumps(manifest,indent=2)+'\n').encode()
(p/'MANIFEST.json').write_bytes(raw)
print(json.dumps(dict(manifest_path=str(p/'MANIFEST.json'),manifest_bytes=len(raw),manifest_sha256=hashlib.sha256(raw).hexdigest(),authored_artifact_count=len(items)),indent=2))
