# Independent adversarial audit: 30004494

Audit date: 2026-10-05 (UTC). Author freeze: hodge_30004494-author-v1.

## Verdict

**REVISE_REQUIRED, limited to one source-scope correction.** The retained mathematical propositions and their stated limitations pass this audit. The general Hodge-theoretic target remains **unsolved, 5/5 approaches exhausted**. No counterexample to the original hypotheses is established. No novelty claim is supported or needed.

The correction concerns an omitted unmodified-base case in the Deng–Tsimerman literature summary. It does not invalidate the algebraic proofs or turn the investigation into a solution. See M1 below and MANDATORY_CORRECTIONS.md. After M1 is incorporated and the resulting packet is integrity-checked, no other blocking issue was found in the reviewed scope.

## Frozen input and audit scope

The ZIP is 25,030 bytes with SHA-256 2880eb1f6345f6326c5b4ed8ab05801aa3c5db71d07e5a383472c74d69bcddbe. MANIFEST.json has SHA-256 1b384c58531496829886e4a0a96820dad434ea796a3c36b96f532e5b6c6a8571. All ten archive members match the frozen directory byte for byte; all nine manifest entries match their sizes and hashes. The source packet was not edited.

Every author file was read, including all arguments in PROOFS.md, the exact-target and source qualifications, five-approach log, source metadata, readiness record, verifier and frozen verifier output. The author's runner was reproduced byte for byte. Independent arithmetic code was written without importing the author's implementation. All arithmetic remains supplemental to the geometric proof audit.

Primary theorem statements, definitions and relevant hypotheses were checked directly at official scholarly URLs. Local retained source PDF hashes were separately verified against the author's metadata. This validates those retained files, not a claim of independently downloaded identical remote bytes. The two public dataset snapshots' complete byte counts and hashes were independently recomputed. Repository search-history claims were not independently rerun; they remain explicitly bounded author observations and are not mathematical evidence.

## M1: mandatory source-scope correction

RESULT.md says the generalized toroidal result changes the base. SOURCE_AUDIT.md §5 similarly discusses only a modified-base route. That omission matters for this target: Deng–Tsimerman v4 Theorem 2.11 allows the original compactification when the monodromy cones satisfy Definition 4.6. The target's fibrewise logarithmic injectivity forces independence of the local monodromy logarithms, by GGR Lemma 3.11(ii). Their nonnegative span is therefore simplicial, and each generator is a face. Thus this special case applies in the integral/unipotent framework being compared. [Deng–Tsimerman, §§2.2, 4.2](https://arxiv.org/html/2506.10109v4), [GGR, Lemma 3.11](https://arxiv.org/pdf/2102.06310v1).

The valid remaining limitations are that projectivity of the generalized toroidal target is Conjecture 2.12 in the inspected version, and that the cited statements do not construct the required effective correction. A necessary change of compactification must not be listed as an obstacle for this particular local-Torelli input. This is a source-interpretation correction, not a new ampleness argument.

## Proof-by-proof findings

### Proposition 1: closed-null-face criterion — PASS

The normalized slice of the closed effective-curve cone is compact: strict positivity of an ample functional on the unit-sphere section bounds the norm. On its intersection with the null face, strict negativity of E has a uniform margin. A relative open neighborhood retains negative E; its compact complement has L bounded away from zero. This produces one positive t working everywhere, not separate thresholds depending on curve classes. Kleiman applies because X is smooth and projective over C. Adding a nef class gives all later integer m. The empty slice/null-face cases are handled correctly.

The curved-cone control is valid. Its limiting null direction has zero correction, so it violates exactly the strictness required by the proposition. It is properly labeled an abstract cone control, with no Hodge realization claimed. Positivity on actual null curves alone has not been substituted for positivity on the complete closed face.

### Proposition 2: fixed integer coefficients — PASS

Approximation inside the open ample cone can preserve coefficients that are exactly zero and the signs of positive coefficients. Increasing t uses nefness, and clearing a single denominator produces a single integral effective divisor. The same divisor works for all subsequent m. No m-dependent correction is introduced. The statement would need nefness; the text supplies it. No semiampleness inference is made from openness.

