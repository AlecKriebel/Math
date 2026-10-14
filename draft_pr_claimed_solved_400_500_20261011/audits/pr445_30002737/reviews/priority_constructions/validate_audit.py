#!/usr/bin/env python3
"""Validate this folder's frozen/source receipts and positive publication list.

No Git actions. No external network. No mathematical proof search.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
BASE=Path(__file__).resolve().parent
FROZEN=BASE.parents[1]/'source_snapshot'/'unsolved_math_prioritization'/'attempts'/'30002737'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,detail=None):
 checks.append({'name':name,'pass':bool(ok),'detail':detail})
receipt=json.loads((BASE/'FROZEN_READ_RECEIPT.json').read_text())
check('twelve_complete_frozen_reads',receipt['read_count']==12 and len(receipt['files'])==12 and all(x['read_complete'] is True for x in receipt['files']))
for x in receipt['files']:
 p=FROZEN/x['path'];check('frozen_'+x['path'],p.is_file() and p.stat().st_size==x['bytes'] and digest(p)==x['sha256'])
check('initial_independence_seal',digest(BASE/'INITIAL_PRIORITY.md')=='fbf3913b766b90169a417ff7d0fc5170775e0312d9cbae1e175946cd484e306f')
check('source_based_independence_seal',digest(BASE/'SOURCE_BASED_INDEPENDENCE.md')=='e34c1a5cc1432236fe6d3aec141504828c141dd0e0c3bb8c803917935343aa26')
source_names=['PRIMARY_SOURCE_RECEIPTS.json','ADDITIONAL_SOURCE_RECEIPTS.json','CONSTRUCTION_SOURCE_RECEIPTS.json','FACTOR_SOURCE_RECEIPTS.json','LATE_SOURCE_RECEIPTS.json','PUBLISHED_SPIN_RECEIPT.json','PUBLISHED_SPIN_RETRY_RECEIPTS.json']
for fn in source_names:
 items=json.loads((BASE/fn).read_text());items=items if isinstance(items,list) else [items]
 for x in items:
  if 'error' in x:continue
  p=BASE/x['private_path']
  check('private_source_'+x['name'],p.is_file() and p.stat().st_size==x['bytes'] and digest(p)==x['sha256'] and p.is_relative_to(BASE/'private_sources'))
result=json.loads((BASE/'RESULT.json').read_text())
for k in ['blocking_issue_count','priority_blocker_count','required_correction_count','optional_improvement_count','mathematical_correctness_reversal_count','earlier_recoverable_broad_resolution_count','earlier_matching_unweighted_geometric_resolution_located_count','frozen_artifacts_completely_read_count','independent_quadrature_certificate_count','new_original_proof_search_attempt_count','completion_estimate_percent']:
 check('integer_'+k,type(result[k]) is int)
check('counts_consistent',len(result['findings'])==result['priority_blocker_count'] and len(result['required_corrections'])==result['required_correction_count'] and len(result['optional_improvements'])==result['optional_improvement_count'])
check('no_unsupported_quadrature_claim',result['independent_quadrature_certificate_count']==0 and result['source_numeric_evidence']['independently_certified'] is False)
check('no_global_firstness_claim',result['global_novelty_clearance'] is False and result['earliest_resolution_established'] is False and result['precise_unweighted_meyer_novelty_established'] is False)
pub=json.loads((BASE/'PUBLIC_FILES.json').read_text())['files']
check('positive_allowlist_unique',len(pub)==len(set(pub)))
for name in pub:
 p=BASE/name
 check('public_'+name,p.is_file() and p.is_relative_to(BASE) and 'private_sources' not in p.parts and p.suffix not in ['.pdf','.png','.html'] and not p.is_symlink())
check('no_private_source_publication',all(not name.startswith('private_sources/') for name in pub))
check('report_present',bool((BASE/'PRIORITY_REPORT.md').read_text().strip()))
report={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'pass':all(x['pass'] for x in checks),'check_count':len(checks),'failure_count':sum(not x['pass'] for x in checks),'checks':checks,'scope':'artifact integrity, integer findings, honest numeric qualification and positive allowlist; no new mathematical proof'}
(BASE/'AUDIT_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['generated_at_utc','pass','check_count','failure_count']},indent=2))
if not report['pass']:raise SystemExit(1)
