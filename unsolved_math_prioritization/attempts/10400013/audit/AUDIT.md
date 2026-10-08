# Independent mathematical and replay audit: AMR-103-0013

Audit date: 2026-10-08 UTC. Problem 10400013, rank 1009.

**Disposition: accept the corrected packet as an audited, source-scoped partial attempt; retain UNSOLVED, 5/5 approaches.** No general knot clause is resolved. The original author's mathematical statements require no correction found by this review. Its verifier requires the small exact-arithmetic correction supplied here. This is an independent mathematical review with executable finite controls, not machine-checked formal proof, human peer review, or a novelty certificate.

## 1. Identity, source question, and scope

The received author archive is 24,812 bytes, SHA-256 `49798e2b582bf9565bd729f8b83ed25939377fc46fe72ce6c5e402cea71ec626`. Its external manifest, bootstrap and test-harness hashes match the supplied pins. All 12 archive members match the frozen distribution. The nine payload files were read, not merely replayed.

The publisher's original Problem 1.13, printed p.391 / PDF p.19, was checked in text and visually. It asks about the number of polynomial **values** with a fixed span, and separately about fixing **both coordinate spans** for the two-variable invariants. It does not explicitly restrict its opening domain to knots; neighboring definitions and the following remark include links. The packet correctly preserves this ambiguity. A knot-only interpretation is neither silently substituted for the original nor refuted by a link example. The descriptive title is editorial, not a claimed original subtitle. [Ohtsuki, publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

The complete retained catalog files were independently hashed and the unique numeric record and keyed research record rejoined. Their canonical record hashes and exact statement match agree with the author metadata. Only hashes, sizes and match results are included here. No corpus records are distributed.

Every source PDF's bytes and hash were independently checked against the author's source inventory. Source inspection was proposition-specific; it does not certify every theorem in every referenced paper. The duplicate gate is explicitly bounded history, not an exhaustive repository or external-literature uniqueness proof. No novelty claim depends on it.

## 2. Credited link counterexample

