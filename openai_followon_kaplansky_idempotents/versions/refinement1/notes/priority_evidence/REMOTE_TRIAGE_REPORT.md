# Ten further research paths opened by the OpenAI mathematics release

Date: 2026-10-06, America/Los_Angeles. Input: local `/Users/alec/Desktop/math`, pinned at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

This is a ranked research agenda, not a proof or priority announcement. Six independent discipline scans, primary-literature checks, targeted whole-corpus duplicate searches, and cross-agent adversarial reviews informed the selection. We did not reprove the source theorems or rebuild Lean. The [release README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md) reports mixed verification scope. Every route assumes its exact upstream theorem survives validation.

Excluded: all first-batch targets and bundled extensions, including multispecies Vlasov–Maxwell and every bosonic-capacity extension; also the separately active wreath/planar-triangle program. Hafnians and smooth-projective rational-point undecidability were unused reserves in the first scan, so they are eligible here. The hafnian weight-encoding gap now has a concrete mechanism.

Order is **launch priority**, balancing theorem impact, clarity, tractability and room for a useful publication. Scores answer the user's question: assuming the target is correct, genuinely novel and published, how important is it within its actual subfield? They do not measure proof probability, independent technical originality, or credit attributable to the follow-on paper. Treat differences of a few tenths as approximate judgments, not measurements. None warrants 10 on present evidence.

| Priority | Target | Source family | Impact / 10 | Remaining mathematical work |
|---|---|---|---|---|
| 1 | Cubic hypersurface GH/KE compactification equals GIT for n≥5 | 037 | 8.7 | Match volume-gap and metric-cone hypotheses; apply established moduli theorem |
| 2 | FPRAS and approximate sampling for arbitrary nonnegative rational hafnians | 113 | 8.2 | Prove compact weight gadget and bit-complexity/sampling bounds |
| 3 | Exponential exact semidefinite extension complexity of TSP | 126 | 8.3 | Reproduce linear-size face projection and PSD monotonicity |
| 4 | Positive-characteristic counterexample to Kaplansky's idempotent conjecture | 197 | 8.8 | Immediate algebra; extract the most explicit available witness |
| 5 | Endpoint nonlinear Maurey extension into every real L1 space | 332 | 8.2 | Extend finite-cut proof and apply full-extension machinery |
| 6 | Bilinear ergodic Hilbert convergence for arbitrary commuting transformations | 082 | 8.3 | Discrete restriction and Calderón transference of full variation |
| 7 | Local ordinary Banach–Mazur rigidity of all von Neumann algebras | 295 | 7.9 | Apply precise cohomological stability theorem, including preduals |
| 8 | C*-simplicity of Thompson F, T, Aut(F), and Comm(F) | 248 | 7.9 | Apply published equivalences to nonamenability of F |
| 9 | Undecidable rational-point existence on smooth projective integral varieties | 004 | 8.1 | Use Poonen's effective geometric reduction |
| 10 | Sperner property of every standard graded Artinian complete intersection | 200 | 7.8 | Apply EGH-to-Sperner theorem in characteristic zero |

## 1. Cubic hypersurface compactifications

