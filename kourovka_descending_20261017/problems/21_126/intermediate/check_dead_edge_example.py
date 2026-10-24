#!/usr/bin/env python3
"""Exact dead-edge example; does not compute a general Dehn function.

A=Z(a) x (Z(b) * Z^2(z,w)), weights (2,3,0,0).
H=ker phi = Z(B) * Z^2(z0,w0) * Z^2(z1,w1),
B=a^-3 b^2, z1=b z b^-1, w1=b w b^-1.
"""
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json

def inverse(letter):return letter[0],-letter[1]
def reduced_words(alphabet,max_length):
    yield ()
    layer=[()]
    for _ in range(max_length):
        nxt=[]
        for w in layer:
            for x in alphabet:
                if not w or x!=inverse(w[-1]):
                    v=w+(x,);nxt.append(v);yield v
        layer=nxt

def normalize(entries):
    stack=[]
    for factor,vector in entries:
        if not any(vector):continue
        if stack and stack[-1][0]==factor:
            _,old=stack.pop();vector=tuple(x+y for x,y in zip(old,vector))
        if any(vector):stack.append((factor,tuple(vector)))
    return tuple(stack)
def fnormal(word):
    entries=[]
    for x,e in word:
        if x=='b':entries.append((0,(e,)))
        elif x=='z':entries.append((1,(e,0)))
        elif x=='w':entries.append((1,(0,e)))
        else:raise AssertionError(x)
    return normalize(entries)
def enormal(word):
    entries=[]
    for x,e in word:
        if x=='B':entries.append((0,(e,)))
        else:
            i=int(x[1]);entries.append((i+1,(e,0) if x[0]=='z' else (0,e)))
    return normalize(entries)
def schreier(word):
    parity=0;out=[]
    for x,e in word:
        if x=='b':
            if e==1:
                if parity:out.append(('B',1))
                parity=1-parity
            else:
                if not parity:out.append(('B',-1))
                parity=1-parity
        else:out.append((x+str(parity),e))
    return tuple(out),parity

def expand(word):
    a=0;out=[]
    for x,e in word:
        if x=='B':a-=3*e;out.extend([('b',e),('b',e)])
        else:
            i=int(x[1]);out.extend([('b',1)]*i);out.append((x[0],e));out.extend([('b',-1)]*i)
    return a,tuple(out)

def main():
    fa=[(x,e) for x in ('b','z','w') for e in (1,-1)]
    ea=[(x,e) for x in ('B','z0','w0','z1','w1') for e in (1,-1)]
    forward=0;backward=0;nonempty=0
    for word in reduced_words(fa,7):
        q=sum(e for x,e in word if x=='b')
        if q%2:continue
        eword,parity=schreier(word);assert parity==0
        a,fword=expand(eword)
        assert a==-3*(q//2)
        assert fnormal(fword)==fnormal(word)
        assert bool(enormal(eword))==bool(fnormal(word))
        forward+=1;nonempty+=bool(enormal(eword))
    for word in reduced_words(ea,5):
        a,fword=expand(word)
        rewritten,parity=schreier(fword);assert parity==0
        assert enormal(rewritten)==enormal(word)
        assert 2*a+3*sum(e for x,e in fword if x=='b')==0
        backward+=1
    # The only stable relations in this example match the dead-edge lifts.
    for i in (0,1):
        rel=((f'z{i}',1),(f'w{i}',1),(f'z{i}',-1),(f'w{i}',-1))
        a,word=expand(rel);assert a==0 and fnormal(word)==()
    cross=(('z0',1),('w1',1),('z0',-1),('w1',-1))
    assert enormal(cross)!=()
    a,word=expand(cross);assert a==0 and fnormal(word)!=()
    exponents=[];a=4
    for d in range(11):
        assert a==(9*3**d-1)//2
        exponents.append({'dead_vertices':d,'upper_exponent':a});a=3*a+1
    out={'generated_utc':datetime.now(timezone.utc).isoformat(),'result':'PASS',
         'group':'Z(a) x (Z(b) * Z^2(z,w)); weights (2,3,0,0)',
         'kernel':'Z(B) * Z^2(z0,w0) * Z^2(z1,w1)',
         'ambient_even_b_words_through_length_7':forward,'nonidentity_forward_cases':nonempty,
         'kernel_generator_words_through_length_5':backward,
         'cross_residue_commutator_nontrivial':True,
         'polynomial_induction_exponents':exponents,
         'scope':'Exact normal-form test in one non-independent-dead example. General theorem depends on proof and independent review, not this finite test.'}
    Path(__file__).with_name('dead_edge_example_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
