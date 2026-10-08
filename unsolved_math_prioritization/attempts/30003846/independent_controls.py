#!/usr/bin/env python3
"""Independent non-asserting checks of finite transformation certificates.
No all-n, continuous-dynamics, or imported-theorem certificate is claimed.
"""
import ast, hashlib, itertools, json, pathlib, sys, time
from check_combinatorics import peel
from check_reduction import reduce, decorate

def need(value,message):
    if not value:raise RuntimeError(message)

def matchings(n):
    def recurse(remaining,pairs):
        if not remaining:
            ordered=sorted(pairs,key=lambda x:x[1]);word=[None]*(2*n)
            for label,(a,b) in enumerate(ordered):word[a]=(label,0);word[b]=(label,1)
            yield tuple(word)
        else:
            a=min(remaining)
            for b in sorted(remaining-{a}):yield from recurse(remaining-{a,b},pairs+[(a,b)])
    yield from recurse(set(range(2*n)),[])

def graph(word):
    owners=set(x[0] for x in word);g={x:set() for x in owners}
    for a,b in itertools.combinations(sorted(owners),2):
        subseq=[x[0] for x in word if x[0] in (a,b)]
        if subseq[0]!=subseq[1] and subseq[0]==subseq[2]:g[a].add(b);g[b].add(a)
    return g

def connected(word):
    g=graph(word)
    if not g:return False
    reached={next(iter(g))};todo=list(reached)
    while todo:
        for x in g[todo.pop()]-reached:reached.add(x);todo.append(x)
    return len(reached)==len(g)

def peelable(word):
    rs=[a for a,s in word if s]
    return all(connected(tuple(x for x in word if x[0] in rs[:k])) for k in range(2,len(rs)+1))

def replay_swaps(word,moves):
    for bump,cut in moves:
        start=word.index((bump,0));end=word.index((bump,1));middle=word[start+1:end]
        need(0<=cut<=len(middle),'swap cut out of bounds')
        x,y=middle[:cut],middle[cut:]
        need(set(a for a,s in x).isdisjoint(a for a,s in y),'nonclosed swap')
        word=word[:start+1]+y+x+word[end:]
        for a in set(x[0] for x in word):need(word.index((a,0))<word.index((a,1)),'feet reversed')
    return word

def initial(word,bumps):
    equivalence=[{i} for i in range(len(word)+1)]
    for l,r in bumps:
        a=word.index(l)+1;b=word.index(r)
        ia=next(i for i,s in enumerate(equivalence) if a in s);ib=next(i for i,s in enumerate(equivalence) if b in s)
        if ia!=ib:
            equivalence[ia]|=equivalence[ib];equivalence.pop(ib)
    vertex={j:min(s) for s in equivalence for j in s}
    edges={e:(vertex[i],vertex[i+1]) for i,e in enumerate(word)};cells={}
    for l,r in bumps:
        gap=tuple(word[word.index(l)+1:word.index(r)])
        cells[l]=((l,),(l,)+gap);cells[r]=((r,),gap+(r,))
    return set(vertex.values()),edges,cells

def path(edges,word):
    need(bool(word),'empty path')
    need(all(e in edges for e in word),'unknown edge')
    pairs=[edges[e] for e in word]
    need(all(pairs[i][1]==pairs[i+1][0] for i in range(len(pairs)-1)),'path endpoint mismatch')
    return pairs[0][0],pairs[-1][1]

def strongly_connected(vertices,edges):
    for v in vertices:
        seen={v};todo=[v]
        while todo:
            x=todo.pop()
            for a,b in edges.values():
                if a==x and b in vertices and b not in seen:seen.add(b);todo.append(b)
        need(seen==vertices,'inner graph not strongly connected')

