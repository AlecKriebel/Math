# PASS2 independent validation

14 October 2026 UTC. This report checks the direct geometric AU construction, the enriched configuration route, and the actual small Floer complexes. It preserves the PASS1 theorem and source-scope adjudication. These are mathematical validation results; no historical-resolution or novelty claim is made.

## Findings

- The direct AU recipe supplies the previously missing direct rule for the exterior state: all-zero geometric sewing, geometric mapping-class action, and normalized inverse-sewing compression. Its use of RT in the subsequent comparison proof is not a definition by importing the exterior state.
- The normalization is `S00^(1−g)`. Omitting it would multiply the raw expression by `S00` at each isolated Heegaard stabilization. The declared extended lift, filling and unknot normalization are consistent.
- The Blanchfield enrichment distinguishes trefoil from mirror, but cannot determine Jones: an independently computed eleven-crossing knot has zero Alexander module and pairing, yet nontrivial Jones polynomial.
- The Floer calculation now uses actual geometric generators. It proves dimensions 3 and 5 for two Markov-equivalent unknot presentations and determines Rees arrows `V` versus `V` and `UV³`. This is not an Euler-only rank inference.

## 1. Direct AU recipe: definitions and comparison

Write `s=S00` and `D=s⁻¹`. The candidate defines

`h(K)=θ_T[D^(g−1) p_C W(f,0) v_H]`.

The three ingredients before applying `θ_T` are genuinely geometric surface operations: the sphere-vacuum inclusion followed by AU sewing, the extended surface action on flat vacua sections, and inverse sewing followed by projection to the vacuum channels of the compression disks. The fundamental filling is a fixed coordinate on the label-1 two-point sector after meridian factorization. No RT exterior vector occurs in these definitions.

The inspected AU geometric source supplies flat bundles, vacuum propagation, sewing and surface naturality. The later comparison identifies these surface operations with the RT modular-functor operations. It is legitimate to use that comparison afterward to prove that every relative Heegaard expression computes the same exterior state. This proof supplies independence rather than assuming it. The relevant primary statements are AU geometric Theorem 11.4 and §12, and AU comparison Theorem 1.1. The BHMV colored splitting and torus-basis statements check the compression and filling normalization.

The recipe is thus a substantive strengthening of PASS1's definition. It remains a construction within established geometric quantum theory. Ordinary H₀ still canonically realizes the horizontal-section space; it is not newly claimed that a knot-dependent boundary operator on the Teichmüller singular chains has been discovered. Source-level explanatory adequacy is a separate adjudication, not a mathematical defect established here.

### 1.1 Degree-zero homology is genuine and natural

For a connected simply connected base `X` and local system `L`, define

`θ:H⁰(X;L)→H₀(X;L), s↦[x,s(x)]`.

The degree-one boundary relations identify `[x,v]` with `[y,P_γv]`. They prove independence of `x`; unique horizontal continuation proves bijectivity. A morphism of flat bundles commutes with path transport and therefore with `θ`. Contractibility of marked Teichmüller space gives the needed hypotheses. Consequently the surface sewing and transport operations act on actual local-system homology after conjugation by these canonical identifications. No additional positive-degree condition is imposed.

### 1.2 Exact normalization and extended lift

Use the stated lift `S₀:a↦b, b↦−a` with weight zero, calibrated by gluing its mapping cylinder between vacuum solid tori to the weight-zero 3-sphere. This pins the phase; one cannot establish that phase from squared trigonometric identities alone.

For level `k≥1`, set `r=k+2` and `α=π/r`. In the chosen unitary normalization,

`S_ab=√(2/r) sin((a+1)(b+1)α)`, for `0≤a,b≤k`,

`s=S00=√(2/r)sin α`,

`d_a=S_a0/S00=sin((a+1)α)/sin α`.

The finite sine orthogonality identity implies `S²=I` and

`D²=Σ_(a=0)^k d_a²=r/(2sin²α)`.

