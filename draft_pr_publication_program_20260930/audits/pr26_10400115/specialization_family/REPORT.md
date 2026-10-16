# PR26 specialization-family adversarial audit

## Verdict and strongest verified result

**PASS_PARTIAL for mathematics, with two required provenance/scope metadata repairs.** Original target10400115/AMR-103-0115 remains UNSOLVED. The original `1/5` is one substantive attempt used out of five allowed, not a completion percentage. The original heuristic completion estimate is10%. This audit validates that partial and consumes no new substantive attempt toward the general problem.

Exact original head: `762f5808268a85a5cb5373d3f7d60ad160b828f5`. All14attempt files in `source_snapshot` match this head byte for byte, including source-budget and reviewer records. The complete PR diff has15paths: those14files plus `unsolved_math_prioritization/QUEUE.md`. Its only queue change is the10400115row from queued0/5 to unsolved1/5, with correctly limited commentary. No Git, canonical file, queue, PR, or publication mutation was performed by this family.

For finitely generated groups and unrestricted finite matrix degree, existence of a faithful representation over Qbar is equivalent to existence over Q. A faithful rational-function representation preserves any specified finite collection of nonidentity elements after some admissible rational specialization. Nevertheless the explicit two-generator Laurent semidirect matrixgroup has a nontrivial kernel under **every** nonzero algebraic specialization of its displayed representation. Each of these is fully proved. None supplies a braid-specific kernel, prohibits all rational representations of a group, or establishes a faithful algebraic braid representation for n>=4.

## Independent ordering and source evidence

Root AGENTS was read; no applicable nested AGENTS was found under the audit program. The literal primary source, full relevant page and surrounding context were read before historical note, reviewer, scripts, root/sibling reconstruction, source-budget, or original PR detail. The parent supplied only the task/head and assigned mechanisms. `EARLY_CRITERIA_RECONSTRUCTION.md` was sealed at2026-10-01T22:06:09.710605+00:00 with SHA256 `7dbb00f9cc2139a9b89010f65e545280735b5fcfefd9abbf8dd5a454a16a280f`; `EARLY_SEAL.json` records this ordering. That artifact contains full independent proofs and pre-registered negative controls. Its bytes remain unchanged. `EARLY_CORRECTIONS.md` preserves the subsequent correction of my mistaken pre-read description of1/5as a score.

