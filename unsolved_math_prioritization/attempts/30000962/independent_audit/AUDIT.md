# Independent audit: recursive determination of quantum knot invariants

Date: 2026-10-07. Target: rank 965, problem 30000962 / OWR-1967-011.

## Verdict

**Accept the central partial results, subject to the corrections supplied here. The unrestricted target remains unresolved.** The frozen author packet is authentic and reproducible, but its central-Gaussian aside overstates a one-value conclusion unless the actual multiplier lattice is checked. A separate, low-severity verifier issue admits Boolean/float schema numbers when a caller deliberately repins the modified manifest. Neither issue invalidates the non-G2 uniqueness theorem, the all-simple-type unknot result, or the original external hash pin.

`CORRECTIONS.patch` is an explicit, unapplied patch against `PROOF.md` and `verify_packet.py`. `PROOF.corrected.md` and `verify_packet.hardened.py` are review copies. The frozen originals and their manifest were not edited. A corrected publication packet must regenerate its own manifest, diagnostic metadata and external receipt; applying this patch does not preserve the old manifest pin.

No source PDFs, source text files, corpus contents, or coordination messages are included in this audit. No publication was performed. The audit does not represent human peer review, formal verification, or a new general G2 solution.

## 1. Input authentication and replay

The 27,913-byte author ZIP has SHA-256 `64d3d4a8562911b3a2853fb3823ab8e52f1a795c663b3a97207f356aac4a2cd1`. Its 14 uniquely named `author/` members match the authored directory byte for byte. The 1,793-byte manifest has SHA-256 `82b3c843525fb245d0fc1a7fb6eaa472ef8589439cd230275687b910a222f0c9`. The executable verifier was separately authenticated at 2,944 bytes and SHA-256 `cb49cfa08609ae88c79b9978556f98e9b2a9cd4c3068d6d01ffd65d8092bdfcc` before execution.

Both normal and optimized outer verifier runs pass; each replays both inner modes. The 4,043 authored diagnostic checks reproduce byte-identically. The authored mutation suite reproduces 2 positive controls and 18 rejected mutations across the stated nine families. There are no assertions whose removal under `-O` changes these checks.

I independently wrote `independent_checks.py` without importing the author diagnostic code. Its 7,421 exact checks pass under normal and optimized Python with identical JSON, including full conjugated Reynolds evaluations, omitted-shift and plain-average negative controls, rational-form coordinate changes in ranks 1–3, complete character-cancellation blocks for the Gaussian counterexample, independently composed PBW terms, and a differently sampled singular-strip family. These are diagnostics, not proofs of universal statements.

The original external manifest hash remains an essential input. Passing a new pin on purpose tests schema validation, not tamper resistance under the original pin.

## 2. Mathematical review by claim

### Lemma 1: invariant equations recover the full equations

**Accepted.** Faithfulness ensures a regular lattice orbit exists. Nondegeneracy makes the orbit-separating hyperplanes proper. The interpolation multiplier is well-defined over the formal-parameter field and nonzero at the selected point. The left-ideal order `D E_gamma P` is correct: the shift reaches the target before multiplication extracts the regular orbit value. The Reynolds sum is in the invariant ideal because the full annihilator is W-stable. Nonzero scalar division is valid. In particular, the proof does not silently omit singular target weights.

There is a useful check on the argument: directly evaluate the conjugated multiplication factor as `D(w^{-1} beta)`. It kills every nonidentity summand before any symmetry of the competing function is used. Thus the extraction itself is even valid for arbitrary competitors once the ideal is known W-stable. The sign hypothesis is still a sufficient way to establish that stability. No strengthening is needed for the packet's stated conclusion.

### Lemma 2: a common finite set for every solution of a fixed ideal

**Accepted, conditional on the cited published theorem.** The source permits arbitrary value vector spaces and uses equality of annihilators. The author does not simply replace that quantifier. The family U of solutions is a set, its product value space is an algebraic vector space, and its universal sequence is cyclic and a quotient of the stipulated holonomic module. The selected finite S is therefore fixed before choosing any competitor.

Every linear automorphism fixing the finite seed span commutes with scalar-coefficient sequence operators and preserves the universal annihilator in both directions. The published equal-annihilator theorem forces it to fix every universal value. Over the characteristic-zero field, a vector outside the seed span can be moved by a basis-scaling automorphism fixing that span. Hence all values lie in the common finite span. Taking coordinates gives one finite reconstruction relation for every solution simultaneously. The argument uses ordinary algebraic basis extension, not an exchange of infinite sums or a finite-dimensionality assumption on the product space.

### Scalar coefficients and lattice/parameter passage

**Accepted after explicit clarification in the reading copy.** The author correctly keeps all unit lattice shifts and selects only integral multiplier vectors `v_i=c B^{-1}e_i`; these are already in the original algebra. The commutation parameter becomes `z=q^c`. No unapproved root multiplier or new lattice point is used. Since `F=C(t)` is finite over `R=C(z)`, an original word-growth bound gives a coordinate growth bound with only a finite dimension factor and a linear word-length change.

