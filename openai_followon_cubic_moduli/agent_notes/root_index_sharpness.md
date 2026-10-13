# Root check: high Cartier index and sharpness

This is a continuation research artifact, not a promoted novelty claim. The initial reviewed manuscript and PDF are unchanged.

## Exact candidate and mechanism

Let X be an n-dimensional klt projective Fano with a weak KE metric and actual Cartier equality -K_X = rL, where L is ample Cartier and r is a positive integer. If r > n/2+1, the DGP quasi-etale stable-factor decomposition cannot contain two positive-dimensional factors. For each factor Z of dimension d, restriction to a fiber over a regular complementary point gives -K_Z = rL_Z with L_Z ample Cartier. Kawamata-Viehweg vanishing for -jL_Z, 1 <= j <= r-1, and the absence of antiample sections imply chi(Z,-jL_Z)=0. The degree-d Hilbert polynomial has r-1 distinct roots, so d >= r-1. Two factors imply n >= 2(r-1), contradiction.

A one-factor stable cover also forces stability downstairs: the reflexive pullback of a proper equal-slope summand of the polystable T_X is a proper equal-slope subsheaf of T_Y. Slopes are compared using the pulled-back anticanonical polarization. This needs the finite quasi-etale pullback argument, not an assumption that an incomplete regular locus admits complete de Rham splitting.

## Local positive-Ricci simplification

Suppose J' is a second parallel orthogonal complex structure on the regular locus. The real 2-form g(J'.,.) is parallel. Its (2,0) component alpha relative to J is parallel because J is parallel. On a positive KE manifold with Ric = lambda g, the contraction of Chern curvature on holomorphic p-forms is -p lambda Id, up to the common sign convention. Thus a parallel holomorphic 2-form obeys 0=-2 lambda alpha and vanishes pointwise. No global integration, completeness or extension of a differential form is needed. The remaining form has type (1,1), equivalent to JJ'=J'J. Therefore J' is a parallel holomorphic endomorphism of T_X on the regular locus. Reflexive extension and stable simplicity give J' restricted to T^(1,0) = c Id; c^2=-1 implies J'=J or -J.

This verifies the algebra of the mechanism. Exact singular metric/algebraic regularity and map/polarization extension are delegated for independent primary-source checking. A general weak KE metric assertion must specify the regularity-identification hypothesis. For the actual noncollapsed cubic GH limits, Donaldson-Sun provides it.

## Sharpness of the strict numerical threshold

For each integer r>=2, take d=r-1 and X=P^d x P^d with L=O(1,1). Then n=2d=2(r-1) and -K_X=rL, exactly at r=n/2+1. The product of equal Fubini-Study KE metrics has the same positive Einstein constant on both factors. Conjugation on the first factor and the identity on the second is a real metric isometry, but its differential reverses J on the first nonzero tangent summand and preserves J on the second. It is neither holomorphic nor antiholomorphic. This falsifies extension of the proposed uniform index criterion to equality. It does not imply failure for every cubic fourfold.

The exact Hilbert polynomial is binom(t+d,d)^2 and L^(2d)=binom(2d,d). At d=2 the degree is6. The quotient of P2 x P2 by factor exchange has degree3 with its descended O(1,1), so it is a plausible cubic-fourfold borderline example. Mixed conjugation does not normalize the factor-exchange action: if tau exchanges factors and c conjugates a factor, (c,id) tau (c,id) = (c,c) tau. Consequently it does not descend, and supplies no cubic counterexample.

## Evidence and remaining gate

DGP Theorem A supplies the essential splitting/stability input (arXiv:2008.05352v1, published 2024 DOI10.5802/crmath.612); the Hilbert-root argument and product counterexample are elementary deductions written above. Independent source and metric audits are ongoing. Novelty is unestablished; current literature contains splitting and the old quotient-by-conjugation convention. No new-solution publication follows from this note.

Checked UTC: 2026-10-07T05:43:14.938150+00:00
