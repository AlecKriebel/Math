# Independent adversarial review: KP-1.85 / 2744

**Verdict: PASS for the unresolved source-and-obstruction package. The full problem remains unsolved in this attempt.** No mandatory mathematical correction was found. This verdict does not certify a universal compact-real arc theorem or a new knot counterexample.

- Review date: 30 September 2026
- Reviewer: independent gpt-6-astra worker, xhigh
- Frozen artifact: `OBSTRUCTION.md`
- Reviewed SHA-256: `99a09c92911e10ee1cba5de34f4ab78274cb8e211fa0f1456ed80b640819f872`
- Source artifact was not edited. A separate snapshot was checked byte-for-byte.

## 1. Exact question and source scope

The full K3 source, Problem 1.85, printed pp. 76–77, asks for an arc on the particular PSL(2,C) component containing the discrete-faithful character of a hyperbolic knot in S3. Compact characters on other components, a conjugation orbit, and an isolated compact character do not suffice. Fixing the orientation clarifies which complete holonomy is meant; complex conjugation preserves the compact real form, so the existence assertion is unaffected by reversing that choice. The artifact handles the affine/GIT character quotient correctly at compact characters.

Source: [K3 book, Problem 1.85](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf). The book and source PDFs were inspected for this review but are not included for redistribution.

