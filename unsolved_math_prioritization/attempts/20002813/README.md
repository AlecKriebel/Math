# Canonical products for the standard algebra-group supercharacter theory

Problem 20002813 / AIM-REPRESENTATION_THEORY-0085. AI-assisted proof exposition and separate mathematical audit, 11 October 2026.

## Accepted result and limits

For every finite-dimensional associative nilpotent algebra J over every finite field F_q, the canonical degree-weighted supercharacter of each two-sided orbit in J* is its unnormalized additive Fourier orbit sum. The pointwise product of two such canonical supercharacters has nonnegative integral coefficients. Each coefficient counts additive decompositions of one fixed functional in the target orbit, and the count is constant on that orbit.

This settles the standard two-sided-orbit algebra-group subcase asked about in the remark to AIM Problem 1.1. The general classification of supercharacter theories with this property remains unresolved by this work. Arbitrary supercharacter theories on the same algebra group, induction products, and Hopf multiplication are outside the theorem. The conventional prefactor-normalized supercharacter is generally distinct from the canonical degree-weighted one. No novelty or first-resolution claim is made.

The foundational construction is credited to Persi Diaconis and I. M. Isaacs, [Supercharacters and superclasses for algebra groups](https://doi.org/10.1090/S0002-9947-07-04365-6), Transactions of the AMS 360 (2008), 2359–2392. The original target is [AIM, Supercharacters and Combinatorial Hopf Algebras, Problem 1.1](https://aimath.org/WWN/supercharacters/supercharacters.pdf), workshop 17–21 May 2010, edited by Carolina Benedetti.

## Complete proof and review

1. [Canonical product proof](ALGEBRA_GROUP_CANONICAL_PRODUCT.md): full theorem, canonical normalization derivation, fixed-target decomposition formula, and boundary checks.
2. [Separate mathematical audit](AUDIT.md): full mathematical challenge audit, source normalization warning, exact finite-field scope, source read limits, and diagnostic summary.
3. [Acceptance report](ACCEPTANCE.md) and [machine-readable acceptance](ACCEPTANCE.json): PASS for the restricted standard-theory theorem, with exact public artifact hashes.
4. [Source verification](SOURCE_VERIFICATION.json), [exact editorial map](EDITORIAL_MAP.json), and [closed public manifest](PUBLIC_MANIFEST.json).

## Normalization corroboration and source boundary

Diaconis–Thiem, [Supercharacter formulas for pattern groups, arXiv:math/0610161v1](https://arxiv.org/pdf/math/0610161v1), Section 2.3, PDF pages 6–7, supplies the conventional orbit prefactor and disjoint irreducible supports. Its page 7 unweighted regular-sum wording is excluded from the proof's dependencies. The proof instead derives the correct regular-character identity directly for unnormalized Fourier orbit sums.

The audit additionally inspected Eric Marberg, [Iterative character constructions for algebra groups, arXiv:1012.2191v2](https://arxiv.org/pdf/1012.2191v2), dated 13 January 2012. Section 2.3, equations (2.2)–(2.3), PDF pages 5–6, corroborates the conventional prefactor and correctly weighted regular-character decomposition. Section 2.2 on page 5 also records equality of the one-sided orbit sizes. This supplementary citation is outside the preserved proof region and implements the audit's nonblocking recommendation.

The direct Diaconis–Isaacs publisher PDF was unavailable with HTTP 403, and no inspected direct copy was obtained. No PDF hash, inspection claim, or unverified product-theorem number is assigned to that unavailable source. Source verification records actual retrieval and inspection history; preparation of this edition rehashes retained files and does not claim new full-paper inspections.

## Verification and publication scope

The symbolic proof applies to all prime powers, including nonprime fields and characteristic two, and also to the trivial algebra. Exact finite diagnostics for UT3 over F2, F3 and F4 passed all 507 orbit products and 26,571 pointwise identities. These counts are supplemental verification metadata; the general theorem does not rest on them. The diagnostic programs and raw tables are excluded, and this edition does not rerun them.

The exposition and separate audit are AI-assisted. “Independent” refers to a separate mathematical check, not external human peer review, journal acceptance, formal proof-assistant certification, or a literature-priority determination. The complete mathematical proof and core audit regions are unchanged under the recorded editorial transformation. Only authored mathematical material, acceptance reports, public citations, and verification metadata are included. Copied source documents or extracts, source images, datasets, raw programs or certificates, and private coordination material are excluded.
