#!/usr/bin/env python3
"""Independent normalized E-relative Hochschild and insertion audit over F_2.

No imports of submission code. Cochains are exact binary vectors. Explicit
exceptions, rather than assertions, make every gate active under python -O.
"""
from itertools import product
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, sys

class AuditFailure(RuntimeError):
    pass

def require(condition, label):
    if not condition:
        raise AuditFailure(label)

def bits(v):
    while v:
        b = v & -v
        yield b.bit_length()-1
        v ^= b

def reduce_vector(v, pivots):
    while v:
        k = v.bit_length()-1
        if k not in pivots:
            break
        v ^= pivots[k][0]
    return v

def elimination(columns):
    """Return independent image pivots and exact domain relations."""
    pivots = {}
    null = []
    for i, col in enumerate(columns):
        v, witness = col, 1 << i
        while v:
            k = v.bit_length()-1
            if k not in pivots:
                pivots[k] = (v, witness)
                break
            v ^= pivots[k][0]
            witness ^= pivots[k][1]
        if not v:
            null.append(witness)
    return pivots, null

def combine(columns, vector):
    out = 0
    for i in bits(vector):
        out ^= columns[i]
    return out

class Model:
    # f,x,y,xy,e,m,xm; radical basis x,y,xy,m,xm.
    A = (0,1,2,3)
    J = (1,2,3,5,6)
    def __init__(self, mutation=None):
        self.mutation = mutation
        self.tables = {}
        self.indices = {}
        self.word_cache = {}
        self.d_cache = {}

    def mul(self, a, b):
        if a in self.A and b in self.A:
            if a & b:
                return 0
            return 1 << (a | b)
        if a in self.A and b in (5,6):
            if a in (2,3):
                return 0
            if a == 1:
                if self.mutation == 'trivial_module' or b == 6:
                    return 0
                return 1 << 6
            return 1 << b
        if a in (5,6) and b == 4:
            return 1 << a
        if a == 4 and b == 4:
            return 1 << 4
        return 0

    def mulvec(self, x, y):
        out = 0
        for a in bits(x):
            for b in bits(y):
                out ^= self.mul(a,b)
        return out

    def words(self, n):
        if n not in self.word_cache:
            if n == 0:
                self.word_cache[n] = [()]
            else:
                self.word_cache[n] = list(product((1,2,3),repeat=n)) + [a+(b,) for a in product((1,2,3),repeat=n-1) for b in (5,6)]
        return self.word_cache[n]

    def outputs(self, word):
        if not word:
            return (0,1,2,3,4)
        return self.A if word[-1] in self.A else (5,6)

    def basis(self, n):
        if n not in self.tables:
            self.tables[n] = [(w,a) for w in self.words(n) for a in self.outputs(w)]
            self.indices[n] = {wa:i for i,wa in enumerate(self.tables[n])}
        return self.tables[n]

    def evaluate(self, f, n, word):
        self.basis(n)
        out = 0
        for a in self.outputs(word):
            i = self.indices[n].get((word,a))
            if i is not None and (f >> i) & 1:
                out ^= 1 << a
        return out

    def differential(self, n):
        if n in self.d_cache:
            return self.d_cache[n]
        self.basis(n)
        self.basis(n+1)
        cols = [0]*len(self.tables[n])
        for row,(w,out) in enumerate(self.tables[n+1]):
            # Compute delta by evaluating each elementary source contribution.
            for a in self.outputs(w[1:]):
                i = self.indices[n].get((w[1:],a))
                if i is not None and (self.mul(w[0],a) >> out) & 1:
                    cols[i] ^= 1 << row
            for slot in range(n):
                merged = self.mul(w[slot],w[slot+1])
                for a in bits(merged):
                    w2 = w[:slot]+(a,)+w[slot+2:]
                    i = self.indices[n].get((w2,out))
                    if i is not None:
                        cols[i] ^= 1 << row
            if self.mutation != 'omit_right_boundary':
                for a in self.outputs(w[:-1]):
                    i = self.indices[n].get((w[:-1],a))
                    if i is not None and (self.mul(a,w[-1]) >> out) & 1:
                        cols[i] ^= 1 << row
        self.d_cache[n] = cols
        return cols

    def circle(self, f,p,g,q):
        n = p+q-1
        if p == 0 or n < 0:
            return 0
        self.basis(n)
        out = 0
        slots = range(p-1) if self.mutation == 'omit_last_insertion' else range(p)
        for word in self.words(n):
            value = 0
            for slot in slots:
                inner = self.evaluate(g,q,word[slot:slot+q])
                for a in bits(inner):
                    # Projection B -> B/E enforces normalization, also for q=0.
                    if a not in self.J:
                        continue
                    w2 = word[:slot]+(a,)+word[slot+q:]
                    value ^= self.evaluate(f,p,w2)
            for a in bits(value):
                i = self.indices[n].get((word,a))
                require(i is not None,'insertion violated E-bimodule corner')
                out ^= 1 << i
        return out

    def bracket(self,f,p,g,q):
        return self.circle(f,p,g,q) ^ self.circle(g,q,f,p)

    def coordinates(self,n):
        return [(a,b,i,n-i) for i in range(n+1) for a,b in product(range(2),repeat=2)]

    def shuffle(self,f,n):
        # Coefficient on the shuffle chain with i x's and j y's.
        coords = self.coordinates(n)
        pos = {m:i for i,m in enumerate(coords)}
        out = 0
        for word in product((1,2),repeat=n):
            i = word.count(1)
            value = self.evaluate(f,n,word)
            for a in bits(value):
                if n == 0 and a == 4:
                    continue  # Coefficient B -> A kills the e-corner.
                require(a in self.A,'all-A restriction has non-A output')
                out ^= 1 << pos[(a & 1,(a >> 1) & 1,i,n-i)]
        return out

    def cup(self,f,p,g,q):
        n=p+q
        self.basis(n)
        out=0
        for word in self.words(n):
            value=self.mulvec(self.evaluate(f,p,word[:p]),self.evaluate(g,q,word[p:]))
            for a in bits(value):
                i=self.indices[n].get((word,a))
                require(i is not None,'cup violated corner')
                out ^= 1 << i
        return out