The appropriate ideal for the imported standard-coordinate theorem is `J=Ann_{A_0}(f)`, where `A_0` is the coordinate algebra over R. Every full-ideal competitor satisfies J. For F-valued competitors take the universal value space `F^U` as an R-vector space; the same automorphism proof applies over exactly the rational-function field in the published theorem. This avoids assuming an unstated coefficient-field generalization.

The reading copy also separates two scalar operations. Denominator clearing works directly in the fraction field of the original Laurent ring. If F is a further finite extension, expand an operator in a basis of F over that fraction field, use the original-valued function to show that every coefficient component annihilates it, and then clear denominators componentwise. Invariance also descends componentwise because W fixes scalars. A single scalar cannot in general bring arbitrary coefficients from a proper field extension back into the smaller ring.

For the knot application, the standard-coordinate growth premise can be obtained directly from dominant-color holonomicity: zero-extend the dominant function, shift by rho, and sum its Weyl pullbacks with signs. Regular weights have exactly one nonzero summand; walls have none. The cited closure properties supply holonomicity on the full lattice. A common parameter root is handled by finite scalar extension and finite residue-class decomposition of multiplier powers. Thus the asserted non-G2 consequence does not depend on an implicit identification of the different quantum-torus presentations, or on the invalid Gaussian one-seed shortcut.

### Theorem 3: non-G2 conclusion

**Accepted at the stated credited scope.** Combining extraction, coordinate holonomicity and the universal common-seed lemma gives uniqueness among all requested sign-equivariant competitors satisfying the invariant equations, including those with larger annihilators. The finite set may depend on the fixed knot and Lie algebra; the proof promises neither a uniform bound nor an effective algorithm. Formal q is essential. The detailed primary theorem excludes G2, and that exclusion is retained.

### Proposition 4 and the singular-strip obstruction

**Accepted.** Sequential propagation in each coordinate proves uniqueness from the stated box because both endpoint coefficients are nonzero at every lattice point. No unproved consistency assertion is needed. The rank-one finite-exception argument follows by grouping finitely many distinct affine exponent functions; their collision set is finite.

For the two-dimensional countermodel, the first forward difference of a function supported on n=0 has support n=-1,0, exactly where its coefficient vanishes. The second recursion's coefficient vanishes on n=0. Arbitrary independent values along that line therefore survive both equations and defeat any finite sample. This refutes only the auxiliary inference from nonzero polynomial endpoints. It is not a knot counterexample or a holonomic counterexample.

### Proposition 5: one-value uniqueness for the zero-framed unknot

**Accepted for the actual simple-root-system form.** The positive-definite form and regularity of rho ensure the normalizing denominator is nonzero. Its finite set of shift characters is distinct. Their maximal ideals are pairwise comaximal, so Chinese remainder idempotents split every solution of their intersection into those character eigenspaces. The eigenfunction relation on the entire lattice fixes each component by its value at zero. Vandermonde independence and the Weyl sign action leave exactly a one-dimensional coefficient space. The value at rho fixes the remaining scalar. Lemma 1 supplies the required full equations from the invariant ones. The argument includes G2 for this unknot only.

### Proposition 6 and semisimple products

**Accepted.** The two slice arguments use actual inclusions of each factor's full annihilator in the product annihilator. Their order gives all first-variable slices on the second seed set, followed by all second-variable slices. The stated tensor construction for a direct sum has independent factors and multiplicative quantum traces. This justifies semisimple sums of the established simple cases. A subalgebra inclusion does not supply this factorization and is correctly not used to claim a G2 reduction.

### Central Gaussian aside: a real but localized scope defect

**Requires the supplied correction.** Clearing denominators of a rational quadratic exponent is a scalar-field operation. It does not imply that each one-step ratio lies in the fixed multiplier lattice of A. The sufficient one-seed condition is

`Q(n+e_i)-Q(n)=c_i+B(v_i,n)` with `v_i` in the actual lattice and `q^{c_i}` in F.

Then, and only as a sufficient assertion, the displayed first-order operators are available. The reading copy states this condition explicitly and retains the unrestricted reductive caveat.

Here is a full-annihilator counterexample to the broader wording. Take `F=C(t)`, `q=t^2`, `Lambda=Z`, `B(a,n)=2an`, and `f(n)=t^{n^2}`. The basic available multiplier acts by `Q_1 h(n)=t^{4n}h(n)`. For a finite normal-ordered operator

`P=sum p_{a,b}(t) Q_1^a E_1^b`,

its action divided by f is

`sum p_{a,b}(t) t^{b^2} (t^{4a+2b})^n`.

Distinct exponential characters over C(t) are independent by the Vandermonde determinant. Therefore P annihilates f exactly when the coefficient sum in each equal-slope group is zero. Equal slopes force the shift exponents b to have the same parity. Replacing f by `h(n)=c_{n mod 2} f(n)` multiplies each such group, for fixed n, by one common scalar. Consequently **every** P in the full annihilator also annihilates every h of this form. This is not merely a failure of the single exhibited recurrence.

