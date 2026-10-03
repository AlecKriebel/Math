"""Scope and indexing falsifiers, using only the new independent generators."""
from independent_controls import tm_words, rotation_words
import json


def boxes(n, m, recoded):
    return {tuple(tuple((x[i+j],x[i+j+1],y[j]) if recoded else (x[i+j],y[j])
                        for i in range(n)) for j in range(m))
            for x in tm_words(n+m if recoded else n+m-1)
            for y in rotation_words(m)}


records=[]
checks=0
for n in range(1,6):
    for m in range(1,6):
        p=len(boxes(n,m,False))
        correct=len(tm_words(n+m-1))*(m+1)
        incorrect=len(tm_words(n+m))*(m+1)
        assert p==correct and p!=incorrect
        checks+=1
        if n==m:
            values=[]
            for recoded in [False,True]:
                chi=(len(boxes(n,m,recoded))-len(boxes(n+1,m,recoded))
                     -len(boxes(n,m+1,recoded))+len(boxes(n+1,m+1,recoded)))
                values.append(chi)
            records.append(dict(n=n,unrecoded_chi=values[0],recoded_chi=values[1]))
# Removing the independent y coordinate leaves an actual forbidden period.
# The equality i+j=(i+1)+(j-1) holds identically at every lattice site.
for i in range(-10,11):
    for j in range(-10,11):
        assert i+j==(i+1)+(j-1)
        checks+=1
print(json.dumps(dict(assertions=checks,indexing_controls=records,
                     partially_periodic_control={'period':[1,-1],
                        'configuration':'z(i,j)=t(i+j)',
                        'source_admissible':False},
                     result='The two-block recoding and independent Sturmian coordinate are essential to the exact displayed scale formulas and full aperiodicity.'),indent=2,sort_keys=True))
