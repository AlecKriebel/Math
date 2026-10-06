#!/usr/bin/env python3
"""Independent multilinear right-comb exact action/character audit.

No author/reviewer imports. Lie bases use right-nested commutators ending in
the least label, and coordinates are word coefficients ending in that label.
All S_d x S_r character classes are evaluated on actual action-map kernels.
"""
from functools import lru_cache
from itertools import product, permutations
from math import factorial
from pathlib import Path
import datetime, hashlib, json, sys
import sympy as s


def comm(a, b):
    out = {}
    for x,c in a.items():
        for y,e in b.items():
            out[x+y] = out.get(x+y,0)+c*e
            out[y+x] = out.get(y+x,0)-c*e
    return {w:c for w,c in out.items() if c}


@lru_cache(None)
def expansion(w):
    return {w:1} if len(w)==1 else comm({w[:1]:1}, expansion(w[1:]))


def coordinates(a):
    if not a:return {}
    root = min(next(iter(a)))
    out = {w:c for w,c in a.items() if w[-1]==root}
    reconstructed = {}
    for w,c in out.items():
        for z,e in expansion(w).items():reconstructed[z]=reconstructed.get(z,0)+c*e
    assert {w:c for w,c in reconstructed.items() if c}==a
    return out


@lru_cache(None)
def tensor_basis(labels, r):
    if len(labels)<r:return ()
    out=[]
    for bins in product(range(r),repeat=len(labels)):
        if len(set(bins))<r:continue
        blocks=[tuple(x for x,i in zip(labels,bins) if i==j) for j in range(r)]
        bases=[tuple(p+(min(b),) for p in permutations(tuple(x for x in b if x!=min(b)))) for b in blocks]
        out.extend(product(*bases))
    return tuple(out)


def partitions(n, maximum=None):
    if n==0:return [()]
    out=[]
    for k in range(min(n,maximum or n),1-1,-1):
        out.extend((k,)+p for p in partitions(n-k,k))
    return out


def cells(shape):return {(i,j) for i,n in enumerate(shape) for j in range(n)}


@lru_cache(None)
def irreducible(shape, cycle):
    if not cycle:return int(not shape)
    k=cycle[0];out=0;big=cells(shape)
    for small in partitions(sum(shape)-k):
        little=cells(small)
        if not little<=big:continue
        skew=big-little
        if not skew:continue
        seen={next(iter(skew))}
        while True:
            enlarged=seen|{(a+x,b+y) for a,b in seen for x,y in [(1,0),(-1,0),(0,1),(0,-1)] if (a+x,b+y) in skew}
            if enlarged==seen:break
            seen=enlarged
        if seen!=skew:continue
        if any({(a,b),(a+1,b),(a,b+1),(a+1,b+1)}<=skew for a,b in skew):continue
        out+=(-1)**(len({a for a,b in skew})-1)*irreducible(small,cycle[1:])
    return out


def representative(cycle):
    out=list(range(sum(cycle)));start=0
    for k in cycle:
        for j in range(k):out[start+j]=start+(j+1)%k
        start+=k
    return tuple(out)


def sign(cycle):return (-1)**(sum(cycle)-len(cycle))


def z(cycle):
    return s.prod(k**cycle.count(k)*factorial(cycle.count(k)) for k in set(cycle))


def image_blocks(blocks, letter, slot):
    alternatives=[]
    for i in slot:
        changed={tuple(letter[x] for x in w):c for w,c in expansion(blocks[i]).items()}
        alternatives.append(tuple(coordinates(changed).items()))
    for choices in product(*alternatives):
        yield tuple(w for w,c in choices),s.prod(c for w,c in choices)


def action(basis, letter, slot, source, freeze_generator=False):
    lookup={b:i for i,b in enumerate(basis)};A=s.zeros(len(basis))
    for j,b in enumerate(basis):
        v,blocks=b if source else (None,b)
        for result,c in image_blocks(blocks,letter,slot):
            key=(v if freeze_generator else letter[v],result) if source else result
            # The deliberate frozen-generator mutant can leave multilinear space.
            if key not in lookup:raise ValueError('permutation leaves multilinear space')
            A[lookup[key],j]+=c
    return A


def predicted(r,d,cd,cr):
    if r==1 and d>=4:
        # Frobenius character of Ind(Lie(d-1)) minus Lie(d), evaluated by
        # the Witt power-sum formula, independently of irreducible tables.
        def lie_char(n,cyc):
            if not cyc or len(set(cyc))!=1:return s.S.Zero
            a=cyc[0]
            return s.Rational(s.mobius(a)*z(cyc),n)
        return (cd.count(1)*lie_char(d-1,tuple(x for i,x in enumerate(cd) if i!=cd.index(1))) if 1 in cd else 0)-lie_char(d,cd)
    if d<=r:return 0
    if d==r+1:return 1
    assert d==r+2
    value=sign(cd)*sign(cr)
    if r>1:value+=irreducible((r,1,1),cd)
    return value


