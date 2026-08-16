#!/usr/bin/env python3
from fractions import Fraction as F

T=(F(-1),F(5))
intervals={
    1:(F(-1),F(2)),
    2:(F(0),F(4)),
    3:(F(2),F(5)),
    4:None,
    5:T,
}
classes=sorted({T[0],T[1]} | {x for J in intervals.values() if J and J!=T for x in J})

def active(t):
    out=set()
    for i,J in intervals.items():
        if J is None: continue
        if J[0] < t < J[1]: out.add(i)
    return frozenset(out)

# Test every endpoint class and every complementary open cell.
tests=[]
for x in classes[1:-1]:
    tests.append((x,'endpoint'))
for a,b in zip(classes,classes[1:]):
    tests.append(((a+b)/2,'cell'))
words=[active(t) for t,_ in tests]
assert all(words), words
assert active(F(2))==frozenset({2,5})  # simultaneous end/start event
assert active(F(1))==frozenset({1,2,5})
assert active(F(3))==frozenset({2,3,5})

# Order-equivalent rational replacement: only equality/order classes matter.
rank={x:F(2*k-7,3) for k,x in enumerate(classes)}
newT=(rank[T[0]],rank[T[1]])
newints={}
for i,J in intervals.items():
    if J is None: newints[i]=None
    elif J==T: newints[i]=newT
    else: newints[i]=(rank[J[0]],rank[J[1]])

def newactive(t):
    return frozenset(i for i,J in newints.items() if J is not None and J[0]<t<J[1])
newclasses=sorted(rank.values())
newtests=[]
for x in newclasses[1:-1]: newtests.append(x)
for a,b in zip(newclasses,newclasses[1:]): newtests.append((a+b)/2)
assert [newactive(t) for t in newtests]==words
print('RATIONAL INTERVAL BRIDGE PASS')
print('SIMULTANEOUS ENDPOINT CLASS PASS')
print('COVERAGE: RELATIVE EMPTY WORD ABSENT')
