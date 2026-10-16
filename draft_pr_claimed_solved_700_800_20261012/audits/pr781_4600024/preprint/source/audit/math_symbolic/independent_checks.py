#!/usr/bin/env python3
"""Independent finite adversarial controls; standard library; no author imports.
Run python3 -I -B independent_checks.py. The proof, not this finite sweep,
establishes the all-n and all-input conclusions. No network or file writes.
"""
from collections import deque
from itertools import product
import json

ALPHABET = '01'
CHECKS = 0

def require(value, label):
    global CHECKS
    CHECKS += 1
    if not value:
        raise AssertionError(label)

def word_list(length):
    return [''.join(x) for x in product(ALPHABET, repeat=length)]

def vertices(edges):
    return {u for u,a,v in edges} | {v for u,a,v in edges}

def advance(edges, states, letter):
    return frozenset(v for u,a,v in edges if u in states and a == letter)

def accepts(edges, word):
    states = frozenset(vertices(edges))
    for a in word:
        states = advance(edges, states, a)
    return bool(states)

def strongly_connected(edges):
    vs = vertices(edges)
    if not vs:
        return False
    for start in vs:
        reach = {start}
        while True:
            nxt = reach | {v for u,a,v in edges if u in reach}
            if nxt == reach:
                break
            reach = nxt
        if reach != vs:
            return False
    return True

def overlap(edges, n):
    return tuple((w[:-1],w[-1],w[1:]) for w in word_list(n)
                 if accepts(edges,w))

def factors(w,k):
    return {w[i:i+k] for i in range(len(w)-k+1)}

def profile_set(w,k):
    left,right=k//2,k-k//2
    return frozenset((w[max(0,j-left):j],w[j:min(len(w),j+right)])
                     for j in range(len(w)))

def reference_approx_membership(edges,w,n):
    if len(w)<n:
        return accepts(edges,w)
    return all(accepts(edges,v) for v in factors(w,n))

def exact_bad_word(domain,target,width,table):
    # All domain vertices are initial/final. Each emits only an edge label.
    # The target state set tracks the COMPLETE finite-word output, not a prefix.
    initial=[(v,frozenset(vertices(target)),'') for v in vertices(domain)]
    todo=deque((s,'') for s in initial)
    visited=set(initial)
    while todo:
        (v,output,buffer),w=todo.popleft()
        for u,a,dest in domain:
            if u!=v:
                continue
            block=buffer+a
            if len(block)==width:
                out=advance(target,output,table[block]); buf=block[1:]
            else:
                out=output;buf=block
            new=(dest,out,buf)
            if not out:
                return w+a
            if new not in visited:
                visited.add(new);todo.append((new,w+a))
    return None

def merge(edges,u,v):
    states=frozenset(vertices(edges))
    for a in u:
        states=advance(edges,states,a)
    require(bool(states),'left connector endpoint belongs to language')
    todo=deque([(states,'')]);seen={states}
    while todo:
        states,mid=todo.popleft()
        end=states
        for a in v:
            end=advance(edges,end,a)
        if end:
            return u+mid+v
        for a in ALPHABET:
            nxt=advance(edges,states,a)
            if nxt and nxt not in seen:
                seen.add(nxt);todo.append((nxt,mid+a))
    raise AssertionError('irreducibility failed to supply connector')