**Target.** For cubic n-folds with n≥5, identify the Gromov–Hausdorff compactification of the Kähler–Einstein moduli space with the classical GIT quotient, hence the corresponding coarse polystable KE/K-moduli space. Focus novelty on n≥5; lower dimensions have prior results, including [Liu's cubic fourfold theorem](https://arxiv.org/abs/2007.14320).

**Route.** Family 037, `The-ordinary-double-point-gap-in-every-dimension-September-24-2026`, gives normalized volume at most `2(k−1)^k` for every singular complex klt k-germ. [Li–Liu](https://arxiv.org/abs/1602.05094), Theorem 1.9, identifies the Sasaki–Einstein Reeb valuation as a global minimizer. Together with the volume-density identity, this supplies the metric ordinary-double-point gap required by [Spotti–Sun, Theorem 1.3(2)](https://arxiv.org/html/1705.00377).

**First package.** Write the exact cone-to-moduli implication, check all lower dimensions, and identify the compactification and its boundary. No new central estimate is apparent. Avoid automatic scheme/stack isomorphism or unrestricted statements about every nonclosed semistable point. Smooth-cubic KE existence needs its own priority check if advertised separately.

**Assessment.** Best combination of a substantial geometric conclusion and an explicit existing conditional theorem. Independent audit accepted the route; the minimization bridge is essential, since an upper bound on an infimum alone does not control an arbitrary Reeb valuation. [Audit](agent_notes/cubic_independent_audit.md).

## 2. Weighted hafnian approximation and sampling

**Target.** A uniform FPRAS for the hafnian of any even-order symmetric matrix with nonnegative rational entries encoded in binary, including arbitrary zero support. Runtime polynomial in total input length, inverse relative accuracy and log inverse failure probability. Include approximate sampling from the weighted perfect-matching distribution.

**Route.** Family 113, `A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026`, treats unweighted graphs and expressly excludes compressed weights from its stated scope. Replace weight W by a simple graph with O(log W) vertices whose two-terminal matching signature is `(W,1,0,0)`: a binary DAG with W source-to-sink paths becomes a matching gadget by splitting vertices. Perfect matchings correspond to paths. Clear rational denominators with polynomial bit length.

**First package.** Prove the bijection, encoded-size bounds, zero branch, and sampler pushforward/self-reduction. Independent review checked the mechanism; finite enumeration verified signatures for W=1,…,64. This is evidence for the reduction, not verification of the upstream FPRAS. Compare existing [restricted hafnian approximation](https://arxiv.org/abs/1409.3905).

**Assessment.** Broad computational utility and a small explicit construction. Very high tractability, but high simultaneous-discovery risk. No signed/complex hafnian or general Gaussian-boson-sampling claim. [Details](agent_notes/computation.md).

## 3. Exact SDP lower bounds for traveling-salesman polytopes

**Target.** Every exact real positive-semidefinite lift of the symmetric TSP polytope on N cities has matrix dimension `2^Ω(N)`.

**Route.** Family 126, `Exponential-PSD-rank-of-positively-shifted-matching-matrices-October-5-2026`, provides the matching-polytope bound. The classical reduction expresses the n-vertex perfect-matching polytope as a projection of a face of a TSP polytope with O(n) cities; [Rothvoss](https://arxiv.org/abs/1311.2369) explicitly records this linear-size reduction. PSD lift dimension cannot increase under a face restriction and projection.

**First package.** Reproduce the reduction and monotonicity with precise size conventions. If claiming a matching `2^Θ(N)` order, separately cite and check the dynamic-programming upper bound. Contrast the linear exponent with the older [Lee–Raghavendra–Steurer bounds](https://arxiv.org/abs/1411.6317).

**Assessment.** A sharp complexity barrier for a canonical optimization polytope. Very short route, with little independent technique. Approximation-factor hardness does not automatically follow. [Details and duplicate checks](agent_notes/computation.md).

## 4. Kaplansky idempotents in characteristic two

**Target.** A torsion-free finitely presented group G whose group algebra `F₂[G]` contains an idempotent other than 0 and 1. Extend the same example to every characteristic-two coefficient field. Also exhibit a nonzero cyclic projective module P with `R ≅ R ⊕ P` and `[P]=0` in `K₀(R)`.

**Route.** The October 4 manuscript in family 197, `A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026`, states `ab=1`, `ac=0`, `c≠0` in such a group algebra. Set `e=1−ba`. Then `e²=e`, while the displayed identities exclude e=0 and e=1. Take P=eR. Independent review checked the noncommutative module calculation.

**First package.** Establish the exact positive-characteristic conjecture and provenance; extract finite presentation and coefficients to the extent the upstream construction permits. An existential consequence does not require that extraction, but do not promise an already explicit numerical certificate. See [group-ring conjecture context](https://arxiv.org/abs/1904.04847).

**Assessment.** Highest theorem-impact score in this batch, but the implication itself is immediate and gives the follow-on author very little independent mathematical credit. A short consequence note is appropriate. No characteristic-zero, odd-characteristic or reduced-C*-algebra conclusion. The listed Lean work for family 197 concerns an earlier torsion-containing example, not this newer input. [Independent audit](agent_notes/arithmetic_logic_adversarial.md).

## 5. Endpoint nonlinear Maurey extension into all L1 targets

**Target.** If X has metric Markov type 2, every Lipschitz map from an arbitrary subset S⊆X to any real L1(μ) extends to X with Lipschitz constant at most `C M₂(X) Lip(f)`, for universal C. This includes Lp sources for finite p≥2 with their known O(√p) dependence.

**Route.** Family 332, `Metric-Markov-Cotype-Two-of-l1-October-5-2026`, proves metric Markov cotype 2 for ℓ1 and states a Hilbert-to-ℓ1 application. Its finite-cut construction extends pointwise and integrably to arbitrary L1(μ). Apply [Mendel–Naor's extension theorem](https://web.math.princeton.edu/~naor/homepage%20files/cat0-extension.pdf). Full extension uses the norm-one bidual projection for [L-embedded L1 spaces](https://page.mi.fu-berlin.de/werner99/mbuch/buch4.pdf).

**First package.** Write the finite-cut generalization and the finite-to-full extension argument, keeping constants and real/complex scope explicit. The independent audit found no additional central obstacle. Do not assume every L1 space is a dual, and do not claim arbitrary subspaces of L1 or noncommutative L1 targets.

**Assessment.** A broad endpoint theorem beyond the source's displayed application. [Detailed independent audit](agent_notes/nonlinear_maurey_independent_audit.md).

## 6. Commuting bilinear ergodic Hilbert transforms

**Target.** For arbitrary commuting invertible probability-preserving S,T and f,g∈L³, the symmetric sums

`H_N(f,g)(x) = Σ_(0<|n|≤N) f(Sⁿx)g(Tⁿx)/n`

converge almost everywhere and in L^(3/2). Prove the full r-variation bound for every r>2. Include the corresponding commuting-flow theorem if useful.

**Route.** Family 082, `Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026`, gives the needed Euclidean pointwise annular variation. A fixed-width cell embedding discretizes the kernel as `ℓ/n + O(n⁻²)` with ℓ bounded away from zero. The summable error is controlled by Hölder; finite-window Calderón transference then handles commuting actions.

**First package.** Prove this restriction lemma and transfer variation, limits and measurability. Two discipline reviewers accepted the mechanism. The recent [Becker–Durcik paper](https://arxiv.org/abs/2603.20173) treats powers of a single transformation, so its displayed theorem is not this arbitrary-commuting result.

**Assessment.** Strongest analysis application in this batch, with a concrete remaining lemma. This is an odd-kernel Hilbert theorem; ordinary one-sided commuting Cesàro averages do not follow. No noncommuting claim. [Route](agent_notes/geometry_analysis.md), [independent audit](agent_notes/physics_topology.md).

## 7. Ordinary Banach–Mazur rigidity of von Neumann algebras

**Target.** For every complex von Neumann algebra M, some ε_M>0 ensures that any other von Neumann algebra N with `d_BM(M,N)<1+ε_M` is Jordan *-isomorphic to M. Obtain the same conclusion from `d_BM(M_*,N_*)<1+ε_M` for their preduals.

**Route.** Family 295, `Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026`, supplies ordinary bounded `H²(M,M)=H³(M,M)=0`. These are exactly the hypotheses of [Roydor's conditional theorem](https://doi.org/10.1142/S1793525321500151), also stated as Theorem 2 in the [author's slides](https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf).

**First package.** Audit the published theorem and compose the implications. The indexed primary-author statement supports general M,N and both versions without separability or finiteness restrictions; direct PDF retrieval was blocked, so full proof inspection remains a publication-stage task. Small bounded associative multiplication perturbations provide a natural companion via established cohomological stability results.

**Assessment.** Broad rigidity with very little new proof work. Keep ε dependent on M, N a von Neumann algebra, and the conclusion Jordan *-isomorphism. The [completely bounded version](https://arxiv.org/abs/1108.1970) is already known and is not the new target. [Evidence](agent_notes/physics_topology.md).

## 8. C*-simplicity in the Thompson family

**Target.** Simplicity of the reduced group C*-algebras of F, T, Aut(F), and abstract Comm(F), with unique-trace consequences as appropriate.

**Route.** Family 248 supplies nonamenability of standard Thompson F. [Le Boudec–Matte Bon](https://arxiv.org/html/1605.01651), Corollaries 4.2 and 4.4, provide the exact equivalences. Their theorem also gives a broader countable circle-homeomorphism overgroup consequence under its specified standard embedding.

**First package.** State the theorem chain, structural consequences and exact group conventions. The independent reviewer checked the named groups and source consequences. No new C*-simplicity criterion appears necessary.

**Assessment.** Important specialist result, but overwhelmingly a consequence of the upstream nonamenability breakthrough and prior equivalences. Use reduced, not full, group C*-algebras; do not relabel already known C*-simplicity of V as new. [Independent audit](agent_notes/arithmetic_logic_adversarial.md).

## 9. Rational-point undecidability for smooth projective varieties

**Target.** No algorithm decides whether an arbitrary smooth projective geometrically integral variety over Q has a rational point. Dimension, degree and height are allowed to vary. A companion can rule out a computable uniform rational-point search-height bound for this class.

**Route.** Family 004 resolves Hilbert's tenth problem over Q negatively. [Poonen, Theorem 1.1(i)](https://math.mit.edu/~poonen/papers/chatelet.pdf), supplies an effective reduction from general rational-point existence to the regular projective geometrically integral case; over Q, regular is smooth. The [published abstract](https://ems.press/journals/jems/articles/1924) explicitly states this implication.

**First package.** Give the exact representation and decision model, apply the effective geometric construction, and establish any height/certificate consequences separately. Naive projective closure or resolution can create rational points and is not a substitute for the reduction.

**Assessment.** A striking geometric restriction of undecidability, yet the hard transfer is already published. No claim about fixed dimension, curves, surfaces, Fano varieties or a finite-point promise. [Evidence](agent_notes/arithmetic_logic.md).

## 10. The Sperner property for all graded Artinian complete intersections

**Target.** For every standard graded Artinian complete intersection A over a characteristic-zero field,

`max_(ideals I⊆A) μ_A(I) = max_j dim_k A_j`,

where μ_A(I) is the minimum number of ideal generators. The Hilbert function is determined by the defining regular-sequence degrees.

**Route.** Family 200 proves the Eisenbud–Green–Harris input. [Harima–Wachi–Watanabe](https://arxiv.org/abs/1601.06928), Theorem 11, prove EGH implies the Sperner property for complete intersections. Eliminate linear generators if necessary to match the source degree conventions.

**First package.** Verify the exact EGH scope, all-ideal versus graded-ideal reduction, and characteristic assumptions. Present a concise solution note with examples of the resulting ideal-generator bound.

**Assessment.** A significant named commutative-algebra consequence with a direct route. It does not prove weak or strong Lefschetz, nongraded statements or positive-characteristic analogues. [Evidence](agent_notes/algebra_groups.md).

## Selection and launch notes

Launch 1–3 first for substantive packages; 5–6 are strong parallel analysis streams. Items 4 and 7–10 are especially short theorem-chain consequences and carry substantial simultaneous-discovery and attribution risk. Their theorem importance must not be confused with the original contribution of a new note.

The next reserve is sharp Brenier stability for bounded positive log-concave nonuniform sources from family 374: the weighted midpoint mechanism passed an independent check, but density approximation and weighted differentiation need more work. Integral density for PGL character varieties and prescribed finite Lebesgue spectral multiplicities were also considered; their incremental contribution was weaker for this batch.

For every stream: validate the exact upstream theorem, refresh literature and companion-paper checks, write the complete argument, and seek fresh adversarial review before claiming resolution or priority. This agenda did not establish that any proposed result is first, did not launch separate research chats, and did not publish a theorem/preprint or mint a DOI. No external individuals were contacted.
