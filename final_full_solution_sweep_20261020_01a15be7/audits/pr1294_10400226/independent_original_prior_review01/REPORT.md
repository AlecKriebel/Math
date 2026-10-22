# Independent original-scope and prior-proof review: PR1294 / 10400226

The full original unrestricted-knot question passes mathematical review. For every integer n>1 with n congruent to 1 modulo 4, the construction produces a tame knot in the three-sphere with determinant n and signature four. Credit belongs to Alper Ferudun's existing unrefereed, AI-assisted preprint, *Knots with Signature 4 and Determinant 4k+1: An Answer to a Question of Shinohara*, Theorem 1.1 and Lemmas 3.1–3.2. This review makes no novelty, earliest-priority, human-refereeing or publication-approval finding.

The exact version DOI is [10.5281/zenodo.23111900](https://doi.org/10.5281/zenodo.23111900). The independently authenticated concept DOI is **10.5281/zenodo.23111899**. A tentative different concept number was not adopted. One qualified existing-publication row is proposed locally, with four literal strings and B exactly blank. Nothing was written to a service.

## Original question, immutable PR and category

The actual publisher [Ohtsuki problem-list PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf) was freshly downloaded, with 4,731,008 bytes and SHA256 `33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd`. Problem 12.21 on printed p.540, physical p.168, attributes the question to Y. Shinohara and asks whether every n=4k+1, k>0, occurs with knot signature 4. The page and surrounding pp.538–541 were read as text, and p.540 was visually inspected. The following remark explains the exclusion of n=1 and older partial restrictions on possible counterexamples. The question imposes no genus, primeness, hyperbolicity, alternatingness or two-bridge condition. Nearby questions with extra knot restrictions are separate questions.

The cache statement SHA256 `51a644c848165cc56e959fb25edb2271ea43c4ebece932e77314003f579ab9bb` agrees with the current catalog digest. The title's truncation does not affect its actual statement. A tame knot realized by an oriented surface in S³ meets the original category; a connected sum is allowed. Either signature convention is covered by mirroring, which changes signature's sign and preserves determinant.

The complete live PR body and all twelve immutable head files were read. Fresh read-only Git-object retrieval binds head `b5ca51999d3dbb901b410e2ab74bfd1671d84dec` and base `5c5d4c9d7a2ea547fdf8a35cf874f604cec27bed`: exactly twelve additions totaling 42,581 bytes, with no QUEUE edit. The live head/base match those pins. Full `PROOF.md` has 7,895 bytes and SHA256 `2be1f719cb6f68b3fef7f9d810a3289c356b36a4992ca02b700b3eb4673b8074`. Historical aggregate-check claims were read as claims; their unavailable historical raw inputs were not invented or described as replayed.

## Actual prior publication and support files

The current [publisher page](https://eulersolve.org/papers/amr-103-0226/), Zenodo record/API and DataCite version and concept records agree on title, Alper Ferudun, Mercury Software GmbH, version 1.0, and publication date 2 October 2026. DataCite marks both DOIs findable and records the reciprocal IsVersionOf/HasVersion relation. The live Zenodo versions endpoint returns exactly one version, record 23111900. These observations authenticate the bounded current publication family; they do not exclude every other possible historical source or package.

All three actual files were freshly downloaded through the archived record with HTTP200, matching both recorded sizes and MD5 checksums:

| Payload | Bytes | SHA256 |
|---|---:|---|
| Source ZIP | 95,868 | `a838f0fcd59184ba3a7f388a7d1c6e62f7914d5e9e98cdb55f1ee3eb148cf699` |
| Verification report | 18,173 | `77f6d786ddb93e332401e9f6fad3bd55f46f5a0f1d9299f23dd1023ed39947fa` |
| Paper PDF | 124,280 | `8db411591685f6793830ee42d86ba2c75f186af70975defb6c1dcb2f9617cbea` |

The PDF has nine pages and matches the PR's primary-paper pin. Actual paper pages 1–4 and 8–9 were read, including the full statement on p.2, realization statement and two-dimensional blocks on p.3, and the full essential proof on p.4. Page 4 was visually inspected. The front matter calls the note unrefereed; p.8 discloses AI assistance and limits its own negative priority search. Those source claims are not replaced by a claim of human peer review here.

Every ZIP entry was read with CRC verification: 46 entries, 41 regular files, 253,393 uncompressed bytes, and `testzip()` returns no bad entry. It contains the manuscript, bibliography, license, report, source programs and recorded outputs; the embedded verification report equals the standalone report byte-for-byte. The full report and reproducibility README were read. Support completeness is verified at the inventory/byte level. Source-author programs were never executed, and their claimed large computations, ancillary lattice route, full determinant/signature classification, explicit knot tables, minimal crossings and stronger realization assertions are not certified by this review.

Direct publisher file mirrors and an attempted AMS download of Shinohara's 1971 paper returned403. The actual archived Ferudun files were obtained and inspected; the 1971 mathematical body was not obtained. The indexed original target is nevertheless directly authenticated in Ohtsuki's publisher PDF. The earlier [Stoimenow publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/83749) was freshly recovered with its PR-pinned SHA256. Its p.383, physical21, independently confirms Question5.1 and the divisor and multiplicative-closure properties. This review does not promote the author's broader historical-search claims into an exhaustive priority judgment.

## Universal argument independently reconstructed

The classical Seifert realization theorem realizes an integral 2g-by-2g matrix V with the requisite unimodular alternating part as the exact Seifert matrix of a knot bounding a genus-g surface. The knot invariants are absolute det(V+Vᵀ) and sign(V+Vᵀ). This exact-matrix assertion is explicitly corroborated in [Friedl's introduction](https://arxiv.org/pdf/0704.3390), p.1; it is separate from that paper's subsequent hyperbolic S-equivalence theorem, which is not used.

The one-component criterion and genus are explicitly corroborated in [Kyushu-hosted knot-theory slides](https://www2.math.kyushu-u.ac.jp/~saeki/Lee-Lectures.pdf), Theorem7.6, physical80, read in text and image. Setting the link-component count to one removes the radical and gives g=(matrix size)/2. Our matrices already have skew part J⊕…⊕J with J=[[0,1],[-1,0]]. Multiplying the second basis vector in each pair by −1 changes J to the slides' opposite sign. This is an integral unimodular basis change, not stabilization or an unsupported change of knot category. No merely rational form or higher-dimensional knot theorem is substituted.

For integers b,c and even y define

```
V(b,c,y) = [[1,1,0,0],
            [0,b,y/2,0],
            [0,y/2,c,1],
            [0,0,0,1]].
```

Its skew part is J⊕J. Its symmetric part S is tridiagonal, with diagonal 2,2b,2c,2 and neighboring entries 1,y,1. Leading minors satisfy

```
D1=2,
D2=4b−1,
D3=2c(4b−1)−2y²,
D4=(4b−1)(4c−1)−4y²=2D3−D2.
```

If b≥1 and D4=n>0, then D2≥3 and D3=(n+D2)/2>0. Sylvester's criterion makes S positive definite, so its determinant is n and its signature is4. Even y is essential for V's integrality.

For a nonsquare admissible n, write n=s²m with m>1 squarefree. All quantities are odd and m≡1 modulo4. Choose an odd prime r dividing m and a nonzero quadratic nonresidue u modulo r. The moduli 4,r,m/r are pairwise coprime, so CRT supplies t modulo4m with t≡3 modulo4, t≡u modulo r, t≡1 modulo m/r. The final modulus1 condition is vacuous when m=r. Thus gcd(t,4m)=1 and the Jacobi symbol (t/m)=−1.

Dirichlet supplies infinitely many primes ℓ in that reduced progression. Exclude the finitely many dividing s; the progression already excludes those dividing m. Consequently ℓ does not divide n and ℓ≡3 modulo4. Quadratic reciprocity, with positive sign because m≡1 modulo4, gives

```
(n/ℓ)=(s²/ℓ)(m/ℓ)=(m/ℓ)=(ℓ/m)=(t/m)=−1.
```

Since (−1/ℓ)=−1, it follows that (−n/ℓ)=1. This final denominator is prime, so there is a nonzero x modulo ℓ with x²≡−n. No square-root inference is taken from a composite-denominator Jacobi symbol. Choose y0 modulo ℓ with 2y0≡x and make y even by adding ℓ if necessary. Then h=(n+4y²)/ℓ is a positive integer congruent to3 modulo4, hence h≥3. Set b=(ℓ+1)/4 and c=(h+1)/4. Both are positive integers, and D4=ℓh−4y²=n. This constructs the required four-dimensional Seifert matrix for every nonsquare n.

If n has a prime divisor ℓ≡3 modulo4, use y=0 and h=n/ℓ. Again h≡3 modulo4, h≥3, and the same b,c work. This includes every square having such a prime divisor, without attempting the nonsquare reduction with m=1.

The remaining case is n=s²>1 with all prime divisors of s congruent to1 modulo4. Choose one such prime p. Since p is nonsquare, its four-dimensional matrix Vp has already been constructed; there is no circular appeal to an unproved square case. Put h=n/p, so h≡1 modulo4 and h≥p≥5. The integral block

```
W(h)=[[-1,1],[0,(h−1)/4]]
```

has skew part J and symmetric determinant −h<0. Its symmetric part has one positive and one negative eigenvalue and signature0. Therefore Vp⊕W(h) has skew part J⊕J⊕J, symmetric determinant **−n**, and signature4. The absolute value in the knot determinant is necessary. Seifert realization supplies the desired knot.

The cases are exhaustive. The constructed surfaces have genus2 in the first two cases and genus3 in the remaining case, so knot genera are bounded above accordingly. This proves the full question for every admissible integer; no finite enumeration supplies the universal quantifier. It does not prove that genus2 suffices for every remaining square, nor that genus3 is necessary. It proves no uniform prime-search bound.

## Standard imports, falsification and exact diagnostics

Dirichlet's reduced-progression statement was freshly authenticated in [Sutherland's MIT Lecture18](https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_lec18.pdf), Theorem18.1 on p.1. Prime reciprocity, Jacobi multiplicativity/reciprocity, the (−1/b) supplement and denominator-one convention were read in the actual [Stanford PBC notes](https://crypto.stanford.edu/pbc/notes/numbertheory/quadrecip.html). The direct Stanford byte download failed; successful web text inspection is recorded without inventing a byte pin. These are explicitly imported classical theorems, as are Seifert realization, CRT and Sylvester's criterion. Their foundational proofs are not claimed newly proved here. All nonstandard steps of the target construction have been independently derived above.

The new `verify_independent.py` uses standard-library integer arithmetic, exact trial-division primality, explicit CRT progression search, separately checked prime square roots, determinant expansion over permutations, and exact rational congruence elimination for inertia. A separate factored Legendre-product calculation checks the Jacobi routine. Its data and code are newly authored, not downloaded author programs or historical raw checks.

All 500 admissible n from5 through2001 and six further distinct cases pass, for **506 inputs**: 481 nonsquares,15 square/divisor cases and10 remaining squares. Another487 checks exercise every available3-mod4 prime-divisor branch. There are10,201 Jacobi-product checks. Eight nonsquare inputs actually require excluding an initial progression prime dividing s; for n=245, s=7,m=5,t=7 modulo20, the initial prime7 must be skipped. This directly challenges the finite-exception clause in Dirichlet's use.

The printed worked example n=33049, b=5,c=437,y=6 has leading minors2,19,16534,33049 and inertia(4,0,0). For n=25 the six-dimensional construction has signed determinant−25 and inertia(5,1,0). Exact mirroring verifies signature−4 with unchanged determinant; an integral basis reversal verifies the opposite alternating-form convention. Additional inertia controls include a zero-diagonal hyperbolic plane and a degenerate zero form.

Normal, `-O`, and `-OO` output hashes agree exactly: `6df7deb1a68cd7f6ff4c1225adb09cbea8452b85fcf56026ff7f9cedfb15df27`. Seventeen deliberately false inputs/conclusions are rejected per mode,51 total: forbidden n, odd y, wrong W congruence, noncoprime CRT moduli, composite-Jacobi square-root inference, omission of the prime-divisor exclusion, loss of the absolute determinant, false genus-two inference, altered skew entry, wrong signature sign and false positive definiteness and omission of b≥1. In the latter countercontrol b=0,c=−1,y=0 gives positive determinant5 but inertia(2,2,0), showing why the b hypothesis matters. In particular Jacobi(2,15)=1 while2 is not a square modulo15. Explicit exception guards remain active under optimization. No floating-point eigenvalue or feasibility authority is used.

## Accounting recommendation and remaining limits

The fresh mandatory numeric-gid read-only ledger check preceded substantive mathematics at10:25:29 UTC:191 nonempty rows and43 columns. No target ID, source problem number or solution DOI matches. The broad Shinohara response-row180 concerns the different Bannai–Koike–Shinohara–Tagami modular-form problem30000160/161, DOI23071924. Ohtsuki response-row28 concerns the distinct SU(5) lens-space conjecture AMR-103-0120, DOI23174156. Broad author/site keywords alone do not establish duplicates.

A fresh repository-release inventory and bounded local exact-alias search are recorded in `source_and_package_receipt.json`. Same-publication version/concept/site aliases should be treated as one credited paper. The proposed row records the complete original conclusion, genus bounds, actual archived payload verification, named standard imports and unrefereed/AI-assisted status. These checks do not prove that no other package or earlier mathematical argument exists. The source itself notes a possible classical lattice route; that sketch is outside this acceptance, so no earliest-priority conclusion follows.

There is **no unresolved mathematical dependency for the stated construction**, subject to the explicitly imported standard theorems. Remaining limits are external human/formal review, the inaccessible1971 historical paper, unreplayed source software and excluded ancillary results. All code and artifacts authored for this review are checkable; copied source/ledger bodies stay private. The final seal covers those private files and every nested manifest. The assigned audit is complete; the parent sweep remains80%. No service write, new publication, DOI action, Git mutation, merge, CASE/readiness change or external contact occurred.
