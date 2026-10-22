#!/usr/bin/env python3
"""Independent exact audit. No network/writes/imports from historical code.

Validator uses Kendall orientation changes; enumerator uses direct swaps.
Explicit guards remain active with python -O. Standard library only.
"""
import collections
import itertools
import json
import math
import sys
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def R(state):
    return tuple(-x for x in reversed(state))


def alphabet(n):
    return tuple(range(1,n+1))+tuple(range(-1,-n-1,-1))


def legal(s,n):
    return (isinstance(s,(tuple,list)) and len(s)==2*n
            and all(type(x) is int for x in s) and set(s)==set(alphabet(n))
            and all(s.index(x)<s.index(-x) for x in range(1,n+1)))


def change(a,b):
    need(len(a)==len(b) and set(a)==set(b),'different alphabets')
    p,q=({x:i for i,x in enumerate(s)} for s in (a,b))
    flipped=[(x,y) for x,y in itertools.combinations(a,2)
             if (p[x]<p[y]) != (q[x]<q[y])]
    need(len(flipped)==1,'Kendall distance is not one')
    x,y=flipped[0]
    need(abs(x)!=abs(y),'same body switch')
    need(abs(p[x]-p[y])==1 and abs(q[x]-q[y])==1,'nonadjacent switch')
    return (x,y),(y,x)


def least_period(w):
    need(len(w)>0,'empty word')
    for k in range(1,len(w)+1):
        if len(w)%k==0 and all(w[j]==w[(j+k)%len(w)] for j in range(len(w))):
            return k
    raise RuntimeError('unreachable')


def check(d):
    need(isinstance(d,dict),'not object')
    need(set(d)=={'schema','n','sequence'},'schema keys')
    need(type(d['schema']) is int and d['schema']==1,'schema')
    n=d['n'];need(type(n) is int and n>=2,'domain n >= 2')
    w=d['sequence'];need(isinstance(w,list) and len(w)>0,'word shape')
    need(all(legal(s,n) for s in w),'axiom i endpoint states')
    moves=[change(w[j],w[(j+1)%len(w)]) for j in range(len(w))]
    need(len(w)%2==0,'axiom iii even length')
    h=len(w)//2
    need(all(tuple(w[(j+h)%len(w)])==R(w[j]) for j in range(len(w))),'axiom iii reverse-toggle')
    need(len(w)==8*math.comb(n,2),'axiom iv length')
    need(least_period(w)==len(w),'axiom iv least period')
    counts=collections.Counter(new for old,new in moves)
    types={(x,y) for x in alphabet(n) for y in alphabet(n) if abs(x)!=abs(y)}
    need(set(counts)<=types,'event alphabet')
    return {'n':n,'length':len(w),'least_period':least_period(w),
            'before_switches':[list(a) for a,b in moves],
            'after_switches':[list(b) for a,b in moves],
            'event_counts_after':[{'pair':list(p),'count':counts[p]} for p in sorted(types)],
            'mixed_event_count':sum(v for p,v in counts.items() if p[0]*p[1]<0),
            'switch_once':all(counts[p]==1 for p in types),
            'separated_state_present':any(all(abs(s[2*j])==abs(s[2*j+1]) for j in range(n)) for s in w)}


def doc(w,n=2):
    return {'schema':1,'n':n,'sequence':[list(s) for s in w]}


def neighbors(s):
    result=[]
    for j in range(len(s)-1):
        if abs(s[j])!=abs(s[j+1]):
            t=list(s);t[j],t[j+1]=t[j+1],t[j];result.append(tuple(t))
    return tuple(sorted(result))


def accepts(w):
    try:check(doc(w));return True
    except ValueError:return False


def transform(w,k=0,back=False,rename=False):
    v=list(reversed(w)) if back else list(w);v=v[k:]+v[:k]
    if rename:v=[tuple((3-abs(x))*(1 if x>0 else -1) for x in s) for s in v]
    return tuple(v)


def canon(w):
    return min(transform(w,k,b,r) for k in range(8) for b in (False,True) for r in (False,True))


