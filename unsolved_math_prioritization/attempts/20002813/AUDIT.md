# Independent AI-assisted audit of canonical algebra group supercharacter products

Date: 11 October 2026 UTC. Problem 20002813 / AIM-REPRESENTATION_THEORY-0085.

## Verdict

**PASS for the stated standard two-sided-orbit supercharacter theory of every finite algebra group.** The submitted proof correctly identifies the canonical degree-weighted character with the unnormalized additive Fourier orbit sum and obtains nonnegative integral pointwise multiplication coefficients by counting decompositions of a fixed functional. No mathematical correction to the submitted argument is required.

This is an affirmative answer to the algebra-group specialization in the remark to AIM Problem 1.1, under the usual interpretation of its natural characters as the standard Diaconis–Isaacs theory. It is not a classification of all finite-group supercharacter theories, nor a result about every supercharacter theory on an algebra group. It is a direct consequence of the established orbit construction; this audit does not establish novelty or a first-resolution date.

The audited input is `ALGEBRA_GROUP_CANONICAL_PRODUCT.md`, SHA-256 `cd8d70495e842559f2d2a82aff32a60ba612d4521099dbf9ab3b38840250b559`, 6,238 bytes. The input was preserved. EDITORIAL_MAP.json records the exact public-edition transformation. This mathematical review is AI-assisted; it is not external human peer review, journal acceptance, or formal certification.

## Exact question and scope check

AIM's *Supercharacters and Combinatorial Hopf Algebras*, edited by Carolina Benedetti, records the workshop of 17–21 May 2010. Problem 1.1 is on PDF page 1. It specifies the degree-weighted normalization

\[
\sigma_X=\sum_{\chi\in X}\chi(1)\chi
\]

and asks when products in this basis have integer nonnegative coefficients. Its accompanying remark asks whether this property holds for the natural characters associated to algebra groups. This is the specialization answered here. The general question and its other suggested families remain outside the submitted theorem.

The product in this question is multiplication of class functions on one fixed finite group, equivalently the character of a tensor product of two representations of that same group. There is no induction product, superinduction, sequence of groups, or Hopf-algebra multiplication in the argument. The word “positive” is understood to allow zero coefficients for absent basis elements; multiplication by the trivial character alone makes the need for this convention clear.

The original PDF confirms the canonical character formula, problem number, and algebra-group remark. The accepted theorem resolves this standard algebra-group subcase; the broader classification remains outside this audit.

## Accepted theorem

Let \(J\) be a finite-dimensional associative nilpotent algebra over an arbitrary finite field \(\mathbb F_q\), and let \(G=1+J\). Fix any nontrivial additive character \(\theta:\mathbb F_q^+\to\mathbb C^\times\). Put \(J^*=\operatorname{Hom}_{\mathbb F_q}(J,\mathbb F_q)\). For a two-sided orbit \(O\subseteq J^*\), let \(X_O\) be its block of irreducible characters in the standard algebra-group supercharacter theory.

Then

\[
\sigma_O(1+x)
=\sum_{\chi\in X_O}\chi(1)\chi(1+x)
=\sum_{\lambda\in O}\theta(\lambda(x)).
\]

For orbits \(O,P,R\) and any fixed \(\nu\in R\), define

\[
m_{O,P}^{R}=\#\{(\lambda,\mu)\in O\times P:\lambda+\mu=\nu\}.
\]

This count is independent of the chosen representative \(\nu\), and

\[
\sigma_O\sigma_P=\sum_R m_{O,P}^{R}\sigma_R,
\qquad m_{O,P}^{R}\in\mathbb Z_{\ge0}.
\]

The coefficient counts decompositions of **one fixed element** of \(R\). It is not the total number of pairs whose sum lies somewhere in \(R\); that larger count is \(|R|m_{O,P}^{R}\).

## Independent proof audit

### Algebra and dual identification

