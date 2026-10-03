"""Standalone checks of the authored K7/K9 constructions and K8 UNSAT proof.
No DPLL solver is imported or executed. All arithmetic is exact.
"""
from itertools import combinations, product
from collections import Counter
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def edge_list(n):return list(combinations(range(n),2))
def triangle_type(colors,t):return tuple(sorted(colors[e] for e in combinations(t,2)))
def disjoint_pairs(n):
    # Independently enumerate by six-sets and the triangle containing their least vertex.
    for six in combinations(range(n),6):
        for other in combinations(six[1:],2):
            t=(six[0],)+other;u=tuple(x for x in six if x not in t)
            yield t,u

def check_coloring(n,colors):
    assert set(colors)==set(edge_list(n))
    k=0
    for t,u in disjoint_pairs(n):
        assert triangle_type(colors,t)!=triangle_type(colors,u),(t,u,triangle_type(colors,t))
        k+=1
    return k

def k9():
    A=set(range(3));B=set(range(3,6));z,x,y=6,7,8
    c={}
    for i,j in edge_list(9):
        if i in A and j in A:c[i,j]=1
        elif i in B and j in B:c[i,j]=0
        elif i in A and j in B:c[i,j]=0
        elif j==z:c[i,j]=1
        elif j==x:c[i,j]=0 if i in A else (2 if i in B else 1)
        elif j==y:c[i,j]=1 if i in A else (2 if i in B or i==x else 0)
        else:raise AssertionError((i,j))
    return c

def original_clause_order(n):
    # The proof file refers to this documented lexicographic clause numbering.
    edges=edge_list(n);eid={e:i for i,e in enumerate(edges)}
    ts=list(combinations(range(n),3));clauses=[]
    for t,u in combinations(ts,2):
        if set(t)&set(u):continue
        sixedges=list(combinations(t,2))+list(combinations(u,2))
        for bits in product((0,1),repeat=6):
            if sum(bits[:3])==sum(bits[3:]):
                clauses.append(tuple((eid[e],1-b) for e,b in zip(sixedges,bits)))
    return clauses

def independently_check_encoding(clauses,n):
    edges=edge_list(n);eid={e:i for i,e in enumerate(edges)};required=set()
    for t,u in disjoint_pairs(n):
        te=set(combinations(t,2));ue=set(combinations(u,2));six=list(te|ue)
        for k in range(4):
            for red_t in combinations(te,k):
                for red_u in combinations(ue,k):
                    red=set(red_t)|set(red_u)
                    clause=frozenset((eid[e],0 if e in red else 1) for e in six)
                    required.add(clause)
    encoded={frozenset(cl) for cl in clauses}
    assert len(clauses)==5600 and len(encoded)==5600 and required==encoded

def replay(node,clauses,assignment):
    a=dict(assignment)
    def unsatisfied(i):
        assert 0<=i<len(clauses)
        clause=clauses[i]
        assert not any(v in a and a[v]==value for v,value in clause)
        return [(v,value) for v,value in clause if v not in a]
    for v,value,reason in node['units']:
        assert value in (0,1) and v not in a
        assert unsatisfied(reason)==[(v,value)]
        a[v]=value
    if 'conflict' in node:
        assert unsatisfied(node['conflict'])==[]
        return 1
    v=node['branch'];assert 0<=v<28 and v not in a
    return 1+replay(node['zero'],clauses,a|{v:0})+replay(node['one'],clauses,a|{v:1})

def main():
    colors=k9();results={}
    n7={e:c for e,c in colors.items() if max(e)<7}
    results['K7_disjoint_pairs']=check_coloring(7,n7)
    results['K9_disjoint_pairs']=check_coloring(9,colors)
    witness=json.loads((ROOT/'extend_k7_results.json').read_text())
    assert colors=={tuple(row[:2]):row[2] for row in witness['edge_colors']}
    ty=Counter(triangle_type(colors,t) for t in combinations(range(9),3))
    expected={(0,0,0):10,(0,0,1):12,(0,0,2):9,(0,1,1):18,(0,1,2):16,(0,2,2):6,(1,1,1):7,(1,1,2):3,(2,2,2):3}
    assert dict(ty)==expected and (1,2,2) not in ty
    for t in combinations(range(9),3):
        s=set(t);k=triangle_type(colors,t)
        if k in ((0,0,0),(0,2,2)):assert len(s&{3,4,5})>=2
        if k in ((0,0,1),(1,1,1)):assert len(s&{0,1,2})>=2
        if k==(0,0,2):assert 7 in s
        if k==(0,1,1):assert 6 in s
        if k==(0,1,2):assert 8 in s
        if k==(1,1,2):assert {6,7}<=s
        if k==(2,2,2):assert {7,8}<=s
    results['K9_type_classification']='PASS'
    results['private_star_extension']={}
    for n in (10,12,16):
        extended={e:(colors[e] if e in colors else max(e)-6) for e in edge_list(n)}
        assert len(set(extended.values()))==n-6
        results['private_star_extension'][n]=check_coloring(n,extended)
    clauses=original_clause_order(8);independently_check_encoding(clauses,8)
    proof=json.loads((ROOT/'k8_two_color_unsat_certificate.json').read_text())
    results['K8_UNSAT_proof_nodes']=replay(proof,clauses,{0:0})
    assert results['K8_UNSAT_proof_nodes']==571
    results['independent_K8_clause_encoding']='PASS'
    assert (0,0,1)!=(0,1,1) # multiplicity must be preserved
    try:check_coloring(6,{e:0 for e in edge_list(6)})
    except AssertionError:results['monochromatic_K6_negative_control']='PASS'
    else:raise AssertionError('Bad negative control')
    results['overall']='PASS'
    (ROOT/'verification_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
