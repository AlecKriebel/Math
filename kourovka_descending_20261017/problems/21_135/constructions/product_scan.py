"""Exact bounded search for degree-multiset identities among library products.

Input is produced by scan_library.g. No approximation, CH, recognition, or
character-table completeness assumption is used. This tests only direct
products of at most two listed factors and publishes no solution claim.
"""
from pathlib import Path
from collections import defaultdict, Counter
from itertools import combinations_with_replacement
import json, hashlib, datetime
BASE=Path(__file__).resolve().parent
ROWS=[json.loads(l) for l in (BASE/'artifacts/library_scan.ndjson').read_text().splitlines()]
GROUPS={((1,1),): {'names':['1 (explicit trivial group)'],'order':1,'radical_free':True,'degrees':{1:1}}}
for name,order,degs,rad in ROWS:
    key=tuple(map(tuple,degs))
    if key not in GROUPS:GROUPS[key]={'names':[],'order':order,'radical_free':rad==1,'degrees':dict(degs)}
    g=GROUPS[key]
    assert g['radical_free']==(rad==1), 'Actual target collision in single tables'
    assert sum(d*d*m for d,m in degs)==order
    g['names'].append(name)
G=list(GROUPS.values())
for g in G:
    d=g['degrees']
    g['fingerprint']=(g['order'],sum(d.values()),d.get(1,0),max(d),sum(k*v for k,v in d.items()),sum(k**3*v for k,v in d.items()),sum(k**4*v for k,v in d.items()))
def fp_product(a,b):return tuple(x*y for x,y in zip(a['fingerprint'],b['fingerprint']))
def mult(a,b):
    c=Counter()
    for x,m in a['degrees'].items():
        for y,n in b['degrees'].items():c[x*y]+=m*n
    return tuple(sorted(c.items()))
BOUND=10**12
rf=[g for g in G if g['radical_free']]
targets=defaultdict(list)
rf_count=0
for a,b in combinations_with_replacement(rf,2):
    if a['order']*b['order']<=BOUND:
        targets[fp_product(a,b)].append((a,b));rf_count+=1
# Also test a single table against a product by the trivial-group convention.
nonrf_count=candidate_count=exact_checks=0
collisions=[]
near=[]
for a,b in combinations_with_replacement(G,2):
    if a['radical_free'] and b['radical_free']:continue
    if a['order']*b['order']>BOUND:continue
    nonrf_count+=1
    cand=targets.get(fp_product(a,b))
    if not cand:continue
    candidate_count+=1
    hd=mult(a,b)
    for c,d in cand:
        exact_checks+=1
        gd=mult(c,d)
        entry={'radical_nontrivial':[a['names'][0],b['names'][0]],'radical_free':[c['names'][0],d['names'][0]],'order':a['order']*b['order']}
        if gd==hd:collisions.append(entry)
        else:
            first=next((n for n in sorted(set(dict(gd))|set(dict(hd))) if dict(gd).get(n,0)!=dict(hd).get(n,0)))
            entry['first_different_degree']=first;entry['G_multiplicity']=dict(gd).get(first,0);entry['H_multiplicity']=dict(hd).get(first,0);near.append(entry)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gap':'4.16.1','ctbllib':'1.3.11','library_table_order_bound':10**8,'library_rows':len(ROWS),'explicit_additions':['trivial group of order 1'],'unique_degree_multisets':len(G),'radical_free_unique_multisets':len(rf),'product_order_bound':BOUND,'radical_free_product_pairs':rf_count,'radical_nontrivial_product_pairs':nonrf_count,'fingerprint_candidates':candidate_count,'exact_multiset_comparisons':exact_checks,'target_collisions':collisions,'moment_near_misses':near,'scope':'Listed character tables and unordered products of two representatives only. Not an exhaustive search over finite groups of the bounded orders.','input_sha256':hashlib.sha256((BASE/'artifacts/library_scan.ndjson').read_bytes()).hexdigest()}
(BASE/'artifacts/product_scan_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['moment_near_misses']},indent=2))
