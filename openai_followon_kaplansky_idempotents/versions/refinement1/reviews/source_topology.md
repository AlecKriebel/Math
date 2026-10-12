# Independent source audit: topology, existence, and formalization scope

Reviewer: internal independent audit agent `source_topology`.
Audit checkpoint: 2026-10-06 22:12 America/Los_Angeles (2026-10-07 05:12 UTC).
Upstream checked read-only: `/Users/alec/Desktop/math`, HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Target request read directly: `notes/ORIGINAL_REQUEST.txt`.

## Verdict and scope

**No substantive gap found in the cone-picture criterion, the rooted disk surgeries, or the deduction of torsion-freeness.** This is an independently checked conditional theorem: if the finite immersed graphs have no reduced spherical arrangement in the paper's precise sense, their cone complex is a finite two-dimensional classifying complex, its group is finitely presented and torsion-free, and both designated roots are protected. In particular, the root-protection assertion has been checked separately; it is not inferred from asphericity alone.

The separate bounded-pattern estimate is a pivotal dependency. I read its statement and image-rank/multiplicity-incidence portions, but do **not** give an independent complete signoff on its block and probability proof in this report. It is assigned to the combinatorics audit. The random-model conditioning/diameter section and planar reduction were also read and checked, with no local gap found. An unconditional acceptance of the October 4 existence theorem still requires that separate combinatorics verdict. No Lean build or numerical matching certificate was obtained here.

This is a source-dependency audit, not a priority audit or complete publication-package review. It does not certify novelty of the follow-on consequence.

## Exact material reviewed

Base directory `sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/`:

| File | Lines actually reviewed | Purpose |
|---|---:|---|
| `sections/topology.tex` | 1–335, complete | Cone-picture representation; all four surgeries; protected roots; asphericity; torsion |
| `sections/algebra.tex` | 1–125, complete | Exact attachment, scalar formulas, root-protection requirement, finite parity product proof |
| `sections/random.tex` | 1–449, complete | Finite types; balanced matchings; girth conditioning; prescriptions; expansion; diameter |
| `sections/planar.tex` | 1–440, complete | Definition of reduced arrangement; closure; digons; separator; extraction parameters and quantifiers |
| `sections/patterns.tex` | 1–250 | Exact bounded-pattern dependency; image complexity; multiplicity incidence; start of grid construction |
| `sections/assembly.tex` | 1–27, complete | Exact existential selection and final group/ring conclusions |
| `sections/introduction.tex` | 1–109, complete | Main claim and stated source lineage |

Other material read: manuscript README and citation block; repository `sources/README.md`; `sources/lean/docs/197.md`; actual declarations and their statements in upstream `lean/OAI/RingTheory/DirectFiniteness/FinitelyPresented.lean` lines 1–44 and `Main.lean` lines 1–13; upstream `lean/ComparatorChallenges/KaplanskyFinitelyPresented.lean` lines 1–14; corresponding `lean/formalization.yaml` entry lines 1266–1268. The upstream tree was not modified.

## Exact topological claim and proof checks

The construction is the pushout

\[
X=F\cup_{\bigsqcup\Lambda\to F}\bigsqcup K_\Lambda,
\qquad G=\pi_1(X,*),
\]

where the finite graphs are immersed in a rose and `K_Λ` denotes the abstract cone on each connected component. Neither a component nor a cone is asserted to embed after attachment. This distinction matters in both picture representation and surgery.

