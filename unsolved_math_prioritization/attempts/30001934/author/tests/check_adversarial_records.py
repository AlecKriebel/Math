import json
from pathlib import Path
from exact_model import trees,maximum,member,require
results=[]
for path in sorted(Path('../results').glob('adversarial_best_n*.json')):
 r=json.loads(path.read_text());n=r['n'];es=tuple(map(tuple,r['edges']));w=r['w'];k=r['k']
 require(member(n,es,w,k),'bad recorded point')
 ts=trees(n,es);vals=[maximum(n,es,w,k,t)[0] for t in ts]
 good=sum(v.denominator==1 for v in vals)
 require(good==r['integer_trees'],'fast exact objective disagrees with Fraction certificate')
 require(len(ts)==r['total_trees'],'tree count mismatch')
 results.append({'n':n,'tree_count':len(ts),'integer_maxima':good,'minimum':str(min(vals)),'maximum':str(max(vals)),'exact_fraction_crosscheck':True})
print(json.dumps(results,indent=2))
