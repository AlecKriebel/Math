# Movable invariant enlargements in three-dimensional flows

**Problem 30003527 · OWR-15575-006 · queue row 1767**  
**Disposition: UNSOLVED by this investigation.** Five new shared substantive passes were completed on 13 October 2026. That continuation's five-pass search is exhausted; the lifetime substantive count is unknown. Verification and correction of those written results do not add a sixth search pass.

This reader collects complete authored proofs and independent AI mathematical audits of restricted positive results and counterexamples to proposed construction lemmas. It does not claim a solution of the unrestricted question, research novelty, a comprehensive literature search, journal peer review, or formal proof-assistant verification.

## The exact question

Let φ: R × R³ → R³ be a continuous full flow, let A ⊂ R³ be compact and invariant under every real time, and let U be any open neighborhood of A. Must there be a compact invariant **movable** B satisfying

A ⊆ B ⊆ U?

Equality B=A is allowed. B need not be connected, a neighborhood of A, isolated, or minimal. No smoothness, nonsingularity, stability, aperiodicity, or dimension-one hypothesis is imposed. Every B is of course finite dimensional as a subset of R³.

Here movability means: for every open O ⊃ B there is an open V with B ⊂ V ⊂ O such that, for every open W ⊃ B, there is a continuous homotopy H: V × [0,1] → O with H(x,0)=x and H(V,1) ⊂ W. V is fixed before W is chosen. The homotopy need not follow the flow, preserve B, or fix B pointwise. The empty compactum is handled directly.