Traczyk's Example 1 gives the closures of odd powers of the half twist in the three-strand braid group. The induced permutation has one transposition and one fixed point, hence exactly two components. The displayed formula gives distinct Laurent polynomials of span 2. The article's larger connected-sum construction concerns three-component links with identical values, which must not be confused with Example 1. We inspected the mathematical article and the defining displayed example. [Traczyk, version of record](https://doi.org/10.24546/E0003672).

The packet's Burau matrices satisfy the braid relation. Their half-twist matrix squares to the scalar matrix t^3 I. Consequently every odd positive or negative power has zero trace. The standard three-braid identity then gives exactly the packet's formula. Our independent controls explicitly include negative powers, an inverse-matrix check, and a permutation-cycle check. The identity agrees with the equivalent form on printed p.26 of [Stoimenow, Properties of closed 3-braids](https://stoimenov.net/stoimeno/homepage/papers/mwf.pdf).

This refutes only the unrestricted-link Jones clause. For knot values W = epsilon t^k V, evaluation and differentiation at 1 force epsilon = 1 and k = 0. The same distinction is explicit in the historical span discussion of [Stoimenow's conference manuscript](https://stoimenov.net/stoimeno/homepage/papers/talk.pdf). Its old unknown-status statement is not a present-day completeness guarantee.

## 3. Audit of the five mathematical approaches

### 3.1 Integral coefficients and the shift

Accepted. Writing V = t^m P with P(1) = 1 gives V'(1) = m + P'(1). Therefore the coefficient list fixes its allowed monomial shift uniquely. The height estimate follows by the triangle inequality on the finite weighted coefficient sum. For bounded span, coefficient-height boundedness is equivalent to finiteness of actual normalized polynomial values.

The residue calculation for spans at most two is correct: the cube-root and value-at-one constraints force residue sums (1,0,0), and a support interval of length at most two contains at most one exponent in each residue class. The derivative then removes the possible monomial shift. This proves statements about values, not unknot detection.

The formal span-10 example has the claimed factorization, derivatives and root values. Our separate exact engine also checks coefficients far beyond machine-integer and floating-point precision ranges. Neither this example nor the height equivalence realizes a new knot polynomial. The author explicitly retains the realization gap.

### 3.2 Bounded braid index and unitary interpolation

Accepted with the exact hypotheses written in the packet. Fix the braid strand bound B independently of the span bound S. Jones's source uses the same letter for different indices; the proof correctly separates strand count b from root order r.

At each root exp(2 pi i/r), r >= 3, the positive normalized Markov trace factors through the positive Temperley-Lieb representation/quotient. Its braid generators are unitary. Cauchy-Schwarz for the positive trace gives |tr(U)| <= 1. The writhe factor is a phase; the remaining normalization has modulus (2 cos(pi/r))^(b-1). The estimate is valid for every strand count b, with no additional requirement b < r. This is the point that allows arbitrarily many interpolation nodes for a fixed B. The source's normalized formula and inequality were checked visually on printed p.12; positivity and the quotient construction are discussed earlier. [Jones, The Jones Polynomial](https://math.berkeley.edu/~vfr/jones.pdf).

Removing the unknown shift does not change the values' moduli on the unit circle. The S+1 nodes indexed by r = 3 through S+3 are distinct. For different r and q their reciprocal difference is at least 1/((S+2)(S+3)) and less than 1/2. Concavity of sine on [0,pi/2] supplies the stated chord lower bound. Each coefficient of a product of S unit-root linear factors has modulus at most the corresponding binomial coefficient, hence at most 2^S. Summing the Lagrange basis bounds gives equation (3), including its S = 0 case. Integrality and the shift lemma finish finiteness of values.

The proof does not bound the number of knots with one value. For links it bounds coefficient lists modulo monomial shifts; it does not eliminate the shifts. The Morton-Franks-Williams inequality has the direction stated in the packet and cannot supply the missing upper braid-index bound. General Jones finiteness is not obtained.

### 3.3 Adequate diagrams

Accepted. A first smoothing change in an A-adequate diagram merges distinct state circles. Each subsequent change raises the circle count by at most one. Every other state therefore has maximal bracket degree at least four below the all-A maximum. The all-B endpoint is analogous. There is no unproved cancellation assumption at either endpoint.

After the writhe monomial and A-to-t conversion, the span equals c minus the Turaev genus of **that same connected adequate diagram**. Thus bounded S and G imply c <= S+G. A bounded crossing count gives finitely many diagram combinatorics and hence knot types; the zero-crossing case is harmless. An arbitrary minimum Turaev genus diagram need not be adequate, and the argument correctly does not substitute that weaker hypothesis. This is stronger than value-finiteness within the stated class, but does not cover all knots.

### 3.4 A fixed two-strand full-twist family

Accepted. Over Q(A), e/delta and 1-e/delta are complementary idempotents. The crossing eigenvalues A and -A^(-3) are nonzero, so the decomposition applies for all integer full-twist counts, including negative ones. Closing against a fixed exterior is a fixed linear map, and the orientation-dependent writhe correction gives two slopes differing by exactly 8.

A fixed common Laurent denominator converts the two rational coefficients into polynomial coefficients without changing their n-independence. If both are nonzero, their supports eventually separate in either direction of n. The extreme terms cannot cancel, and subtracting the fixed denominator span proves the required linear lower growth of Jones span. If only one eigenchannel remains, ratios of knot values are monomials in t: the possible A exponents here are multiples of four. The knot normalization lemma makes all such values equal. Both channels cannot vanish. No evaluation at a denominator pole is used. Full twists preserve endpoint matching and therefore preserve the one-component closure.

This is a fixed-exterior theorem. It does not establish a uniform complexity bound over varying exteriors or simultaneous twists in unrestricted numbers of boxes.

### 3.5 Specialization kernels

Accepted strictly as formal algebra. Ohtsuki's displayed substitutions are exactly P(t,t^(1/2)-t^(-1/2)) for Jones and F(-t^(-3/4),t^(1/4)+t^(-1/4)) for Jones, with a = 1 for Q. The packet uses those conventions consistently.

For the HOMFLY expression, the R factor vanishes on the Jones curve, l^2-1 vanishes on the Alexander specialization, and S vanishes on the extra unit curve. The extreme l exponents are -4 and 6; the m exponents run from 0 to 8. For the Kauffman expression, the cubic expression in z cancels a+a^(-1) on the Jones curve; the squared a-difference cancels at a = 1. Its coordinate spans are 8 and 8. Coefficient dependence on N is nonconstant, and the indicated parity statements hold. Independent exact substitutions used N as large as 10^100.

These are elements of formal polynomial rings with the stated symmetries, not realized knot invariants. They establish the noninjectivity of the proposed finite-specialization recovery maps. No geometric realization, full collection of knot restrictions, or negative solution of either two-variable clause is certified.

## 4. Literature scope and remaining clauses

- The 2025 Jones paper establishes a finite **candidate** list through span six. Its actual small-span identification through four and its unresolved candidate realization distinction were checked, as were its higher-span formal constructions and Question 4.3. The omitted span-six enumeration is not independently reconstructed by this audit. [Kanenobu, Kishimoto and Sumi](https://doi.org/10.24546/0100498237).
- The 2026 Q paper classifies actual values through degree four. Its odd constant-coefficient property makes degree equal span for knots. The higher-degree construction is formal and Question 3.3 concerns actual knot values. The full mathematical text was inspected; no general Q resolution follows. [Ishikawa, Kanenobu, Kishimoto and Sumi](https://doi.org/10.24546/0100501377).
- The 1999 Jones fixed-span result refers to **weak/canonical genus**, visibly denoted by a tilde in Theorem 4.1 and Corollary 4.4 on printed pp.685–686. It is not a statement with only minimal Seifert genus bounded. These pages and the original notation were checked; the finite diagram-generator theorem remains a credited published input. [Stoimenow](https://doi.org/10.5802/afst.949).
- The September 2026 Ichihara v1 manuscript states a cosmetic-surgery result under additional hypotheses. Its landing page and introductory low-span discussion were checked; its full proof/computation was not audited and is not an input here. [Version-specific arXiv page](https://arxiv.org/abs/2609.32507v1).

A supplementary targeted live search found no reason to promote the packet's disposition. This is bounded evidence, not an exhaustive current-literature search. The accepted conclusion is that **this attempt does not resolve the general knot Jones, knot Q, skein/HOMFLY, or Kauffman clauses**. The credited link Jones counterexample remains separate.

## 5. Verifier defect, actual patch, and certificate semantics

The original verifier's negative unit-monomial power uses `v**n` for negative n. Python returns floats even when v is the integer 1 or -1. This contradicts the advertised integer/rational implementation; ordinary equality checks conceal the type change. Six independent positive/negative sign and exponent probes reproduce it. No false mathematical equality or changed diagnostic output was found from this issue in the tested finite ranges.

`CORRECTION.patch` replaces this operation by an integer parity-selected sign. It also updates the affected file's manifest entry and the bootstrap's manifest pin. Every other payload file, including PROOF.md, remains byte-identical. `CORRECTED_MANIFEST.json` inventories the corrected distribution. The original archive and original freeze were never modified.

The corrected verifier produces the same 32,681 diagnostic checks and byte-identical diagnostic output. A runtime type guard independently checks every cleaned polynomial coefficient while the corrected diagnostic runs. The independent exact engine is separate from the author's ring implementation and rejects floating coefficients and noninteger/boolean exponents.

The bootstrap authenticates its manifest by an externally supplied pin, then all payload bytes and inventory before launching isolated Python. The external bootstrap and test-harness pins must also be checked. This is a static-distribution integrity mechanism, not a signature from a trusted mathematician. A re-pinned malicious bootstrap would have no authority; tests assume the externally verified scripts and normal filesystem behavior. No hostile concurrent-writer or time-of-check/time-of-use sandbox guarantee is made.

Both original and corrected freezes were run as uid 1000 with actual write attempts denied. All normal, -O and -OO modes pass; corrected relocation also passes from a separate read-only location. Author-authored mutation controls were rerun separately from the independent controls. Independent malformed-claim probes test every declared field and add duplicate keys, wrong JSON types, nonfinite values, bool/float confusion, missing and extra fields. Independent integrity probes include manifest and packet symlinks, hidden entries and rehashed forged proof/executable payloads; forged executables do not run. Neither assertions nor docstrings are relied on for rejection.

The checks certify reproducible finite diagnostics, byte integrity and conservative claim flags. They cannot certify knot realization of formal examples, unitarity's source theorem from first principles, every source theorem, exhaustive literature coverage, historical novelty, or a global solution. Acceptance of the scoped mathematical arguments comes from the written review above, not a PASS token.

## 6. Reproduction and final disposition

Use `AUDIT_MANIFEST.json` and its separately communicated SHA-256 pin to authenticate this review distribution. It includes the actual correction, corrected freeze, independent checks, source identity readback, and replay receipt summaries. The original author distribution is a separate immutable input.

Run `python -I -S -B independent_checks.py ORIGINAL_FREEZE corrected_freeze`, and repeat with `-O` and `-OO`. Run the corrected freeze's `test_bootstrap.py` independently. The receipt files record the exact outcomes and limitations. All public artifacts are authored review/proof/code or permitted public verification metadata; no source PDFs, source extracts, screenshots, catalog contents, or private coordination are included.

**Accepted disposition: UNSOLVED by this attempt; five substantive approaches; limited positive results and one credited link-only negative result. No mathematical statement changed by the correction.**
