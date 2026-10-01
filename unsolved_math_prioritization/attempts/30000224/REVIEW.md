# Independent review of the Macaulay quartic partial results

**Verdict: PASS for the stated restricted obstructions, with the original question unresolved.** No substantive mathematical gap was found in the frozen note. The review supports three exclusions: binomial ideals in the displayed coordinates; arbitrary ideals containing the reduced quadric equation; and homogeneous ideals of generic multiplicity one or two. It does not support an exclusion of every Cohen–Macaulay thickening.

**Target:** 30000224 / OWR-824-008.  
**Reviewed document:** `PARTIAL_RESULTS.md`.  
**Frozen commit:** `31000d83ecd8fc048c80ed031b8de7741c4c2025`.  
**SHA-256:** `8d6995c10f48640f33afc5a437766eaccead99808e7b3c7f770bb52a8e900444`.  
**Date:** 30 September 2026. **Reviewer model:** gpt-6-astra, xhigh.

This is an independent AI mathematical review, not human peer review or formal verification. No novelty or priority determination is made.

## Exact source scope

The question in [Singh's Oberwolfach contribution](https://ems.press/content/serial-article-files/45993?nt=1), printed p. 1116, has the characteristic-zero parametrization used in the note and asks for an arbitrary ideal with the stated radical. [Singh–Walther, Example 3.5 and Question 3.6](https://arxiv.org/pdf/math/0701524), repeats that scope. Neither formulation restricts the proposed thickening to be homogeneous. The note correctly preserves this distinction throughout and does not turn the homogeneous multiplicity result into a general exclusion.

The geometry may be checked after passing to an algebraic closure. The toric prime remains prime by its monomial parametrization, and the two inclusions between the proposed ideal, the prime, and a power of the prime preserve the radical after extension. Cohen–Macaulayness is preserved in this characteristic-zero field-extension setting. No descent argument is used to create an ideal.

## Deficiency and the binomial exclusion

The monomial argument identifies exactly one hole: the missing degree-one monomial \(u=s^2t^2\). Once all exponents in degree two are present, adding the available exponents 0, 1, 3, 4 gives every exponent in the next degree. Thus \(B/A=K(-1)\), not an unproved stabilization inferred only from the finite computation.

The four residue classes of exponents modulo four give a genuine free basis \(1,x,u,y\) over \(K[w,z]\). The two-dimensional Cohen–Macaulayness of \(B\), together with the finite-length quotient, yields \(H^1_{\mathfrak m}(A)=K(-1)\). All listed monomial identities are correct. The missing element with square and cube in \(A\) also establishes the failure of seminormality.

For the binomial proposition, a Cohen–Macaulay quotient with this unique minimal prime has no embedded associated primes, hence its defining ideal is primary for that prime. The product of the four variables is outside the prime, so Laurent localization contracts the proposed ideal back to itself. Each binomial in the prime has opposite coefficients because the point \((1,1,1,1)\) lies on the parametrized variety. There are no monomials in the prime.

The Laurent quotient is therefore the group algebra of a finitely generated abelian group. Its finite factor has reduced group algebra in characteristic zero, including when the base field is not algebraically closed; the algebra is a product of finite separable extensions. The free factor only adjoins Laurent variables. Reducedness forces equality of the localized ideal and its radical, and contraction gives the original toric prime, contradicting the deficiency calculation. This agrees with [Eisenbud–Sturmfels, Section 2](https://arxiv.org/pdf/alg-geom/9401001). The result correctly does not exclude non-binomial polynomial powers or non-binomial determinantal constructions.

## The quadric-contained case

The Segre description and divisor class are correct. The parametrization is \(([s^3:t^3],[s:t])\), and the second projection identifies the curve with \(\mathbb P^1\). Its divisor class on the smooth quadric is \((1,3)\).

The main point of this exclusion is that homogeneity is deduced, rather than assumed. Let \(S=R/(wz-xy)\) and let \(J\) be the image of a proposed ideal. The quadric cone is a normal Cohen–Macaulay domain. At a prime containing its height-one prime \(P\), the quotient has dimension one less than the ambient localization. Cohen–Macaulayness of the quotient and the depth lemma make \(J\) maximal Cohen–Macaulay there. At the other primes, \(J=S\). Thus \(J\) is rank-one, torsion-free, and satisfies S2, so it is reflexive.

The height-one localizations of a reflexive ideal determine it inside the fraction field. The only nonunit localization occurs at \(P\), where the ambient ring is a DVR and \(J_P=P^rS_P\). Therefore \(J=P^{(r)}\). Scaling invariance over an infinite field does imply that this symbolic power is homogeneous: for any polynomial, its finitely many homogeneous components can be recovered by a Vandermonde combination of distinct scalar dilations.

On the projective quadric the ideal sheaf is consequently \(\mathcal O_Q(-r,-3r)\). The stated exact sequence with the quadric ideal is valid, and the intermediate line-bundle cohomology on \(\mathbb P^3\) vanishes. Künneth then gives

\[
h^1(\mathcal I_{rC}(r))=h^1(\mathcal O_Q(0,-2r))=2r-1.
\]

A homogeneous Cohen–Macaulay quotient of dimension two has a saturated ideal and vanishing deficiency module, so this is a contradiction. The proof allows the proposed ideal to be nonhomogeneous at the outset. It does not replace containment of the reduced equation by containment of a higher power; that boundary is essential and is stated correctly.

## Homogeneous generic double structures

Primaryness correctly lets the generic length-two calculation descend to \(\mathfrak a^2\subseteq\mathfrak b\): if an element of \(\mathfrak a^2\) belongs to the ideal after localization, multiplication by some element outside \(\mathfrak a\) puts it in the ideal globally, and primaryness then removes that multiplier.

The nilpotent layer is an \(\mathcal O_C\)-module of generic rank one. A torsion subsheaf would have zero-dimensional support inside \(\mathcal O_Y\), contrary to local Cohen–Macaulayness of the projective curve. Since \(C\) is smooth, this layer is a line bundle. The conormal surjection follows from the square-zero inclusion.

The Jacobian construction of the conormal kernel is justified by the two Euler sequences. The homogeneous Euler identity introduces the invertible scalar four, so the diagram gives the same kernel after rescaling. The Jacobian is surjective on every fiber, and the two displayed cubic columns form a full-rank kernel frame at every projective point. In particular, the splitting \(\mathcal O(-7)^2\) is established explicitly, rather than merely quoted. It also matches the quartic discussion on printed p. 463 of [Eisenbud–Van de Ven](https://eisenbud.github.io/papers/pdfs/1981-001.pdf).

A line-bundle quotient \(\mathcal O(e)\) of that conormal bundle requires \(e\ge-7\). At twist two, its first cohomology vanishes and the extension sequence gives

\[
h^0(\mathcal O_Y(2))=(e+9)+9=e+18\ge11.
\]

Arithmetic Cohen–Macaulayness would make restriction from the ten-dimensional space of ambient quadrics surjective. This is impossible. Generic multiplicity one is also excluded by primary contraction and the known failure of Cohen–Macaulayness of the reduced quotient.

No preservation of Cohen–Macaulayness under homogenization or degeneration has been assumed. The conclusion is correctly restricted to homogeneous ideals. In particular it leaves nonhomogeneous generic double structures outside this particular exclusion.

## Linkage and the failed residual-intersection shortcut

The Segre factorization is correct. I independently checked the stronger exact ideal equality

\[
(w,x)\cap(y,z)\cap\mathfrak a
=(wz-xy,\;wy^2-x^2z).
\]

Since \(wy\notin\mathfrak a\), taking the colon by \((w,x)\cap(y,z)\) recovers \(\mathfrak a\). This verifies the linkage description, consistent with [Boix–Eghbali, Remark 5.7](https://arxiv.org/pdf/1806.04405). No general preservation of set-theoretic Cohen–Macaulayness under linkage is inferred.

The degree-four Koszul cycle is a cycle and is not a boundary. The coefficient argument is valid because the degree-four part of the boundary module is spanned by constant combinations of the six displayed boundaries. The four annihilation identities are correct and show that the resulting nonzero homology class has maximal-ideal annihilator after localization.

The depth chain is valid at the homogeneous maximal ideal:

\[
\operatorname{depth}(R/I)=1,\quad
\operatorname{depth}I=2,\quad
\operatorname{depth}Z_1=3,\quad
\operatorname{depth}B_1=1,\quad
\operatorname{depth}Z_2=2.
\]

The nonzero socle gives depth zero for \(H_1\); the equalities then follow from the depth lemma in cases of unequal adjacent depths. Auslander–Buchsbaum yields projective dimension two for \(Z_2\).

[Hassanzadeh, Theorem 1.2 and Corollary 3.19](https://arxiv.org/pdf/2409.05705), require precisely the numerical and homological conditions tested in the note. The first alternative fails because \(2<4\); the cycle bound at index two fails because \(2>1\); and sliding depth fails already at first homology. This blocks that application, without claiming that every possible linkage route is impossible.

The Du Bois and graded tests in [Ma–Schwede–Shimomoto, Proposition 4.9 and Corollary 4.10](https://arxiv.org/pdf/1605.02755), also have the scope stated in the note. Nonseminormality prevents the Du Bois hypothesis, and the exhibited local-cohomology defect is in degree one, outside the required nonpositive degrees. Failure of a sufficient obstruction is not evidence of existence.

## Reproducibility

The author's exact verifier was copied into an isolated replay directory and rerun without changes. All **135 assertions** passed, and its `verification.json` matched the supplied file byte-for-byte.

The independently written `independent_checks.py` uses SymPy exact arithmetic and passed six groups of checks:

- Recovering the toric ideal directly from elimination of the parametrization
- Computing the ideal intersection and verifying the linkage colon consequence
- Recovering the cubic conormal frame from a coefficient-matrix nullspace, with no syzygies of smaller degree and no common projective zero of its maximal minors
- Recomputing the Koszul boundary and augmented ranks, and checking all four variable multiples by independent linear algebra
- Checking the semigroup hole and the four residue classes for the free module basis
- Checking consistency of the elementary cohomology dimensions

Run `python independent_checks.py` from the review directory. Python 3 and SymPy 1.14.0 were used. The full output is in `independent_results.json`. These finite computations support the explicit certificates; the ring-theoretic and sheaf-theoretic arguments above provide the universal conclusions.

## Disposition and residual class

The partial package is suitable for a draft research pull request with status **partial/stalled**, not claimed solved. Any still-possible solution must be non-binomial in the stated coordinates, primary for the toric prime, and have the quadric equation nonzero but nilpotent in its quotient. In the homogeneous case its generic multiplicity must be at least three. The note has neither constructed such an ideal nor excluded the remaining class, especially the nonhomogeneous possibilities.

There are no required mathematical changes to the frozen note within this review's scope.
