# Metric rigidity at the boundary of cubic compactifications

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · Version 1.0, 6 October 2026 · CC BY 4.0

A sharp Cartier-index rigidity criterion for singular Kähler–Einstein Fanos and an explicitly attributed cubic metric compactification application in dimensions at least five.

## Original abstract

We deduce a sharp Cartier-index criterion for complex-structure rigidity on singular Kähler–Einstein Fano varieties. If −K_X = rL with L ample Cartier and r > dim(X)/2 + 1, then the tangent sheaf is stable and every parallel orthogonal complex structure on the regular locus equals the given one or its negative. The proof combines the decomposition theorem of Druel–Guenancia–Păun with a Hilbert-polynomial index bound and local positive-Ricci curvature. Applied to cubic n-fold limits, n ≥ 5, it identifies the ordinary metric Gromov–Hausdorff compactification with cubic GIT modulo conjugation, including the singular boundary. We also record the complex-preserving comparison as an attributed consequence of the unrestricted ordinary-double-point gap, Li–Liu's global Reeb minimum, and Spotti–Sun's established transfer. The complex algebraic comparison is already publicly stated in stronger form by Kong–Shen–Zhao–Zhao; no first-solution claim is made.

## The idea in plain English

A complex algebraic variety also has an underlying real geometric shape. Forgetting the complex structure can identify distinct algebraic varieties with the same metric. This note gives a criterion under which a positive Kähler–Einstein metric determines the complex structure up to conjugation, even when the variety is singular.

The criterion measures how divisible the anticanonical line bundle is by an actual ample Cartier line bundle. Above a strict dimension-dependent threshold, a finite cover cannot split into two positive-dimensional factors. The remaining complex structure is forced to have one global sign.

For cubic hypersurfaces of dimension at least five, the paper applies this criterion to the entire singular boundary of the Kähler–Einstein compactification. Once the stated external normalized-volume gap and established transfer are accepted, two boundary cubics have the same underlying metric exactly when their complex points agree up to conjugation.

The complex cubic comparison is already prior public work, including a stronger result of Kong, Shen, Zhao and Zhao. The additional deductions here are the singular Cartier-index criterion and the argument identifying the metric fibers; first priority is not certified.

## The precise result

Theorem 1 concerns an irreducible normal projective complex klt Fano variety X of dimension m≥1 carrying a positive weak Kähler–Einstein current with bounded potentials, smooth on X_reg. Let L be ample Cartier and let the positive integer r satisfy the actual line-bundle identity ω_X^[−1]≅L^⊗r. If r>m/2+1, then T_X and the tangent sheaf of every irreducible normal finite quasi-étale cover are slope stable for the anticanonical polarization. No such cover is a product of two positive-dimensional normal projective varieties. Every parallel orthogonal complex structure I on (X_reg,g) equals J or −J.

The strict threshold is sharp in this general class: P^(r−1)×P^(r−1), with L=O(1,1) and its equally normalized product Kähler–Einstein metric, has m=2r−2 and admits mixed factor conjugation. This is a general-Fano equality example, not an example among cubic fourfolds.

For n≥5, set G_n=P(H⁰(P^(n+1),O(3)))//SL(n+2), and let σ be coefficientwise complex conjugation. Theorem 2, using the cited unrestricted OpenAI upper-gap theorem in every dimension 2≤k≤n, identifies the complex/polarized Gromov–Hausdorff compactification of smooth Kähler–Einstein cubic n-folds with G_n(ℂ), and the ordinary metric Gromov–Hausdorff compactification with G_n(ℂ)/⟨σ⟩. The closed-point interpretation is the cubic Q-Gorenstein smoothing locus in smoothable K-polystable coarse moduli.

Every metric isometry between the actual Kähler–Einstein cubic boundary varieties is holomorphic or antiholomorphic, including across their singular loci. In the antiholomorphic case it is holomorphic to the conjugate variety. In this formulation the cubic hyperplane Cartier line bundle is preserved, and all fibers of forgetting complex structure are precisely conjugation orbits.

## Why the result holds

Druel–Guenancia–Păun supply a finite quasi-étale product cover with stable tangent factors. Restricting the genuine Cartier root to each factor, klt Kawamata–Viehweg vanishing gives the r−1 negative integer roots of its Euler-characteristic polynomial. A factor therefore has dimension at least r−1; two factors contradict m<2(r−1). Stability descends through the finite étale big open set and holds on every finite quasi-étale cover.