1. **Relative cone replacement (topology lines 55–81).** A spanning tree supplies a free basis of `π₁(Λ)`. Attaching one ordinary disk per basis loop produces a simply connected acyclic complex `Y_Λ`, hence a contractible CW complex. Both `Y_Λ` and `K_Λ` contain `Λ` as a CW subcomplex. Cell-by-cell extension gives maps and homotopies relative to `Λ`, so replacing the cones in the pushout preserves homotopy type relative to `F`. This does not assume that the attaching immersion embeds its domain. The presentation-complex reduction is therefore valid.
2. **Picture representation (lines 83–105).** Mapping-cylinder collars and finite subdivision allow a surface map to be made simplicial. A target disk point avoiding images of source edges and degenerate triangles has finitely many inverse images in nondegenerate source triangles, each locally a homeomorphism. Expanding a small target disk and collapsing its complement to the attaching boundary produces disjoint cone disks with complement mapping to the rose. All homotopies can fix a prescribed outer label word.
3. **Minimality and pairing (lines 121–160).** Minimal total boundary length exists over nonempty collections of nonnegative integers. Tightening inner graph paths preserves the map up to homotopy because the cone is contractible; constant inner disks can be removed. The rooted path is tightened with fixed graph endpoints. Since those endpoints are distinct, it cannot become empty. A picture witnessing either an essential sphere or a null path from a root to a distinct vertex has at least one ordinary inner disk. Generic fibers of rose-edge interior points give disjoint arcs pairing inverse letters; circles may be discarded because they carry no boundary occurrences.
4. **Same-edge lift (lines 162–194).** If paired occurrences traverse the same undirected graph edge, a thin band around the pairing arc maps into a small rose-edge interval. It has a lift into that particular abstract graph edge agreeing with both boundary lifts. The adjacent cone disks are consequently in the same cone component. This is why the local shortening uses the actual edge `e`, not just a coincident letter label.
5. **Two different inner disks (lines 200–208).** Their union with the band is a disk mapping through one abstract cone. Its new boundary is `PQ` from `(eP,e⁻¹Q)`, with two edge occurrences removed. Contractibility gives a homotopy relative to the remaining surface, preserving essentiality in the sphere case and preserving the outer word in the disk case.
6. **Inner disk to exterior disk (lines 210–216).** Enlarge the formal exterior disk, discard its interior, and restrict the old map to its complementary disk. The new outer graph path is `PQR` from `(PeR,e⁻¹Q)`, with its original endpoints retained. The sum of old inner and outer lengths falls by two. This is a restriction argument, not an assumption of a new filling.
7. **Both ends on exterior disk (lines 218–227).** The disk plus band is an annulus. Of its two complementary disks, retain the one whose boundary contains the marked break. Its map fills `PR` from `PeQe⁻¹R`, retaining the fixed endpoints. No assumption that `Q` separately bounds a disk is made or needed. Since root and endpoint differ, `PR` cannot tighten to an empty graph path.
8. **Both ends on one inner disk (lines 231–270).** The union is again an annulus mapping through one cone. Capping the complementary regions with maps into that cone yields shortened boundaries `P,Q`. In the rooted case retain the complementary component containing the exterior disk, preserving its outer path and reducing inner length by at least two. In the sphere case one new sphere must remain essential: lift the original sphere and use a single lift of the abstract cone for both caps. The original homology class is the sum of the capped sphere classes, since the discrepancy factors through the contractible abstract cone. Hurewicz in the simply connected universal cover identifies `π₂` with `H₂`. This avoids the invalid inference that an immersed cone image itself is an embedded contractible subspace.
9. **Contradiction (lines 277–284).** Every same-edge pair yields a lower-length picture retaining the failure being minimized. Hence all pairs use distinct underlying edges and the resulting picture satisfies the exact reduced-arrangement definition. Absence of such arrangements rules out both failures independently.
10. **Asphericity and torsion (lines 286–335).** `π₂(X)=0` implies `H₂(\widetilde X)=0`; the simply connected two-dimensional universal cover has no higher cellular homology, so all homotopy groups vanish by the first-nonvanishing-group form of Hurewicz, and Whitehead makes it contractible. Its chains form a length-two free `ℤG` resolution of `ℤ`. Restriction to any prime-order cyclic subgroup remains free because `ℤG` is free over that subgroup ring. This would force all cohomology above degree two to vanish, whereas the explicit alternating `(u−1),N` resolution gives `H^k(C_ℓ;\mathbb F_ℓ)=\mathbb F_ℓ` in every degree. Thus no torsion can occur.