The SL/SU formulation is indeed Conjecture 1.9 of [Chinburg–Reid–Stover](https://arxiv.org/abs/1706.00952), current arXiv v3, 27 July 2020, published in IMRN 2022. I also checked the adjoining Theorem 1.8 and Corollary 1.10 to ensure no unconditional universal resolution was overlooked there. Their arithmetic hypotheses cannot be silently dropped. The introduction actually recalls a curve of irreducible SU(2) characters somewhere in the character variety for each nontrivial knot, stronger than existence of one point. The artifact's weaker wording remains true, and its central conclusion is correct: those results do not locate such a curve on the distinguished component. Mentioning the stronger known statement would be an optional clarification, not a repair.

## 2. Finite quotient and preservation of arcs

I independently checked both directions of the normalization argument.

1. A hyperbolic knot exterior is aspherical and has vanishing second cohomology with Z/2 coefficients. Its projective representations therefore lift. The lift ambiguity is precisely H1 with Z/2 coefficients, a group of order two. The quotient statement must apply to the liftable projective locus first; for knot exteriors that locus is the whole character variety. The artifact makes this additional step rather than assuming liftability for arbitrary groups.
2. A finite algebraic quotient is closed and preserves dimension on each irreducible curve. A canonical SL curve thus maps onto the projective canonical curve. Smoothness and complex dimension one at discrete faithful holonomy prevent an ambiguity among local irreducible components.
3. A projectively compact representation, after conjugation into PSU(2), has every SL lift in SU(2). Indeed an SL representative of a PSU(2) matrix differs from a unitary representative only by a scalar whose square is one. This establishes the group-level bridge, not just real trace values.
4. Finite fibers prevent an actual unitary character arc from collapsing to a point. The relevant compact-character loci are semialgebraic: use finitely many generators and relations, the real algebraic SU(2) representation locus, and polynomial character functions. On a complex algebraic curve an infinite semialgebraic locus contains an arc. Restriction away from finitely many exceptional points handles branching and singularities.
5. Conversely, an arc on the projective canonical curve has infinitely many unitary lifts. One of the finitely many irreducible components of its algebraic preimage contains infinitely many of them. Its image is the whole projective curve, since a positive-dimensional closed irreducible subset of that curve is the curve itself. It contains a point above the complete holonomy, so smoothness there identifies it as a lifted canonical component. If a different lift of the complete holonomy was initially chosen, the central sign twist carries one such component to the other and preserves the unitary locus.

In particular, a general uncountability argument was not used in place of semialgebraicity, and the quotient was not incorrectly treated as an everywhere-free two-fold cover. These details agree with [Heusener–Porti, Proposition 4.2, Remark 4.3 and Example 4.6](https://arxiv.org/pdf/math/0302075). Branch fibers can be smaller.

## 3. Existing geometric theorem

I read the proof of Dix's Theorem 3.3.3, its preceding quotient lemma, Corollary 3.3.4, and the limitations in Section 5. The stated assumption is a Euclidean cone structure on the pair (S3,K) with angle at most pi. It gives a real unitary character curve on every SL canonical component. The two-bridge corollary is an established subcase.

The proof does control both positive-dimensional unitary deformations and membership in the canonical component: Euclidean rotational holonomy is smooth under the stated assumptions; regeneration supplies nearby hyperbolic cone characters; decreasing the cone angle reaches complete holonomy along smooth characters. The component cannot change along that smooth path. The almost-product exclusion and the hyperbolic-knot hypothesis occur in the source proof. Its Section 5 explicitly leaves the more general Montesinos degeneration question for future work. The artifact preserves those distinctions.

Source: [Dix dissertation, Section 3.3, printed pp. 14–16, and Section 5](https://escholarship.org/content/qt27j2v475/qt27j2v475_noSplash_7f3e70d717e17eaf9515cffc4ef313be.pdf). This is a source-verification and logical-dependency audit, not a new independent derivation of every cited cone-manifold theorem.

## 4. Multiple components and real-locus obstructions

[Boyle–Rouse](https://arxiv.org/abs/2403.07157), current v1 dated 11 March 2024, Theorem 1.1 and Remarks 1.2–1.3, concerns the two SL lifts of the same oriented complete holonomy. I read those statements and their surrounding definition. The nontrivial meridian-sign character is an automorphism of the SL character variety and takes one holonomy lift to the other. Uniqueness of the smooth local component then gives the exchange of the two canonical curves. The finite quotient identifies their images. The example 10_157 therefore supplies no second distinguished projective component and no counterexample to the desired arc.

The complex-conjugation test is also valid as a conditional obstruction: two distinct irreducible complex algebraic curves have only finitely many points in common, while all compact-real characters are fixed by the real structure in trace coordinates. One must still exhibit a qualifying knot. [Long–Reid, Section 5](https://math.rice.edu/~ar99/fields_of_defn_published.pdf) carefully distinguishes knot complements in S3 from their more general one-cusped constructions. Section 6 concerns invariant trace fields; those fields must not be confused with the field of definition of the canonical curve. The artifact does not make this mistake or present the general-manifold examples as knot counterexamples.

## 5. Algebraic controls and reproducibility

The isolated-point example is irreducible over C: viewed as a monic quadratic in y over C(x), its discriminant has an odd-order zero at x=-1 and is not a square. Gauss's lemma passes this to C[x,y]. For |x|<1/2 the nonnegative lower bound forces the only real zero near the origin to be the origin. The separate parameterized real arc is nonconstant, so the example precisely distinguishes an isolated point from an arc elsewhere.

The elliptic-generator matrices are separately conjugate over SL(2,R), but their product is diagonal with entries -1/4 and -4. Its trace has absolute value greater than two, excluding simultaneous conjugacy into SU(2). No relation making these matrices into a knot-group representation is asserted.

The submitted verifier was copied before execution so its output-writing behavior did not touch the author's files. Its 21 exact assertions pass. Independent checks additionally test the SO(3) adjoint action of rational unit quaternions, orientation and orthogonality, central-sign invisibility, multiplication, sign-twisted word traces, rank-two free-group finite quotient controls including smaller exceptional fibers, and independently derived acnode and elliptic-pair identities. All 121 independent exact assertions pass with SymPy 1.14.0, as recorded in `independent_results.json`. These are diagnostics, not finite evidence for the conjecture itself.

## 6. Final disposition

The source search was bounded, and neither the author's search nor this review establishes exhaustive absence of later literature. Current arXiv version histories and the principal theorem statements were checked on 30 September 2026. The package's explicit unresolved disposition is appropriate.

**Required corrections: none.** Preserve the original problem's `unsolved` status, no full-solution credit, and no novelty claim for the cited cone theorem or the elementary normalization deductions. A new substantive mathematical edit should receive a new review; a purely administrative change can be checked by an exact diff.
