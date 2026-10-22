#!/usr/bin/env python3
"""Validate serialized counterexample witnesses and mutate real certificates."""
import copy
import itertools
import json
from pathlib import Path
import check_cochain as source
from check_cochain_independent import validate

ROOT = Path(__file__).resolve().parent

def require(ok, why):
    if not ok:
        raise ValueError(why)

def validate_receipt(r):
    require(r['word'] == 'ababa' and r['directed_edge_length'] == 10, 'wrong walk')
    require(r['central_orders_checked'] == 120 and r['accepted_central_orders'] == 0, 'central totals')
    require(r['complete_vertex_orders_checked'] == 1440 and r['accepted_complete_vertex_orders'] == 0, 'full totals')
    require(r['rotation_and_inverse_variants_checked'] == 20, 'variant count')
    rows=r['all_central_order_results']
    require(len(rows)==120, 'row count')
    expected=set(itertools.permutations(range(5)))
    seen=set()
    for row in rows:
        order=tuple(row['central_order_low_to_high'])
        require(order in expected and order not in seen, 'malformed order')
        seen.add(order); h={v:i for i,v in enumerate(order)}; overlaps=[]
        for i in range(5):
            for j in range(i+1,5):
                if 'ababa'[i]!='ababa'[j]:continue
                a,b=sorted((h[i],h[(i+1)%5]));c,d=sorted((h[j],h[(j+1)%5]))
                if max(a,c)<min(b,d):overlaps.append([i,j])
        require(bool(overlaps) and row['overlapping_same_leaf_excursion_pairs']==overlaps,'invalid overlap witness')
        require(row['accepted_leaf_orders']==0,'invalid leaf acceptance')
    directed=tuple((label,sign) for label in 'ababa' for sign in (1,-1)); variants=[]
    for inverse in (False,True):
        word=tuple((label,-sign) for label,sign in reversed(directed)) if inverse else directed
        for shift in range(10):
            w=word[shift:]+word[:shift]
            periods=[p for p in range(1,10) if 10%p==0 and w==w[:p]*(10//p)]
            require(not periods,'word is periodic')
            variants.append({'inverse':inverse,'cyclic_shift':shift,'proper_periods':periods})
    require(r['nonpower_checks']==variants,'invalid periodicity certificate')

def reject(name, f):
    try:f()
    except (ValueError,KeyError,TypeError,IndexError):return name
    raise ValueError('mutation accepted: '+name)

def main():
    r=json.loads((ROOT/'audit/independent_backtracking/verification_receipt.json').read_text())
    validate_receipt(r); tests=[]
    bad=copy.deepcopy(r);bad['all_central_order_results'][0]['overlapping_same_leaf_excursion_pairs']=[[0,1]]
    tests.append(reject('malformed overlap witness',lambda:validate_receipt(bad)))
    bad=copy.deepcopy(r);bad['nonpower_checks'][0]['proper_periods']=[2]
    tests.append(reject('false periodicity certificate',lambda:validate_receipt(bad)))
    bad=copy.deepcopy(r);bad['all_central_order_results'][0]['central_order_low_to_high']=[0]*5
    tests.append(reject('malformed central order',lambda:validate_receipt(bad)))
    vs=[0]*4; es=[(1,1),(2,1),(1,-1),(2,-1)];h,_,_=source.solve(vs,es)
    validate(vs,es,h)
    invalid=h[:];invalid[1]=invalid[0]
    tests.append(reject('invalid height certificate',lambda:validate(vs,es,invalid)))
    oriented=es[:];oriented[2]=(1,1)
    tests.append(reject('edge orientation corruption',lambda:validate(vs,oriented,h)))
    print(json.dumps({'PASS':True,'receipt_orders_validated':120,'rotation_inverse_checks_validated':20,'actual_mutations_rejected':tests},indent=2))
if __name__=='__main__':main()
