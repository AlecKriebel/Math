# Smooth, complex, and symplectic isotopy of curves in the four-ball

## Result and scope

**KP-4.104 / 2980: unresolved in this report. Five distinct mathematical approaches were carried out; none proves the requested example, its impossibility, or the infinite-family assertion.** This is a rigorous partial report, not a solution or a novelty claim. The useful outputs are an explicit global-conjugation cancellation in a tempting braid example, an obstruction to recycling the known infinite annulus family, and precise limitations on three geometric constructions.

The target is the 2026 K3 problem on pp. 277–278 [K3]. In paraphrase: find nonsingular complex curves properly embedded in the standard ball in complex dimension two, having boundary in one transverse link type in the standard contact three-sphere, that belong to one smooth isotopy class but to different complex isotopy classes; ask the stronger separation by symplectic isotopy as well, and ask for infinitely many examples in one smooth class.

The ambient form is the standard real symplectic form on the ball, not a holomorphic symplectic form, a varying symplectic form, a closed K3 surface, or an arbitrary Stein surface. The letter K3 in the source title names the problem collection. All fillings considered here are smooth embedded surfaces; allowing singular members of an isotopy would change the equivalence relation. Complex isotopy means a family of complex curves for the standard complex structure. Symplectic isotopy means a family of embedded surfaces symplectic for the fixed ambient form. Thus complex isotopy implies symplectic isotopy, which implies smooth isotopy. The converses are the issue.

### Boundary conventions

The source writes that a single transverse link bounds the curves, but does not impose a full list of parametrizations, collar germs, or labels. Its quasipositive-braid discussion and the primary annulus construction [BVHM, abstract and Theorem 10] use the same **transverse link type**, with boundary representatives allowed to be transversely isotopic. We use that unmarked convention for the target. We do not identify it without proof with a problem fixing a particular analytic boundary point set and its entire collar.

When a lemma below uses a stationary collar, that is an explicit stronger hypothesis. When capping is used, the line is a distinguished component and the intersection points are treated with the labeling conventions in [GS, §5]. Non-equivalence with extra markings does not establish non-equivalence after forgetting them. Conversely, forgetting labels can discard precisely the invariant one hoped to use.

## Source and current-literature audit

Checked on 2026-10-08. The authoritative target was read in the actual April 2026 author-hosted K3 PDF, whose metadata and hash are recorded separately. An older AIM problem-list URL is not used as a substitute for this text.

The following primary material was inspected before the approaches:

- [BVHM], Theorem B/10 and its proof: infinitely many complex analytic annuli have one transverse boundary type, but their double branched covers have different first homology. They are not smoothly isotopic. The annulus subfamily uses odd parameters; even parameters give a disconnected surface.
- [Hay], Theorem A: complex-realizable pairs are topologically isotopic but not ambiently diffeomorphic. This is the wrong side of the smooth-isotopy requirement. The currently served arXiv record is v2, dated 2021-03-23; no later version was inferred from a recent crawl date.
- [CG], introduction and Corollaries 1.5–1.6: infinitely many smoothly isotopic exact Lagrangian fillings can be separated by Hamiltonian-isotopy invariants. A Lagrangian surface is not a symplectic surface. Section 4 below explains why the distinction cannot simply be transported.
- [Ore], the corrected 2019 v3, §0: fixed three-braids have finitely many Hurwitz orbits, and a particular exponent-two braid has two orbits. We use the corrected manuscript, which flags corrections to the published version. Section 2 explicitly removes the apparent obstruction in that two-orbit example by allowing global conjugation.
- [GS], Proposition 5.1 and its labeling discussion: under the stated incidence hypotheses, adding a distinguished symplectic line preserves the set of symplectic isotopy classes. Only the transverse, nonsingular case is used below.
- [ST], Theorem C: the closed symplectic isotopy problem in the projective plane has a positive answer in degrees at most 17.

Fresh searches also covered combinations of smooth isotopy, complex curves, quasipositive surfaces, symplectic isotopy, four-ball, and 2025/2026; the current research pages of Hayden and Starkston; and Golla's December 2025 lecture notes [Gol]. No primary result meeting the exact contrast was verified. This is a bounded negative search, not a proof that no result exists. The current K3 text still poses the target and distinguishes it from the results above. A search result from an automated problem repository was not treated as a mathematical source.

## 1. Attempt: deform a smooth isotopy into a symplectic one

The proposed strategy was to turn a given smooth isotopy into a symplectic isotopy by local Hamiltonian extension or by an exact-form Moser argument. Local extension is valid; the missing global positivity is not automatic.

