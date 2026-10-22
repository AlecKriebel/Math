# Independent adversarial audit: Problem 2306043

Date: 5 October 2026 (UTC). Queue rank: 683. Problem label: AMR-022-6043.

## Verdict

**PASS as an unresolved five-approach partial investigation, with the stated source-proof limits retained.** Recommend `exhausted`, `5/5`, zero discoveries, no candidate solution. The packet supplies neither a full-class proof nor a counterexample in the normalized univalent class S. No mathematical correction to the frozen packet is required by this audit.

This is a fresh audit of the submitted arguments, not a sixth research approach. It did not delegate proof work, alter the frozen packet, or make remote writes. Publication safety is limited to authored audit material, code, and public verification metadata. Source PDFs, images, extracted text, catalog contents, and private coordination are not included.

## Immutable subject and replay

The audited `FROZEN_MANIFEST.json` has SHA-256:

    21ac6f2720eb4492499e1034053e9652bbc41fca6b47613077cfb05eece936f6

All 13 listed payload files match their declared SHA-256 values and byte counts, totaling 42,715 payload bytes. The directory contains precisely those files and the manifest. Integrity was checked before and after the independent controls.

The original standard-library control program passed all 2,945 assertions. Its parsed output equals the stored `CONTROL_RESULTS.json` exactly. The separate audit program passed 8,564 assertions: 8,500 mathematical/algebraic controls and 64 integrity/replay assertions. These finite checks corroborate formulas; they do not establish the infinite statements or prove univalence.

Run the independent checks with Python 3, supplying the frozen public directory:

    python3 verify_independent.py /path/to/frozen/public

## Source and normalization findings

