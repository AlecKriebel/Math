# Independent continuity and tensor-core review

## Version and verdict

- Target: UnsolvedMath 30001179 / OWR-3392-005, Skeide's free-product-system generation question.
- Reviewed candidate: `CANDIDATE_PROOF.md`, 20,525 bytes, SHA-256 `152881a86b39c8b8afec166842000b8b256cad2ac04c764731e23468d8877d85`.
- Recorded WIP: `wip/free-product-generation-30001179`, commit `6d1d44e7ffee89976a50fc1f4db5a350a033247e`. I checked the local WIP candidate has the same hash; I did not independently retrieve this remote commit.
- Frozen-manifest SHA-256: `3a70527e48d0d08b5cdb259aec24cf7c98fa230b7d533cc94b90abf8cc56d0f6`.
- Review completed: 2026-10-03 UTC. This review is bound to the bytes above; changes require reassessment.

**Verdict in the assigned scope: no fatal gap found.** The explicit continuous field, continuity at zero, varying-cut continuity, tensor-core identification, generation of the finite-word sector, and nonzero orthogonal infinite sector withstand the checks below. The assertions do not rely on an illicit common conull set for all cuts or on nonseparable counting measure. Some continuity details can usefully be made explicit, but they follow from the candidate's actual constructions rather than a replacement construction.

The algebraic construction still depends on the prefix-density and run-chart factorization being correct. I read the entire proof and cross-checked those prerequisites, including the density direction and ordinal boundary behavior, without finding a defect; they receive a separate dedicated independent review. This is an audit outcome, not a public solved claim or a literature-priority certification.

## 1. Exact source category

I read the relevant original text and visually inspected the local images of original pp.529–530, rather than relying only on SOURCE_GATE.md.

The original definition on p.529 specifies a family of Hilbert B–B bimodules, central unit reference vectors, pointed B-bilinear unitaries from the pointed reduced free product to the time-sum fibre, associativity, and canonical zero-time identifications. It explicitly describes this as the algebraic definition, then leaves continuity/measurability conditions on the bundle as additional choices and specifically discusses products of continuous sections through the natural tensor inclusion.

The p.530 question is the intersection over all finite ordered time partitions of the embedded tensor products and whether that subsystem generates the entire given free system. It is not restricted there to full Fock systems or systems already constructed from a spatial tensor system. The forward construction and its recovery question occur separately immediately afterwards.

Consequently B=C is a legitimate specialization of the source's universal question. A counterexample with this coefficient algebra is sufficient for the universal assertion. The candidate does not need to prove the dubious general Hilbert-module statement that arbitrary intersections automatically commute with internal tensor products: it computes its Hilbert-space intersection directly and separately proves the resulting family is a tensor product system.

The continuity provided here is a separable continuous Hilbert field, with a continuous reference section and continuous elementary free multiplication; it is locally trivial at every positive time. No assertion of local triviality at zero is necessary or made. The dimension-one zero fibre is standard and does not conflict with this continuous-field formulation.

Source bindings checked:

- Original report PDF SHA-256: `5121d8ec30d2c1346cbbdd68164915d5a24fb31e5a94a3a3215ba576954ee64d`.
- Extracted report text SHA-256: `f766220fadce4b3717aa1f76db45e914e124cea87e3af019012583673f098450`.
- Page 529 image SHA-256: `1521d9700c8dec075bbedc077a5f9d7112095a481f84ad5ed753e517442b2e1d`.
- Page 530 image SHA-256: `bdcd77d900b92394491a50a04e1ee1d6db58a8d0182ff2dcef676afe431a4bf1`.

## 2. Measured-space and factorization prerequisites cross-checked

The set C is Borel: coordinate convergence, the limiting a, and the existence and positivity/finiteness of the displayed Cesaro limit are Borel conditions. The inverse coordinates a, d, and z are Borel. The two defining conditions of Gamma follow exactly when one reconstructs z from a sequence in C. Finite prefixes and tails preserve these conditions. Thus the Borel bijection used in the candidate is genuine.

