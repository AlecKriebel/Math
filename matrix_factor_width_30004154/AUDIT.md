# Independent mathematical audit: exact higher-order matrix decomposability

Date: 21 October 2026. Catalogue row 1834, ID 30004154. Verdict: **PASS as restricted results and counterexamples; not a solution of the unrestricted original problem.** No mathematical correction was required. No queue edit or publication was performed.

## Accepted claims

1. **Range reduction and finite-ray LP.** In any PSD rank-one decomposition of Q, every factor is orthogonal to ker Q. For Q=BB^T with B full column rank, application of a left inverse gives reduced target I. Intersecting each coordinate support with range B is therefore exact, not a relaxation. When every reduced support kernel has dimension at most one, there are finitely many rays and a scalar nonnegative linear feasibility problem. Conic Caratheodory bounds a feasible certificate by r(r+1)/2 rays. A compressed separating H need not itself be an ambient dual certificate, a distinction correctly retained in the drafts.

2. **Generic critical rank.** Row-full-spark, not merely full column rank, implies minimum nonzero range support n-r+1. At k=n-r+1, every omitted r-1 rows define a line. Hence the LP applies at r=n-k+1. This is a lower bound and a boundary test, not an assertion that every full-spark matrix attains that factor width. The negative rank-two example explicitly shows nonattainment.

3. **Complete real rank-two test.** After deleting zero rows, a nonzero reduced vector either annihilates exactly one parallel row class or no rows. Keeping precisely classes of multiplicity at least N-k is correct. The normalized rank-one matrix identity gives the doubled-angle convex-hull condition, including boundary antipodes; an open semicircle is the correct forbidden set. Three terms suffice; two terms occur exactly for an eligible perpendicular pair in whitened coordinates. The rational target-G version correctly uses G^{-1}-orthogonality. Neither arbitrary ambient rotations nor arbitrary reduced right-coordinate changes preserve the unmodified test. The complex/real limitations are stated correctly.

4. **Rational n=4,k=3 counterexample.** Independently reconstructed Q from B and Y from the displayed integer matrix. Every listed principal minor of orders one through three matches exactly and is positive. The pairing is -1/4. The normalized Gram's two nonzero eigenvalues are 72/25 and 28/25, with all entries positive. The spectral necessary condition is therefore strictly insufficient.

5. **Positive-definite perturbation.** Q+I/1000 is positive definite; independent Sylvester-minor checks pass. Its pairing with Y is exactly -12781/52000. Normalization leaves diagonal entries one and strictly decreases positive off-diagonal entries, so Perron monotonicity gives normalized spectral radius at most 72/25. The alternative Loewner proof in the draft also works. This establishes a full-rank failure of the candidate spectral characterization, not a failure of the existing generic SDP.

6. **All-k spectral counterexamples.** For k>=3, n=k+1, p=ceil(n/2), q=floor(n/2), take p rows (1,3/4) and q rows (1,-3/4). Only the two perpendicular-to-row lines can produce non-full support, and each projector has diagonal ratio 9/16, so their nonnegative cone cannot contain I_2. Hence fw(Q)=n. The normalized positive matrix has within-class entries 1 and cross-class entries 7/25; its maximum row sum is p+7q/25=n-18q/25. Since q>=2, this is at most n-36/25<n-1=k. This proof is uniform in k. These repeated-row matrices are not full-spark; no full-spark claim should be attached to this particular family.

7. **Schur complement obstruction.** With v=(1,1_{k-1},0_{k-1}) and w=(1,0_{k-1},1_{k-1}), Q=vv^T+ww^T belongs to FW_k. Eliminating the first coordinate gives exactly zz^T/2, with z=(1_{k-1},-1_{k-1}). The rank-one range lemma forces factor width 2k-2>k for k>=3. Thus scalar Schur-complement closure genuinely fails. A positive scalar pivot is present; no pseudoinverse or singular-pivot convention is needed.

8. **Symmetric slice.** The common block diagonal d/binomial(n-1,k-1) and off-diagonal c/binomial(n-2,k-2) sum to the intended matrix. The two block eigenvalue inequalities reduce to the stated positive-c and negative-c conditions. For c>=0 the dual kI-J gives necessity. For c<=0, PSD gives d+(n-1)c>=0 and the construction is sufficient. This is credited as known, not novel.

## Source and scope audit

The recovered OWR report, printed p.1595, explicitly asks for conditions for exact higher-order decomposability. I separately inspected the recovered companion manuscript's Appendix A: equation (37) is already a residual-minimizing SDP, and its surrounding prose states both the zero-optimum exactness criterion and extension to general k. Accordingly, generic SDP feasibility cannot count as resolving the intended open problem.


The research credits factor-width literature and explicitly identifies the rank-two convex geometry as scalable-frame/diagram-vector theory. No priority claim is established by these independent deductions. The Shaked-Monderer January 2027-issue paper is not excluded merely because of its issue date: accessible preview inspection is recorded, but no full PDF was inspected, and full overlap remains unverified. No exhaustive-literature or current-open-status claim is certified by this audit. Source PDFs, source text and corpus records remain separate from the authored audit.

## Reproducibility

Independent replay: `python replay.py`.

This script does not import author code. It checks the displayed dual, every listed minor, both pairings, normalized nonzero spectrum, PD principal minors, the positive three-term example, a zero-row plus repeated-parallel-row regression case, exact symmetric boundary constructions, Schur identities for k=3..11, and repeated-row spectral counterexamples for k=3..30. Finite sample checks complement, rather than replace, the uniform proofs above. Both author scripts were also rerun successfully. SymPy is required for the independent script; the author's low-rank script uses standard-library rational arithmetic.

The independent replay transcript is `replay.txt`; `replay.json` records the earlier certificate-only structured run. Author replay transcripts are `author_exact_replay.txt` and `author_low_rank_replay.txt`.

## Audited draft hashes

- RESEARCH.md: 0610c251844cd5228c89af2e3be45230b3373dc8f1bc07b1f5f3d8901c1ec1c6
- LOW_RANK.md: d1066a369fa256b789252adebc118305315389e635d483c26ecd0981a2f9fcc4
- verify_exact.py: cc0bda2f22be11b75b725af51848d225d2108545c4f3bbf65b5ac1b53cf34cb1
- verify_low_rank.py: 333f504e6ae0d4c7abbe92320af4aa16bdce668b3efe0b985dd54d498c336e7a

These hashes identify the inspected versions. Later edits require checking their changed claims.
