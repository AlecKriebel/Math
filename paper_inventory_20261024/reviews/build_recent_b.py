import json
from pathlib import Path
root=Path('/Users/alec/Documents/Math/paper_inventory_20261024/reviews')
records={x['id']:x for x in json.loads((root/'recent_b_records.json').read_text())}
out=root/'recent_b.json'
rows=json.loads(out.read_text()) if out.exists() else []
def add(id,field,impact,added,reason,lay,surprise,sreason,rec,preason,gap,step,boundary):
 x=records[id]
 rows.append(dict(record_id=id,title=x['title'],field=field,impact=impact,added_contribution=added,impact_reason=reason,lay_summary=lay,surprise=surprise,surprise_reason=sreason,publication_recommendation=rec,publication_reason=preason,exact_gap=gap,next_step=step,claim_boundary=boundary,review_basis='Inventory triage of checksum-bound published PDF extraction: abstract, exact main claims, proof architecture, attribution and scope passages inspected; not a new line-by-line proof verification or exhaustive worldwide novelty audit.',text_paths=[s['text_path'] for s in x['sources']]))
def save():
 out.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 (root/'recent_b.md').write_text('# Recent manuscripts B: inventory triage\n\nConditional impact assumes correctness, genuine added novelty and eventual publication. Readiness is assessed separately. Review is not independent human peer review.\n\n'+ '\n\n'.join(f"## {r['record_id']}: {r['title']}\n\nImpact {r['impact']}/10; surprise {r['surprise']}/10. {r['publication_recommendation']}.\n\nAdded contribution: {r['added_contribution']}\n\n{r['impact_reason']}\n\nBoundary: {r['claim_boundary']}\n\nRemaining gap: {r['exact_gap']}\n\nNext step: {r['next_step']}\n\nBasis: {r['review_basis']}" for r in rows)+'\n')