These are identities at every level, not consequences inferred from a finite test. Since `0<α≤π/3`, both `s` and `d₁=2cos α` are nonzero.

An isolated cancelling handle pair has raw vacuum matrix element `p₀S₀i₀=s`. Hence its reverse compression must carry `D=s⁻¹`. A relative genus-g splitting with torus boundary has exactly `g−1` such compression handles, giving `D^(g−1)=s^(1−g)`. In the genus-one unknot exterior there is no compression factor; the state in the meridian basis is `S₀e₀`. Its label-1 coefficient is

`S10=d₁s`.

At genus two, the raw stabilized expression acquires one factor `s`; the extra `D` cancels it. Repeating this local relation gives the same result after any number of isolated stabilizations. Handle slides and arbitrary presentations are covered by the geometric/RT comparison, not merely by this scalar test.

A nonzero change of the fixed label-1 coordinate multiplies the numerator and unknot denominator together and cancels. The vacuum channel is fixed by the unit/propagation normalization; an arbitrary genus-dependent vacuum rescaling would not be harmless.

### 1.3 Anomalies

The chosen handlebody Lagrangian is its boundary kernel. The compressionbody Lagrangian is the pullback of the peripheral meridian Lagrangian, together with the compression-disk kernel. It is Lagrangian of the correct dimension. With the source-boundary orientation convention, the gluing map is a morphism between the oriented extended surfaces.

At each of the two decomposition gluings, the boundary Lagrangian agrees with the Lagrangian induced from one adjoining cobordism. Thus each Maslov triple has repeated entries and its index is zero. At the final exterior/filling gluing the triple is `(Qℓ,Qm,Qm)`, again zero. The direct formula therefore computes the declared weight-zero object rather than leaving an unspecified projective scalar.

### 1.4 Trefoil normalization, checked independently

Put `z=exp(πi/r)`, so the source Jones variable is `t=z⁻²`. The fundamental two-strand channels have quantum dimensions `[3]=z²+1+z⁻²` and `[1]=1`; `[2]=z+z⁻¹`. After the stated writhe correction, the positive three-crossing braid trace is

`([3]z⁻³−z⁻⁹)/[2] = z⁻²+z⁻⁶−z⁻⁸ = t+t³−t⁴`.

This is an exact Laurent identity after multiplying by the nonzero denominator, and agrees with PASS1's independently implemented bracket. At level one, `[3]=0`; the same identity remains valid because `[2]≠0`. The fundamental normalization therefore handles the low-level endpoint too.

`check_su2_calibration.py` verifies the complete S-matrix orthogonality, dimension sum, nonzero filling coefficient and trefoil identity for levels 1–12 in exact cyclotomic quotient fields over Q. It also checks the stabilization exponent algebra for genera 1–24. No floating point approximation is used. These computations supplement the preceding proofs and the cited sewing theorem; they do not replace either.

## 2. Alexander-one knot: exact obstruction to Blanchfield-only extraction

The source is the explicitly displayed PD on the primary Knot Atlas K11n42 page. Define `K_D` by that diagram, avoiding the page's warning about conventions for the named knot's mirror. The code independently:

1. Reads PD crossings in the documented counterclockwise convention, beginning with the incoming under-edge.
2. Determines their signs from the oriented edge sequence and obtains writhe `−1`.
3. Enumerates all `2¹¹=2048` bracket smoothing states, counting circles by disjoint-set union.
4. Applies the source writhe and variable normalization.
5. Collapses overpasses to Wirtinger generators, constructs the Fox Alexander matrix, and computes a cofactor over Q[t].

The computed normalized polynomial is

`V_KD(t)=−t⁴+2t³−2t²+2t+t⁻²−2t⁻³+2t⁻⁴−2t⁻⁵+t⁻⁶`,