Nilpotence makes \(1+x\) invertible by a finite geometric series, and associativity gives the group law \((1+x)(1+y)=1+x+y+xy\). The bijection \(J\to G\), \(x\mapsto1+x\), identifies the counting measures, not their group laws.

Define \(e_\lambda(1+x)=\theta(\lambda(x))\). These are additive-group characters of \(J\) pulled back to the underlying set of \(G\). They need not be ordinary linear characters of \(G\), and the proof does not assume that they are.

For distinct \(\lambda,\mu\), the nonzero \(\mathbb F_q\)-linear map \(\lambda-\mu:J\to\mathbb F_q\) is surjective. Its composite with nontrivial \(\theta\) is therefore nontrivial. Thus the map from \(J^*\) to the additive character group of \(J\) is injective. Both sets have size \(|J|\), so it is bijective. Additive Fourier orthogonality gives

\[
\langle e_\lambda,e_\mu\rangle_G=\delta_{\lambda,\mu}.
\]

This argument works for every prime power. It never requires \(\theta\) to be injective on \(\mathbb F_q^+\), an invalid requirement when \(q\) is a nonprime prime power. Equivalently, one may use a nonzero trace character. The case \(J=0\) is also covered.

### Conventional and canonical normalization

Write \(F_O=\sum_{\lambda\in O}e_\lambda\). The standard conventional character is

\[
\tau_O=\frac{r_O}{|O|}F_O,
\qquad r_O=|\lambda G|.
\]

Diaconis–Thiem, Section 2.3, supplies this formula and the assertion that every irreducible character belongs to the support of exactly one distinct conventional supercharacter. These are established inputs from the standard theory, not consequences of Fourier orthogonality alone. Indexing by distinct orbits, rather than by all individual functionals with repetition, is essential.

The Fourier identity is

\[
\sum_O F_O(1+x)=\sum_{\lambda\in J^*}\theta(\lambda(x))
=\begin{cases}|G|,&x=0,\\0,&x\ne0.\end{cases}
\]

Hence \(\sum_O F_O=\rho_G\), the regular character. Each \(F_O\) is a positive scalar multiple of the character \(\tau_O\) and has precisely its irreducible support. In the expansion of \(\rho_G\), a fixed irreducible \(\chi\) has coefficient \(\chi(1)\). Only the single \(F_O\) whose support contains \(\chi\) can contribute that coefficient. It follows that the coefficient of \(\chi\) in this \(F_O\) is exactly \(\chi(1)\). Therefore \(F_O=\sigma_O\).

There is no circular assumption that a rational rescaling of a character is again a character with integral multiplicities: integrality and the precise multiplicities follow from the regular-character comparison. The disjoint-support hypothesis prevents cancellation or mixing between different orbit blocks.

In particular,

\[
\sigma_O(1)=\langle\sigma_O,\sigma_O\rangle_G=|O|,
\quad
\tau_O(1)=r_O,
\quad
\langle\tau_O,\tau_O\rangle_G=r_O^2/|O|.
\]

Thus \(c_O=\langle\tau_O,\tau_O\rangle_G/\tau_O(1)=r_O/|O|\), as the submission states. This is a check on the canonical identity, not a replacement for its proof.

Some primary references use \(|G\lambda|\) instead of \(|\lambda G|\). The sizes agree: the two one-sided orbit dimensions are the equal row and column ranks of the bilinear form \((x,y)\mapsto\lambda(xy)\). The inversion map on \(G\) ranges over all \(1+J\), so these orbits are translates of the corresponding linear images. There is no normalization conflict from this notational choice.

### Two-sided linear transport

For \(g,h\in G\), define

\[
(T_{g,h}\lambda)(x)=\lambda(g^{-1}xh^{-1}).
\]

The map on \(J\) inside this evaluation is well-defined, invertible, and \(\mathbb F_q\)-linear. Therefore \(T_{g,h}\) has the same properties on \(J^*\). The set of these transformations is closed under composition and inversion. The convention for the right factor can be described using the opposite group; the proof uses only this set of invertible transformations and its orbits.

