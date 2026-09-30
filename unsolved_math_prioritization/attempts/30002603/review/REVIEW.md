# Independent review: 30002603, linear shape edges under a discrepancy-tail condition

**Verdict: PASS_SCOPED_SUMMABLE_DISCREPANCY_LINEAR_EDGE_THEOREM. No mandatory correction.**

Reviewed PARTIAL.md SHA-256:
\[
\texttt{b4967d2db1f98b67ae458b7bd65c1eb21f32f08b47be917947dce9058ca0b4c9}.
\]

The sufficient condition
\[
\sum_{k\ge1}\sqrt{p_k\log(e/p_k)}<\infty
\]
does imply the claimed linear shape edges for the stated fair-sign model. The logarithmic endpoint-density corollary with exponent \(p>3/2\) follows. The general temporal law and uniform-density case remain unresolved. Recommended status: **unsolved, 1/5**. This is an independent AI audit, not a human peer review or historical-priority certification.

## 1. Source and exact scope

I read the original contribution in [OWR 28/2014, printed pp.1542–1543](https://ems.press/content/serial-article-files/46518), including the rendered conjecture page. Its lazy-path product environment, independence assumptions, density condition on the product potential and mean-zero temporal factor match the submitted account. Its simultaneous corner and linear-piece discussion supports the two one-sided intervals in the statement. Nothing here settles its full temporal-law range or the separately discussed two-field model.

I checked [BKMV, arXiv:2310.08379v2](https://arxiv.org/pdf/2310.08379v2), Theorems 2.1–2.4, Remark 2.5, the shape argument and Section 4's deletion mechanism. The theorem page was visually inspected. The cited result assumes a positive endpoint power for its linear-edge theorem; the submitted logarithmic density does not satisfy that hypothesis. The mechanism and prior theorem are credited. The accepted/in-press bibliographic qualification is preserved; this audit uses the exact v2 source and does not certify an independently compared final journal edition.

## 2. Shape existence and conditional limits

The source's endpoint-power assumption is not silently imported into the weakened setting. The submitted argument supplies the needed replacement:

- Nonzero rational directions have a stationary mixing joint time/space shift. Finite cylinder events eventually depend on disjoint coordinates in both iid fields. Bounded actions supply the subadditive integrability and lower bound.
- At zero slope, independence on disjoint spatial edges and positive endpoint-tail probabilities provide a finite favorable edge almost surely. Laziness allows arbitrary consecutive fair signs to be followed on that edge. Travel and return costs are bounded independently of the time horizon.
- The deterministic cone comparison extends rational limits inside the cone. For continuity at a ballistic boundary, a path ending near that boundary has only \(O(\epsilon T)\) non-East steps. Its deterministic first-visit terms use distinct spatial variables and distinct temporal signs, so the independence needed for the concentration/entropy estimate holds.
- The first-visit lower bound yields the stated strict slope bound \(K\ge c-\mathbb E|F(0)|>0\).

The conditional expectation assertion does not require an illicit uncountable Fubini intersection. First take a common event for the countable rational directions, then use the deterministic monotonicity of \(A^*(T,n)-cT\) to squeeze every horizon sequence. Continuity at \(t=1\) was established separately. Bounded convergence applies to these bounded normalized actions. Intersecting with the countably many discrepancy ergodic events is legitimate: the discrepancy process is a finite-range function of an iid field, hence ergodic, although its coordinates are not independent.

These points also justify use of this fixed spatial realization for the adaptive loop lengths later in the proof.

## 3. Uniform entropy estimate and deterministic temporal choice

For a deterministic retained set, changing one retained sign changes the minimum by at most \(2c\). McDiarmid's two-sided inequality therefore gives the stated exponent with denominator \(2c^2N\).

The endpoint-list count is a valid overcount of all sets obtained by deleting at most \(m+1\) intervals. With \(q=m+1\), substituting
\[
a_n(m)=2c\sqrt{N\{q\log(e(N+1)/q)+4\log(N+1)\}}
\]
cancels the exponential endpoint count and leaves
\(2(m+2)^2(N+1)^{-8}\le2(N+1)^{-6}\).
Summing over \(m\) gives the claimed vanishing failure probability. The additive logarithmic term explicitly covers \(m=0\).

The bound holds simultaneously for every retained set. Thus selecting sets from a minimizing path after seeing the signs creates no independence problem. The full-path concentration, conditional expectation limit, and adjacent-pair law have intersection probability tending to one, which is enough to select the deterministic sign sequence separately for each \(n\).

The limit
\[
a_n(m_n)/n\longrightarrow
2c\sqrt{\ell\delta\log(e\ell/\delta)}
\]
is correct also at \(\delta=0\), using \(x\log(1/x)\to0\). This error function is increasing on \([0,1]\).

## 4. Loop geometry and action inequality

The spatial one-dimensionality is used correctly. Removing the initial origin loop and terminal endpoint loop confines the remainder to \([0,n]\). At later stages, a first-to-last visit loop cannot contain a previously processed site, since it would need to visit that site again to return. An earlier removed interval cannot lie inside a new loop either: its retained initial endpoint is such a processed site. Therefore each removed piece is indeed a disjoint interval in original time.

The final retained path visits each site \(1,\ldots,n\) once and has length \(n\). For a nonoverlapping \((-1,+1)\) pair inside an interior loop, laziness gives the discrepancy lower bound, and the ordering ensures the discrepancy is at least that of the loop's selected site. The endpoint loops require only the unweighted bound.

A sign pair not internal to one of the removed intervals crosses a boundary of the interval/singleton partition. There are at most \(2(n+1)\) such boundaries, so the pair-count loss is valid.

Most importantly, equation (11) needs only the cost of an admissible compressed path as an upper bound for the new minimum. The proof never assumes that this path remains optimal. The submitted formulation is sufficient throughout.

## 5. Finite-level summation, diagonal choice and affinity

The sign of the key concavity inequality is correct:
\[
\ell\Lambda(1/\ell)-c(\ell-t)\ge t\Lambda(1/t).
\]
Combined with the lower concentration bound and the action upper bound, it forces the weighted discrepancy cost to be at most the entropy error.

The discrepancy-level argument first sums only finitely many levels. Each index in level \(k\) is counted \(k-1\) times, and its weight exceeds \(2c/k\), giving at least \(c\) times its pair count for \(k\ge2\). The infinite series is used only to bound these finite sums uniformly:
\[
M_\ell\le2\sqrt{\ell}\bigl(1+\sqrt{\log\ell}\bigr)S=o(\ell).
\]
There is no unproved exchange of a limsup with an infinite series.

For each fixed level \(h\), the spatial frequency limit and the finite-sum bound hold eventually. Choosing increasing sufficiently large thresholds in \(n\) yields \(h_n\to\infty\), \(m_{n,h_n}/n\to0\), and the stated uniform complement-pair bound. This elementary diagonal selection is valid. A sufficiently large integer \(\ell\) leaves a positive linear quantity of early-loop pairs, hence removes at least \(\ell n/6\) times.

The resulting subsequential retained-length limit satisfies \(1\le t\le5\ell/6<\ell\), with vanishing concentration error. The action comparison forces equality in the above concavity inequality. Equality at the strictly interior point \(1/\ell\) of the chord from \(0\) to \(1/t\) forces a concave function to be affine on that chord. Evenness and the positive slope bound give exactly the asserted two-sided formula.

## 6. Endpoint-density corollary and unresolved cases

For \(0<h\le c\), low discrepancy forces the central variable into the upper endpoint tail and at least one neighbor into the lower tail. Independence gives the product-tail bound. The logarithmic density bound then yields
\[
p_k=O\!\left(k^{-2}(\log k)^{-2p}\right),\qquad
\sqrt{p_k\log(e/p_k)}
 =O\!\left(k^{-1}(\log k)^{1/2-p}\right).
\]
The last series converges for \(p>3/2\). The proposed normalized density is finite, positive and continuous in the interior and vanishes more slowly than every positive power at its endpoints.

As a separate exact diagnostic, for uniform \(F\) on \([-c,c]\) I obtain
\[
p_k=\frac1{k^2}-\frac1{3k^3}\quad(k\ge2),\qquad p_1=1.
\]
The modified discrepancy has an atom of mass \(1/3\) at \(2c\), corresponding to the central value being the smallest of the three samples. This confirms the distinct \(k=1\) convention and the divergence of this sufficient criterion for the uniform density. That divergence says nothing about whether the actual uniform-density shape has a linear edge.

## 7. Reproduction and publication disposition

All **128,070** author assertions replayed with a byte-identical receipt. The independent standard-library checker passes **27,814** exact assertions, including longer paths with arbitrary interior deletion order, independent dynamic-programming minima, all small retained-set counts including \(m=0\), exact finite-level inequalities, the uniform-tail formula and atom, endpoint containment, and time-extension monotonicity.

These checks do not prove an infinite-volume probability theorem. The concentration, shape, diagonal and summability arguments were separately audited above.

The artifact is suitable for a scoped partial-result PR with the frozen mathematical text and the eight listed review files. Preserve **unsolved, 1/5**, the fair-sign restriction, the general and uniform-density gaps, the attribution to BKMV, and the unconfirmed priority statement. No mathematical revision is required.

