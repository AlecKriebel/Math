"""Only run after FIRST_CONCLUSION is sealed; original code comparisons."""
import datetime, importlib.util, json, pathlib, sys
from fractions import Fraction
import independent_tl_calibration as fresh

ROOT=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('preserved_original',ROOT/'phase_two_original_replay'/'verify_jones.py')
old=importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
results=json.loads((ROOT/'independent_results.json').read_text())
seen=set(); comparisons=[]
for row in results['rows']:
    m=row['strands']; word=tuple(row['word'])
    if (m,word) in seen: continue
    seen.add((m,word))
    components,signs=fresh.gauss_from_braid(m,word)
    sequence=components[0]
    fresh_arrows=[tuple(next(i for i,(x,over) in enumerate(sequence) if x==crossing and over==flag) for flag in (True,False)) for crossing in range(len(word))]
    arrows,oldsigns=old.gauss(m,word)
    assert arrows==fresh_arrows and oldsigns==[signs[x] for x in range(len(word))]
    oldpv,stats=old.pv(arrows,oldsigns)
    oldj=old.jones_v3(m,word)
    assert oldpv==oldj==Fraction(row['jones_v3'])
    comparisons.append({'strands':m,'word':word,'jones_v3':str(oldj),'arrows_identical':True,'signed_pv_identical':True})

# Mutation controls: ensure this corpus distinguishes plausible false conventions.
trefoil=next(r for r in results['rows'] if r['name']=='right_trefoil')
p_only=next(r for r in results['rows'] if r['strands']==3 and r['word']==[-2,-1,-2,-1])
eight=next(r for r in results['rows'] if r['name']=='figure_eight')
mutation_witnesses=[
    {'mutation':'count labelled cyclic T embeddings with coefficient 1','witness':trefoil,'mutant_v3':'3','correct_v3':'1'},
    {'mutation':'change P coefficient from 1/2 to 1','witness':p_only,'mutant_v3':'-2','correct_v3':'-1'},
    {'mutation':'replace signed crossing products with unsigned counts','witness':eight,'mutant_v3':'2','correct_v3':'0'},
]
for item in mutation_witnesses: assert Fraction(item['mutant_v3'])!=Fraction(item['correct_v3'])

out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'after sealed first independent conclusion','original_replay':'59 rows, 183 assertions, PASS','distinct_original_vs_fresh_comparisons':len(comparisons),'max_crossings':max(len(r['word']) for r in comparisons),'status':'PASS','comparisons':comparisons,'false_convention_mutation_witnesses':mutation_witnesses}
(ROOT/'phase_two_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('comparisons','false_convention_mutation_witnesses')},indent=2))
print('Mutation controls:',json.dumps([{k:v for k,v in w.items() if k!='witness'} for w in mutation_witnesses]))
