# Independent audit: K3 Problem 3.47, elliptic Reeb orbits

Audit date: 2026-10-08 UTC.

## Verdict

Accept the separately pinned corrected packet as an authored partial-results and failed-inference record. Both universal questions remain unresolved after five mathematical approaches. No counterexample, universal existence theorem, or novelty claim is established.

The only required correction found is source attribution: K3 itself gives the inclusive spectral definition of ellipticity in its contact-topology introduction on printed/PDF page 160. The frozen report looked only at the problem's page 164 when discussing where that convention came from. Its mathematical convention was already right. The correction cites the controlling K3 definition directly and updates the corresponding audit and source-inspection metadata.

Frozen eight-file packet manifest SHA-256:

    e807c15d1bcd72e46389a6f9955a9a8c6ce73e764b036ae2a08aa356d9b9c4a1

Corrected eight-file packet manifest SHA-256:

    7beb5ce3cb8b294c18ab9256c896a79cd8fe8920e46bd253c30a02bbe849407f

Every original file remains byte-for-byte unchanged. `SOURCE_ATTRIBUTION_CORRECTION.patch` changes only the relevant wording in `REPORT.md` and `AUDIT.md`, K3's inspection entry in `SOURCE_PINS.json`, and the consequent manifest hashes. `STATUS.json`, `README.md`, the exact verifier, and its recorded output are unchanged.

## 1. Statement, convention, and elementary reduction

Both K3 subquestions were checked in the pinned 2026 author manuscript at page 164, including visual inspection. They contain no genericity, finite-orbit, nondegeneracy, pinching, or symmetry assumption. Page 160 was separately rendered and visually inspected. Its section-level ellipticity definition includes all transverse eigenvalues of modulus one. Abreu–Macarini's introduction and footnote agree.

For a real symplectic two-by-two return map, the determinant is one and the characteristic polynomial is t^2 - tr(P)t + 1. The discriminant gives exactly the report's three cases. At trace +2 or -2, nontrivial Jordan blocks remain included. A trace -2 simple orbit can itself avoid eigenvalue +1 while its double cover is degenerate; nothing in the reduction mistakenly excludes this case. Any orbit degenerate in the usual eigenvalue-+1 sense has trace +2 and already satisfies the inclusive conclusion.

Therefore a genuine counterexample must have only hyperbolic simple orbits, with every cover nondegenerate. Conversely, if an iterate has all eigenvalues on the unit circle, the moduli of the underlying eigenvalues were already one. The round Hopf example correctly diagnoses the failure of a strictly-nonreal reinterpretation. Positivity relative to the chosen coorientation is harmless: reversing the sign of a defining contact form reverses its Reeb direction and inverts return maps, preserving inclusive ellipticity.

The radial pullback formula uses homogeneity of the Liouville form and its vanishing on radial vectors. It gives star-shaped geometry, not convexity. The strict-convexity implication used later is the dynamical-convexity result identified in the cited sources.

## 2. ECH finite and filtered counting

### Finite case and exact hypotheses

The all-hyperbolic reduction supplies the nondegeneracy needed to use the ordinary ECH chain complex. Hyperbolic admissibility restricts the multiplicity of each simple orbit to one. On S^3 every orbit set is in homology class zero. With N simple orbits there are at most 2^N admissible orbit sets, including the empty set.

The cited homogeneous U-sequence has nonzero classes in distinct gradings: torsion of the grading ambiguity class permits integer relative grading and U changes grading by two. These classes are linearly independent. Finite chain dimension cannot support their infinite-dimensional span in homology. This argument does not identify ECH generators with single orbits.

The stronger literature route has the correct scope. The two-or-infinitely-many theorem requires a closed connected contact three-manifold and torsion first Chern class, with no nondegeneracy condition. The exactly-two theorem requires a closed contact three-manifold with exactly two simple orbits and concludes their irrational ellipticity and nondegeneracy. S^3 has zero H^2, so the former torsion condition is automatic. These statements settle the finite-orbit case only.

### Filtered asymptotic

Bounded-period simple orbits of a fully nondegenerate nonsingular field on a compact manifold form a finite set. Otherwise compactness gives a limiting periodic orbit with positive limiting period, and isolation at that period, including a possibly multiple cover, contradicts the accumulation. Requiring nondegeneracy of all covers is important here and is available.

Let V be the contact volume. For any fixed epsilon in (0,1), choose delta > 0 with (1+delta)(1-epsilon) < 1. The U-sequence Weyl law gives c_k^2 <= (1+delta)2Vk once k is sufficiently large. Thus every sufficiently large k up to floor((1-epsilon)L^2/(2V)) has c_k < L. The finitely many omitted classes produce the reported O(1) loss.

