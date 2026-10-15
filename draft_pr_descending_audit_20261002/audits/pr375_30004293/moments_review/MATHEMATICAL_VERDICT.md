# Independent mathematical verdict, sealed before author replay

Mathematical body sealed UTC: 2026-10-03 06:58:05 UTC (original file/sha receipt finalization time). This verdict follows independent source formulation and exact controls, and candidate mathematical prose review. At that sealing no author checker, historical review or root/sibling verdict had been read. The opening timestamp was corrected after replay using the original file modification time; all mathematics remains byte-identical to the original sealed body. The original SHA receipt is retained separately. Frozen target: commit `36c29bb039471f132889d577c9322d78925b62dd`, `snapshot/unsolved_math_prioritization/attempts/30004293`.

**Verdict:** The Turn 5 moment, rare-tail and larger-normalization logarithmic-moment claims are mathematically valid as written, conditional only where stated on the packet's explicitly proved Turn 4 uniform counting bound. I found no mandatory mathematical correction in this assigned route. The packet's status must remain **unsolved**: it does not determine a finite exponent, equality of the deterministic extended liminf/sup, or convergence in probability of \(\log M(D)/\log\log D\). Finite counts are not proof of those probabilistic limits.

## Universal proof of the moment claim

For a finite positive-integer set (B\), its (2^{|B|}\) subsets have sums among (0,\ldots,S\), with (S=\sum B\). Thus (m(B)\ge 2^{|B|}/(S+1)\). This includes the empty set, and includes zero's empty representation. It is a lower bound; separated components can create new collisions, so no reverse multiplicative identity follows.

Fix an integer (n\ge1\). Every realized (B\subseteq[1,n]\) contains 1, and
\[
 P(B_n=B)=\frac1n\prod_{i\in B\setminus\{1\}}\frac1{i-1}.
\]
Indeed factor the probabilities of all coordinates (2,\ldots,n\) absent, whose product is (1/n\), then multiply by their selected-to-absent odds. Sets omitting 1 have probability zero and are never divided by. This formula also proves the exact deletion ratio \(P(B)/P(B\setminus K)=\prod_{i\in K}(i-1)^{-1}\) for distinct selected entries (i\ge2\); it is compatible with Turn 4's reconstruction weights.

For fixed (q>0\), put (t=2^q>1\), (a=t-1\). Define
\[
 Z_n=E[t^{N_n}]=\prod_{i=1}^n(1+a/i),\qquad dQ_t/dP=t^{N_n}/Z_n.
\]
Multiplying each Bernoulli mass by its weight shows the coordinates remain independent with tilted success probabilities \(t/(i+a)\), including probability one at (i=1\). Consequently
\[
 E_{Q_t}S_n=t\sum_{i=1}^n\frac{i}{i+a}\le tn.
\]
The pigeonhole bound, change of measure, and convexity of \((s+1)^{-q}\) give the universal chain
\[
 E[M(n)^q]\ \ge Z_nE_{Q_t}(S_n+1)^{-q}
 \ge\frac{Z_n}{(1+E_{Q_t}S_n)^q}
 \ge\frac{Z_n}{(1+tn)^q}.
\]
All expectations are finite at finite (n\). No concentration assertion for (S_n\) was used. For fixed (t\), summing \(\log(1+a/i)=a/i+O_t(i^{-2})\) after finitely many coordinates proves \(Z_n\asymp_t n^a\). Thus \(E[M(n)^q]\ge c_qn^{2^q-1-q}\) eventually. The exponent is zero at (q=1\) and strictly increasing there and above since \(2^q\log2-1>0\) for (q\ge1\). It is strictly positive for every (q>1\). There is no uniformity in growing (q\) or (t\).

For (q=2\), (t=4\),
\[
 Z_n=(n+1)(n+2)(n+3)/6,
\]
so division by (n\) and the limit of the displayed coarse bound gives \(\liminf E[M(n)^2]/n\ge1/96\). An independently checked sharper finite-(n\) control uses
\[
 E_{Q_4}S_n=4n-12(H_{n+3}-H_3),
\]
and hence replaces (4n+1\) in that denominator by (4n+1-12(H_{n+3}-H_3)\). It has the same asymptotic constant, and does not claim optimality.

For real (D\), take (n=\lfloor D\rfloor\); (M(D)=M(n)\). The product denoted (Z_t(D)\) has integer indices (i\le D\), so (Z_t(D)=Z_n\). Increasing the coarse denominator from (tn+1\) to (tD+1\) preserves the bound. Since (n/D\to1\), the powers and constant also transfer. A growing cutoff is not replaced inside an event without checking its threshold.

