# Independent audit of the scalar-transfer bridge, revision 2

Problem 30000576 / OWR-1323-013, rank 658. Audited 4 October 2026.

## Verdict

**PASS: the bridge removes the exact complex-scalar HOLD.** The revision supports `already_solved` as a **prior-literature resolution with an independently audited scalar bridge**. Both original questions have negative answers, conditional only on the explicitly cited published existence result being used as a literature input in the ordinary way.

The proof of the real-to-complex theorem in PROOF.md §§1–5 is complete. No mathematical correction is required. This is not a new counterexample or a priority claim. The construction and full proof in Bayart–Bermúdez (2009) remain uninspected and have not been independently audited. Direct confirmation of that example's scalar field also remains unavailable; it is now unnecessary because the valid bridge covers the real case and the complex case applies directly.

The original attribution-only packet and original HOLD audit remain unchanged. That HOLD was warranted for the original packet; the present verdict applies to the separately frozen revision 2.

## Exact original target and published input

The [original problem](https://doi.org/10.4171/OWR/2006/37), printed p. 2272, §5, was independently inspected in extracted text and on the page image. It concerns bounded linear operators forming a strongly continuous semigroup indexed by real nonnegative time on a separable complex Banach space. Its chaos definition is a dense orbit plus dense semigroup-periodic vectors. It asks whether every positive-time operator must be chaotic and whether at least one must be. No time-zero obstruction or weaker chaos definition is relevant.

The [publisher's 2009 abstract](https://academic.oup.com/blms/article/41/5/823/299533) was independently retrieved and confirms the existence attribution, without enough hypotheses to establish the target alone. [Mangino–Peris (2011)](https://www.impan.pl/shop/en/publication/transaction/download/product/90233), introductory definitions on pp. 227–228 and the paragraph before Proposition 2.6 on p. 235, was rechecked in context. It places the no-chaotic-time example in the separable-Banach, bounded-linear C0 framework with the relevant definition. Its separate mixed-time example is not substituted for the stronger assertion. The attribution and bibliography refer to Bayart and Bermúdez, *Semigroups of chaotic operators*, BLMS 41 (2009), 823–830, DOI 10.1112/blms/bdp055. This remains a published input rather than an inspected construction.

[Kalmes (2006)](https://d-nb.info/983023670/34) explicitly permits real and complex spaces on printed p. 5. Theorems 2.7 and 4.5 on pp. 16 and 24 support the compact-orbit/weak-mixing mechanism; those locations and the rendered p. 24 were inspected. The thesis is corroboration, not a necessary missing lemma: the revision supplies the needed argument itself. Its historical statement that the individual-chaos problem was open predates the 2009 result and is not current-status evidence.

## Independent proof audit

### 1. Common real periods: valid synchronization, not an LCM assumption

For a finite list of nonempty open sets, hypercyclicity supplies finitely many time translates of one vector h inside them. Each fixed S_r is continuous, so the intersection of their inverse images is an open neighborhood of h. It therefore contains a periodic vector p. If S_a p=p, then commutation gives S_a S_r p=S_r p for each chosen r. Thus the resulting tuple belongs to the chosen rectangle and has the very same positive real period a.

Rectangles form a base for the finite product topology. This proves density of periodic vectors of the diagonal semigroup. Neither injectivity nor surjectivity of S_r is needed. The proof does not assert that arbitrary independently chosen periodic coordinates share a real period, or that P is a linear subspace. That distinction directly repairs the original HOLD.

### 2. Scaled return sequence: all required quantifiers and boundedness are present

For nonzero X a hypercyclic vector h is nonzero. Density of its orbit gives, for each integer n≥1, a time t_n with ||S_(t_n)h−nh||<1. Hence S_(t_n)h/n→h. This uses fixed-radius orbit approximation to points whose norms diverge; it does not require the orbit to visit a prescribed time interval or a monotone sequence of times.

For a fixed z=S_r h, linearity and commutation give the explicit estimate

    ||S_(t_n)z/n−z|| ≤ ||S_r||/n.

Every fixed S_r is bounded. No uniform bound on all S_r, no uniform convergence on Z, and no extension of pointwise convergence from Z to all of X is used. Since only finitely many fixed z-coordinates are later selected, the coordinate limits imply the product limit.

The proof's positive-time check is sufficient. In fact a stronger fact follows: t_n→∞. For any M, continuity of t↦S_t h on [0,M] bounds its norm by C_M; the return estimate would force n||h||−1<C_M whenever t_n≤M. Thus only finitely many such indices exist. This strengthening is explanatory, not a needed repair.

### 3. Compactness and diagonal transitivity: correct order of choices

Density of P implies density of P^m, so an arbitrary nonempty open U in X^m contains a tuple y of individually periodic points. A coordinate of period a has its entire positive orbit in the compact continuous image of [0,a], because S_(ka+s)y=S_s y. The finite product of these coordinate orbit sets is compact even when their real periods are incommensurate. Thus the tuple sequence S^(m)_(t_n)y has a convergent subsequence with strictly increasing indices n_k→∞ and some limit b.

Only after this subsequence and b have been selected is z chosen in dense Z^m∩(V−b). The convergence for every fixed z along the original sequence survives that subsequence. Then

    u_k=y+z/n_k→y,
    S^(m)_(t_(n_k))u_k=S^(m)_(t_(n_k))y+S^(m)_(t_(n_k))z/n_k→b+z.

Openness of U and V gives a sufficiently large k landing from U to V at positive time. The construction does not assume that S_(t_n)(u_k−y) tends to zero; it deliberately tends to z. It does not replace relative compactness by boundedness. It proves every finite diagonal power transitive, not merely coordinatewise transitive with unrelated times.

### 4. Baire step: valid on the stated space

A finite product of a separable Banach space is a complete separable metric space and has a countable base. Each G_l is open since every time map is continuous. An arbitrary, possibly uncountable, union of open inverse images is still open. Transitivity makes G_l dense. The Baire intersection is nonempty (indeed dense), and any point in it has an orbit meeting every base element. This establishes a dense orbit of the diagonal action. Section 1 supplies its dense periodic set. No theorem asserting weak mixing from mere hypercyclicity is being assumed.

### 5. Complex Banach structure and continuity: valid

The displayed circle-supremum norm is finite by the sum bound, definite by the angles 0 and π/2, and subadditive by the real triangle inequality. Multiplication by a+ib with modulus r shifts the angle and multiplies the expression by r; the supremum over a full circle is unchanged by this shift. The zero scalar is immediate. Thus the norm is genuinely complex-homogeneous. The maximum/product lower bound and sum upper bound prove equivalence with a complete separable product norm.

Complex linearity and the semigroup law follow coordinatewise. Taking the supremum in the real operator bound yields ||S_t^C||≤||S_t||, and the stated sum estimate proves strong continuity at every time (one-sided at zero). The real coordinate identification is a homeomorphism of dynamical systems, which is all that transfer of dense orbits and periodic sets needs. The diagonal square therefore makes the complexification chaotic.

### 6. Fixed-time nonchaos: preserved for either possible failure of chaos

For each fixed positive t, real-part projection R is continuous, onto, and intertwines S_t^C and S_t, hence also all their integer powers. A dense discrete orbit upstairs projects to a dense orbit downstairs: the inverse image of every nonempty open set downstairs is nonempty and open. The same argument applies to a dense periodic set, whose members project to periodic points. Therefore chaos upstairs implies chaos downstairs. Contraposition preserves nonchaos without assuming in advance whether hypercyclicity or periodic density fails.

The equivalent fixed-time periodic-set identity is valid: positive integer periods of two coordinates synchronize by LCM. It is correctly restricted to a fixed operator. The zero-space exception is harmless under the explicitly stated dense-orbit/dense-periodic definition and cannot supply the no-chaotic-time counterexample.

### 7. Application and quantifiers: exact target reached

If the attributed example is complex, it already has the target field. If it is real, the audited theorem produces a separable complex Banach C0 example, and the contrapositive factor argument rules out chaos of its operator at every positive real t. The same single example thus refutes both the every-time and the some-time claims. No particular construction details, special form of the Banach space, extra frequent-hypercyclicity criterion, or mixed-time substitute are needed.

## Replay, adversarial controls and limits

The supplied freeze hash is

    0f77ea2dc8653f7680a5709778158b5a4df71811ae9d7a30d5adaefeeb8b2c80

All 14 revision-2 files, including its manifest, and all 18 bound historical files were independently rehashed. All 15 supplied packet checks and all 8,369 supplied exact controls were actually rerun; their outputs match the frozen result files.

The new independent verifier adds exact controls for a non-Hilbert l1^3 complexification norm, bounded operator extensions (including a zero operator), irrational real-period incompatibility versus integer LCM, periodic-orbit subsequences, amplification of vanishing perturbations, the failure of boundedness to imply precompactness, and the failure of dense-set pointwise convergence to imply global convergence. It also exhaustively checks finite onto semiconjugacies and includes a non-surjective countercontrol, positive-time quantifier controls, and a proof-byte mutation check. These are sanity and adversarial controls, not finite-dimensional hypercyclic examples or a machine verification of the Banach-space proof. The infinite-dimensional arguments above were separately inspected.

The irrational-period control represents time as a+b√2: the first rotating plane is fixed exactly when b=0 and a is integral; the plane of period √2 is fixed exactly when a=0 and b is integral. Uniqueness of these coefficients proves the common period is zero. Finite samples illustrate this analytic obstruction without purporting to prove irrationality by exhaustive search. The c00 convergence countercontrol similarly has its exact l2 witness x_n=1/n, with square summability bounded by the telescoping series 1/[n(n−1)].

`AUDITED_INPUTS.json` binds both generations of inputs. `AUDIT_BINDING.json` binds the authored audit, source metadata and verification output. A test result generated before binding honestly records that its own manifest was not yet checked; rerun `verify_audit.py` without `--bootstrap` to check the complete final binding. No third-party text, source PDFs, corpus contents or private coordination files are included. No frozen files were edited, and no remote writes, uploads, source access escalation, author outreach or publication actions were performed.

## Permitted disposition

The parent may record **prior-literature `already_solved`**, answers **no / no**, attributed to Bayart–Bermúdez (2009), with the exact-scalar HOLD removed by this audited bridge. Preserve the disclosure that the published 2009 construction is an uninspected input. Do not relabel this as a newly discovered counterexample, an independent reconstruction of that construction, or a full proof audit of the 2009 paper.
