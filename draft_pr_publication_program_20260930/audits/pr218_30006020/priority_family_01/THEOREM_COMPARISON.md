# Theorem-to-theorem comparison and adversarial deductions

Audit: PR218 / problem30006020 / OWR-14298589-005. UTC cutoff: 2026-10-18. This is authored analysis, not redistributed source text. Native source pins and exact read extents are in FRESH_SOURCE_PINS.json, FOLLOWUP_SOURCE_PINS.json and QUERY_READ_LEDGER.json.

## Exact target and success test

The target law is the all-topological-type normalized multiset of maximal horizontal cylinder areas in the principal holomorphic quadratic stratum Q(1^(4g−4)); there is no height bound. The square-count cutoff tends to infinity at fixed g, followed by g→∞. The target includes, for every s_g→0 with g s_g→∞, vague convergence of Σδ_(area/s_g) to PPP(dx/(2x)) and all fixed joint compact-window count moments. The particular window is [g^(-1/2),2g^(-1/2)] with Poisson mean (log2)/2.

A covering prior theorem must match the ensemble, counting convention, normalization, limit order, and growing-window quantifiers. A theorem about cycles in another random geometry or fixed microscopic intervals does not pass that test merely by sharing an intensity tail.

## Located primary coverage

| Component | Verified primary location | Classification | Exact gap |
|---|---|---|---|
| Discrete composition probability ∏ζ(2j_i)/(2j_i)/(k! h_n), n=3g−3 | [DGZZ](https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf), (1.7)–(1.8), Lemma3.6/(3.20)–(3.23) | Exact prior model | None: this is P_(n,∞,1/2), with uniformly ordered cycles. |
| Independent-Poisson conditioning representation | [ABT00](https://www.columbia.edu/cu/simontavare/STpapers-pdf/ABT00.pdf), (1.1); [AT94 facsimile](https://arxiv.org/pdf/1308.3279), Lemma5 | Exact standard framework | No new conditioning identity. |
| Every-rate unmarked mesoscopic PPP | ABT00 Theorem3.1 plus the substitution below | Direct prior-theorem consequence | No additional rate restriction is needed. |
| Unmarked fixed joint count moments | AT94 Lemma5/(126) plus coefficient ratio | Direct prior-theorem consequence | TV alone would be insufficient; moments use the factorial identity. |
| Fixed-genus geometric cylinder-area law | [DL](https://ems.press/content/serial-article-files/51451?nt=1), Theorems1.4/3.2 | Exact published input | Does not itself state a genus-dependent moving-window limit. |
| One-vertex concentration; positive monomial mixture with nearly unit coefficients | DL Theorem4.1 proof, (6.1), Lemma6.4 proof, pp.5116–5119; DGZZ Theorems1.12/5.2 | Exact published inputs extremely close to whole-law approximation | Need to remove residual coefficients and k-prefactors uniformly, normalize, and control exceptional events. |
| Full geometric area-multiset TV approximation by the ideal Dirichlet mixture | Same DL/DGZZ inputs | Explicit extraction/consequence, no separate earlier complete theorem located | This is a short uniform synthesis, not new geometric enumeration. |
| Geometric marked PPP and all moments at every mesoscopic rate | Previous row, classical probability, Gamma tails, geometric moment transfer | No located earlier complete same-target theorem | The bridge, marking, and unbounded-moment transfer must actually be supplied. |
| Fixed microscopic Poisson law | [Liu thesis](https://www.imj-prg.fr/theses/pdf/mingkun_liu.pdf), Remark1.5.9; [OWR](https://doi.org/10.4171/owr/2024/41), Theorem2 | Prior intellectual announcement, with detailed formula | Fixed microscopic windows are different quantifiers from windows escaping with genus. The complete announced manuscript remains unread/unlocated. |

## Independent parameter check for the assembly theorem

Put a_j=ζ(2j)/(2j), Z_j~Poisson(a_j), and A=ζ(2)/2. Then

- j P(Z_j=1)=j a_j exp(−a_j)=1/2+O(1/j);
- for l≥2, j P(Z_j=l)≤A^l/(l! j^(l−1))≤j^(−1) A^l/l!.

Thus ABT's uniform logarithmic condition holds with parameter θ=1/2, e(j)=C/j and constants c_l having Σl c_l<∞. The probabilistic conditioning relation applies to positive real weights directly; an integer combinatorial interpretation is unnecessary.

Let q_n=n s_g. For a fixed compact union of windows choose b_n=ceil(Bq_n). Then b_n=o(n), q_n→∞, so Theorem3.1 applies to the complete count vector through b_n. Independent counts in disjoint windows are exactly Poisson and their means tend to (1/2)log(b/a). This supplies the unmarked law for every allowed rate, including q_n growing more slowly than log n. Describing this portion as a new local Poisson theorem would be materially inaccurate.

AT94's selected-component identity specializes to

E ∏(C_j)_(r_j) = 1_(R≤n) (h_(n−R)/h_n) ∏a_j^(r_j), R=Σj r_j.

The analytic factorization H(z)=(1−z)^(−1/2)B(z), B analytic for |z|<4, B(1)=sqrt2, is already visible in DL Lemma6.7/DGZZ's related generating functions. It gives h_n~sqrt(2/π)n^(−1/2). For fixed-order window moments, R=O(q_n)=o(n), so the ratio tends uniformly to one. This is a routine credited consequence, not a novel identity.

## What Gamma marking adds

For independent unconditioned Poisson counts, attaching a Gamma(2j,1) mark to each size-j component gives a Poisson process with intensity

ρ(y)=Σ_(j≥1) a_j exp(−y)y^(2j−1)/(2j−1)!
    =exp(−y)/y Σ_(m≥1)(cosh(y/m)−1).

The functional expression is already the announced microscopic intensity, so it cannot be claimed as newly discovered. Its m=1 term is (1−exp(−y))²/(2y); the remaining terms are O(y exp(−y/2)). Consequently 2qρ(2qx)→1/(2x) uniformly on compact subsets away from zero.

This intensity calculation by itself is about an independent analytic model. To compare the conditioned model at every rate, one may choose b_n=floor(sqrt(nq_n)). Then b_n=o(n), b_n/q_n→∞. ABT couples all sizes through b_n under a common marking kernel. A Gamma lower tail bounds intrusions of larger sizes into any fixed rescaled compact window by C sqrt(n) exp(−c b_n), using h_(n−j)/h_n≤C sqrt((n+1)/(n−j+1)). This vanishes. Fixed factorial moments follow from AT and the same tail split. Finally T=ΣY_i is Gamma(2n,1), so T/(2n)→1, and higher-moment bounds transfer count moments after dilation. These are additional deductions, but standard and short. No inspected earlier primary statement gives this exact Gamma-marked finite assembly together with all such moments.

The genuinely geometric obligation is stronger than identifying the analytic intensity: the exact DL mixture must be uniformly compared to this assembly, with polynomial exceptional-event control and logarithmic moments of the total cylinder count. The candidate/preprint supplies that comparison from the prior positive formulas. This is a defensible consequence contribution, with a modest claim level.

## Falsification of the endpoint-only shortcut

A fixed microscopic limit plus a macroscopic PD limit does not logically force the mesoscopic conclusion. For any normalized partition (X_i), fix m≥1 and s_g→0 with gs_g→∞, and replace it by

((1−m s_g)X_i)_i together with m new parts equal to s_g.

For all sufficiently large g the masses are positive and still sum to one. Macroscopic changes vanish; new microscopic points escape every fixed compact set since g s_g→∞; existing microscopic coordinates undergo a dilation tending to one. The endpoint limits are preserved. At scale s_g, however, m atoms are added at 1. This is a checkable obstruction to interchanging the genus limit with a limit of microscopic windows. A uniform quantitative microscopic theorem could close that gap, but a limiting-density tail alone cannot.

Likewise, whole-law TV closeness does not transfer unbounded moments: a variable equal to n with probability 1/n and zero otherwise is TV-close to zero but has mean one. The quantitative count-moment transfer in the note is a real requirement even though its tools are standard.

## Distinct current geometric results

Fresh arXiv2312.10517 returned BGL v1, not its final publisher edition. The inspected TheoremsA/B concern cycle lengths of random metric ribbon graphs with a fixed number of faces and total boundary length asymptotic to12g. These cycles do not form the target area partition. Its “mesoscopic” discussion on p.5 concerns a different map scaling limit.

Liu–Rafi–Souto–Trin arXiv2605.03833v1, introduction Theorems8.3/8.5, concerns frequencies of curve types with a fixed self-intersection number. Baroni–Fisac–Liu arXiv2609.01382v1 Theorem1.1 concerns exact word lengths on a fixed once-punctured torus. Neither inspected statement matches the target.

Artigiani–Pardo arXiv2610.06609v1 (5 October2026), TheoremsA/B/C, counts bounded-length cylinders on Z-covers of genus-two Abelian square-tiles, modulo deck action, and compares Siegel–Veech constants on cyclic covers. This is not the principal quadratic random area ensemble or a normalized partition in one fixed direction. These inspected main statements establish no target anticipation. Full-text term scans are discovery aids only, not proof that the papers contain nothing else.

## Normalization reservation

The freshly matched OWR primary PDF prints 4g−4 in its microscopic summary. The freshly matched thesis uses 6g−6; DL's monomial Dirichlet parameters have total 2(3g−3)=6g−6. A fixed dilation leaves dx/(2x) invariant, which explains why the mesoscopic constant does not resolve this discrepancy. The fixed microscopic laws differ under those multipliers. Retain the reservation; do not silently identify them or promote a microscopic correction.

