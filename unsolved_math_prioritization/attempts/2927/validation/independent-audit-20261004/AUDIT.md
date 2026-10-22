# Independent audit of KP 4.51 partial results

## Verdict and scope

Audit completed on 2026-10-04 UTC against the frozen rank 596 / problem 2927 package. **PASS for the stated partial results and their limited status.** No blocking mathematical error was found in Proposition 4.1, its smooth definite corollary, or the displayed stabilization certificate. This is a mathematical review with supplementary exact computations, not a formal proof-assistant certification.

The full problem is **unsolved in this attempt, 5/5 approaches used**. The low-indefinite cases with minimum index one or two remain outside the proved general results. Kawauchi's published full-resolution claim remains **unverified**, neither accepted nor refuted by this audit. Nothing here permits an `already_solved`, `claimed_solved`, novelty, or full-resolution designation or a Findings-field change.

The frozen public manifest SHA-256 is:

    1bddbd487f555afa16feb2b822dc09ef819343f8ab908b21021fafb6de0561da

The public files and frozen gate were not edited. All audit outputs are separate. No remote writes, outside communications, additional proof-search approach, or helper delegation occurred. Source PDFs and source text remain private and are not copied into this audit deliverable.

## Proposition 4.1

The proposition assumes a nonsingular Hermitian matrix H over Z[x,x^-1], positive augmentation H(1), and standard positive coefficient lattices Q_p for arbitrarily large odd primes. Here nonsingular has its usual ring-theoretic meaning: the adjoint is an isomorphism, equivalently det H is a unit. It does not merely mean det H is a nonzero polynomial.

### The spectral bound is uniform in cover degree

The determinant is a Hermitian Laurent unit. The units are ±x^k, and invariance under x -> x^-1 forces k=0. Thus det H is ±1. Positive definiteness at x=1 selects +1. On the unit circle, substitution intertwines the Laurent involution with complex conjugation, so each H(z) is an ordinary Hermitian matrix. Its inertia cannot change on the connected circle without a zero eigenvalue. Its determinant never vanishes. Consequently every H(z) is positive definite.

The minimum eigenvalue is continuous in z; taking its minimum on the compact circle gives c>0. Crucially, c depends on H, not n. For v(x)=sum_j v_j x^j, the continuous and finite Fourier identities are

    B_infinity(v,v) = (1/2π) integral v(e^{iθ})* H(e^{iθ}) v(e^{iθ}) dθ,
    Q_n(v,v) = (1/n) sum_{z^n=1} v(z)* H(z) v(z).

The second identity uses the unique degree-below-n representative of v. The corresponding Parseval equalities yield exactly the two coefficient-norm lower bounds in the frozen proof. No limit of changing-dimensional matrices or exchange of an infinite series is being used.

For norm one, sum_j ||v_j||^2 <= 1/c. Integral coefficients imply that each nonzero scalar coefficient contributes at least one, so both the scalar count and the occupied-position count are bounded by K. A large coefficient cannot evade this bound. Choosing K before p is legitimate. The hypothesis of arbitrarily large standard prime covers supplies a p above the subsequent matrix-dependent threshold. Finite successful tests do not establish that hypothesis.

### Localization and unwrapping do not assume a short cyclic interval

The graph uses all occupied positions, joining positions of cyclic distance at most d even if the relevant coefficient of H happens to vanish. This can add unnecessary edges, but cannot remove any possible interaction. Therefore different graph components are Q_p-orthogonal. Each component vector is nonzero and has positive integral norm. Their norm sum is one, forcing a single component.

The proof does not assume that this connected component already lies in a short interval in the cyclic ordering. A tree lift assigns an integer coordinate to each vertex. The difference of any two lifted coordinates is the sum along their unique tree path, so has absolute value at most d(q-1). This proves the claimed diameter bound, rather than merely a bound from one chosen root.

Because p>2dK, an edge's short representative is unique. For a non-tree edge, the lifted difference and its short representative differ by a multiple of p with absolute value at most d(q-1)+d=dq<=dK<p. It must be zero. This checks cycle consistency, including an edge crossing the displayed residue cut.

The Laurent self-pairing has exponents in [-D-d,D+d]. As D+d=dK<p, its only exponent divisible by p is zero. Hence taking the coefficient of the identity after cyclic reduction gives the original constant coefficient. This is the precise no-aliasing requirement at this step; it is weaker than the later injectivity requirement, and the chosen threshold satisfies both. Distinct residues remain distinct during the lift. Translation into [0,D] changes the quotient vector only by its deck translate.

### Integral coefficient norm one implies Laurent norm one