The earlier exact formulation is Krystyna Kuperberg's Question 14(1), printed p.390, with definitions on p.389, in J. E. Vaughan (ed.), [*Open Problems Collected from the Spring Topology and Dynamical Systems Conference 2006*](https://topology.nipissingu.ca/tp/reprints/v31/tp31132.pdf), Topology Proceedings 31 (2007), 379–401. The later catalogue source is Kuperberg's *Shape of minimal sets in aperiodic flows*, printed p.2019 of [Oberwolfach Reports 14 (2017), Dynamische Systeme](https://doi.org/10.4171/OWR/2017/32). The report was published in 2018; this is not the question's first appearance. The title's aperiodic-flow context does not restrict its separately stated final question.

## Main restricted affirmative result

**Theorem.** If K is an isolated invariant compactum of a continuous full flow on R³, has finitely many connected components, and has covering dimension at most one, then K is movable. No finite-rank assumption on its first Čech cohomology is required. For this class, B=K answers the enlargement question in every prescribed neighborhood.

Read the [corrected V2 proof](proofs/ONE_DIMENSIONAL_ISOLATED_MOVABILITY_V2.md) and [independent acceptance](audits/DIMENSION_ONE_ACCEPTANCE.md), together with the [ambient block refinement](proofs/AMBIENT_BLOCK_REFINEMENT.md) and its [acceptance](audits/AMBIENT_BLOCK_ACCEPTANCE.md). The proof supplies actual neighborhood homotopies:

1. Finite entry-surface disk/strip cuts produce arbitrarily small blocks with relative Ȟ⁰ and Ȟ¹ over F₂ equal to zero.
2. Surface-complement geometry and controlled collars give loop-surjective overlaps. Stopped backward flow, van Kampen, and a finite-time-safe forward push prove π₁-surjectivity from each target neighborhood into the block.
3. Covering dimension at most one supplies a fixed finite-graph factorization of a neighborhood inclusion. Lifting that finite graph into each target neighborhood produces the required movability homotopy.

The graph step is essential. A fundamental-group epimorphism alone is not used as a homotopy section of a three-manifold inclusion.

**Version warning:** the original proof contained a genuine error in its empty-entry paragraph and is not accepted as written. Only V2 is accepted. When the entry surface E is empty, N=N⁻ and D=N⁺=K; backward flow is the correct direction. The [correction record](CORRECTIONS.md) and [authored patch](corrections/EMPTY_ENTRY_CORRECTION.patch) identify the exact change. No theorem hypothesis was broadened.

## Other established results

| Result and exact scope | Complete proof | Independent audit |
|---|---|---|
| Isolated K is movable when Ȟ⁰(K;F₂) and Ȟ¹(K;F₂) are finite dimensional; coefficient bridge and explicit collar homotopies. This reconstructs a theorem already announced by Sánchez-Gabites. | [Finite-type proof](proofs/COEFFICIENT_BRIDGE.md) | [Structural acceptance](audits/STRUCTURAL_ACCEPTANCE.md) |
| Every isolated invariant K has free integral Ȟ¹, without a finite-rank assumption. | [Freeness proof](proofs/OBSTRUCTION_AUDIT.md) | [Structural acceptance](audits/STRUCTURAL_ACCEPTANCE.md) |
| Every isolated K has finitely many complementary components and finite-rank free Ȟ². A stationary planar Hawaiian earring realizes infinite-rank Ȟ¹ and is movable. Finite-component K admits the stated actual block refinement. | [Ambient proofs](proofs/AMBIENT_BLOCK_REFINEMENT.md) | [Ambient acceptance](audits/AMBIENT_BLOCK_ACCEPTANCE.md) |
| A dyadic solenoid plus Hausdorff-approaching incompatible-winding circles is nonmovable, although its integral Ȟ¹ is free and the displayed homology bonding maps are surjective. | [Geometry and nonmovability](proofs/SATELLITE_CIRCLE_AUDIT.md); [cohomology](proofs/SATELLITE_COHOMOLOGY.md) | [Satellite acceptance](audits/SATELLITE_ACCEPTANCE.md) |
| For isolated K and one fixed u∈H¹(O;Z), the winding magnitudes on its clopen circle components take only finitely many distinct values. The preceding satellites have magnitudes 3·2ⁿ and cannot be isolated for any continuous full flow. | [Finite-winding theorem](proofs/SATELLITE_ISOLATION_OBSTRUCTION.md) | [Isolation-obstruction acceptance](audits/ISOLATION_OBSTRUCTION_ACCEPTANCE.md) |
| Actual stable-entry quotients have finite-polyhedral shape, but an abstract movable collared trace plus finite-shape quotient and stable tails does not force movability. The abstract example is not an R³-flow realization. | [Collar and quotient proof](proofs/COLLARED_QUOTIENT_OBSTRUCTION.md); [direct folded-core supplement](proofs/DIRECT_CORE_SUPPLEMENT.md) | [Collared-quotient acceptance](audits/COLLARED_QUOTIENT_ACCEPTANCE.md) |

The finite-winding result rules out a **proposed isolated realization route**. An actual isolated flow realization was never established or claimed. It does not rule out simultaneous invariance with additional nearby invariant structure. The [forced-extra-structure note](proofs/FORCED_EXTRA_STRUCTURE.md) explains the exact contrapositive; its optional extension to cyclic-Ȟ¹ clopen connected compacta has not been separately certified by the circle theorem's audit.

The [elementary route lemmas](proofs/STRUCTURAL_ROUTES.md) also give valid trapping and compatible-core-circle sufficient conditions. A realized all-enlargements retraction obstruction would suffice for a negative answer, as proved in the [structural proof](proofs/OBSTRUCTION_AUDIT.md), but no such realization is supplied here.

### Scope of the 2013 satellite correction

The topological satellite example refutes only the unqualified circle-approximation implication in Kuperberg's [*Periodicity generated by adding machines*](https://trim.imath.kiev.ua/index.php/trim/en/article/view/310), p.145. The preceding sentence introduces a nonsingular flow. An interpretation that additionally requires simultaneous invariance is stronger and is **not refuted** by this topological example. Neither the paper's adding-machine theorem nor the full invariant-enlargement problem is disproved. Periodic points near a set also do not by themselves give whole periodic orbits confined to a prescribed neighborhood.

## The vertical shortcut cascade

For nonempty compact stationary C, the bounded globally Lipschitz field F_C=min(1,dist(·,C))e₃ has a continuous full flow. Each nonstationary orbit is one entire complementary interval of a vertical fiber. A compact invariant superset can add only whole bounded fiber gaps, subject to closedness. Write M_r(C)=Inv({dist(·,C)≤r}).

| Proposed sufficient condition | What the authored construction proves | Proof and audit |
|---|---|---|
| Fill every sufficiently short vertical gap; use a uniform bound on fiber components; glue movable slabs. | A nonmovable stretched-book compactum has at most two fiber components and every bounded gap has length 1. Short-gap filling leaves it unchanged. Its small slab pieces and their intersections are movable. | [Short-gap proof](proofs/VERTICAL_GAP_COUNTEREXAMPLE.md); [acceptance with direct slab proof](audits/VERTICAL_GAP_ACCEPTANCE.md) |
| Every selected metric radius, or all sufficiently small radii, give movable cores. | Movable stationary C can have a nonmovable prescribed M_r. One movable C has bad radii tending to zero. | [Metric-threshold proof](proofs/METRIC_THRESHOLD_COUNTEREXAMPLE.md); [acceptance](audits/METRIC_THRESHOLD_ACCEPTANCE.md) |
| An ambient regular distance value or Lipschitz distance sphere suffices. | A movable C has nonmovable M₁ despite no Clarke critical value in [3/5,∞). Every smaller core equals C. The unit neighborhood is not isolating. | [Regular-radius proof](proofs/REGULAR_RADIUS_COUNTEREXAMPLE.md); [acceptance](audits/REGULAR_RADIUS_ACCEPTANCE.md) |
| Exclude boundary orbit segments, or require strict quadratic contacts. | A curved wall gives strict internal quadratic contacts with coefficient 1/98 and no nontrivial vertical boundary segment; M₁ remains nonmovable. Smaller cores are movable by cap retraction and need not equal C. | [Quadratic supplement](proofs/QUADRATIC_TANGENCY_SUPPLEMENT.md); [acceptance](audits/QUADRATIC_TANGENCY_ACCEPTANCE.md) |
| Hausdorff continuity at r, even with ambient regularity and movability at every smaller radius, suffices. | One movable C has every 0<r<1 core movable and M₁ nonmovable, while the core family is Hausdorff-continuous from both sides at 1. Auxiliary columns remove the jump while retaining a nonmovable retract. | [Continuity counterexample](proofs/LEFT_CONTINUITY_COUNTEREXAMPLE.md); [acceptance](audits/LEFT_CONTINUITY_ACCEPTANCE.md) |

These are failures of particular construction rules. In the movable-stationary-set examples, **B=C already satisfies the original enlargement request**. The short-gap example also fails to exclude every other permitted enlargement. A bad selected core, even at arbitrarily small radii, is not an all-enlargements counterexample. The continuity example does not refute almost-every-radius or co-countably-many-good-radii statements by other arguments.

## Precisely what remains missing

An affirmative solution must produce a compact invariant movable B in every prescribed U for arbitrary continuous φ and arbitrary compact invariant A. The isolated dimension-one theorem leaves several distinct gaps:

- In dimensions two and three, the finite-graph argument is unavailable. Loop surjectivity alone supplies neither coherent lifts of relations nor a homotopy on a higher-dimensional domain.
- Infinitely many connected components require control beyond the finite disjoint-pasting argument.
- Most importantly, A need not be isolated or possess an isolated invariant enlargement inside U. The identity flow illustrates why isolation cannot be assumed, even though that flow itself has invariant finite-polyhedral enlargements.

On the vertical branch, it remains unproved here that every compact C has **some** arbitrarily small radius with movable M_r(C). None of the constructions refutes that existential assertion. Even a proof of it would still need a separate reduction to address arbitrary flows.

A negative solution must instead exhibit one actual full flow φ, compact invariant A, and open U, and exclude **every** compact invariant movable B with A⊆B⊆U, including B=A and disconnected B. Nonmovability of A alone, of a chosen core, or of an abstract collar/quotient example does not meet that requirement. No such triple and exclusion proof were obtained.

## Reading and verification

- [Proof and audit index](PROOF_INDEX.md) gives dependencies, exact scopes, and the five-pass development.
- [Sources, versions, and credit](SOURCES.md) identifies imported results and inspection limits; [source identity metadata](SOURCE_METADATA.json) records available public PDF hashes and sizes.
- [Corrections and historical status](CORRECTIONS.md) distinguishes the corrected theorem from its original and identifies superseded proposals and wording clarifications.
- [Artifact provenance](ARTIFACT_PROVENANCE.json) distinguishes original reviewed bytes from public-reader bytes. Dated proof files retain drafting-time status sentences; the final acceptance table and linked reports give their completed review status.
- [Integrity instructions](INTEGRITY.md), [manifest](MANIFEST.json), and [verifier](verify_reader.py) support offline byte-integrity and inventory checks. **Hashes and a successful verifier run do not prove the mathematics.**

Only authored mathematical material, public citations, and safe verification metadata are included. Third-party source PDFs and extracts are not redistributed.
