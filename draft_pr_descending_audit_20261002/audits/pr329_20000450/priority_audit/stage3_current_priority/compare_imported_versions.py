"""Computed semantic/serialization comparison from pinned primary dataset bytes.

Does not pretend reconstructed bytes are a historically retrieved local file.
"""
from pathlib import Path
import json,hashlib
s=Path(__file__).resolve().parent;p=s/'private_evidence'
report=json.loads((p/'upstream_research_results/source.bytes').read_bytes())['AIM-ALGEBRAIC_NUMBER_THEORY-0102']
problem=next(x for x in json.loads((p/'upstream_problems/source.bytes').read_bytes()) if x.get('id')==20000450)
rootreport=json.loads((p/'imported_report/stdout').read_bytes())
rootproblem=json.loads((p/'imported_payload/stdout').read_bytes())
def h(b):return hashlib.sha256(b).hexdigest()
variants=[]
for label,value,target in [('report',report,'56ce26a89b743cdf34807407c9e392dd1738b92c1982c661132ab159172eb93a'),('problem',problem,'e6a7aa151df6b3d291512e580ad3367da317f493464a38e04997ef40b3fde033')]:
 for ascii_ in [True,False]:
  for newline in ['', '\n']:
   b=(json.dumps(value,indent=2,ensure_ascii=ascii_)+newline).encode()
   row={'record':label,'ensure_ascii':ascii_,'trailing_newline':bool(newline),'bytes':len(b),'sha256':h(b),'matches_legacy_source_manifest':h(b)==target}
   variants.append(row)
   if row['matches_legacy_source_manifest']:
    (p/f'computed_legacy_{label}_serialization.json').write_bytes(b)
out={'kind':'computed_semantic_and_serialization_comparison_not_historical_retrieval_receipt','report_semantically_equal':report==rootreport,'problem_semantically_equal':problem==rootproblem,'problem_differing_keys':[k for k in set(problem)|set(rootproblem) if problem.get(k)!=rootproblem.get(k)],'variants':variants}
(p/'IMPORTED_SEMANTIC_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
