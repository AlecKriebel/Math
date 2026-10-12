# Independent acceptance: a sharp two-factor partition-sign obstruction

Date: 12 October 2026. Verdict: **ACCEPTED, within the exact restricted scope below.**

## Accepted statement

For every set S of at most two positive integers, let

P_S(q) = product over m in S of (1 + sum over j >= 1 of epsilon_(m,j) q^(mj)), multiplied by product over m not in S of (1-q^m)^(-1),

where every epsilon is independently +1 or -1 and every constant term is +1. Some coefficient of degree at most 86 has absolute value at least 2. The bound is sharp: with S = {1,2}, a signed prefix is feasible through degree 85.

This answers the specific first-two-factor question asked by David Newman in his 25 June 2017 MathOverflow follow-up, and proves the stronger at-most-two-factors version. It does not settle the original problem in which all factors may be changed. An affirmative unrestricted solution would require a negative coefficient in at least three distinct factors among terms of total degree at most 86. No novelty or priority is asserted.

## Independent derivation and completeness

For a fixed S, define C_S(q) = product over m not in S of (1-q^m)^(-1). A state at degree n contains every sign epsilon_(m,j) with m in S and mj <= n. No sign is fixed beforehand and no distinct states are identified.

At degree n, first multiply the old finite signed polynomials (containing only terms of degree below n) by C_S. Let A_n be the resulting coefficient of q^n. There is one fresh sign for each m in S dividing n. Each fresh term contributes only its own sign at degree n, because all other factors must supply their constant term. Products of two fresh nonconstant terms have degree 2n. Therefore the complete extension condition is |A_n + sum of fresh signs| <= 1.

The root is the unique empty assignment. Retain every fresh-sign tuple meeting that condition. Restriction of any feasible assignment is feasible at the previous level, and its actual fresh-sign tuple is among the tuples tested. Induction proves that the computed frontier is exactly the complete feasible set. No symmetry reduction, parity pruning, bound on search nodes, floating-point comparison, dominance assumption, or heuristic filtering is used. Signs in different coefficients of a factor and signs in the two factors remain independent. Later terms cannot repair an earlier coefficient.

If neither 1 nor 2 is in S, the coefficient of q^2 is 2. Independently verified singleton obstructions are degree 31 for S={1} and degree 11 for S={2}. A second index larger than the corresponding obstruction degree cannot yet affect that obstruction. The complete finite list is thus the 30 pairs (1,b), 2 <= b <= 31, and the 9 pairs (2,b), 3 <= b <= 11, together with the two singleton controls. Both equality endpoints are included and were executed explicitly.

## Independent arithmetic evidence

The audit implemented and ran the first-two-factor enumerator before reading any candidate implementation or certificate. Its source hash at that point was 8c09e5f9a1fd598ef84cd1d5dc0448288e8d0c9241ca8a8be81224cbf55740fe. It found degree 85 feasible with six assignments, degree 86 empty, and peak frontier width 462. A separate exhaustive scan of all 32,768 raw sign assignments through degree 10 agreed with the exact frontier, not only its count. Fixing the second factor positive reproduced the known first-factor obstruction at degree 31, including all 40 maximal first-factor polynomials.

A separately authored generic direct-convolution implementation then exhausted all 39 pairs plus the two singleton controls. Before candidate code or data were inspected, it independently reproduced all thresholds and the total 23,683 nonempty states. The first-two case accounts for 11,620 states, counting its root once.

A standalone replay verifier uses a different derivation of the fixed tail. If s_k is the sum of divisors d of k with d not in S, formal logarithmic differentiation gives

c_0 = 1, and n c_n = sum from k=1 to n of s_k c_(n-k).

It checks exact divisibility and uses cached convolution with the second factor. This differs from the direct enumerator's Euler-factor partition dynamic programming and explicit product over old coefficients. The complete canonical-state digests, all frontier cardinalities, maximal-degree counts, terminal states, and witness fields agree for all 41 cases. The locally retained compact replay certificate is 100% regenerated from arithmetic, not accepted merely by its hash. This certificate is not included in this prose edition.

After those independent computations were complete, the frozen candidate proof and full certificate were inspected. The independent full-certificate comparison uses our own arithmetic to regenerate every frontier and compares actual sets of complete sign strings against all supplied states. It imports neither the candidate producer nor the candidate verifier. Every supplied frontier agreed. No candidate code and no external source-author code was executed.

The exact first-empty degrees are:

- {1}: 31; {2}: 11
- {1,2}: 86; {1,3}: 59; {1,4}: 84; {1,5}: 31; {1,6}: 59
- {1,b} for every 7 <= b <= 31: 31
- {2,3}: 40; {2,4}: 81; {2,5}: 23
- {2,b} for every 6 <= b <= 11: 11

## Terminal obstruction and sharpness

The candidate's six printed degree-85 states were independently reconstructed and multiplied by all fixed geometric factors through degree 86. Their degree-86 residuals, in the candidate's order, are -8, -6, -6, -4, -4, -8. The only fresh signs at degree 86 are epsilon_(1,86) and epsilon_(2,43), whose sum is -2, 0, or 2. Every resulting coefficient is at most -2. This directly checks the final rejection and the degree convention.

All six states are feasible through degree 85. The complete printed coefficient list of the candidate's state 1 agrees with independent explicit polynomial convolution. Its coefficients also have the ordinary partition-number parity. A different selected final state is recorded in a locally retained witness record, including all 86 product coefficients and compact positive-sign intervals; that separate record is not included in this prose edition. The two witnesses differ only because different valid terminal states were selected.

