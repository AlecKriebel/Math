# Independent algebra/projective audit of PR 46

Mathematical verdict: **PASS for the exact target**, with the disposition **already_solved** and existing-author credit. This is a scoped mathematical audit, not an approval to accept, merge, or publish the PR.

The target is: for every d>=2, a nonempty open subset of the full real degree-d rational-map space, of dimension 2d+1, consists of maps whose every periodic point on CP^1 is in RP^1. The open topology is the ordinary real coefficient/projective topology. No assertion about the entire real-periodic locus being open, Hermite polynomials, higher-dimensional projective space, or journal publication is included.

The exact reviewed head is a39d178b10f75fb127058b08e0d0002b3ae97f8a. All 13 frozen scientific files match snapshot_manifest.json and have mode 0444. The preparation manifest has SHA-256 da37655e9b3bab420862a0c17c761e67fa9a4bc2028a328d033547249c54ad2e; all 318 file bindings were rechecked. File-level hashes are in original_bindings.json. No original file was modified.

## Independence and mechanism

Before reading candidate files or another reviewer’s conclusion, I wrote independent_proof.md. Its mechanism is a negative-residue affine rational map

    f(z)=Az+B-sum_j c_j/(z-p_j), A>1, c_j>0,

with d-1 distinct real poles. For any nonreal point, |Im f(z)|>A|Im z|. Iteration gives an exponential lower bound, so no nonreal periodic point can occur at any period. Infinity is real and attracting, and finite poles map to that fixed point. An attracting real fixed point persists under every sufficiently small real coefficient perturbation. A real projective conjugacy moves it back to infinity, after which simple real poles, negative residues, and slope >1 persist. This gives a neighborhood in all 2d+1 coefficient directions, not just the 2d-dimensional displayed fixed-infinity family. The proof handles d=2 and every higher degree and needs no finite-period extrapolation.

Only after that written proof and its first controlled computation launch did I read the candidate. The new proof is an audit mechanism, not a claim of new mathematical discovery.

## Adversarial comparison with the complete original exposition

SOURCE_STATUS.md supplies a different direct all-period mechanism: strictly interlacing negative roots and strictly positive coefficients of equal-degree numerator and denominator. The chart fixes just the denominator’s leading coefficient; the numerator’s leading coefficient remains free. Therefore its neighborhood has d+1+d=2d+1 coordinates. Real simple roots continue in disjoint intervals under small real perturbations, with strict root order and coefficient signs retained. The resultant remains nonzero. This genuinely gives full ambient openness.

The common residue sign proves real fibers and excludes real ramification. The pole coordinate 1/f and the infinity coordinate 1/z are essential: the written exposition explicitly supplies their nonzero differentials. Composition then preserves both real fibers and absence of real ramification, including an intermediate orbit passing through infinity.

Homogeneous iteration retains strictly positive coefficients in every homogeneous degree and cannot introduce a common projective zero. Thus the n-th iterate has exact degree e=d^n, with both affine polynomials of degree e and nonzero positive leading coefficients. Its e poles are real, simple, finite, and negative. On each interval between consecutive poles the iterate is monotone and has opposite infinite endpoint limits, yielding e-1 distinct real fixed points. Positivity gives an additional distinct fixed point on the positive axis. The fixed-point polynomial has degree e+1; a nonreal conjugate pair would leave room for at most e-1 real roots with multiplicity, contrary to those e distinct real roots. This proves all roots are real for each arbitrary n. Infinity is not fixed by these iterates, because their leading-coefficient quotient is finite. Poles cannot be extraneous fixed-point roots by coprimality.

This argument does not assume all fixed points are simple. A repeated real fixed point would not undermine the degree/conjugate-pair contradiction. The finite checks of simplicity are stronger properties of the tested examples, not a hidden premise of the written theorem.

