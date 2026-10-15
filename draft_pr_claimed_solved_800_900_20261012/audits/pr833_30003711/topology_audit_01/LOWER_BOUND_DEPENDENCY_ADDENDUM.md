# Late lower-bound dependency challenge

Timestamp: 2026-10-15 UTC. This addendum was written after the independent upper-bound reconstruction and main report, upon a new concern communicated within the authorized audit team. It is not a completed independent lower-bound audit and does not assume that the inaccessible 2025 journal text has the same argument as the 2023 preprint.

The upper-bound proof uses no cohomology calculation from Chen–Wan §4. Its orbit sections, dimension bound, colored domains, and join section remain valid conditional only on the group/spectral input. The **equality** claim needs the separate external lower bound, so a serious defect there would block promoting g=8 while leaving g<=8 intact.

There is a concrete internal consistency test for the inspected v2 Proposition 4.2(1). Write Q=PU3/K, c:Q->BK for its principal-cover classifying map, and work over F3. The relevant auxiliary statements to check are:

1. Q is a closed oriented real 8-manifold. This follows directly from the connected compact Lie group PU3 and finite right translations; translations preserve orientation.
2. c*:H^1(BK;F3)->H^1(Q;F3) is an isomorphism. This follows if the preimage of K in SU3 is the order-27 Heisenberg group with center the kernel C3 and abelianization K. This is the exact group input the lower-bound family must certify.
3. c*(y y')=0 for degree-one generators y,y' of H*(BK;F3). One way to certify it is the nontrivial central extension class in H^2(BK;F3): its inflation along its total group vanishes. Another is the preprint's own c1=y y' identification for the preimage of K in U3, since the associated U3 bundle becomes trivial on Q. These identifications are meaningful hypotheses to verify, not assumptions supplied by the upper-bound argument.

If (2) and (3) hold, the rest is a short decisive deduction. Since

    H*(BK;F3)=F3[x,x'] tensor exterior(y,y'),
    deg x=deg x'=2, deg y=deg y'=1,

any degree-7 class a is yP(x,x')+y'Q(x,x') with P,Q of polynomial degree 3. For every degree-one class b on BK, ab is a multiple of y y', since y^2=(y')^2=0 in odd characteristic. Thus c*(a)c*(b)=0. By (2), this pairs c*(a) trivially with every element of H^1(Q;F3). Mod-3 Poincare duality on the oriented 8-manifold Q makes the H^7 by H^1 pairing nondegenerate. Therefore c*(a)=0 for every a in H^7(BK;F3), contradicting the nonzero-map assertion in v2 Proposition 4.2(1).

This conditional calculation is independent of Leary's detailed presentation and isolates two small auxiliary facts for the lower-bound adversary to settle. In particular “the theorem statement was retrieved” cannot be used as a response to it. It does **not** prove that no other lower-bound mechanism could establish genus>=8.

The original independent reconstruction remains preserved as a timestamped record of the pre-challenge state. DECISION.json and TOPOLOGY_AUDIT.md now distinguish cleared upper-bound topology from unresolved equality. No changes to the upper-bound mathematics are indicated by this challenge.
