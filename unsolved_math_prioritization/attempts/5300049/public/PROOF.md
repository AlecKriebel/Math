# Positive lower Lyapunov exponent and access from an attracting basin

**Outcome: partial analysis; the general question is not resolved here.**

## 1. Question and precise scope

The target is Przytycki's Problem 1.2 in the 1992 *Problems in Holomorphic Dynamics*, printed pp.29–30 ([primary source](https://www.math.stonybrook.edu/preprints/ims92-7.pdf)). Its basin setting is a simply connected domain U in the Riemann sphere, a proper holomorphic self-map f of degree at least two whose iterates converge to a point of U, and a holomorphic extension to a neighborhood of the closure of U. For x in its boundary, assume

    lower_chi(x) = liminf_{n→∞} (1/n) log ||D(f^n)(x)|| > 0.

Must a continuous curve γ:[0,1]→closure(U) exist with γ([0,1))⊂U and γ(1)=x?

We use the spherical derivative, so the statement is coordinate independent. Smooth metrics on the compact boundary give the same lower exponent: changing metric multiplies the n-step norm by a bounded ratio of endpoint metric densities, whose logarithm divided by n tends to zero. No complete or local backward invariance is added to the question.

### Source comparison

Przytycki's 1994 paper gives accessibility for points possessing suitable shrinking pullback telescopes, including the requirement that the relevant inverse images remain in the designated basin. Its Corollary 0.2 gives an almost-everywhere conclusion for positive-exponent invariant measures on a completely invariant rational basin. These hypotheses cannot simply be dropped. See [published paper, Theorem A, conditions (0.0)–(0.3), Theorem B, Corollary 0.2, and Remark 0.7](https://www.impan.pl/~feliksp/access.pdf).

