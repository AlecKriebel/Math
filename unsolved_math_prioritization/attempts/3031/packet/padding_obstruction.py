#!/usr/bin/env python3
"""Exact spectra of an8-vertex deficit16 gadget plus rainbow filler vertices."""
import itertools,json,math
from gap_six_gadgets import proper_clique,signature

def g16():
    e=proper_clique(8)
    e[1,6]=7;e[2,5]=8;e[3,4]=9;e[0,1]=10;e[3,5]=11
    assert math.comb(8,2)-len(set(e.values()))==16
    return e

def padded_spectrum(e,n):
    counts={};witnesses={};h=8
    for mask in range(1<<h):
      S=[i for i in range(h) if mask>>i&1]
      d=math.comb(len(S),2)-len({e[i,j] for i,j in itertools.combinations(S,2)})
      for r in range(n-h+1):
        t=len(S)+r;colors=1 if t==0 else 2+math.comb(t,2)-d
        mult=math.comb(n-h,r);counts[colors]=counts.get(colors,0)+mult
        witnesses.setdefault(colors,{'core_subset':S,'filler_vertices':list(range(h,h+r)),'deficit':d})
    assert sum(counts.values())==2**n
    return counts,witnesses

def main():
    e=g16();sg=signature(8,e);assert 4 not in {d for ds in sg.values() for d in ds}
    out={'gadget':{'n':8,'total_deficit':16,'edge_colors':[[i,j,c] for (i,j),c in e.items()],'deficits_by_size':sg},'examples':[]}
    for n,m in [(22,43),(24,64)]:
      cnt,wit=padded_spectrum(e,n);out['examples'].append({'n':n,'c':math.comb(n,2)+2-16,'m':m,'avoids_m':m not in cnt,'palette_spectrum':sorted(cnt),'weighted_subsets':sum(cnt.values()),'target_witness':wit.get(m)})
    assert out['examples'][0]['avoids_m'];assert not out['examples'][1]['avoids_m']
    print(json.dumps({'gadget_deficits':sg,'examples':[{k:v for k,v in ex.items() if k!='palette_spectrum'} for ex in out['examples']]},indent=2));open('padding_obstruction_checks.json','w').write(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