def monomial_bracket(m,n):
    # Differentiation independently implemented as a multivariable contraction.
    out=defaultdict(int)
    for pos,dual in ((0,2),(2,0),(1,3),(3,1)):
        if m[pos]%2 and n[dual]%2:
            exponents=[m[t]+n[t] for t in range(4)]
            exponents[pos]-=1
            exponents[dual]-=1
            if min(exponents)>=0 and exponents[0]<2 and exponents[1]<2:
                out[tuple(exponents)] ^= 1
    return {a for a,c in out.items() if c}

def actual_coordinate_set(model,v,n):
    coords=model.coordinates(n)
    return {coords[i] for i in bits(v)}

def shuffle_chain_gate(max_n=9):
    # Bare bar middle factors; endpoints carry polynomial exponents.
    for n in range(max_n+1):
        for i in range(n+1):
            j=n-i
            words=[w for w in product((1,2),repeat=n) if w.count(1)==i]
            boundary=defaultdict(int)
            for w in words:
                if not w:
                    continue
                boundary[(w[0],w[1:],0)] ^= 1
                boundary[(0,w[:-1],w[-1])] ^= 1
                for s in range(n-1):
                    if w[s]!=w[s+1]:
                        boundary[(0,w[:s]+(3,)+w[s+2:],0)] ^= 1
            expected=defaultdict(int)
            for t,k in ((1,i),(2,j)):
                if k:
                    for w in product((1,2),repeat=n-1):
                        if w.count(1)==i-(t==1):
                            expected[(t,w,0)] ^= 1
                            expected[(0,w,t)] ^= 1
            require({k for k,v in boundary.items() if v}=={k for k,v in expected.items() if v},'shuffle chain boundary')
    return max_n

