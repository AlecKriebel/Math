# Elliptic Reeb orbits on the standard contact three-sphere

## Result and scope

**Unresolved after five mathematical approaches.** Neither a proof nor a counterexample to the universal assertion in K3 Problem 3.47(a) or (b) was obtained. The completed results below are reductions, conditional criteria, and explicit obstructions to proposed arguments. They are not claimed to be new literature results.

The problem was checked in the actual 2026 K3 author manuscript, printed page 164 (PDF page 164), against the supplied problem record. The older AIM workshop report is not used as the statement source. A visual inspection confirmed both subquestions. In our notation they ask whether every contact form for the standard contact structure on S³ has an elliptic closed Reeb orbit, and whether this holds at least for the forms induced on smooth strictly convex boundaries in R⁴. No genericity, nondegeneracy, symmetry, pinching, or finite-orbit assumption occurs in either question. [K3]

We use the **inclusive spectral convention**: a periodic orbit is elliptic when every eigenvalue of its transverse return map has absolute value one. This includes parabolic/degenerate cases. K3 explicitly adopts this convention in its contact-topology introduction (§3.5, printed/PDF p.160), and its cited Abreu–Macarini paper uses the same convention. The distinction is essential: the standard round sphere has Hopf fibers with identity return map, so a version requiring strictly nonreal eigenvalues for every form would already fail. No such reinterpretation is used here. [K3, §3.5; AM]

There are five independent attacks below: ECH chain counting; disk-return fixed-point indices; Hamiltonian index/pinching; hyperbolicity and topology; and perturbative compactness. Bibliographic work, normalization, numerical checks, and this audit count as zero additional attacks.

## 1. Normalizations and completed elementary reductions

Let α be a smooth positive contact form on S³ and ξ = ker α. Write R for its Reeb field. The time-T return map along a periodic orbit restricts to a symplectic map P on the two-dimensional plane ξ. Thus det P = 1 and its characteristic polynomial is

    q_P(t) = t² − (tr P)t + 1.

Consequently:

- |tr P| < 2 gives a nonreal unit-circle pair;
- |tr P| = 2 gives a possibly nonsemisimple repeated eigenvalue +1 or −1;
- |tr P| > 2 gives a real reciprocal pair off the unit circle.

This proves that an orbit fails inclusive ellipticity exactly when it is hyperbolic. Every iterate of a hyperbolic orbit is nondegenerate. Conversely, eigenvalues of P^m are the m-th powers of those of P, so ellipticity of an iterate implies ellipticity of the simple underlying orbit.

**Reduction 1.** Each universal question is equivalent to excluding a form in its stated class whose simple periodic orbits are all hyperbolic. Every such counterexample would automatically be nondegenerate, including all covers. The degenerate case is not a separate obstacle under the inclusive convention: a degenerate return map already has both eigenvalues equal to 1.

For fixed ξ_std, every positive defining form is fα_std for a smooth f > 0. The radial map x ↦ √f(x)x pulls the standard Liouville form on its star-shaped image back to fα_std: terms differentiating √f disappear since the radial vector is annihilated by the Liouville form. Thus (a) has a star-shaped formulation, but star-shaped does not mean strictly convex. The stronger geometric condition in (b) gives dynamical convexity, expressed in the disk trivialization as μ_CZ^−(γ) ≥ 3 for every periodic orbit, including covers. It does not impose the higher-iterate bound used below. [AM, HS]

## 2. Approach 1: ECH counting and the finite-orbit escape

### 2.1 A direct finite-generator contradiction

Assume all simple orbits are hyperbolic. The preceding reduction supplies the nondegeneracy needed for the ordinary ECH chain complex. An admissible ECH orbit set can contain each hyperbolic simple orbit only with multiplicity one. If there were N simple orbits in total, there would therefore be at most 2^N chain generators over F₂, including the empty set.

On S³, ECH has a sequence of nonzero homogeneous classes σ_k with Uσ_(k+1) = σ_k. The degrees differ by two, so these classes are linearly independent. A finite-dimensional chain complex cannot have infinite-dimensional homology. This is a contradiction. The ECH admissibility and U-sequence inputs are recorded in [TI, §§2.1–2.5]; they are standard established ECH facts, not conjectural contact-homology foundations.

