# Acceptance: bounded tracking for short leads and a genuine mixed-lead theorem

Shared PASS3 independent audit. This accepts a deterministic short-threat controller and a restricted mixed short/long announcement theorem. The original game remains unresolved because intermediate leads are excluded from the mixed theorem.

## Audited inputs and decision

- `../pass3_independent/BOUNDED_TRACKING.md`, SHA-256 `f3aaf3404d9dcadd917ad9c027e284cf54c79cf05c0bf173b19ba30d6430887d`.
- `../pass3_independent/MIXED_LEAD_COROLLARY.md`, SHA-256 `2d54149f12e6eb288ac4b7079917202c26da645695451628aa3387a5a3755c80`.

Both pass the full mathematical audit without a required correction. The associated exact constants checker was also run successfully, verifying 228 integer guard-charge cases. The proof below checks the analytic and adaptive-game steps beyond that computation.

## 1. Every current and next-time short threat is budgeted

A short bomb announced after move r has 1≤t−r≤15. Before move n, each current-time or next-time short pair already announced has a witness in rounds n−15,…,n−1. Distinct pairs at the two different target times require different announcement witnesses. Thus the local current count m_n and complete next-time count b_n satisfy m_n+b_n≤15.

The maintained guard m_n≤8 gives at least one currently safe neighbor. If all such neighbors had eight or more preexisting next-time bombs, the accepted neighborhood-covering lemma would require at least sixteen distinct current/next pairs, a contradiction. An admissible move is currently safe and has at most seven preexisting next-time bombs around it. The following Devil announcement adds at most one, preserving the guard for the next move.

This is an infinite induction; it does not reuse the original finite move-17 argument without a new bound. The lead restriction supplies the same fifteen-pair budget at every round. Other ignored announcements consume budget and cannot invalidate that upper bound.

## 2. Exact directional loss estimate

For an L1-normalized direction, reflect/exchange coordinates to obtain (x,1−x), 1/2≤x≤1. The nine ordered projections have the form stated in the input, with their only internal ordering breakpoint at x=2/3. Their worst losses after excluding k choices are exactly bounded by

0, 1/2, 2/3, 1, 1, 4/3, 2, 2, 2.

The table satisfies both D_k≤k/2 and D_k≤2(k+7)/13. If r_n choices fail the next-time guard, the covering lemma gives b_n≥r_n+7 when r_n>0. The number of excluded choices is at most m_n+r_n≤8. Hence their directional loss is at most m_n/2+2b_n/13. When r_n=0, the first table bound suffices.

For Euclidean unit w, multiplying by ||w||_1 gives

w·delta≥1−alpha m_n−beta b_n,

with alpha=√2/2, beta=2√2/13. The comparison is valid even if the displayed right side is negative: writing c=m_n/2+2b_n/13≥0 and l=||w||_1∈[1,√2], the difference between l(1−c) and 1−√2 c is (l−1)+(√2−l)c≥0.

Thus the chosen inward-maximizing admissible move enjoys this bound with C=alpha+beta=17√2/26<0.93. No average or random directional choice is used.

## 3. Radial drift and amortized radius

The controller receives z_n before choosing its move and only needs that next point. When d_(n−1)=||a_(n−1)−z_(n−1)||_2≥60 and reference speed is at most 0.01, the current target vector e=z_n−a_(n−1) has length at least 59.99. Along any legal move segment, the Euclidean norm Hessian has norm at most 1/(||e||−√2). The quadratic remainder is therefore at most 1/(||e||−√2)<0.02.

Combining this with the directional bound and the reference increment gives

d_n≤d_(n−1)−0.97+alpha m_n+beta b_n.

For any N consecutive move indices, a given short pair can be counted in m at only its own target time, and in b at only the preceding move. Each sum therefore has at most N+15 announcement witnesses, an upper bound that also covers intervals near time zero. A pair may contribute to both separate sums; the proof explicitly pays both coefficients and does not treat them as disjoint.

