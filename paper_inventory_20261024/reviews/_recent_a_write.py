import json,os
ROOT='/Users/alec/Documents/Math/paper_inventory_20261024/reviews'
ASSIGN=json.load(open(ROOT+'/recent_a_assignment.json'))
PATH=ROOT+'/recent_a.json'
def add(i,field,impact,contribution,reason,lay,surprise,surprise_reason,recommendation,pub_reason,gap,next_step,boundary,full=False):
 r=ASSIGN[i]
 a=json.load(open(PATH)) if os.path.exists(PATH) else []
 row=dict(record_id=r['id'],title=r['title'],field=field,impact=impact,added_contribution=contribution,impact_reason=reason,lay_summary=lay,surprise=surprise,surprise_reason=surprise_reason,publication_recommendation=recommendation,publication_reason=pub_reason,exact_gap=gap,next_step=next_step,claim_boundary=boundary,review_basis=('Read the full extracted manuscript, including proof and attribution; assessment only, not a fresh independent proof or worldwide priority audit.' if full else 'Read targeted passages in the complete checksum-matched manuscript extraction: abstract, exact main claim, proof mechanism and attribution/scope disclosures. Not an exhaustive line-by-line proof check or worldwide priority audit.'),text_paths=[s['text_path'] for s in r['sources']])
 a=[q for q in a if q['record_id']!=r['id']]+[row]; a.sort(key=lambda q:q['record_id']);json.dump(a,open(PATH,'w'),indent=2,ensure_ascii=False)
 with open(ROOT+'/recent_a.md','w') as f:
  f.write('# Recent papers, partition A\n\nScores assume correctness and assess the manuscript\'s added contribution, preserving stated attribution. They are not citation forecasts or certification of novelty.\n\n')
  for q in a:
   f.write('## '+str(q['record_id'])+' — '+q['title']+'\n\nImpact '+str(q['impact'])+'/10; surprise '+str(q['surprise'])+'/10. '+q['publication_recommendation']+'.\n\n'+q['added_contribution']+' '+q['impact_reason']+'\n\nBoundary: '+q['claim_boundary']+'\n\nRemaining gap: '+q['exact_gap']+' Next: '+q['next_step']+'\n\nBasis: '+q['review_basis']+'\n\n')
