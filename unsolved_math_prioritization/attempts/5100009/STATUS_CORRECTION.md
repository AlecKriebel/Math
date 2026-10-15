# 5100009: k118 is a published theorem

**Proposed disposition: `already_solved`, 0/5 substantive author turns.**
This is a source-status correction, pending separate review, not a new proof or a novelty claim.

## Exact target and table identity

Let a nondegenerate periodic billiard in an ellipse with semiaxes a>b>0 have odd period N, with its sides tangent to a fixed strict confocal ellipse. Write Q_i for the caustic contact on the traversed chord P_i P_(i+1). The imported quantities are ordinary positive Euclidean lengths

    l_i = |P_i-Q_i|,   r_i = |P_(i+1)-Q_i|,
    L = sum_i |P_(i+1)-P_i|.

The full target is that both sums equal L/2 and are constant along the family.
Both the arXiv v11 Table 2 (p. 5) and the final Table 2 (p. 345) retain code k118, odd N, and value L/2. Their Section 3.1 definitions agree with the imported lengths. Both tables credit Hellmuth Stachel with discovery. Changes to neighboring row labels do not change this target.

There is no angle in this invariant. The angle and signed-area notation in the imported setup is unused. Lengths are not signed, and a star is traversed in billiard order rather than sorted by boundary position. The outer and inner polygon areas also play no role.

## Published resolution and precise transfer

Hellmuth Stachel, *The geometry of billiards in ellipses and their Poncelet grids*, **Journal of Geometry 112, article 40 (2021)**, DOI [10.1007/s00022-021-00606-2](https://doi.org/10.1007/s00022-021-00606-2), Theorem 4.5, p. 24, explicitly identifies k118 and states the required two half-perimeter sums. Lemma 4.4 on the same page establishes perimeter invariance.

Stachel's equation (3.1), p. 6, uses l_i=|P_i Q_i| and rho_i=|P_i Q_(i-1)|. Thus imported r_i=rho_(i+1); cyclic summation removes this indexing difference. His odd-period congruence is l_(i+n)=rho_i for N=2n+1.

The printed proof invokes conjugate billiards, Lemma 3.11 / equation (3.13), and Corollary 4.2. The latter treats both odd and even turning number, so it covers primitive odd stars as well as convex orbits. These are published inputs, not newly proved lemmas in this packet.

## Scope and audit cautions

For least period N, retain the standard coprimality condition gcd(N,tau)=1. No assumption tau=1 is made. If an N-term traversal repeats a shorter orbit and N is odd, its least period is also odd; all three length sums scale by the repetition count. This elementary interpretation does not create a further invariant.

The source list's confocal pair is elliptical. We do not extend the result to degenerate caustics, nonclosed chains, signed segment lengths, or even-period half-perimeter claims. A degenerate two-bounce diameter is not an odd nondegenerate orbit. In particular, no even-repeat loophole is being used. The symbol P' in Stachel's conjugate-billiard argument is not the outer tangent-intersection polygon called P' in the invariant list.

The published theorem and its proof were accessed in full, not inferred from an abstract or search snippet. The two table rows and theorem page were visually inspected. The source PDFs stay outside the portable mathematical packet; their URLs and hashes are recorded in source_manifest.json.

## Prior work and validation

The pinned upstream report classified this as OPEN-TRIAGE after an incomplete literature search. That third-party report is not an earlier Alec/campaign proof attempt. The current gate found no matching prior campaign PR, exact branch, or committed target folder. Related k117 work is credited in prior_work_gate.json; its product theorem is not used as a substitute for this sum theorem.

`python verify.py` checks cyclic indexing exactly and exercises positive segment lengths, tangency, chord partition, odd-star congruences, both sums, and perimeter invariance at high precision. These finite diagnostics cannot establish the theorem; the published result does. No original proof-attempt turn was consumed. Separate source-scope review is required before queue promotion or a claimed-resolution PR.