### Lemma 1.1: stationary-collar symplectic isotopies extend Hamiltonianly

Let S_t be a smooth family of compact symplectic surfaces in a fixed symplectic manifold, stationary on a collar of their boundaries. There is a compactly supported Hamiltonian isotopy taking S_0 to S_t, with support away from that collar.

Proof. At each point of S_t, split the velocity of a parametrization into its tangent part and its symplectic-normal part N_t, using the direct sum T M|S_t = T S_t ⊕ (T S_t)^ω. This splitting exists because ω restricts nondegenerately to T S_t. The tangent velocity changes only the parametrization. Prescribe a function H_t to be zero on S_t and prescribe its differential on all ambient tangent vectors along S_t by

    dH_t = -ι_(N_t) ω.

The prescribed covector annihilates T S_t, so it is compatible with H_t|S_t=0. A tubular neighborhood realizes this smooth first jet, with a cutoff chosen away from the stationary collar. For the convention ι_(X_H)ω=-dH, X_H=N_t along S_t. Its flow therefore has exactly the required normal velocity. Uniqueness for the ordinary differential equation gives the moving images S_t. Compactness and the cutoff give the flow for the whole interval. □

This is standard symplectic isotopy extension, recorded with proof to expose the hypothesis, not claimed as a new result. It also implies local uniqueness: sufficiently C¹-small normal graphs over a fixed compact symplectic surface, with a fixed collar, are joined by scaling the graph section, since positivity is open.

### The failed global step

A smooth path need not remain inside that open set. Neither exactness nor agreement of cohomology makes affine interpolation of symplectic forms symplectic. The failure persists when the endpoint forms are positive on the same distinguished plane.

Put e_ij=dx_i∧dx_j on R⁴ and P=span(∂_1,∂_2). Consider

    ω₀=e₁₂+e₃₄,
    ω₁=e₁₂+2e₁₃−2e₂₄−3e₃₄.

Both are closed and exact; their squares equal twice the standard volume form; both restrict to e₁₂ on P. But for ω_t=(1−t)ω₀+tω₁, the coefficient of half its square is

    (1−4t)+4t²=(1−2t)².

At t=1/2 the form is degenerate. Thus even these strengthened endpoint conditions do not justify the straight-line Moser proof. This example does not prove that no other path exists between these particular forms; it refutes the proposed automatic interpolation step.

**Exact gap.** One needs a global path of embedded surfaces with positive pulled-back area form throughout, or an appropriate relative path of symplectic forms with the required endpoint and submanifold control. Lemma 1.1 extends a path after it exists. It does not construct it from a smooth path.

## 2. Attempt: use a small Hurwitz-inequivalent quasipositive pair

The proposed construction starts with two quasipositive factorizations of the same braid and hopes that a Hurwitz obstruction separates the resulting curves while their smooth embeddings agree. This must be tested against global conjugation and changes of braid presentation.

Write B₃=⟨a,b | aba=bab⟩, let z=(ab)³, and set β=a²b²a²b²z⁻¹. The two length-two factorizations arising from [Ore]'s example simplify to

    P=(a, (ab²)a(ab²)⁻¹),
    Q=(a²ba⁻², b).

Their products both equal β. Here is an algebraic verification. Put W=a²b²a²b². The braid relation gives z=a²ba²b, and z is central. Thus

    (P₁P₂)z=a²b²ab⁻¹abab=a²b²a²b²=W,
    (Q₁Q₂)z=a²b(a⁻²z)b=a²b²a²b²=W.

In the first equality chain, substitute aba=bab in the final substring; in the second use a⁻²z=ba²b. In the second factorization, the apparently longer conjugator a²ba² is z b⁻¹, which commutes with b. Their Hurwitz-orbit distinction is an imported result of [Ore], not established by a finite orbit search here.

### Proposition 2.1: the pair becomes equivalent under global conjugation

Let g=ab⁻¹a⁻¹. Then g P_i g⁻¹=Q_i for i=1,2, and consequently g commutes with β.

Proof. The braid relation implies b⁻¹ab=aba⁻¹. Hence

    gag⁻¹ = a(b⁻¹ab)a⁻¹ = a²ba⁻².

Also g(ab²)=ab, so

    g[(ab²)a(ab²)⁻¹]g⁻¹=(ab)a(ab)⁻¹=b,

where the last equality follows from aba=bab. Multiplying the two identities proves the centralizer assertion because the products are the same β. □