Removing k coordinates gives d(tail)=2^{-k}d(original). With a and d recoverable from the tail, the first k coordinates have conditional Gaussian scales 2^{k-j}d(tail). Haar measure d(delta)/delta is unchanged by the parameter rescaling. Consequently the candidate's equation is mu(d p_k(v,y))=q_k(v;y) dv mu(dy), and the concatenation unitary from the product measure uses q_k^{-1/2}, not q_k^{1/2}. This direction is consistent.

For lengths omega*n+m and omega*p+q with p>0, the first word's finite suffix is absorbed as a finite prefix of the second word's first infinite block. The latter remains in C; no infinite block is lost. The number n of infinite blocks is additive, while finite suffix length is absorbed according to ordinal addition. The coordinate map remains injective because the input lengths are fixed. This is not an assertion that ordinal addition is cancellative when lengths vary.

At a fixed cut, a convergent block whose limit is not at the cut changes side only finitely often. The whole word has finitely many blocks and a finite suffix, so there are finitely many maximal convex color runs. Runs can cross omega-block boundaries. Their order types still have the required form, with an initial tail of a block, possibly full intervening blocks, and a finite final prefix. The only altered infinite block is a finite tail or a finite-prefix absorption, already covered by the prefix lemma. Its ordinal length and coordinates determine each run uniquely. Countably many finite lists of lengths below omega-squared suffice.

These checks do not reveal a hidden source of uncountably many charts, a discrete nonseparable label space, or a discarded positive-measure boundary event. Full factorization and associator verification should be read together with the dedicated measure/factorization audit.

## 3. Separability and support projection continuity

Each sector is a standard Borel space with sigma-finite measure. A concrete finite-measure exhaustion bounds each a parameter, bounds each d parameter away from zero and infinity, and bounds every finite suffix coordinate. The Gaussian product coordinates have probability measure. Countably many sectors therefore give a sigma-finite, countably generated measured space, and H=L2(Omega,nu) is separable.

For a fixed word of nonzero grade, the set of its coordinates consists of finitely many convergent sequences and a finite suffix. Its closure is compact, and its supremum is either an actual coordinate or one of the finitely many block limits. For each fixed t, the event sup=t is consequently contained in a countable union of coordinate-equality events and finitely many limit-equality events. Each is null. Products with other factors remain null because all measures are sigma-finite.

It follows that the upper-interval indicators converge almost everywhere when t_j tends to a positive t. The lower endpoint is fixed at zero and causes no extra varying-boundary problem. Dominated convergence against |h|^2 gives strong continuity of P_t.

At zero, every nonempty word with all coordinates positive has at least one positive coordinate, so eventually it cannot lie in (0,t_j) when t_j tends to zero. Words with a nonpositive coordinate never contribute. Thus the nonvacuum projections tend strongly to zero. The vacuum projection is constant. This proves the asserted strong continuity at zero without requiring finiteness of nu(Omega((0,t))).

The sections P_t h have continuous norms and inner products, pass through every fibre vector, and a countable dense set of h gives a countable fundamental family. They therefore supply a separable continuous field. All continuous sections of this field are locally H-norm continuous, and the norm-continuous sections of H lying in the fibres satisfy its local section criterion.

There is no additional global separability problem. The increasing union over integer t of E_t has a separable completion inside H. Every positive-coordinate word is bounded, so this completion is exactly the support space for positive labels if that inductive limit is needed.

## 4. Dilation and multiplication continuity

In each infinite block, common translation changes only a; common positive dilation changes a to ra and d to rd, leaving z unchanged. These actions are strongly continuous in L2(da d(log d) gamma). Strong continuity of dilation follows from ordinary dilation in a, translation in log d, and density of elementary functions in the Gaussian coordinate. Tensor products and finite-sector approximation extend it to H.

The sector scaling exponent is n+m, since each infinite block contributes one factor r from da and each finite letter one from Lebesgue measure; d(delta)/delta contributes none. Hence the displayed r^{-(n+m)/2} factor is correct. D_r maps E_1 to E_r and gives the claimed positive-time local trivializations.