Summing over an excursion whose preceding errors are all at least 60 gives an increase of at most 15C, since the linear drift coefficient −0.97+C is negative. Entry into such an excursion from below 60 overshoots by less than √2+0.01, hence starts below 62. Every point of the excursion is below 62+15C<76. Initialization d_0=0 and the guard at move 1 are both valid.

Therefore the input's claimed bound ||a_n−z_n||_2<80 holds, with the stronger proved bound below 76. Every short collision is avoided before its round's new announcement. The proof applies pathwise to arbitrary adaptively chosen short streams and successively supplied references of the stated speed.

## 4. Reference process for the mixed theorem

The mixed construction sets E=25921, K=3,000,000, A=600,000,000, ell_j=j(1+floor(log₂j))², M_j=K ell_j and L_j=200M_j. The independent D_j are uniform lattice displacements in [−M_j,M_j]². Linear real-valued reference interpolation over L_j moves has Euclidean speed at most √2/200<0.01, so the deterministic tracker applies.

The reference may be real-valued between endpoints. The proof does not silently invoke the earlier lattice-reference theorem: it directly counts integer displacement values in a real-shifted square. Future draws are not consulted before their blocks begin. The actual controlled history depends only on revealed reference draws, already observed short bombs, and deterministic tie choices, so an announcement in block j cannot reveal D_(j+1).

The tracker ignores long bombs but remains defined on a hypothetical legal continuation after a long collision. It still avoids every short bomb and retains its error bound on every such extended history. This removes any need to condition on survival or on a future good event.

## 5. Adaptive long-target probability and summation

Condition on the actual history through announcement n and its chosen target (p,t). For a long target, t≥S_(j+2), so D_(j+1) is an unrevealed independent complete block in the reference endpoint. Thus z_t=D_(j+1)+Z with conditional independence of the two summands. The selected target time is fixed by the conditioning; later Devil actions do not alter the independent reference path.

An actual hit implies ||z_t−p||∞<80. For any real shift Z, each length-160 coordinate interval contains at most 161 integer values of D_(j+1). Therefore the conditional long-hit probability is at most E/(2M_(j+1)+1)². The tracking correction can be arbitrarily correlated with D_(j+1); only the pointwise geometric implication is used. Nonlong announcements have an empty long-hit event.

With L_j rounds in block j, the total long-hit probability is strictly less than

(50E/K) sum_j ell_j/ell_(j+1)²

≤(50E/K) sum_j 1/ell_j ≤100E/K=25921/30000<1.

The monotonicity step and dyadic reciprocal-sum bound are valid. Strictness follows from each denominator (2M+1)² being larger than 4M². Since short collisions are impossible, infinite survival probability is strictly greater than 4079/30000 against every admissible adaptive Devil.

A finite-horizon losing Devil would defeat every realization of this legal randomized controller, contradicting that positive survival probability. Including absolute time in the state, the accepted finite-game dichotomy and compactness extraction therefore supply one deterministic infinite strategy for the stated mixed lead class.

## 6. Explicit long threshold and exact scope

For j≥2, the same dyadic estimate gives n≥A j²b(j)²/20 and g(n)=S_(j+2)−n≤(9/2)A j b(j)². Hence g(n)<21√A√n(1+log₂n). In block j=1, g(n)≤9A. The claimed ceiling of the maximum of these two expressions is therefore a sufficient all-n long threshold.

The permitted announcements are precisely ineffective pairs, leads 1–15, or targets at least the stated block threshold. The theorem does not handle effective leads between these ranges. Such medium leads can invalidate the fifteen-pair guard while failing the fresh-complete-block condition.

This result is compatible with the earlier tracking attacks. Their terminal carpets require many distinct announcement rounds and leads up to the carpet size, exceeding fifteen for a radius-80 tracker while falling within the excluded medium range. No contradiction or unrestricted conclusion follows.
