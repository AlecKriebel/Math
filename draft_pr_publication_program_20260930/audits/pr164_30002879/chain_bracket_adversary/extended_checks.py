#!/usr/bin/env python3
"""Export explicit cocycle witnesses, even-degree squares and F_4 insertions."""
import sys
sys.dont_write_bytecode = True
import json, random
from pathlib import Path
from itertools import product
from datetime import datetime, timezone
from direct_cochains import Model, bits, elimination, combine, require, monomial_bracket, actual_coordinate_set

def canonical_lifts(model,n):
    matrix=model.differential(n)
    _,kernel=elimination(matrix)
    coords=[model.shuffle(c,n) for c in kernel]
    piv,_=elimination(coords)
    allowed={(0,0,0,0),(0,1,0,0),(1,1,0,0)} if n==0 else {a for a in model.coordinates(n) if a[2]>0 or a[1]==1}
    positions={a:i for i,a in enumerate(model.coordinates(n))}
    lifts={}
    for monomial in sorted(allowed):
        target=1<<positions[monomial]
        witness=0
        while target:
            k=target.bit_length()-1
            require(k in piv,'missing actual cocycle coordinate')
            target ^= piv[k][0]
            witness ^= piv[k][1]
        f=combine(kernel,witness)
        require(combine(matrix,f)==0,'canonical witness fails cocycle')
        lifts[monomial]=f
    return lifts

def f4mul(a,b):
    z=0
    while b:
        if b&1:
            z ^= a
        b >>= 1
        a <<= 1
        if a&4:
            a ^= 7  # alpha^2 + alpha + 1.
    return z

def addto(d,k,v):
    d[k]=d.get(k,0)^v
    if d[k]==0:
        del d[k]

def field_cochain(lifts,scalars):
    out={}
    for m,f in lifts.items():
        for i in bits(f):
            addto(out,i,scalars[m])
    return out

def evaluate4(model,f,n,word):
    model.basis(n)
    out={}
    for a in model.outputs(word):
        i=model.indices[n].get((word,a))
        if i is not None and f.get(i,0):
            out[a]=f[i]
    return out

def circle4(model,f,p,g,q):
    n=p+q-1
    if p==0 or n<0:
        return {}
    model.basis(n)
    out={}
    for word in model.words(n):
        for slot in range(p):
            inner=evaluate4(model,g,q,word[slot:slot+q])
            for a,c in inner.items():
                if a not in model.J:
                    continue
                outer=evaluate4(model,f,p,word[:slot]+(a,)+word[slot+q:])
                for b,d in outer.items():
                    i=model.indices[n].get((word,b))
                    require(i is not None,'F4 insertion corner')
                    addto(out,i,f4mul(c,d))
    return out

def shuffle4(model,f,n):
    out={}
    for word in product((1,2),repeat=n):
        i=word.count(1)
        for a,c in evaluate4(model,f,n,word).items():
            if n==0 and a==4:
                continue
            require(a in model.A,'F4 restriction corner')
            addto(out,(a&1,(a>>1)&1,i,n-i),c)
    return out

def differential4(model,f,n):
    out={}
    cols=model.differential(n)
    for i,c in f.items():
        for row in bits(cols[i]):
            addto(out,row,c)
    return out

def run():
    model=Model()
    lifts={n:canonical_lifts(model,n) for n in range(4)}
    witnesses=[]
    for n in lifts:
        for m,f in lifts[n].items():
            witnesses.append({'degree':n,'monomial':m,'cochain_binary_hex':hex(f),'basis_order':'Model.basis(degree) in direct_cochains.py'})
    squares=[]
    for m,f in lifts[2].items():
        sq=model.circle(f,2,f,2)
        require(combine(model.differential(3),sq)==0,'actual divided square is not a cocycle')
        squares.append({'class':m,'divided_square_class':sorted(actual_coordinate_set(model,model.shuffle(sq,3),3))})
    selected=[]
    pairs=[((0,0,2,1),(0,1,0,0)),((0,0,3,0),(1,1,0,0)),((1,0,1,2),(0,0,1,0)),((1,0,1,2),(0,1,0,1)),((1,0,1,1),(0,1,0,0)),((1,0,1,1),(0,1,0,2)),((1,0,3,0),(1,1,0,2))]
    for m,k in pairs:
        p,q=m[2]+m[3],k[2]+k[3]
        h=model.bracket(lifts[p][m],p,lifts[q][k],q)
        n=p+q-1
        require(combine(model.differential(n),h)==0,'selected bracket not cocycle')
        value=actual_coordinate_set(model,model.shuffle(h,n),n)
        require(value==monomial_bracket(m,k),'selected bracket mismatch')
        selected.append({'left':m,'right':k,'actual_value':sorted(value),'cochain_binary_hex':hex(h)})
    rng=random.Random(16430002879)
    f4count=0
    for p,q in [(2,3),(3,2),(3,0),(2,1),(1,2),(1,0)]:
        for repeat in range(16):
            left={m:rng.randrange(4) for m in lifts[p]}
            right={m:rng.randrange(4) for m in lifts[q]}
            f,g=field_cochain(lifts[p],left),field_cochain(lifts[q],right)
            require(not differential4(model,f,p) and not differential4(model,g,q),'F4 input cocycle')
            h=circle4(model,f,p,g,q)
            for i,c in circle4(model,g,q,f,p).items():
                addto(h,i,c)
            n=p+q-1
            require(not differential4(model,h,n),'F4 bracket cocycle')
            expected={}
            for m,a in left.items():
                for k,b in right.items():
                    for z in monomial_bracket(m,k):
                        addto(expected,z,f4mul(a,b))
            require(shuffle4(model,h,n)==expected,'F4 actual insertion mismatch')
            f4count+=1
    return {'status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),'explicit_cocycle_witnesses':witnesses,'selected_actual_positive_degree_brackets':selected,'actual_even_degree_divided_squares':squares,'F4_actual_bracket_pairs':f4count,'F4_definition':'F2[alpha]/(alpha²+alpha+1), coefficients encoded 0,1,alpha,1+alpha as 0,1,2,3','scope':'Extra square diagnostics do not claim an all-degree restricted or strict Gerstenhaber presentation.'}

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path('extended_evidence.json')
    try:
        result=run()
        code=0
    except Exception as exc:
        result={'status':'FAIL','UTC':datetime.now(timezone.utc).isoformat(),'error_type':type(exc).__name__,'reason':str(exc)}
        code=1
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='explicit_cocycle_witnesses'},indent=2))
    sys.exit(code)
