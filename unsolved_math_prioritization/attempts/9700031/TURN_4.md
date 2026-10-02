# Turn 4: sampled traffic completion and the remaining positive-mark moment

**Author turn 4 of 5. The ordinary-axiom beta>3 target remains unresolved.** This turn tries to remove the continuum-version obstruction without assuming a jointly measurable family of individual routes. It constructs a traffic measure from countably sampled routes, and identifies it with the intended integral whenever (JM) is available. This is a completion of the traffic object, not a proof that arbitrary bare FDDs have a jointly measurable deterministic route realization.

## 1. Exact technical scope

Use the source's measurable FDD condition (2.13), countable sampled-subnetwork construction, and joint intrinsic-major-road extension discussed in Proposition 6.3. More explicitly, assume a standard measurable realization of the background sampled network, its countably many sets E_r for rational r>0, and the routes between any additional countable independent sample of endpoint locations. Joint kernels for each finite set of extra locations are measurable, consistent, and have the stated Euclidean covariance. Call this countably sampled setup (CS).

This is the setup needed to implement the source sampling definitions. We do not assert a fully formal construction from an arbitrary nonmeasurable assignment of FDDs. Unlike (JM), (CS) does not assert a jointly measurable path for every continuum endpoint pair in a realized environment.

All statements below hold for a fixed exponent. At beta=3 the ordinary first route-length moment is sufficient. At beta=3+alpha>3 we require the additional intrinsic-mark moment M_alpha from Turn 3 when claiming finite expected traffic. Without that moment, the proof below does not establish the original beta>3 finiteness assertion.

## 2. The abstract exchangeable-array lemma

Let (mu_ij)_{i!=j} be a jointly exchangeable array of random locally finite positive Borel measures on R^2, with mu_ij=mu_ji, and let B be an auxiliary background unchanged by relabeling the array. Assume

    E mu_12(K) < infinity                                      (1)

for every bounded Borel K. Let I_n be the sigma-field of events invariant under all permutations of the first n labels, fixing labels after n and the background, and let I_infinity=intersection_n I_n.

For a bounded Borel set A, finite-group averaging gives

    (1/[n(n−1)]) sum_{i!=j≤n} mu_ij(A)
          = E[mu_12(A) | I_n].                                 (2)

To verify this, average the random variable mu_12(A) over the finite group of label permutations. The average is invariant and has the same integral as mu_12(A) against every invariant bounded random variable, precisely the defining conditional-expectation property. Each ordered pair occurs equally often in the group orbit.

The reverse martingale convergence theorem now gives a.s. and L1 convergence of (2) to

    nu(A) := E[mu_12(A) | I_infinity].                          (3)

Conditional expectation of a random measure yields a random Borel measure nu. For completeness, this can be constructed on a countable generating ring on each bounded window, using the conditional distribution kernel on the standard Borel space R^2 and then increasing the windows. Its expected mass on each bounded window is finite by (1), so it is locally finite almost surely. Taking a countable determining family of continuous compactly supported functions and bounds on an exhaustion by compact sets also proves vague convergence of the empirical measures to nu. For a particular additional bounded Borel A, (2) still converges by the same reverse martingale argument; vague convergence alone is not being used to claim convergence on arbitrary sets.

If a random Borel set H is measurable with respect to the invariant background, restriction commutes with this construction:

    E[mu_12 restricted to H | I_infinity] = nu restricted to H. (4)

Thus background road bands can be handled coherently. No independence between different pair measures is assumed. Ordinary independent-pair laws of large numbers would not justify this lemma.

## 3. Applying the lemma to importance-weighted route samples

Choose any fixed probability density g on R^2 with 0<g(x)<infinity everywhere, and sample X_1,X_2,... independently from g, independently of the source route FDDs and the background Poisson sampling. Use (CS) to realize all their routes jointly with the background E_r. For a fixed road band F_r=E_r minus E_{2r}, define

    mu_ij^(r)(A) = |X_j−X_i|^(−beta)/[g(X_i)g(X_j)]
         * H^1(R(X_i,X_j) intersect F_r intersect A).            (5)

Distinct endpoints have probability one, and each pair measure is locally finite because the individual route has finite length. The array is jointly exchangeable, including its endpoint marks.

At beta=3 the unconditional first moment is exactly

    E mu_12^(r)(A) = 2 pi |A| d log 2.                          (6)

Indeed the factors g cancel when the two sampled locations are integrated out. The planted-route support, scaling and mass-transport calculation in Turn 3 uses only these measurable finite-location kernels and the sampled road process at this expectation level. The planted-route support follows from the source planted-point property, or its superposition/expectation argument; a pathwise continuum route integral is unnecessary for (6).

The abstract lemma gives a locally finite random band-traffic measure nu_r and the a.s. empirical limit on bounded test sets. The mean remains (6). Use one common sampled array and its invariant sigma-field for all dyadic bands. By (4) these limits are consistent restrictions of one positive random measure on the union of the road bands.

Turn 3's major-road cutoff proof uses only sampled witnessing routes, so it holds in (CS): a bounded spatial window meets only finitely many bands above any fixed road-size threshold. Therefore

    nu restricted to E_r is locally finite almost surely        (7)