and the selected Alexander cofactor is `−t⁵`. Thus `Δ_KD=1`. The implementation first calibrates both invariants on the negative trefoil PD; the bracket gives `t⁻¹+t⁻³−t⁻⁴`.

The unit cofactor gives the stronger module statement directly. The Fox rows lie in the kernel of the boundary row `(t−1)(1,…,1)`. In the usual `e_i−e_n` basis of that kernel, the invertible cofactor supplies a full set of relations, so the Alexander first homology is zero. Equivalently, the square Seifert presentation has unit determinant. Its Blanchfield pairing is necessarily the zero pairing. The unknot has precisely that same datum but Jones polynomial 1. Therefore no function of the isometry class of `(Alexander module, Blanchfield pairing)` alone equals Jones for every knot.

This is an obstruction to that specified enriched datum, not to all complement local systems or all secondary operations. The independent algebraic review also accepts the configuration report's trefoil pairing `u/(u²−u+1)` versus its negative: an isometry would require norm `−1` in Q(ζ₆), while the norm of `a+bζ₆` is `a²+ab+b²>0` for a nonzero element.

The source PD and comparison-table input are retained separately. The distributable checker accepts that input as a JSON argument; it does not embed or redistribute the copied data. Output metadata includes the exact input byte count and SHA256. The computed polynomial, matrix and determinant are independent calculation outputs. The stored replay is `K11N42_REPLAY.txt`. A standalone publication is not a self-contained offline replay of this PD test: it requires the separately sourced, hash-identified JSON input as an explicit command-line argument. The geometry and Floer fiber tests do not require that fixture.

## 3. Floer geometry: actual generators before rank claims

### 3.1 Source-diagram correspondence

The source starts with lower semicircular arcs `a_i`, and curves `b_i` bounding thin regular neighborhoods of upper semicircles. Simultaneously replacing concentric circles by concentric squares through a radial ambient isotopy gives exactly the rectangular lower U-arcs and upper U-neighborhood boundaries used by the PL implementation. The punctures on the horizontal axis stay fixed. The neighborhoods remain disjoint and nonnested.

Each PL braid generator is supported in a disk of radius 1.4 around the midpoint of two adjacent negative-axis punctures. That disk contains exactly those two punctures and lies strictly in the negative half-plane. The additional quantum punctures can be placed in the source-prescribed regions near the positive endpoints, outside these supports. After rescaling, all objects fit in the source disc.

The mesh map has positive oriented area on every source and target triangle and is the identity on the support boundary. Its degree is one. Positivity prohibits a cancellation of sheets, so it is an orientation-preserving PL homeomorphism. Its inner disk undergoes precisely a half-turn, with the turn tapering to zero through the annulus. It is therefore one of the two elementary half twists, not an arbitrary puncture permutation. Smoothing corners away from the finitely many transverse intersection neighborhoods preserves all intersections and the punctured-disc mapping class.

The inverse half twist has one intersection in the two-strand case. It cannot represent the source's positive generator, whose computed polynomial already requires at least three generators. The tested three-intersection half twist is consequently the positive source convention. Exact local signs and winding gradings furnish a second calibration.

### 3.2 Counts and gradings

Independent replay gives intersection matrices

`[[3]]` and `[[1,2],[1,3]]`.

The source arcs and circles are separately disjoint. The numbers of configuration generators are therefore their permanents, respectively 3 and 5. This is a geometric upper as well as lower bound, not a rank inferred from an Euler characteristic.

Exact monodromy replay gives the following `(A,Q,S)` triples, where `S` is the set of canonical coordinates:

- Two strands: `(0,1,∅)`, `(1,1,∅)`, `(1,2,{1})`.
- Three strands: `(0,1,∅)`, `(1,1,∅)`, `(1,3,{1})`, `(2,3,{1})`, `(2,4,{1,2})`.

The right anchor path makes the prescribed exterior detour and has winding +1 around the nearby quantum puncture. Replacing it by a straight path would omit that winding and yield an incorrect canonical grading. The synchronized particle paths are checked for collisions; for two particles the square of their difference tracks the discriminant winding. The returned signs and monomials agree with the source polynomials.