def main():
    even=((0,'0',0),(0,'1',1),(1,'1',0))
    golden=((0,'0',0),(0,'1',1),(1,'0',0))
    alternating=((0,'0',1),(1,'1',0))
    singleton=((0,'0',0),)
    full=((0,'0',0),(0,'1',0))
    basic={'even':even,'golden':golden,'alternating':alternating,
           'singleton_unused_symbol':singleton,'full':full}
    all_words=[w for length in range(8) for w in word_list(length)]
    possible=tuple(product(range(2),ALPHABET,range(2)))
    graphs=[tuple(e for bit,e in zip(bits,possible) if bit)
            for bits in product((0,1),repeat=8)]
    graphs=[g for g in graphs if vertices(g)=={0,1} and strongly_connected(g)]
    for graph in graphs+list(basic.values()):
        for n in (2,3,4):
            approx=overlap(graph,n)
            require(strongly_connected(approx),'irreducible canonical graph')
            for w in all_words:
                require(accepts(approx,w)==reference_approx_membership(graph,w,n),
                        'appended-edge labels include exactly the full finite language')
    # Endpoint/profile equivalence is checked independently of any graph.
    profile_classes=0
    for k in range(1,5):
        signatures={}
        for length in range(2*k,10):
            for w in word_list(length):
                suffix=w[-(k-1):] if k>1 else ''
                key=(frozenset(factors(w,k)),w[:k-1],suffix)
                p=profile_set(w,k)
                if key in signatures:
                    require(signatures[key]==p,'factor/boundary signature determines profiles')
                else:
                    signatures[key]=p
        profile_classes+=len(signatures)
    padded=[]
    # Explicit bad words are padded in irreducible approximations, never in T.
    for n in range(2,9):
        approx=overlap(even,n)
        m=next(j for j in range(n,n+3) if j%2)
        bad='0'+'1'*m+'0'
        require(accepts(approx,bad) and not accepts(even,bad),'unbounded even obstruction')
        U=''
        for w in word_list(n):
            if accepts(even,w):
                U=merge(even,U,w)
        while len(U)<2*n:
            U=merge(even,U,U)
        V=merge(even,U,U)
        W=merge(approx,merge(approx,U,bad),U)
        require(accepts(even,V),'good padded word belongs to T')
        require(accepts(approx,W) and not accepts(even,W),'ideal padding retains bad factor')
        for k in range(1,n+1):
            require(profile_set(V,k)==profile_set(W,k),'saturation for every k <= n')
        padded.append({'n':n,'bad':bad,'good_length':len(V),'bad_length':len(W),
                       'checked_k':list(range(1,n+1))})
    # Exact reachability handles all finite word lengths, brute force checks it.
    cases=0
    for outputs in product(ALPHABET,repeat=4):
        table=dict(zip(word_list(2),outputs))
        for domain in basic.values():
            bad=exact_bad_word(domain,even,2,table)
            bounded=next((w for w in all_words if accepts(domain,w)
                          and not accepts(even,''.join(table[w[i:i+2]]
                                     for i in range(len(w)-1)))),None)
            if bad is None:
                require(bounded is None,'exact emptiness agrees with brute-force controls')
            else:
                require(accepts(domain,bad),'exact witness is a domain word')
                require(not accepts(even,''.join(table[bad[i:i+2]]
                        for i in range(len(bad)-1))),'exact witness produces forbidden output')
                if len(bad)<=7:
                    require(bounded is not None,'all short exact witnesses independently recovered')
            cases+=1
    # A width-three identity completion on the even shift may choose either
    # output on forbidden 010. Once n>=3, the completions agree everywhere.
    for missing_output in ALPHABET:
        table={w:(w[1] if accepts(even,w) else missing_output) for w in word_list(3)}
        require(exact_bad_word(overlap(even,3),even,3,table) is not None,
                'changing completion cannot repair even-shift identity')
    require(exact_bad_word(full,even,1,{'0':'0','1':'0'}) is None,
            'nononto constant even-shift map extends from full shift')
    require(not accepts(singleton,'1'),'short words do not pass vacuous local constraint')
    for n in range(2,7):
        require(exact_bad_word(overlap(alternating,n),alternating,1,
                {'0':'0','1':'1'}) is None,'irreducible periodic nonmixing control')
        require(exact_bad_word(overlap(golden,n),golden,1,
                {'0':'0','1':'1'}) is None,'SFT identity positive')
    print(json.dumps({'status':'PASS','checks':CHECKS,'two_vertex_irreducible_graphs':len(graphs),
                      'exact_radius_two_rule_cases':cases,'profile_signature_classes':profile_classes,
                      'saturation_controls':padded,
                      'scope':'Independent finite controls; no proof by bounded extrapolation.'},
                     indent=2,sort_keys=True))

if __name__=='__main__':
    main()