at beta=3, and nu is sigma-finite on the union of E_r. The empirical importance-weighted traffic on E_r also converges locally: in a bounded window the same finite random collection of bands suffices for every sample size, since the absence of higher background roads is a point-set statement. Their finitely many empirical limits can be added. This does not exchange a limit with an uncontrolled infinite series.

For beta=3+alpha>3 and M_alpha<infinity, Turn 3 identity (13) supplies finite expectation on E_r itself. The lemma then applies directly to the measures in (5) with F_r replaced by E_r. This yields the analogous locally finite traffic completion in the stated moment range. It does not establish M_alpha<infinity under the ordinary axioms.

## 4. Independence of the auxiliary endpoint sampling density

The joint law of the completed traffic and background does not depend on the positive density g. Here is a coupling argument that also explains why importance weights are essential.

Given two positive densities g and h, sample endpoint locations with density q=(g+h)/2. Independently conditional on each location x, label it G with probability g(x)/(2q(x)), otherwise H. Equivalently, labels are initially fair independent choices and locations then have their labeled density. Conditional on all locations, draw the routes through their common (CS) kernel; the labels do not enter that kernel. The G and H subsequences have the respective sampled-network laws.

For a bounded spatial test function and an integrable band measure, write a_ij for its unweighted geometric pair contribution. Conditional on the locations and route array,

    E[ 4 * 1{i,j both G} * a_ij/[g(X_i)g(X_j)] ]
                         = a_ij/[q(X_i)q(X_j)].                 (8)

The normalization for the G subsequence differs from the factor 4/n(n−1) by a ratio tending to one almost surely, since its count divided by n tends to 1/2.

The difference between the thinned weighted average in (8) and its conditional mean tends to zero in L1. First truncate the importance-weighted pair contributions and restrict both label probabilities to be at least epsilon. The resulting summands are uniformly bounded. Pairs with disjoint labels are conditionally independent; only O(n^3) out of O(n^4) ordered pair-pairs overlap, so the conditional variance of their average is O(1/n). The truncated L1 difference therefore vanishes. Removing the truncation and then epsilon uses the integrable band first moment: the expected tails of both weighted averages are exactly the corresponding endpoint integrals, and decrease to zero by dominated convergence. Positivity is used for the tail bounds. This establishes the claim without a boundedness assumption on the original importance ratios.

The mixed-density and G-subsequence averages already have almost-sure band limits by Section 2. Their vanishing difference in probability forces those limits to agree in the coupling. The same argument applies to H. Taking a countable determining class gives equality of the random band measures, jointly with the background. A countable collection of bands yields the claimed density-independence for nu.

## 5. Covariance and agreement with a measurable continuum version

Translation, rotation or dilation transforms the sampled endpoint density into another positive density. The source (CS) covariance and the density-independence just proved therefore transfer Euclidean covariance to the completed traffic measure. For a dilation c, the importance-weighted endpoint elements contribute c^4, route length contributes c and the kernel contributes c^(−beta). Hence the spatial push-forward has distributional factor c^(beta−5), matching the source statement.

If a jointly measurable route realization (JM) is given, condition on the complete realized network and its road process. The locations X_i are iid and the pair contribution in (5) is then a deterministic symmetric measurable kernel of X_i,X_j. The integrable U-statistic strong law shows its band average converges to its endpoint integral. One can also prove this special law by first approximating integrable kernels by finite sums of bounded product kernels, applying the scalar iid law, and controlling the L1 tails through the reverse-martingale limit. Consequently the completed band measure agrees almost surely with the continuum traffic integral defined in Turn 1. The finite-band assembly extends agreement to each E_r at beta=3.

Thus this construction is not a different object on already measurable SIRSNs. Without (JM), it supplies a sampled-traffic completion with the prescribed empirical interpretation. It does not manufacture a jointly measurable deterministic route map, and that stronger version assertion remains unproved.

## 6. What the construction leaves open above beta=3

At beta=3+alpha, the exact unconditioned pair expectation on E_r is proportional to M_alpha. If M_alpha is infinite, the integrable-array lemma cannot be invoked on E_r; nor does an infinite unconditioned mean prove that the completed traffic is infinite almost surely. Conditional means may be finite in each realization while having infinite average, as the beta=3 whole-cutoff traffic already demonstrates.

This leaves two possible routes for the remaining author turn: establish enough positive road-size mark integrability from the geometric SIRSN axioms, or prove quenched finiteness by a stronger localization that does not demand finite unconditioned expectation. No such implication has been established in this turn. No counterexample satisfying all SIRSN axioms has been constructed.

## 7. Scope and turn count

The reverse-martingale and U-statistic tools are classical probability, here applied explicitly to the source countable-route data. The proof claims a measurable traffic completion under (CS), not a previously unknown general path-version theorem. Independent review is required for this construction, especially the band integrability, common invariant sigma-field and density-change coupling.

**Status: original ordinary-axiom 3<beta<4 unresolved; author count 4/5.** Under (JM), all earlier results remain exactly as stated. Under (CS), the critical traffic object can be defined through sampled routes and agrees with the JM traffic when present. Uncalibrated progress estimate for the full target: 60%. No novelty claim.