The standard monodromy description must allow changes of the fiber identification, giving simultaneous conjugation. Thus a distinction erased by Proposition 2.1 supplies no obstruction for the unmarked target. We do not infer complex isotopy from this algebra alone, nor claim that Hurwitz plus conjugation is a complete equivalence theorem for every boundary convention. The exact negative conclusion is that this proposed invariant cannot distinguish this candidate pair.

For a second check, the homological lifts of a and b to the once-punctured torus act by

    A=[[1,1],[0,1]], B=[[1,0],[-1,1]].

The two vanishing-cycle column pairs can be chosen as ((1,0),(-1,-2)) and ((2,1),(0,1)). Each presents H₁≅Z/2. Equality of these groups is only necessary for smooth isotopy, not sufficient. The global-conjugation argument is stronger and disposes of the proposed Hurwitz invariant directly.

At braid index two there is an even simpler exclusion: B₂ is infinite cyclic, every conjugate of its positive generator is that generator, and the exponent determines the whole quasipositive tuple. There is no distinct tuple in this model. [Ore]'s finiteness for a fixed three-braid limits a fixed-presentation infinite-family strategy; it is not a theorem about every representative of a transverse link after arbitrarily many Markov moves.

**Exact gap.** A useful new braid candidate would need an explicit smooth isotopy and an obstruction invariant under all moves allowed by the chosen symplectic or complex category, including at least global conjugation. Raw Hurwitz non-equivalence, equal Euler characteristic, and equal branched-cover homology do not provide that pair of certificates.

## 3. Attempt: recycle the infinite family through branched-cover invariants

The proposed strategy was to start with the known infinite complex-annulus family and retain a symplectic distinction while eliminating its smooth distinction. The first test already excludes the original family.

### Lemma 3.1: smooth isotopy preserves the canonical double branched cover

If two properly embedded oriented surfaces in the ball are smoothly ambiently isotopic, their double covers branched over the surfaces are diffeomorphic. The statement holds with boundary markings preserved when the isotopy preserves them.

Proof. On the surface complement, the canonical two-sheeted cover is specified by sending every meridian to 1 in Z/2. An ambient isotopy transports meridians to meridians, so preserves this character and lifts to the cover of the complements. The lift extends over the branch locus in the normal-disk model u↦u². Equivalently, transport the branched-cover construction along the isotopy. This produces a diffeomorphism of the covers. □

Consequently any invariant of the smooth cover, its homology in particular, must agree for a target pair. The same observation applies directly to the smoothly marked complement and its smooth invariants.

For the [BVHM, Theorem 10] family, its handle calculation supplies the following abelian relation matrix in three generators (a,c,b):

    R_n = [[ 1,  2, 1],
           [ 0,  0, 1],
           [-1, -2, 1],
           [ 0, -n, 1]].

We independently reduce this presentation. The second relation gives b=0. The first gives a=−2c. The third becomes redundant. The fourth becomes nc=0. Therefore

    coker(R_nᵀ) ≅ Z/n for n≠0, and ≅ Z for n=0.

This is a universal integral calculation, not an extrapolation from data. For positive odd n, the branch surfaces are annuli and these homology groups have different orders. Lemma 3.1 rules out smooth isotopy between any two with different n. Selecting the odd subsequence preserves both the boundary type and the smooth obstruction; it does not repair it.

The exact checker additionally computes every determinantal divisor for −100≤n≤100. It obtains (1,1,|n|), with rank two at n=0. This verifies implementation and signs against the universal elimination above. It is not used as a proof for untested n.

Choosing parameters with the same absolute value only removes this particular necessary-condition obstruction. It does not construct a smooth isotopy, a new infinite family, or a symplectic obstruction. Similarly, equal Euler characteristic, signature, or fundamental group cannot certify smooth equivalence.

**Exact gap.** A branched-cover strategy needs a single smooth branch-pair isotopy class supporting distinct symplectic or Stein information, together with a proof that that information is invariant under the target isotopies. Distinct smooth covers prove the wrong statement. No such new branch pair or separating invariant is constructed here.

## 4. Attempt: perturb distinguishable exact Lagrangian fillings

The proposed strategy uses [CG]'s smoothly isotopic, Hamiltonian-inequivalent fillings and tries to perturb them into symplectic or complex curves.

### Lemma 4.1: retaining a Legendrian boundary is impossible

Let λ be the standard Liouville form on the ball and ω=dλ. A nonempty compact oriented ω-symplectic surface cannot have its whole boundary Legendrian in the standard contact sphere.

Proof. If Λ is Legendrian then λ vanishes on its tangent line. Stokes' theorem gives ∫_S ω=∫_Λ λ=0. A symplectic surface with its symplectic orientation has strictly positive area. Contradiction. □

