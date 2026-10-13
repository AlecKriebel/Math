# Independent dynamical adversarial review

**Verdict: PASS within the exact abstract ordered-pair scope.** Blocking issues: **0**. Required repairs: **0**. Unresolved mathematical gaps in that target: **0**.

Reviewer: `/root/pr462_dynamical_adversary`. PR: **462**. Problem: **30005528 / OWR-13750333-009**. Frozen head: `3d5701d67e18745715d384c3db3fbee588b42a98`. Review completed 2026-10-12 UTC. This review makes no original-priority determination and no packing-realization claim.

## Inputs, independence, and exact target

Read root AGENTS.md, SOURCE_RECEIPT.json, frozen release PROOF.md, and frozen release SOURCE_GATE.md. The proof and source-gate bytes and SHA256 match the receipt: proof 5,592 bytes / `8bed828b7f0856e049691e282a2df84fc795957b4c3116a9142ef6d8bf84e56f`; source gate 1,904 bytes / `993c98811010767c73cea29a7cd93800abaad1c39e12a1bb9bd0c838ed5fb75e`. Independent hypotheses were recorded in RESEARCH_LOG.md before any peer or historical audit. Neither historical audits nor peer reviews were read. No original proof-search turns, proof edits, git operations, service operations, publication, or external-individual communication occurred.

