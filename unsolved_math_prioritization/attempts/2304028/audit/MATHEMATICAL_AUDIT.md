# Independent mathematical and reproducibility audit

Problem 2304028 / AMR-022-4028, rank 1033. Audit date: 2026-10-08 UTC.

## Decision

**ACCEPT — KNOWN-SOLVED, with zero new proof-search approaches.** The existing theorem settles both parts of the target for every nonlinear real polynomial. The inspected report correctly distinguishes imported universal mathematics, independently checkable local algebra, and finite implementation tests. No mathematical correction or replacement proof is required. No claim of novelty is justified or made.

This decision applies to the four original public files identified below and the external manifest with SHA-256 `b76dfab10d985100f7dc23854491ee83dddd6364a1eb8dee2fb7dc5ceeb22000`. All four files were read in full and independently hashed before executing the verifier. The originals were preserved byte-for-byte. Nothing was published, no queue was edited, and no authors were contacted during this audit.

## 1. Exact target and literature disposition

The target asks about a polynomial P with real coefficients and degree d at least two: first, existence of a nonreal zero of Q=P²+P′, and second, a lower bound of d−1 nonreal zeros. It does not restrict the sign of the leading coefficient, assume that P has real roots only, or require its roots to be simple. The original wording does not separately specify whether repeated zeros are counted once or according to multiplicity; the available distinct-root result resolves both readings.