## Adversarial checks and provenance controls

All semantic checks use explicit exception gates; none relies on Python assertions. Normal Python, -O, and -OO replay runs agree. The compact-certificate controls reject nine semantic corruptions per mode: a missing boundary case, wrong factor index, wrong frontier count, wrong state digest, wrong terminal residual, a flipped witness sign, wrong sharpness degree, wrong total, and an extra unverified claim. A separate external-pin test rejects a whitespace-only byte change. This gives 30 rejected corruptions and three accepted intact compact replays.

The full-candidate controls independently reject removal of a feasible state, insertion of an infeasible state, omission of a boundary pair, and an invalid sign character. A changed mathematical proof fails its external proof pin. These give 15 further rejected corruptions across the three Python modes, together with six accepted intact full-certificate/proof-data runs. The final file manifest has an external hash anchor; changing a file and recomputing a local manifest does not preserve that anchor.

## Primary-source scope

1. [Newman, A Product Related to Unrestricted Partitions](https://mathoverflow.net/questions/146359/a-product-related-to-unrestricted-partitions), 30 October 2013. The inspected primary page states the unrestricted sign-array problem and a historical search beyond 100 but below 110. No solution is supplied in the rendered answer section. This is historical context, not proof of current worldwide open status.
2. [Newman, A simplified version of an old problem about the generating function for unrestricted partitions](https://mathoverflow.net/questions/272822/a-simplified-version-of-an-old-problem-about-the-generating-function-for-unrestr), 22 June 2017. Aaron Meyerowitz's revised answer gives the first-factor degree-31 obstruction. Newman's 25 June comment asks specifically about independently changing the first two factors. The present theorem covers exactly that follow-up.
3. [Andrews and Newman, Binary Representations and Theta Function, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf). The introduction and odd-dilate formula were inspected as text, and the first page was inspected visually. The published paper distinguishes the unrestricted question from its affirmative odd-dilate identity. The local published PDF was verified as 260,035 bytes, SHA256 31a846dc5eecc6359c3931cbeb37c281273545f25c770c6ebc8c221a5b5870c1. Its historical 2018 unknown-status statement is not promoted to a 2026 global-status determination.
4. [Newman, Yet another question about unrestricted partitions](https://mathoverflow.net/questions/282057/yet-another-question-about-unrestricted-partitions), September 2017. Max Alekseyev reports a sharp degree-121 feasible prefix in a different numerator/denominator-sign class. That class can change many factors but restricts them to alternating geometric patterns. It neither contradicts nor establishes the arbitrary at-most-two-factor theorem. The claimed degree-121 maximum and source-author code were not independently audited or executed here.

Targeted current web searches found no matching degree-86 prior result in the inspected primary material; this is not an exhaustive novelty search. The original unrestricted problem remains unresolved by this audit. No copied primary-source document or raw page text is included in this prose edition.

## Accepted frozen candidate

- TWO_FACTOR_OBSTRUCTION.md: 11,857 bytes; SHA256 7d1522c8f0c75a33df310742786acf0612dd2f133efed5fb681dbf2b7d228036
- Full raw all-state certificate (not distributed in this prose edition): 1,182,664 bytes; SHA256 f9da20d1f63cb04bc00591ed445ab7d68e7f01aeeafc9b43eccced1634d3c2eb
- SOURCE_ADDENDUM.md: 1,484 bytes; SHA256 734b1d0512a5d369f0cd3fa6fd7121fafd1e8964013b429c8a642515e99774bc

The theorem and proof require no mathematical correction. Acceptance is specific to these frozen bytes and the stated class. Publication, journal review, novelty, three-or-more-factor feasibility, and any infinite unrestricted construction are outside this verdict.

## Prose-edition distribution and later integrity supplement

The preceding report is the complete substantive independent audit, with only the distribution-reference edits documented in EDITORIAL_MAP.json. Its mathematical reasoning, hypotheses, finite reduction, recurrence completeness argument, arithmetic conclusions, adversarial checks, source distinctions and limitations are retained. The accepted authored proof and historical addendum are reproduced byte-for-byte. No mathematical correction was required.

All described exhaustive computations and full-frontier set comparisons were performed and independently checked locally. Programs, the 1,182,664-byte full raw all-state certificate, the separate compact replay record and detailed execution outputs are absent from this prose edition. The explicit states and coefficient list printed in the authored proof are retained as mathematical proof content. The prose edition is not an executable replay package, and its public hashes and aggregate totals do not themselves establish exhaustive completeness.

The frozen audit's 30 compact-certificate/control rejections and 15 full-candidate/proof rejections total 45. After that report was frozen, six additional bundle-integrity corruptions were rejected: an altered report with the original manifest, and the same alteration with a recomputed local manifest, each under normal Python, -O and -OO. The former failed file integrity; the latter failed the externally fixed manifest pin. Three intact postseal bundle checks also passed and semantically replayed the 41-case result. Thus the complete recorded control history totals 51 deliberate rejections: 45 earlier controls plus six later bundle-integrity controls. The six later checks are not six new mathematical cases.

This is AI-assisted research and independent AI-assisted verification. It is not external human peer review, journal acceptance, proof-assistant certification or a novelty determination. The unrestricted problem remains unresolved by this work.
