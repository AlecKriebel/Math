# Independent audit: centered-arc Hilbert series and ADE surface germs

Problem 30005416 / OWR-12697689-012. Audit date: 11 October 2026.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made. The historical question’s intended category and worldwide current status are not certified.

## Verdict

**ACCEPT the mathematics with the stated category boundaries.** The crossing and pinch-point counterexamples are correct for the scheme-theoretic centered-arc algebra with the natural jet-weight grading. The normal finite-type surface converse is also correct over an algebraically closed field of characteristic zero; with a rational center over any characteristic-zero field, its conclusion is geometric ADE. No fatal gap or counterexample to that restricted theorem was found.

**Do not convert this into an unqualified historical-resolution or novelty verdict.** The broad counterexample from a crossing is already in the foundational paper. Neither the 2013 nor the 2023 question explicitly states normality or isolatedness, but the writer's intended category cannot be recovered definitively from that omission. The normal-surface theorem is an explicitly scoped converse, and worldwide priority for either that derivation or the pinch-point observation is unestablished. A complete literature/proof-history search was not performed.

The original mathematical report was authenticated and reviewed at SHA-256 357df0630930399d03cbdac239bf1d39cd279db27f000d26372ea30f26b14967, under creator manifest SHA-256 a1f4d31a2dd58ee28a8bec08aac72b94b8453c5b7738cedb81c24c52cc799655. All 42 manifest members, totaling 5,327,454 bytes, were independently rehashed and the inventory checked closed. The creator external-seal SHA-256 is 4ebd215f60c49e3fcd1e5ec5f31de791b9421ba6d5c477bb58ac3fe92acd52d3. The independent audit has its own separately authenticated closed 26-member inventory. VERIFICATION.json retains the original proof, audit, inventory and external-seal identities. The public proof includes the citation-strengthening supplement described below; the original report remains unchanged.

## 1. Exact target and source category

Write

\[
C(q)=(1-q)^{-3}\prod_{i\ge2}(1-q^i)^{-2}.
\]

The official 2023 OWR contribution defines the invariant from the scheme of arcs centered at a closed point, over a characteristic-zero field, with dimensions taken over that field. Its question follows the ADE formula. The surrounding contribution explicitly includes nonreduced schemes. It does not say that the converse is restricted to normal or isolated surfaces. The 2013 manuscript resets the discussion to an affine scheme over a field in Section 4.1; its characterization question is 4.5. In the alternate author manuscript the corresponding question is 4.4. The nearby question about eventual counts of jet components is different and must not be substituted.

These observations justify distinguishing broad and normal-surface readings. They do not justify claiming the author intended reducible or nonnormal examples to settle the question. In particular, BMS has the ADE and normal-crossing formulas together on page 9, years before the later questions.

The historical catalog record’s open label and 2026-08-22 literature date are historical input metadata. They do not invalidate the proof, establish novelty, or prove that a scoped result answers the intended historic problem. Bounded search findings do not establish complete prior-proof history or worldwide priority.

## 2. Scheme structure, weights, and completion: passed

For a rational center, centered jets over **every** test algebra A send the maximal ideal into (t) in A[t]/(t^(m+1)). Centered arcs send it into tA[[t]]. Consequently:

- Functions nonzero at the center become units, so localization at the center changes neither centered functor.
- The finite-jet homomorphism factors through a finite maximal-ideal quotient and uniquely extends to the completed local ring.
- The arc homomorphism uniquely extends continuously by t-adic convergence. This argument works when A has nilpotents; it is not merely a statement about field-valued arcs.
- A formal change of coordinates gives a polynomial expression for each fixed t-coefficient, homogeneous of its jet weight. A unit multiple of a defining equation gives the same coefficient ideal.

Thus the completed presentation is legitimate for the actual scheme-theoretic centered-arc algebra. It is not a replacement by the set of arcs or the reduction of the arc scheme.

Every variable of index i has positive weight i. In weight h, no equation of weight greater than h and no variable of greater weight can contribute. The centered m-jet algebra therefore agrees with the arc algebra in weights h <= m. This proves the exact stabilization needed in the report. No injectivity claim about an entire finite-truncation ring map is needed, and such a claim would generally be unsafe.