def exhaustive():
    states=tuple(sorted(s for s in itertools.permutations(alphabet(2)) if legal(s,2)))
    need(len(states)==6,'six states')
    graph={s:neighbors(s) for s in states}
    edges={tuple(sorted((s,t))) for s,ts in graph.items() for t in ts}
    need(len(edges)==6 and sorted(map(len,graph.values()))==[1,1,2,2,3,3],'graph shape')
    for s in states:
        need(R(R(s))==s,'involution')
        need({R(t) for t in graph[s]}==set(graph[R(s)]),'graph automorphism')
        for t in states:
            try:change(s,t);adj=True
            except ValueError:adj=False
            need(adj==(t in graph[s]),'direct-swap versus orientation oracle')
    path_words=set();candidates=0
    def visit(path):
        nonlocal candidates
        if len(path)==5:
            if path[-1]==R(path[0]):
                candidates+=1
                w=tuple(path[:4]+[R(s) for s in path[:4]])
                if least_period(w)==8:
                    need(accepts(w),'path verification');path_words.add(w)
            return
        for nxt in graph[path[-1]]:visit(path+[nxt])
    for s in states:visit([s])
    # Second enumeration tries every half tuple without path pruning.
    product_words=set()
    for first in itertools.product(states,repeat=4):
        w=first+tuple(map(R,first))
        if accepts(w):product_words.add(w)
    need(path_words==product_words,'enumerations agree')
    details=[(w,check(doc(w))) for w in sorted(path_words)]
    separated={w for w,d in details if d['separated_state_present']}
    once={w for w,d in details if d['switch_once']}
    no_mixed={w for w,d in details if d['mixed_event_count']==0}
    need(separated==once,'n=2 separated iff switch-once')
    for w in path_words:
        base=check(doc(w))
        for k,b,r in itertools.product(range(8),(False,True),(False,True)):
            q=check(doc(transform(w,k,b,r)))
            need(q['mixed_event_count']==base['mixed_event_count'],'mixed symmetry')
            need(q['switch_once']==base['switch_once'],'switch-once symmetry')
    reps=sorted(set(map(canon,path_words)))
    return {'states':[list(s) for s in states],
            'graph':[{'state':list(s),'neighbors':[list(t) for t in graph[s]],'R':list(R(s))} for s in states],
            'edges':len(edges),'half_path_candidates':candidates,'half_tuple_search_space':6**4,
            'primitive_weak_words':len(path_words),'switch_once_words':len(once),
            'separated_state_words':len(separated),'no_mixed_event_words':len(no_mixed),
            'symmetry_orbits':len(reps),
            'orbits':[{'representative':[list(s) for s in w],
                       'size':sum(canon(v)==w for v in path_words),'properties':check(doc(w))} for w in reps]}


def controls(witness):
    import copy
    results=[]
    def reject(name,d):
        try:check(d)
        except (ValueError,TypeError,KeyError) as e:
            results.append({'name':name,'rejected':True,'reason':str(e)});return
        raise RuntimeError('negative control accepted: '+name)
    reject('not object',[])
    for name,key,value in [('boolean schema','schema',True),('boolean n','n',True),('n1 zero period','n',1)]:
        c=copy.deepcopy(witness);c[key]=value;reject(name,c)
    for name,value in [('boolean endpoint',True),('zero endpoint',0),('duplicate endpoint',2)]:
        c=copy.deepcopy(witness);c['sequence'][0][0]=value;reject(name,c)
    for name,index,state in [
            ('wrong endpoint order',0,[-1,2,1,-2]),
            ('stationary transition',1,[1,2,-1,-2]),
            ('simultaneous swaps',1,[2,1,-2,-1]),
            ('nonadjacent exchange',1,[-2,2,-1,1]),
            ('wraparound jump',7,[2,-2,1,-1]),
            ('lost half involution',4,[1,2,-1,-2])]:
        c=copy.deepcopy(witness);c['sequence'][index]=state;reject(name,c)
    c=copy.deepcopy(witness);c['sequence']*=2;reject('wrong full length',c)
    short=[(1,2,-2,-1),(1,2,-1,-2),(2,1,-1,-2),(1,2,-1,-2)]
    reject('length8 least period4',doc(short*2))
    for name,a,b in [('same-body helper',(1,-1,2,-2),(-1,1,2,-2)),
                     ('nonadjacent helper',(1,2,-1,-2),(-1,2,1,-2))]:
        try:change(a,b)
        except ValueError as e:results.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise RuntimeError('negative helper accepted: '+name)
    return results


def run(path):
    w=json.loads(Path(path).read_text());r=check(w)
    need(r['n']==2 and r['mixed_event_count']==0,'witness obstruction')
    need([e['count'] for e in r['event_counts_after']].count(2)==4,'duplicate supports')
    return {'schema':1,'status':'PASS','arithmetic':'exact finite enumeration',
            'witness':r,'enumeration':exhaustive(),'negative_controls':controls(w),
            'scope':'finite four-axiom n2 audit; no novelty certification'}


if __name__=='__main__':
    need(len(sys.argv)==2,'usage: exact_combinatorics.py WITNESS.json')
    print(json.dumps(run(sys.argv[1]),sort_keys=True,indent=2))