### Theorem 3: constructive surface theorem — PASS

Kodaira's lemma applies to the big Cartier divisor and gives a fixed effective G. Any null curve must occur among its finitely many components. The Hodge index theorem first gives negative semidefiniteness of the intersection matrix. If a nonzero kernel vector existed, replacing its entries by absolute values would produce a nonzero effective real divisor with square zero in L-perp. The signature theorem would make its numerical class zero, contradicting its positive intersection with an ample divisor. This closes the otherwise easy-to-miss linear-dependence issue.

For P=-A, the strictly convex quadratic minimization argument gives P^{-1}1 componentwise positive, including disconnected matrices. Rationality and a common denominator give integral coefficients and a uniform negative intersection with every null component. The diagonal (-1,-2) control correctly refutes a universally positive eigenvector shortcut.

Uniformity is genuinely proved. Outside the finitely many components of G, cH-E ample bounds E.C by cH.C for every curve simultaneously; m>=kc suffices there. Finitely many remaining positive-L components supply finitely many further thresholds. L.E=0 and L²>0 then give positive self-intersection for all sufficiently large m. Nakai–Moishezon applies to the resulting integral divisors. The proof does not depend on the cone being polyhedral or on the nef and big divisor already being semiample.

The theorem is conditional on its algebraic hypotheses; it does not silently prove higher-dimensional Hodge positivity. Independent Hirzebruch-surface controls recover the sharp threshold m>=2 for L=S+eF, E=S, e>=1.

### Proposition 4.1: relative ampleness — PASS

