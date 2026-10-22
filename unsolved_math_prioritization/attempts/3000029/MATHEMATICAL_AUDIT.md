# Independent mathematical audit: minimum rigidity cut

Problem 3000029 / AMR-029-0029. Audit completed 10 October 2026.

## Verdict

**ACCEPTED PARTIAL RESULT.** The unrestricted deterministic polynomial-time question is not solved. No hardness reduction or novelty claim is accepted or asserted. The exact budgeted clique-cover identity, bounded-regime algorithms, fixed-basis counterexample, and infinite unique-cut family are correct in the stated category.

A narrow source-description caveat was added during the independent audit. No mathematical statement or proof was changed. This public edition preserves the complete accepted analytic arguments and binds [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): 18,943 bytes; SHA-256 `ace77ee8a54b693e06478b113a2c5f207b2ebe253d6cd6d37269580244813307`.

Editorial changes record completed acceptance, use public file names, and distinguish historical supporting observations from edition preparation. The source caveat does not assert a replacement theorem or infer the source author's intent. This audit is AI-assisted and unrefereed; acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. All source retrieval, rehash, inspection and computational descriptions below are recorded proof-review or independent-audit history, not new edition-preparation work. Programs and raw outputs are excluded; the analytic proof depends on no omitted executable.

## 1. Exact objective and source boundary

The accepted input is a finite simple graph on a fixed vertex set of size n >= 2 that is generically locally rigid in the Euclidean plane. All vertices survive deletion. The unweighted objective is the smallest number of edges whose deletion reduces planar generic rigidity rank below 2n-3. Generic local rigidity and generic infinitesimal rigidity coincide; generic global rigidity is a stronger, different property. No topological planarity assumption is imposed in the general problem.

