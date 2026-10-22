#!/usr/bin/env python3
"""Read-only scoped semantic dedup; outputs no unrelated account metadata."""
import json,hashlib,re,datetime
from pathlib import Path
root=Path('/Users/alec/Documents/Math')
out=root/'final_full_solution_sweep_20261020_01a15be7/audits/pr0280_30000156/reviews/reconciliation_priority_20261021'
private=root/'final_full_solution_sweep_20261020_01a15be7/private/pr0280_priority_reconciliation'
ledger=root/'final_full_solution_sweep_20261020_01a15be7/raw/pr0280/final_reconciliation_live_ledger.json'
account=root/'final_full_solution_sweep_20261020_01a15be7/raw/pr0397/prepublication_7b18298a735e492aa1e467f16eeb92f1/account_complete.json'
patterns={
 'exact_identifiers':r'30000156|OWR[- _]?768[- _]?006|(?:pull/|PR[ _]?)280(?:\b|/)',
 'source_title':r'maps? over finite fields|integrability and reversibility|vivaldi',
 'birational':r'bi[- ]?rational|triangular',
 'period_distribution':r'(?:period|orbit|cycle).{0,50}(?:distribut|limit|cdf|converg)|(?:distribut|cdf).{0,50}(?:period|orbit|cycle)',
 'finite_field_dynamics':r'finite[- ]fields?.{0,80}(?:dynam|maps?|cycle|orbit|period)|(?:dynam|maps?|cycle|orbit|period).{0,80}finite[- ]fields?',
 'totient_application':r'totient|primitive.{0,30}(?:quadratic|values)|phi\(p|φ\(p|varphi',
 'exact_model':r'\(u.{0,10}u.{0,8}2.{0,8}1.{0,8}v|\(x.{0,10}x.{0,8}2.{0,8}1.{0,8}y'
}
compiled={k:re.compile(v,re.I|re.S) for k,v in patterns.items()}
def match(x):
 s=json.dumps(x,ensure_ascii=False); return [k for k,p in compiled.items() if p.search(s)]
rows=json.loads(ledger.read_text())['values']
records=json.loads(account.read_text())['records']
ledger_hits=[{'row':i+1,'match_groups':match(x),'data':x} for i,x in enumerate(rows) if match(x)]
account_hits=[{'match_groups':match({'metadata':x.get('metadata'), 'title':x.get('title'), 'files':[f.get('filename', f.get('key','')) for f in x.get('files',[])]}),'data':x} for x in records]
account_hits=[x for x in account_hits if x['match_groups']]
(private/'semantic_dedup_candidates.json').write_text(json.dumps({'ledger':ledger_hits,'account':account_hits},indent=2,ensure_ascii=False)+'\n')
# Narrow state search and authored prepared manifest search, only keyword candidates held privately.
state_hits=[]
for p in sorted((root/'.zenodo-state').glob('*.json')):
 try:d=json.loads(p.read_text())
 except Exception:continue
 m=match(d)
 if m:state_hits.append({'path':str(p.relative_to(root)),'match_groups':m,'data':d})
(private/'local_state_candidates.json').write_text(json.dumps(state_hits,indent=2,ensure_ascii=False)+'\n')
receipt={
 'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Full existing 175-row ledger and 194-record authenticated account snapshot; title, original wording, finite-field period-distribution model, exact model and arithmetic aliases screened. Account candidate metadata remains private.',
 'patterns':patterns,
 'inputs':[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [ledger,account]],
 'ledger_rows':len(rows), 'account_records':len(records),
 'ledger_candidates':[{'row':x['row'],'match_groups':x['match_groups']} for x in ledger_hits],
 'account_candidate_count':len(account_hits),
 'local_state_candidate_count':len(state_hits),
 'private_review_file':'private/pr0280_priority_reconciliation/semantic_dedup_candidates.json',
 'interpretation':'Candidate screening only; each hit needs target equivalence assessment. Generic keywords are not duplicates.'
}
(out/'MODEL_DEDUP_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['timestamp_utc','ledger_rows','account_records','ledger_candidates','account_candidate_count','local_state_candidate_count']},indent=2))