**Completed conclusion.** Any hypothetical counterexample to either part has infinitely many simple periodic orbits.

This also follows from stronger published/established results: torsion first Chern class gives two or infinitely many simple orbits, without a nondegeneracy hypothesis; exactly two simple orbits forces both to be irrationally elliptic. Since H²(S³;Z)=0, the torsion hypothesis is automatic. Thus the entire finite-orbit case of (a), and hence (b), is already affirmative. [TI, Theorem 1.1; TWO, Theorem 1.2]

### 2.2 Quantitative version proved from the same count

Let V = ∫_(S³) α∧dα and let N(L) count simple orbits of action strictly less than L. For a nondegenerate form, N(L) is finite: compactness of bounded-period trajectories, a positive lower bound for periods of a nonsingular field on a compact manifold, and isolation of every closed orbit including its covers rule out an accumulating sequence of bounded-period simple orbits.

The ECH Weyl law gives c_(σ_k)(α)²/k → 2V. For every ε > 0 and all sufficiently large L, at least

    floor((1−ε)L²/(2V)) − O(1)

linearly independent σ_k have spectral value less than L. Their representatives lie in the action-filtered complex. Every generator of that complex is a subset of the N(L) simple hyperbolic orbits, so its dimension is at most 2^N(L). Hence

    liminf_(L→∞) 2^N(L)/L² ≥ 1/(2V),

or equivalently

    N(L) ≥ log₂(L²/(2V)) + o(1).

For clarity, this is only a lower bound; it does not estimate N(L) from above. The Weyl law refers to action-weighted ECH orbit sets, not to a single elliptic orbit. [TI, Proposition 2.12]

**Exact remaining gap.** Infinitely many hyperbolic simple orbits can supply infinitely many finite subsets. Neither infinite ECH rank nor this logarithmic lower bound contradicts such a flow. Treating an ECH spectral representative as one simple orbit would be invalid.

A relevant new manuscript is Shibata's September 2026 preprint: its Theorem 1.1 asserts that any nondegenerate closed connected contact three-manifold with at least three simple orbits has a simple positive hyperbolic orbit. This excludes an all-negative-hyperbolic candidate if the preprint's theorem is used, but it does not exclude an all-hyperbolic candidate. Its proof has not been independently audited here, and none of our completed proofs depends on it. [S]

## 3. Approach 2: global disks and Lefschetz indices

Dynamical convexity on S³ gives a disk-like global surface of section with binding of disk Conley–Zehnder index 3. [HS, Theorem 1.3] A tempting argument is that a disk return map must have a fixed point of index +1, which must be elliptic. The last implication is false.

For a nondegenerate fixed point of an orientation-preserving area-preserving surface map with derivative A,

    ind = sign det(I−A) = sign(2−tr A).

Both an elliptic fixed point and a **negative hyperbolic** fixed point have index +1. A positive hyperbolic point has index −1. Thus Brouwer/Lefschetz counting alone cannot distinguish elliptic from negative hyperbolic behavior.

We pushed the argument through all iterates in a deliberately favorable setting. Assume a C¹ area-preserving diffeomorphism f of the closed disk has no periodic point on its boundary and all interior periodic points are hyperbolic. These extension/boundary assumptions are explicit additional hypotheses; we do not infer them from a global section without analysis at its binding.

Let a_d and b_d be the numbers of positive and negative hyperbolic cycles of least period d. Compactness and the assumptions imply finitely many fixed points for each f^n. Lefschetz's formula, with L(f^n)=1, gives

    Σ_(d|n) d[−a_d + (−1)^(n/d+1)b_d] = 1.                 (3.1)

Indeed each least-period-d cycle gives d fixed points for f^n. A positive hyperbolic return remains positive under every iterate; a negative hyperbolic return is negative for odd iterates and positive for even ones.