The primary compilation’s [Problem 4.28 and Update 4.28](https://arxiv.org/html/1809.07200) were checked against the target. The update identifies Sheil-Small’s solution and Eremenko’s alternative argument. The displayed version is arXiv:1809.07200v2, dated 21 September 2018. Thus retaining only the earlier real-rooted special case would misstate the recorded literature status.

The decisive published source is Bergweiler, Eremenko and Langley, [Zeros of differential polynomials in real meromorphic functions](https://doi.org/10.1017/S0013091504000690), Proceedings of the Edinburgh Mathematical Society 48 (2005), 279–293. Its Theorem A supplies d−1 distinct nonreal zeros of Q that are not roots of P. Substituting P meets every hypothesis, including when P has repeated roots. This directly settles the target.

The bibliographic identity of Sheil-Small’s 1989 paper was checked against the [Annals publisher record](https://annals.math.princeton.edu/1989/129-1/p07): volume 129, pages 179–193, DOI 10.2307/1971490. Its original full proof is not claimed to have been inspected. Attribution is supported by the compilation and the later published theorem.

### Version and provenance checks

- The journal’s relevant numbering is Theorem A on page 279, Lemma 2.1 on page 282, and the proof of Corollary 1.1 on pages 282–283.
- The [2004 author manuscript](https://www.maths.nottingham.ac.uk/plp/pmzjkl/PAPERS/realz-edin.pdf) uses Theorem A, Lemma 10, and Corollary 1. Its title page dates it 14 October 2004. Its theorem agrees with the published statement; its numbering must not be represented as journal numbering.
- The corroborative [Wiman manuscript](https://www.math.purdue.edu/~eremenko/dvi/bel4.pdf) is explicitly dated **25 July 2002** on its first page. The final metadata correctly records that manuscript date. It is corroboration only; no journal-year inference is substituted for the date actually displayed.
- The recorded source-document byte counts and SHA-256 digests were independently recalculated from the retained inspected bytes and all matched. Official public endpoints were also reopened to check identity and the relevant statements. This is not a claim that a second raw-byte HTTP download was obtained for every artifact.
- The published theorem and proof page images were inspected, and page 282 was independently rendered and inspected for the dynamical lemma. Source documents and rendered pages are excluded from the public audit slice.

## 2. Imported mathematics versus independent checks

Two universal results remain explicitly imported: Theorem A, which alone suffices for the classification, and the rational-map case of the Fatou/Leau-domain lemma used in the report’s alternative exposition. Neither is proved by finite testing.

The imported dynamical input gives μ−1 disjoint invariant attracting domains at a parabolic fixed point of multiplicity μ, one limiting direction per domain, with equally spaced directions; each domain contains a critical value in the rational case. The published Lemma 2.1 is the source. The following application and algebra have been independently checked rather than assumed from a numerical experiment.

### 2.1 Rational-map degree and infinity

Set F(z)=z−1/P(z)=(zP(z)−1)/P(z). A common divisor of zP−1 and P divides 1, so there is no cancellation. The numerator has degree d+1 and the denominator degree d. Therefore the rational map has degree d+1, hence is nonlinear.

Write A(w)=w^dP(1/w); its constant coefficient is the nonzero leading coefficient of P. In the local coordinate w=1/z, direct simplification gives

G(w)=1/F(1/w)=wA(w)/(A(w)−w^(d+1)),

G(w)−w=w^(d+2)/(A(w)−w^(d+1)).

Because the denominator is nonzero at w=0, the zero of G−w has order exactly d+2. This is the fixed-point multiplicity at infinity. It is not d, d+1, or the rational-map degree. Separately, G′(0)=1, so infinity has local degree one and is not a critical point. The distinction between fixed-point multiplicity and local mapping degree is handled correctly.

### 2.2 Why domains give distinct nonreal critical points

There are d+1 directions and at most two lie on the real axis. At least d−1 domains consequently have a nonreal limiting direction. A real point cannot lie in any such domain: F preserves the extended real line, so every defined forward iterate of a real point is real or infinity, incompatible with that limiting direction. A domain does not contain the parabolic fixed point, which lies on its boundary.

Choose a critical value from each of these d−1 domains. They are finite, nonreal, and distinct because the domains are disjoint. Choose a critical preimage for each chosen value. Different values cannot have the same preimage. A real preimage is impossible because F is real. A root of P is a pole of F and has value infinity, so it cannot be one of these preimages. Infinity is likewise excluded.

At each selected finite point c with P(c) nonzero,

F′(c)=1+P′(c)/P(c)²=Q(c)/P(c)².

Thus these are distinct nonreal zeros of Q outside the zeros of P. This step needs critical **values**, followed by the preimage argument; it does not silently assume that a critical point is located in the same domain as its value. No unproved assertion about counting critical points with multiplicity is being used.

This yields the universal lower bound conditional on the imported Fatou lemma. It is a checked exposition of existing mathematics, not a new independent discovery.

### 2.3 Shared roots and repeated-root contract

At any root a of P of multiplicity m≥1, write t=z−a and P=t^m u with u(a) nonzero. Product differentiation gives

Q=t^(m−1) [m u+t u′+t^(m+1)u²].

At t=0, the bracket equals m u(a), which is nonzero in characteristic zero. The multiplicity in Q is therefore exactly m−1. For m=1 this says a is not a root of Q. For m>1 it identifies every shared root and its exact multiplicity, including nonreal repeated roots. The theorem’s outside-P count avoids all these shared roots, so shared multiplicity cannot mask a deficient distinct-root count.

Also deg Q=2d: P² contributes a nonzero leading coefficient in degree 2d, whereas P′ has degree d−1. There is no leading-term cancellation.

### 2.4 Conjugation and exact sharpness

Since Q has real coefficients, nonreal roots occur in conjugate pairs with equal multiplicity. Both the distinct count and the multiplicity-weighted nonreal count are even. The theorem’s d−1 bound thus strengthens to 2 floor(d/2): d−1 when d is odd, and d when d is even.

For P=−z^d, exact differentiation gives

Q=z^(d−1)(z^(d+1)−d).

Every root of the second factor is nonzero and simple, because its derivative is (d+1)z^d. If d is odd, d+1 is even and this factor has exactly the two real roots ±d^(1/(d+1)); the other d−1 roots are nonreal. If d is even, d+1 is odd and there is exactly one real root; the other d roots are nonreal. The zero of order d−1 at the origin is real. This attains the parity-adjusted lower bound for every degree under both counting conventions.

Boundary examples are also correct: P=−z is linear and gives z²−1 with no nonreal roots; the rational function P=1/z² gives (1−2z)/z⁴ with only one finite zero, which is real. Neither contradicts the stated nonlinear-polynomial theorem. No extension to rational or complex-coefficient inputs has been accepted.

## 3. Independent reconstruction of the finite verifier

The input ledger has 24 authored cases: 22 nonlinear cases and two linear boundary cases. There are positive and negative monomials in degrees two through eight, other low-degree examples, repeated real roots, repeated nonreal roots, and a mixed repeated-root example.

The verifier’s arithmetic uses Python Fraction values, polynomial long division, monic Euclidean gcd, and exact Sturm sign variation at ±infinity. The squarefree quotient Q/gcd(Q,Q′) contains each zero once. Dividing that squarefree polynomial by its gcd with P removes all shared zeros exactly once. For a squarefree real polynomial, degree minus the exact real-root count is the distinct nonreal count.

The multiplicity-weighted real count is recovered through successive gcd layers: a root of multiplicity m appears in exactly m layers. The chain strictly loses multiplicity until a nonzero constant remains. Constant squarefree polynomials correctly have zero real roots. The Sturm chain uses the negative remainders and the signs of leading terms at both infinities, with zero entries omitted when counting changes.

I separately reconstructed all six expected values for every case using exact rational real-root isolation on Q itself, squarefree-factor degrees, and root counts for the shared gcd. This agreed in all 24 cases. I also independently checked shared-factor exponents drop by one, the no-cancellation identity, and the inverse-coordinate identity for every case. SymPy 1.14.0 was used for this second exact reconstruction. It shares the author’s oracle library, so it is not advertised as a third independent computer-algebra implementation; the standard-library Fraction/Sturm verifier remains a separate implementation.

No floating-point roots or tolerance-based classifications were used. These tests are finite implementation evidence only. The published universal theorem, not the finite examples, decides KNOWN-SOLVED.

## 4. Replays, malformed inputs, and trust boundaries

The author’s replay script was run from a separate copy. Its complete JSON receipt reproduced identically: three successful runs and 72 rejected runs. All successful runs reported 24 finite cases and 25 internal rejection controls.

A separately authored reviewer harness reconstructed the same 24 negative scenarios and three optimization modes, again obtaining **3 positive and 72 negative runs**. It then added **6 positive and 126 negative runs**. Across the reviewer harness, that is nine successful and 198 rejected executions. The additional successful fixtures use degree nine and coefficient magnitude 1,000,000 with both signs; they are test-only, newly pinned fixtures and do not alter the production ledger or its pin.

Every replay ran with actual UID=EUID=1000 under Python 3.12.14. Four attempted writes to the frozen payload, its manifest, and the hostile directory were denied by permissions. The positive runs used a read-only payload, `-I -B`, and a hostile working directory and environment containing replacement standard-library module names and Python startup settings. Normal, `-O`, and `-OO` runs all agreed. The non-isolated invocation rejected before importing the replaceable modules.

### Type, schema, and numerical attacks

The original 25 internal rejection controls consist of ten invalid scalar values, eleven invalid polynomial encodings, and four invalid JSON encodings. Exact `type(value) is int` checks exclude bool, integral floats, fractions, strings, nulls, and containers. JSON duplicate keys and explicit NaN/infinity constants are rejected. Unknown and missing keys, bad or duplicate identifiers, case-count changes, leading zero coefficients, and out-of-scope degrees or coefficient magnitudes are rejected.

The reviewer additionally exercised false booleans, fractional coefficients, nulls and objects, negative bounds, a 1001-digit integer, both signs of exponent overflow, floating underflow and negative zero, an integer exceeding Python’s parser digit limit, empty and constant polynomial arrays, missing/extra/nontyped expectation objects, and malformed manifest fields. Manifest attacks included traversal names, invalid hash types/case, invalid byte counts, duplicate members/keys, a manifest symlink, and an unlisted directory. Every negative execution failed as intended.

There is no fixed-width arithmetic overflow path in the polynomial computation: integers and Fractions use arbitrary-precision arithmetic, and accepted coefficient magnitudes and degrees are bounded. Float exponent overflow produces a float and is rejected by exact integer validation, rather than being misclassified as an integer. Optimization cannot erase the checks because the delivered verifier uses explicit exceptions rather than assertions.

### Integrity and provenance boundaries

The original external manifest digest stayed fixed. Re-pinning is used only for deliberately modified test fixtures, so semantic rejections can be exercised after the integrity gate. That procedure is not evidence that a changed payload could pass under the original digest. A changed ledger was also explicitly rejected with the original manifest and pin.

The trusted verifier’s own hash was checked externally before every reviewer execution. A substituted verifier was detected and deliberately not run. This is necessary: a malicious program cannot authenticate itself merely by printing a successful self-check. Neither a supplied digest nor a newly generated manifest is automatically a trusted provenance record.

The pinned four-file inventory has no unlisted files, and each permitted member must have its expected size and hash. The validator checks ledger and manifest semantics; it does not independently adjudicate the scholarly assertions in the report or metadata. Those were checked by the human-readable mathematical/source audit above. Hashes identify bytes, not correctness or redistribution permission.

The bounded-input statement concerns accepted schemas and the externally frozen payload. The verifier reads files before some size comparisons and has no streaming memory limit or operating-system resource sandbox. No denial-of-service, race-free filesystem, or hostile-owner security guarantee is inferred. The actual audit uses fixed, externally checked inputs and enforced read-only permissions; this limitation does not affect the mathematical disposition or the observed replay results.

## 5. Independent byte record and source-free publication boundary

The candidate’s public payload totals **29,920 bytes**:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| REPORT.md | 8230 | 67b28d2bef4ade9f5badcf80551dd334c490d73d5054f70ff001a88dd35ea540 |
| SOURCE_METADATA.json | 3139 | 33c55ad7772f852cdeb5e343c3717262ae2f9827e99a43b0b9357ed780e5c3e9 |
| cases.json | 9131 | 5b75514f7123069c78d1251ac23f6043bca1aa19165236fc3a833e44e93babb9 |
| verify.py | 9420 | c665a143651efce5532f41d55db02471f1c4b1e0e7146477a87ad36f2369a58c |

The external manifest is 631 bytes with the digest stated at the beginning of this audit. Its digest is recorded outside the payload; the manifest must not be placed inside the exact four-member directory used by the verifier.

The source-free allowlist is limited to those four candidate files, this authored audit, the accompanying authored verification metadata, and the external hash/allowlist metadata. Source PDFs, HTML, extracted source text, rendered source pages, source datasets, and coordination files are excluded. This audit paraphrases the target and cites public sources rather than reproducing the source’s question or proof passages.

The audit’s verification metadata records the independent counts, scenario outcomes, source-document hashes, and original-payload hashes. Source hashes and byte counts identify retained evidence without distributing it. An external supplemental hash manifest binds this audit and its verification metadata without asking either document to authenticate itself.

**Final disposition: ACCEPT / KNOWN-SOLVED. New approaches: 0. Required correction patch: none. Remaining mathematical gap for the stated target: none, with the published theorem and Fatou lemma explicitly treated as imported results.**