| Potential failure | Result of the adversarial check |
|---|---|
| Merely polynomial or fixed-infinity openness | Rejected: candidate coefficient chart has all 2d+1 coordinates. Independent proof normalizes a persisting fixed point. |
| Degree loss or cancellation | Excluded at the seed, on its neighborhood by resultant nonvanishing, and under homogeneous iteration by the common-zero argument. |
| Infinity omitted | Candidate shows it is never fixed by an iterate; independent family includes it as a real attracting fixed point. |
| Poles counted as fixed points | Coprimality forbids extraneous polynomial roots; projective orbit handling is explicit. |
| Real-fibered alone assumed sufficient | No: the extra coefficient/attractor condition does essential work. The frozen negative control has nonreal fixed points. |
| Finite-period tests treated as the proof | No: both written mechanisms quantify over arbitrary n. |
| Multiple roots or real ramification | Root-count proof tolerates fixed multiplicities; the poles are simple because the real map is unramified. |
| Complex perturbations smuggled into the topology | No: all perturbations are real, in Rat_d(R). |
| Restriction to d=2 | No: both formulas and proofs apply to every d>=2. |
| Historical source theorem confused with the lower-dimensional Chebyshev family | No: v1 separates the ambient theorem from that additional family. |

No mathematical correction is mandatory for the exact conclusion. As optional publication housekeeping, the frozen README sentence saying no PR has been opened is historical and should not be treated as the current PR state. The source qualification in SOURCE_STATUS.md is appropriate: the known result is verified as a preprint result, and no journal publication is certified by this audit.

## Primary-source verification and confidence

The full original OWR contribution was read through the primary publisher PDF. Printed page 669 explicitly asks the full ambient-interior question after giving Chebyshev existence; its claim that the question was open is a March 2020 workshop snapshot. Confidence that this identifies the exact target: 0.99. [Oberwolfach Report 12/2020](https://ems.press/content/serial-article-files/46848).

The April 2020 v1 introduction and Theorem 2, printed page 2, explicitly assert a nonempty ambient open subset. Section 2.2, printed page 6, uses interlacing with positive coefficients and iteration. The target second assertion is sufficient; this audit does not certify every unrelated claim in the paper. Confidence in the exact known-result attribution: 0.99. [Kozhasov–Kummer v1](https://arxiv.org/pdf/2004.10003v1).

The October 2020 v2 Example 1, printed page 3, uses strictly interlacing polynomials and an attracting real fixed point and explicitly concludes interior membership. Its isolated sentence mentions fixed points, but the defined locus, Lemma 9, and Theorem 3’s proof provide all-period scope. Its infinity example agrees with the independent mechanism developed here. Confidence that the current revision retains the conclusion: 0.99. [Kozhasov–Kummer v2](https://arxiv.org/pdf/2004.10003v2).

The current primary arXiv record gives the v1 and v2 submission dates and shows no journal-reference field or withdrawal notice in the inspected record. This supports the stated preprint qualification, not a claim of exhaustive publication-history research. Confidence in that scoped metadata statement: 0.95. [arXiv record](https://arxiv.org/abs/2004.10003).

Only authored paraphrases and source references are retained here. No primary-source PDF, OCR, rendered source page, cache, download header, cookie, or source body was copied into this owned directory. Local foreign PDF hashes in the original provenance remain references; I did not independently download and hash those PDFs.

## Actual computations and limits

The new independent program passes 15 exact cases: twelve iterates, covering d=2 through period 5, d=3 through period 3, and d=4,5 through period 2, plus three exact projective conjugacies moving the attracting fixed point from infinity to 7. It verifies degree, coprimality, all finite fixed roots real and simple, and the conjugated attractor multiplier 1/2. These controls support indexing and normalization; the written inequality and local normalization are the infinite-period/full-neighborhood proof.

The first run failed because it tested polynomial gcd equality to 1, although a nonzero constant gcd already proves squarefreeness. The corrected test checks degree zero. The original failed source and its complete failed-run capture are preserved, and the successful run has separate complete stdout/stderr and real PID/UTC records.

Both frozen programs were then executed from their exact unmodified bytes. Only the __file__ output base was redirected to owned receipt directories, to prevent writing into the immutable snapshot. All 51 author assertions and 848 original review assertions pass, and both generated receipts are byte-identical to the frozen submitted receipts. Their prelaunch source/operator hashes, launcher and child PIDs, UTC times, command arguments, complete stdout/stderr, and completion return codes are retained in separate capture directories.

No mathematical gap remains for the scoped nonempty-interior existence claim. This audit leaves unrelated source classification results, journal publication history, native queue/control-plane decisions, and PR acceptance to their respective scopes. The frozen turns.json remains substantive_turns_used=0 and source_verification_responses=1; no budgeted new proof attempt was made. No external person was contacted, and no Git/index/branch/native/remote mutation occurred.
