# Euler index constraints, and their exact limit

Checkpoint 2026-10-24T20:23:42.513208+00:00. Derived filter, no novelty or solution claim. Bounded calculation100%; full21.128discovery estimate8%.

Write Q_T=P_T/Z(P_T), where P_T is the pure spherical Artin group. The reviewed CP3.1/Cor3.2 reduction makes the commensurability question equivalent for Q_F4 and Q_H4, each having a finite classifying complex. Brieskorn's Poincare formula and the exact profile computations give χ(Q_F4)=−240 and χ(Q_H4)=−5040.

## Index-rigidity lemma

For any group Q with finite K(Q,1) and χ(Q)≠0, isomorphic finite-index subgroups U,V have equal indices in Q. Indeed finite-sheeted CW covers give χ(U)=[Q:U]χ(Q) and χ(V)=[Q:V]χ(Q), whereas group isomorphism identifies their Euler characteristics. Thus every partial self-isomorphism in the abstract commensurator has index ratio1. In particular Q has no isomorphism onto a proper finite-index subgroup. This says nothing about infinite-index embeddings.

For a common subgroup of Q_F4 and Q_H4, with respective indices a,b, the same argument gives −240a=−5040b, hence a=21b. A hypothetical index-one H4 quotient model would therefore need index21 in Q_F4. All four129pairs give ratios21,105/32,96/5,462 (left index divided by right), reproduced in ../../21_129/root_review/profile_reproduction.json relative to the problems directory.

These rational constraints are arithmetically admissible: both Q groups surject onto F2 and have a subgroup of every positive index, by the reviewed subarrangement argument. This does not say the needed subgroups are isomorphic. Ordinary Euler characteristic alone cannot separate the pair: the free groups F241 and F5041 have Euler characteristics−240 and−5040 and a genuine index21 inclusion F5041≤F241, by Nielsen–Schreier.

## Why central products invalidate a naive whole-group index argument

For the split pure group P=Q×Z, let U≤P have finite index. Since the virtual center of these Q groups is trivial (CP's strong indecomposability inputs), Z(U)=U∩Z(P), and U/Z(U) identifies with its projection Ubar≤Q. Counting cosets in a central extension gives

[P:U]=[Q:Ubar]·[Z(P):U∩Z(P)].

An isomorphism U≅V preserves their centers and identifies Ubar,Vbar. The Q indices are equal in a single type by the lemma, but the two central indices need not be equal. Explicitly Q×rZ≅Q×sZ for every positive r,s, with indices r,s in P. Thus P is not index-rigid, and all positive rational self-commensurator index ratios occur in P. One must quotient the intrinsic center before invoking the nonzero Euler argument.

For two types the relation a=21b governs only the centerless quotient indices; central cyclic indices can be independently adjusted. The pure groups themselves have Euler characteristic zero and supply no absolute Euler equality to close the question.

## Remaining gap

One needs an actual isomorphism at admissible indices or an additional rigorously virtual obstruction. Self-index rigidity and ratio21 do not provide either. No assumption of characteristic parabolics, equal indices, algebraic cover realization, or whole-group profinite equivalence has been inserted.
