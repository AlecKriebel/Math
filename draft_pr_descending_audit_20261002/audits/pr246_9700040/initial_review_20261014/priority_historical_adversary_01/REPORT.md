# Historical priority audit: finite piles, random ranks and Hammersley layers

UTC report: 2026-10-15T04:06:43.516429+00:00. Scope completion: 100% of this assigned historical family; historical worldwide firstness and proposer acceptance are not claimed.

The strongest verified finding is **automatic complete prior coverage by a published2001 finite determinant**, after an explicit geometric equivalence. This is materially stronger evidence than citing old RSK ingredients or the old two-particle calculation. The parent reports independent confirmation of the corrected equivalence; its separate verification belongs to the parent audit. This artifact includes a correction prompted by root adversarial review and preserves the superseded original.

## Exact target and criteria

The target is the unique finite-prefix-consistent stationary law for positive ordered particles, drift dX_i/dt=X_i, unit space-time PPP events, nearest particle strictly right of an event jumping to it, and events beyond the last tracked particle ignored. The descriptive source is Aldous's February2018 problem page. A complete law must specify all simultaneous finite threshold probabilities. A historical source may cover the law by a direct exact equivalence without literally naming the later problem. A conclusion that a source explicitly resolved that later question needs separate textual evidence.

The candidate at parent-supplied head0b4db59eb5515f2d90d8b8df33b6b729b78b48f1 supplies positive Poissonized nested-shape factorial-determinant sums and rational truncation. Its PROOF.md explicitly disclaims novelty. This report does not attribute a firstness claim that the candidate did not make; it assesses mathematical contribution and missing prior credit.

## Verified source findings

| Mechanism/source | Exact mathematical coverage | Exact gap or limit |
|---|---|---|
| Aldous–Diaconis1993, printed36–37, equations(40)–(42), Lemma33 | Same drift/jump model; joint stationary representation X_i=Gamma(B(i)); finite-deck rank compatibility; coupling uniqueness. | The draft does not display a convenient general joint B distribution and contains a sign/time-origin defect in its displayed transformation. Its stationary representation is independently reidentified here. |
| Same notes, printed39, equations(45)–(48) | First particle and two-particle density. | Two coordinates alone do not specify the full law. |
| Same notes, printed9–10, and Aldous–Diaconis1999, printed418–419 | Uniform permutation RSK, first insertion row equal to pile tops, tableau dimension formula. | An old one-time LIS formula alone is insufficient; coherent value restriction must be checked. COHERENT_RANK_DERIVATION.md supplies that check. |
| Aldous–Diaconis1995, author-PDF internalpages5–7, especially internalpage6 after Rule2 | Empty-boundary increasing-path count and the arbitrary-initial-configuration variational formula. | Ordinary spatially stationary Poisson Hammersley configurations are a different law. The drift change and reflected boundary must be identified explicitly. |
| Aldous–Diaconis1999, section5.2, printed427 | Fixed-left-pile rescaling and recurrence/CLT framework. | It does not display a general joint stationary threshold formula there. |
| Levikson–Rolski–Weiss2001, printed420,423,425, equation(2.4), Theorem2.5 | Explicit finite determinant for the no-jump probability of the last finite Hammersley particle from arbitrary ordered initial positions. | This is not superficially a simultaneous stationary threshold formula; the exact reflected-initial-row equivalence is proved below and in the dedicated artifact. |
| LRW2001, printed432, Proposition2.9 | Joint no-jump events for selected particles. | It is not directly the stationary threshold event. Using all tracked no-jump events would give the wrong two-coordinate formula. |
| LRW2001, printed434–435, Theorem3.2 | Single-layer marginal as a Toeplitz/Bessel determinant. | The diagonal marginal alone is not the full-law evidence. The earlier off-diagonal Theorem2.5 is the relevant complete covering result. |
| Levikson–Rolski–Weiss1999, *On a Poisson hyperbolic staircase*, primary publisher abstract | One layer's time-indexed finite-dimensional distributions. | Time indices for the first layer are not simultaneous particle-index coordinates. Not used to prove all-law coverage. |

Whole primary bytes for the four Aldous items were independently retrieved again and matched the supplied pins exactly. LRW2001 was retrieved from its primary journal archive and inspected in original page images, including all determinant/event pages above. The source-search ledger records exact URLs, dates, pins, methods and failures; full PDFs, extracted text and renders remain private reading copies excluded from the authored manifest.