At n=1, b_1−a_1=1. Comparing the identities for n=2^k and n=2^(k−1) yields

    b_(2^k) − a_(2^k) = b_(2^(k−1)),    k≥1.              (3.2)

In particular b_(2^k)≥1 for every k. This gives a genuine conditional period-doubling conclusion, but still no elliptic orbit.

More decisively, the formal assignment

    a_d=0 for every d;
    b_d=1 if d is a power of two, and b_d=0 otherwise

satisfies (3.1) for **every positive integer n**. Write n=2^k m with m odd. The sum becomes

    −(1+2+⋯+2^(k−1)) + 2^k = 1.

For odd n this is simply b_1=1. This is a formal index model, not a realization by a disk map or a Reeb flow.

**Exact remaining gap.** A genuine geometric restriction beyond the Lefschetz identities is needed to prohibit the infinite hyperbolic period-doubling pattern. A global section, orbit infinitude, and fixed-point index positivity do not by themselves prove ellipticity. Moreover general part (a) lacks dynamical convexity and does not automatically supply the particular global disk used in this attack.

## 4. Approach 3: Hamiltonian index growth, convexity, and pinching

On S³, Abreu–Macarini's higher-iterate criterion specializes as follows: if for some fixed integer k>1 every periodic orbit satisfies

    μ_CZ^−(γ) ≥ 3,       μ_CZ^−(γ^k) ≥ 4k−1,

then an elliptic orbit exists. Their Hessian-pinching corollary supplies this mechanism when R/r<√2. Here pinching means bounds

    R^(−2)|v|² ≤ <D²H(x)v,v> ≤ r^(−2)|v|²

for the homogeneous degree-two defining Hamiltonian. It is not merely an arbitrary estimate on inner and outer Euclidean radii. Their symmetry criterion separately supplies ellipticity for antipodally invariant dynamically convex forms. [AM, Theorem B and Corollaries 2.7, 2.11]

We attempted to obtain the iterate bound from dynamical convexity alone. In dimension two a hyperbolic symplectic path has the exact iteration law

    μ_CZ(γ^m) = m μ_CZ(γ).

Therefore the allowed value μ_CZ(γ)=3 produces 3k, which is strictly smaller than 4k−1 for every k>1. In fact the binding provided by the global-disk theorem has index 3. In a putative all-hyperbolic dynamically convex flow that binding must be negative hyperbolic, so this is a concrete obstruction, not an irrelevant parity case. [HS, Theorem 1.3]

### A positive Hamiltonian linear system with hyperbolic monodromy

The following explicit construction tests the stronger hope that positivity of the instantaneous quadratic Hamiltonian forces elliptic monodromy.

Use J=[[0,−1],[1,0]] and H_a=diag(a,1/a), a>0. The solution of ż=JH_a z for time π/2 is

    Q_a = [[0,−1/a],[a,0]].

For a=2 and then b=1, two quarter-turn segments give

    Q_1 Q_2 = diag(−2,−1/2).

Each Hamiltonian matrix is positive definite, but the product has trace −5/2 and is negative hyperbolic. Append a full positive rotation, whose endpoint is identity. Along the eigenvector e_1, the lifted angular change is 3π; hence the path has Conley–Zehnder index 3 in this fixed trivialization, and its iterates have indices 3m. One may smooth the positive-definite coefficient at the joins, including the periodic seam, with arbitrarily small change in the monodromy. Negative hyperbolicity and the index persist because the endpoint remains away from eigenvalue 1.

This is a transverse linear-system construction, **not** a realization of an all-hyperbolic strictly convex hypersurface in R⁴. It disproves only the proposed local-linear inference from positivity to ellipticity and shows exactly why a global pinching/index argument requires more information.

**Exact remaining gap.** Convexity supplies the first index threshold but not the needed higher-iterate threshold for the index-three binding. No way was found to force a different orbit to be elliptic without the actual extra symmetry or pinching assumptions.

## 5. Approach 4: rule out hyperbolicity using the topology of S³

The known absence of Anosov flows on S³ suggests this chain of implications:

    no elliptic orbit → all periodic orbits hyperbolic → flow Anosov → contradiction.

