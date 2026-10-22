#!/usr/bin/env python3
"""Fresh exact finite diagnostics; the arbitrary-size theorem is a written proof."""
import hashlib,itertools,json
def need(c,m):
    if not c:raise ValueError(m)
def reduce_word(w):
    out=[]
    for x in w:
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return tuple(out)
def inverse(w):return tuple(-x for x in reversed(w))
def cyclic(w):
    w=reduce_word(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return min((w[i:]+w[:i] for i in range(len(w))),default=())
def horowitz(signs):
    w=(1,)
    for m,e in enumerate(signs,1):
        z=w if e==1 else inverse(w);zi=inverse(z)
        w=reduce_word(zi+(2,)*(2*m)+z+(2,)*(2*m-1)+zi+(2,)*(2*m)+z)
    return w
ID=(1,0,0,1)
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def inv(a):return (a[3],-a[1],-a[2],a[0])
def det(a):return a[0]*a[3]-a[1]*a[2]
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def evaluate(w,a,b):
    lookup={1:a,-1:inv(a),2:b,-2:inv(b)};out=ID
    for x in w:out=mul(out,lookup[x])
    return out
def trace(a):return a[0]+a[3]
def integer_binding(n):
    raw=abs(n).to_bytes(max(1,(abs(n).bit_length()+7)//8),'big')
    return {'sign':(n>0)-(n<0),'bits':abs(n).bit_length(),'absolute_big_endian_sha256':hashlib.sha256(raw).hexdigest()}
def main():
    need(cyclic((1,2))==cyclic((2,1)),'cyclic rotation control')
    need(cyclic((2,1,-2))==cyclic((1,)),'conjugation control')
    need(cyclic((1,))!=cyclic((-1,)),'oriented inversion control')
    need(cyclic((1,1))!=cyclic((1,1,1)),'proper power control')
    n=8;a=(1,n,0,1);b=(1,0,-n,1);u=b
    for j in range(2,4):u=comm(a,u)
    v=mul(mul(b,u),inv(b));reps=[((1,2,0,1),(1,0,2,1)),((2,1,1,1),(1,1,0,1)),(u,v)]
    need(all(det(x)==1 for pair in reps for x in pair),'SL2 determinant')
    families=[];faults=[]
    for m in range(1,5):
        words=[horowitz(signs) for signs in itertools.product((-1,1),repeat=m)]
        need(all(words) and len({cyclic(w) for w in words})==2**m,'nontrivial free conjugacy family')
        row={'m':m,'classes':len(words),'max_reduced_length':max(map(len,words)),'representations':[]}
        altered=reduce_word(words[-1]+(2,));detected=[]
        for i,(x,y) in enumerate(reps):
            matrices=[evaluate(w,x,y) for w in words];ts=[trace(z) for z in matrices]
            need(all(det(z)==1 for z in matrices),'word determinant');need(len(set(ts))==1,'common exact trace')
            if i==2:need(abs(ts[0])>2,'actual n8k3 subgroup hyperbolicity')
            detected.append(trace(evaluate(altered,x,y))!=ts[0])
            row['representations'].append({'index':i,'trace':integer_binding(ts[0]),'common_trace':True})
        need(any(detected),'deliberately altered word must be detected');faults.append({'m':m,'appended_b_detected_in_representations':detected});families.append(row)
    print(json.dumps({'status':'PASS','families':families,'canonical_word_controls':4,'actual_altered_word_controls':faults,'n8_k3_basis':{'u':list(u),'v':list(v)},'scope':'Fresh stdlib exact integer/free-word diagnostics from the visually checked Horowitz recurrence, m1–4 and three SL2 representations including the fixed genus2 n8,k3 construction. Not an arbitrary-m proof, Johnson-depth proof, geometric realizability certificate for other n, or ambient nonconjugacy certificate. Those rest on written arguments. No historical omitted program/receipt replay or source-author code execution claimed.'},sort_keys=True))
if __name__=='__main__':main()