The [original EGRES problem](https://oldlemon.cs.elte.hu/egres/open/Destroying_rigidity) and its [discussion](https://oldlemon.cs.elte.hu/egres/open/Talk:Destroying_rigidity) were inspected in their complete retained text. Live direct opening failed in this audit, so that inspection is not represented as a successful fresh fetch. Their minimum-cut formulation is the minimum-cocircuit problem for the restricted rigidity matroid. The discussion's hypergraphic result has restricted scope; transversal minimum-circuit hardness does not supply rigidity minimum-cocircuit hardness.

The [2017 report by Bérczi, Bernáth, Király and Pap](https://egres.elte.hu/tr/egres-17-07.pdf), printed page 3 / PDF page 4, was independently opened and inspected. It explicitly separates the polynomial minimum-cut results for unions of graphic/hypergraphic matroids from the rigidity-matroid question. This is historical source evidence, not a worldwide-current-openness certificate.

The global-rigidity clique-addition problem is not interchangeable with this deletion problem, and its results are not used to resolve the present question.

### Classical rank and component formulas

The survey [Rigidity of Graphs and Frameworks: A Matroid Theoretic Approach](https://arxiv.org/abs/2508.11636), by James Cruickshank, Bill Jackson, Tibor Jordán and Shin-ichi Tanigawa, gives the needed exact assumptions in Theorem 3.1 and equation (2), pages 10-11. Those pages were read and visually inspected. It states planar rigidity through a spanning (2,3)-tight subgraph and credits the rank-cover simplification to Lovász and Yemini. For a finite simple graph, rank is the minimum of sum(2|X|-3) over covers of its edges by vertex sets of size at least two; an optimal cover may be 1-thin and consist of maximal rigid components. Isolated vertices need not be covered. The empty edge set has the empty cover and rank zero.

The [Lovász-Yemini publication record](https://doi.org/10.1137/0603009) was checked. Its full original 1982 article was not obtained in this audit; no claim of reading its full proof is made. The exact formula was checked in the above author-written survey and independently derived below. This is sufficient because the submitted proof does not use an uninspected specialized theorem.

The general count-matroid rank formula should not be silently conflated with a minimum-cut algorithm: its partition/uncovered-edge rank minimization concerns the rank of a fixed edge set. Here two-vertex cover sets have cost one, allowing individual leftover edges to be covered. The proof needs only the (2,3) sparsity matroid on simple graphs, with all nonempty edge supports having at least two vertices and positive count 2|V(F)|-3. It makes no claim for arbitrary parameters or arbitrary count matroids.

### Servatius printed-condition caveat

[Servatius's dissertation](https://users.wpi.edu/~bservat/phddissertation.pdf), Chapter 4, Theorem 2, printed pages 32-33 / actual PDF pages 52-53, was read and visually inspected. Its printed even-subfamily condition (2)(b) combines a strict '>' with '+2'. For the two triangles on {0,1,2} and {0,3,4}, the union size and displayed right-hand side both equal five. Their union has rank six; adding edge 13 yields a seven-edge Laman graph on five vertices. Thus {13} is a cocircuit, while these two residual rigid blocks do not satisfy that printed strict condition.

The audit does not infer the source author's intent or assert a replacement theorem. The submitted Laman proof does not invoke the printed condition. A narrow caveat now says exactly that. The statement that the rigid-block description is classical remains warranted independently by the rank-cover source and direct proof.

[Yu and Anderson](https://skoge.folk.ntnu.no/prost/proceedings/ifac2008/data/papers/0554.pdf), Section 3.2 and Lemma 3 on printed page 6586 / PDF page 3, were visually inspected. Their degree bound matches the report for rigid graphs on at least three vertices. Their deliberate convention calling one- and two-vertex graphs non-rigid is not imported. [Jordán's extremal paper](https://doi.org/10.1007/s00373-021-02327-4) has a 2020 preprint and a 2021 published version; its extrema and specified families do not supply arbitrary-input optimization. All eight supplied source byte counts and hashes match the retained copies. No source text or page rendering is included as an audit deliverable.

## 2. Rank-budget cover identity and closure

Let H be a maximum-cardinality nonspanning subset of the rigid edge set E. For each e in E minus H, maximality forces r(H+e)=2n-3. A one-element rank increase is at most one, so r(H)=2n-4; no excluded edge lies in the closure of H. Therefore H is a hyperplane of the restricted matroid and its complement is a cocircuit.

Take a Laman-independent basis B of H. If two tight vertex sets meet in at least two vertices, induced edge counting and the sparsity upper bound on their intersection imply that their union is tight. More explicitly, for tight A,C,

|B[A union C]| >= |B[A]| + |B[C]| - |B[A intersection C]|
               >= 2|A union C|-3.

Independence makes equality hold. Hence distinct maximal tight sets intersect in at most one vertex. Every B-edge starts a tight two-vertex set and belongs to a maximal one. Their induced edge sets are disjoint and exhaust B, so their costs sum to |B|.

For an H-edge outside B, its fundamental circuit in B+e has one more edge than the Laman bound on its support. Removing e leaves a tight B-set containing both endpoints. Thus every H-edge is covered by the cliques of maximal tight sets. Conversely, any pair in such a clique is in the closure of B and hence H. No deleted E-edge can be covered. This proves the exact retained-edge representation and cost 2n-4.

For any candidate family, without any thinness assumption, subadditivity gives rank of its clique union at most its total cost. A family with cost at most 2n-4 therefore gives a valid deletion. Combining both directions proves the stated optimization identity. The use of arbitrary rather than already-rigid candidate subsets introduces no hidden feasibility assumption.

The component identification is also valid. If H[Y] is rigid, take a Laman basis D on Y. Each D-edge lies in a maximal tight B-set. Starting with D, attach the corresponding complete rigid sets along these covered edges. Each attachment shares two distinct vertices, so the union is rigid. The independent B-subgraph on that union spans all attached sets; its rank is therefore 2|U|-3, making U tight. Maximality forces every used component into a single maximal tight set. This also verifies the edge-closure claim used later.

For n >= 3 a rank-(2n-4) residual cannot have an isolated vertex: its rank would be at most 2n-5. At n=3 the remaining two-vertex graph has rank at most one, so this boundary is valid. For n=2, K2 has cut value one and the empty family gives cost zero. The report excludes n=1 and correctly states that no feasible edge deletion destroys its rigidity; no zero optimum is fabricated.

Nothing in this identity optimizes over its exponentially many candidate subsets and families in uniform polynomial time.

## 3. Degree, nullity, algorithms, and complete graphs

For a rigid graph on n >= 3, minimum degree is at least two. Deleting all but one incident edge at a minimum-degree vertex leaves at most 2n-5 rank on the other vertices plus one incident constraint, strictly below 2n-3. This gives rho <= delta-1 without assuming the other induced graph is rigid.

If q0=m-(2n-3), retain a basis minus one edge. Exactly q0+1 edges have been deleted and rank is 2n-4. Thus 1 <= rho <= min(delta-1,q0+1), with no missing additive constant or negative-nullity case in the rigid domain.

[Lee and Streinu](https://arxiv.org/abs/math/0702129), basic algorithm, Theorem 8, Corollary 9 and its complexity analysis on PDF pages 10-11, were visually checked. The parameters k=2, ell=3 are in the allowed upper range 0 <= ell < 2k; n=2 is expressly allowed, and every n >= 3 meets the matroid-size threshold. Both endpoints are protected while collecting ell+1=4 pebbles; one pebble is consumed on acceptance. Their basic algorithm has O(nm) time for these fixed parameters, which is already sufficient. The faster component-aware variant is not needed for any claim here.

With that basic oracle, the enumeration takes O(nm times sum_{j=1}^b binomial(m,j)). Concrete valid bounds include:

- delta <= D fixed: O(n m^D).
- q0 <= C fixed: O(n m^(C+2)); since m=2n-3+q0, also O(n^(C+3)) for fixed C.
- Simple topologically planar rigid inputs, n >= 3: delta <= 5 and m=O(n), so O(n^6) suffices.

These are class-wise polynomial / XP bounds, not an FPT bound or an arbitrary-input polynomial bound. A bounded average-degree class has a bounded-minimum-degree upper bound. No graph embedding is needed to justify the special-case enumeration.

For K_s, s >= 3, the claimed rho=s-2 follows by an induction retaining rigidity after at most s-3 deletions. In the nonempty-deletion step choose a vertex incident with d >= 1 missing edges. The remaining (s-1)-vertex graph has at most s-4 missing edges, and the removed vertex retains at least two distinct neighbors because d <= s-3. The s=3 base has no missing edges. K2 is properly separated.

## 4. Fixed-basis obstruction

K3,3 is a nine-edge Laman basis of K6. Adding any one of the six same-side nonbasis edges yields a ten-edge circuit: every proper vertex subset is sparse, including the extremal 3+2 subset with at most seven edges. Thus each of these six fundamental circuits contains every basis edge. The fundamental cocircuit at each b in the basis is exactly {b} union (E(K6) minus B), of size seven. The true cut is four by the complete-graph lemma. This invalidates the one-arbitrary-basis shortcut only. The report does not extrapolate it to adaptive basis algorithms or hardness.

## 5. Infinite family and all parameter boundaries

Take t >= 1, s >= t+3, q >= 2. The edge-inflated K2,q has n=(2s-3)q+2 vertices and 2q binomial(s,2) edges. Distinct inflated cliques share at most one skeleton vertex and share no edge. Its selected bases are obtained from the independent K2,q skeleton by two-neighbor vertex additions, giving an independent set of size 2q(2s-3)=2n-4. Subadditivity across the cliques gives the reverse rank bound.

Equality between the full rank and the sum of ranks of the disjoint clique edge sets implies a direct sum of their restricted matroids. Therefore rank on any induced vertex set X is the sum of f(|X intersection C_e|), where f(0)=f(1)=0 and f(j)=2j-3 for j >= 2.

For an active edge family A with h >= 2, let k be its number of incident z-vertices. If exactly one hub is incident then h=k >= 2, and h <= 2(h+1)-4. If both hubs are incident then h <= 2k=2|V(A)|-4, including k=1,h=2. Thus the report's inequality holds in every case. Repetition of skeleton vertices contributes at most 2h-|V(A)| to the sum of active intersection sizes. The resulting rank is at most 2|X|-4. If h=0, X of size at least two has rank zero; if h=1, equality with the rigid rank is possible only if all of X lies in that clique. Hence the maximal rigid blocks are exactly the 2q cliques, including at the smallest q=2,s=4,t=1 boundary.

Any missing pair lies in different blocks and therefore outside the closure, so it raises rank by one to 2n-3. Any chosen brace rigidifies. There are enough distinct braces: the concrete choice uses one private vertex of one clique and t of the s-2 private vertices in the other; s-2 >= t+1.

For a deletion D with |D| <= t that is not all of T, a brace survives. Every damaged clique loses at most t <= s-3 edges and stays rigid by the complete-graph lemma. Its closure recovers the full clique; hence the residual closure contains H and the surviving brace and is rigid. This proves minimum value t and uniqueness of T, for arbitrary distinct missing-pair braces. No disjoint-brace or particular-endpoint assumption is hidden in this argument.

For q=2 the skeleton is the four-cycle and remains connected after any vertex deletion. For every q >= 2, deleting a private vertex leaves its clique connected, while deleting a skeleton vertex leaves a connected skeleton and every affected clique attached through its other endpoint. Thus H is 2-vertex-connected. Across every nontrivial vertex cut, connectedness supplies a split clique, contributing at least s-1 crossing edges. For the concrete braces, any private vertex in a clique incident with z2 is untouched and has degree s-1. Consequently lambda(G)=delta(G)=s-1. Equality is claimed only for the concrete brace choice, as required.

The unique cut exposes 2q maximal rigid blocks. For any budget-feasible clique cover attaining it, its union must cover H. Including any missing pair would raise rank to 2n-3, contradicting the budget. Each cover set must therefore lie within one maximal block. Every block has edges, and distinct blocks share no edges, so at least 2q sets are needed. This rejects every bound depending only on rho on the number of sets needed for an optimum. It neither proves NP-hardness nor excludes other optimization methods.

## 6. Recorded independent finite verification and limits

The independent audit records that the initial proof-review verifier was read, compiled, and replayed in both O2 and O3/NDEBUG configurations before and after the source-caveat edit. All reported fields except elapsed time agree. Its explicit exception-based checks survive NDEBUG. Exhaustive counts are 33,866 labeled graphs on orders 2-6 and 8,128 rigid inputs. The basic pebble game and greedy vertex-subset sparsity implementation match. The recorded large-family rigid-component count is a construction/theorem value, not an independent exhaustive component enumeration; the proof above establishes it. The four larger deletion suites are sampled, not exhaustive, as the report correctly discloses.

The audit records two separately authored checks that imported no initial proof-review code:

1. The exhaustive graph check directly enumerates all sparse edge sets, applies a maximum-subset transform to obtain ranks, and compares these with a min-plus clique-union cover dynamic program. It checks closure equals the maximal-rigid-block clique union and block-cost additivity for every one of the 33,866 graphs, not just rigid inputs. It enumerates complete-ground hyperplanes and checks all 75,139 distinct optimal residuals among rigid inputs for exact one-rank drop and cocircuit restoration. It also checks both bounds and all K6 fundamental cocircuit contents. Rigid graph counts by order are 1,1,7,156,7963. All checks pass.

2. The family check uses exact rigidity matrices modulo the prime 2^31-1 and independently computes their stress-space dual representations. It applies the exact identity r(E-D)=r(E)-|D|+r*(D) to all deletion subsets under test. Nonzero modular minors are exact certificates that the corresponding integer-polynomial minors are nonzero in characteristic zero; deficient upper bounds come from the analytic clique cover. It performs 56,564 deletion checks: every single brace among 42 missing pairs for (q,s,t)=(2,4,1); eleven brace choices for (2,5,2), with all deletions of size at most two; the concrete (2,6,3) family, with all 41,728 deletions of size at most three; and every single brace among 100 missing pairs for (3,4,1). Every missing pair is checked for single-edge restoration in all four residual families. All checks pass.

The audit records that both checks were rerun with Python optimization enabled; their exception-based checks remained active, and outputs agreed after excluding elapsed time. Two negative controls rejected an incorrect manifest pin and altered proof bytes. Edition preparation did not rerun these mathematical tests. [ACCEPTANCE.json](ACCEPTANCE.json) retains aggregate results only. Finite verification supplements the analytic proofs. The modular specialization is not a floating-point or unverified genericity argument. The tests do not certify an infinite parameter family, mathematical novelty, or the remaining complexity classification.

## 7. Acceptance boundary

Accept the stated partial mathematics and scoped computational evidence. Preserve the general problem as unresolved by this attempt, with no arbitrary-input polynomial algorithm, no hardness reduction, and no novelty assertion. The remaining task is an exact uniform polynomial-time optimization over rigidity hyperplanes / the budgeted cover families, or an appropriate rigorously established hardness reduction. Hashes and exhaustive finite computations do not close that gap.