For fixed input ordinal grades, the global concatenation unitary is fixed as the time parameters vary. The translated inputs are norm continuous. Applying that fixed bounded unitary therefore proves continuity without estimating possibly unbounded pointwise Radon–Nikodym multipliers. For finite alternating words the same argument applies with repeated source fibres.

Finite-grade approximation is locally uniform: if R_N projects to finitely many grades and x_s is norm continuous near s0, then

||(1-R_N)x_s|| <= ||x_s-x_s0|| + ||(1-R_N)x_s0||.

The projections preserve each fibre. The multilinear product norm bounds and unitarity then pass continuity from finite grades to arbitrary continuous sections. At a zero-time boundary each centered section of the vanishing fibre tends to zero. Terms that contain it vanish; the vacuum and single surviving-factor terms have the stated limits. This covers the corners as well as the edges of the time quadrant.

## 5. Full structural and inverse continuity at varying cuts

The candidate explicitly proves continuity of elementary free-word sections. The following routine consequence makes the topology of the full structural maps and their inverses unambiguous, including at zero.

Let J=H free-product H, with its usual countable alternating-word direct sum. Put A_t=P_t-P_vac on H-perpendicular-vacuum. Define Q(s,t) on J to be the vacuum projection plus, on each alternating word summand, the tensor product of A_s and A_t in that word's color order. Each tensor product is strongly continuous, and finite-word approximation gives strong continuity of Q(s,t). Its range is the embedded E_s free-product E_t.

Extend the structural unitary by zero off its source fibre:

V(s,t)=u_(s,t) Q(s,t): J -> H.

The continuity argument already in Lemma 7, first on finite elementary vectors and then by the uniform norm bound, proves strong continuity of V. It is a partial isometry with initial projection Q(s,t) and final projection P_(s+t).

For a fixed h in H and a converging parameter p=(s,t) -> p0, the norm-square identity is

||V(p)*h-V(p0)*h||^2
= ||P_(s+t)h||^2 + ||P_(s0+t0)h||^2
  - 2 Re <h,V(p)V(p0)*h>.

Strong continuity of P and V makes this tend to zero. Thus the inverse structure maps are strongly continuous as maps of the continuous source and target fields too. At strictly positive times this can alternatively be phrased as strong continuity of fixed-Hilbert-space unitaries after dilation trivialization, which automatically implies strong continuity of their adjoints.

Accordingly the construction has more than merely separately measurable multiplication. It does not need a conull set on which every real cut is simultaneously admissible. All fixed-parameter operators are well defined modulo their own null sets, and these explicit operator estimates establish their joint dependence.

## 6. Exact tensor intersection

The canonical inclusion A tensor B into A free-product B decomposes as vacuum, the two single centered factors, and the ordered centered tensor A-perp-vacuum tensor B-perp-vacuum. Iterating it over time intervals gives at most one centered contribution per interval, in the prescribed latest-to-earliest order.

By the run-chart factorization, the image is the entire support subspace of words with nonincreasing interval colors. Half-density factors are finite and nonzero almost everywhere and cannot change these support subspaces. This is a genuine multiplication-projection characterization of T_pi, not just a statement about individual basis words.

For each fixed t use the countable set of rational c in (0,t). Apart from the countable union of the corresponding null boundary events, a word fails actual nonincreasing order exactly when some earlier coordinate is below a later coordinate. The index set is countable, and a rational cut between those two values detects the failure. Intersections of these countably many multiplication projections therefore give L2 of the actual nonincreasing support M_t.

The independent pairs z_(2j),z_(2j+1) yield both strict signs infinitely often almost surely. Hence an infinite block has a rise almost surely, and a sector with any infinite block has zero measure on M_t. Restriction to interval events cannot resurrect that null set, even though such conditioning destroys the original independence. Sigma-finiteness justifies all products and restrictions. In each finite sector equal-coordinate sets are null, leaving precisely the decreasing simplex.

