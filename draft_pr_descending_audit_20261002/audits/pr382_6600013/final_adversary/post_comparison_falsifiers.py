"""Additional counterfeit-assumption falsifiers after the independent seal.

Only the auditor's own exact arithmetic is imported; no candidate code.
"""
import json
from independent_controls import rank,mul

def cover(q,horizontal,vertical):
    edges=4*q;faces=4*q;b1=[[0]*edges for _ in range(q)];b2=[[0]*faces for _ in range(edges)]
    at=lambda sheet,label:4*(sheet%q)+label
    shifts=[*horizontal,*vertical]
    for g in range(q):
        for k,s in enumerate(shifts):b1[(g+s)%q][at(g,k)]+=1;b1[g][at(g,k)]-=1
        for i in range(2):
            for j in range(2):
                col=4*g+2*i+j
                b2[at(g,i)][col]+=1;b2[at(g+horizontal[i],2+j)][col]+=1
                b2[at(g+vertical[j],i)][col]-=1;b2[at(g,2+j)][col]-=1
    assert all(not x for row in mul(b1,b2) for x in row)
    r1=rank(b1);r2=rank(b2)
    return [q-r1,edges-r1-r2,faces-r2]

results=[]
for q in [2,3,5,7]:
    genuine=cover(q,(1,0),(1,0));asymmetric=cover(q,(1,0),(0,0));zero=cover(q,(0,0),(0,0))
    assert genuine==[1,4,q+3]
    assert asymmetric==[1,q+3,2*q+2] and asymmetric!=genuine
    assert zero==[q,4*q,4*q]
    results.append({'degree':q,'both_factor_monodromies_surjective':genuine,'only_horizontal_monodromy_surjective':asymmetric,'zero_monodromy':zero})
# Noncommuting S3 transports do not close an elementary square.
p=[1,0,2];q=[0,2,1];commutation=[p[q[i]]==q[p[i]] for i in range(3)]
assert not all(commutation)
# A two-to-one fold has a branch point. Fibre summation of 1 is discontinuous.
fibres=[{'target':'0','preimages':['1/2'],'sum_constant_1':1},{'target':'1/100','preimages':['99/200','101/200'],'sum_constant_1':2}]
print(json.dumps({'cover_rank_hypothesis_falsifiers':results,'nonflat_transport':{'horizontal':p,'vertical':q,'commutes_by_sheet':commutation,'is_cover_transport':False},'finite_to_one_fold_fails_covering_transfer':fibres,'scope':'Counterfeits falsified; frozen candidate retains the required hypotheses.'},indent=2))
