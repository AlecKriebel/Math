"""All small partial graphs: global completions vs local probabilities."""
from collections import Counter
from fractions import Fraction
from itertools import combinations,product
import hashlib,json,pathlib

here=pathlib.Path(__file__).resolve().parent
counts=Counter()
def cyclic(edges,triple):
    return all(sum((i,j) in edges for j in triple if i!=j)==1 for i in triple)
def completed(fixed,pairs):
    absent=[p for p in pairs if p not in fixed and tuple(reversed(p)) not in fixed]
    for orientations in product([False,True],repeat=len(absent)):
        yield fixed|{pair if bit else tuple(reversed(pair)) for pair,bit in zip(absent,orientations)}
def local(fixed,triple):
    states=list(completed(fixed,list(combinations(triple,2))))
    return Fraction(sum(cyclic(s,triple) for s in states),len(states))
for n in range(5):
    pairs=list(combinations(range(n),2));triples=list(combinations(range(n),3))
    for choices in product([0,1,-1],repeat=len(pairs)):
        fixed={pair if direction==1 else tuple(reversed(pair))
               for pair,direction in zip(pairs,choices) if direction}
        states=list(completed(fixed,pairs))
        expected=Fraction(sum(sum(cyclic(s,t) for t in triples) for s in states),len(states))
        local_sum=sum(local(fixed,t) for t in triples)
        assert local_sum==expected
        limit=Fraction(n*(n*n-1 if n%2 else n*n-4),24)
        assert expected<=limit
        counts['partial_graphs']+=1;counts['global_completions']+=len(states)
        counts['local_global_expectation_equalities']+=1

examples=[]
for description,fixed,triples in [
    ('positive dependence: same missing edge closes both paths',
     {(0,1),(1,2),(0,3),(3,2)},[(0,1,2),(0,2,3)]),
    ('negative dependence: opposite orientations close the two paths',
     {(0,1),(1,2),(2,3),(3,0)},[(0,1,2),(0,2,3)])]:
    states=list(completed(fixed,list(combinations(range(4),2))))
    marginal=[Fraction(sum(cyclic(s,t) for s in states),len(states)) for t in triples]
    joint=Fraction(sum(all(cyclic(s,t) for t in triples) for s in states),len(states))
    assert marginal==[Fraction(1,2),Fraction(1,2)]
    assert joint != marginal[0]*marginal[1]
    examples.append({'description':description,'fixed_edges':sorted(fixed),
                     'triples':triples,'marginal_probabilities':list(map(str,marginal)),
                     'joint_probability':str(joint),'product_of_marginals':str(marginal[0]*marginal[1])})
result={'status':'PASS','scope':'all partial oriented complete graphs through four vertices',
        'counts':dict(counts),'dependence_examples':examples,
        'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'limitation':'Examples show dependence is real; finite exhaustive tests support the universal expectation derivation.'}
(here/'COMPLETION_DEPENDENCE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
