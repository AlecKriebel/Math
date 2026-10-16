# Independent source and analytic mechanism — pre-candidate seal

Written 2026-10-03 18:52 UTC. This document precedes reading candidate proof/code/history, prior PASS files, or other family analyses. Routing `SOURCE_MANIFEST.json` and `SOURCE_NORMALIZATION.md` were the only candidate files read. Fresh retrieval metadata is `retrieval.json`; lossless full PDF text streams and rendered visual pages are under ignored `private/`. Both pinned hashes and byte counts matched. All five Carleson pages and Hayman–Lingham PDF page 61, printed page 60, were visually read, not inferred from OCR. Carleson OCR is visibly corrupt and cannot establish exact signs/quantifiers.

## Exact source scope and priority

Hayman–Lingham Problem 3.2 concerns a nonconstant harmonic function on all Euclidean space in dimension at least three and a path escaping to infinity along which the values tend to positive infinity. Update 3.2 expressly records an affirmative result, credits Fuglede and earlier Talpur/Hayman work, states the continuous/harmonic path case affirmatively, and cites Carleson's polygonal theorem. Its historical sentence about a regularity question must be read together with those subsequent sentences. No novelty follows from a catalog entry.

Carleson 1976, pp.35–39, states the stronger theorem for subharmonic functions whose supremum is positive infinity. Section 2 handles continuity; Sections 3–5 address the general case through smoothing, exceptional cubes, and potential estimates. This audit does not independently certify that discontinuous extension. The target is the finite, entire, real-valued harmonic case. Carleson's printed thinness criterion on p.35 appears with the word “thin”; I will not rely on that criterion or its asserted inheritance in this elementary audit. The affirmative theorem and its continuous-case argument are visibly present. This is a source-priority finding, independent of the candidate proof's correctness.

The bounded subharmonic example in Hayman–Lingham is the continuous function equal to −1 in the unit ball and to −|x|^(2−n) outside, including value −1 at the origin. It is nonconstant, bounded above by zero, and outside Carleson's unbounded-above hypothesis. It invalidates an unrestricted nonconstant-subharmonic version, not the harmonic statement.

## Independently developed mechanism

The following argument arose before opening the candidate proof. It uses ordinary ball Poisson comparison and elementary topology; it requires no fine potential theory.

1. **One-sided harmonic Liouville, including a zero center.** If entire harmonic u is bounded above by M, h=M−u is nonnegative harmonic. On a radius-R sphere centered at 0 the normalized Poisson kernel at fixed z is

   K_R(z,ζ)=R^(n−2)(R²−|z|²)/|Rζ−z|^n,

   with ζ on the unit sphere and normalized surface probability. With t=|z|/R its bounds are (1−t)/(1+t)^(n−1) and (1+t)/(1−t)^(n−1). Both tend to one. The mean-value identity gives sphere average h=h(0), so these bounds squeeze h(z) to h(0) as R tends to infinity. If h(0)=0, nonnegativity and mean value already give h=0 on every sphere and everywhere; no division by h(0) is permitted. Thus a nonconstant entire harmonic u is unbounded above. Dimension one is affine and separate; the source asks n≥3, while this ball argument works n≥2.

2. **Bounded nonnegative entire subharmonic means.** For finite continuous subharmonic w with 0≤w≤S and S=sup w, ball comparison gives w(z)≤(sup K_R(z,·)) A_R(w), where A_R is the sphere average about 0. Consequently liminf A_R(w)≥w(z) for every fixed z. Taking sup over z yields A_R(w)→S. This does not say w is constant: the preceding source example, shifted by one, is a direct control against that false assertion. No monotonicity or rate is needed.

3. **Zero pasting with arbitrary component boundary.** Let C be a connected component of {u>a}; define w_C=u−a on C and zero elsewhere. At any point of ∂C, u=a: a boundary point with u>a would have a connected positive neighborhood belonging to C; continuity excludes u<a. Hence w_C is continuous. For a ball D, let H be harmonic on D with boundary values w_C. Then H≥0. On C∩D, compare the subharmonic u−a with H: on ∂C it is zero, and on ∂D the desired bound holds. The usual maximum principle on this bounded intersection, using continuous boundary limits, gives w_C≤H. Outside C, zero≤H. No smoothness, regularity of C, or harmonic measure for C is assumed. This proves subharmonicity of w_C by the ball comparison characterization.

4. **At most one bounded-value component.** If two distinct nonempty components C,D at level a have finite positive suprema S,T for their pasted functions, then w_C/S+w_D/T≤1 everywhere because their supports are disjoint. Step 2 makes the sphere averages of the two summands tend separately to one, contradicting their sum being at most one. Thus at most one such component can have bounded values. This is stronger than merely saying components are spatially unbounded.

5. **Nested choice without finite branching.** First choose a component C_1 of {u>1} where u is unbounded: if there is one component it carries all sufficiently large values; if there are at least two, Step 4 supplies an unbounded-value component. If u is unbounded on C_k, the components of {u>k+1} lying in C_k cover all points of C_k above k+1. With exactly one child it must carry unbounded values; with at least two children, Step 4 again gives an unbounded-value child. Every child is wholly in C_k since a connected set contained in {u>k} belongs to one component. This works for any infinite number of children; no maximum over infinitely many finite bounds is taken. Inductively select C_(k+1)⊂C_k.

6. **Whole-tail polygon and properness.** Pick x_k∈C_k. Both x_k and x_(k+1) lie in C_k. A connected open Euclidean set is polygonally connected: the points reachable by finite polygonal chains from one point form a nonempty relatively open and relatively closed subset. Connect these endpoints by a finite polygon inside C_k and parametrize it continuously on [k,k+1]. Every point of that stage has u>k. Therefore the entire tail has u→+∞. For each compact K, continuity makes sup_K u finite; every stage with k>sup_K u misses K. Only finitely many stages, each with finitely many pieces, can meet K. This proves local finiteness in space and properness, not merely escaping vertices. No injectivity, ray, monotonicity, rate, or total-length bound is claimed.

## Falsifiable gates for candidate review

The candidate must supply the exact normalized kernel, treat zero-center h, avoid bounded-subharmonic Liouville, justify component-boundary pasting without regularity, distinguish unbounded values from spatial unboundedness, handle infinite children, and control all stage points. Finite arithmetic/sampled geometries cannot certify the theorem by themselves. Credit and scope must remain explicit, and historical inaccessible-object/global negative claims cannot be certified from accessible local files alone.

At this pre-candidate checkpoint, primary-source mathematical classification is established; candidate proof correctness and implementation/reproduction are still unassessed. Best-guess mathematical-audit completion 25%; live/prepared packet audit 0%; novel theorem contribution 0 if the candidate merely reproduces the established target.