This obstruction concerns the actual geometric boundary, and does not require exactness of the original Lagrangian. A perturbation must move its boundary, for example toward a transverse pushoff.

In a cotangent neighborhood of an oriented Lagrangian surface F, a graph of a one-form εη has pulled-back symplectic form εdη, using the convention ω=dθ. To make the graph positive requires dη>0. If η vanishes on the boundary tangent line then Stokes again forbids that condition. Allowing a nonzero boundary integral can remove the area obstruction, but introduces additional boundary choices. This explicit local calculation supplies neither a canonical global perturbation in the ball nor invariance of the original filling invariant after perturbation.

There is a particularly useful consistency test. [CG] includes the maximal-tb Legendrian (4,4) torus link. Its positive transverse pushoff has the standard transverse (4,4) type. In the standard unmarked capping setting of Section 5, every resulting symplectic filling lies in the unique degree-four symplectic class. Thus **any** proposed conversion into that capped class must lose the Hamiltonian distinction. This is a conditional obstruction to an invariant-preserving conversion, not an assertion that a conversion with all desired boundary controls exists.

**Exact gap.** One needs (i) a boundary-controlled conversion producing complex endpoints, (ii) retention of the common smooth isotopy class, and (iii) a separating invariant surviving this conversion and invariant under symplectic paths. [CG] proves none of these three statements for symplectic surfaces merely by proving its Lagrangian theorem. Lemma 4.1 invalidates the simplest boundary-fixed version.

## 5. Attempt: projective capping, degree reduction, and complex deformation

The proposed strategy caps fillings of the standard transverse T(d,d), applies projective-plane classification or deformation of polynomials, and then tries either to prove general uniqueness or to transport a counterexample back to the ball.

### Capping statement used and its boundary

In the capping convention explained in [K3, Remark (2)], a nonsingular degree-d symplectic curve with a generic distinguished line yields a proper surface in the ball with transverse boundary T(d,d). Conversely the standard cap supplies such a pair. [GS, Proposition 5.1(1)] identifies symplectic isotopy classes before and after adding this generic line: all intersections are transverse smooth points, so its singular-incidence restriction is satisfied.

This is a statement about configurations with a distinguished line and the indicated equivalence of boundary identifications. It is not an assertion that an arbitrary closed isotopy fixes a predetermined cap pointwise. We use that imported correspondence only in its stated unmarked setting.

Combined with [ST, Theorem C] and connectedness of nonsingular algebraic curves of fixed degree, it gives one symplectic isotopy class in this standard capped setting for 1≤d≤17. The conclusion is about symplectic isotopy, not about all paths remaining complex after a fixed ball cut. In particular, it cannot settle the complex-only branch of KP-4.104 for arbitrary transverse links.

### Adjunction calculation and failure of stabilization

For a closed degree-d symplectic curve C in CP², choose a compatible almost complex structure preserving T C. The complex splitting of T CP²|C into tangent and normal lines gives

    3d = χ(C) + d²,
    g(C) = (d−1)(d−2)/2.

The standard ball filling removes d disks, so its Euler characteristic is

    χ(S)=χ(C)−d=2d−d².

The full-twist braid calculation agrees: d sheets and d(d−1) positive bands give χ(S)=d−d(d−1). For d=4 this is χ(S)=−8 and g(C)=3; d=17 gives g(C)=120; d=18 gives g(C)=136.

Adding an ordinary internal handle while retaining the same cap and degree increases the closed genus by one. It contradicts the displayed adjunction equality if the resulting capped surface is required to be symplectic. Thus the common smooth-topological tactic of stabilizing surfaces until they become isotopic cannot simply be applied while retaining this symplectic filling problem. This is an obstruction in the fixed standard-cap class, not a claim about every possible modification of boundary link or degree.

### Why connected polynomial space does not solve the ball problem

Nonsingular projective curves of fixed degree form the complement of a complex discriminant in a projective parameter space and hence are path connected. Cutting by a fixed ball imposes a second requirement: transversality to its real boundary. Its failure need not have real codimension at least two.

An explicit example already occurs for the smooth complex lines C_c={w=c} in C². In the unit ball their intersection is a disk when |c|<1, a tangency point when |c|=1, and empty when |c|>1. The complex curve never becomes singular, but the boundary-transversality wall |c|=1 has real codimension one in the complex c-plane. Consequently avoiding the complex discriminant alone does not preserve the relative embedding or transverse boundary type. This example demonstrates the gap; it is not a pair of target counterexamples.