## The complete prior covering equivalence

Define, for integer a,

    l_a(z)=sum_{s>=max(0,a)} z^s/[(s-a)! s!],
    H_m(z_1,...,z_m)=det[l_(i-j)(z_j)]_(i,j=1..m), H_0=1.

LRW2001's published result is

    P_y(Y_k(t)=y_k)=exp(-t y_k) H_(k-1)(t y_1,...,t y_(k-1)).

For 0<x_1<...<x_k, set y_j=x_k-x_(k-j), x_0=0. Then the target law satisfies

    P(X_i>x_i for all i)
      =exp(-x_k) H_(k-1)(x_k-x_(k-1),...,x_k-x_1).

The checkable bridge is as follows. An empty-boundary PPP layer count gives X_i>x_i iff the prefix rectangle of widthx_i has increasing-chain length at mosti-1. For an initial increasing rowy, unrestricted patience sorting with that virtual prefix has

    U=max_{j=0,...,k-1}[j+L((y_j,x_k)x(0,1))]

pile tops belowx_k; the finite prefix has min(k,U) such particles. The last particle stays at its initial valuex_k iff U<k. Rotating the rectangle by180 degrees turns these suffix-chain bounds into exactly the original prefix-chain bounds in reverse index order. Thus the published last-no-jump determinant evaluates every joint stationary survival probability. Ordering and continuity handle missing coordinates, ties, zeros and arbitrary query order.

LRW2001_ALL_JOINT_EQUIVALENCE.md contains the full deterministic argument, rate/drift identification, boundary analysis, exact source locators and historical limits. The incorrect original assertion that no extra unrestricted pile could appear was caught by root review, preserved in history/, and replaced with the finite-prefix capmin(k,U). The event equivalence did not change. The negative control y_1=2 followed by1/2,1 creates two unrestricted piles and one finite particle, confirming why this cap is necessary.

The independently written lrw_reflection_check.py uses exact rational arithmetic and no candidate imports. It verifies coefficients through degree7 for rational threshold vectors of lengths2,3,4,5 and tests11,534 finite configurations pathwise. All pass, including the added negative control. This validates conventions; the proof establishes the general equivalence.

## A second complete route already implicit in the1993 construction

The B law is fully specified algorithmically by old finite-deck compatibility: for b=(1=b_1<...<b_k=N), its joint mass is the count of permutations of sizeN with complete final pile-top rowb divided byN!. RSK makes that count a finite hook-weighted count of tableaux with specified first row. The omitted rank mass after cutoffN is exactly P(L_N<k), itself a finite RSK sum, bounded bymin(1,(k-1)^(2N)/N!) for k>=2. Mixing independent Poisson arrival positions at these ranks gives every joint probability with rigorous error control. Therefore calling B an unspecified probabilistic input overstates the historical gap; the source lacked a convenient displayed general formula, not a definition of the joint law.

COHERENT_RANK_DERIVATION.md also derives exactly the candidate nested-shape weights from this historical joint construction by value-restricted insertion tableaux, with no unsupported Markov assumption. Independent exhaustive enumeration through eight cards checks complete row histograms, hook dimensions,255 compatibility equalities, the old second-rank mass and tail inequalities. This confirms a fully automatic covering combination even without the stronger2001 determinant.

## Scope recommendation

The candidate may remain mathematically correct and useful as a positive-series and certified-arithmetic exposition. It should credit the2001 off-diagonal no-jump determinant and identify its complete stationary-law consequence before promotion. The broad simultaneous stationary law should not be presented as a new discovery. The exact historical statement supported here is **earlier complete covering description via an explicitly proved equivalence**, not evidence that LRW stated Aldous's2018 question, that its authors claimed to solve it, that the proposer accepted it, or that no still earlier equivalent formula exists.

Under the source's qualitative request, a finite determinant in explicitly defined entire functions is substantial evidence of an already available fairly explicit description. Acceptance of that interpretation is the parent audit's decision. The posted page remaining online supplies neither proof of novelty nor a refutation of the equivalence.

No external communication, provider writes, Git/index/ref changes, commits or pushes were made by this family. No other priority-family files or chats were read before independent reconstruction, and no sibling chats were consulted afterward. Parent messages supplied later leads; this report's substantive2001 lead and finite-rank reconstruction were independently developed and authenticated within the assigned family.