Depending on whether braid words act on the left or right, the second sequential action can be named `σ₁σ₂` or `σ₂σ₁`. Either is related to the first unknot presentation by positive stabilization and, if needed, conjugation. The conclusion here is failure under Markov equivalence of knot presentations. It does not depend on silently choosing a word-composition convention.

Every `(A,Q)` occurs once. The quantum differential preserves both gradings and lowers Maslov degree, so it is zero. Its homology dimensions are consequently 3 and 5. Merely coarsening to the Jones grading cannot change those underlying dimensions, proving that this coarsened quantum braid homology is not a knot invariant.

### 3.3 Rees arrows forced by ordinary knot Floer theory

Both closures are unknots. Ordinary hat knot Floer homology has one generator in Alexander degree zero and none in the nonzero Alexander degrees. Every nonzero-A block in the computed diagrams has exactly two generators, so its ordinary differential must be a nonzero arrow. The source positivity of the two Rees exponents determines the direction uniquely.

Using

`W=Σ_(i∈S)(3(n−i)+1)`, `R=Σ_(i∈S)(n−i)`,

`B=Q−W+R`, `C=R−W`,

the first complex has one arrow `V`. The second has one arrow `V` in A=2 and one arrow `UV³` in A=1. This is an exact deduction from verified generators, HFK of the unknot, Alexander preservation and coefficient positivity. It does not claim that a numerical simulation counted pseudoholomorphic discs.

Independent F₂ boundary-matrix calculations give:

- At `U=V=0`: dimensions `(3,5)`.
- At `U=0,V=1`: dimensions `(1,3)`.
- At `U=1,V=0`: dimensions `(3,5)`.
- At `U=V=1`: dimensions `(1,1)`.

Thus these two one-variable boundary specializations also fail to give a knot-invariant complex. Inverting both variables still has the PASS1 pure-gauge collapse. No conclusion about every other nonunit quotient, relative theory or modified differential follows.

## 4. Deliverables and limits

- `check_su2_calibration.py` / `SU2_CALIBRATION.json`: independent exact quantum normalization checks.
- `check_pd_k11n42.py` / `K11N42_REPLAY.txt`: independent PD bracket and Fox computation; copied source input kept separately.
- `PL_MARKOV_REPLAY.txt` / `PL_GRADING_REPLAY.json`: audited exact replay of the Floer report's geometric implementation.
- `check_floer_fibers.py` / `FLOER_FIBERS.json`: independent algebraic derivation and fiber-rank checks from the geometric rows.
- `MANIFEST.json`: output and dependency hashes, excluding copied source data from distribution.

The direct AU theorem is mathematically strengthened and no defect was found. The configuration and Floer conclusions are bounded obstructions with explicit counterexamples. None of these results justifies replacing the original qualitative problem by an unrestricted impossibility theorem, declaring novelty, or claiming what Roberts or subsequent authors regard as its final resolution.

## Primary references

- Andersen–Ueno, geometric vacua, flat bundles and sewing: https://arxiv.org/pdf/math/0306235v2
- Andersen–Ueno, structure-preserving CFT/WRT comparison: https://arxiv.org/pdf/1110.5027v2
- BHMV, colored splitting and torus basis, §§4.9–4.11: https://webhomes.maths.ed.ac.uk/~v1ranick/papers/bhmv.pdf
- Gilmer–Masbaum, extended weights and repeated-entry Maslov vanishing: https://arxiv.org/pdf/0912.4706v3
- Anghel–Juhász v4, source curves, quantum grading, Rees deformation and examples: https://arxiv.org/pdf/2601.08805v4
- Knot Atlas, explicit PD example: https://katlas.org/wiki/K11n42
- Knot Atlas, PD orientation convention: https://katlas.org/wiki/Planar_Diagrams
