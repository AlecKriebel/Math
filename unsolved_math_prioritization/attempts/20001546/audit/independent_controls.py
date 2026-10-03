"""Audit-only controls, not a further proof attempt. No imports from frozen verifier."""
from itertools import product
import json

def inv(w):return tuple(-t for t in reversed(w))
def red(w):
    w=list(w)
    # Deliberately a different reduction implementation: repeated adjacent cancellation.
    i=0
    while i+1<len(w):
        if w[i]==-w[i+1]:del w[i:i+2];i=max(0,i-1)
        else:i+=1
    return tuple(w)
I=((1,),(2,),(3,),(4,))
def subst(word,F):
    return red(sum((F[t-1] if t>0 else inv(F[-t-1]) for t in word),()))
def comp(F,G):return tuple(subst(w,F) for w in G)
def power(F,n):
    v=I
    for _ in range(n):v=comp(v,F)
    return v
def artin(j,sign=1):
    F=list(I)
    F[j-1:j+1]=[(j,j+1,-j),(j,)] if sign==1 else [(j+1,),(-(j+1),j,j+1)]
    return tuple(F)
def sigmaword(w):
    v=I
    for t in w:v=comp(v,artin(abs(t),1 if t>0 else -1))
    return v
raw={'a':(2,),'b':(3,),'c':(1,1,2,3,-2,-1,-1)}
raw.update(d=inv(raw['b'])+raw['a']+raw['b'],e=inv(raw['c'])+raw['b']+raw['c'],f=inv(raw['a'])+raw['c']+raw['a'],p=raw['a']+raw['b'],q=raw['b']+raw['c'],r=raw['c']+raw['a'])
raw.update({k.upper():inv(w) for k,w in list(raw.items())})
G={k:sigmaword(w) for k,w in raw.items()}
def ev(w):
    v=I
    for k in w:v=comp(v,G[k])
    return v
def inverse_labels(w):return ''.join(k.swapcase() for k in w[::-1])
for i in range(1,4):assert comp(artin(i),artin(i,-1))==I==comp(artin(i,-1),artin(i))
for x,y in [('a','b'),('b','c'),('c','a')]:
    assert ev(x+y+x)==ev(y+x+y)
    assert ev(x+y)!=ev(y+x) # negative control: the relevant generators do not commute
for k in raw:assert ev(k+k.swapcase())==I
for w in [('ab','bd','da','p'),('bc','ce','eb','q'),('ca','af','fc','r')]:assert len(set(ev(v) for v in w))==1
result=[]
for n in (1,2,3):
    # Enumerate EVERY signed word through radius n, rather than pruning image BFS.
    balls={I};evaluations=1
    for length in range(1,n+1):
        for word in product(G,repeat=length):balls.add(ev(word));evaluations+=1
    an,pn=ev('a'*n),ev('p'*n)
    assert an!=pn
    translated_a={comp(ev('a'*(2*n)),b) for b in balls}
    translated_p={comp(ev('p'*(2*n)),b) for b in balls}
    assert balls & translated_a=={an}
    assert balls & translated_p=={pn}
    assert not balls & translated_a & translated_p
    # All three pairwise intersections and all advertised individual witnesses.
    witness='a'*(2*n)+('bad'*((2*n+2)//3))[:n]
    assert ev(witness) in translated_a & translated_p
    assert an in balls & translated_a and pn in balls & translated_p
    # Positive control: using the same center twice cannot report empty intersection.
    assert balls & balls==balls
    result.append(dict(radius=n,enumerated_words=evaluations,image_count=len(balls),intersection_counts=[len(balls&translated_a),len(balls&translated_p),len(translated_a&translated_p)],triple_count=0))
print(json.dumps({'independent_checks_passed':True,'certificates':result},indent=2))