def run(mutation=None):
    model=Model(mutation)
    for a,b,c in product(range(7),repeat=3):
        require(model.mulvec(model.mul(a,b),1<<c)==model.mulvec(1<<a,model.mul(b,c)), 'basis multiplication associativity')
    unit=(1<<0)|(1<<4)
    for a in range(7):
        require(model.mulvec(unit,1<<a)==1<<a and model.mulvec(1<<a,unit)==1<<a,'two-sided unit')
    dims=[]
    lifts={}
    cycles={}
    matrices={n:model.differential(n) for n in range(5)}
    for n in range(4):
        for column in matrices[n]:
            require(combine(matrices[n+1],column)==0,'delta squared zero')
    for n in range(5):
        dpiv,kernel=elimination(matrices[n])
        cycles[n]=kernel
        previous=[] if n==0 else matrices[n-1]
        bpiv,_=elimination(previous)
        expected=3 if n==0 else 4*n+2
        hh=len(kernel)-len(bpiv)
        require(hh==expected,f'cohomology dimension degree {n}: {hh}, expected {expected}')
        coords=[model.shuffle(c,n) for c in kernel]
        spiv,snull=elimination(coords)
        allowed={(0,0,0,0),(0,1,0,0),(1,1,0,0)} if n==0 else {a for a in model.coordinates(n) if a[2]>0 or a[1]==1}
        for co in coords:
            require(actual_coordinate_set(model,co,n)<=allowed,f'actual gamma image lies in L degree {n}')
        require(len(spiv)==expected,f'gamma surjective onto claimed image degree {n}')
        for relation in snull:
            require(reduce_vector(combine(kernel,relation),bpiv)==0,f'gamma kernel is an actual boundary degree {n}')
        bycoord={m:i for i,m in enumerate(model.coordinates(n))}
        lifts[n]={}
        for m in sorted(allowed):
            target=1<<bycoord[m]
            witness=0
            while target:
                k=target.bit_length()-1
                require(k in spiv,f'canonical coordinate has no cocycle lift {m}')
                target ^= spiv[k][0]
                witness ^= spiv[k][1]
            f=combine(kernel,witness)
            require(combine(matrices[n],f)==0,'lift is a cocycle')
            require(model.shuffle(f,n)==1<<bycoord[m],'lift has exact shuffle coordinate')
            lifts[n][m]=f
        dims.append({'degree':n,'cochains':len(model.basis(n)),'differential_rank':len(dpiv),'cocycles':len(kernel),'boundaries':len(bpiv),'HH':hh,'gamma_rank':len(spiv),'gamma_kernel_checked_as_boundaries':len(snull)})
    count=0
    examples=[]
    for p in range(4):
        for q in range(3):
            if p+q==0:
                continue
            n=p+q-1
            for m,f in lifts[p].items():
                for k,g in lifts[q].items():
                    h=model.bracket(f,p,g,q)
                    require(combine(matrices[n],h)==0,'actual insertion bracket is a cocycle')
                    actual=actual_coordinate_set(model,model.shuffle(h,n),n)
                    expected=monomial_bracket(m,k)
                    require(actual==expected,f'actual insertion bracket mismatch {m},{k}: {actual}, expected {expected}')
                    count+=1
                    if p in (2,3) and q in (0,1,2) and actual and len(examples)<36:
                        examples.append({'left':m,'right':k,'value':sorted(actual),'arity':n})
    cups=0
    for p in range(4):
        for q in range(4-p):
            for m,f in lifts[p].items():
                for k,g in lifts[q].items():
                    h=model.cup(f,p,g,q)
                    require(combine(matrices[p+q],h)==0,'actual cup is a cocycle')
                    target=tuple(a+b for a,b in zip(m,k))
                    expected={target} if target[0]<2 and target[1]<2 else set()
                    require(actual_coordinate_set(model,model.shuffle(h,p+q),p+q)==expected,'actual cup coordinate')
                    cups+=1
    squares=[]
    for m,f in lifts[1].items():
        sq=model.circle(f,1,f,1)
        require(combine(matrices[1],sq)==0,'degree-one square is cocycle')
        squares.append({'class':m,'restricted_square':sorted(actual_coordinate_set(model,model.shuffle(sq,1),1))})
    return {'status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),'family':'independent normalized E-relative cochain / actual insertion','field':'F_2 exact; universal field extension justified separately','mutation':mutation,'dimensions':dims,'actual_insertion_pairs':count,'actual_cup_pairs':cups,'positive_degree_examples':examples,'degree_one_squares':squares,'shuffle_chain_max_degree':shuffle_chain_gate(),'strict_gates_survive_optimization':True,'scope':'Finite computations are diagnostics; all-degree claims require the separate derivation.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--mutation',choices=['trivial_module','omit_right_boundary','omit_last_insertion'])
    args=parser.parse_args()
    try:
        result=run(args.mutation)
        if args.mutation:
            raise AuditFailure('mutation unexpectedly survived; fail-closed mutation gate')
        exitcode=0
    except Exception as exc:
        result={'status':'FAIL','UTC':datetime.now(timezone.utc).isoformat(),'mutation':args.mutation,'error_type':type(exc).__name__,'reason':str(exc)}
        exitcode=1
    payload=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(payload)
    print(payload)
    sys.exit(exitcode)
