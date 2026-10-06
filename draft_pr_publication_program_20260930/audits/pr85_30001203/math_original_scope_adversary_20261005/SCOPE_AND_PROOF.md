# Independent original-scope adversarial audit of PR 85

Target: problem 30001203 / OWR-3394-020; claimed submitted head `7271f51995532791220ac8e6b738a578d5d59143`. Audit family: original publication scope, intrinsic observability metric, global state ambiguity. Central proof-search turns: 0. No submitted prior review was read before this report.

**Verdict: the submitted covering/Nash construction refutes the original printed manifold conjecture. No hidden source hypothesis excluding the example was found.** The report leaves one interpretive caveat explicit: uniform matrix bounds require a choice of state-coordinate normalization or background metric; the source does not prescribe one. The compact example has both arbitrary-fixed-background and finite-normalized-atlas uniform bounds. A demand for bounds in every possible coordinate system is impossible for every positive Riemannian metric and is not a coherent alternative reading of the source.

This verdict addresses the mathematical/source-scope claim. Authentication of the dataset pair and immutable Git head belongs to the parent audit. The parent reports completed source-pair authentication in `../original_source_authentication_20261005/SOURCEPAIR_AUTHENTICATION_V2.json`; this family has not independently reauthenticated that record. No priority, novelty, historical-status, or publication-readiness claim follows from this audit.

## Primary-source scope