Likewise, if formal defining equations differ in maximal-ideal order N+1, their t-coefficients through order N agree. The conclusion holds over arbitrary coefficient algebras, not just over a field. This is sufficient for the D_n-to-pinch argument; no limit of geometric points or flatness of a family is being invoked.

The BMS factorial-normalized derivative variables differ from ordinary coefficient variables by invertible scalar factors in characteristic zero. The weights and Hilbert series coincide. The report correctly excludes any unproved positive-characteristic extension of its normal theorem.

## 3. Counterexamples: passed, with prior credit

### 3.1 Crossing cylinder

For xy=0 in three-space the centered equations are F_j = sum_(a=1)^(j-1) x_a y_(j-a), j >= 2. Over an algebraic closure, their vanishing locus at level m is the union of the displayed m linear subspaces, each of codimension m-1. This determines the height of the original ideal even though the ideal need not be radical. The same height calculation for every prefix, together with Cohen–Macaulayness of the successive complete intersections, proves regularity of the displayed sequence. Therefore its Hilbert series is the claimed product. Passing to stabilized weights gives C.

The nilpotent check is valid: x_1 y_2 is nonzero in weight 3 but its square vanishes using F_2 and F_3. The reduced centered-arc ring instead has all x_i y_j equal to zero. To justify that last description, a prime quotient is a domain, so x(t)y(t)=0 implies that one whole series vanishes; the radical is the intersection of the all-x and all-y ideals. Its series is 2H^2-H, for H=product_(i>=1)(1-q^i)^(-1), and its weight-3 coefficient is 17 rather than 18. The report does not accidentally use this reduced algebra.

BMS Proposition 3.9 with d=e=2 gives the very same crossing cylinder formula. Its use as a counterexample is mathematically sound but not a novel formula or newly discovered broad obstruction.

### 3.2 Pinch point

The equation x^2-y^2 z differs from the standard D_n equation x^2-y^2 z-z^(n-1) only in order n-1. For any fixed N, choosing n-1>N makes all coefficient equations through weight N identical. The known D_n formula consequently forces agreement with C in every fixed weight. It is legitimate to choose n separately for each N. Neither reducedness of arc schemes nor a uniform family limit is required.

The injection of the completed local quotient into k[[u,v]] via x=uv, y=u, z=v^2 is correct. Monicity in x gives a unique representative a(y,z)+x b(y,z); even and odd v-exponents cannot cancel. This proves domain and geometric-domain assertions, including after any field extension. The Jacobian singular locus is the line x=y=0 in characteristic zero. The fraction x/y is integral, satisfies T^2-z, and is not local-regular: modulo y, x remains nonzero in the ring with x^2=0 and cannot be killed by a unit. Hence the surface is nonnormal and nonisolated, although geometrically integral and formally irreducible.

The weight-1 element x_1 is a nonzero nilpotent in its centered-arc algebra because F_2=x_1^2. This supplies a second explicit safeguard against counting only reduced arcs.

The pinch example defeats proposed repairs based solely on irreducibility or formal irreducibility. It does not defeat a normality or isolated-hypersurface restriction. No first-discovery claim is warranted from the bounded searches performed here.

## 4. Infinite regular-sequence criterion: passed

The decisive step was independently checked rather than inferred from finite computations. For R_j=S/(f_1,...,f_j), K_j=Ann_(R_(j-1))(f_j), and P_j=product_(i<=j)(1-q^(d_i)), multiplication by f_j gives

\[
H_{R_j}=(1-q^{d_j})H_{R_{j-1}}+q^{d_j}H_{K_j}.
\]

The correct normalized telescoping identity is

\[
\frac{H_{R_j}}{P_j}=H_S+\sum_{i=1}^j\frac{q^{d_i}H_{K_i}}{P_i}.
\]

Each summand on the right has nonnegative coefficients, because every inverse Euler factor does. With finitely many d_i below any bound, the sum, product, and quotient limits are well-defined coefficientwise. Each ideal piece stabilizes for the same reason. Thus H_B=H_S product_i(1-q^(d_i)) forces every annihilator K_i to vanish. A zero equation is also correctly detected: its annihilator contains 1.

