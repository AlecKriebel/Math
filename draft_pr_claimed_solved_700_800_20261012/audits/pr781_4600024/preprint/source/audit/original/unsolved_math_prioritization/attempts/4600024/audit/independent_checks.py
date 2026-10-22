#!/usr/bin/env python3
"""Auditor-authored exact finite controls, independent of author code.
These tests are not a substitute for the proof or the imported PRZ theorem.
"""
from collections import deque
from itertools import product
import json

COUNT = 0

def require(value, label):
    global COUNT
    COUNT += 1
    if not value:
        raise RuntimeError(label)

def allwords(n):
    return (''.join(v) for v in product('01', repeat=n))

def walk(g, states, word):
    for letter in word:
        states = frozenset(t for s in states for a,t in g[s] if a == letter)
    return frozenset(states)

def language(g, w):
    return bool(walk(g, frozenset(g), w))

def irreducible(g):
    for q in g:
        reached = {q}
        while True:
            larger = reached | {t for s in reached for a,t in g[s]}
            if larger == reached:
                break
            reached = larger
        if reached != set(g):
            return False
    return all(g.values())

def approx(g,n):
    good = [w for w in allwords(n) if language(g,w)]
    vertices = {w[:-1] for w in good} | {w[1:] for w in good}
    return {v: [(w[-1],w[1:]) for w in good if w[:-1]==v] for v in vertices}

def connector(g,left,right):
    initial = walk(g, frozenset(g),left)
    todo = deque([(initial,'')]); seen = {initial}
    while todo:
        states, middle = todo.popleft()
        if walk(g,states,right):
            return left+middle+right
        for letter in '01':
            nxt=walk(g,states,letter)
            if nxt and nxt not in seen:
                seen.add(nxt); todo.append((nxt,middle+letter))
    raise RuntimeError('no connector')

def image(w,ell,table):
    return ''.join(table[w[i:i+ell]] for i in range(max(0,len(w)-ell+1)))

def bad_dfa(g,ell,table):
    first=('',frozenset(g))
    states=[first]; index={first:0}; rows=[]
    for buf, ends in states:
        row=[]
        for a in '01':
            b=buf+a
            new=(b,ends) if len(b)<ell else (b[1:],walk(g,ends,table[b]))
            if new not in index:
                index[new]=len(states); states.append(new)
            row.append(index[new])
        rows.append(row)
    rejecting={i for i,(_,ends) in enumerate(states) if not ends}
    return rows,rejecting

def bad_word(domain, rows, rejecting):
    # Graph/DFA reachability with a separate full word in each queue entry.
    todo=deque((q,0,'') for q in domain); seen={(q,0) for q in domain}
    while todo:
        q,s,w=todo.popleft()
        if s in rejecting:
            return w
        for a,t in domain[q]:
            z=rows[s][int(a)]
            if (t,z) not in seen:
                seen.add((t,z)); todo.append((t,z,w+a))
    return None

def profile(w,k):
    l=k//2; r=k-l
    return frozenset((w[max(0,i-l):i],w[i:i+r]) for i in range(len(w)))

def pad_check(g,n,w,ell,table):
    h=approx(g,n)
    U=''
    for t in allwords(n):
        if language(g,t):
            U=connector(g,U,t)
    while len(U)<2*n:
        U=connector(g,U,U)
    V=connector(g,U,U)
    W=connector(h,connector(h,U,w),U)
    require(language(g,V),'good padded word')
    require(language(h,W),'bad padded word in approximation')
    require(not language(g,image(W,ell,table)),'padded badness persists')
    for k in range(1,n+1):
        require(profile(V,k)==profile(W,k),'all profile scales agree')
    return len(V),len(W)

def labelled_image(g,ell,table):
    # Fixed-length input contexts ending at a presentation vertex.
    states=set()
    for q in g:
        for b in allwords(ell-1):
            for t in walk(g,{q},b):
                states.add((t,b))
    return {(q,b):[(table[b+a],(t,(b+a)[1:])) for a,t in g[q]] for q,b in states}

def includes(g,h):
    # L(g) subset L(h), using simultaneous subset construction.
    init=(frozenset(g),frozenset(h)); todo=[init]; seen={init}
    for x,y in todo:
        if x and not y:
            return False
        for a in '01':
            nxt=(walk(g,x,a),walk(h,y,a))
            if nxt not in seen:
                seen.add(nxt); todo.append(nxt)
    return True

def main():
    graphs=[]
    # Every binary-labelled graph on two vertices, including nondeterminism.
    for bits in product(range(4),repeat=4):
        g={q:[(str(a),t) for a in range(2) for t in range(2)
              if bits[2*q+a] & (1<<t)] for q in range(2)}
        if irreducible(g):
            graphs.append(g)
    short=[w for d in range(8) for w in allwords(d)]
    pad_cases=0
    identity={'0':'0','1':'1'}
    for g in graphs:
        rows,rej=bad_dfa(g,1,identity)
        for n in range(2,5):
            h=approx(g,n)
            require(irreducible(h),'canonical graph irreducible')
            for w in short:
                expected=(language(g,w) if len(w)<n else
                          all(language(g,w[i:i+n]) for i in range(len(w)-n+1)))
                require(language(h,w)==expected,'two-sided extension including short words')
            w=bad_word(h,rows,rej)
            if w is not None:
                pad_check(g,n,w,1,identity); pad_cases+=1
    E={0:[('0',0),('1',1)],1:[('1',0)]}
    rule_cases=0; self_rules=0; onto_rules=0; non_sft_positive=[]; negative_paddings=0
    for values in product('01',repeat=8):
        table=dict(zip(allwords(3),values)); rows,rej=bad_dfa(E,3,table)
        for w in short:
            state=0
            for a in w:
                state=rows[state][int(a)]
            require((state in rej)==(not language(E,image(w,3,table))),'bad DFA including empty and short words')
        valid=bad_word(E,rows,rej) is None
        if valid:
            self_rules+=1
            onto=includes(E,labelled_image(E,3,table))
            if onto:
                onto_rules+=1
            for n in range(2,6):
                w=bad_word(approx(E,n),rows,rej)
                if w is None and onto:
                    non_sft_positive.append({'table':''.join(values),'n':n})
                elif w is not None:
                    require(language(approx(E,n),w),'negative input witness')
                    require(not language(E,image(w,3,table)),'negative output witness')
                    pad_check(E,n,w,3,table); negative_paddings+=1
        # Direct contexts test ideal property for every forbidden short word.
        for w in short:
            if not language(E,image(w,3,table)):
                for u,v in [('0',''),('','1'),('01','10')]:
                    require(not language(E,image(u+w+v,3,table)),'two-sided ideal')
        rule_cases+=1
    # Nonmixing irreducible unary-on-a-binary-alphabet and period-two controls.
    periodic=[{0:[('0',0)]},{0:[('0',1)],1:[('1',0)]}]
    for g in periodic:
        for n in range(2,5):
            require(irreducible(approx(g,n)),'periodic canonical graph')
            require(includes(g,approx(g,n)) and includes(approx(g,n),g),'periodic SFT equality')
    print(json.dumps({'status':'PASS','checks':COUNT,'two_vertex_irreducible_graphs':len(graphs),
        'canonical_orders':[2,3,4],'words_through_length':7,'identity_padding_cases':pad_cases,
        'width_three_rules':rule_cases,'even_shift_self_rules':self_rules,
        'even_shift_onto_rules':onto_rules,'self_map_negative_padding_cases':negative_paddings,
        'non_sft_onto_positive_controls':non_sft_positive,
        'scope':'Finite controls only; universal result is audited in AUDIT.md.'},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