B_infinity extends to a positive definite real bilinear pairing on the real vector space of finite coefficient sequences. Translation preserves this pairing's norm. A nonzero finite sequence cannot be proportional to its nontrivial translate: its extreme occupied exponent would change. Thus the two vectors are genuinely linearly independent, including the possibility of negative proportionality.

Strict Cauchy–Schwarz gives absolute pairing less than one for every nonzero translate. The pairings are integers, hence vanish. They are the nonconstant Laurent coefficients with an immaterial index reversal. The constant coefficient is one. This argument proves the identity h(v,v)=1, and does not infer it from pointwise complex norm one or from a finite selection of coefficients.

### The prime deck argument handles signs

A standard positive integral lattice of rank rp has exactly rp norm-one unoriented lines, with signed representatives forming its only norm-one vectors. Any integral isometry permutes these lines. Since T^p=1, line orbits have size 1 or p.

On a fixed line the eigenvalue is ±1; oddness of p excludes -1. A length-p signed cycle has zero trace regardless of signs on its arrows. Therefore trace T is the number of fixed lines. In the original free cyclic coefficient basis, T consists of r regular p-cycles, with trace zero. There are no fixed lines, so there are exactly r full orbits. This argument would need alteration for even or composite degrees; the proof correctly restricts to odd primes.

Distinct chosen orbits give Q_p(v_i,x^k v_j)=0 for every k. Those pairings recover every coefficient of the reduced Laurent cross-pairing. It is therefore zero in Z[x]/(x^p-1), not merely zero at augmentation. After individually normalizing the lifts, every cross-pairing has exponent support inside [-D-d,D+d]. Two integers in this interval differ by at most 2dK<p; none coincide modulo p. Cyclic reduction is injective on this support. Thus the unreduced cross-pairing is exactly zero.

### The columns form an integral Laurent basis

There are r columns, and their Gram matrix is I_r. The determinant equation is

    overline(det V) det H det V = 1.

Since det H=1, overline(det V) is a multiplicative inverse for det V in the original Laurent ring. The adjugate inverse therefore lies in that ring. This establishes surjectivity and an actual integral basis, not only independence, a finite-index sublattice, a rational basis, or a stable/Witt equivalence. No compactness or integrality gap remains in this step.

## Smooth definite corollary

The standard finite-free equivariant homology framework for closed oriented π1=Z manifolds is an imported topological input, explicitly acknowledged by the package. It is not proved by the finite checker. The general cover identification is also consistent with the chain-level universal-coefficient argument: Z[x]/(x^n-1) has a length-one free resolution over the Laurent ring, and H_1 of the universal cover vanishes. No extra H_1 Tor term contributes to H_2. Equivariant intersection reduces to the cyclic group ring, and taking its identity coefficient gives the ordinary form. This is the mechanism in FHMT07 Lemma 2.2; it is not a splitting-descent theorem.

For a finite cyclic cover Y, π1(Y)=Z, b1=b3=1, and χ=b2. Multiplicativity of Euler characteristic and signature gives the claimed b2 and signature scaling. A definite form therefore remains definite. Ordinary H2 is torsion-free here, consistent with Poincaré duality and the universal coefficient theorem since H1=Z.

The circle-surgery argument was checked independently:

- A generator of π1(Y) can be represented by a smooth embedded circle. Its oriented rank-three normal bundle over S1 is trivial.
- Removing this circle, or a small tubular neighborhood, leaves π1 unchanged. General position applies both to loops and to their two-dimensional homotopies since the circle has codimension three.
- Attaching D2×S2 kills the primitive generator, so the closed surgered manifold Y' is smooth and simply connected.
- Excision for (Y,Y0) gives H3=Z and H2=0. The map from H3(Y)=Z is intersection with the primitive circle and is an isomorphism. The exact sequence gives H2(Y0)≅H2(Y).
- Excision for (Y',Y0) gives H3=0 and H2=Z. The boundary map to H1(Y0)=Z is the primitive attaching circle, hence an isomorphism. The exact sequence gives H2(Y0)≅H2(Y').
- Representatives of two-dimensional classes and their intersection computations can be placed in the common interior Y0. Thus the isomorphisms preserve the integral pairing, not just its rank and signature.

Donaldson's definite diagonalization theorem for closed simply connected smooth four-manifolds now applies directly to Y'. No unmentioned non-simply-connected version is needed. The resulting standardness holds for all finite cyclic degrees, and therefore supplies the unbounded-prime hypothesis. Orientation reversal treats the negative definite case, and rank zero is separately harmless. No geometric finite-cover descent claim enters this corollary.

## Algebraic certificate and finite-cover controls