Local positive-Ricci curvature kills the parallel (2,0) part of g(I·,·), so I commutes with J. Reflexive extension, GAGA and stable-sheaf simplicity then force the single global sign I=±J. This local argument does not require completeness of the regular locus.

The cubic dependency chain is explicit: the external upper bound vol̂(x,X)≤2(k−1)^k for all 2≤k≤n → Li–Liu’s global minimum over all centered real valuations and the identity vol̂(v_ξ)=k^kΘ(C) → the smooth-link singular-cone bound Θ(C)≤2(1−1/k)^k → Spotti–Sun’s iterated-cone and Cartier-root theorem → −K_Z=(n−1)L_Z with L_Z Cartier and L_Z^n=3 → Fujita’s degree-three classification, positive CM polarization and Spotti–Sun’s moduli continuity transfer → the complex/polarized GH/GIT homeomorphism. Proposition 3 and Corollary 4 state the intermediate implications conditionally on the upper gap. Only the gap’s upper bound is used, not its equality classification.

The strict transfer estimate is (1/2)b_n(n+1)^n=(n−1)^n(1+1/n)^n<3(n−1)^n, with b_n=2(1−1/n)^n. The actual Cartier root and the cubic smoothing locus are essential. Li–Liu is applied to the smooth-link case with its canonical-form hypotheses; Spotti–Sun’s iteration handles other singular links.

On the actual cubic GH limits, Donaldson–Sun identify the metric and analytic regular loci. The Cartier criterion fixes the sign there; continuity and normal extension carry the isometry across the singularities. Singular complete-intersection Picard Lefschetz recovers the hyperplane bundle. Polarized compactness and a compact-to-Hausdorff quotient argument finish the ordinary metric comparison.

## Scope and limitations

The general criterion requires a genuine ample Cartier root, a positive Einstein constant, the stated bounded-potential weak metric and the strict inequality r>m/2+1. A merely Q-Cartier divisor or a Ricci-flat analogue is outside its scope.

The cubic compactification application is a deduction at the declared external-theorem level. The pinned unrestricted OpenAI ordinary-double-point upper-gap preprint and its sole dimension-four companion are principal external inputs whose complete proofs are not freshly recertified here. Fujita’s required classification statement and hypotheses are used as an external theorem; its full chapter proof has not been accessed. The general Cartier-index criterion itself does not require the upper-gap theorem.

The metric-isometry application concerns actual polarized GH limits of smooth Kähler–Einstein cubics, for n≥5. It does not classify arbitrary metric completions of nonsmoothable weak Kähler–Einstein varieties. The general sharpness example neither proves nor disproves the cubic-fourfold assertion.

The comparison stated here is topological and concerns the specified smoothable closed points. No scheme or stack equivalence, moduli-functor equivalence, assertion about every nonclosed semistable orbit, effective GH-distance estimate or modulus of continuity is claimed.

The complex cubic K/GIT comparison, smooth tangent stability, smooth metric rigidity, decomposition and conjugation convention retain their prior attribution. No first-solution, first-disclosure, exhaustive worldwide novelty or current global open-status claim is made. Finite arithmetic checks do not prove the geometric source theorems.

## Status and AI use

AI tools were used extensively in research, derivation, drafting and verification. Internal AI-assisted reviews are not independent human or journal peer review. This is an unrefereed preprint without formal proof-assistant certification, including no formal certification of the upstream gap. The named author is responsible for its claims and citations.

The manuscript and Zenodo’s declared publication date are 6 October 2026, version 1.0. Zenodo created the record on 7 October 2026 UTC. These edition dates do not establish historical priority.

## Read the paper

Read the complete 8-page paper in the on-page PDF reader.

