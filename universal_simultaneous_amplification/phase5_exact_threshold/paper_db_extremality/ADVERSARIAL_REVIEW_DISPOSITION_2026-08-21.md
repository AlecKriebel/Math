# Disposition of the second external adversarial review

Date: 2026-08-21

This record classifies each recommendation against the labelled Markov chains,
the manuscript source, the exact certificates, and the public-release history.
No headline theorem was assumed merely because the review endorsed it.

## Necessary formal repairs accepted

1. **Rectangular phase spaces and stationary-law uniqueness — correct.**  A
   stop from a singleton active set produces an empty pre-sampling cache, so
   the sample and retarget channels do not share one state space.  The paper
   now defines
   \(A:\mathcal Z_n\to\mathcal Y_n\) and
   \(R:\mathcal Y_n\to\mathcal Z_n\), extends the dual stationary law by zero
   at both excluded boundary sets, types \(M=AR\) and \(K=RA\), and proves
   irreducibility and aperiodicity of \(K\).  The integration verifier now
   checks the two finite phase spaces and the empty-cache boundary directly.

2. **Mixed-difference notation — correct.**  The operators \(\Delta_i\) and
   \(\Delta_T\) are now defined before the coverage proposition.

3. **Normalized-kernel versus raw-weight notation — correct.**  The paper now
   defines \(P(W)\), \(\rho_{\mathrm{dB}}(W,r)\), and the scale-free defect on
   normalized kernels, and proves in the integration verifier that its raw-
   weight and normalized forms agree exactly.

4. **Companion-work citation — partly correct.**  The cover letters and
   provenance file already disclosed the companion software archives, so
   there was no undisclosed-submission defect.  Because the Introduction
   discusses the growing-family frontier, however, the manuscript now cites
   the public unrefereed beyond-three-halves companion release and states its
   bounded scope neutrally.

## Correct clarity repairs accepted

5. **Large-order strictness — no proof gap, but the wording was loose.**  The
   displayed positive polynomial already implies \(\beta_N<19/20\), and
   direct algebra gives \(\varepsilon_N<1/20\) for \(N\ge46\).  Both strict
   inequalities are now stated with the latter cleared polynomial included.

6. **Ordered sum defining \(z(B)\) — correct clarification.**  The sum is now
   explicitly over ordered pairs \((w,i)\in B^2\) with \(w\ne i\).

7. **Smaller editorial points — accepted where presently actionable.**  The
   abstract now says “within” the two symmetric \(K_4\) families; the author
   summary uses “in the strong-selection limit”; the local radius uses the
   Frobenius norm; open undirected statements refer to kernels induced by
   undirected weightings; and almost-sure forward absorption is justified.

8. **Persistent archive identifier — correct as a future release gate, not a
   present defect.**  No identifier exists for this consolidated version.
   The availability statement now says so explicitly, points to the recorded
   archive checksum and clean-room test, and requires replacement by the real
   versioned identifier after a human-authorized release.  No DOI or external
   submission was fabricated or initiated.

## Independent checks retained

The previous exact all-sector replay, labelled active-chain reconstruction,
strong-selection sum-of-squares replay, and clean-room package test remain
load-bearing.  This revision adds explicit regression checks for the
rectangular phase boundary, normalized/raw defect equality, notation guards,
and companion citation.  It also binds the displayed symmetric-sector
verifier hash and makes that verifier assert the exact minimum rational margin
printed in Appendix A.

The complete exact suite passed both in the development tree and from a fresh
archive extraction with the pinned environment.  The extracted 30-page PDF
was byte-identical to the repository PDF.  A full visual pass found one
post-pagination float defect; the corrected $K_4$ figure now remains below
its appendix heading, and a second visual pass found no remaining layout
defect.  Two independent hostile reviewers found no remaining mathematical,
scope, citation, or package objection.

Status at this checkpoint: review fully adjudicated and validated.
Best-guess completion: 100% of this review-response cycle.
