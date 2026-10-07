# Fresh analytic/category/exact-KS dependency review of V3

Checkpoint: 2026-10-07 05:25 UTC (2026-10-06 22:25 PDT). Best-guess completion: **100% of this assigned source-proof audit**. This does not estimate global Hodge-conjecture resolution or publication readiness.

## Verdict and exact scope

**No substantive mathematical gap was exposed in the assigned analytic/category/exact-KS slice of the pinned October 4 mixed-K3 proof.** The relative interior-root construction meets its ordinary-output, neighborhood, collar, and CF-extension obligations. Stokes removes curvature without assuming a bounding cochain. Finite comparisons and copy reconstruction yield the full ordinary mirror subcategory, and saturation plus Serre duality yields the asserted perfect complex as a summand. Sharp cap rank identifies the exact transcendental tensor and makes the full semiregularity trace injective. Deformation, specialization, and the standard-KS conversion have the stated hypotheses.

This is affirmative source-level verification **relative to the accepted foundations listed below**. It is not a formal verification, a reconstruction of every foundational PDE theorem, or a numerical computation of Floer moduli spaces. It is a scoped slice for the parent complete-package review; it does not approve the CM/mixed-group assembly, Bülles theorem, priority, deposit metadata, or final PDF.

I read the original human request at `/Users/alec/.codex/attachments/236d83ea-ee16-4344-9bf8-fb179081c720/Pasted text.txt` and AGENTS.md, then the actual eight proof files before any prior audit. A narrower fresh KS child was attempted, but the concurrency limit prevented it. No additional fresh subreview is claimed. No individual was contacted, and no Git, publication, tracker, upstream, or frozen-package mutation occurred. Only this report and assigned scratch checks were written. The parent retained unchanged copies of those checks under `checks/review3_checks/analytic/`.

## Exact source identity

The proof base is

`sources/pinned/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/build/manuscript/`