Only the first arrow is automatic. Contreras–Mazzucchelli prove an Anosov criterion requiring BOTH uniform hyperbolicity of the closure of the periodic set AND Kupka–Smale transversality of stable/unstable intersections. Pointwise hyperbolicity of each periodic orbit supplies neither hypothesis. [CM, Theorem D]

There is a precise quantitative obstruction to replacing uniform hyperbolicity by a uniform separation of return multipliers from the unit circle. Consider the formal sequence of return matrices

    P_j = diag(2,1/2),       T_j=j.

All traces equal 5/2 and all multipliers are uniformly separated from the unit circle. Yet the expanding exponent per unit time is (log 2)/j, tending to zero. If constants C,κ>0 gave a uniform unstable estimate for every iterate of every orbit, then on orbit j one would need

    2^m ≥ C^(−1) exp(κ m j)  for every m≥1.

Taking m-th logarithms and letting m→∞ forces log2 ≥ κj for every j, impossible. The formal matrices are not claimed to be realized by the target Reeb flow; they establish that the spectral data used by this attempted argument do not contain the required uniform rate estimate. Uniform splitting angles and transversality present additional issues.

**Completed conditional reduction.** An all-hyperbolic counterexample on S³ cannot simultaneously have uniformly hyperbolic periodic-set closure and the Kupka–Smale property, by [CM, Theorem D] and the no-Anosov fact. In the Kupka–Smale subclass, its periodic-set closure must fail uniform hyperbolicity.

**Exact remaining gap.** Establishing uniform hyperbolicity (or a substitute that forces ellipticity) from the specific Reeb/convex geometry remains unproved. Promoting all-hyperbolic periodic data to an Anosov flow would assume the crucial missing result.

## 6. Approach 5: approximation, compactness, and loss of period bounds

Generic ellipticity is weaker than universal ellipticity. For example, Contreras–Mazzucchelli prove elliptic closed-geodesic existence on a C²-open dense set of smooth metrics on S². [CM, Corollary 1.1] We investigated whether taking limits closes the gap.

### Bounded-period closure lemma

Let α_j→α in C² on a fixed compact three-manifold, with α and all α_j contact. Suppose α_j has an inclusively elliptic orbit γ_j of period T_j≤B for one common B. Then α has an inclusively elliptic periodic orbit.

**Proof.** The Reeb fields converge in C¹. Their nonvanishing limit on a compact manifold gives a common positive lower bound on nonzero periods. One way to see this is to cover the manifold by finitely many flow-box neighborhoods for the limit field; C¹-close fields have, in smaller neighborhoods, a coordinate whose derivative has fixed nonzero sign. Uniform velocity bounds then prevent any sufficiently short trajectory from leaving such a smaller neighborhood and closing.

After taking a subsequence, the starting points converge and T_j→T∈(0,B]. Continuous dependence of flows gives φ_α^T(x)=x. C¹ convergence of flows on bounded time intervals also gives convergence of derivatives. Choose continuously varying local frames for the contact planes at the starting points. The transverse return matrices therefore converge to the return matrix P of this period-T orbit. Each P_j has |tr P_j|≤2, hence |tr P|≤2. The limit is elliptic. If the period-T orbit is a multiple cover, its simple underlying orbit is elliptic by Reduction 1. ∎

**Consequences.** For any fixed B, existence of an elliptic orbit with period at most B is a closed property in this C² topology. If α has only hyperbolic periodic orbits and α_j→α has elliptic orbits, the periods of every such chosen sequence tend to infinity. Thus density of elliptic forms cannot settle the question without a uniform period bound. The same bounded-period mechanism applies to C²-converging metrics after identifying their unit bundles smoothly; their geodesic vector fields converge in C¹.

### Why symmetry averaging does not provide the missing approximation

Write α=fα_std. Under the antipodal involution ι, invariant forms correspond to even f. For any continuous f define D=||f−f∘ι||_∞. For every even g,

    D ≤ 2||f−g||_∞.