## Universal proof of the rare polynomial-tail claim

Fix \(\gamma>0\) and \(t>(1+\gamma)/\log2\). Choose fixed \(\delta>0\) with \((t-\delta)\log2>1+\gamma\). Under \(Q_t\),
\[
 E N_n=t\log n+O_t(1),\qquad \operatorname{Var}N_n\le E N_n.
\]
Chebyshev gives \(Q_t(|N_n-t\log n|\le\delta\log n)\to1\). Markov and \(E_{Q_t}S_n\le tn\) give \(Q_t(S_n\le4tn)\ge3/4\). Their intersection (F_n\) therefore has tilted probability at least (1/2\) for all sufficiently large (n\). On (F_n\), pigeonhole yields
\[
 M(n)\ge n^{(t-\delta)\log2}/(4tn+1)>n^\gamma,
\]
and the upper count bound yields \(t^{-N_n}\ge n^{-(t+\delta)\log t}\). It follows that
\[
 P(M(n)\ge n^\gamma)\ge P(F_n)
 =Z_nE_{Q_t}[t^{-N_n}\mathbf1_{F_n}]
 \ge c_t n^{-I(t)-\delta\log t},
 \quad I(t)=t\log t-t+1.
\]
First take the (n\)-liminf with fixed (t,\delta\), then choose (t\) decreasing to (t_\gamma=(1+\gamma)/\log2\) and \(\delta\) decreasing to zero subject to the strict condition. Continuity gives exactly Turn 5's lower logarithmic tail rate \(-I(t_\gamma)\). No uniform asymptotic statement in varying (t\) is used. For real (D\), first use an integer-cutoff exponent \(\gamma'>\gamma\), since eventually \(\lfloor D\rfloor^{\gamma'}\ge D^\gamma\), and only afterwards let \(\gamma'\downarrow\gamma\). Turn 5 handles this correctly.

This is a lower bound on a vanishing-probability-compatible tail, not a positive-probability conclusion. The rate is positive because (t_\gamma>1\), (I(1)=0\), and (I'(t)=\log t>0\). Independent confirmation of the rarity mechanism: for (1<\alpha<t\), under the ordinary model Chernoff at parameter \(\log\alpha\) gives
\[
 P(N_n\ge\alpha\log n)\le n^{\alpha-1-\alpha\log\alpha+o(1)}\to0,
\]
while its probability under \(Q_t\) tends to one. Intersecting it with (S_n\le2tn\) has tilted probability at least \(1/2-o(1)\). The same pigeonhole/change-of-measure calculation contributes at least \((1/2-o(1))Z_n/(2tn+1)^q\) to the raw (q\)-moment from that vanishing ordinary-probability event. Thus the moment route's high-count weighting is an actual mechanism in this model, not merely an abstract counterexample.

## Larger-normalization logarithmic moments

Write (L=\log D\) and \(X_D=(\log M(D))(\log L)/L\). The Turn 4 explicit exceptional probability
\[
 p_D=2e^{-\epsilon L/2}+2(L+3)e^{-(\log L)^2/3}
\]
is valid for all sufficiently large real cutoffs with the stated growing parameters. On its complementary event, convolution yields
\[
 X_D\le Y_D=(\log k)(\log L)/L+(\log2)(\log L)N(D^c)/L.
\]
Here (k=\lfloor L/(\log L)^3\rfloor\), (t_0=\lceil\log_2k\rceil\), (c=(\log3-1+\epsilon)/t_0\), and \(cL\to\infty\). For a sum (N\) of independent Bernoulli variables of mean \(\mu\), the (j\)-th factorial moment is at most \(\mu^j\); expanding integer powers and applying Lyapunov for noninteger powers gives \(E N^r=O_r((1+\mu)^r)\). Variance at most \(\mu\) gives (N/\mu\to1\) in probability. Applying a strictly higher fixed moment gives uniform integrability for every fixed power, so (N/\mu\to1\) in every fixed (L^r\). This includes the deterministic coordinate 1.

Since (E N(D^c)=cL+O(1)\), it follows that (Y_D\to C_\epsilon=(\log3-1+\epsilon)(\log2)^2\) in every fixed (L^r\). For any (p>0\), Cauchy-Schwarz on the exceptional event and the unconditional (\log M\le N(D)\log2\) give
\[
 E[X_D^p\mathbf1_{B_D}]\le C_p(\log L)^p p_D^{1/2}\to0.
\]
Thus \(\limsup E X_D^p\le C_\epsilon^p\), and letting \(\epsilon\downarrow0\) gives Turn 5's (C_*^p\). Using a larger power gives uniform integrability of (X_D^p\) for sufficiently large (D\). This argument legitimately passes through expectation; it does not derive it from an almost-sure limsup alone. It bounds a scale (L/\log L\), much larger than the unresolved \(\log L\) scale, and does not assert (X_D\) converges to (C_*\).

## Cross-scope checks for the first four turns

- Turn 1 correctly fixes the subset, finite-prefix and empty-set conventions. The independent-annulus strong law, tensor lower bound and monotonic interpolation give its almost-sure lower result without a rate assumption. Fixed (r\) amplification establishes \(\beta_{k^r}\ge\beta_k^r\), so the supremum equals the large-(k\) limsup. Finite modifications multiply (M\) by at most a constant power of 2, giving deterministic extended tail liminf/sup; this does not make them finite or equal. The element/sum cutoff comparisons preserve only the leading normalized limits. The credited FGK lower threshold is a source input, not verified here by checking the entire long entropy proof.
- Turn 2 orients a relation by its largest entry and solves for the second largest, so its count does not insert an additional free factor of that entry. Independence only applies to valid distinct supports. Summability for fixed relation length and the separate uniform growing-length bound are sound. Fixed-cardinality stabilization is a finite random bound; it neither bounds unrestricted cardinality nor its expectations by a universal constant.
- Turn 3 uses only the diagonal quotient. The recorded binary vectors are independent modulo the diagonal, so residual sums determine at most one recorded tuple. Distinct coordinates imply (t\ge\lceil\log_2k\rceil\). The residual support condition follows from reading entries in descending order. The probability ratio must and does use (1/(K_j-1)\). Fixed-(k\) constants are not applied to growing (k\) in this turn.
- Turn 4 explicitly counts at most (2^{j+1}-1\) diagonal cosets, since zero and one have the same coset. Summation by parts uses residual cumulative upper counts and a single (h_t\) error. The gap follows because (h_1-1=\log3-1>0\) and all later increments minus one are negative. Its vector/bin count and geometric sum have explicit (k\)-dependence; growing (k\) leaves (t_0R=o(L)\). This supports the uniform exceptional probability used for Turn 5 logarithmic moments. It gives an upper scale (\exp(O(L/\log L))\), not a polylogarithmic exponent bound.

The first four turns' conclusions are compatible with large Turn 5 raw moments: almost-sure subpolynomial growth permits finite-cutoff moments dominated by rare paths. Fixed-cardinality bounds concern another restriction. The literal infinite supremum is unbounded, while every finite cutoff has finite moments. The packet keeps these distinct.

## Falsifiable controls and their limits

Independent code uses no candidate/checker imports and no downloaded data. It exactly enumerates 10,943 configurations over (D=1,2,3,4,5,6,8,10,12,14\), with 55,580 rational/integer assertions. It compares coefficient multiplication with a separate direct subset enumeration through (D=10\), checks complement symmetry, total subset count, exact configuration probabilities and total mass, (q=1,2,3,4\) tilted partition functions and means, all steps of the inequality chain, and the second-moment telescope. Full code, stdout, stderr and exact rational report are retained in this directory.

Two independent logical counterexamples make the implication boundaries checkable. Let (Y_D=D^2\) with probability (D^{-1}\), and (Y_D=1\) otherwise. Then \(\log Y_D/\log\log D\to0\) in probability but \(E Y_D^2=1-D^{-1}+D^3\). Its expected logarithm tends to zero. To test failure of logarithmic uniform integrability, instead let (Y_D=D^D\) with probability (D^{-1}\), otherwise 1. The same normalized logarithm tends to zero in probability, but its mean is \(\log D/\log\log D\to\infty\). These are logical controls, not original-question counterexamples or asserted laws for (M(D)\).

## Source and promotion boundaries

Reviewed original OWR contribution and FGK definitions/theorems/full Lemma 2.1 proof/remark; source identities and access hashes are in SOURCE_IDENTITY.json, with third-party bytes private. The Lemma's prefix remark already supports the elementary lower-bound scope; the literal unboundedness corollary is credited prior-result bookkeeping. The Mao-Song v2 fixed-(k\) identities/local repairs and Tenenbaum powers/polynomial results have different scopes, and neither supplies an implicit prefix upper bound or completes an independently audited set of premises here. The packet records those boundaries correctly. This review is not a novelty certification, an exhaustive literature survey, or an independent verification of the full general FGK/Mao-Song framework.

Mandatory mathematical fixes in assigned scope: **none found**. Mandatory retained disposition: **unsolved after 5/5 author turns**, with the exact quantitative gap stated above. Bounded-review completion estimate at sealing: 80%; original quantitative research target remains unresolved.