The original standard-library checker was copied to a separate replay directory before execution because it writes controls.json beside itself. Its generated JSON was byte-for-byte identical to the frozen JSON. The public files were not rerun in place or changed.

The new independent SymPy implementation does not import the frozen checker. It verifies:

1. det L=1, Hermitian symmetry, and A-B²/2=I/2.
2. det P=-1 and every Laurent coefficient of P* (L⊕[-1]) P = [1]⊕H⊕I2.
3. Every intermediate identity in the derivation of u,A,w,B,C,E, including the perpendicular projection and the equality of its five derived columns with the displayed P.
4. Cyclic matrices assembled by extracting coefficients from scalar pairings, separately from the frozen circulant assembler, for all degrees 1 through 12.
5. An exact Schur complement for each finite matrix proving positivity and determinant one; characteristic parity; w norms 4n; and c norms 12,8,4n-8 for n=1,n=2,n>=3 respectively.
6. The corresponding short-characteristic obstruction for every n>=3 tested, with n=1,2 functioning as negative controls for that test.
7. Asymmetric Laurent-shear controls at primes 3,5,7,11, including inverse, Gram reconstruction, deck isometry, deck order, and trace.
8. 114 connected support configurations across six admissible (p,d,K) tuples, testing lift diameter and consistency including wraparound.
9. Negative controls: replacing the involutive transpose with ordinary transpose fails; corrupting one displayed matrix coefficient fails.

All passed under SymPy 1.14.0. These tests supplement the analytic/combinatorial proof; they cannot validate an unbounded-prime hypothesis or the omitted geometric descent proof. The certificate really shows extension of L⊕[-1]. It says nothing by itself about smoothability of every stabilization or a cancellation theorem for all indefinite forms.

## Source and claim boundaries

The K3 statement and remarks on printed pages 230–231 were visually checked from the private rendered pages. The source question omits the word oriented, while its splitting remark explicitly uses the oriented setting. The package expressly adopts the ordinary involution and oriented interpretation and does not silently settle the twisted nonorientable variant.

The [HT97 primary manuscript](https://math.berkeley.edu/~teichner/Papers/form.pdf) was checked at Theorems 1 and 2. Its threshold is r-|s|>=6, which is exactly minimum index at least three. The [FHMT07 primary manuscript](https://math.berkeley.edu/~teichner/Papers/Nonsmooth.pdf) was checked at Theorems 1.2 and 1.5, Conjecture 1.3, and Lemma 2.2. It supports the nonsmoothability correction, the cover framework, and the limited use of the classical example. Neither source supplies the missing general low-index conclusion.

The private Kawauchi 2013 proof pages 4–9 and the 2014 author text were inspected. The 2013 descent claim and the 2014 full smooth conclusion genuinely match the intended topological target. The displayed final vanishing claim in Sublemma 2.3.1 was additionally visually checked on page 7. Reading that statement does not establish its validity. This audit does not reconstruct the cited exact-leaf machinery or certify the descent proof, and asserts no counterexample or false step. The [author bibliography](https://sites.google.com/view/kawauchiwriting), checked live on the audit date, lists the 2013 and 2014 papers without an attached correction notice. That is no substitute for checking their proofs.

The private census v1 contains the cited universal splitting assertion and Kawauchi references; v2 does not. The [arXiv version history](https://arxiv.org/abs/2412.04768v2) confirms the 13 May 2026 v2 date. The [journal article](https://link.springer.com/article/10.1007/s00454-026-00818-w), independently read live, is dated 25 February 2026 and omits the assertion and references. The removal's reason is not established. The package correctly avoids labeling it a retraction or disproof. K3 retaining the question is also not a mathematical refutation.

All private source-manifest hashes passed. The available pinned repository duplicate receipts were reviewed as provenance rather than rerun as a new remote audit. Their reported scope is properly limited; this audit does not certify the absence of unindexed or newly created duplicates. No novelty search or novelty certification was performed.

## Corrections and disposition

**Blocking corrections: none.** The definite-case proof, exact stabilization certificate, finite-cover obstruction, high-indefinite imported threshold, and unresolved-gap statement may stand as the audited partial package.

Two optional clarifications would improve a later revision but are not needed to make the frozen argument valid: explicitly define nonsingular as det H a Laurent unit at the proposition; and give the two normalized Fourier formulas displayed above. These are explanatory additions, not missing hypotheses or repairs. Any later revision must receive its own manifest; the current freeze must remain unchanged.

Retain the exact low-index/descent gap, the unverified-prior-claim hold, the five-turn budget, and the private-source publication boundary. This audit adds no sixth approach and authorizes no remote publication or queue mutation.