Boundary cases checked: disconnected labeled graphs; immersed rather than embedded cones; graph loops before girth conditioning; outer endpoints identified at the rose vertex but distinct in the abstract graph; self-bands; essentiality after sphere splitting; constant boundaries; a single intact exceptional path shorter than `L`; repeated path occurrences; orientation/sign convention for inverse pairing; cyclic rather than merely linear immersion on ordinary boundaries.

## Planar/probabilistic interface checks

The deterministic reduction does not take a union over all arrangement sizes. Its `ε` is obtained first from the bounded-pattern theorem, then diameter/closure constants, then fixed `U,η,K₀,C,I`; only afterwards is `n` taken large. Every finite arrangement, regardless of disk count or total length, extracts a path system for that same triple. This addresses the critical unbounded quantifier.

The short-closure construction deletes at most two incident edges, retaining minimum degree at least 127. Two distinct reduced walks with the same endpoint give a nonempty reduced based loop of length `O(log n)` avoiding the deleted edges. They need not be cyclically reduced at their basepoint because the joins to the given segment and the return geodesic use the avoided edges. Thus the original segment is retained without cancellation.

The interval-pair count uses `sum_Q(ℓ_Q−2χ(Q))=2N₀−4`, which remains valid for disconnected regular neighborhoods and complementary regions with multiple boundary components. Only one monogon is possible at the exceptional break. Marking and pairing cuts produces at most `6N'` interval pairs.

The separator budgets use totals rather than requiring every cluster to be good. Deletion loses at most `2ηUH₀` original occurrences; closure adds at most `(3D₀/U)H₀`. The discarded bad clusters cost at most `H₀/16` each for unpaired proportion and interval count. There is at most one short cluster, containing only the intact exceptional path; it costs less than `H₀/2`. Thus some cluster survives with `L≤H≤CL`, the required rooted interval condition, and the distinct-edge comparison condition.

The girth-conditioning switch is also compatible with overlapping domain/codomain vertex sets. It transposes two slot matches, retains all outgoing types, creates no short cycle when the switched edges are sufficiently distant and the auxiliary edge is not bad, and has a unique inverse determined by the missing prescribed pair. Its counting gives the claimed conditional upper bound without needing a lower probability bound for large girth. No contradiction in the stated expansion/diameter estimates was found.

## Strongest justified explicitness

The source gives a finite **existence construction**, not a listed graph, numerical presentation, or multiplication certificate.

- Use `q=128`, the projective plane over `\mathbb F₁₂₈`, `v=16513`, `p=129/16513`, and seven Fano-plane extra letters. The signed alphabet has 16520 letters, hence the rose has **8260 generators**.
- Pair seven extras with seven distinct ordinary letters; pair remaining ordinary letters. This arbitrary choice is fixed before matching. Choose sufficiently large `m≡1 mod 4`, `n=vm`, `|A|=vm`, `|B|=v(m−1)`.
- Line classes have sizes `m,m−1`; the exact extra-part counts are `a_m=(129m−1)/4`, `b_m=129(m−1)/4`. Balanced within-line assignments are fixed; `x_A` has all seven extras and `x_B` is any fixed root in `B`.
- For each inverse pair and side independently, choose a bijection between equally sized outgoing-letter slot sets. Condition on girth `L=floor(c₀ log n)` for a sufficiently small fixed `c₀` satisfying the two explicit inequalities in random lines 229–230. The source proves that sufficiently large admissible `m` admit an outcome with no reduced arrangement. It does not supply a numerical threshold or choose and list the outcome.
- Once an outcome exists, a concrete finite presentation is obtained by choosing a spanning tree in every component `Λ`. For every oriented nontree edge `e:u→v`, choose tree paths `Q_u,Q_v` from the component tree root and impose the relator word `label(Q_u e Q_v⁻¹)`. One chosen orientation of each nontree edge suffices. These relators normally generate every closed graph-path label. This presentation on the rose's 8260 generators has `E(Γ)−V(Γ)+c(Γ)` relators.
- Exact counting from the prescribed incidences gives `E(Γ_A)=1065540m`, `E(Γ_B)=1065540(m−1)`, and `V(Γ)=16513(2m−1)`. Consequently the above presentation has `1049027(2m−1)+c(Γ)` relators. This count is derived here; it is not a numerical witness because neither `m` nor `c(Γ)` is supplied.
- In the root-containing components, take any graph paths from the roots to each vertex. Their group labels `g_x,h_y` determine `a=Σg_x`, `b=Σg_x⁻¹`, `c=Σh_y⁻¹`. These finite scalar sums have coefficients in `\mathbb F₂` after collecting equal group elements; different nonroot vertices need not have distinct labels. Root protection does guarantee that only the root contributes to the identity coefficient of each applicable sum. In particular `c` has identity coefficient one.
- No termination proof for an effective search checking infinitely many reduced arrangements is supplied. An existential theorem does not require such an algorithm. Calling this a finite construction is valid; calling it a computed or independently enumerated multiplication certificate is not.

