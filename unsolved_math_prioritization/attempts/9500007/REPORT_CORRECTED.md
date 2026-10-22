# Shy reflected-Brownian couplings: scope, reductions, and remaining obstruction

## Outcome

The implication in Burdzy's Problem 7 is not resolved here. No complete resolution was located in the bounded primary-source search completed on 8 October 2026. The current author-maintained page still presents the question without a solution notice. This is a search result, not a certification of worldwide openness or priority.

The proofs below establish restricted reductions and elementary obstructions. In particular, a twice continuously differentiable deterministic map between normally reflected Brownian motions in a regular Euclidean domain must be a rigid Euclidean isometry. This does not construct such a map from an arbitrary shy coupling. No novelty claim is made for these reductions.

## 1. Exact target and conventions

For a bounded connected open set D in R^d, d >= 2, the question is whether the existence of reflected Brownian motions X,Y on one probability space with

    P(inf_{t >= 0} |X_t-Y_t| >= epsilon) > 0

for some deterministic epsilon > 0 implies the existence of another such pair X',Y' and a single deterministic, time-independent function f with

    P(Y'_t=f(X'_t) for every t >= 0) = 1.

The separation constant and initial points need not be inherited from the first pair. This is an existential implication. Showing that one shy coupling is not a function coupling does not disprove it. [Burdzy, Problem 7](https://sites.math.washington.edu/~burdzy/open_mathjax.php).

The source specifies no common filtration, co-adaptedness, joint Markov property, regularity or measurability of f, boundary regularity, or initial-law convention. We do not silently add these. A reflected process takes values in the closure of D; reflection on a general rough open set requires a separately specified construction. All semimartingale arguments below explicitly use ordinary normal reflection in bounded connected C2 domains. Results concerning a Borel f or a time-homogeneous Feller Markov coupling are labeled accordingly. They do not cover every interpretation of the source statement.

For continuous paths, the event involving all times equals the event involving nonnegative rational times. Also P(inf |X-Y| > 0)>0 is equivalent to existence of a deterministic positive epsilon with the displayed positive-probability bound, by a countable union over epsilon=1/n. Positive-probability separation is weaker than almost-sure separation. The graph and manifold analogues are different targets.

## 2. Literature boundary

- Benjamini, Burdzy and Chen's *Shy couplings*, published in 2007, develops Markov couplings with specified marginal transition behavior. Its author/preprint files were inspected in Sections 2–4. The graph example is numbered 3.8 in both retrieved early files; the problem page refers to published Example 3.9. We do not claim that these are byte-identical published versions. The annulus rotation example already supplies rigid shy couplings. [Preprint](https://arxiv.org/abs/math/0509458), [publication](https://doi.org/10.1007/s00440-006-0008-3).
- Kendall's *Brownian couplings, convexity, and shy-ness* proves nonexistence results for co-adapted couplings in bounded convex domains, including all bounded planar convex domains. These do not apply automatically to arbitrary couplings. [Paper](https://arxiv.org/abs/0809.4682).
- Bramson, Burdzy and Kendall's published electronic reprint, arXiv:1007.3199v4, Theorems 1–2, rules out shy co-adapted couplings in bounded CAT(0) domains satisfying uniform exterior-sphere/interior-cone conditions, including the corresponding simply connected planar domains. Its Section 5.3 conjectures existence of a rigid-motion shy coupling whenever a shy co-adapted coupling exists; Section 5.4 explicitly separates the non-co-adapted question. [Paper](https://arxiv.org/abs/1007.3199).
- Their *Rubber Bands, Pursuit Games and Shy Couplings*, Theorem 5.5, excludes shy co-adapted couplings in bounded CL domains, including the stated regular star-shaped class. Section 6 shows that a stable rubber band does not suffice for shyness: an added large region can destroy it. Thus a deterministic evasion strategy alone is not a Brownian shy-coupling construction. [Paper](https://arxiv.org/abs/1207.0597).

Boundary conditions and coupling classes in these results matter. Nonexistence in a restricted co-adapted class makes the restricted implication vacuous there; it does not settle the literal broader premise.

## 3. Smooth deterministic-map rigidity

**Proposition 1.** Let D be a bounded connected C2 domain. Let X and Y be normally reflected Brownian motions in its closure, and suppose Y_t=f(X_t) simultaneously for all t almost surely. Assume f extends to a C2 map on a neighborhood of the closure. No co-adaptedness of the given pair is assumed. Then

    f(x)=Qx+b on the closure of D,

where Q is orthogonal and QD+b=D.

**Proof.** For ordinary reflected Brownian motion,

    X_t=X_0+B_t+integral n(X_s) dL_s,

where the reflection term has locally finite variation. Ito's formula therefore gives the pathwise quadratic-covariation identity

    [f_i(X),f_j(X)]_t
      = integral_0^t (Df Df^T)_{ij}(X_s) ds.

The process Y is itself reflected Brownian motion, so its quadratic covariation is delta_ij t. This identity is a path-law fact and does not require that the Brownian part of Y remain a martingale in the filtration of X. Differentiation in time yields Df(X_s)Df(X_s)^T=I for almost every s, almost surely. A reflected Brownian motion in a bounded connected C2 domain has strictly positive interior transition density at every positive time. Tonelli's theorem and continuity of Df consequently imply

    Df(x)Df(x)^T=I for every x in D.

The square matrix Df is orthogonal, so its columns e_i=partial_i f form an orthonormal basis. Put A_kij=<partial_k partial_i f,e_j>. Equality of mixed partials makes A symmetric in its first two indices; differentiating <e_i,e_j>=delta_ij makes it antisymmetric in its last two indices. Consequently

    A_kij=A_ikj=-A_ijk=-A_jik=A_jki=A_kji=-A_kij,

and A=0. All second derivatives of f vanish. Connectedness gives f(x)=Qx+b with one constant orthogonal Q, and continuity extends this identity to the closure.

At a positive time, the supports of X_t and Y_t are both the closure of D. Since f is continuous and now an affine isometry, support of f(X_t) is f(closure D). Hence f(closure D)=closure D. A C2 domain is regular open, so taking interiors gives f(D)=D. This proves the proposition. □

**Proposition 2.** Under the hypotheses of Proposition 1, the pair is shy if and only if f has no fixed point in the closure of D. If it is shy, its separation is uniformly positive on every path, not only on an event of positive probability.

**Proof.** If f has no fixed point, compactness gives min_{closure D}|x-f(x)|>0. Conversely, if f(z)=z, then |x-f(x)| <= 2|x-z|. Reflected Brownian motion in a bounded connected C2 domain visits every nonempty relative neighborhood of z almost surely. One way to see this is to use strict positivity and continuity of the Neumann heat kernel at a fixed positive time on the compact closure: every such neighborhood has a uniform positive probability of being entered at each sufficiently spaced observation. The Markov property bounds perpetual avoidance by (1-p)^n, which tends to zero. Apply this to a countable sequence of shrinking neighborhoods. Thus inf_t |X_t-f(X_t)|=0 almost surely. □

**Corollary 3 (centroid obstruction).** If the volume centroid c of a bounded connected C2 domain lies in its closure, it admits no shy function coupling with f as regular as in Proposition 1.

Indeed, any affine isometry preserving D preserves volume and fixes its centroid: Qc+b=c. Proposition 2 applies. This is only a smooth-map obstruction, not a nonexistence theorem for all shy couplings or all measurable maps.

**Converse construction.** If QD+b=D and Qx+b has no fixed point in the closure, applying this map to X transforms its driving Brownian motion to QB and its inward normal to Qn. The transformed Skorokhod equation is again normal reflected Brownian motion. Thus Y=QX+b is a co-adapted shy coupling. For an annulus a<|x|<b in R2 and nonzero rotation angle theta modulo 2pi, its separation is at least 2a|sin(theta/2)|. This is the familiar symmetry construction, not a new solution.

**Remaining gap.** Neither Proposition 1 nor its converse turns an arbitrary separated joint process into a deterministic map. Even completing a classification for every measurable f would leave this existence step.

## 4. A stationary joining reduction, and failure of generic purification

A Markov coupling here means a time-homogeneous Markov process Z=(X,Y) whose transition kernel has the prescribed marginal kernels from every starting pair. A Feller semigroup below is strongly continuous on continuous functions on the compact state space.

**Proposition 4.** Let Z be a jointly measurable Feller Markov coupling on S×S, where S is compact metric, and suppose the marginal semigroup has a unique invariant probability m. If

    P(Z_t in K for every t >= 0)>0

for a closed set K in S×S, then there is an invariant probability nu of the joint semigroup supported on K, and both marginals of nu are m.

**Proof.** For continuous g and a fixed h>0, write

    A_t=g(Z_{t+h})-P_h g(Z_t).

Conditional expectation of A_t given the information at time t is zero. If s>=t+h, A_t is measurable by time s and E[A_s | F_s]=0. Therefore E[A_t A_s]=0. Since |A_t|<=2||g||, the variance of T^{-1} integral_0^T A_t dt is at most 8h||g||^2/T. Along T=n^2 these variances are summable. Chebyshev and Borel–Cantelli give almost-sure convergence to zero.

Also the difference between the time averages of g(Z_{t+h}) and g(Z_t) has absolute value at most 2h||g||/T. Hence, along T=n^2,

    integral (P_hg-g) dnu_T -> 0,
    nu_T = T^{-1} integral_0^T delta_{Z_t} dt.

Use a countable dense subset of C(S×S) and positive rational h. There is one event of probability one on which every identity holds. Choose a path on its intersection with the positive-probability event of perpetual membership in K. Compactness supplies a weakly convergent subsequence of nu_{n^2}. The limit nu is supported on K. Feller continuity passes the identities to the limit; density extends them to every continuous g; strong continuity extends rational h to all h. Thus nu is invariant. Its marginals are invariant for the marginal semigroup and hence equal m. □

For a bounded connected C2 domain and a Feller Markov coupling, choose S=closure D and K={(x,y):|x-y|>=epsilon}. The unique invariant marginal is normalized volume. This gives an exact reduction to a stationary separated joining. It does not apply without the Feller/Markov assumptions and does not say the joining is supported on a function graph.

**Proposition 5 (finite-state warning).** In the class of finite-state continuous-time Markov chains, the analogue of the existential implication is false.

Take three states and the symmetric generator

    Q = [ -3   1   2
           1  -4   3
           2   3  -5 ].

For an ordered pair (i,j) with i!=j and the remaining state k, define transitions

    (i,j) -> (j,i) at rate q_ij,
    (i,j) -> (k,j) at rate q_ik,
    (i,j) -> (i,k) at rate q_jk.

Every coordinate has generator Q, while the two coordinates never coincide. This is a Markov, co-adapted avoidance coupling with distinct deterministic starting states.

Suppose a deterministic function f gave another coupling Y_t=f(X_t) with these same marginal chains. Both marginal laws converge to the uniform distribution. Therefore f must push uniform measure to uniform measure and hence be a permutation. Invertibility makes the transition behavior of f(X) the conjugate of Q, so f must commute with Q. Its three diagonal entries are distinct; therefore the only such permutation is the identity. That coupling cannot be shy in the discrete metric. This proves the claim.

The exact checker verifies the six-state joint generator, both marginal generators, invariant weights, and all six possible permutations. It does not convert this example to a Euclidean domain. The example shows why taking an extreme joining or selecting a deterministic partner from its support needs a specifically Euclidean diffusion argument; a general Markov-chain purification theorem would be false.

## 5. Measurable maps: an energy reduction, with a declared stopping point

**Proposition 6.** Let D be a bounded connected C2 domain with normalized volume m, and let P_t be its normal-reflection semigroup. Suppose f:closure D -> closure D is Borel and Y_t=f(X_t) almost surely at every time, where X,Y have reflected-Brownian marginal laws. Then f_*m=m. For every bounded h in H1(D),

    h composed with f belongs to H1(D),
    E(h composed with f,h composed with f)=E(h,h),

where E(u,u)=(1/2) integral_D |gradient u|^2 dm.

**Proof.** The marginal law of a bounded regular reflected Brownian motion converges in total variation to m. Pushing the law of X_s forward by the Borel map f is a contraction in total variation, so comparison with the law of Y_s shows f_*m=m.

For bounded Borel h, the two-time identity Y=f(X) gives

    E[h(f(X_{s+t})) h(f(X_s))]
      = E[h(Y_{s+t}) h(Y_s)].

Let s tend to infinity. On the left use the Markov property of X in its own filtration; on the right use that of Y. Total-variation convergence permits bounded measurable integrands. The result is

    <h composed with f, P_t(h composed with f)>_m
      = <h,P_t h>_m.

Their L2 norms are also equal. Divide the difference between squared norm and the displayed inner product by t, then let t decrease to zero. The standard quadratic-form characterization of the Neumann semigroup gives membership in H1 and the stated equality. □

In particular each coordinate of f is in H1 and

    integral_D gradient f_i · gradient f_j dm = delta_ij.

These are integrated identities. They are not, by themselves, pointwise orthogonality of Df, continuity, injectivity, or a deterministic partner extracted from an arbitrary joining. Upgrading this route would require justified local carré-du-champ/regularity arguments and handling possible noninvertibility. No such upgrade is claimed here.

Order-isomorphism results relating heat diffusion to geometry are relevant but cannot simply be invoked: the required bijectivity/intertwining hypotheses have not been established from the source premise. The inspected Arendt–Biegert–ter Elst abstract concerns Dirichlet-type heat semigroups on manifolds; it is not a ready-made theorem for this Neumann, potentially noninvertible setting. [Primary abstract](https://arxiv.org/abs/0806.0437).

## 6. Why graph thickening and non-rigid examples do not finish the target

The graph example cited by the source suggests replacing edges by thin tubes. Such a construction would have to establish all of the following for one positive tube width: exact normally reflected Brownian marginal laws, correct junction behavior, a strictly positive probability of infinite-horizon uniform separation, and impossibility of every admissible deterministic-function shy coupling in that same domain. A graph limit alone establishes none of the last two claims.

The infinite-horizon inference has a concrete elementary obstruction. Let T_n be a geometric killing time with per-step killing probability 1/n, n>=2. For each fixed integer T,

    P(T_n>T)=(1-1/n)^T -> 1,

but P(T_n=infinity)=0 for every finite n. Thus arbitrarily good fixed-window survival cannot be substituted for permanent survival at a fixed tube width. Likewise breaking visible geometric symmetries is not a proof against every Borel f.

There is a separate useful correction to a displayed example in the electronic reprint arXiv:1007.3199v4, page 40, Section 5.3. As printed, the annulus-product construction uses the same interval process in both coordinates. That displayed pair is related by the rigid map diag(-1,-1,1), so it does not prove the asserted stronger non-rigidity claim. The PDF page was visually inspected; the observation is not based only on text extraction. This is a local issue with that example, not a challenge to the paper's nonexistence theorems or its existential conjecture.

An elementary repair is as follows. Let U be reflected Brownian motion in the annulus a<|u|<b, and let V and W be independent reflected Brownian motions in (0,1), independent of U. On D=(annulus)×(0,1), put

    X=(U,V), Y=(-U,W).

Product Neumann semigroups give normally reflected Brownian marginals in this bounded connected product domain. Start all components at deterministic interior points. The pair is co-adapted and Markov, and |X_t-Y_t|>=2a always. At a fixed positive time the conditional law of W_t given (U_t,V_t) is non-atomic, so Y_t cannot be a Borel function of X_t. In particular it is not a rigid-motion image. However the same domain admits the rigid shy pair (U,V),(-U,V). Therefore the repaired example refutes only the stronger assertion about every coupling; it supports no negative answer to Problem 7.

## 7. Covariance control and the reflection obstruction

For a co-adapted coupling in a regular domain, use the convention

    dX=dB+n(X)dL^X,
    dY=J dB+K dC+n(Y)dL^Y,
    JJ^T+KK^T=I,

with predictable matrices and independent Brownian motions B,C. Put Z=X-Y and

    Sigma=(I-J)(I-J)^T+KK^T=2I-J-J^T.

Ito's formula gives

    d|Z|^2 = 2 Z·((I-J)dB-KdC) + tr(Sigma)dt
              +2 Z·n(X)dL^X -2 Z·n(Y)dL^Y.

**Proposition 7.** On a stochastic interval during which both particles remain interior, if |X-Y| is constant, their Brownian increments are synchronous there: J=I and K=0 almost everywhere in time, almost surely.

**Proof.** There is no reflection term on that interval. A constant |Z|^2 makes the local-martingale-plus-finite-variation decomposition above identically zero. Thus integral tr(Sigma)dt=0. Sigma is a sum of positive-semidefinite matrices, so I-J=0 and K=0 almost everywhere. □

This is a fixed-distance statement, much stronger than a positive lower bound. Radial noise cancellation does not imply synchronous noise: in dimension two, J=diag(1,-1), K=0 and Z=(r,0) give Z^T Sigma Z=0 but Sigma=diag(0,4), with positive drift of |Z|^2. The checker verifies this identity exactly. For ordinary normal reflection in the stated C2 setting, boundary-time sets have zero Lebesgue measure almost surely, while the local-time measures are supported on those sets. Thus the normal-local-time terms are singular with respect to dt and cannot cancel an absolutely continuous covariance drift in an identically constant-distance identity.

**Audit corollary to Proposition 7.** The same synchronous-increments conclusion holds across boundary visits whenever the distance is almost surely constant throughout a fixed interval, or throughout an interval between stopping times where the stopped semimartingale statement is valid. Indeed, uniqueness of the continuous local-martingale/finite-variation decomposition first makes the martingale part vanish. The remaining finite-variation identity has absolutely continuous part tr(Sigma)dt and a singular part carried by the boundary-time sets. Uniqueness of the Lebesgue decomposition forces tr(Sigma)=0 almost everywhere, hence J=I and K=0 there. The boundary-time assertion follows from the absence of boundary mass at each positive time and Tonelli. This is a correction and corollary within the fifth existing approach, not a sixth approach.

For a varying distance, reflection terms can affect cumulative distance balances, and their signs depend on geometry. A positive lower bound on distance does not supply the constant-distance hypothesis. No Lyapunov function or invariant-support theorem establishing the desired symmetry in arbitrary nonconvex domains has been obtained. Conditioning on never approaching must not be used to change marginal Brownian laws without proof.

## 8. Exact remaining problem

The five routes above leave the central implication untouched in its full scope. A complete positive solution would need to obtain a function coupling from an arbitrary shy reflected-Brownian coupling, with source-compatible hypotheses; a negative solution would need one bounded connected Euclidean domain with shyness and a proof excluding every admissible f. Neither has been supplied.

The useful retained statements are the smooth-map classification, the centroid obstruction in that class, the compact-Feller invariant-joining reduction, the finite-state obstruction to general purification, the Borel-map energy identities, and the interior constant-distance covariance lemma. All have explicit narrower hypotheses. Their elementary exact checks supplement, and do not replace, the mathematical proofs.

## 9. Reproducibility and inspection limits

`SOURCE_METADATA.json` records public source identifiers, versions, retrieval observations, byte counts and hashes; it contains no source bodies. `CERTIFICATE.json` is newly authored finite algebra. `verify.py` checks that certificate and does not prove the Euclidean target, assess novelty, or fetch sources. `replay_controls.py` exercises valid and invalid certificate inputs under normal, optimized, and doubly optimized Python, with genuine non-root execution and failed writes to a read-only packet. The external manifest pin is kept separately from the packet.

The author problem page, primary abstracts, selected theorem statements, definitions, relevant arguments and the displayed example were inspected. Entire literature proofs were not reverified. Search-engine publication/crawl timestamps were not treated as dates of new mathematical results. The retrieved 2005 files of *Shy couplings* were not relabeled as the final 2007 article. The 2012 rubber-band preprint was not relabeled as byte-identical to its 2014 publication. No evidence of a complete current solution was found in this bounded search.
