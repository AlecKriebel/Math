# Checkpoint 1 — Field Selection and Novelty Boundary

**Status:** conditional pass after two adversarial reviews (7/14).

## 1. Proposed field

**Noncommutative comparative statics (NCS)** is the proposed study of
order-sensitive response in constrained systems.

Classical comparative statics associates an equilibrium or optimum with each
external parameter value and asks how the endpoint changes. NCS instead treats
an adjustment protocol as part of the model. It asks whether responses to
externally compatible interventions commute, how local failures of commutation
accumulate, and when they leave persistent memory.

The motivating pattern recurs in:

- engineering systems that preserve feasibility by redistributing load;
- optimization models whose active constraints change;
- software or database repair that minimizes edits already made;
- economic and biological systems with adjustment costs;
- sequential algorithmic recourse and model editing.

The claim is not that these domains lack mathematics. The claim to test is
that they lack a shared mathematical object centered on the compositional
defect of a response protocol, especially when responses are noninvertible or
cross singular active-set strata.

## 2. Basic object: a directed response complex

A preliminary deterministic response complex consists of:

1. a directed cubical or cellular parameter complex \(K\);
2. a feasible-state space \(X_b\) over each vertex \(b\);
3. a selected response map
   \(T_e:X_{s(e)}\rightharpoonup X_{t(e)}\) on each intervention edge;
4. a metric or divergence \(d_b\) on each target fiber;
5. a declared class of admissible paths and states.

For a directed square \(\sigma\) with the two boundary paths \(p\) and \(q\)
from the same source to the same target, define the pointwise order defect

\[
  \Delta_\sigma(x)=d_{t(\sigma)}(T_p x,T_q x).
\]

This definition does not require response maps to be invertible. If the maps
are set-valued, the first extension will use directed Hausdorff excess or a
coupled optimal-transport discrepancy rather than choosing a hidden
tie-breaker.