The tempting unnormalized expression can have alternating coefficients and does not by itself show that defects cannot cancel. The report uses the normalized identity, which eliminates that objection completely. It requires no Noetherian hypothesis, reduced quotient, or domain assumption for S. The application to an infinite positive-weight polynomial ring is valid.

## 5. Normal-surface converse: passed

All of the following hypotheses and transitions matter:

1. **Finite type and a rational closed center.** The coefficient of q is the embedding dimension, because a minimal completed presentation has no linear equations. Equality with C forces embedding dimension 3; it also excludes smooth surface points.
2. **Normality and excellence.** Completion of the normal finite-type local ring is a normal domain of dimension 2. In a minimal Cohen presentation by k[[x,y,z]], its kernel is a height-one prime. This regular local ring is factorial, so the kernel is principal. Without the stated normal/excellent hypotheses this argument cannot simply be reused.
3. **Return to an algebraic neighborhood.** The hypersurface/complete-intersection property descends from completion and is open for a finite-type scheme. Normality gives regularity in codimension one. In characteristic zero, regularity is smoothness; after shrinking, the only singular point is O. One can also restrict to the unique normal irreducible component through O. This supplies the integral finite-type lci variety required by the imported theorem, rather than applying it directly to a formal scheme.
4. **Every prefix is regular.** The centered coefficient equations F_j have prescribed weight j. The normalized criterion applies to F_2,F_3,..., including the possibility of a zero equation, and proves every finite prefix regular in the infinite polynomial ring. Faithfully flat polynomial extension then proves regularity in S_m itself. In particular F_2 is nonzero and multiplicity is two.
5. **Dimensions are exact.** The centered m-jet fiber is cut out by m-1 regular equations in 3m variables, hence has dimension 2m+1. Since the singular locus of the chosen neighborhood is just O, its entire singular jet locus has that dimension, strictly less than 2m+2.
6. **Jet irreducibility and ADE.** Mustaţă Proposition 1.4 applies to an integral finite-type lci variety. Every component of the full jet scheme has dimension at least 2m+2, while the smooth-locus preimage is irreducible of that dimension. The singular fiber cannot support an additional component. Thus every full jet scheme is irreducible. Theorem 0.1 then gives rational singularities; the hypersurface is Gorenstein, and a rational Gorenstein surface singularity is ADE.

As an additional direct source check, the final arXiv v5 has **Theorem 4.4 on PDF page 19**, which states for surfaces in characteristic zero that all jet schemes are irreducible exactly when the singularities are rational double points. This theorem can replace the last classification sentence once jet irreducibility has been established. Its proof was inspected; its deeper imported motivic-integration theorem was not re-proved. The creator cited v4 accurately, and the relevant statements in final v5 agree. This is a citation-strengthening supplement, not a mathematical correction.

The exact point where the broad examples evade the proof is Step 3: the singular locus is a curve, so a bound for one centered fiber cannot be substituted for a bound on all jets above the singular locus. One cannot infer normality merely from the centered Hilbert series.

## 6. Ground field, residue field, and split forms: passed

Over a characteristic-zero field k, finite-type normality is geometrically preserved because k is perfect. At a k-rational point, every homogeneous coefficient space commutes with extension to an algebraic closure, preserving its dimension. The normal geometric component through the lifted point is well-defined locally. Applying the theorem there proves geometric ADE; descent of a chosen split normal form is neither needed nor valid in general.

For example x^2+y^2+z^2 over the reals is a geometric A_1 form and has the same scheme-theoretic Hilbert series, although its real quadratic tangent cone is anisotropic. This illustrates why real-valued arcs alone cannot define this invariant and why the conclusion must not promise a split equation. This example was included in the independent finite controls.

At a nonrational closed point, the OWR dim_k convention has constant term [kappa(O):k]. Equality to C therefore forces a rational center. If dimensions are instead taken over the residue field as in BMS, one must rebase the centered question to that field. Closedness ensures a finite algebraic residue extension; characteristic zero makes it separable, so this rephrasing does not introduce infinitesimal directions from a transcendental residue field. The report's distinction is necessary and correct. Nothing here asserts the same formulation at arbitrary nonclosed points.

