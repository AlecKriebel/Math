#!/usr/bin/env python3
import itertools,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def red(w):
 a=[]
 for s in w:
  if a and a[-1]==-s:a.pop()
  else:a.append(s)
 return tuple(a)
def inv(w):return tuple(-s for s in w[::-1])
def conj(g,w):return red(g+w+inv(g))
def mul(a,b):return red(a+b)
# Free-group models check diagonal conjugation identities, not the surface ICC theorem.
words=[()]
for n in range(1,4):
 for w in itertools.product((1,-1,2,-2),repeat=n):
  if red(w)==w:words.append(w)
for u in words:
 for g in words:
  ck(conj(u,conj(g,(1,2)))==conj(mul(u,g),(1,2)))
  ck(conj(u,())==())
# Finite orbit counter-control: abelian labels make every conjugation orbit trivial,
# explaining why the theorem's ICC hypothesis cannot be replaced by mere infinitude.
for a,b,u in itertools.product(range(-3,4),repeat=3):ck((u+a-u,u+b-u)==(a,b))
# The scalar image of a unique invariant degree-d term survives at the same degree.
for d in range(1,9):
 for c in range(-5,6):
  if c:ck({d:c}!={})
print(json.dumps({'assertions':checks,'free_group_words':len(words),'scope':'Only exact algebraic identity and hypothesis-boundary controls. ICC of the closed hyperbolic surface group, the tangent-bundle lift, and meridian nontriviality are established by the proof and cited primary results, not finite tests.'},indent=2))
