#!/usr/bin/env python3
"""Construct exact separated-start positive controls; no file writes."""
import collections,json,math
from exact_combinatorics import R,check,doc,need
out=[]
for n in range(2,8):
    start=tuple(x for j in range(1,n+1) for x in (j,-j))
    target=R(start);rank={x:i for i,x in enumerate(target)}
    path=[start];current=list(start)
    while tuple(current)!=target:
        j=next(j for j in range(len(current)-1) if rank[current[j]]>rank[current[j+1]])
        need(abs(current[j])!=abs(current[j+1]),'cross-body')
        current[j],current[j+1]=current[j+1],current[j];path.append(tuple(current))
    need(len(path)-1==4*math.comb(n,2),'geodesic length')
    word=path[:-1]+list(map(R,path[:-1]));r=check(doc(word,n))
    need(r['switch_once'] and r['separated_state_present'],'separated switch-once')
    before=collections.Counter(map(tuple,r['before_switches']))
    after=collections.Counter(map(tuple,r['after_switches']))
    need(before==after and set(before.values())=={1},'both switch conventions')
    out.append({'n':n,'half_length':len(path)-1,'full_length':len(word),
                'least_period':r['least_period'],'switch_once':True})
print(json.dumps({'status':'PASS','positive_controls':out},sort_keys=True,indent=2))