A stronger pointwise formulation appears in [Przytycki's 2021 survey, Theorem 8.1](https://www.impan.pl/~feliksp/Siles.pdf): uniform shrinking of a geometric coding tree and local backward invariance give accessibility for points with positive **lower** exponent. The underline on χ is visible in the PDF but disappears in plain-text extraction. This is not restricted to an existing Lyapunov limit. Consequently, irregularity of the exponent is not a reason to ignore this theorem. The local backward-invariance hypothesis still remains. The [2018 survey, §10](https://www.impan.pl/~feliksp/FP_ICM_Survey_home.pdf) likewise retains it.

For the completely invariant rational attracting-basin subcase, the coding tree in the basin has uniformly shrinking edges, and its backward vertices accumulate on the boundary, as explained in the 1994 paper's Remark 0.4. Together with Theorem 8.1 this gives the requested pointwise conclusion in that subcase. This is a cited literature consequence, not a new theorem claimed here. The original setup is broader.

The rest of this note proves elementary auxiliary statements and pinpoints where five approaches stop. None of the obstruction examples below is asserted to be a counterexample to the holomorphic basin question.

## 2. Attempt 1: turn one orbit into a positive-exponent measure

Let X be a compact forward-invariant subset of the sphere on whose neighborhood f is holomorphic. Put φ=log||Df||, with φ=−∞ at critical points. The function is bounded above, and φ_M=max(φ,−M) is continuous for every positive integer M.

**Proposition 1.** If lower_chi(x)=L>0, every weak limit μ of

    μ_N = (1/N) Σ_{j=0}^{N−1} δ_{f^j(x)}

is f-invariant and satisfies ∫φ dμ≥L. In particular φ is μ-integrable.

**Proof.** Compactness gives weak subsequential limits. For every continuous h on X,

    ∫(h∘f−h) dμ_N = [h(f^N(x))−h(x)]/N → 0,

so μ is invariant. If the orbit ever met a critical point, all subsequent n-step derivatives at x would vanish. Thus all orbit values of φ are finite. For fixed M, along a subsequence N_k defining μ,

    ∫φ_M dμ = lim_k ∫φ_M dμ_{N_k}
             ≥ liminf_k ∫φ dμ_{N_k} ≥ L.

If A is a finite upper bound for φ, the nonnegative functions A−φ_M increase to A−φ. Monotone convergence yields ∫φ dμ=lim_M∫φ_M dμ≥L. Its positive part is bounded and its negative part has finite integral. ∎

Ergodic decomposition then supplies at least one ergodic component with positive integral. This gives a legitimate input to measure-theoretic accessibility results when their basin hypotheses hold. It does not identify the original x with a point in the full-measure set supplied by such a result.

**Exact failure of the point-transfer step.** Let f(z)=z², U={|z|<1}, and

    θ = Σ_{k=1}^∞ 2^(−k²),    x=exp(2πiθ).

The binary digits of θ are one at square positions and zero elsewhere. This expansion is not eventually periodic, since it has infinitely many ones with unbounded gaps. Thus x≠1 and no forward iterate of x is 1. Every orbit point is on the unit circle, where ||Df||=2, so lower_chi(x)=log 2.

For each fixed m, among the first N left shifts of these digits the proportion whose initial m digits contain a one is at most

    m( floor(sqrt(N+m)) + 1 ) / N,

which tends to zero. All other shifted angles lie in [0,2^(−m)]. Uniform continuity of a test function on the circle, first choosing m large and then N large, proves μ_N→δ_1. But x is outside the support {1}. Therefore even a positive-exponent orbit can generate a positive-exponent invariant measure whose support does not contain that orbit's starting point.

In this example x is accessible by a radial segment. It disproves the proposed measure-to-original-point inference, not the target statement.

**Gap after attempt 1:** a theorem about μ-almost every point, or even every point in supp μ, need not say anything about the original x. The remaining basin-side hypothesis is separate.

## 3. Attempt 2: select expanding times from the derivative products

**Proposition 2 (record-time form of the Pliss estimate).** Let real numbers a_i≤A be given. Fix c<b≤A with A>c. Suppose S_N=Σ_{i=1}^N a_i≥bN. Then at least

    ((b−c)/(A−c)) N

indices n≤N satisfy

    Σ_{i=k+1}^n a_i ≥ c(n−k)    for every 0≤k<n.

**Proof.** Set T_0=0, T_n=S_n−cn, and M_n=max_{0≤j≤n}T_j. Whenever M_n>M_{n−1}, n has the claimed property, because T_n exceeds all previous T_k. At each such index the increase of M is at most A−c: indeed T_n=T_{n−1}+a_n−c≤M_{n−1}+A−c. Since M_N≥T_N≥(b−c)N and M_0=0, the number of strict record increases is at least the displayed lower bound. ∎

Apply this with a_i=log||Df(f^{i−1}(x))||. Given 0<c<b<lower_chi(x), the hypothesis holds for all sufficiently large N. Thus the set of these expanding times has positive lower density, and the corresponding suffix derivatives are at least exp(c(n−k)). This is a genuine consequence of the original assumption.

One must not replace this scalar conclusion by any desired geometric pullback conclusion without an argument. In particular, the following often proposed strengthening is false for scalar sequences.

**Proposition 3.** Positive lower average and a uniform upper bound do not imply a_i/i→0, nor that the large negative terms have arbitrarily small average contribution.

**Proof.** Set a_i=1 except at i=2^k, k≥2, where

    a_{2^k}=1−2^(k−2).

For 2^m≤N<2^(m+1), m≥2, summing the geometric series gives

    S_N=N−(2^(m−1)−1).

Hence S_N/N≥1/2 and S_{2^m}/2^m→1/2; the lower average is 1/2. Yet

    a_{2^m}/2^m=2^(−m)−1/4 → −1/4.

For every fixed K>0, at N=2^m and m sufficiently large the term a_N is below −K, so

    (1/N) Σ_{i≤N, a_i<−K} (−a_i) ≥ 1/4−2^(−m).

The limsup is therefore at least 1/4 for every K. ∎

This scalar model has not been realized as a derivative itinerary of a map satisfying the problem. It establishes only that the above extra estimates cannot follow from the two numerical assumptions alone. The 2021 theorem does not demand these extra estimates: its telescope method is more flexible. In particular Proposition 3 is not an objection to that theorem.

**Gap after attempt 2:** record times do not themselves select pullback pieces on the U side. The modern theorem handles positive lower exponents when its local backward-invariance hypothesis is available; that hypothesis has not been proved in the original general setting.

## 4. Attempt 3: contract a local inverse branch and concatenate curves

The simplest direct proof works with an additional component-return condition.

**Proposition 4.** Let q∈∂U, let D be a Euclidean disk centered at q, and let F be holomorphic on a neighborhood of D with F(q)=q, F(D)⊂D and sup_D|F'|≤ρ<1. Suppose

    F(U∩D)⊂U.

If for some z∈U∩D and integer m≥1 the points z and F^m(z) belong to the same connected component of U∩D, then q is accessible from U by a finite-length curve.

**Proof.** An open connected subset of the plane is polygonally connected, so there is a finite polygonal path η in U∩D from z to F^m(z). For k≥0, F^{km}∘η lies in U∩D and joins F^{km}(z) to F^{(k+1)m}(z). They can be concatenated in order on intervals [1−2^(−k),1−2^(−k−1)]. Convexity of D and the derivative bound give |F(w)−q|≤ρ|w−q| and length(F^{km}∘η)≤ρ^{km}length(η). Thus the concatenation tends uniformly to q on its final intervals and extends continuously by γ(1)=q. Its length is at most length(η)/(1−ρ^m). ∎

For a repelling periodic boundary point, the inverse of the corresponding return map fixing q admits such a contracting disk after shrinking it. The inverse-function theorem supplies this analytically. It does not supply F(U∩D)⊂U, or the component-return condition. A forward-invariant U need not be declared locally backward-invariant merely because an inverse branch exists in an ambient disk.

For f(z)=z^d, d≥2, all boundary points of the unit disk are accessible explicitly by t↦tx; moreover ||D(f^n)(x)||=d^n there. This is a consistency check, not evidence that the missing component conditions hold for a general basin.

**Gap after attempt 3:** the available contracting map acts on the surrounding surface. A curve constructed there must be shown to stay in the specified basin. The added hypotheses above precisely make that step legitimate, and have not been derived in general.

## 5. Attempt 4: nested approach domains and prime-end topology

**Proposition 5.** For a plane domain U and q∈∂U, the following are equivalent:

1. q is accessible from U.
2. There exist nonempty connected open sets V_n⊂U with V_{n+1}⊂V_n, q∈closure(V_n), and diam(V_n)→0.

**Proof.** Suppose γ gives an access. Choose increasing t_n→1 so that γ([t_n,1))⊂B(q,2^(−n)). Let V_n be the component of U∩B(q,2^(−n)) containing this connected curve tail. Components of an open planar set are open and path connected. Each smaller tail is in V_n, so V_{n+1}⊂V_n. Also q∈closure(V_n) and diam(V_n)≤2^(1−n).

Conversely choose z_n∈V_n and a path in V_n from z_n to z_{n+1}. Concatenate those paths on intervals tending to 1. For w∈V_n we have |w−q|≤diam(V_n), by approximation of q with points of V_n. The final portions therefore tend uniformly to q. Adding the endpoint gives a continuous access. ∎

Merely having accessible points converge to q does not provide this nested system. For a concrete topological control, consider

    U=((0,1)×(0,1)) \ ⋃_{n≥2} ({1/n}×(0,1/2]),
    q=(0,1/4).

The removed slits are relatively closed in the rectangle, so U is open. Any two points can be joined by first moving within their vertical strips above height 1/2, then across, so U is connected. Its complement in the sphere is connected: every slit attaches to the rectangle's outside boundary. By the usual plane-domain criterion, U is simply connected.

Each q_n=(1/n,1/4) is accessible horizontally from the adjacent strip, and q_n→q. Nevertheless q is inaccessible. If a curve inside U tended to q, a final tail would have heights strictly between 1/8 and 3/8. At some time t_0 on that tail its horizontal coordinate is a>0. Choose n with 1/n<a. Later the horizontal coordinate is less than 1/n. The intermediate value theorem forces the curve to meet the removed slit x=1/n at a height below 1/2, a contradiction.

There is no holomorphic map asserted on this example. It tests only the proposed topological passage from dense accessible points to every boundary point.

**Gap after attempt 4:** to apply Proposition 5 at the specified x one must produce compatible components at arbitrarily small scales. Density of accessible periodic points, or a full-measure accessible subset, does not produce those components.

## 6. Attempt 5: diagonal limits of shrinking coding-tree edges

Perhaps uniform shrinking alone could make the set of branch endpoints closed. The following exact abstract tree shows why that compactness step is invalid.

For a finite binary word w of length n, define a real vertex v(w) as follows. Set v(empty)=1. If w has no one, put v(w)=1. Otherwise let k be the position of its first one (positions start at 1), and put

    v(w) = 1 − min(max(n−k,0),k)/(k+1).

Join each vertex to its parent's vertex by the real segment between their values. This is a map of an abstract rooted binary tree into the plane; it is not asserted to be an embedded tree or a holomorphic coding tree.

**Proposition 6.** Edge diameters tend to zero uniformly with their generation; every infinite branch has an endpoint; the set of branch endpoints is not closed.

**Proof.** The edge ending at generation n has nonzero length only when its first one was at a position k satisfying k<n≤2k. That length is exactly 1/(k+1)≤2/(n+2), and otherwise it is zero. This proves uniform shrinking.

The all-zero branch has every vertex equal to 1. A branch whose first one is at k reaches the value 1/(k+1) by generation 2k and then stays there. Thus the endpoint set is exactly

    {1} ∪ {1/(k+1): k≥1}.

It has 0 in its closure, but no branch ends at 0. The branches 0^(k−1)1000… converge symbolically to 000…, while their endpoints tend to 0 rather than to the limiting branch's endpoint 1. ∎

This counterexample to a bare diagonal argument has all branches convergent and a quantitative uniform edge bound. It does not satisfy the extra dynamical and telescope hypotheses of the published theorem. In that theorem the significant telescopes, rather than uniform shrinking alone, control how a diagonal branch approaches the intended point.

**Gap after attempt 5:** even if roots and edges can be chosen and shrunk, one still has to prove that the selected boundary point admits the requisite basin-side telescopes. Compactness of the symbolic space alone does not establish it.

## 7. What is proved, and what remains

The auxiliary results above are complete proofs of their stated claims. They give:

- an invariant positive-integral measure from any positive-lower-exponent orbit;
- a quantitative positive density of expanding suffix times;
- an explicit finite-length access under local contraction, basin preservation and component return;
- a precise nested-domain criterion for accessibility;
- exact limitations on three shortcuts (measure transfer, naive recurrence inference, and diagonal endpoint compactness).

The published pointwise theorem with local backward invariance is a substantial known positive result and covers the completely invariant rational attracting-basin subcase. We have neither removed that local hypothesis in the original setting nor constructed a holomorphic basin violating the conclusion. The scalar, comb and abstract-tree examples address only the stated proof shortcuts. Therefore this packet is an unresolved, five-attempt analysis, with no full solution, novelty, or general counterexample claim.

The executable checks corroborate only finite arithmetic and structural instances of Propositions 2, 3 and 6 and the simple control examples. They are not a formal proof checker and do not verify accessibility in arbitrary Julia sets.
