import json
from pathlib import Path
root=Path('/Users/alec/Documents/Math/paper_inventory_20261024/reviews')
records={x['id']:x for x in json.loads((root/'recent_b_records.json').read_text())}
contribution_scores={23306332:7,23310484:8,23318851:4,23328912:6.5,23331232:2.5,23331295:5.5,23331395:8,23331709:4.5,23333002:5.5,23333353:6.5,23352246:8,23355942:3,23356680:7.5,23357263:3.5,23358014:6.5,23383952:5.5,23384007:2.5,23384938:2.5,23385608:3.5,23387442:6.5,23387753:7.5,23387814:6.5,23390181:7,23392409:6,23393596:7,23395703:6,23397854:4,23408971:3,23409879:4.5,23410944:8,23411482:2,23414025:8,23414444:3,23418581:5.5,23422039:3.5,23423290:2.5,23425412:5,23428090:2,23430475:2.5,23430530:2.5,23430660:3.5,23430776:2.5,23430927:5,23431313:7,23431716:7,23439776:4.5,23440389:6,23441167:2.5}
out=root/'recent_b.json'
rows=json.loads(out.read_text()) if out.exists() else []
def add(id,field,impact,added,reason,lay,surprise,sreason,rec,preason,gap,step,boundary):
 x=records[id]
 rows.append(dict(record_id=id,title=x['title'],field=field,impact=impact,added_contribution=min(impact,contribution_scores.get(id,impact)),added_contribution_reason=added,impact_reason=reason,lay_summary=lay,surprise=surprise,surprise_reason=sreason,publication_recommendation=rec,publication_reason=preason,exact_gap=gap,next_step=step,claim_boundary=boundary,review_basis='Inventory triage of checksum-bound published PDF extraction: abstract, exact main claims, proof architecture, attribution and scope passages inspected; not a new line-by-line proof verification or exhaustive worldwide novelty audit.',text_paths=[s['text_path'] for s in x['sources']]))
def save():
 out.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 (root/'recent_b.md').write_text('# Recent manuscripts B: inventory triage\n\nConditional impact assumes correctness, genuine added novelty and eventual publication. Readiness is assessed separately. Review is not independent human peer review.\n\n'+ '\n\n'.join(f"## {r['record_id']}: {r['title']}\n\nImpact {r['impact']}/10; surprise {r['surprise']}/10. {r['publication_recommendation']}.\n\nAdded contribution: {r['added_contribution_reason']} (added-contribution score {r['added_contribution']}/10)\n\n{r['impact_reason']}\n\nBoundary: {r['claim_boundary']}\n\nRemaining gap: {r['exact_gap']}\n\nNext step: {r['next_step']}\n\nBasis: {r['review_basis']}" for r in rows)+'\n')