Each such class lies in the image of filtered ECH. Independence in full ECH gives the same lower bound on the dimension of that image, hence on the filtered chain dimension. Positive orbit actions ensure that every orbit in a generator of total action below L itself has action below L. Consequently the filtered dimension is at most 2^N(L), even though many subsets have action too large to appear.

This proves liminf 2^N(L)/L^2 >= 1/(2V). The logarithmic notation is valid as a one-sided asymptotic: the negative part of N(L) - log_2(L^2/(2V)) tends to zero. It does not assert that the difference itself tends to zero, nor give an upper bound. Infinitely many hyperbolic orbits remain fully compatible with this necessary lower bound.

## 3. Global disks and all-iterate Lefschetz constraints

The disk-section theorem cited as Hryniewicz's Theorem 1.3 states the Hofer–Wysocki–Zehnder result with a binding of lower-semicontinuous disk Conley–Zehnder index 3. It does not require genericity. It supplies the open-disk return dynamics, but does not by itself supply the extra closed-disk regularity and aperiodic-boundary assumptions used for the report's Lefschetz calculation. The report keeps those additional assumptions explicit.

At a nondegenerate area-preserving fixed point, det(I-A)=2-tr(A). Thus negative hyperbolic points have positive local index, as elliptic points do; positivity of local index does not prove ellipticity. A least-period-d cycle contributes d fixed points to the n-th iterate when d divides n. Its negative-hyperbolic contribution changes sign precisely when n/d changes parity.

Subtracting the identities at 2^k and 2^(k-1) cancels all earlier-cycle terms except the sign change of the previous top cycle. The remaining equality is 2^k(b_(2^k)-a_(2^k)-b_(2^(k-1)))=0. This verifies the recurrence and forces a negative hyperbolic cycle at every dyadic period in the stated conditional setting.

For n=2^k m with m odd, one negative cycle at each dyadic least period gives the total 2^k - sum_(i<k)2^i = 1. This checks every integer n, not only the dyadic iterates. It is a formal solution to the index equations. Neither area-preserving disk-map realization nor Reeb-flow realization follows. A finite truncation fails, and is used as an explicit negative control in the audit.

## 4. Hamiltonian indices and convexity

For the standard contact sphere in dimension three, the Abreu–Macarini specialization uses n=1 and fiber Robbin–Salamon index 4. Their higher-iterate criterion therefore gives the stated bounds 3 and 4k-1 for a fixed integer k>1. Their antipodal criterion and Hessian-pinching criterion are separate additional hypotheses. The pinching quantity is the bound on the Hessian of the homogeneous degree-two Hamiltonian, not an arbitrary ratio of Euclidean radii.

For a hyperbolic two-dimensional symplectic path, the Conley–Zehnder index iterates linearly. An index-three binding is negative hyperbolic under the counterexample assumption, and its k-th iterate has index 3k. The shortfall from 4k-1 is exactly k-1>0. Dynamical convexity alone does not close this gap.

The quarter-turn fundamental solution is obtained from (JH_a)^2=-I. Multiplying the two specified segments gives diag(-2,-1/2), with determinant one and trace -5/2. The vector e_1 traverses angle pi during the two segments; appending a full positive rotation changes its lifted angle to 3pi without changing the endpoint. For this negative hyperbolic endpoint the fixed-trivialization Conley–Zehnder index is 3. Small smoothing within the positive-definite cone leaves the endpoint nondegenerate and preserves that index. The exact matrix need not survive smoothing, and the report does not claim it does.

This establishes a local linear-system obstruction to a proposed inference. It does not construct a convex hypersurface with all its closed characteristics hyperbolic.

## 5. Topology, uniform rates, and compactness

The cited Anosov criterion really has both hypotheses retained in the report: uniform hyperbolicity of the closure of periodic trajectories and stable/unstable transversality for every pair of periodic orbits. Pointwise hyperbolicity does not provide either one.

For the formal return matrices with multipliers 2 and 1/2 and periods j, the expanding rate per unit time is log(2)/j. Applying a hypothetical uniform exponential bound to m returns and then letting m tend to infinity forces log(2)>=kappa*j for every j, which is impossible for a fixed positive kappa. This demonstrates the missing rate information; it is not a realization of those data on S^3. The conditional use of the no-Anosov fact is therefore correctly scoped.

