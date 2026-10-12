# Independent adversarial geometry verdict

**Verdict: PASS for the stated smooth-manifold construction. No blocking
mathematical defect was found in this review family.** The exact Gramian,
smooth curvature, completeness, local observability, and global two-sheet
ambiguity follow under the assumptions stated below. This is an independent
automated mathematical review, not human peer review or a historical novelty
determination.

Item: PR85, problem 30001203 / OWR-3394-020, parent-specified immutable head
`7271f51995532791220ac8e6b738a578d5d59143`; intake label `claimed_solved 1/5`.
Central proof-search turns: **0**. This review does not modify that intake label.
The prior submitted review was not read. No external individual was contacted;
no Git/index mutation, PR action, publishing action, or tracker edit was taken.

## Strongest independently verified result

Let `S` be the smooth genus-two hyperbolic surface constructed in `PROOF.md`,
let `pi:M->S` be the connected unramified double cover, and let
`e:(S,g)->R^17` be the smooth isometric embedding supplied by the original Nash
compact theorem. For `f=0` and `h=e circ pi`, every fixed interval `T>0` has

\[
P_T=T\pi^*g,\qquad K(P_T)=-1/T.
\]

The state manifold `M` is compact, connected, smooth, oriented and of genus
three. The metric is complete, and `f` has a global smooth flow for all real
times. The observation is a smooth rank-two immersion and is locally injective.
Every **attained** output history has exactly two distinct initial states.
Consequently the asserted global injectivity implication fails if compact
multiply connected state manifolds and this finite output dimension are allowed.

## Step-by-step adversarial checks

| Step challenged | Evidence and falsification attempt | Result |
|---|---|---|
| Hyperbolic genus-two surface exists | Explicit disk vertex radius `2^(-1/4)`; angle exactly `pi/4`, checked independently through geodesic-circle tangents | Pass |
| Gluing creates no cone corner | Opposite-side boundary reversal yields one eight-corner link; total angle `2pi`; vertex holonomy fixes point and tangent frame | Pass |
| Quotient is a smooth closed oriented surface | Interior disks, edge disks and vertex disk cover quotient; `V-E+F=-2` | Pass |
| Two-cover is connected and unramified | Surface relation maps trivially to `Z/2`; image contains its generator; pinned Hatcher theorem matches all local hypotheses; transitive monodromy | Pass |
| Cover is a legitimate compact smooth manifold | Lifted charts give local diffeomorphism; separation/countability and finite-sheet compactness checked directly | Pass |
| Cover genus is three | Lift a triangulation; `chi(M)=2chi(S)=-4` | Pass |
| Nash supplies smooth embedding, not only `C^1` | Original Theorem 2 permits `k=infinity`; compact positive metric and dimension 17 directly checked | Pass |
| Exact observability metric | Constant flow and identity variational derivative yield the actual history integral `T dh^*dh=T pi^*g` | Pass |
| Uniform bounds | Compact unit tangent bundle gives positive finite comparison to any fixed background metric; chosen finite disk atlas gives `4T I<=P_T<=(64T/9)I` | Pass with explicit meaning |
| Curvature and scaling | Local isometry; independent conformal calculation and exact polynomial identity yield `-1/T` | Pass |
| Both completeness requirements | Zero field flow is identity for all real times; geodesic flow cannot escape compact speed bundle in finite time | Pass |
| Rank and local injectivity | Restrict to a single evenly covered disk sheet and use the embedding `e` | Pass |
| Global history fibers | Injectivity of `e` makes `h` fibers exactly the two-point `pi` fibers; all trajectories constant | Pass |
| Possible low-dimensional obstruction | The observation has ambient dimension 17 as supplied by the smooth theorem, so a three-dimensional immersion obstruction cannot invalidate it | Pass |

The independent standard-library checker passes. Its checks concern exact
elementary algebra, topology of the explicit gluing, monodromy data and chart
constants. They are not a numerical construction of the smooth Nash embedding.

## Exact assumptions and nonblocking clarifications

1. **Uniformity is relative to a fixed comparison structure.** Both a fixed
   smooth background metric and one chosen finite atlas are verified. No metric
   has coordinate-matrix eigenvalue bounds invariant under arbitrary chart
   rescalings. The original source states local coordinates but leaves the
   reference for uniform bounds implicit. If another formulation requires one
   global Euclidean coordinate domain or simple connectivity, this particular
   compact example does not meet that added hypothesis. This is a scope
   qualification, not an unresolved geometric step.
2. **Fix `T>0`.** Curvature `-1/T` is uniformly negative over states for each
   fixed positive interval. Constants need not remain uniform as `T` ranges
   over `(0,infinity)`. The zero-length limit is excluded in the source.
3. **Use a valid octagon pairing.** The submission mentions paired sides without
   spelling out the combinatorics. The explicit opposite-side pairing above
   realizes its claimed surface and validates the existence step. Adding that
   pairing would make the submitted proof more immediately checkable.
4. **Say 'every attained history'.** A history generated by this system has
   exactly two preimages. A function of time outside the image of the history
   map has no preimages. The submitted statement's intended meaning is clear,
   but 'attained' prevents a literal reading over arbitrary output functions.
5. **Classical imports remain imports.** Nash's smooth compact theorem and
   Hatcher's covering realization were accessed directly with matching
   hypotheses. This review does not reproduce Nash's full iteration. Its use
   is not circular and does not transfer the central observability question to
   an unsupported equivalent assertion.

No primary-source access gap remains for those imports. There is no remaining
gap in the assigned geometric verification. A separate source-scope review and
any novelty audit are outside this family's conclusion.

## Reproduction and artifacts

- Independent proof: `PROOF.md`.
- Original theorem locators, hashes and access record: `SOURCE_PINS.md`.
- Exact checker: `checks/check_geometry.py`.
- Recorded successful output: `checks/check_geometry_result.json`.
- Research checkpoints: `RESEARCH_LOG.md`.

Reproduce the elementary checks from this folder:

```sh
python3 checks/check_geometry.py
```

All audit artifacts are within this dedicated review directory. No submitted
artifact was edited. Best-guess completion: **100% of the assigned geometric
review**, with scope and novelty tasks expressly excluded from this percentage.

