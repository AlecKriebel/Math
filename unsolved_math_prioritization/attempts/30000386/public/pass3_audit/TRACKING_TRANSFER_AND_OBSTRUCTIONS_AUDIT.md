# Acceptance: correction transfer and two tracking obstructions

Shared PASS3 independent audit. This accepts conditional transfer criteria and obstructions to specified controllers/certificates. It does not accept an unrestricted Angel construction or a full-game Devil strategy. Exact input versions are pinned in the accompanying manifest.

## 1. Global-reference correction transfer

Audited input: `../pass3_survival/COUPLING_TRANSFER.md`, SHA-256 `b900a987975f20e81784d7eede41637bd1822283556af9c3606bc5a7725d3723`.

Accepted. At announcement time n, conditioning on the complete actual corrected history and Devil's selected pair fixes its target t. Every reference draw with start S_i>n remains inaccessible to the corrected controller and independent of this conditioning. This is stronger than conditioning merely on the reference history, and the document states the needed access restriction.

For a completed fresh block of maximum length L*(n,t), the reference endpoint is X_t=D_i+Z, with Z conditionally independent of D_i. All other reference displacements and the fixed within-block interpolation determine Z. The target-dependent index i is fixed after conditioning, so choosing the longest completed fresh block creates no selection bias.

The error Y_t−X_t need not be independent of D_i. On the good event G, a hit at p implies X_t is in the radius-r(t) lattice square around p. This proves the displayed small-ball bound on hit intersect G. The proof does not condition on G, so G may depend on all future randomness without invalidating uniformity of D_i in the underlying conditional calculation.

On G every short hit is excluded; off G is charged by epsilon. The sum of the long hit-and-good bounds therefore covers every actual lethal event. Ineffective pairs have no hit event. A total below one gives positive survival probability uniformly over every adaptive Devil, and the accepted finite-horizon determinacy plus compactness argument supplies a deterministic strategy if the stated good-event hypotheses are proved.

Those hypotheses are not constructed here. The theorem is a correct conditional route to the full target, not its completion.

## 2. Move-then-hold finite-block carpet attack

Audited input: `../pass3_survival/MOVE_HOLD_BRIDGE_OBSTRUCTION.md`, SHA-256 `158c729de519e6845f471b0f7910af39d7766dabc257a5edd2628110611e5166`.

Accepted. Put M=(4R+1)²≤L and u=T−M. After seeing Y_u, Devil announces every point of Y_u+[−2R,2R]², one in each round u,…,T−1, all for T. There are exactly M available rounds and M targets; the round-u move is observed before its announcement. All leads are between one and M.

On the pause event ||D||∞≤L−M, the reference has completed both coordinate motions by u, hence X_u=X_T. Tracking within R at u and T implies ||Y_T−Y_u||∞≤2R. Thus survival and tracking cannot both hold on that event. Its probability is exactly [2(L−M)+1]²/(2L+1)²; the geometric implication does not assume anything about how the correction depends on D.

For a deterministic envelope r(t), taking R_j as its maximum over the closed block makes the same attack valid whenever M_j≤L_j. Attack intervals for distinct blocks do not overlap. Every attack targets its own block endpoint and is short under the transfer theorem's definition. The pause events depend only on independent D_j, even though carpet centers depend adaptively on actual positions.

If infinitely many blocks satisfy M_j≤eta L_j for some eta<1, their pause probabilities are at least (1−eta)². Independence makes the probability of avoiding every such pause zero. Therefore a positive-probability global short-safe tracking event against every Devil requires liminf R_j/√L_j≥1/4, as claimed.

## 3. Divergence of that specific repair-factor accounting

The continuation of the same input is accepted. If L_(j+1)/L_j tends to one, then eventually R_j≥√L_j/8. Choose a time t_j attaining the deterministic block maximum R_j. For every announcement n in block j−2, t_j is an allowed long target. The completed fresh blocks before t_j are among j−1 and j, giving L*(n,t_j)≤2L_j eventually.

Thus the exact supremum defining q_n is at least

min(1,(2R_j+1)²/(2L*+1)²) ≥ 1/(400L_j).

The constants follow from numerator at least L_j/16 and denominator at most 25L_j². Capping at one cannot spoil this smaller lower bound. There are L_(j−2) such announcement rounds, so the block charge is eventually at least 1/800. Different j charge distinct announcement blocks; the series diverges.

Both cited schedules have neighboring length ratio tending to one, including the dyadic logarithmic schedule: its occasional factor ((b+1)/b)² tends to one. Choosing a small error only at endpoints does not avoid the argument because t_j may be an interior time.

This proves failure of the stated sufficient q-summation bridge for that reference, not failure of every corrected policy or every correlated probability accounting method.

## 4. Linear-interpolation endpoint recovery

Audited input: `../pass3_devil/ENDPOINT_RECOVERY_OBSTRUCTION.md`, SHA-256 `7bcfa23203891f452436004fb96ce30de9c01a4e04b4b4bf2c197807c7ef5013`.

Accepted. If an observed history at m<T constrains every continuation retaining a promised property to a known set C of at most T−m endpoints, Devil can cover C using one time-T announcement in each of |C| rounds. It may wait until T−|C|,…,T−1, which are still no earlier than m. This uses neither stored credit nor future observations. It forces collision or violation of the property, not collision regardless of the property.

For the even-length linear interpolation, the midpoint identity b_T−2b_m+b_s∈{0,1}² is exact for positive and negative integer displacements. Writing a_u=b_u+e_u gives an error combination e_T−2e_m+e_s of coordinate magnitude at most 4R. Hence every tracked endpoint lies in a square with (8R+2)² cells centered as stated. With actual-start anchoring e_s=0, the bound is 3R and the square has (6R+2)² cells.

If the appropriate cell count M is at most L/2, all targets can be announced in the final M rounds after the midpoint observation. For fixed R this uses a fixed bounded lead, even as L grows. For R=o(√L), the attack applies eventually. Nothing forces an unrestricted Angel to keep the tracking promise.

The generic correction estimate P(Y=p)≤(2R+1)²/(2L+1)² is also correct under the stated original conditioning and pathwise error bound. Its factor is sharp as a bound for arbitrary endpoint corrections: map the central radius-R subset of the uniform displacement box to zero. This example concerns endpoint concentration; no additional legal-trajectory realization is claimed.

If surviving interpolation guarantees require R_j=Omega(√L_j), the charged cost L_(j−1)(2R_j+1)²/(2L_j+1)² is bounded below by a positive multiple of L_(j−1)/L_j. Bounded adjacent length ratios therefore prevent summability. Again this is an obstruction to the worst-case bound, not a demonstrated actual loss probability for all repaired paths.

## 5. Relation to the local-reset gate

The separately proved `ROBUST_BLOCK_COUPLING_GATE.md` uses actual-start reference blocks and bounds hit intersect tracking-good by (4rho+1)²/(2M+1)², retaining only the most recent endpoint and prefix errors. The endpoint-recovery attack concerns whether a controller satisfying its tracking premise exists, rather than refuting that implication.

The local-reset gate was independently checked in `../pass3_devil/COUPLING_GATE_INDEPENDENT_AUDIT.md`, SHA-256 `ee42ee4045fa77f5f174169a819b3404feea580c4ffeed9f05196bbc130cedcc`. Fresh draw timing after each actual start boundary, fixed reference interpolation, and use of hit intersect good rather than hit conditional on good are essential to that accepted statement.