The full Krener contribution was read on printed pp. 674–675 of [OWR 11/2009](https://ems.press/content/serial-article-files/46211), DOI `10.4171/OWR/2009/11`. Its hypotheses and target are:

| Feature | Published formulation | Consequence for this audit |
|---|---|---|
| State | Local coordinates on an n-dimensional manifold | No global Euclidean chart or simple connectivity is stated. |
| Output | Euclidean space of dimension p | No upper bound on p or relation p<n is stated. |
| Dynamics | Autonomous observed system | No exclusion of f=0 is stated. |
| Observation period | Some fixed T>0 | The history definition uses 0<=t<T, despite interval notation [0,T]. |
| Global target | Injectivity of the initial-state-to-output-history map | Distinct covering sheets remain distinct states. |
| Gramian | Exact variational integral along each initial-state trajectory | An arbitrary unrelated metric would not suffice. |
| Bounds | Positive definiteness and boundedness, uniform over initial states | A normalized basis/background is implicit but unspecified. |
| Geometry | Uniformly negative curvature; geodesic completeness | No further topology or extrinsic embedding condition is present. |
| Scaling | Conditional observation-noise normalization | The noise-free example has no additional covariance assumption to satisfy. |

[Krener–Ide, *Measures of Unobservability* (2009)](https://calhoun.nps.edu/server/api/core/bitstreams/fe670a91-21d7-4ff0-a25e-01be2e5d4164/content), Section I, was independently read in full. It uses the same history injectivity definitions and exact local Gramian. It discusses local singular values and warns that their numerical values depend on state and output scaling. It explicitly permits parameters to be treated as extra states having zero time derivative. Its later convention of calling an empirical finite-difference Gramian the local Gramian does not alter the exact integral printed in the OWR question. Its Euclidean calculations and vortex application do not impose a global Euclidean state space on the separate manifold conjecture. The entire institutional PDF was downloaded and inspected as the primary paper; its example sections do not impose hidden hypotheses on the OWR question.

## Independent intrinsic derivation

Let F_t be the flow and define the observation-history map

    O_T(x)(t) = h(F_t(x)),   0 <= t < T,

with values in L^2([0,T];R^p). In the smooth finite-time situation under consideration,

    (dO_T)_x(v)(t) = dh_{F_t(x)} (dF_t)_x(v).

Thus the source Gramian, intrinsically, is

    P_T(x)(v,w) = integral_0^T <dh_{F_t(x)} dF_t(v),
                                      dh_{F_t(x)} dF_t(w)> dt.

This is precisely O_T^* of the L^2 inner product, as a covariant two-tensor on the state manifold. In coordinates, dF_t is the fundamental matrix Phi(t) and dh is H(t), giving the source's integral Phi^T H^T H Phi. For a change of initial-state coordinates with Jacobian J=dx/dz, the matrix transforms as

    P_z = J^T P_x J.

The identity follows directly from the tensor formula; it is not an assumption that matrix eigenvalues remain invariant under changes of state coordinates. Curvature and geodesic completeness are properties of this tensor, hence coordinate invariant.

For f=0, F_t is the identity for every real t and its differential is the identity. Hence, for every fixed T>0,

    P_T = T h^*<.,.>.

Local observability and global observability are different requirements: a positive-definite P_T makes dO_T injective, but does not rule out two separated points having the same O_T. The submitted example realizes exactly that possibility.

## Independent verification of the construction

1. Let S be the smooth closed oriented genus-two surface obtained by the usual commutator-word side gluing of a regular hyperbolic octagon with interior angles pi/4. Such a polygon exists: its interior angle varies continuously from the Euclidean octagon angle 3pi/4 for small radius to zero as the vertices approach the ideal boundary. More concretely the circumradius R satisfying cosh(R)=(cot(pi/8))^2 gives that angle. All eight vertices become one vertex. The four paired edges yield smooth hyperbolic charts by gluing two half-disks isometrically, and the eight vertex sectors have total angle 2pi, yielding a smooth hyperbolic disk, with no cone point. The resulting compact surface has V-E+F=1-4+1=-2 and an oriented smooth metric g of curvature -1.

2. The presentation pi_1(S)=<a1,b1,a2,b2 | [a1,b1][a2,b2]=1> maps surjectively to Z/2 by sending a1 to 1 and the other generators to 0. Every commutator maps to zero, so the relation is respected. Its kernel has index two. The covering-space existence theorem supplies a connected two-sheeted cover pi:M->S. A smooth structure on M is obtained by lifting each smooth chart of S through evenly covered neighborhoods; overlap maps are exactly smooth overlap maps on S, so pi is a smooth local diffeomorphism.

3. The cover is compact. For completeness of this usually implicit point, cover the compact base by finitely many relatively compact neighborhoods whose closures lie in evenly covered neighborhoods. Each closure has exactly two compact lifted copies. Their finite union covers M. Pull back g to gtilde=pi^*g. Each lifted chart makes pi a local isometry, so gtilde has curvature -1. The smooth compact metric is geodesically complete: a unit-speed geodesic remains in the compact unit tangent bundle, and its smooth geodesic vector field therefore has a complete flow. This avoids needing to infer geodesic completeness from a numerical calculation.

4. Nash's original compact smooth isometric embedding theorem supplies e:(S,g)->R^17, with e smooth and injective and e^*<.,.>=g. The theorem was visually checked in the original 1956 paper, Theorem 2, printed p. 59 (PDF page 41 of the pinned copy): it applies to C^k positive metrics and gives C^k isometric embeddings for 3<=k<=infinity in n(3n+11)/2 dimensions. For n=2 this number is 17; smooth g meets its hypotheses. The use of an embedding, as distinct from a C^1 immersion, is justified by that theorem. No low-codimension negative-curvature embedding theorem is being assumed.

5. Put f=0 and h=e o pi. The intrinsic calculation yields

    P_T = T (e o pi)^*<.,.> = T pi^*(e^*<.,.>) = T gtilde.

At T=1 this is exactly gtilde, not a separately imposed state metric. Therefore its sectional curvature is identically -1, which is uniformly negative, and it is geodesically complete. Its smoothness and definiteness follow from the smooth local isometry pi and smooth embedding e.

6. Since pi is a local diffeomorphism and e is injective, h is injective on sufficiently small neighborhoods of each point. Constant trajectories identify output histories with h(x), so the system is locally observable on every positive-length interval. For every s in S, its two lifts x1!=x2 obey h(x1)=e(s)=h(x2). Their histories agree for all real times. Conversely h(x1)=h(x2) implies pi(x1)=pi(x2), because e is injective. Thus each attained output history has exactly two distinct initial states. The failure of global observability is a genuine manifold-point ambiguity and cannot disappear through a coordinate reparametrization.

7. The source requires a fixed T, so T=1 suffices. For any other fixed T>0 the same example has P_T=T gtilde. A constant metric scaling leaves the Levi-Civita connection unchanged and divides sectional curvature by T, giving -1/T; geodesic completeness and the two-state ambiguity persist. Uniformity over T approaching zero or infinity is not a stated requirement.

The covering dependencies were independently checked in [Hatcher's author-hosted Chapter 1](https://pi.math.cornell.edu/~hatcher/AT/ATch1.pdf): surface-group presentation on printed p. 51, Proposition 1.32 on p. 61 (sheets equal index), and Proposition 1.36 on pp. 66–67 (realization of subgroups). The lifting proof there applies because a connected smooth surface is path connected, locally path connected, and semilocally simply connected. The octagon and completeness arguments above supply direct checkable geometric reasons for the remaining elementary dependencies.

## Uniform bounds and the exact interpretive boundary

Let q be any independently fixed smooth background Riemannian metric on the compact M. The q-unit tangent sphere bundle is compact. The function (x,v)->gtilde_x(v,v) is continuous and strictly positive on it. It therefore attains a minimum c>0 and maximum C<infinity. By homogeneity,

    c q <= P_1 = gtilde <= C q   on all of M.

This proof works for every fixed smooth q, not solely the choice q=P_1.

There is also a fixed-atlas interpretation matching the source's local-coordinate language. At every point choose an isometric chart to a sufficiently small centered disk in the Poincare disk model, restricted to radius at most 1/2. Compactness gives a finite subcover. In every such chart, writing r^2=u^2+v^2,

    P_1 = 4/(1-r^2)^2 I_2,
    4 I_2 <= P_1 <= (64/9) I_2.

These are common numerical bounds across the fixed atlas. The restriction need not be an exactly radius-1/2 disk; smaller charts give the same inequalities. Smooth coordinate overlaps do not need to preserve eigenvalues, and no assertion that they do is used.

A quantifier over every possible state chart would make any positive metric fail the hypothesis: replace a coordinate x by z=a x at a given point, so J=a^-1 I and P_z=a^-2 P_x. Arbitrarily large/small a destroy any common positive lower or finite upper bound. A condition restricted to one global Euclidean chart would be an additional hypothesis absent from the original published formulation and would exclude the submitted compact state manifold by assumption. Such a strengthened question is not settled by this compact example. The audit does not infer that the source's author intended an unstated strengthening.

## Adversarial checklist and remaining gaps

| Attempted falsifier | Result |
|---|---|
| State manifold silently widened from original Euclidean domain | Falsifier fails: original explicitly uses local coordinates on a manifold. |
| Simply connectedness or unique geodesics silently omitted | No such hypothesis appears in the complete contribution. |
| f=0 outside observed-system definition | No exclusion appears; all flows/variational dynamics exist globally. |
| Output dimension too large | Original p is unrestricted; Nash dimension 17 is legitimate. |
| Wrong Gramian or unrelated negative metric | Exact intrinsic calculation gives P_T=T pi^*g. |
| Coordinate transformations invalidate curvature | Tensor transformation law verifies coordinate invariance. |
| Uniform bounds asserted for arbitrary chart rescaling | Submission explicitly uses fixed background/fixed atlas; those bounds are valid. |
| Nonlocal duplicate outputs are mere coordinate duplicates | They are distinct covering points; equality of histories is exact. |
| Completeness confused with compactness of image | Completeness is established on compact state M with its actual Gramian metric. |
| Nash theorem only C^1, or requires positive sectional curvature | Original smooth compact theorem uses a positive-definite metric, not positive curvature. |
| Endpoint convention [0,T) changes conclusion | Histories agree for all t, so either endpoint convention fails injectivity. |
| Extra hypothesis hidden in Krener–Ide | No condition in its relevant Section I excludes this example. |

Strongest verified result: a smooth, complete, compact, locally observable system satisfying the original printed geometric hypotheses and normalized uniform bounds has exactly two indistinguishable initial states for every attained output history.

Exact remaining gaps within this family: none in the mathematical counterexample under the coherent manifold meaning of uniform bounds. The source's unprescribed coordinate normalization is a stated semantic limitation, not a constructed failure of a hypothesis. External audit limits: the parent reports source-pair authentication complete, but this family has not independently checked that authentication, frozen-head identity, or author-file status assertions; novelty and priority remain unassessed. There was no need for outside input or communication.