**Exact gap.** Beyond the established capped degrees, one would need a new global symplectic classification or an actual nonisotopic pair with a smooth isotopy. For the complex-only branch, one must control the ball-boundary transversality chamber along a complex deformation. Neither degree arithmetic nor connectedness before imposing the real boundary condition provides that control. No implication from failure of a closed symplectic isotopy conjecture to the exact complex-endpoint/smooth-isotopy target is claimed without additional construction.

## Attempt accounting and acceptance boundary

There are exactly five substantive approaches above: global deformation; explicit braid-factorization construction; branched-cover construction; Lagrangian-to-symplectic conversion; and projective capping/complex deformation. Each identifies a mathematical strategy, carries out an actual derivation, and ends with the remaining gap. Source recovery, current-literature search, exact arithmetic checks, and this audit contribute zero additional attempts.

The report proves the local extension lemma, the explicit simultaneous-conjugation identities, the cover-homology reduction and smooth-isotopy obstruction for the imported family, the Legendrian-boundary area obstruction, and the stated numerical and boundary-wall calculations. All are restricted observations; no broad novelty is asserted. The imported low-degree classification and generic-line correspondence are clearly separated from the calculations.

For an affirmative resolution one still needs a concrete transverse link type, explicit complex fillings, a smooth isotopy under specified boundary identifications, and a valid complex or symplectic non-isotopy obstruction. An infinite answer also needs all examples in one smooth class and a pairwise obstruction surviving all permitted moves. None has been provided here. For a negative resolution one would need a general injectivity theorem for the relevant forgetful map on isotopy classes, far stronger than the local results above.

## Reproducible exact checks

Run `python verify_exact.py` from any directory. The script uses only the Python standard library and writes to stdout by default; `--output PATH` is an explicit optional output destination. It does not read source PDFs or a local corpus. The expected output is `EXACT_CHECKS.json`.

All validations use an always-active `require` that raises on failure. Normal, `-O`, and `-OO` executions were compared byte for byte. The script checks the braid relation and inverse actions first, then verifies the common product, simultaneous conjugation, centralizer identity, Smith determinantal divisors, the degenerate affine-form path, and adjunction/Euler identities. The mathematical proofs in this report, rather than bounded tests, justify universal claims. No executable tries to decide smooth, complex, or symplectic isotopy.

## References

- **[K3]** R. İnanç Baykur, Robion C. Kirby, and Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, April 2026 preliminary author version, Problem 4.104, pp. 277–278; Problem 4.101, pp. 273–274. [Author-hosted PDF](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf).
- **[BVHM]** R. İnanç Baykur and Jeremy Van Horn-Morris, *Fillings of genus-1 open books and 4-braids*, IMRN 2018, 1329–1346. [Paper](https://arxiv.org/abs/1604.02945), [publication](https://doi.org/10.1093/imrn/rnw281).
- **[Hay]** Kyle Hayden, *Exotically knotted disks and complex curves*, arXiv:2003.13681v2 (2021). [Paper and version history](https://arxiv.org/abs/2003.13681).
- **[CG]** Roger Casals and Honghao Gao, *Infinitely many Lagrangian fillings*, Annals of Mathematics 195 (2022), 207–249. [Paper](https://arxiv.org/abs/2001.01334), [publication](https://doi.org/10.4007/annals.2022.195.1.3).
- **[Ore]** Stepan Yu. Orevkov, *On the Hurwitz action on quasipositive factorizations of 3-braids*, corrected arXiv:1409.4726v3 (2019). [Versioned paper](https://arxiv.org/abs/1409.4726v3), [author manuscript](https://www.math.univ-toulouse.fr/~orevkov/orb-e.pdf).
- **[GS]** Marco Golla and Laura Starkston, *The symplectic isotopy problem for rational cuspidal curves*, Compositio Mathematica 158 (2022), 1595–1682. [Paper](https://arxiv.org/abs/1907.06787), [publication](https://doi.org/10.1112/S0010437X2200762X).
- **[ST]** Bernd Siebert and Gang Tian, *On the holomorphicity of genus two Lefschetz fibrations*, Annals of Mathematics 161 (2005), 959–1020, Theorem C. [Publisher page](https://annals.math.princeton.edu/2005/161-2/p09), [publisher PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v161-n2-p09.pdf).
- **[Gol]** Marco Golla, *Surfaces in 4-manifolds and complex curves*, arXiv:2512.09181 (December 2025), contextual lecture notes. [Paper](https://arxiv.org/abs/2512.09181). This is not used as a new resolution claim.

Only authored analysis, exact checks, bibliographic facts, and verification metadata belong to this packet. Source documents and source text are not included.
