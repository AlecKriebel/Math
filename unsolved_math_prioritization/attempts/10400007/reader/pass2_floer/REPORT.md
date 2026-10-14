# Small Markov-pair test for divisor-weight Floer repairs

## Result

For the actual two-variable complex of Anghel–Juhász, a coefficient-only repair is sharply constrained. A small Markov-equivalent pair of unknot presentations already forces both divisor-weight variables to become units. The accepted PASS1 calculation then removes every weight and returns ordinary knot Floer homology.

This is a bounded statement about base changes of this specified complex. It does not exclude other Floer complexes, categorical correspondences, genuine geometric vacuum/sewing constructions, or the accepted conformal-block realization. No categorification condition is imposed on Roberts's original problem.

## 1. Specified proposal

Let k=F2 and R=k[U,V]. Use qCFB_plus(beta) of [Anghel–Juhász, *Quantum braid Floer homology*, arXiv:2601.08805v4](https://arxiv.org/pdf/2601.08805v4), Definition 8.26. These are finite free R-complexes. Their differential is

    d(x) = sum_y count(x,y) U^(B(x)-B(y)) V^(C(x)-C(y)) y.

The variables record divisor/domain quantities, not ordinary noninvertible monodromies. A genuine rank-one local system on the punctured-disc configuration space still has the invertible monodromies given in Definition 2.1. Thus a nonunit Rees specialization is a divisor-relative chain proposal; it is not itself a rank-one local system with noninvertible holonomy.

Test the proposal

    D_A(beta)=qCFB_plus(beta) tensor_R^L A

for a nonzero commutative unital R-algebra A. Can this become a Markov-invariant chain object while keeping U or V noninvertible?

## 2. Certified diagrams, not ranks guessed from Euler characteristics

Take beta1=sigma1 in B2 and the two-twist braid beta2 in B3 obtained by applying the positive first and second elementary actions in that order. Depending on left/right action notation, its word is written sigma1 sigma2 or sigma2 sigma1. The two words are conjugate; beta2 is therefore a positive stabilization of beta1, possibly followed by conjugation. Both closures are the unknot. The theorem only requires invariance under Markov equivalence and does not depend on selecting a multiplication convention.

The accompanying exact rational program constructs actual representatives of the source punctured-disc diagrams. All geometric predicates use fractions.Fraction. The initial lower semicircular arcs are replaced by lower rectangular U arcs, and the upper semicircle neighborhoods by narrow upper-U neighborhoods. A radial ambient isotopy converts these systems to those in source equation (1.1), preserving punctures and nesting data. The neighborhood width is 1/40. The q punctures sit immediately outside the corresponding lower right arcs and outside the upper-U neighborhoods, as in Definition 1.8.

Each elementary half twist is supported in the polygonal disc of radius 7/5 about the midpoint of the adjacent negative-axis punctures. It contains precisely those two punctures, stays in x<0, and misses all q and w punctures. Its inner polygon has radius 11/20 and rotates through a half turn; sixteen annuli interpolate to the identity on the outer boundary. Thirty-two rational circle directions triangulate the annuli. Every domain and target triangle has strictly positive oriented area, checked exactly. The fixed simple boundary and positive local degrees prove that the PL map is a homeomorphism. Its half-twist class follows by interpolating the angular maps on the annuli. Smoothing away from the finitely many transverse crossings produces a permitted smooth representative without changing any count.

The intersections are transverse in segment interiors. Their matrices, with rows indexed by transformed arcs and columns by circles, are

    beta1: [3]
    beta2: [1 2; 1 3].

Their permanents are 3 and 5. The inverse of the first PL half twist gives only one intersection. This calibrates the Artin sign: it cannot be the source's positive sigma1, whose Euler polynomial has three nonzero monomials. Thus the three-intersection representative is the positive action under the source conventions.

For additional verification, the code computes A from signed winding about z and w, Q from q-winding and the discriminant exchange exponent, and the Euler sign from the oriented local intersections and the permutation sign. The right anchor path must detour once around q_i; using the arc itself would incorrectly omit the canonical-generator correction. The code implements this detour and obtains exactly the source polynomials of Section 9.2 after its e=-d conversion.

The resulting data (A,Q,S), with S the set of canonical coordinates, are:

    beta1:
      (0,1,empty), (1,1,empty), (1,2,{1}).
    beta2:
      (0,1,empty), (1,1,empty), (1,3,{1}),
      (2,3,{1}), (2,4,{1,2}).

The Euler signs in these orders are respectively (+,-,+) and (+,-,+,-,+). Each listed (A,Q) occurs exactly once. These independently calculated coefficients match

    Omega_beta1^q = d - xd + xd^2,
    Omega_beta2^q = d - xd + xd^3 - x^2 d^3 + x^2 d^4.

### Consequence for the quantum differential

The quantum differential preserves (A,Q). Therefore it is zero on both of these diagrams, and

    dim qHFB(beta1)=3,    dim qHFB(beta2)=5.

This conclusion uses actual chain-generator counts and the gradings. It is not inferred from an Euler polynomial alone. Regrading by J=A-Q and parity M+Q retains the zero differential and the different total dimensions. Hence the Jones-regraded quantum complexes are not quasi-isomorphic, even after forgetting all gradings. Their Jones super Euler polynomials nevertheless both equal 1.

## 3. Forced divisor-weight differentials

The full hat knot Floer homology of the unknot has one generator in A=0 and none in other Alexander degrees. Both diagrams have one generator in A=0 and precisely two generators in each other occupied A degree. Since the ordinary knot Floer differential preserves A, each such two-generator block must have a nonzero differential. Source Proposition 8.9 says W cannot decrease along a contributing positive domain, fixing its direction in these examples. The exponents are consequently determined without separately enumerating holomorphic discs.

Recall

    W=sum_(i in S)(3(n-i)+1),
    R0=sum_(i in S)(n-i),
    B=Q-W+R0,    C=R0-W.

For beta1 the arrow runs from (A,Q,S)=(1,1,empty) to (1,2,{1}); its exponents are (0,1). Thus it is multiplication by V.

For beta2:

- The A=1 arrow runs from (1,1,empty) to (1,3,{1}), with exponents (1,3), hence multiplication by UV^3.
- The A=2 arrow runs from (2,3,{1}) to (2,4,{1,2}), with exponents (0,1), hence multiplication by V.

Every disc between a given pair has these same exponents. Since the coefficient of the corresponding ordinary differential is 1 in F2, the weighted coefficient is exactly the displayed monomial. No other arrows are possible because all other A blocks are disjoint.

Thus, as ungraded finite free differential modules, the complexes consist of one free zero-differential generator and the blocks

    beta1:  R --V--> R,
    beta2:  R --V--> R  and  R --UV^3--> R.

Homological shifts need not be suppressed when writing the actual complexes; the rank argument below is independent of those shifts.

## 4. The coefficient-only obstruction

### Theorem

Let A be a nonzero commutative unital F2[U,V]-algebra, and let u,v be the images of U,V. If D_A(beta1) and D_A(beta2) are quasi-isomorphic, then u and v are units in A.

### Proof

A quasi-isomorphism in the derived category remains an isomorphism after derived base change to any residue field kappa(m). Since the original complexes are finite free over R, the resulting residue-field complexes are the termwise specializations just computed. Their homology dimensions are:

    v=0:                 3 and 5;
    v nonzero, u=0:      1 and 3;
    u and v nonzero:     1 and 1.

Therefore neither u nor v can vanish in any residue field of A. A nonunit in a nonzero commutative unital ring lies in a maximal ideal, so u and v must both be units. This also covers nonflat quotients: the derived functor and perfect original complexes make the residue-field test legitimate.

### Consequence

For every such candidate base change that repairs even this one Markov pair, the PASS1 gauge substitution

    e_x=u^(-B(x))v^(-C(x))x

removes all weights for every braid. The complex becomes ordinary hat knot Floer tensored with A; its displayed Jones degree becomes Alexander after the gauge change. Thus coefficient-only base change cannot repair Markov invariance while retaining the nonunit divisor-weight refinement.

This includes the tempting one-variable boundary proposals U=0,V invertible and V=0,U invertible, which fail already on the tested pair. The homogeneous relation UV=1 avoids this failure precisely by forcing both weights invertible and therefore collapses by the same gauge computation.

## 5. What remains outside the theorem

A repair may change the chain theory rather than base-change its ring: new objects, morphisms, relative support conditions, sheaf-theoretic nearby cycles, or additional divisor data could alter the stabilization defect. None of those is ruled out. They would require explicit geometric stabilization and conjugation maps, coefficient compatibility, and the appropriate move relations. The current computation supplies an exact defect that such maps must address; it does not supply those maps.

For example, a proposal to kill the cone of multiplication UV^3 in a tensor-compatible category makes that scalar action invertible. Because U and V commute, this also makes both actions invertible on the retained objects. Such a proposal must explain how it avoids merely reproducing the gauge-localized theory. This observation concerns that specific cone-killing proposal, not arbitrary Verdier quotients.

The original question may also be approached without any categorification. The direct geometric conformal-block route is unaffected by this obstruction. No source-level resolution or impossibility conclusion is claimed from the Floer calculation.

## 6. Verification limits

The program verifies rational planar geometry, signed intersections, local-system exponents, and the finite algebra. The deduction of full Floer arrows additionally uses the source's same-braid invariance, grading comparison, and positivity results, together with ordinary unknot knot Floer homology. Those analytical theorems have not been reproved here. The source PDFs remain private; the deliverable contains only authored analysis, calculations, and public citations.