def replay_GS(word,bumps,moves,expected):
    V,E,C=initial(word,bumps);base=tuple(word);source=E[word[0]][0];sink=E[word[-1]][1]
    original_feet={e for pair in bumps for e in pair};dummies=set(word)-original_feet
    need(len(V)==len(bumps)+len(dummies)+1,'initial vertex count')
    for m in moves:
        if m[0]=='add':
            _,e,w=m;w=tuple(w);need(e not in E and e not in C,'fresh edge violation');ends=path(E,w);E[e]=ends;C[e]=((e,),w)
        elif m[0]=='rw':
            _,target,side,witness,reverse,at=m;need(target!=witness,'self-witness rewrite');need(side in (0,1),'invalid cell side')
            u,v=C[witness][::-1] if reverse else C[witness];old=C[target][side]
            need(at>=0 and old[at:at+len(u)]==u,'rewrite occurrence mismatch')
            sides=list(C[target]);sides[side]=old[:at]+v+old[at+len(u):];C[target]=tuple(sides)
        elif m[0]=='del':
            _,e=m;u,w=C[e];need(u==(e,) and e not in w,'invalid defining deletion')
            need(e not in dummies and e not in (word[0],word[-1]),'protected edge deleted')
            need(all(e not in a+b for f,(a,b) in C.items() if f!=e),'nonunique occurrence at deletion')
            base=tuple(t for a in base for t in (w if a==e else (a,)));del C[e];del E[e]
        else:raise RuntimeError('unknown move')
        for u,v in C.values():need(path(E,u)==path(E,v),'cell endpoints differ')
        need(path(E,base)==(source,sink),'base not transported')
        need(all(b!=source and a!=sink for a,b in E.values()),'source/sink lost')
    need(E==expected.edges and C=={k:tuple(v) for k,v in expected.cells.items()},'replay differs from producer')
    innerV=V-{source,sink};innerE=set(E)-{word[0],word[-1]}
    need(dummies<=set(E),'dummy lost');need(len(innerE)==len(innerV)==len(bumps)+len(dummies)-1,'core edge vertex counts')
    strongly_connected(innerV,E)
    need(set(C)==set(E)-dummies,'core active set')
    outgoing={v:[e for e in innerE if E[e][0]==v] for v in innerV}
    need(all(len(es)==1 for es in outgoing.values()),'core not deterministic')
    def cycle(v):
        out=[];initial=v
        for _ in range(len(innerE)):
            e=outgoing[v][0];out.append(e);v=E[e][1]
        need(v==initial and set(out)==innerE,'not single cycle');return tuple(out)
    for e,(top,bottom) in C.items():
        need(top==(e,),'core top is not active edge')
        wanted=cycle(E[e][0])+(e,) if e==word[-1] else (e,)+cycle(E[e][1])
        need(bottom==wanted,'core rule mismatch')
    expectedbase=tuple(a for e in word for a in expected.mapping[e]);need(base==expectedbase,'base mapping differs')
    return len(moves)

def negative_controls():
    rejected=[]
    def reject(label,f):
        try:f()
        except (RuntimeError,AssertionError,KeyError,ValueError):rejected.append(label);return
        raise RuntimeError('negative control accepted: '+label)
    reject('own_nonassert_guard',lambda:need(False,'injected'))
    reject('hardened_nonclosed_swap',lambda:__import__('check_combinatorics').perform(((0,0),(1,0),(1,1),(0,1)),0,1))
    reject('independent_nonclosed_swap',lambda:replay_swaps(((0,0),(1,0),(1,1),(0,1)),[(0,1)]))
    d=((0,0),(1,0),(0,1),(1,1));w,b=decorate(d,[0,0,0]);k,m,_=reduce(w,b)
    reject('independent_self_witness',lambda:replay_GS(w,b,[('rw','L0',1,'L0',False,0)],k))
    reject('independent_illegal_delete',lambda:replay_GS(w,b,[('del','L0')],k))
    reject('independent_empty_path',lambda:path({'a':(0,1)},()))
    reject('independent_bad_endpoint',lambda:path({'a':(0,1),'b':(2,3)},('a','b')))
    reject('hardened_self_witness',lambda:k.rewrite('L0',1,'L0'))
    return rejected

def main():
    start=time.time();rows=[];totalswaps=totalGS=maxmoves=0;negatives=negative_controls()
    for n in range(2,8):
        total=irr=already=swapcount=cases=0;seen=set()
        for d in matchings(n):
            total+=1
            if not connected(d):continue
            irr+=1;already+=peelable(d);target,moves=peel(d)
            need(replay_swaps(d,moves)==target,'swap certificate output mismatch');need(peelable(target),'output not peelable');swapcount+=len(moves)
            if n<=6 and target not in seen:
                seen.add(target);variants=itertools.product(range(4),repeat=3) if n==2 else [[0]*(2*n-1),[1]*(2*n-1),[i%3 for i in range(2*n-1)]]
                for amounts in variants:
                    word,bumps=decorate(target,amounts);K,certificate,_=reduce(word,bumps)
                    count=replay_GS(word,bumps,certificate,K);cases+=1;totalGS+=count;maxmoves=max(maxmoves,count)
        rows.append(dict(n=n,matchings=total,irreducible=irr,already_peelable=already,replayed_swaps=swapcount,independent_GS_instances=cases,distinct_GS_inputs=len(seen)))
        totalswaps+=swapcount
    result=dict(status='PASS',rows=rows,total_replayed_swaps=totalswaps,total_replayed_GS_moves=totalGS,max_GS_moves=maxmoves,negative_controls_rejected=negatives,elapsed_seconds=round(time.time()-start,3),limitations='Finite certificate verification only. Matchings, crossing graphs, closed-cut replay, directed paths, elementary GS operations and final cores are checked independently; peel/reduce provide the certificates. This neither proves the all-n result nor verifies continuous dynamics or external imported theorems.')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