The average g=(f+f∘ι)/2 attains equality. Thus the exact C⁰ distance from f to the even functions is D/2. Unless f is already even, fixed-antipodal invariant forms cannot approximate it arbitrarily well. For f=2+x_1 on S³, the distance is exactly 1.

There is also no orbit-preserving averaging identity. For a fixed contact form β,

    R_(fβ)=f^(−1)R_β+Y,  Y∈kerβ,
    dβ(Y,v)=df(v)/f²  for v∈kerβ.

These equations follow directly from the two Reeb equations. If Y vanished everywhere, df would vanish on kerβ; writing df=hβ and differentiating, restriction to kerβ yields h dβ=0, hence h=0 and f is constant on each connected component. Nonconstant rescalings therefore generally change the orbit curves, not just their speed. Moreover averaging is not known here to preserve dynamical convexity.

**Exact remaining gap.** No a priori period bound was obtained for elliptic orbits in approximating generic or symmetric flows. Fixed-symmetry forms are not even dense. The compactness lemma isolates a sufficient missing estimate rather than providing it.

## 7. Final status and interpretation

- Both universal K3 subquestions remain unresolved in this packet.
- All degenerate cases containing a degenerate orbit satisfy the inclusive spectral conclusion immediately.
- Every finite-simple-orbit flow on S³ satisfies the conclusion by existing theorems.
- A hypothetical counterexample is nondegenerate, has infinitely many simple hyperbolic orbits, and satisfies the explicit ECH counting lower bound above.
- In the dynamically convex subclass, the index-three disk binding would be negative hyperbolic. The September 2026 Shibata theorem, if invoked, additionally forces a positive hyperbolic simple orbit.
- The global-disk index model, positive-Hamiltonian matrix construction, hyperbolicity rate obstruction, and bounded-period closure lemma expose different precise gaps. None constructs a counterexample or proves global ellipticity.

The source check is bounded as of 2026-10-08. No retrieved primary source settled either universal question. Negative search findings are not a proof of novelty or of absence of later/unindexed work. No source text, source PDF, or dataset is included in this authored packet.

## Public references

[K3] R. İnanç Baykur, R. C. Kirby, D. Ruberman (eds.), K3: A New Problem List in Low-Dimensional Topology, AMS Mathematical Surveys and Monographs 295 (2026), §3.5, p.160 (ellipticity convention), and Problem 3.47, p.164. Author manuscript: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

[AM] M. Abreu, L. Macarini, Dynamical convexity and elliptic periodic orbits for Reeb flows, Mathematische Annalen 369 (2017), 331–386. Final author version: https://arxiv.org/abs/1411.2543v3 . DOI: https://doi.org/10.1007/s00208-017-1532-4

[TI] D. Cristofaro-Gardiner, U. Hryniewicz, M. Hutchings, H. Liu, Proof of Hofer–Wysocki–Zehnder's two or infinity conjecture, author manuscript v2 (2024): https://arxiv.org/abs/2310.07636v2

[TWO] D. Cristofaro-Gardiner, U. Hryniewicz, M. Hutchings, H. Liu, Contact three-manifolds with exactly two simple Reeb orbits, Geometry & Topology 27 (2023), 3801–3831. https://doi.org/10.2140/gt.2023.27.3801 . Author version: https://arxiv.org/abs/2102.04970v4

[HS] U. Hryniewicz, Systems of global surfaces of section for dynamically convex Reeb flows on the 3-sphere, Journal of Symplectic Geometry 12 (2014), 791–862. https://arxiv.org/abs/1105.2077

[CM] G. Contreras, M. Mazzucchelli, Proof of the C²-stability conjecture for geodesic flows of closed surfaces, Duke Mathematical Journal 173 (2024), 347–390. https://doi.org/10.1215/00127094-2023-0010 . Final author version: https://arxiv.org/abs/2109.10704v4

[S] T. Shibata, Existence of a positive hyperbolic orbit in three-dimensional Reeb flows, preprint v1, posted 14 September 2026: https://arxiv.org/abs/2609.16176v1 . This manuscript's theorem is reported with its preprint status; our proofs do not depend on it.
