# Independent theorem-to-target reconstruction

The source-first target freeze precedes reading inherited family verdicts. This reconstruction states the checkable implications used in the final whole-packet judgment; it does not infer historical explicit recognition from present verification.

## Literal target

OWR Proposition 3 assumes I(G,n) nonzero and I(G,n+1)=0. Each full numerical scenario forces MLT=n+1; together they place WMLT in {n,n+1}. A model meeting those ideal hypotheses but violating either numerical requirement disproves the universal numerical claim. A model satisfying the PD-intersection antecedent does not disprove the bare union of antecedents.

## Earlier singleton K4,4

Gross–Sullivant Section 5 gives WMLT=2 for every bipartite graph containing an edge. The construction uses a rank-one all-ones matrix on each edgeless part, then puts the parts in blocks: S=diag(J4,J4) has the same diagonal/cross statistics as the positive-definite identity. A one-observation sample has a singular observed 2x2 principal block on any edge, excluding a PD completion. Positive probability follows from continuity of completions, or directly from the candidate's open box: diagonal >=9801/10000, four cross entries each <=202/10000 in magnitude, hence strict row margin >=8993/10000.

Blekherman–Sinn Theorem 2.1 gives generic completion rank 4 because 4<=binomial(4,2)=6. Their definition is dominance of the ordinary symmetric rank<=4 projection, exactly the singleton OWR statistic map. Every polynomial in the exact elimination ideal vanishes on that dominant image, so I4=0. For I3, the observed 4x4 cross determinant is a permitted full symmetric 4-minor; substituting the statistic relations proves direct ideal membership, and evaluation at cross block I4 proves it is nonzero. No radicality assumption is involved. Since the ideals decrease with rank, this is also the first zero index.

There is a direct real submersion check independent of that theorem. At X=[I4;V], with V rows e1+e2,e2+e3,e3+e4,e4+e1, an adjoint kernel stress has form K=[diag(a),C;C^T,diag(b)]. The equation KX=0 gives C=-V^T diag(b) and diag(a)=V^T diag(b)V. Each cyclic unordered off-diagonal pair picks out one b_j, so b=C=a=0. Thus the statistic differential is surjective. Every eliminated polynomial vanishes on its real-open Gram-statistic image, hence is zero.

Theorem 2.7 independently gives MLT=min(M,5), where M is the least k with k(k+1)/2>=8. Since 6<8<=10, M=4 and MLT=4. The source's definition uses generic PSD rank and PD completion, matching the rank-indexed zero-mean convention. I inspected its proof through Lemmas 2.8–2.10; the proof distinguishes arbitrary sparse annihilators for completion rank from PSD annihilators for MLT. Its treewidth wording outside this applied branch does not supply any premise here.

Hence earlier exact coverage yields (first zero ideal,WMLT,MLT)=(4,2,4). At n=3 neither full numerical scenario holds. Moreover pi(I8) is in V(I3), through the actual rank-two PSD preimage S, so the second antecedent holds. The older splitting mechanism is the same block construction, not merely an unrelated bound. This implication requires no assertion that an older paper explicitly discussed the later OWR formulation.

For the tied model K11=K22, the statistic map is obtained by summing the first two diagonal outputs. Composing a surjective differential with that surjective output map keeps dominance; the cross determinant survives; edge 3–5 still rules out rank one. These facts prove I3 nonzero/I4 zero/WMLT=2, but do not transfer the ordinary MLT=4. Exact earlier publication of this tied example is not established by the old ordinary-graph theorems.

## Earlier equally vertex-colored C4

Take edges 12,23,34,41, one common vertex color, four distinct edge colors. The projection is (tr S,s12,s23,s34,s41) in OWR coordinates. The polynomial f=t12*t34-t23*t41 is nonzero and is directly the full 2-minor with rows 1,3 and columns 2,4 after statistic substitution. Thus I1 is nonzero.

At X=[e1,e3] in R^(4x2), the derivative of the five statistics has independent columns: x11 supplies trace derivative 2; x21,x22,x42,x41 independently supply the four edge derivatives 1. The selected minor is 2. Therefore I2=0 by the same exact-ideal real-open argument. Doubling all four edge outputs gives minor 32 and leaves every fiber and ideal-zero assertion invariant.

A feasible concentration matrix has common diagonal lambda and independent cycle edges. Direct cancellation gives

    x1(Kx)1-x2(Kx)2+x3(Kx)3-x4(Kx)4
      = lambda (x1^2-x2^2+x3^2-x4^2).

Outside the proper quadratic zero set, Kx=0 forces lambda=0. A PSD matrix with every diagonal zero is zero. Thus no nonzero PSD concentration matrix annihilates generic x. The trace statistic makes the PSD-statistic image closed: bounded statistics bound the traces, hence all entries, of PSD preimages. A boundary point would admit a nonzero supporting functional, represented by a PSD concentration matrix K, with x^T Kx=0 and therefore Kx=0. The preceding identity excludes this generically. The statistics are interior and admit a PD completion: subtract a small positive multiple of pi(I4), choose a PSD preimage, and add that multiple of I4. The standard log-likelihood compact-sublevel/score argument gives a unique MLE.

The exceptional quadratic zero set has Gaussian probability zero. Consequently MLT=WMLT=1. Rank-zero data have trace zero and cannot match PD statistics. A direct PD-intersection witness is e1e1^T and I4/4, with equal statistics. The equal-diagonal cycle Laplacian annihilating (1,1,1,1) verifies that exceptional failure remains possible; no every-sample claim is required.

This is the m=4 specialization of Homs–Kuznetsova–Stolz Proposition 3.26, using their exact Definitions 2.1–2.13 and 3.8 and Proposition 3.9. At n=1 it meets the exact original ideal hypotheses yet has MLT=1 rather than 2. Its distinct graph does not weaken coverage of the same universal numerical question. It also meets the PD-intersection antecedent and therefore supplies no counterexample to a bare SOS/intersection union.

## Disposition consequence

Both routes precede the October 1 candidate. Under the user's meaning of already_solved as an earlier-covered answer, a carefully qualified correction is defensible for the full literal numerical question. It is not a historical first-recognition certificate, an OWR retraction claim, an exact tied-model anticipation finding, or a resolution of the bare mechanism question. Completing the concrete correction designed while the PR is eligible, then immediately skipping the corrected open draft, respects the claimed_solved-only process without opening another research or publication task at the corrected status.
