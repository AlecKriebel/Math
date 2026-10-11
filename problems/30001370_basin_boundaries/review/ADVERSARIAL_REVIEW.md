# Independent AI-assisted source and proof review: 30001370

## Verdict

**PASS: complete answer to the stated original problem; claimed_solved, 3/5 author turns.** No mandatory mathematical correction was found. This is an independent AI-assisted audit, not a journal referee certification or a certification of historical novelty.

The reviewed conclusion is precisely that, for the two-branch Möbius system and tanh feedback with 0 < A ≤ 2/5 and 6 < B ≤ 16, the basin W of the constant density equals each noncentral basin's boundary in the relative L1 topology of the space D of all probability densities. No boundedness, positive lower bound, BV regularity or rate of attraction is imposed on those densities.

## Immutable binding and evidence

The 25-file author packet is bound by FINAL_AUTHOR_MANIFEST.json, SHA256 `a871f0312e49b6aeb227d6b80c90a6afc6b00ce7b4a7303bbc2a53af289d9d2b`, at [commit be4730c4](https://github.com/AlecKriebel/Math/tree/be4730c4f09b4fe5cc82bbedb8cb154894124dfd/problems/30001370_basin_boundaries). TURN_3.md has SHA256 `aaf53a6a0055e1195df53a8db46e31bcc7aea88189d4ecfa6b18596089c9e123`.

All 25 raw local Git blob hashes and lengths match the immutable remote listing. All 43 entries across the three historical manifests and final manifest verify. All three source PDF hashes and lengths verify. The three author programs were read and replayed; their complete stdout matches the frozen receipts byte for byte: 60,278 + 445 + 211 = 60,934 assertions. A separate standard-library verifier passes 18,678 rational controls. Its 400-interval covering certificate is independent of the author's 40-row CSV. Computational controls supplement the analytic audit below; they do not prove its infinite-dimensional assertions by finite testing.

## Exact source and prior-result boundary

The full Keller contribution in [OWR49/2009](https://ems.press/content/serial-article-files/46250), printed pp.2713–2715, was read. Pages2714–2715 were visually inspected. The report fixes D, the formula, parameter range and convergence topology, then explicitly asks the common-boundary question. [Publisher metadata](https://ems.press/journals/owr/articles/4132) confirms the 2009 volume and 1 September 2010 publication date.

The inspected primary predecessor is [Bardet–Keller–Zweimüller, arXiv:0812.4040v1](https://arxiv.org/abs/0812.4040), corresponding to CMP292 (2009),237–270, DOI10.1007/s00220-009-0854-9. The final journal PDF is not represented as inspected. The audit checked its definitions, Theorem2/Example1, Lemma4 inverse expansion argument, §4.1 branch action, Proposition3 and its proof, Proposition4 and its proof, and Lemma14/Proposition5 derivative statement. The source's Example1 contains the required parameter rectangle; the report independently states the exact theorem there. Assumption I is also directly compatible with G': 16−100a² ≤ 25−50a on 0≤a≤.4. Global convergence and basin openness apply to all D. The old boundary result is only on W∩D', where D' is a compact analytic mixture class. In particular it gives the needed boundary property at 1. The candidate does not assert D' is dense in D.

The rank-one inverse mechanism, analytic core, global convergence and boundary seed are credited earlier results. The full-D backward-transport approximation is the additional argument audited here. Neither a bounded literature search nor this review establishes priority.

## Turn 1: homeomorphism, sections and topology

The increasing Möbius transport h_r fixes the interval endpoints, has inverse h_−r, and T_r = T_0∘h_r off its null cut. Its signed-density pushforward is an L1 isometry. Approximation by continuous functions proves joint strong parameter/density continuity, without incorrectly claiming operator-norm continuity.

For any target v the scalar feedback equation has a unique root: its residual is increasing by at least the parameter increment, and it changes sign at ±A. The L1 root bound B/2 and the transport isometry prove continuity of the exact inverse K^−1. Thus K is a homeomorphism of D.

The section of P_0 handles a zero target-density fiber correctly: both original branch densities vanish there, and setting the two weights to one makes their average one. The resulting positive linear section is an isometry, fixes the original density and maps D to D. Hence P_0 and F are relatively open surjections, with continuous sections through each point.

The boundary pullback argument uses continuity, openness and complete invariance of the basin, not an ambient-interior assertion. Disjoint open basins and global convergence put both boundaries inside W. W itself is closed as the complement of the two open basins. Symmetric dyadic approximation is valid. The first-turn warning that unquantified continuous sections alone do not close the proof is correct.

## Turn 2: separate linear result

The example x³−3x/20 has zero mean and zero phi, while phi(P_0 f)=1/320, so ker(phi) is not invariant. The qualification is restricted to the inspected preprint's short proof, not an assertion that its theorem is false.

The resolvent functional converges in operator norm for lambda>1. Its eigenfunctional relation, projection and finite-iterate rank-one identity are correct. The tail identity on ker L proves strong L1 stability by exactness of doubling. The variation estimate is 7·2^−n on the correct BV stable kernel. High-frequency symmetric cosines show no uniform L1 operator-norm contraction. No nonlinear L1 differentiability or stable-manifold theorem is inferred. This turn is not needed for the final nonlinear proof.

## Turn 3: full analytic audit

1. **Probability-space inverse.** The scalar equation remains uniquely solvable on any probability space. Along a bounded interpolation the implicit residual derivative is at least one and all scalar derivatives are bounded on the compact rectangle, so differentiation under expectation is valid. The rank-one inverse formula acts on real L2 with arbitrary probability weights. To check its norm estimate, a vector with nonzero projection on q may be rescaled to q−p, p perpendicular to q; the perpendicular case follows by continuity. The inequalities E q ≥ ||q||² and |E p|≤||p|| are sufficient. The cross term uses 2√v t≤v+t²; the two one-variable maxima give the claimed coefficients. The feedback bound G'≤16−100a² is valid throughout the interpolation, including varying means. The rational covering certificate proves a norm strictly below24/25 over the whole parameter interval. It is not a sampled parameter test.

2. **Self-consistent backward laws.** The continuous cumulative transform of the absolutely continuous terminal law is uniform even with zero-density intervals. Each next-variable sublaw conditioned only by a branch event is dominated by the unconditioned absolutely continuous law. Its smooth inverse-branch pushforward is therefore absolutely continuous. The unique implicit feedback parameter is exactly the mean feedback of that new law. Original branch labels are reused on the same probability space, so they cancel in the coupled L2 input difference; no independence is needed. Endpoint assignments are null after the absolute-continuity induction. This proves F^n v_n=1, rather than only an external-parameter identity.

3. **Monotone lifts and regularity.** At every old cut, the adjacent images agree at the new cut because the later lift fixes the endpoints. Each finite lift is continuous, nondecreasing, onto and absolutely continuous. On each branch the inner original map is a smooth bi-Lipschitz map; this justifies composition with the absolutely continuous later lift. A generic composition-of-AC assertion is not being used. Finite cylinder maps also preserve null sets in both directions, validating the derivative formula for rough terminal densities. Flat intervals are allowed.

4. **Uniform distortion.** The inverse derivative constants 3/4 and25/96 and log-derivative constants1 and35/24 hold on the entire rectangle. Summing the recurrence gives sum Delta≤384 epsilon, d_0≤101 epsilon and sum d_j≤403 epsilon. Hence the logarithmic product distortion is at most963 epsilon, and the looser964 is valid. No constant grows with n.

5. **Unweighted derivative estimate.** The direct branch action on w_y agrees with the primary source, and its parameter rectangle preserves |y|≤2/3. Every normalized density in that mixture class lies between1/2 and2. Thus the external original parameter sequence applied to the constant density is bounded by2, even though the nonlinear orbit u_n need not be bounded. The transfer identity yields integral |u_n(X_n)−1| dx≤2 epsilon. This is Lebesgue integration, avoiding an unjustified square of u_n or a change to u-weighted integration.

6. **Total variation rather than weak approximation.** For an absolutely continuous monotone onto H, H_*(H' dx)=dx follows from continuous test functions and an antiderivative. It remains true with flat intervals. The comparison with a continuous g is a finite-signed-measure estimate, so possible atoms in H_*(g dx) do not invalidate it. In contrast, H_*(u dx) is already known to be absolutely continuous from the backward-law construction. Combining uniform displacement, L1 derivative control, pushforward contraction and density of continuous functions gives v_n→u in full L1. No uniform convergence-rate assumption on F^n u is used.

7. **Closure conclusion.** Every finite preimage of1 belongs to both basin boundaries by the open-map pullback. Closedness of the boundaries and the approximation now give W contained in both. The converse was supplied by the disjoint open basins and global convergence. This proves exactly the source assertion on all D.

## Limits

The result is restricted to the stated Möbius/tanh system and parameter rectangle. It does not imply a differentiable L1 stable manifold, arbitrary transfer-operator results, finite-particle large-deviation conclusions, or novelty. The three frozen turns require no alteration. All source dependencies should remain credited in any presentation.