The bounded-period closure lemma is valid. C^2 convergence of contact forms gives C^1 convergence of their Reeb fields, because the formula for the field uses the form and its first derivatives and the limiting contact denominator stays uniformly nonzero. Flow boxes and nonvanishing of the limiting field provide a common positive lower period bound. Compactness then produces limiting starting points and a period in a compact subset of (0,B]. C^1 flow convergence identifies the limiting transverse return derivative after continuous frame choices. The trace interval [-2,2] is closed. A multiple-cover limit causes no loss, by the earlier eigenvalue-modulus argument.

If the limit has only hyperbolic periodic orbits, failure of the approximating elliptic periods to tend to infinity would yield a bounded subsequence and contradict the lemma. Merely having arbitrarily large periods is a weaker statement; the report correctly states period escape. The analogous geodesic conclusion is valid after smooth identifications of the varying unit bundles.

The fixed-antipodal symmetry distance follows from the triangle inequality at antipodal points and is attained by averaging. The rescaled Reeb-field formula has the correct sign and factor f^(-2). If its horizontal correction vanished identically, df=h beta and d(df)=0 restricted to the contact plane would force h=0. No orbit-preserving or dynamical-convexity-preserving averaging principle has been smuggled in.

## 6. Current sources and limits of the review

Seven supplied PDF hashes and sizes were rechecked. The theorem locations were read in those pinned files. Primary online metadata and available primary PDF renderings were checked again on the audit date. `SOURCE_AUDIT.json` distinguishes these operations; it does not claim a second byte-identical PDF download from a browser rendering.

Shibata's manuscript was confirmed as v1, posted 14 September 2026. Its general result asserts a positive hyperbolic simple orbit under nondegeneracy and at least three simple orbits. The b1=0 intermediate result excludes an all-negative-hyperbolic simple spectrum. These results do not exclude a mixed all-hyperbolic spectrum and do not establish elliptic existence. This audit checks attribution and hypotheses, not the preprint's full holomorphic-curve proof. None of the packet's completed elementary deductions relies on that proof.

A bounded current-source search also encountered orbit-infinitude results and 2026 higher-dimensional finite-orbit ellipticity results. Their additional scope does not settle either universal question here. Failure to retrieve a solution is not evidence of novelty or a guarantee that no unindexed solution exists.

## 7. Reproducibility and negative controls

The frozen and corrected exact verifiers were each run normally, with -O, and with -OO. All six runs reproduced the recorded 762-byte output, SHA-256 c15a15b794bd5a48682ae7c807b0e255f02e2f1cab55e32254be04044e71c637.

Every run used actual UID/EUID 1000 inside bubblewrap with the complete filesystem read-only and no writable rebind. Opening each frozen, corrected, and independent verifier for writing returned EROFS in all three modes. Read-only status was not inferred from chmod bits. No network-namespace isolation is claimed.

The independent exact script uses a different matrix representation, binary powering, and a Cayley–Hamilton trace recurrence. It checks 1,849 rational quarter-turn parameter pairs, 180 integer determinant-one matrices with 2,880 power checks, 4,096 formal Lefschetz identities, 20 dyadic recurrences, 27 filtered-subset cases, and 1,023 higher-iterate gaps. It explicitly includes both parabolic boundaries and the identity-return convention.

Six meaningful mutations were rejected for their intended reasons in each Python mode: reversing the quarter-turn product, reversing the index parity, dropping the cycle weight, truncating the dyadic model, reversing the index inequality, and changing a parabolic trace target. All 18 controls raised explicit exceptions, rather than optimized-away assertions. A same-size one-byte alteration also changed the frozen report's hash. All input hashes were rechecked after execution.

Reproduction command, with the two public packet directories supplied explicitly:

    python3 reproduce_audit.py ORIGINAL_PUBLIC CORRECTED_PUBLIC

The driver emits `REPRODUCIBILITY_RESULTS.json` content on stdout and writes nothing. Finite arithmetic controls are diagnostic evidence, not proofs of ECH, ODE compactness, or universal orbit existence. The mathematical deductions above were reviewed separately.

## Acceptance boundary

Accept only the corrected partial-results interpretation. Reject descriptions claiming a solution, a realized all-hyperbolic example, an implication from pointwise hyperbolicity to Anosov, a smooth closed-disk return extension without its hypotheses, or certified proof of the new preprint. Source checks and this independent review add zero mathematical approaches. No publication or queue update is performed by this audit.

Public source links are recorded in `SOURCE_AUDIT.json` and the corrected packet's bibliography. This audit contains authored mathematics and public verification metadata; it includes no source PDF, copied source-body excerpt, dataset contents, or private coordination record.