Thus the rational-cut intersection is the displayed F_t. The full partition intersection is contained in it. Conversely for any one fixed finite partition every decreasing finite word avoids its boundaries almost everywhere and has the required interval order. Therefore F_t is contained in every individual T_pi. This last inference is about closed subspaces and does not take an uncountable union of boundary null sets. The argument correctly handles the all-cut versus rational-cut issue.

## 7. F is maximal and continuous as a tensor subsystem

At fixed total finite length m, a decreasing tuple has a unique split at t into k later labels and m-k earlier labels, except for the null event that a label equals t. The disjoint L2 sum over m and k gives exactly F_s tensor F_t -> F_(s+t). Ordinary finite concatenation is Lebesgue-measure preserving, so no density factor is omitted here. This proves surjectivity as well as isometry.

The finite-decreasing support projection is a fixed projection on H commuting with every P_t. Consequently its fibre restrictions form a continuous subfield with enough sections; its positive-time dilation trivializations also restrict. The multiplication continuity follows from the already checked continuity in E.

Any tensor subsystem with inherited multiplication has, at each finite partition, its entire t-fibre in the image of the corresponding tensor product of E-fibres. It must therefore lie in every T_pi and in F_t. Since F has just been proved to be a tensor subsystem, it is maximal in exactly the source's sense.

## 8. Free hull, completion, and properness

The finite-word support projection is a fixed orthogonal direct-sum projection. Its range K_t is closed. Both directions of the fixed-cut factorization preserve finite words: a finite word has finite runs, and finitely many finite words concatenate to a finite word. Thus K is a free subsystem, not only a subfamily stable under forward products. Its field is continuous for the same fixed-projection reason as F's.

Every partition-wise free product of F-fibres lies in K. Conversely, outside the finite union of equal-coordinate diagonals, any m-tuple can be separated into distinct rational-endpoint partition cells. The corresponding free-word summand uses the singleton sector from the appropriate F-fibre for each cell, and its image is the full L2 support rectangle. Countably many rational partitions cover the distinct-coordinate set. Their support ranges have closed span the entire finite m-sector. Summing over m proves that the free hull is exactly K.

This is a Hilbert-space closed-span assertion, not a claim that individual tuples are Hilbert basis vectors. The candidate's support-projection sentence is the correct bridge. Arbitrarily fine partitions cannot produce grade omega vectors by norm completion because K is already an orthogonal direct-sum closed subspace and all those partition ranges stay in K.

For any t>0 the proposed region a in [t/3,2t/3] and d in [t/100,t/50] has finite positive parameter measure. Conditional on such d, the events |z_j| < (t/(3d))2^j are independent with positive success probabilities; the sum of their failure probabilities is finite. Their infinite product is positive. In fact the minimum threshold is already 50/3 at j=0. All coordinates then remain strictly in (0,t). Intersecting with Gamma preserves full Gaussian measure.

The image region has finite positive mu measure, so its indicator gives an actual nonzero square-integrable grade-omega vector. It remains orthogonal to K after Hilbert completion. No limiting quotient or measure-class operation identifies it with a finite-grade vector.

## 9. Presentation improvements and limits

No new author construction or substantive repair is demanded by the assigned checks. For a polished version, useful additions would be:

1. State explicitly that the continuous fields use the ambient norm-continuous support-subspace sections, and give a countable fundamental family.
2. Include the short Q/V argument above if claiming continuity of the entire structural unitary and its inverse, rather than only the elementary-section formulation already written.
3. State that the F and K projections commute with P_t, thereby explicitly recording their continuous subsystem structures.
4. In the generation argument, phrase the cover as full L2 support rectangles or support projections, avoiding an isolated literal reading of individual tuples as Hilbert vectors.
5. Keep the exact source's algebraic category distinct from any unspecified stronger regularity convention. The explicit continuous-field convention proved here is substantive and appropriate; no theorem about every conceivable extra regularity axiom is established.

No files authored for the candidate were changed. No remote writes, PR, publication, or solved-status mutation were performed. No new proof search was undertaken.