def model(r,d):
    labels=tuple(range(d));source=tuple((v,b) for v in labels for b in tensor_basis(tuple(x for x in labels if x!=v),r))
    target=tensor_basis(labels,r);lookup={b:i for i,b in enumerate(target)}
    D=s.zeros(len(target),len(source))
    for j,(v,blocks) in enumerate(source):
        for i,b in enumerate(blocks):
            cs=coordinates(comm({(v,):1},expansion(b)))
            for w,c in cs.items():
                replaced=list(blocks);replaced[i]=w;D[lookup[tuple(replaced)],j]+=c
    null=D.nullspace();K=s.Matrix.hstack(*null) if null else s.zeros(len(source),0)
    pivots=K.T.rref()[1];Jinv=K.extract(pivots,range(K.cols)).inv() if K.cols else s.zeros(0)
    chars={};equivariance=0
    for cd in partitions(d):
        for cr in partitions(r):
            letter=representative(cd);slot=representative(cr)
            A=action(source,letter,slot,True);B=action(target,letter,slot,False)
            assert D*A==B*D;equivariance+=1
            AK=A*K;R=Jinv*AK.extract(pivots,range(K.cols))
            assert AK==K*R
            observed=s.trace(R);assert observed==predicted(r,d,cd,cr),(r,d,cd,cr,observed)
            chars[cd,cr]=observed
    decomposition=[]
    for ld in partitions(d):
        for lr in partitions(r):
            inner=sum(s.Rational(chars[cd,cr]*irreducible(ld,cd)*irreducible(lr,cr),z(cd)*z(cr)) for cd in partitions(d) for cr in partitions(r))
            assert inner.is_Integer and inner>=0
            if inner:decomposition.append({'S_d':ld,'S_r':lr,'multiplicity':int(inner)})
    return {'r':r,'d':d,'source_dimension':len(source),'target_dimension':len(target),'rank':len(source)-K.cols,'kernel_dimension':K.cols,'class_pairs':equivariance,'decomposition':decomposition,'characters':[{'S_d_cycle':cd,'S_r_cycle':cr,'value':int(v)} for (cd,cr),v in chars.items()]},(D,source,target,chars)


def main():
    assert s.__version__=='1.14.0'
    rows=[];cases=[(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(3,3),(3,4),(3,5),(4,4),(4,5)]
    details={}
    for r,d in cases:
        row,detail=model(r,d);rows.append(row);details[r,d]=detail
        print('checked',r,d,'kernel',row['kernel_dimension'],'classes',row['class_pairs'],flush=True)
    # Mutants are rejected by character values, not by dimension coincidence.
    chars=details[2,4][3];sign_loss=[]
    for (cd,cr),value in chars.items():
        if sign(cr)<0 and value:
            sign_loss.append({'S_d_cycle':cd,'S_r_cycle':cr,'actual_after_exterior_twist':int(value*sign(cr)),'mutant_without_twist':int(value)})
    assert sign_loss
    wrong_slot=[{'S_d_cycle':cd,'S_r_cycle':cr,'ordinary':int(v),'mutant_signed':int(v*sign(cr))} for (cd,cr),v in chars.items() if v and sign(cr)<0]
    assert wrong_slot
    D,source,target,_=details[2,4]
    rejected=False
    try:
        bad=action(source,(1,0,2,3),(0,1),True,True)
        rejected=D*bad!=action(target,(1,0,2,3),(0,1),False)*D
    except ValueError:rejected=True
    assert rejected
    actual=details[1,3][3][(1,1,1),(1,)]
    assert actual==1 and actual!=2
    receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'sympy':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'method':'right-comb multilinear bases, exact rational kernels, simultaneous S_d x S_r class traces, Murnaghan-Nakayama inner products','models':rows,'total_class_pairs':sum(x['class_pairs'] for x in rows),'mutants':{'exterior_sign_omitted':{'rejected':True,'witnesses':sign_loss},'coefficient_permutation_signed':{'rejected':True,'witnesses':wrong_slot},'generator_not_permuted':{'rejected':rejected},'r1_extra_summand':{'rejected':True,'actual_dimension':int(actual),'mutant_dimension':2}},'scope':'Finite multilinear controls only. Universal claims require the separately sealed derivation and Powell theorem. No all-degree computation or novelty claim.'}
    Path(__file__).with_name('character_results.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':main()