[Open the PDF](https://aleckriebel.com/research/metric-rigidity-cubic-compactifications/paper.pdf)

[Download the PDF](https://aleckriebel.com/research/metric-rigidity-cubic-compactifications/paper.pdf) (download)

[Download the Zenodo original PDF](https://zenodo.org/records/23204952/files/paper.pdf) (download)

On-page PDF reader: [Metric rigidity at the boundary of cubic compactifications — complete paper PDF](https://aleckriebel.com/research/metric-rigidity-cubic-compactifications/paper.pdf)

## Supporting materials

[Complete source and verification materials (ZIP)](https://aleckriebel.com/research/metric-rigidity-cubic-compactifications/source-and-verification.zip) (download)

[Zenodo original ZIP](https://zenodo.org/records/23204952/files/source-and-verification.zip)

## Collaborate on this result

Substantive collaboration on independent verification of the singular rigidity argument, a meaningful mathematical extension, or development toward journal submission is welcome. Authorship and responsibilities would reflect actual research and writing contributions and mutual agreement.

## Cite this paper

Kriebel, Alec. (2026). Metric rigidity at the boundary of cubic compactifications (Version 1.0, 6 October 2026). Zenodo. 10.5281/zenodo.23204952.

[10.5281/zenodo.23204952](https://doi.org/10.5281/zenodo.23204952)

```bibtex
@misc{kriebel2026_23204952,
  author = {Kriebel, Alec},
  title = {Metric rigidity at the boundary of cubic compactifications},
  year = {2026},
  month = oct,
  doi = {10.5281/zenodo.23204952},
  url = {https://aleckriebel.com/research/metric-rigidity-cubic-compactifications/},
  version = {1.0},
  publisher = {Zenodo},
  note = {Unrefereed preprint; version 1.0, dated 6 October 2026. Zenodo record created 7 October 2026 UTC. Prepared with extensive AI assistance.}
}
```

## Background and prior work

[Druel, Guenancia and Păun, A decomposition theorem for Q-Fano Kähler–Einstein varieties](https://doi.org/10.5802/crmath.612). Established singular Kähler–Einstein stable-factor product cover, with the bounded-potential and quasi-étale pullback hypotheses used here.

[OpenAI, The ordinary-double-point gap in every dimension](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/paper.pdf). Principal external unrestricted upper-gap preprint; its sole companion is The normalized-volume gap in dimension four. These complete proofs are not independently recertified by this note.

[Li and Liu, Kähler–Einstein metrics and volume minimization](https://arxiv.org/abs/1602.05094v3). The established global Reeb minimum over all centered valuations, including the irregular case, and the density normalization.

[Spotti and Sun, Explicit Gromov–Hausdorff compactifications of moduli spaces of Kähler–Einstein Fano manifolds](https://arxiv.org/abs/1705.00377v1). Established gap-to-cubic transfer, singular-cone iteration, limiting Cartier root and moduli continuity.

[Fujita, On singular del Pezzo varieties](https://doi.org/10.1007/BFb0083337). The degree-three Gorenstein classification. The required definition and statements were checked in the available original preview; the full chapter proof remains an external input.

[Kong, Shen, Zhao and Zhao, K-moduli of cubic hypersurfaces](https://drive.google.com/file/d/1eB16wLGE2G5QrbV-pUDmw_ieLMiLlOcO/view). Prior public manuscript stating a stronger complex algebraic comparison, including stacks and good moduli spaces. Earliest public posting and the full separate proof are not certified here.

[Donaldson and Sun, Gromov–Hausdorff limits of Kähler manifolds and algebraic geometry, II](https://arxiv.org/abs/1507.05082v1). The regular-locus identification and normal extension interface for actual GH limits.

[Grothendieck, SGA 2, corrected edition](https://arxiv.org/abs/math/0511279). Exposé XII, Corollary 3.7 supplies Picard Lefschetz for global projective complete intersections, including singular ones.

[Li, Wang and Xu, On the proper moduli spaces of smoothable Kähler–Einstein Fano varieties](https://arxiv.org/abs/1411.0761v4). The smoothable K-polystable closed-point interpretation; equal dimension and volume alone do not specify the cubic smoothing locus.

[Peternell and Wiśniewski, On stability of tangent bundles of Fano manifolds with b₂=1](https://arxiv.org/abs/alg-geom/9306010v2). Prior smooth complete-intersection tangent stability.

[Spotti, Degenerations of Kähler–Einstein Fano manifolds](https://arxiv.org/abs/1211.5334). Prior smooth positive-KE splitting and rigidity up to factorwise conjugation.

[Odaka, Spotti and Sun, Compact moduli spaces of del Pezzo surfaces and Kähler–Einstein metrics](https://arxiv.org/abs/1210.0858). Prior singular del Pezzo compactifications and ordinary metric quotient by conjugation; lower-dimensional cubic comparisons are further credited in the manuscript.
