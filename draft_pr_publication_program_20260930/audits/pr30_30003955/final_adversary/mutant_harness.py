#!/usr/bin/env python3
"""Deliberate false assertions, each must actually exit nonzero.

Run one mode at a time. A nonzero exit is an expected falsification, never PASS.
"""
import sys
from new_controls import heis_mul, heis_inv, fold, I, rank, boundary_words

mode=sys.argv[1]
X,Y=(1,0,0),(0,1,0);Z=heis_inv(heis_mul(X,Y))
if mode=='reverse_order':
    assert fold([Z,Y,X],heis_mul,I)==I,'DELIBERATE_MUTANT: reversed killed word remains killed'
elif mode=='relative_conjugator':
    conj=heis_mul(heis_mul(Y,X),heis_inv(Y))
    assert fold([conj,Y,Z],heis_mul,I)==I,'DELIBERATE_MUTANT: independent whisker conjugation harmless'
elif mode=='planar_rotation':
    words,g,b=boundary_words([1,2,-1,-2])
    assert (g,b)==(0,3),'DELIBERATE_MUTANT: interlaced ribbon is planar pants'
elif mode=='independent_seams':
    assert rank([[1,1],[0,0]])==2,'DELIBERATE_MUTANT: duplicated seam classes independent'
elif mode=='proper_means_intransitive':
    rotations={(1,b) for b in range(5)}
    assert len({b for a,b in rotations})<5,'DELIBERATE_MUTANT: proper affine rotation subgroup intransitive'
elif mode=='nonperfect_factor':
    stabilizer={1,2,3,4}
    # Multiplicative F5* is the C4 abelianization. The stabilizer is its entire image.
    assert stabilizer=={1},'DELIBERATE_MUTANT: point stabilizer killed by nonzero cyclic character'
elif mode=='outer_essential_g2':
    assert 2-2>0,'DELIBERATE_MUTANT: genus-two outer boundary has positive-genus exterior'
else:raise ValueError('Unknown mutant')