Numerical evidence reproduced by exact rational arithmetic: the ordinary-row weighted matrix bound is `71589573988/72026254783 ≈0.9939371997570104<1`; the extra-row ratio to `f(t)=4` is `195474585/311633336 ≈0.6272582628964958<1`. These verify only the elementary strict inequalities at `q=128`, not the central probabilistic theorem.

## Lean scope

The actual earlier theorem is `OAI.KaplanskyCounterexample.finitelyPresented_counterexample` in upstream `lean/OAI/RingTheory/DirectFiniteness/FinitelyPresented.lean` lines 35–40. It explicitly quantifies an arbitrary finite characteristic-two field and a finitely presented group containing an element of odd prime order. Its fuller theorem at lines 14–30 supplies the earlier selected search data and repeats that torsion conclusion. It is **semantically incompatible** with treating it as a formalization of a torsion-free `\mathbb F₂` example.

The family documentation's heading references torsion-free group algebras, but its listed companion manuscripts and scope concern the September 23 characteristic-two torsion-containing construction, the determinant consequence, and the September 26 odd-characteristic torsion-containing example. The comparator file has `sorry`; it is a comparator statement, while the actual proof declaration is in the `OAI` tree. Neither file supplies the October 4 asphericity/protected-roots theorem.

I did not run Lean: reproducing a build of the earlier theorem would not verify the audited October 4 dependency. No formalization claim is used in this report. The available source-level evidence is the mathematical topology proof itself.

## Exact source hashes

SHA-256 at this checkpoint:

| File | SHA-256 |
|---|---|
| `direct-finiteness.pdf` | `7950476863f21811aaccb99ab12f24f81741e5077ca290394d029063024aaee8` |
| `build/paper.tex` | `573c88ef3fdf465fc10b132d2c3b8d502b27b5d40cd5ef403ab3cc5e5c2d474b` |
| `build/sections/topology.tex` | `f1e50e15464174e5ef32d9dfe966fe7e12b4dd480af60a27228d901cc159b1b0` |
| `build/sections/algebra.tex` | `71fe26eab4e6a01564a687c522bbceb8923182c0201af9685eac84d9f86a141f` |
| `build/sections/random.tex` | `bb172b92ba622e262c2bf124e70c3cd55922200083c09db658615759b81323c4` |
| `build/sections/planar.tex` | `e3a1a4e23dd6871a9746ffde05d32297e695f3167b8efa0f0a4cad5da8c9ae6b` |
| `build/sections/patterns.tex` | `20c6cc1f3fb035150831e5091c98313f04e7a9d8aaa347507020b176394ed4ea` |
| `build/sections/assembly.tex` | `3987e23ea7c5c8d217ca539d5a307d59f8eac5b8381a0afe411125e57f0bee4a` |

Checkpoint estimate: this agent's assigned geometry/formalization-scope audit **100% complete**; unconditional mathematical resolution estimate is deliberately left to integration with the other source audits. Publication package review **0% complete by this agent**. No git operations or external communication were performed.