For any one chosen seed, leave its parity multiplier equal to 1 and change the other parity multiplier. The seed value is unchanged but the solution is different. Conversely `E_1^2-t^4 Q_1` gives a nonsingular two-step recurrence, so two consecutive values suffice. In the Section 2 coordinate bridge this example uses `c=2`, `v=1`, and `z=t^4`; that bridge correctly proves finite determination and never promises one seed.

### G2 PBW obstruction

**Accepted at its explicitly limited scope.** The selected two source terms have the stated exponent shifts and coefficients. Both increase the root weight by the short simple root. In AB, the B shift changes b by -2 and c by +1, contributing the combined factor q^(-5); the q-integer contributes the additional ratio involving c+1 and c. A does not change a or b, so B's coefficient is unaffected in BA. The two rational witnesses differ. Thus no coordinate-independent scalar q-commutation constant exists for this pair, and the elementary pairwise-q-commuting multinomial shortcut is unavailable for that decomposition. This says nothing adverse about the published PBW formula, a different decomposition, or the underlying conjecture.

## 3. Imported source scope independently checked

These are source-scope checks, not independent reconstructions of every external theorem's proof.

- [Original report](https://ems.press/content/serial-article-files/46168): inspected the defining passage and Conjecture 11 on printed p.1223. Its sign-equivariant uniqueness problem is distinct from adjacent Conjecture 12. The Cartan-determinant conventions do not by themselves resolve arbitrary central normalizations.
- [Sikora v2](https://arxiv.org/pdf/0807.0943): the extracted header identifies arXiv:0807.0943v2, 18 July 2008. Theorem 3, Proposition 5, Example 2, operator relations and Section 2 support the retained simple non-G2 scope, sign convention and unknot input. A journal-final version was not verified.
- [Garoufalidis–Le 2005 author text](https://people.mpim-bonn.mpg.de/stavros/publications/holonomic.pdf): Theorem 6 is a standard fundamental-weight-coordinate statement on dominant colors excluding G2. The surrounding discussion and Appendix A identify the missing G2 PBW structure-constant premise. The 20 July 2005 author version was used, not a claim of byte identity to the journal PDF.
- [Garoufalidis–Le 2016](https://ems.press/content/serial-article-files/44334): Sections 2–3 permit an arbitrary R-vector value space; Proposition 4.1 gives quotient closure; Proposition 3.4 compares the positive and invertible operator conventions; Theorem 5.2 and Proposition 5.4 give the relevant coordinate/extension closures; Theorem 7.4 on printed p.523 has the literal equal-annihilator quantifier. Its general introductory wording is not evidence that G2 was added to the earlier knot theorem.
- [Kuniba–Okado–Yamada 2013](https://emis.de/ft/13018): Section 5.4, root-vector definitions and Lemma 4 on printed p.19 agree with the selected multiplication terms and the q-integer convention used in the calculation. The entire source was not independently audited.
- [Belletti v1](https://arxiv.org/html/2512.10837v1): Theorem 2.7 concerns an elimination criterion, while Section 3.2 explicitly works with Kauffman-bracket skein modules. This inspected scope supplies no arbitrary-G2-color theorem. It remains a versioned preprint citation here.

All these inspections used web-provided text. Independent screenshot attempts for GL16 p.523 and KOY13 p.19 failed with cache misses. No pixel inspection, local source-PDF bytes, source-PDF sizes or source-PDF hashes are certified. No blocked source-download command was retried. A bounded source inspection cannot certify global current openness or historical priority.

## 4. Verifier issue and regression controls

The frozen verifier tests `schema != 1`. In Python, `True == 1` and `1.0 == 1`, so manifests deliberately changed to either value and deliberately repinned are accepted. `schema_diagnostics.json` records the two reproductions. This is a strict-schema overclaim, not a way to evade the original hash pin.

The supplied one-line repair requires `type(schema) is int` as well. `test_hardened_schema.py` installs the hardened verifier only into temporary copies, updates its manifest entry, pins each controlled test manifest, and checks baseline integer 1 against Boolean, float, string, different integer and null alternatives in both outer interpreter modes. The result is 2 accepted baselines and 10 rejected malformed-schema cases. These new tests are distinct from the original 18 controls, which still reproduce against the unchanged freeze.

## 5. Provenance and remaining boundaries

Both complete local corpus files were independently rehashed. The 68,931,837-byte problem corpus has 15,458 records and SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`. The 80,334,822-byte research corpus has 6,701 records and SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`. There is one matching problem record, identical to the author's local extracted record, and no exact `OWR-1967-011` research key. The canonical target-record hash and cleaned-statement hash reproduce. These are metadata-only findings; corpus contents are excluded. The separately named selected-pair hash was not recomputed because its pair-construction schema is not supplied in the packet.

The historical repository attempt gate was inspected as a bounded author record, not independently re-run against the repository during this mathematical audit. The ledger records five substantively distinct approaches. Source checks, finite diagnostics, and this audit are not additional solution attempts.

The unresolved parts remain arbitrary nontrivial G2 knot functions and the unrestricted reductive-center conventions. There is no knot counterexample, no general resolution, and no assertion of novelty. Corrected partial conclusions may be reported with those boundaries. The original freeze should not receive an unqualified all-claims-pass label because the Gaussian wording and strict-schema claim required repair.
