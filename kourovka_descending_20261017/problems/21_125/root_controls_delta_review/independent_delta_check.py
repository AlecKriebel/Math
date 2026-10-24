#!/usr/bin/env python3
"""Exact boundary checks for the theoretical height-cover delta.

Finite checks do not prove the embedding or homology assertions; the
unbounded arguments are given in AUDIT.md. No author modules imported.
"""
from itertools import product
from pathlib import Path
import json


def reduce(word):
    ans = []
    for x in word:
        if ans and ans[-1] == -x:
            ans.pop()
        else:
            ans.append(x)
    return tuple(ans)


def inverse(word):
    return tuple(-x for x in reversed(word))


def substitute(word, images):
    result = []
    for x in word:
        image = images[x] if x > 0 else inverse(images[-x])
        result.extend(image)
    return reduce(result)


def words(length):
    yield ()
    layer = [()]
    for _ in range(length):
        nxt = []
        for w in layer:
            for x in (1,-1,2,-2):
                if not w or x != -w[-1]:
                    nxt.append(w + (x,))
        yield from nxt
        layer = nxt


def modular_rank(columns, p):
    # Build a basis by eliminating columns against earlier pivot vectors.
    basis = {}
    for col in columns:
        v = [x % p for x in col]
        for i in sorted(basis):
            if v[i]:
                v = [(a-v[i]*b)%p for a,b in zip(v,basis[i])]
        pivot = next((i for i,a in enumerate(v) if a), None)
        if pivot is not None:
            scale = pow(v[pivot],-1,p)
            basis[pivot] = [(a*scale)%p for a in v]
    return len(basis)


def modular_height_betti(m, d, p):
    # Apply J=(I+N) repeatedly to each standard basis vector; this uses
    # neither binomial coefficients nor the predicted nilpotent factor.
    columns = []
    for j in range(m):
        col = [int(i==j) for i in range(m)]
        for _ in range(d):
            col = [(col[i]+(col[i+1] if i+1<m else 0))%p for i in range(m)]
        col[j] = (col[j]-1)%p
        columns.append(col)
    return 1+m-modular_rank(columns,p)


def main():
    reduced_words = list(words(5))
    word_count, normal_forms = 0, 0
    for d in range(1,13):
        embedding = {1:(1,)*d,2:(2,)}
        domain_twist = {1:(1,),2:(2,1)}
        domain_twist_inverse = {1:(1,),2:(2,-1)}
        fiber_twist = {1:(1,),2:(2,)+(1,)*d}
        fiber_twist_inverse = {1:(1,),2:(2,)+(-1,)*d}
        images = set()
        for w in reduced_words:
            image = substitute(w,embedding)
            assert bool(image)==bool(w)
            assert image not in images
            images.add(image)
            assert substitute(substitute(w,domain_twist),embedding)==substitute(image,fiber_twist)
            assert substitute(substitute(w,domain_twist_inverse),embedding)==substitute(image,fiber_twist_inverse)
            word_count += 1
        normal_forms += len({(image,k) for image in images for k in range(-3,4)})
        # [B,u]=B^-1 u^-1 B u is theta^d(B) preceded by B^-1.
        assert reduce((-2,)+fiber_twist[2])==embedding[1]
    homology = []
    for m in (1,2,3,4,5,8,13,21):
        for d in (1,2,3,4,6,8,9,12,16,25,27,32,49,60,64):
            for p in (2,3,5,7,11):
                q, rem = 1, d
                while rem%p==0:
                    rem//=p
                    q*=p
                actual = modular_height_betti(m,d,p)
                assert actual==1+min(m,q), (m,d,p,q,actual)
                homology.append({'m':m,'d':d,'p':p,'b1':actual})
    result={'status':'PASS','free_word_images_checked_including_identity':word_count,
            'distinct_tested_height_normal_forms':normal_forms,
            'positive_and_negative_twist_intertwinings':2*word_count,
            'modular_homology_cases':len(homology),'homology_cases':homology,
            'scope':'Finite implementation and boundary checks only; all infinite claims require the independent proofs in AUDIT.md.'}
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='homology_cases'}))


if __name__=='__main__':
    main()