The morphism is between projective varieties; ample twisting of a relatively ample invertible sheaf is applicable. Once rkL-E is ample, nefness of L supplies every larger exponent, including other residue classes modulo r. Conversely, an absolutely ample invertible sheaf is relatively ample, and twisting by a base pullback preserves relative ampleness. Therefore the claimed equivalence has the correct fixed-E quantifiers. The result does not supply an effective boundary-supported relatively ample negative divisor. [Stacks, Lemmas 29.38.7 and 29.38.10](https://stacks.math.columbia.edu/tag/01VG).

### Proposition 4.2: generic-immersion weakening — PASS

The product of two fine modular curves provides a genuine integral polarized weight-one variation with generically immersive period map; the two factors vary independently. Blowing up an interior point leaves an SNC boundary unchanged nearby, while the exceptional curve lies entirely in the smooth open base. The pulled-back variation is constant along that curve, so its Hodge determinant has degree zero there; each boundary component is disjoint from it. Every proposed corrected class has degree zero on that curve, regardless of coefficients and m.

The exceptional curve contributes a tangent kernel, so the construction fails the required everywhere injectivity. It is consequently only a counterexample to the generic-immersion weakening. It cannot be used to mark the original problem solved or disproved. Pullback functoriality needed locally is ordinary smooth-family functoriality; no unproved boundary-descent claim is required.

### Proposition 4.3: boundary blowups — PASS

The sign of the exceptional correction is correct: O(-F) is the relatively ample tautological bundle. Ample twisting yields k*pi*(m0L-E)-F. The replacement E'=k*pi*E+F is fixed, effective, integral and supported on the reduced total boundary, though its coefficients need not all equal one. Nefness supplies every m>=km0. The smoothness/SNC conditions are explicitly assumed. This proves upward stability only; descent of a successful correction was not claimed. [Stacks, blowing-up properties](https://stacks.math.columbia.edu/tag/01OF).

### Theorem 5.1 and the dual alternative — PASS

The finite-generator assumption is used precisely where a common threshold is selected. Nefness makes the null face generated by the zero-L generators. Rational feasible coefficients can be scaled once. Strict positivity on every generator then means positivity on the whole closed cone, so Kleiman applies.

The dual sign is correct: infeasibility of Ba<0 with a>=0 is certified by y>=0, y nonzero, B^T y>=0. Introducing nonnegative slack gives the finitely generated closed cone used by the separation argument. Strict inequalities can be normalized to Ba<=-1 because the number of rows is finite. The rational-certificate conclusion is valid under the rationality convention stated in the theorem. The simultaneous-choice matrix is a legitimate algebraic obstruction, not a geometric counterexample.

Nonblocking clarification: place “rational polyhedral” in the theorem's opening hypothesis, rather than clarifying rational generators afterward. Finite polyhedrality alone does not mean rational polyhedrality. The underlying real feasibility statement remains valid; rational dual certificates require rational data.

## Bundle identities and current-source checks

The determinant calculation is correct under the specified unipotent canonical-extension convention. From the polarized annihilator sequence, d_p=d_(n+1-p)*T^{-1}; the determinant local system T is torsion and has trivial boundary monodromy. Pairing factors gives G=L² modulo torsion in even weight and G=L²*d_r^{-1} modulo torsion in weight 2r-1. In weight one G=L. Killing torsion justifies the even-weight semiampleness deduction. The same formal deduction is unavailable in odd weight >=3.

BFMT v2 Corollary 1.3 concerns an integral polarizable pure variation, unipotent boundary monodromy, and the full Griffiths bundle. Its projective period-image construction and ample pullback identification do not produce a boundary-supported effective relatively anti-ample divisor. The extra hypotheses of the more general CY theorem were not silently discarded. Only applicability and statement scope were audited here, not the entire proof of that preprint. [BFMT v2](https://arxiv.org/html/2508.19215v2).

The 2021 progress report's withdrawal and incomplete Theorem 1.7 proof were independently confirmed. GGR v6 corrects individual-determinant descent and includes the relevant odd-weight upper-half-product failure in Appendix A; that failure is not, by itself, a failure of ampleness after boundary correction. Neither discarded claim enters the retained proofs. [Withdrawal record](https://arxiv.org/abs/2106.04691), [GGR v6](https://arxiv.org/html/2010.06720v6).

The normal/conormal sign caution for the infinity paper is warranted. Theorem 5.1's divisor identity and Corollary 5.4's negative conormal expression are compatible in additive notation. Fibrewise identities and local coefficient signs do not choose one effective vector for every null direction. [Period maps at infinity, §5](https://arxiv.org/html/2509.08508v1).

The original target and its fixed-coefficient quantifiers match the official report and precise 2021 formulation. The irreducible-boundary statement carries finite cone generation and level-one differential assumptions; the surface statement uses everywhere ordinary immersion. These conditions were not erased. The earlier GGLR source was only used with the author's disclosed landing-page-level inspection. [OWR24/2020](https://publications.mfo.de/bitstream/handle/mfo/3797/OWR_2020_24.pdf).

## Independent computation and limits

See INDEPENDENT_VERIFICATION.json for actual counts. The independent runner uses a permutation determinant/Cramer's-rule implementation, exhaustive small sign matrices, an exact interval arrangement deciding real primal/dual feasibility for all 2x2 integer matrices in a fixed range, and associated-graded determinant bookkeeping distinct from the author's upper-filtration pairing code. It also checks concrete ruled-surface numerical examples and the curved-cone quantifier obstruction.

These checks do not prove Hodge index, Kodaira's lemma, Kleiman, Nakai–Moishezon, positivity of Hodge extensions, genuine cone realizability, or the original conjecture. Those are geometric inputs or goals and were reviewed separately at the written-argument level. No finite assertion count can replace the missing global effective boundary correction.

## Safe deliverable and conclusion

The audit directory contains only this original analysis, correction instructions, public source verification metadata, exact-control code/output, verdict metadata and an integrity manifest. It excludes source PDFs, source extracts/images, raw dataset records, and private coordination. No remote write was made.

The appropriate mathematical status remains unsolved. The general missing step is one effective boundary combination strictly negative on every nonzero class of the entire closed L-null face. All retained reductions preserve that gap. Correct M1, retain the current limitations, and do not upgrade this partial-result packet to a complete solution.