The governing [Hayman-Lingham compilation](https://arxiv.org/pdf/1809.07200v2), printed pages 114-115 and 133-134, was checked independently. The inspected convention is log(f/z) = 2 sum gamma_n z^n. The target concerns the absolute-linear radial sum; the historical update concerns a different, quadratic sum. Its lower-growth assertion uses non-little-o and does not state a counterexample to the original question. The source's big-O notation does not expressly impose a constant uniform over S. The packet's fixed-function interpretation, and its warning against silently strengthening that quantifier, are sound. The document is publicly marked as a draft.

The [Duren-Schiffer paper](https://msp.org/pjm/1988/131-1/pjm-v131-n1-p06-p.pdf), printed pages 106-107, was checked as text and page images. Equation (3) has weighted squared modulus, constant one half, positive Hayman index, and maximal-growth direction normalized to 1. For a direction exp(i theta), applying the theorem to exp(-i theta) f(exp(i theta)z) yields the packet's reference exp(-i n theta)/n. The modulus removes the rotation factor. Alpha equal to 1 is separately legitimate by the Koebe equality characterization; alpha equal to 0 is outside the finite-energy hypothesis.

Verified cached PDF metadata agrees with the packet: Hayman-Lingham, 1,706,228 bytes, SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`; Duren-Schiffer, 1,034,965 bytes, SHA-256 `698b00f1de7bbafd1f87038c2faf2ede815612a89f46435670dde110be0133cf`. Both official public PDF URLs also opened during this audit. The hashes describe the inspected cached bytes, not an unperformed fresh download.

## Mathematical review

### Turn 1: Abel reformulation and logarithmic loss

The Abel identity follows from nonnegative double-sum interchange. Its reverse big-O and little-o implications use r_N = 1 - 1/(2N), with r_N^N at least one half; no monotonicity of individual coefficients is required. All coefficient series needed for the Milin generating-function argument converge absolutely for fixed r below 1: choose a coefficient-estimate radius rho with sqrt(r) < rho < 1. The triangular weight is N+1-n, and its generating kernel is r^n/(1-r)^2.

The energy is sum |b_n|^2 r^n/n, for b_n = n gamma_n. Cauchy-Schwarz pairs it with sum n r^n = r/(1-r)^2. The resulting square-root logarithm is genuinely unbounded and cannot be absorbed into a constant. The packet does not assert the stronger zero-additive-constant single partial-energy inequality for arbitrary f in S; it uses the valid double-sum theorem.

### Turn 2: Dyadic shortcut and sparse control

Bounded dyadic energies imply the desired linear partial-sum bound. They also imply sum_{n<=N} |b_n|^2 <= 4KN and hence the quadratic radial sum is O((1-r)^(-1)). That would contradict the update's particular fixed-function non-little-o assertion. This is a valid obstruction to the stronger intermediate premise, conditional on the attributed historical theorem, rather than a disproof of the target.

In the sparse sequence, all-index energy is bounded by summing complete blocks through the last occupied index. The radial lower bound has the stated positive ratio to the quadratic comparison scale. Consecutive occupied masses have ratio less than one half, while their cumulative mass divided by the current occupied index tends to zero. Thus its linear majorant has the stated little-o behavior. This correctly shows that a large quadratic sum need not force the problematic linear behavior. The disjoint-interval integral estimate for its signed series has the correct inequality direction.

### Turn 3: Positivity and sharp subclass results

The Fourier formula has factor 1/pi because only the positive-frequency analytic half of the real part contributes. The coefficient bound of 2 follows. Substitution into the logarithmic derivative gives |n gamma_n| <= 1-sigma, and the displayed extremizer attains every radial bound. Its logarithmic derivative is sigma + (1-sigma)(1+z)/(1-z), so the standard starlike criterion applies. For positive sigma its growth estimate gives zero Hayman index. The phase-aligned reduction uses the opposite evaluation angle and is correct. No passage from real coefficients to nonnegative coefficients, or from S to the starlike class, occurs.

### Turn 4: Positive-index Abel and Cesaro limits

The theorem input supplies finite energy of d_n = gamma_n - exp(-i n theta)/n. For any fixed cutoff, the finite head vanishes after multiplication by 1-r; the radial tail is bounded by the square root of its weighted energy times sqrt(r). Taking the radial limit before sending the cutoff to infinity proves the required little-o perturbation. The reverse triangle inequality then gives the limit 1.

The same cutoff argument with sum_{n<=N} n = N(N+1)/2 proves the Cesaro limit 1. This direct argument avoids invoking an unjustified Tauberian equivalence of exact limits. The explicit bound and dependence on log(1/alpha) have the correct constants. No uniform tail control, alpha-zero extension, or novelty claim is asserted.

### Turn 5: Infinite relaxed model and non-univalence safeguard

The Rudin-Shapiro recursion preserves disjoint supports and signs, and its sum-of-squared-moduli identity proves the maximum-modulus bound. Independent checks also recover the P coefficients from the binary adjacent-one formula, rather than only repeating the recurrence.

The block supports are disjoint. The coefficients have subexponential growth, giving locally uniform convergence inside the disk. Every prefix energy bound is valid even when a prefix stops within a block, because charging its whole block is an upper bound. Summing these prefix inequalities gives every Milin double-sum inequality for this relaxed model.

The signed growth estimate follows from disjoint intervals [N_j/2,N_j] and -log(r) >= 1-r. The absolute radial lower bound uses all N_j terms of one block; r_j^(2N_j) >= 1/4 gives (1-r_j)A(r_j) >= sqrt(m_j)/32. This diverges for one fixed infinite coefficient sequence, not a varying family of finite examples.

Radial integration gives a summable supremum bound sqrt(m_j/(8N_j)) for each G block. Consequently the block series defines a continuous bounded extension to the closed disk and an analytic interior function. This does not require absolute summability of all individual boundary Taylor coefficients. The exponential construction has the stated normalization and zero-free quotient.

Most importantly, F'(z) = exp(2G(z))(1+2H(z)). The real seed is -z, and the entire infinite remaining tail at 3/4 has the stated rational upper bound. The intermediate-value argument therefore proves a real interior critical point and excludes F from S.

The audit strengthens this safeguard without changing the construction: for q = 49/100 and 51/100, use

    T(q) = q^256 [256/(1-q) + q/(1-q)^2].

Exact rational arithmetic verifies 1 - 2(49/100) - 2T(49/100) > 0 and 1 - 2(51/100) + 2T(51/100) < 0. Since |R(q)| <= T(q) for the full infinite tail, a critical point lies strictly between those two rationals. This is an infinite-tail certificate, not root-finding on a truncation.

## Required limitations and publication scope

- Hayman's 1980 construction remains an attributed input from the inspected problem update. The cached purported article download is HTML, and the DOI route failed again during this audit. The original construction and proof were not independently inspected.
- The de Branges-Milin theorem, the starlike criterion, and Bazilevich's inequality are established external inputs. The full original proofs, including Duren-Schiffer's later variational argument, were not reconstructed here.
- The original problem website again failed to open. The audit does not claim direct verification of its current live wording or status.
- A bounded supplementary search did not identify a verified resolution. Search silence does not establish that the exact question is still open in all current literature.
- Historical queue, branch, and PR checks in the packet were not refreshed by this mathematical audit. Publication should perform its normal live duplicate and state checks separately.
- The source material was inspected privately. The audit deliverables contain authored analysis, authored code, and public metadata only.

These limitations do not invalidate the qualified partial results. They must remain visible. The packet is suitable for publication as an audited, unresolved five-turn attempt, with no solution, counterexample in S, or discovery claimed.