at public snapshot `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. I read topology, curvature, comparison, realization, cohomology, setup, exactks, and auxiliary in full, including the parametric product/sign proof. I subsequently read the current note, D2 ledger section, publication README/VALIDATION, and the reconciled reports below. The V3 note's source hash is `f9566f03e925bc2cff721fc80d231276733a4540d27450589da98df6c229cfe8`; the note was checked here for this dependency slice.

| File | SHA-256 |
| --- | --- |
| topology.tex | 153d29eed2f02aa956ac8898dbf01fd5b13c4e4e69999a5f67bdbf501d921864 |
| curvature.tex | 5eb8d9656ceeab8aa4dfdceb10566b61ed9d44a23113188ceae11c39dc880f49 |
| comparison.tex | f6e817648b5866991cff23b7e90643c00d8924f85f8d5e0128643f90ae148be2 |
| realization.tex | 338c65d26d9cade6acffc202127697f51af84853a19a2506daf1489080f9ef8d |
| cohomology.tex | a1d4ec1325dcb9a4e618476e96927b2ba3396ba519547842e6f223f6db066e92 |
| setup.tex | f5d66939d1eea98d1d2172f0c73746d32bd60f313cae0373879d091a1632e850 |
| exactks.tex | a9a7aeaebd251e193e4790dc650504386404c13fb3fa91cadcad73ffc3b1fd87 |
| auxiliary.tex | f22972ef19438c508be5fd929b3ef3c58c9f932b617c3f03bde09bc4f1b9935d |

## Accepted standard foundations and matching hypotheses

These are external mathematical inputs, not gaps concealed as “standard.”

- Accept rational spin tangential Pontryagin–Thom/Thom realization, DGMS compact-Kähler formality, surgery over the specified polycyclic target/Noetherian group ring, Gromov–Lees for a formal Lagrangian monomorphism with zero pulled-back symplectic class, the relative subcritical contact isotropic h-principle and neighborhood theorem, EEMS stabilization traces, and Eliashberg–Murphy's exact loose-end cancellation. The pinned topology supplies the spin/determinant data, high dimension, chosen zero-area classes, exact simply connected target, loose negative end, and zero signed count.
- Accept [Akaho–Joyce §§4–5](https://people.maths.ox.ac.uk/joyce/AkahoJoyce.pdf) for immersed fixed-jump Fredholm/gluing and spin caps, and the corrected FOOO disk charts/exponential gluing cited at curvature:63–88. I freshly inspected [AFOOO v1](https://arxiv.org/abs/2606.12257v1) Theorems 9.3/9.6, Propositions 14.5/14.8 and 16.3/16.14, and [Charts II §8](https://arxiv.org/html/1808.06106v2#S8). AFOOO supplies the finite curved cyclic category, homotopy units, prescribed-neighborhood CF extension after collaring, and mixed interior/ordinary data. Unobstructedness and the root-to-point adaptation require the manuscript's additional proof, checked below.
- Accept the enhanced generating construction in [Seidel's quartic theorem v4](https://arxiv.org/pdf/math/0310414v4) and the finite faithful functor of [Abouzaid, Theorem 2.10/Appendix A](https://ems.press/content/serial-article-files/32222). Exact primary hypotheses were read in the saved primary texts. Quartic graded rational spheres and finite tautologically unobstructed torus graphs meet them. Torus fullness and uniform generation are additional source arguments, not consequences automatically attributed to faithfulness.
- Accept Todd-modified HKR/cap compatibility, boundary–bulk/Atiyah–Chern trace factorization, and rational Clifford representation theory. I freshly checked [Pridham Corollary 2.25 and Remark 2.27](https://arxiv.org/html/1208.3111): the latter's smooth-proper Hodge-degeneration retraction supplies the passage from the truncated de Rham obstruction image to individual trace components.
- Fresh reads of [Stacks 0DIG](https://stacks.math.columbia.edu/tag/0DIG) and [0DJZ](https://stacks.math.columbia.edu/tag/0DJZ) confirm the compatible pseudocoherent-tower and relative-perfectness hypotheses. Accept proper GAGA, finite-presentation descent, proper Hilbert parameters/countability, period/arithmetic quotient algebraicity, Buskin's rational K3 Hodge-isometry theorem, and algebraicity of abelian Hodge homomorphisms, polarizations/Lefschetz inverses/Künneth projectors. The proof supplies actual smooth proper/regular families and parallel tensors.

No full proof of those foundational results was reconstructed. Their applications and the new relative constructions were checked; their names alone were not treated as evidence for unobstructedness or the Hodge conjecture.

## 1. Topology and energy

The current exact-KS construction uses **g=2^19**, hence **n=524290** with the quartic. This is not the n=514 construction in the October 3 companion. It meets g even, n≥12, the surgery stable ranges, 2+2<2n, and 2+n<2n.

The torus-bundle model's H² horizontal quotient is H²(D)/Z. The H¹(D)⊗u differential is injective by the stipulated wedge hypothesis; independence of z_j makes the Λ²u differential injective, and their vertical degrees prevent cancellation. The Spin→SU pullback adds no degree-two generator. Its surviving odd-Chern differentials vanish for TD consisting of a K3 tangent bundle and trivial torus bundle. The horizontal functional pairing with a is closed since z_j a=0, so a's dual class lifts before bordism/surgery.

The target π₁ is polycyclic: a quotient of the torus-fiber Z^r extends π₁(D)=Z^(2g), and the second pullback has two-connected fiber. Circle/two-sphere surgeries over that target preserve the spin tangential data and give the stated H² description. Extra null-image circles and S⁴×S^(n−4) summands preserve it while controlling actions and Euler characteristic. The homology injection is the explicit projection-formula deduction

f_*(f* x ∩ [L]) = ν PD^−1(xa).

Vanishing means x∈Z, hence f* x=0. This is the exact topological premise later used in curvature removal.

The local exact-domain mechanism retains **chosen zero-area filling classes**; it does not posit a filling-independent action in the K3 target with nonzero π₂. Adjustable source-null loops and local exact sheet perturbations achieve zero chosen areas. The image graph loops are killed by exterior isotropic disks avoiding the source. Zero area permits the required horizontal prequantization lifts with zero winding. The source preimage remains a disk while the target becomes contractible. Its punctured completion has the exact, cylindrical, simply connected, loose negative-end cancellation data. Disk replacement there preserves the pushed class and low (co)homology. The resulting double sign gives odd ordered branch degrees.

The energy lemma does not assume the full period group is discrete. For the finite sheet union K, relative forms vanishing near K have comass bounds on J₀-holomorphic polygons. Bounded area bounds every coordinate in the integral relative homology lattice modulo torsion. Only finitely many energy values lie below a cutoff, independently of markings. Thus there is a positive nonconstant gap δ and a locally finite additive monoid.

## 2. Relative roots, ordinary outputs, and corners

For a tree with its distinguished interior-mark vertex, every other vertex's output is the edge along the unique path to that mark. Cutting in any order or contracting a connected subtree retains that output and the same root type. External cyclic relabeling does not reroot an ordinary child, even when its external labels cross the numbering seam. No input-cyclic condition on a fixed child has been introduced.

Reciprocal internal flags remain when the external word is empty. Diagonal matches are over L; reciprocal matches are over the fixed double-value point. They are composed before using degree vanishing. Constant ordinary bivalent disks have zero or two switches and contract through the existing ordered cap duality. Constant interior roots with a boundary flag are stable; the one-input diagonal constant is the regular space L. Stable constant switching roots use the fixed-jump local operator with the interior-mark coordinate, without an incidence mark transverse to a constant map. The unstable zero-input constant root is excluded. There is no interior-evaluation submersion requirement.

Augmented matching is solved recursively toward the leaves. At each diagonal edge, the child's output evaluation can be prescribed; induced changes at its input flags are then corrected farther down the tree. Joint submersivity of all evaluations on one parent is unnecessary. A switch adds no positive-dimensional matching equation.

The manuscript supplies more than tree equality. On a broken tree the quasi-component indices are the union of inherited lower root indices and fixed ordinary indices. Under partial smoothing a subtree contains the mark or has one ordinary outgoing flag; the persistence used in Charts II's openness/properness proof is therefore preserved. New compact-core spaces are added off a smaller prescribed neighborhood and saturated under finite groups. Direct sums and surjectivity persist after shrinking. Properness gives obstruction-space inclusions/semicontinuity; inclusions compose and admissible auxiliary forgetting commutes with normalization. This gives chart/coordinate-change compatibility on higher corners.

Charts II's boundary-output clause remains on ordinary children. The parent needs augmented regularity and integration to a point instead. The proof specifies that adaptation rather than literally applying an output-evaluation theorem to a root without output.

Compatible corner CF products are **outer-collared first**. A closed smaller collar is then the compact set in AFOOO Proposition 14.5; f maps to a point. Its neighborhood/transversality hypotheses hold, and compatible thickening preserves the prescribed collar integrations and ordinary child counts. Finite equivariance uses auxiliary parameter representations, not averaging single-valued transverse sections. Stabilizer weights remain.

Costs are E+ε(k−1) for ordinary vertices and E+εk for roots, with 0<ε<δ. At a split r+s=k,

[E_P+ε(r+1)] + [E_Q+ε(s−1)] = E_total+εk.

Each genuine factor is positive: nonconstant ordinary zero-input cost≥δ−ε; zero-energy ordinary stable vertices have at least two inputs; a constant one-input root costs ε. The zero-energy unary strip is the fixed de Rham differential. Thus factors have lower cost, while arity controls constant switching polygons. The finite induction closes under faces. No missing rerooting, matching, neighborhood, collar, or constant-switch condition was identified.

## 3. Stokes and curvature removal

With k diagonal degree-one inputs, virtual dimension is n+k−1 and η∧b^k has degree n+k−2. Stokes applies at one below top degree. No nonconstant spheres exist; a constant sphere tree with at most one interior mark and one attachment cannot be stable. Boundary collapse would retain a nonconstant sphere.

At k=0 each boundary product has a root with one input and an ordinary curvature child. Composition gives p₁^η(m₀), including switches. Only afterward does degree two rule out odd branch-sector curvature. The regular zero-energy diagonal root gives the fixed nonzero-sign pairing ∫_L c∧i*η.

For positive degree-one b, suspended input degrees are zero. Normalized labeled strata give k child positions for s=0 (gaps), 0<s<k (block starts), and s=k (attaching/rooted orders). External cyclic labels are not quotiented out. Insertion signs are positive, including point sectors. Input differentials give the de Rham part of m₁. Dividing by k, adding the separate k=0 identity, and summing yields

Σ_(r≥0) p_(r+1)^η(m₀^b,b,…,b)=0.

The first curvature coefficient is a closed two-form; only the zero-energy single-input pairing survives at that valuation. The ambient homology injection and Poincaré duality make its class zero. Canonical transfer has positive F₀ and cohomology-isomorphic leading F₁. A first nonzero canonical curvature class would transfer to a nonexact leading form, contradiction. Finite-cutoff promotion gives the same argument without comparing all root functionals across pseudo-isotopies. The degree-two canonical space is H²(L), proving the bound without circularly assuming unobstructedness.

## 4. Comparison and categorical completion

Hamiltonian data keep chords fixed, vanish near intersections, have pure strip necks, and exponentially approach component core data. Forcing disappears at bubble scale. A stable constant strict-word polygon would require a forbidden triple intersection. Domain-dependent core variations give polygon regularity without a simple-map assumption; strips use the corrected regular-point argument.

The path comparison specifies augmented surjectivity, core obstruction transports, spectral gaps, weighted parametrices, small cutoff/seam errors, Neumann correction, and uniform quadratic estimates. Strip-core marks are retained when contracting multiple breaks. Exponential domain coordinates are not incorrectly equated with inverse-length Kuranishi coordinates. Relative integration reaches the actual ordinary count at its regular endpoint.

The domain-chain proof handles one parameter smoothing several nodes through λ_i(t,y)=t c_i(t,y), c_i>0. Nodal regularity includes y. Gluing coverage gives the oriented end for t>0, without a false smoothness claim at t=0 in exponential coordinates. Internal strip breaks cancel, external ones give the differential, and removed ignored factors are included in the regularity requirements. The inward prism contracts each operad arity. The sign normalization gives dg-operad identities and the finite-arity homotopy identifies the split product with the factor tensor product.

Finite strict systems have bounded arity and Hom ranks. Functor/inverse-linear equations are a finite polynomial system. Arbitrarily accurate valuation solutions with nonnegative coordinates contradict a fixed Nullstellensatz unit-ideal identity if no algebraic solution exists. The actual field-extension comparison is therefore justified; no infinite-system compactness is asserted.

Ordinary quartic spheres are graded/rational and admit the stated common disk/sphere-free J₀; Seidel's enhanced generating model and copy invariance apply. Additional pencil cycles span the primitive 21-space. Euler Gram forms and the nonconstant mirror period give a 21-dimensional algebraic Mukai space and make relations descend.

For torus graphs, base and total π₂ vanish, the graph π₁ map is injective, and spin/grade requirements hold. Section/frame trivializations remove gerbe twists. One graph–fiber intersection gives the rank-one local module; the multiplier −εMb and signed rank-one matrix decomposition give the theta numerical class. Faithfulness plus |det(M−M')| dimension equality gives fullness for definite pairs. Same-slope copies have identical lines, since nontrivial Picard-zero quotients would contradict faithfulness. Three slopes force common shifts. Relative Serre sequences over proper Picard-zero parameter spaces give uniform powers; length g+1 and Ext^(g+1)=0 split off a vector-bundle generator. No unsupported blanket torus HMS is used.

Three distinct copies give invertible degree-zero arrows via nonzero ordered triple products, associativity, self-Hom⁰ dimension≤1, and units. Canonical ranks/degrees bound each fixed Hom in the finite exhaustion. Fixed A∞/functor/unit/pairing/inverse equations are finite and pass to the field ultraproduct. Its countable cardinal bound allows an abstract C embedding, which need not fix a previously named coefficient C. The proof uses abstract scalar extension, not evaluation of Novikov series.

Cofinal later copies give Yoneda telescopes. Eventually strict arrows identify each evaluation with the full representable; derived maps form a homotopy limit of equivalences. Thus full enhanced self-Homs are recovered. Factor external generators generate Perf(B×E^g).

Saturation represents the proper restricted module Hom(−,L)|_A by E. Its cone is right orthogonal; ambient Serre shift [n] makes it left orthogonal. The triangle splits, so Ext²(E,E) is a direct block of Hom²(L,L). **Saturation alone would not suffice.** Transverse Floer Euler characteristic gives one common nonzero rational normalization of intersection with νa; some individual pairings may vanish.

## 5. Exact cap rank, KS normalization, and deformation

The actual cap calculation uses Todd-modified HKR directly on the mirror, without assuming cohomological HMS. K3 HH¹=0 removes cross terms. HH² has dimension 22+binom(2g,2)=b₂(D). Normalization changes are invertible row/column scalings.

The full cap action factors HH²→Ext²→HH_(−2) by boundary–bulk/Atiyah traces, not merely the determinant trace into H²(O). If the cap kernel equals dim Z, its rank equals b₂(D)−dim Z, the upper bound on the middle-space dimension. Consequently the full trace is injective. Strict inequality would not suffice.

The formal tensor's powers 4,7,10 separate all nine operator degrees from degree two. Lefschetz injectivity forces λ=π=0 and preservation of three alternating tensors. Two relative operators kill multiplicity freedom. The full Clifford commutant makes an x=0 kernel scalar, and its highest-weight-two lowering equation kills that scalar. Spin lowering supplies every x∈N⊕Qt₀; hence dim Z=19. Injective projection to H²(Y) gives the H¹-wedge hypothesis.

For the actual tensor, kernel dimension≥19 leaves ≥16 dimensions after x_e=0. Zero transcendental component would leave only scalar L and x₀, contradiction. Its nonzero component embeds the simple three-dimensional K3 structure into tensors of non-CM elliptic H; the only three-dimensional irreducible is Sym²H. The similarity multiplier is a rational square by determinants in odd dimension and positive by signatures, giving a rational Hodge isometry.

The x_N image has dimension≥14, exceeding maximal isotropic dimension 9; choose nonisotropic x_N. The commutant of its 17 perpendicular Clifford directions is span{1,ΔΓ_x}; relative operators remove multiplicity freedom. The nonzero commutator [ΔΓ_x,Γ_y]=κq(x,y)Δ makes the lowest component c times the formal one. Equivariance gives the same c in all three components. The t_− equation then gives c²=1 modulo the line U₀ because J(x_N) lies outside it. Changing the isometry's sign gives **C=C_***. Thus actual/formal kernels both have dimension 19 and semiregularity is injective. Euler tests alone were not used to determine this component.

For the auxiliary tensor the totally real Galois, d'≥5, d'≡5 mod 8, all-real-signature, and Witt-index≥2 hypotheses are explicit. Powers 6,9,12 force λ=π=0. The first relative copy operator gives block diagonality; the second's nonzero off-diagonals force four identical blocks. Projecting H¹ from one copy against H² on another gives wedge injection. Torus Euler tests determine the whole class; conjugate weight decompositions give sharp cap rank. Parallel spin invariance and degree extraction yield exactly the four-slot tensor.

At each Artin small extension I is annihilated by the maximal ideal, so central Ext²⊗I is the obstruction space. The horizontal-Hodge condition plus smooth proper degeneration/Pridham's retraction kills each trace, and injectivity kills the obstruction. Compatible perfect lifts have uniform finite Tor amplitude. Proper flat finite presentation, perfect central restriction, and regular completed base give the cited effectivity hypotheses. Finite-presentation descent is dominant because the smooth local ring injects into its completion.

Every-fiber algebraicity is obtained from actual cycles on a dense open, then countably many proper relative Hilbert parameters for rational cycle expressions. Connected parameter components retain the prescribed global parallel class. Closed images covering an open force one image to equal the complex irreducible base. This is not an inference from density alone.

In the full primitive family, h,H⁰,H⁴ and spin-invariant terms remain parallel Hodge. Algebraic degree/projector/polarization operations remove auxiliary powers and extract J. Central volume gives L_(vz)=L_vR_z; postcomposition by right even z^−1w yields the exact map x↦vxw. Those even right operators are abelian Hodge endomorphisms and algebraic.

Rank-19 indefinite NS supplies a rational hyperbolic plane and rational ample classes of every desired positive squareclass. Witt comparison, very-general wall avoidance, Buskin, and induced abelian isogenies transport the **exact** tensor across degrees. Specialization retains the entire prescribed parallel primitive class at Picard jumps. Algebraic projection to T(S), splitting C⁺(T(S)) as a polarizable weight-one substructure, and isogeny/polarization conversions cover every nonisotropic w and chosen rational polarization. Rank-two/CM transcendental cases arise by specialization/restriction, not by assuming they satisfy the initial rank-three mirror argument.

## 6. Fresh checkable evidence

The retained unchanged script `checks/review3_checks/analytic/check_identities.py` and `identity_results.json` originated under `checks/package_review_3/analytic/`. They passed using only Python's standard library:

- 701 rooted labeled trees through five vertices, 15,405 normalization orders, and 164,249 cut/sector cases.
- 2,176 additive cost/stable lower-factor checks.
- 32 determinant permutation parities, 3,600 count-normalization pairs, and 119 boundary normalization checks.
- Exact rational Clifford matrices in dimensions 2,4,6: full commutant dimension one, coordinate-perpendicular commutant dimension two, and the ΔΓ commutator identity.
- A strict-rank boundary example: composite rank one through a middle space of dimension two does not force trace injectivity.

These check finite displayed identities and combinations, not Kuranishi existence, nonlinear gluing, analytical cyclic weights, the enormous actual spin representation, or a Hodge theorem. The dimension-18 claim rests on the general Clifford restriction argument, not extrapolation from small matrices. Source hashes are recorded in the result JSON.

The upstream Lean declarations were inspected. They cover rational sandwich membership/injectivity, right-factor changes, even-Clifford transport, and tensor conversion/compression. They contain no varieties, Hodge structures, Chow groups, Floer construction, or geometric KS algebraicity. No Lean build is relied on.

## 7. Reconciliation and strongest result

The earlier `reviews/analytic_falsification.md` and corner subreview positively validate the relative construction but exclude topology/HMS/semiregularity. This fresh direct review agrees and checks those current-source interfaces. `reviews/ordinary_hms_verifier.md` is supported by the exact primary hypotheses and the source's added fullness/generation proof.

`agent_notes/realization_audit.md` first had broad analytic caveats, then an affirmative relative-extension pass. Its earlier coverage caveat is not a contrary defect. This fresh review also reads the complete Hamiltonian/product comparison outside that targeted pass.

`agent_notes/ks_geometry_audit.md` chiefly reviews the **October 3 companion**, with n=514, and then records its outstanding analytic validation premises. Those constants/labels must not be transplanted to the current mixed proof with n=524290. The current exact-KS and semiregularity proof was checked directly here; this closes the assigned current-source review coverage, without pretending to re-prove the entire older companion. `agent_notes/root_cm_and_deformation_audit.md` gives conditional propagation; the present slice additionally checks its pivotal realization/rank premises in the current proof. CM remains separately assigned.

The frozen D2 ledger and note accurately expose the base theorem and distinguish unformalized audits from formal certificates. No correction to frozen V3 was found necessary in this slice.

**Strongest verified result:** relative to the explicitly accepted foundations, the pinned mixed manuscript supplies its controlled-Ext perfect complex and Euler data, identifies the exact full-Clifford KS tensor by sharp rank, and transports that actual algebraic class through its stated families and slot conversions. No additional unsupported lemma or counterexample remains identified in this assigned slice. Complete-package acceptance remains the parent review's responsibility.
