"""Check the exact two-step conference graph reduction on prime-order Paley graphs."""
from pathlib import Path
from itertools import combinations
import json
import twinwidth as t

def paley(p):
    squares={i*i%p for i in range(1,p)}
    return tuple(sum(1<<j for j in range(p) if (j-i)%p in squares) for i in range(p))

def main():
    results=[]
    for n in (5,13,17,29):
        a=paley(n);k=(n-1)//4;D=2*k;per_first=[];triple_counts={}
        for u,v in combinations(range(n),2):
            rem=set(range(n))-{u,v};A={w for w in rem if a[u]>>w&1 and a[v]>>w&1};B={w for w in rem if not(a[u]>>w&1) and not(a[v]>>w&1)};C={w for w in rem if a[u]>>w&1 and not(a[v]>>w&1)};E=rem-A-B-C
            assert sorted([len(A),len(B)])==[k-1,k] and len(C)==len(E)==k
            safe=0
            for x,y in combinations(sorted(rem),2):
                bad=({x,y}<=C or {x,y}<=E or x in A and y in B or y in A and x in B)
                part=tuple([1<<w for w in sorted(rem-{x,y})]+[(1<<u)|(1<<v),(1<<x)|(1<<y)])
                actual=t.width(a,part)<=D
                assert actual==(not bad)
                safe+=actual
            assert safe==6*k*k-4*k+1;per_first.append(safe)
        for triple in combinations(range(n),3):
            mask=sum(1<<v for v in triple);part=tuple([mask]+[1<<i for i in range(n) if not(mask>>i&1)])
            e=sum((a[u]>>v)&1 for u,v in combinations(triple,2));expect=3*k-int(e in (1,2));actual=t.width(a,part)
            assert actual==expect;triple_counts[str(actual)]=triple_counts.get(str(actual),0)+1
        results.append({'n':n,'k':k,'first_pairs':len(per_first),'safe_disjoint_second_pairs_per_first':per_first[0],'triple_red_degree_counts':triple_counts,'all_claims_verified':True})
    Path(__file__).with_name('conference_results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()