The official [OWR report](https://ems.press/content/serial-article-files/47016), printed p.1254 / PDF page 60, was inspected as extracted text and a locally rendered image. Definition 1 uses ordered-pair tiles, matching endpoints, and the displayed N+1-symbol numerator divided by N. Question 1 asks for an infinite compact topological alphabet with continuous positive size, with every periodic sequence strictly above the infimum. Its separate Remark 4 motivates a packing problem; Question 1 itself adds no packing-realization restriction. The rendered page is private review material and is excluded from the public manifest.

The target is therefore existence of the stated abstract game, not equivalence to a distance-restricted packing. Extra properties claimed by the proof (connected metric alphabet, closed relation, attained minimum, dense periodic starting points, exclusion of eventual periods, and the explicit bounded-period estimate) were also checked.

## Reconstruction from the definitions

Let alpha be irrational and let X = S^1 x [0,1], c(z,t) = 1+t, and F(z,t) = (exp(2 pi i (alpha+t))z,t). Take the tile relation to be the graph of F.

**The topology and positivity are valid.** Both factors are compact connected metric spaces; their product is infinite, compact, connected, and metrizable. The size is continuous and lies in [1,2], so it is strictly positive. F is continuous, preserves height, and has continuous inverse (z,t) -> (exp(-2 pi i (alpha+t))z,t). Its graph is a continuous image of compact X into the Hausdorff product X x X, hence compact and closed. In particular there is exactly one successor and one predecessor for each symbol.

**Every legal sequence is exactly a forward orbit.** Write its first symbol as x. The first tile must be [x,Fx]. The endpoint-matching condition forces the next first symbol to be Fx, and its second symbol to be F^2 x. Induction gives tile j equal to [F^(j-1)x,F^j x]. Conversely these tiles always form a legal sequence. This establishes a bijection between starting symbols and legal one-sided infinite sequences and leaves no nondeterministic legal competitor unexamined.

**The average statement holds for every real height.** Height is an F-invariant continuous function, so every symbol in the orbit starting at (z,t) has size 1+t. At length N the numerator has N+1 terms. Its quotient is (1+1/N)(1+t), with difference (1+t)/N from 1+t. The difference is at most 2/N, uniformly over all real t in [0,1]. Thus every orbit has an ordinary limit, which agrees with the source's limsup, and equals 1+t. No rationality, equidistribution, or finite sampling enters this argument.

The minimum is 1 and is attained precisely by every starting point in the bottom circle S^1 x {0}. This verifies attainment and characterizes all minimizing legal sequences.

**Tile periods are point periods, including eventual periods.** For any p >= 1, periodicity of all tiles implies that tile 1 and tile p+1 agree, hence their first symbols give F^p x = x. Conversely this point equality implies F^(j+p)x = F^j x for every j, so both components of each tile repeat with period p. Direct iteration gives F^p(z,t) = (exp(2 pi i p(alpha+t))z,t). Since z is on the unit circle and is nonzero, F^p(z,t) = (z,t) is equivalent to p(alpha+t) being an integer.

It follows that a legal sequence is periodic if and only if alpha+t is rational. If alpha+t = a/b in lowest terms with b > 0, the least period is exactly b: integer p times a/b is an integer if and only if b divides p. There is no extra identification or quotient in the ordered-pair alphabet.

If the tile sequence is eventually periodic, there are m >= 0 and p >= 1 with F^(m+p)x = F^m x. Applying the already established inverse F^(-m) gives F^p x = x. Therefore eventual periods coincide with periods in this construction. At the bottom, alpha+t = alpha is irrational, excluding every period and eventual period. Every periodic sequence consequently has t > 0 and average strictly greater than the attained minimum 1.

**Periodic competitors are dense throughout the whole alphabet.** Their heights are (Q-alpha) intersect [0,1]. Rational density in [alpha,alpha+1], interpreted in the relative topology, makes this height set dense even at both endpoints. At each such height every phase z is periodic. Every product neighborhood therefore contains a periodic point. Taking rational rotations decreasing to alpha gives positive heights decreasing to zero, and hence periodic averages tending to 1. Irrational alpha means neither endpoint rotation alpha nor alpha+1 is rational; endpoint density does not require periodic endpoint points.

## Independent invariant-measure check

This is an alternative mechanism for checking the minimizing obstruction, not an imported theorem about periodic optimization. For any F-invariant Borel probability measure mu on X, the continuous cost has integral

    integral(c dmu) = 1 + integral(t dmu) >= 1.

Equality requires mu(t >= 1/k) = 0 for each positive integer k (otherwise the second integral is positive), hence mu is supported on the bottom circle. Normalized circle length measure on that circle is invariant under its rotation and has cost integral 1. Every measure supported on a finite F-orbit instead lies at one height t > 0, so its cost integral is 1+t > 1. This checks both existence of a minimizing invariant measure and impossibility of a periodic minimizing measure independently of a finite computation.

The relation between this measure check and the sequence target is fully justified here: every sequence has the invariant constant cost proved above, and actual bottom-circle orbits exist. No unsupported principle identifying arbitrary minimizing measures with realized sequences is needed.

## Bounded periods: a separate compactness mechanism and the universal estimate

For each Q >= 1 define P_Q as the union, over 1 <= p <= Q, of Fix(F^p). Every Fix(F^p) is closed because F^p is continuous and X is Hausdorff. Thus P_Q is compact. It is disjoint from the bottom circle by irrationality, so the continuous height function has a strictly positive minimum on P_Q whenever P_Q is nonempty. In this game P_Q is nonempty even for Q=1, since an integer rotation exists in the interval [alpha,alpha+1]. This proves a positive bounded-period cost gap using topology rather than a Diophantine search. It also identifies the failed compactness inference: the union over all p of Fix(F^p) need not be closed, although each fixed-period set is closed.

The explicit estimate for alpha = sqrt(2) is universally correct. For a periodic height, write r = sqrt(2)+t = p/q in lowest terms. Here r > sqrt(2), r <= sqrt(2)+1, and p,q are positive integers. Therefore p^2-2q^2 is a positive integer, at least 1, and

    t = (p^2-2q^2)/(q^2(r+sqrt(2)))
      >= 1/((2sqrt(2)+1)q^2)
      >= 1/((2sqrt(2)+1)Q^2)   if q <= Q.

All denominator inequalities are in the correct direction and denominators are positive. This proves the displayed frozen estimate for all least periods and all real permitted heights, not only sampled rationals. Any sequence of periodic averages approaching 1 must have least periods tending to infinity. In particular unbounded period is a necessary escape from each compact P_Q.

## Explicit competitors and annulus coordinates

For every integer n >= 1, n sqrt(2) is nonintegral. Thus m = floor(n sqrt(2))+1 obeys m-1 < n sqrt(2) < m, and t_n = m/n-sqrt(2) obeys 0 < t_n < 1/n <= 1. Its rotation is m/n, with least period n/gcd(m,n); this is often smaller than n (n=4 gives m=6 and least period 2). Hence these are actual legal periodic competitors, their costs tend to 1, and none is a minimizer. Neither floating-point ceiling nor unreduced period is used in the independent controls.

The annulus map H(z,t)=(1+t)z has continuous inverse H^(-1)(u)=(u/|u|,|u|-1) for 1 <= |u| <= 2. It is a homeomorphism. Conjugation gives H F H^(-1)(u)=exp(2 pi i (sqrt(2)+|u|-1))u, and the cost becomes |u|. This verifies the claimed planar form, closed tile graph, strict positivity, and all periodicity and cost claims under that coordinate change. The domain excludes zero, which is essential to cancel the phase in the point-period argument.

## Adversarial checks and reproducible artifacts

`dynamical_controls.py` is self-owned, standard-library-only code, independent of the released checker. It uses integer square roots and exact Fraction arithmetic, including exact comparison of a+b sqrt(2) by sign and rational square comparisons. It deliberately contains no Python assertions as acceptance gates.

Both normal and optimized (`-O`, optimization level 1) runs passed with `/opt/homebrew/bin/python3`, recording interpreter/version and script hash in `controls_normal.json` and `controls_optimized.json`. Each checked 10,003 prescribed approximants, including n with 31, 61, and 121 decimal digits; 12,232 reduced rational rotations with q <= 200 and all smaller candidate periods; four exact rational-phase tile models; and 16 finite averaging cases. The analytic proofs above certify universal claims. The finite controls certify implementation arithmetic within the reported range.

Six deliberately false/corrupted controls were rejected in both modes: dropped +1 in the numerator, confusing n with its reduced denominator, invalid n=0, a false tile period, corrupted endpoint matching, and an unconditional false predicate. These controls demonstrate that rejection logic remains active under -O. Invalid data is constructed in memory; no invalid fixture is public.

Additional mathematical boundary attacks give the expected failure modes without undermining the frozen proof: rational alpha would allow periodic bottom minimizers; adding the planar origin would prevent cancellation of z; changing size to t would violate strict positivity; and sampling only rational heights would miss the periodic heights, because their defining difference rational-minus-sqrt(2) is irrational. The released construction makes none of these alterations.

## Exact remaining gap and limitations

There is **no unresolved mathematical gap in the frozen abstract ordered-pair counterexample or its stated robustness properties**. Every legal sequence, every real height, every finite or eventual tile period, both interval boundaries, reduced denominators, topology, positivity, and annulus conjugacy are accounted for. The bounded-period statement is a universal deduction independently corroborated by a compactness argument.

This review does not establish historical novelty, does not reproduce the released computational script, does not realize the graph as an interval-packing relation, and does not resolve the stricter packing conjecture. These are outside the frozen target, not missing premises of its proof. No numerical approximation or unverified external mathematical theorem is needed for the verdict. Private downloaded PDF and rendered image are excluded from PUBLIC_FILES.json. Only positive-listed, self-authored report, log, checker, result, and exact-control output files are public.