A fiberwise isometry \(\phi_b:X_b\to X'_b\) acts by

\[
  T'_e=\phi_{t(e)}T_e\phi_{s(e)}^{-1}.
\]

The scalar defect is invariant under this gauge change. Non-isometric changes
of units must transform the cost/divergence as part of the model.

## 3. What is intended to be new

The field-level novelty target is the combination of:

- a response complex that permits directed and noninvertible adjustment;
- local order defects attached to commuting external intervention cells;
- quantitative local-to-global bounds for accumulated order-debt;
- a smooth-limit theorem recovering ordinary connection curvature;
- a stratified extension in which active-set seam and junction defects coexist
  with smooth curvature;
- explicit separation of **reset response** (re-optimize from a fixed
  reference) from **carry response** (minimize change from the current state).

The smooth metric-minimal lift by itself is standard and is not counted as a
new object.

## 4. Foundational theorem targets

### T1. Gauge invariance

Prove that square defects and path-comparison inequalities are invariant under
fiberwise isometries, and state the correct covariance under general changes
of units.

### T2. Quantitative local-to-global order-debt

If edge responses are nonexpansive and every elementary commuting square has
uniform defect at most \(\varepsilon_\sigma\), then transports along two paths
related by square swaps differ by at most the sum of the defects encountered.
For \(L\)-Lipschitz maps, downstream amplification factors enter explicitly.
The bound should be sharp on a constructed family.

### T3. Smooth-limit reduction

For a smooth feasible bundle with incremental quadratic adjustment cost,
show that the normalized square defect converges to the norm of the ordinary
Ehresmann curvature:

\[
  \Delta_{\square_\epsilon}(x)
    = \epsilon^2\|\Omega_x(u,v)\|+O(\epsilon^3).
\]

This is a reduction/consistency theorem, not a novelty theorem.

### T4. Reset/carry separation

Prove that a unique strongly regular reset section has zero order defect,
whereas carry response may have nonzero defect on the same feasible family.
This prevents the two semantics from being conflated.

### T5. Stratified response decomposition

For a finite active-set stratification with smooth cellwise transports and
specified seam maps, decompose path discrepancy into cell-curvature,
seam-mismatch, and codimension-two junction contributions. State conditions
under which vanishing of all three gives path independence.

## 5. Prior-art collision table

| Existing field | What it already supplies | Boundary of the NCS claim |
|---|---|---|
| Parametric optimization / comparative statics | solution-map derivatives, KKT sensitivity, active-set regularity | NCS adds an explicit sequential response protocol and compares equivalent intervention orders |
| Ehresmann connections / Riemannian submersions | horizontal lift, curvature, holonomy | exactly the smooth invertible sector; not claimed new |
| Redundant robotics | weighted-pseudoinverse lift, repeatability, closed-loop drift | a principal prior instance and validation case |
| Geometric mechanics | geometric phase from cyclic control/shape change | smooth reversible sector only |
| Moreau sweeping / rate-independent systems | moving constraints, projections, jumps, dissipation, hysteresis | NCS focuses on compositional defects between intervention orders and cross-domain discrete/smooth comparison |
| Quantitative/metric rewriting | local diamonds, quantitative Church–Rosser/Newman theory, nonexpansive and graded context amplification | the elementary swap bound is prior-art-compatible; NCS must add response rectification and cross-sector scaling |
| Higher-dimensional automata / trace theory | precubical independence cells and path equivalence by adjacent swaps | supplies the intervention substrate; not claimed new |
| Path-category and quiver representations / Ulam stability | functors on paths, quotients by relations, approximate representations and rectification | the closest categorical formulation and the main novelty benchmark |
| Lattice/discrete gauge theory | edge transport, plaquette defect, gauge covariance, continuum curvature limits | exactly the invertible discrete sector; not claimed new |
| Scattering diagrams / wall crossing | wall maps, path-ordered products, joints, consistency | a major comparator for seam and junction response |
| Exit-path categories / hybrid systems | constructible transport, guards, resets, saltation, and stratified paths | seam maps require protocol data; the stratification alone is insufficient |
| Cyclic projections / operator products | noninvertible projection maps, order, and convergence | projection examples are baselines, not novelty evidence |
| Online optimization / convex-body chasing | movement cost under changing feasible sets | optimizes a time sequence; NCS compares alternative orders representing the same external endpoint |
| Algorithmic recourse | minimal actionable interventions, including sequential variants | an application community; NCS studies algebra/geometry of composing recourse responses |
| Hybrid systems / nonsmooth mechanics | guards, resets, saltation, event-driven flow | supplies seam dynamics; NCS seeks an invariant order-defect decomposition |

## 6. Falsification gates

The proposed field is a no-go if any of the following remains true after the
foundational paper:

1. all definitions translate without residue into an ordinary connection,
   solution map, sweeping process, or confluence theorem;
2. no theorem survives noninvertible response maps;
3. defect rankings can be changed arbitrarily by coordinate rescaling;
4. the local theory cannot predict held-out order effects;
5. active-set examples are merely numerical discretization artifacts;
6. no two natural applications outside a single established subfield use the
   same invariant.

## 7. Reviewer communities

The proposal is intentionally legible to researchers in:

- variational analysis and optimization;
- differential geometry and geometric mechanics;
- hybrid and nonsmooth dynamical systems;
- mathematical economics / comparative statics;
- theoretical computer science (rewriting, incremental computation, repair);
- algorithmic recourse and trustworthy machine learning.

Outside expert feedback would be valuable after the manuscript is mature, but
this project will not prepare or initiate outreach; only the human researcher
may communicate externally.

## 8. Checkpoint decision

Proceed only as a **conditional research program**, not yet as an established
new branch. Checkpoint 2 must use an exact presented-category formulation,
define partial-map domains and morphisms, demote the baseline lemmas, and prove
a source-conditioned rectification result plus an obstruction/counterexample.
