"""Sufficient local reconstruction certificate, independent of automorphism enumeration."""
from colored_involutions import *

def reconstruct(M,C):
    n=len(M);colors=sorted(set(sum(M,[])));S=[i for i in range(n) if M[0][i] in (1,2)]
    outside=[x for x in range(n) if x not in S]
    raw={}
    for x in outside: raw.setdefault(tuple(M[x][s] for s in S),[]).append(x)
    P=[[s] for s in S]+list(raw.values());rounds=0
    while True:
        PP=[]
        for cell in P:
            ds={}
            for x in cell:
                sig=[]
                for target in P:
                    cc=Counter(M[x][y] for y in target)
                    sig.extend(cc[c] for c in colors)
                ds.setdefault(tuple(sig),[]).append(x)
            PP.extend(ds.values())
        if len(PP)==len(P):break
        rounds+=1;P=PP
    other=[cell for cell in P if cell[0] in outside]
    assert all(C[0][C[0][x]]==x for x in range(n))
    assert all(C[0][x]!=x for x in outside)
    assert all(set(C[0][x] for x in cell)==set(cell) for cell in P)
    good=all(len(cell)==2 and C[0][cell[0]]==cell[1] for cell in other)
    return {'vertices':n,'commuting_vertices':len(S),'raw_fiber_sizes':dict(Counter(map(len,raw.values()))),'refinement_rounds':rounds,'stable_cell_sizes':dict(Counter(map(len,other))),'two_point_criterion_pass':good}

if __name__=='__main__':
 results={}
 for name,D in [('A5_2',alternating_class(5,2)),('A6_2',alternating_class(6,2)),('PSL2_7',psl2_prime_class(7)),('PSL2_11',psl2_prime_class(11)),('A7_2',alternating_class(7,2)),('A8_4',alternating_class(8,4))]:
  results[name]=reconstruct(*tables(D));print(name,results[name])
 with open('local_reconstruction_results.json','w') as f:json.dump(results,f,indent=2)