If \(\nu'=T_{g,h}\nu\), simultaneous application to both entries gives the bijection

\[
(\lambda,\mu)\longmapsto(T_{g,h}\lambda,T_{g,h}\mu)
\]

between decompositions of \(\nu\) in \(O\times P\) and those of \(\nu'\) in \(O\times P\). Each input orbit is preserved and linearity preserves the sum. The inverse transformation gives the inverse bijection. Thus the decomposition count is constant on the full target orbit, not merely on a conjugacy orbit or a smaller subset.

### Product calculation and integrality

The additive-character identity \(e_\lambda e_\mu=e_{\lambda+\mu}\) holds pointwise on \(G\), regardless of its nonabelian group law. Consequently

\[
F_OF_P=\sum_{\nu\in J^*}
\#\{(\lambda,\mu)\in O\times P:\lambda+\mu=\nu\}\,e_\nu.
\]

Grouping by two-sided orbits gives \(F_OF_P=\sum_Rm_{O,P}^{R}F_R\). Substituting the proved identity \(F_R=\sigma_R\) completes the result. Every coefficient is an actual finite cardinality. No unproved divisibility condition, computational pattern, generic characteristic assumption, or conventional-basis product theorem is needed.

### Boundary checks

- The zero orbit is \(\{0\}\), with \(\sigma_{\{0\}}=1_G\). Its product with \(\sigma_O\) is \(\sigma_O\).
- Negation commutes with all two-sided transformations, so \(-O\) is an orbit. The coefficient of the zero orbit in \(\sigma_O\sigma_P\) is \(|O|\) when \(P=-O\), and zero otherwise. This agrees with Fourier orthogonality and complex conjugation.
- At the identity the formula gives \(|O||P|=\sum_Rm_{O,P}^{R}|R|\), which also directly partitions all input pairs.
- The proof covers characteristic two, arbitrary extension fields, and the trivial algebra.
- Arbitrary supercharacter coarsenings or refinements of an algebra group are not covered merely because the underlying group is an algebra group.

## Source hygiene and attribution

The Diaconis–Thiem preprint's page 7, item (a), describes an unweighted regular-character sum in wording incompatible with the conventional prefactor displayed on that page. The submission correctly avoids using this assertion. For \(UT_3(\mathbb F_2)\), four conventional characters have degree 1 and one has degree 2, so their unweighted degree sum is 6, whereas the regular character has degree 8. The canonical characters instead have degrees 1,1,1,1,4 and sum to the regular character. This is a concrete normalization diagnostic.

The foundational construction should be credited to Persi Diaconis and I. M. Isaacs, *Supercharacters and superclasses for algebra groups*, Transactions of the AMS 360 (2008), 2359–2392, DOI [10.1090/S0002-9947-07-04365-6](https://doi.org/10.1090/S0002-9947-07-04365-6). The publisher PDF was unavailable with HTTP 403 in the source acquisition and this follow-up. No direct inspection or byte hash of that PDF is claimed. The inspected Diaconis–Thiem paper explicitly attributes its orbit construction and conventional tensor-product closure to that work. This audit does not assign an unverified Diaconis–Isaacs theorem number to the canonical pair-count formula.

A further primary corroboration is Eric Marberg, *Iterative character constructions for algebra groups*, arXiv:1012.2191v2, Section 2.3, equations (2.2)–(2.3), PDF pages 5–6. It states the conventional orbit normalization and gives the correctly weighted regular-character decomposition. The exact inspected bytes and pages are recorded in the companion source manifest. This reinforces the normalization argument; the canonical product formula is independently derived above.

The theorem should be described as a source-grounded elementary consequence of standard algebra-group supercharacter theory. No priority claim or general statement that the whole 2010 problem has been solved follows from this audit.

## Exact finite stress tests

An independently authored, self-contained Python script checks \(UT_3(\mathbb F_q)\) for \(q=2,3,4\). It uses no downloaded software or numerical character approximations. For \(\mathbb F_4\), it constructs \(\mathbb F_2[t]/(t^2+t+1)\) and uses the trace character; for \(\mathbb F_3\), values are exact coefficient vectors in \(\mathbb Z[\zeta_3]\).

The script constructs two-sided orbits from the inverse left/right actions, enumerates every input-orbit pair, verifies constancy of each target-orbit count, and checks the product equality at every group element. It also checks the additive-dual bijection, the regular-character identity, conventional norms, identity degrees, and zero-orbit coefficients.

The verification metadata covers field sizes 2, 3 and 4. Aggregate pass counts are recorded below; raw computational tables and programs are not reproduced.

All 507 orbit products and 26,571 pointwise identities pass in exact arithmetic. These computations are falsification checks for representative examples, not a substitute for the general proof and not a claim to compute arbitrary irreducible character tables.

## Acceptance and remaining limits

There are no blocking mathematical findings. The following presentation requirements should accompany any accepted version:

1. Keep the standard two-sided-orbit theory and arbitrary finite-field hypotheses explicit.
2. Keep the canonical basis distinct from the conventional prefactor-normalized basis.
3. Define a structure coefficient using one fixed target functional.
4. Credit the established orbit construction and make no novelty claim.
5. Treat this as a proved algebra-group subcase of the broader problem.
6. Retain the honest direct-inspection limitation for Diaconis–Isaacs; prefer the inspected weighted identity when adding corroborating sources.

The input already satisfies the first five requirements and discloses the sixth limitation. Adding Marberg as corroboration is recommended, not required for validity. The README supplies this corroborating citation without changing the accepted proof.

## Source and inspection pins

1. AIM problem list: [public PDF](https://aimath.org/WWN/supercharacters/supercharacters.pdf), 53,794 bytes, SHA-256 `b25dad747e4e42f81db9346826caf0de42d54800c612e59d1031b0fafd48105c`. Version: workshop 17–21 May 2010; no separate revision date printed. Retrieved in the supplied source screen at 2026-10-11T19:37:34.156856Z. PDF page 1 was rendered and visually inspected afresh in this audit; it contains Problem 1.1 and the algebra-group remark.
2. Persi Diaconis and Nathaniel Thiem, *Supercharacter formulas for pattern groups*: [arXiv PDF v1](https://arxiv.org/pdf/math/0610161v1), 271,277 bytes, SHA-256 `e351061ff641525350cd80d945d2cd7d32bba3673fbc7de60513d0ec2c0af430`. The supplied unversioned retrieval resolves to bytes carrying the v1 stamp dated 4 October 2006. Retrieved in the source screen at 2026-10-11T19:37:41.003592Z. PDF pages 6–7 were visually inspected for the standard-theory scope, action, prefactor, support assertion, and the excluded regular-sum wording. The title/version and bibliography attribution were also checked in extracted text.
3. Eric Marberg, *Iterative character constructions for algebra groups*: [arXiv PDF v2](https://arxiv.org/pdf/1012.2191v2), 273,349 bytes, SHA-256 `ab79e486d056a94ef945c3435061de422e43872a47190400ec6d97a3f6203916`. Retrieved on 11 October 2026 UTC. PDF pages 1, 5 and 6 were visually inspected: the title and version stamp identify v2 dated 13 January 2012; Section 2.3 equations (2.2)–(2.3) supply the normalization and weighted regular-character identity. Section 2.2, on page 5, also expressly records equality of the one-sided orbit sizes.

SOURCE_VERIFICATION.json records exact PDF hashes and sizes, inspection history, and access limitations. Source PDFs, extracted text, and inspection images are not reproduced. No entire proof of any cited paper was re-audited.