[Ohtsuki's primary source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printedp470/PDFpage98, visually shows Qbar. The full page was locally rendered and inspected; p469/p471 context was also read. The exact target for each fixed n>=4 is existence of a finite d and rho:B_n->GL_d(Qbar), with rho(w)=I implying w=1 for every finite braid word, including arbitrary length and inverse generators. No matrix degree is fixed. A negative result must address every degree and every representation for the specified braid index. The source's historical open-status statement is not proof of today's literature status.

[Krammer's primary paper](https://arxiv.org/pdf/math/0405198), Annals155(2002)131-156, TheoremB, works with q real0<q<1 and t formal over R[t^{+-1}]. Its introductory comparison explains that the earlier n=4method uses real t instead. Parameter letters cannot be silently identified across conventions; a faithful representation with one formal parameter is not a representation over Qbar. [Bigelow's later primary exposition](https://web.math.ucsb.edu/~bigelow/publications/08.pdf), pp51-53, also distinguishes the Laurent homology module from its field extension. No problematic published matrix formula was used here.

After sealing, the full relevant [Scherich2023paper](https://msp.org/agt/2023/23-5/agt-v23-n5-p03-s.pdf) statements/proof were read: Theorem1.1and proof, and complete§3.3with Corollary3.10and Example3.11. They conclude discreteness for certain Salem-number specializations. They assert no injectivity. The general logical implication is invalid: a homomorphism with discrete image may have an arbitrarily large kernel. This family did not run a global literature search or independently certify that no later solution exists.

Fresh Ohtsuki and Scherich PDFs match original `source_checksums.json` in both byte count and SHA256 (`SOURCE_HASH_RECHECK.json`). Foreign PDFs/rendered source bytes and isolated replay bytes remain in ignored `tmp/`; first-party artifacts record hashes/URLs only. No outside individual was contacted, and no outreach was prepared.

## Universal proof audit

### Restriction of scalars

Let finite generators have images A_i in GL_d(Qbar). Finitely many algebraic entries generate a number field K with finite degree m over Q. The inverses are already in M_d(K), since A_i^{-1}=adj(A_i)/det(A_i), det(A_i)!=0. Thus all words have coefficients in K. Acting on the underlying Q-vector space K^d defines T:GL_d(K)->GL_{dm}(Q). It preserves products and inverses. If T(A)=I then A fixes each K-standard basis vector, hence A=I; kernels are identical. Inclusion Q->Qbar gives the converse. The number field need not have integral generator entries, and its rational block matrices need not be integral. Finite generation ensures the single finite coefficient-field descent in this proof; Qbar itself does not become a finite-dimensional Q-vector space. Nothing here preserves the original matrix degree.

**Adversarial outcome:** no defect. Original prose says all group matrices include inverses in K, correctly though compactly; no extra inverse-entry assumption is missing.

### Finite-set specialization, with determinant and denominator controls

For rho:G->GL_d(Q(x_1,...,x_r)), choose a single nonzero polynomial h containing entry denominators for generators and their inverses. One may instead use generator denominators plus determinant numerators; inverse adjugates then lie in the same localization. Include each parameter factor when nonzero Laurent coordinates are required. All matrices lie in GL_d(R) for R=Q[x_1,...,x_r,h^{-1}], and all group relations hold in R by its injection into the rational-function field.

For finitely many elements s with rho(s)!=I choose a nonzero entry p_s/h^{k_s} of rho(s)-I. The product P=h product p_s is nonzero. Induction on variables shows some integer tuple a has P(a)!=0: select preceding coordinates keeping a nonzero polynomial coefficient nonzero, then avoid finitely many roots in the last coordinate. Evaluation R->Q is defined and sends generator inverses to actual inverses, so rho_a is a group homomorphism preserving each selected element from the identity. For pairwise injectivity on a finite set, apply this to its finite nonidentity pair differences. This reasoning uses an infinite field and integral-domain polynomial coefficients; it fails over a finite field or after imposing an arbitrary subvariety on parameter tuples.

**Adversarial outcome:** original assertion is correct for unconstrained finitely many rational/Laurent parameters with the stated denominator/determinant avoidance. It does not assert separation on every lower-dimensional locus. The new controls explicitly reject determinant-zero, denominator-zero and zero-Laurent-coordinate tuples, and exhibit a prescribed curve that kills a nonzero witness everywhere.

### Every algebraic specialization of the displayed two-generator representation fails

Put D=diag(x,1), U=[[1,1],[0,1]], x indeterminate. The generated group is exactly M(k,f)=[[x^k,f],[0,1]], k in Z, f in Z[x,x^{-1}]. Multiplication is M(k,f)M(l,g)=M(k+l,f+x^kg). Every such matrix is realized, since U(f)=product_i D^i U^{c_i} D^{-i} for f=sum c_i x^i; the product is finite, i may be negative, and c_i signed integers. Parameterization is unique as rational functions. Thus the inclusion is faithful and identifies this group with the restricted wreath/semidirect structure Z[x,x^{-1}]rtimesZ. It is not a free group on the two displayed generators: conjugate upper translations commute.

For any alpha in Qbar\{0}, evaluation is a homomorphism on the Laurent coefficient ring, with image in Q(alpha). It is **not** a homomorphism from the entire field Q(x), since a nonzero annihilating polynomial p would map to0although invertible in that field. The group matrices use only Laurent denominators, so the restricted evaluation is valid.

Choose nonzero p in Z[x] with p(alpha)=0 by clearing denominators from its rational minimal polynomial. U(p)!=I formally and maps toI. Nonintegral alpha merely changes the leading coefficient from monic to nonmonic; no root/integrality/unit exception arises. Multiplying p by x^j gives signed-index annihilator words as well. Every admissible algebraic alpha therefore gives a nontrivial kernel. Explicitly, kernel={(k,f):alpha^k=1 and f(alpha)=0}. For non-roots of unity, k=0 in the kernel; for an order-mroot of unity, D^m is an additional kernel element. Alpha=0is excluded because D is singular and x^{-1}has no value. For transcendental nonzero alpha, this Laurent evaluation and the exponent map are injective, so the displayed representation remains faithful over its transcendental coefficient field.

**Adversarial outcome:** original proof is valid universally, including rational fractions, algebraic units/nonunits, roots of unity and negative indices. It correctly restricts the conclusion to this representation. No braid-specific conclusion follows. The audit does not attempt to determine whether the example group has some different rational representation.

### Countability and finite dimensionality

For a countable group, all-word identity loci form a countable union of proper algebraic loci (after admissibility exclusions). Qbar is countable too; such a union can cover it. In this example all nonzero algebraic parameters are covered by zero sets of the countably many integer annihilating polynomials realized as translations. Therefore “each finite set can be separated” and “one parameter separates all words” cannot be interchanged. This is no claim that a countable union must always exhaust the algebraic parameters. Nor does the argument deny the availability of real/transcendental generic points.

A family of rational representations with trivial joint kernel gives a map into a product. If the family is infinite, no finite dimension has been established. The example gives a stronger exact diagnostic: for any finite collection of algebraic parameter specializations, U(product_j p_j) is nonidentity formally yet killed by all of them. Thus no finite direct product of those particular specializations is faithful. This is validation of the partial mechanism, not a new attempt at the braid target.

## Computations and reproduction

Original `verify.py` and `review/independent_checks.py` were read and replayed unmodified in `tmp/pr26_specialization_replay`, using the existing repository environment with SymPy1.14.0. Both exited0and reproduced adjacent historical receipts byte for byte. Original author receipt has11conjugation identities and5annihilator examples plus low-strand identities; reviewer receipt has35assertions. The historical reviewer script SHA256 is `b5e407e45511403cb5875e81ffbc2cce5f6b30f4c74dde7531f808ed121d6608`. Current replay is checkable evidence of present reproducibility, not proof of when a past run occurred, what model ran it, or its historical independence.

New `independent_controls.py` does not import SymPy or original scripts. It uses Python's exact Fraction arithmetic, Laurent dictionaries, companion matrices and rational Gaussian elimination. **144assertions PASS.** The mechanisms include:

- nonmonic rational/quadratic annihilators, cubic nonunits, fifth/fourth roots of unity, quadratic units, alpha=+-1, each with four positive/negative Laurent shifts;
- whole-field Q(x)evaluation rejection, a nonannihilating Laurent word that survives, and symbolic nonzero/transcendental boundary;
- a nonempty freely reduced commutator word that isIin this semidirect group, rejecting the false-free-group inference;
- nontrivial joint kernels for a finite direct product of different parameter specializations;
- degrees2,3,4restriction blocks, nonintegral coefficients, generator inverses and signed word powers, multiplication and identity reflection;
- multivariable rational coefficient specialization with exact nonidentity commutator, denominator/determinant/Laurent invalid-point rejection, imposed-curve failure, and finite-field failure of the infinite-field avoidance principle.

These computations are exact; floating-point tolerance and numerical conditioning do not enter. Samples illustrate/falsify boundary inferences; the universal claims rest on proofs, not144finite checks. Reproduce from repository root:

```text
python3 draft_pr_publication_program_20260930/audits/pr26_10400115/specialization_family/independent_controls.py --receipt tmp/pr26_specialization_controls_replay.json
```

Historical receipt, head/manifests, source hashes and independent receipt are separately preserved. No tests were added to canonical attempts and no historical receipt was overwritten.

## Required metadata repairs and optional clarifications

1. **Required:** original `readiness.json.review_hash` is `16717ef9457560e93f7f319a303a38bc2693cf47ed6bd54c70a429f019d60420`, while the frozen final `review/REVIEW.md` hash is `fae44a01605446f34113ffaf30db5f78ad74a136ab71006b1d72c7f5252f1acb`. The review summary correctly points to the latter. Repair the active readiness pointer after preserving original evidence. The unmatched readiness value is not an attestation of the reviewed frozen document.
2. **Required:** PR body says every change is confined to the attempt directory, but QUEUE.md is changed as well. Replace this with accurate scope:14attempt files and the single matching queue status row. The queue content itself is appropriate for the unresolved partial.
3. **Optional exposition:** explicitly name the evaluation's Laurent/localized-ring domain rather than the whole rational-function field, and give the finite number-field inverse argument/negative-index word realization if expanding the note. The original note's scoped proof already supports these details; no mathematical correction is required.

No novel result, full target resolution, or present-day comprehensive literature certification is supported by this audit. The exact remaining gap is a single finite-dimensional algebraic/rational representation of B_n(for unresolved indices) with a proof of injectivity on every braid element, or a universal obstruction across arbitrary finite dimensions and all such representations. Automatic specialization has been rejected; it should stay blocked until a materially new uniform mechanism or primary theorem appears.
