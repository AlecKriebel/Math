#!/usr/bin/env python3
"""Independent finite checks; neither these nor the compiler prove input bounds."""
import importlib.util
import json
import platform
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("candidate", ROOT / "code/binary_compiler.py")
candidate = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = candidate
spec.loader.exec_module(candidate)


def accepts(states, initial, accepting, delta, word, positive=False):
    # This independent oracle DISABLES outward raw rules rather than asserting.
    tape = ("<",) + tuple(word) + (">",)
    pending = [(initial, 0, False)]
    seen = set(pending)
    while pending:
        q, pos, moved = pending.pop()
        if q in accepting and (moved or not positive):
            return True
        for r, d in delta(q, tape[pos]):
            assert r in states and d in (-1, 0, 1)
            if not 0 <= pos + d < len(tape):
                continue
            nxt = (r, pos + d, True)
            if nxt not in seen:
                seen.add(nxt)
                pending.append(nxt)
    return False


def truth(h, bits):
    w = h*h
    if len(bits) % w:
        return False
    # Compose the full relation, independently of a path-state NFA.
    relation = {(p,p) for p in range(h)}
    for start in range(0, len(bits), w):
        letter = {(p,q) for p in range(h) for q in range(h)
                  if bits[start+p*h+q] == 1}
        relation = {(p,r) for p,q in relation for q2,r in letter if q == q2}
    return bool(relation)


def ordinary_source(h):
    # Ordinary, no markers or epsilon transitions. Acceptance consumes the word.
    w = h*h
    start = ("S",)
    states = {start}
    states.update(("U",p,t) for p in range(h) for t in range((p+1)*h))
    states.update(("V",q,t) for q in range(h) for t in range(q+1,w))
    accepting = {start} | {("U",p,0) for p in range(h)}
    def delta(q,b):
        if q == start:
            return set().union(*(delta(("U",p,0),b) for p in range(h)))
        kind,v,t = q
        if kind == "V":
            return {("U",v,0)} if t+1 == w else {("V",v,t+1)}
        out = {("U",v,t+1)} if t+1 < (v+1)*h else set()
        if b == 1 and t//h == v:
            destination = ("U",t%h,0) if t+1 == w else ("V",t%h,t+1)
            out.add(destination)
        return out
    assert len(states) == (3*h**3-h)//2+1
    return states, start, accepting, delta


counts = {"ordinary_source_words":0, "endmarked_source_words":0,
          "fooling_crosses":0, "raw_one_state_nondeterministic_machines":0,
          "pullback_comparisons":0, "complement_identity_words":0}
for h, limit in ((1,12),(2,12)):
    states, q0, final, delta = ordinary_source(h)
    endmarked = candidate.binary_liveness_source(h)
    for length in range(limit+1):
        for bits in product((0,1), repeat=length):
            active = {q0}
            for b in bits:
                active = set().union(*(delta(q,b) for q in active)) if active else set()
            assert bool(active & final) == truth(h,bits)
            counts["ordinary_source_words"] += 1
            for positive in (False,True):
                assert accepts(endmarked.states, endmarked.initial,
                               endmarked.accepting, endmarked.transition,
                               bits, positive) == truth(h,bits)
                counts["endmarked_source_words"] += 1

for h in range(1,6):
    w = h*h
    I = tuple(int(t//h == t%h) for t in range(w))
    pairs = []
    for p in range(h):
        e = tuple(int(t == p*h+p) for t in range(w))
        for t in range(w):
            pairs.append((e+I[:t], I[t:]+e))
    for i,(x,y) in enumerate(pairs):
        for j,(_,y2) in enumerate(pairs):
            assert truth(h,x+y2) == (i == j)
            counts["fooling_crosses"] += 1

# Check every one-state raw nondeterministic table, including illegal outward
# rows. Normalize those rows before invoking the candidate's legal-row compiler.
moves = ((0,-1),(0,0),(0,1))
subsets = tuple(tuple(m for i,m in enumerate(moves) if mask>>i&1)
                for mask in range(8))
relation_words = tuple(word for k in range(3) for word in product(range(16),repeat=k))
for rows in product(subsets,repeat=4):
    raw = {symbol:row for symbol,row in zip(("<",0,1,">"),rows)}
    legal = {symbol:tuple((r,d) for r,d in row
                         if not(symbol == "<" and d == -1)
                         and not(symbol == ">" and d == 1))
             for symbol,row in raw.items()}
    for final in (frozenset(),frozenset({0})):
        binary = candidate.Machine((0,),0,final,lambda q,b:legal[b])
        compiled = candidate.pullback(2,binary)
        counts["raw_one_state_nondeterministic_machines"] += 1
        for word in relation_words:
            bits = tuple((R>>t)&1 for R in word for t in range(4))
            for positive in (False,True):
                lhs = accepts((0,),0,final,lambda q,b:raw[b],bits,positive)
                rhs = accepts(compiled.states, compiled.initial,compiled.accepting,
                              compiled.transition, word,positive)
                assert lhs == rhs
                counts["pullback_comparisons"] += 1

for word in (word for k in range(4) for word in product(range(16),repeat=k)):
    bits = tuple((R>>t)&1 for R in word for t in range(4))
    relation = {(p,p) for p in range(2)}
    for R in word:
        letter = {(p,q) for p in range(2) for q in range(2) if R>>(2*p+q)&1}
        relation = {(p,r) for p,q in relation for q2,r in letter if q == q2}
    assert (not truth(2,bits)) == (not relation)
    counts["complement_identity_words"] += 1

print(json.dumps({"status":"passed", "python":platform.python_version(), **counts,
                  "scope":"Encoding only; upstream lower bounds not established."},
                 sort_keys=True,indent=2))