## 7. Independent adversarial computations

An independent control program was authored for this audit; code and raw computational outputs are omitted from this prose edition. It does not import or execute creator or source-author code. It builds coefficients by truncated polynomial convolution, enumerates exponent-count monomials with a species-grouped variable order, and computes ideal-piece ranks by exact integer fraction-free row elimination over Q. This differs from the creator's Fraction-based implementation. The complete results were reproduced identically under ordinary Python, -O, and -OO; no assertions are used as required checks.

Through weight 10 the target coefficients are

1, 3, 8, 18, 38, 74, 139, 249, 434, 734, 1215.

Positive cases: crossing, pinch, D_4, anisotropic quadratic form, pinch under x -> x+y^2, and pinch multiplied by the unit 1+z. All agree. Genuine negative controls:

- The doubled plane first differs at weight 4, with 39 instead of 38.
- The normal isolated hypersurface x^2+y^3+z^6 agrees through weight 9 but has 1216 rather than 1215 in weight 10.
- The cusp cylinder x^2+y^3 has the same first discrepancy at weight 10.
- The reduced crossing has 17 instead of 18 in weight 3.
- Adding z^(N+1) is invisible through weight N; adding z^N is detected in its coefficient equations. This last control concerns equations, not a claim that every such perturbation changes the Hilbert series.

The isolated non-ADE example is especially informative. Its first four potentially nonzero centered equations are F_2,...,F_5. In the quotient by F_2,F_3,F_4, exact rational Gröbner reduction shows that y_1^5 is nonzero but y_1^5 F_5=0; y_1^4 F_5 remains nonzero. Also x_1=x_2=y_1=0 gives a 12-dimensional linear space inside its fifth centered-jet fiber, whereas a regular prefix would give dimension 11. Thus a finite-prefix defect really occurs, and the normalized identity predicts a Hilbert discrepancy no later than weight 10. The independent coefficient calculation finds it exactly there. This is a deliberate attempted counterexample to the positive route, and it is correctly rejected rather than misclassified from the creator's shorter weight-8 agreement.

Finite checks remain controls, not proofs of infinite equality or a proof that no other singularity exists. The all-weight conclusions rest on the reviewed symbolic arguments and cited theorems.

## 8. Current-source and provenance limits

The source-byte identities and exact creator and auditor read/visual scopes are retained in SOURCES.json. Whole-source retrieval, text search, reading selected mathematical passages, rendered-page inspection, and full-proof audit are distinct.

- The 2026 Afsharijoo–González Pérez–Mourtada arXiv record currently lists only v1, dated 17 January 2026. Its inspected pages 1–5 use the known A_r series for partition identities and propose an initial-ideal conjecture. They do not prove the converse at issue.
- The 2025 Mourtada survey, located independently through that paper's references, has a forward ADE theorem in Section 2. The inspected definitions and proof do not resolve the intended scope of the older characterization question. Lexical absence of a phrase is not a proof that no related result exists anywhere.
- The 2020 HDR passages inspected give the broader forward canonical-hypersurface formula. No reverse characterization was found in those passages.
- Mustaţă final v5, independently retrieved, preserves the imported hypotheses and supplies the surface-specific theorem just discussed.
- Additional targeted searches for pinch-point/Whitney-umbrella arc Hilbert statements and normal-surface converses did not locate a direct priority source. Their coverage is limited; no absence-of-prior-work claim follows.

No author was contacted and no source-author code was executed. This prose edition retains the complete mathematical review, essential examples and coefficient counts, scope and novelty qualifications, and inspection history. It excludes copied source documents, derived source extracts, source-page images, programs, raw computational outputs and private coordination material. Edition preparation reauthenticates the evidence bytes and verifies packaging; it adds no mathematical experiment, new scholarly-source-body inspection or literature survey.

## Recommended disposition

Accept the report's crossing proof, integral pinch-point deduction, noncancellation lemma, and characteristic-zero normal-surface equivalence. Retain the category ambiguity, prior credit, geometric-versus-split distinction, and unknown novelty. An unqualified claim that a newly solved historical open problem has been established would go beyond this audit.
